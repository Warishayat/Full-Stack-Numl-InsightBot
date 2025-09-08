from langchain_community.tools import Tool
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.agents import initialize_agent, AgentType
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
import warnings


warnings.filterwarnings('ignore')
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
Serp_key = os.getenv("SERPER_API_KEY")

embeddings = HuggingFaceEmbeddings()
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()


#retriver as a tool
def retriever_tool(query: str) -> str:
    docs = retriever.get_relevant_documents(query)
    if not docs:
        return "No relevant information found in the knowledge base."
    return "\n".join([doc.page_content for doc in docs])

search = GoogleSerperAPIWrapper(serper_api_key=Serp_key)

tools = [
    Tool(
        name="KnowledgeBase",
        func=retriever.get_relevant_documents,
        description="Useful for answering from NUML documents."
    )
]

reasoning_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    streaming=False
)

agent = initialize_agent(
    tools,
    reasoning_llm,
    agent="zero-shot-react-description",
    verbose=True
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def run_agent_with_buffer(user_query):
    agent_result = agent.run(user_query)
    memory.save_context({"input": user_query}, {"output": agent_result})
    final_llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()]
    )
    prompt = f"""
    You are a helpful assistant.
    The user asked: {user_query}
    Based on what was found: {agent_result}
    Considering previous conversation: {memory.load_memory_variables({})['chat_history']}
    Provide a clear, helpful final answer:
    """
    final_llm.predict(prompt)


if __name__ == "__main__":
    print(run_agent_with_buffer("Numl offer which courses?"))