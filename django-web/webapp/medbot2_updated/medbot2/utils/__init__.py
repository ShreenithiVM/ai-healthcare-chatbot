from pymongo import MongoClient
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

client = MongoClient("mongodb+srv://shivani2311k:1234@cluster0.zv9ja.mongodb.net/")
db = client["chatbot"] 
collection = db["details"] 

documents = [doc for doc in collection.find()]


