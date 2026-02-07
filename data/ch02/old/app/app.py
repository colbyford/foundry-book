#!/usr/bin/env python3
"""
Azure Cosmos DB MCP Server (Foundry-Compatible)

Provides tools for querying and exploring Cosmos DB containers.
All optional parameters have defaults, and all outputs are structured JSON.
"""

import json
import logging
import os
import sys
from typing import Optional, List, Dict, Any
from azure.cosmos import CosmosClient, exceptions
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('cosmos-mcp-server')

__version__ = "0.3.0"


class CosmosDBConnection:
    """Manages the connection to Azure Cosmos DB."""
    def __init__(self, uri: str, key: str, database: str, container: str):
        self.uri = uri
        self.key = key
        self.database = database
        self.default_container = container
        self._client = None
        self._database_client = None

    def get_client(self) -> CosmosClient:
        if not self._client:
            self._client = CosmosClient(self.uri, credential=self.key)
            logger.info("Connected to Cosmos DB")
        return self._client

    def get_database_client(self):
        if not self._database_client:
            self._database_client = self.get_client().get_database_client(self.database)
        return self._database_client

    def get_container_client(self, container_name: Optional[str] = None):
        if not all([self.uri, self.key, self.database, self.default_container]):
            raise RuntimeError("Missing Cosmos DB connection parameters")
        container = container_name or self.default_container
        return self.get_database_client().get_container_client(container)


cosmos_connection: Optional[CosmosDBConnection] = None
mcp = FastMCP("Azure Cosmos DB Explorer", version=__version__)


# ------------------------------
# Core Tools
# ------------------------------

@mcp.tool()
def list_collections() -> dict:
    try:
        db_client = cosmos_connection.get_database_client()
        containers = list(db_client.list_containers())
        return {"containers": [c["id"] for c in containers]}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def query_cosmos(query: str) -> dict:
    try:
        container = cosmos_connection.get_container_client()
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return {"count": len(items), "items": items}
    except exceptions.CosmosHttpResponseError as e:
        return {"error": f"Cosmos DB error {e.status_code}: {e.message}"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def describe_container(container_name: Optional[str] = None) -> dict:
    try:
        container = cosmos_connection.get_container_client(container_name)
        items = list(container.query_items(query="SELECT * FROM c OFFSET 0 LIMIT 1",
                                           enable_cross_partition_query=True))
        if not items:
            return {"container": container_name or cosmos_connection.default_container, "fields": []}
        sample = items[0]
        fields = [{"name": k, "type": type(v).__name__} for k, v in sample.items()]
        return {"container": container_name or cosmos_connection.default_container, "fields": fields}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def count_documents(container_name: Optional[str] = None) -> dict:
    try:
        container = cosmos_connection.get_container_client(container_name)
        result = list(container.query_items(query="SELECT VALUE COUNT(1) FROM c",
                                            enable_cross_partition_query=True))
        count = result[0] if result else 0
        return {"container": container_name or cosmos_connection.default_container, "count": count}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_sample_documents(container_name: Optional[str] = None, limit: int = 5) -> dict:
    try:
        limit = max(1, min(limit, 100))
        container = cosmos_connection.get_container_client(container_name)
        query = f"SELECT * FROM c OFFSET 0 LIMIT {limit}"
        docs = list(container.query_items(query=query, enable_cross_partition_query=True))
        return {"container": container_name or cosmos_connection.default_container,
                "limit": limit,
                "documents": docs}
    except Exception as e:
        return {"error": str(e)}


# ------------------------------
# Advanced Tools
# ------------------------------

@mcp.tool()
def find_implied_links(container_name: Optional[str] = None) -> dict:
    """
    Detect relationship hints in a container by analyzing field name patterns.
    """
    try:
        container = cosmos_connection.get_container_client(container_name)
        items = list(container.query_items(query="SELECT * FROM c OFFSET 0 LIMIT 10",
                                           enable_cross_partition_query=True))
        if not items:
            return {"container": container_name or cosmos_connection.default_container,
                    "relationships": []}

        relationship_hints = set()
        id_fields = set()
        for doc in items:
            for key in doc:
                key_lower = key.lower()
                if key_lower.endswith(('_id', '_fk', '_ref', '_key')) and key_lower not in ('id', '_id'):
                    relationship_hints.add(key)
                if 'id' in key_lower:
                    id_fields.add(key)

        return {
            "container": container_name or cosmos_connection.default_container,
            "foreign_key_candidates": sorted(relationship_hints),
            "id_fields": sorted(id_fields)
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_partition_key_info(container_name: Optional[str] = None) -> dict:
    """Return partition key information for the container."""
    try:
        container = cosmos_connection.get_container_client(container_name)
        properties = container.read()
        partition_key = properties.get('partitionKey', {})
        paths = partition_key.get('paths', [])
        kind = partition_key.get('kind', 'Hash')
        return {
            "container": container_name or cosmos_connection.default_container,
            "paths": paths,
            "kind": kind
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_indexing_policy(container_name: Optional[str] = None) -> dict:
    """Return the indexing policy for the container."""
    try:
        container = cosmos_connection.get_container_client(container_name)
        properties = container.read()
        indexing_policy = properties.get('indexingPolicy', {})
        return {
            "container": container_name or cosmos_connection.default_container,
            "indexingPolicy": indexing_policy
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def list_distinct_values(field_name: str, container_name: Optional[str] = None) -> dict:
    """Return all unique values for a given field in the container."""
    try:
        container = cosmos_connection.get_container_client(container_name)
        query = f"SELECT DISTINCT VALUE c.{field_name} FROM c"
        values = list(container.query_items(query=query, enable_cross_partition_query=True))
        return {
            "container": container_name or cosmos_connection.default_container,
            "field": field_name,
            "distinct_values": values
        }
    except Exception as e:
        return {"error": str(e)}


# ------------------------------
# Server Initialization
# ------------------------------

def main():
    global cosmos_connection
    try:
        cosmos_connection = CosmosDBConnection(
            uri=os.getenv("COSMOS_URI"),
            key=os.getenv("COSMOS_KEY"),
            database=os.getenv("COSMOS_DATABASE"),
            container=os.getenv("COSMOS_CONTAINER")
        )
        # Test connection
        cosmos_connection.get_container_client()
        logger.info("Successfully connected to Cosmos DB")
    except Exception as e:
        logger.error(f"Failed to initialize Cosmos DB connection: {str(e)}")
        sys.exit(1)

    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting Azure Cosmos DB MCP server on port {port}...")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
