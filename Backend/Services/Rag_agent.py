from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()

def build_faiss_index(
    file_path: str,
    index_path: str = "faiss_index",
    chunk_size: int = 1000,
    chunk_overlap: int = 100
):
    """
    Builds a FAISS vector index from a text file and saves it locally.

    Args:
        file_path (str): Path to the text/markdown file.
        index_path (str): Directory name to save FAISS index. Default = "faiss_index".
        chunk_size (int): Maximum number of characters per chunk. Default = 1000.
        chunk_overlap (int): Overlap between chunks. Default = 100.

    Returns:
        str: Path to the saved FAISS index.
    """

    print("load the file")
    loader = TextLoader(file_path, encoding="utf-8")
    docs = loader.load()
    print("Document is loaded.")
    
    print("Documents are converted into chunks and overlap.")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(docs)
    print("Converted to Chunks")
    

    print("Embeddings the documents")
    embeddings = HuggingFaceEmbeddings()

    print("Creating the vector store")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    print("Save the vectorstore local..")
    vectorstore.save_local(index_path)
    print(f"FAISS index saved at: {index_path}")

    print("All done")
    return index_path


#test
if __name__ == "__main__":
    file_path = r"C:\Users\HP\Desktop\Numl-Saas-Chatbot\Full-Stack-Numl-InsightBot\Backend\Services\all_text.md"
    build_faiss_index(file_path)
