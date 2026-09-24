from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

PERSIST_DIRECTORY = "data/chroma"


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=embeddings
)

query = "What should we do when a seller has a high late-delivery rate?"

results = vector_store.similarity_search(query, k=3)

print("\nRAG Search Results:\n")

for i, document in enumerate(results, start=1):
    print(f"--- Result {i} ---")
    print(document.page_content)
    print()
    