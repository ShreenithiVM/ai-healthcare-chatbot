from pymongo import MongoClient

client = MongoClient("mongodb+srv://shivani2311k:1234@cluster0.zv9ja.mongodb.net/")
db = client["chatbot"] 
collection = db["details"] 

collection.delete_one({'name': 'iyuotyiu'})

docs = collection.find()
for doc in docs:
    print(doc)