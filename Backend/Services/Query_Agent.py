from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def load_faiss_index(index_path: str = "faiss_index"):
    """Load the FAISS index from local storage."""
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.load_local(index_path, embeddings,allow_dangerous_deserialization=True)
    return vectorstore

def query_index(vectorstore, query: str, k: int = 3):
    """Query the FAISS index and return the most relevant documents."""
    docs = vectorstore.similarity_search(query, k=k)
    return docs

#Testing
if __name__ == "__main__":
    vs = load_faiss_index("faiss_index")
    question = "which courses numl offer for software engineering?"
    results = query_index(vs, question)

    for i, doc in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(doc.page_content)
