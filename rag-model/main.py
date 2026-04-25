import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Pinecone
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# Load environment variables from .env
load_dotenv()

class ChatBot():
    def __init__(self):
        # Load and split text documents
        loader = TextLoader('./horoscope.txt')
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=4)
        docs = text_splitter.split_documents(documents)

        # Initialize HuggingFace Embeddings with an explicit model name
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Fetch API keys
        pinecone_api_key = os.getenv('PINECONE_API_KEY')
        huggingface_api_key = os.getenv('HUGGINGFACE_API_KEY')

        if not pinecone_api_key or not huggingface_api_key:
            raise ValueError("Missing API keys. Please check .env file.")

        # Initialize Pinecone client
        pc = Pinecone(
            api_key=pinecone_api_key,
            environment="us-east1-gcp"
        )

        # Connect to the existing Pinecone index
        index_name = "my-index"  # Use the name of your manually created index
        index = pc.get_pinecone_index(index_name)

        # Use the index directly in Pinecone's vector store
        docsearch = Pinecone(
            index=index,
            embedding=embeddings,
            text_key="text"  # Adjust this if your text key is different
        )

        # Create retriever from Pinecone
        retriever = docsearch.as_retriever()  # Use the correct method to create a retriever

        # HuggingFace model setup
        repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        self.llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            model_kwargs={"temperature": 0.8, "top_k": 50},
            huggingfacehub_api_token=huggingface_api_key
        )

        # Define the prompt template
        template = """
        You are a fortune teller. These humans will ask you questions about their life.
        Use the following piece of context to answer the question.
        If you don't know the answer, just say you don't know.
        Keep the answer within 2 sentences and concise.

        Context: {context}
        Question: {question}
        Answer:
        """
        self.prompt = PromptTemplate(template=template, input_variables=["context", "question"])

        # Chain everything together
        self.rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def get_answer(self, question):
        return self.rag_chain.invoke({"question": question})

if __name__ == "__main__":
    bot = ChatBot()
    while True:
        user_input = input("\nAsk me anything (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        result = bot.get_answer(user_input)
        print("\n🔮 Fortune Teller Says: ", result)