import os
from autogen_ext.models.ollama import OllamaChatCompletionClient

# Configure Ollama server address
os.environ["OLLAMA_HOST"] = "http://hc4.isl.lab.nycu.edu.tw:11434"

# Create client (change model name if needed)
ollama_client = OllamaChatCompletionClient(
    model="llama3.2:latest",
    temperature=0.2
)

# Export the client for other files to use
__all__ = ["ollama_client"]
