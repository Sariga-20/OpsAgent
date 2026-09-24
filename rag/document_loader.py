from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter


DOCUMENT_PATH = Path("documents/delivery_policy.txt")


def load_and_split_document():
    """
    Load the delivery policy and split it into
    clean section-based chunks.
    """

    text = DOCUMENT_PATH.read_text(
        encoding="utf-8"
    )

    splitter = RecursiveCharacterTextSplitter(
        separators=[
            "\n\n",
            "\n",
            ". ",
        ],
        chunk_size=700,
        chunk_overlap=0
    )

    chunks = splitter.create_documents([text])

    return chunks


if __name__ == "__main__":

    chunks = load_and_split_document()

    print("Number of chunks:", len(chunks))

    for i, chunk in enumerate(chunks, start=1):

        print(f"\n--- Chunk {i} ---")
        print(chunk.page_content)