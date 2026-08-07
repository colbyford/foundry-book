# pip install "azure-ai-projects>=2.0.0" 

import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

## Example: https://<account_name>.openai.azure.com
endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

## Example: gpt-5.4-mini
model_name = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]

with DefaultAzureCredential() as credential:
    with AIProjectClient(
      endpoint=endpoint,
      credential=credential
      ) as project_client:
        client = project_client.get_openai_client()

        ## Create a red team with built-in safety evaluators
        red_team = client.evals.create(
            name="Red Team Agentic Safety Evaluation",
            data_source_config={
              "type": "azure_ai_source",
               "scenario": "red_team"
              },
            testing_criteria=[
                {
                    "type": "azure_ai_evaluator",
                    "name": "Prohibited Actions",
                    "evaluator_name": "builtin.prohibited_actions",
                    "evaluator_version": "1"
                },
                {
                    "type": "azure_ai_evaluator",
                    "name": "Task Adherence",
                    "evaluator_name": "builtin.task_adherence",
                    "evaluator_version": "1",
                    "initialization_parameters": {
                      "deployment_name": model_name
                      },
                },
                {
                    "type": "azure_ai_evaluator",
                    "name": "Sensitive Data Leakage",
                    "evaluator_name": "builtin.sensitive_data_leakage",
                    "evaluator_version": "1"
                },
            ],
        )
        print(f"Created red team: {red_team.id}")