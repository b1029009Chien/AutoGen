from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
import asyncio

async def main():
    # Create an Ollama model client pointing to your local instance
    model_client = OllamaChatCompletionClient(
        model="qwen:1.8b", 
        base_url="http://localhost:11434"
    )

    # Create an assistant agent using the Ollama client
    agent = AssistantAgent(
        name="weather_presenter",
        model_client=model_client,
        system_message="You are a weather presenter."
    )

    # Run the task
    response = await agent.run(
        task="What is the weather in Hong Kong today?"
    )

    print(response)

    await model_client.close()

# Run the async main function
asyncio.run(main())
