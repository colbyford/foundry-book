import openai
from foundry_local import FoundryLocalManager

## Pick a model.
## By using an alias, the most suitable model will be downloaded to your device.
alias = "qwen2.5-0.5b"

## Create a FoundryLocalManager instance, which will start the Foundry service
manager = FoundryLocalManager(alias)

## Use the OpenAI Python SDK to interact with the local model.
client = openai.OpenAI(
    base_url=manager.endpoint,
    api_key=manager.api_key  # API key is not required for local usage
)

## Generate a response
response = client.chat.completions.create(
    model=manager.get_model_info(alias).id,
    messages=[{"role": "user", "content": "Which O'Reilly book is the best for learning AI skills?"}]
)
print(response.choices[0].message.content)