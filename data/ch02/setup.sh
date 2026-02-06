## Login
# az login
azd auth login

## Initialize the environment
azd init

azd env set COSMOS_URI https://<YOUR DATABASE HERE>.documents.azure.com:443/
azd env set COSMOS_KEY <YOUR KEY HERE>
azd env set COSMOS_DATABASE RealEstateCatalog
azd env set COSMOS_CONTAINER Properties


## Provision Azure resources
azd provision

## Deploy the Python App
azd deploy

## Get URL
azd deploy
