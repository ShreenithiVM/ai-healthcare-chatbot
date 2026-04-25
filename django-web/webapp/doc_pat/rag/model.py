from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
import os

# Load the document (text file with homeopathy knowledge)
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "homeopathy_data.txt")

try:
    loader = TextLoader(file_path)
    docs = loader.load()
except Exception as e:
    raise FileNotFoundError(f"Could not load the document: {e}")

# Create embeddings and vector store
embedding = HuggingFaceEmbeddings()
vectorstore = FAISS.from_documents(docs, embedding)

# Initialize the LLM
llm = OpenAI(temperature=0.2)

# Set up the Retrieval QA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

# Function to get a response using RAG
def get_rag_response(question: str) -> str:
    return qa_chain.run(question)
