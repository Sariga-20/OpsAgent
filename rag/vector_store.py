from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from rag.document_loader import load_and_split_document


PERSIST_DIRECTORY = "data/chroma"


def create_vector_store():

    documents = load_and_split_document()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )

    return vector_store


if __name__ == "__main__":

    vector_store = create_vector_store()

    print("Vector database created successfully!")
    print("Stored documents:", vector_store._collection.count())