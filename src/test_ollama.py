from langchain_ollama import ChatOllama


# Connect LangChain to the local Ollama model
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


# Test the LLM
response = llm.invoke(
    "Explain what an AI agent is in one simple sentence."
)


print("\nLLM Response:")
print(response.content)