from langchain.tools import tool
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


@tool
def search_delivery_policy(query: str) -> str:
    """
    Search the delivery operations policy and return
    the most relevant policy sections.
    """

    results = vector_store.similarity_search(
        query,
        k=2
    )

    if not results:
        return "No relevant delivery policy information was found."

    policy_sections = []

    for document in results:

        text = document.page_content.strip()

        if text and text not in policy_sections:
            policy_sections.append(text)

    policy_context = "\n\n".join(
        policy_sections
    )

    return f"""
DELIVERY POLICY — RETRIEVED EVIDENCE

{policy_context}

IMPORTANT:
Use only the policy statements contained above.
Do not invent additional policy rules.
If the retrieved policy does not answer something,
state that the policy does not specify it.
"""


if __name__ == "__main__":

    query = (
        "seller late delivery history "
        "high risk orders operational actions "
        "human approval"
    )

    result = search_delivery_policy.invoke(
        {"query": query}
    )

    print(
        "\n========== DELIVERY POLICY ==========\n"
    )

    print(result)