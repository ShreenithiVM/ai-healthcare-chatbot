from langchain_community.tools import tool
from langchain_groq import ChatGroq
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.agents import Tool
from langchain.tools.base import StructuredTool
# from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_experimental.utilities import PythonREPL
from pymongo import MongoClient
from utils.prompts import create_template, fetch_template, update_template

llm = ChatGroq(
    model="llama3-70b-8192",  
    temperature=0.0,
)

client = MongoClient("mongodb+srv://shivani2311k:1234@cluster0.zv9ja.mongodb.net/")
db = client["chatbot"] 
collection = db["details"] 

def create_appointment(name: str, date: str, time: str, description: str, **kwargs):
    """ Creates a MongoDB document with the following fields:
        - name: string (the name of the patient)
        - date: string (the date of the appointment in YYYY-MM-DD format)
        - time: string (the time of the appointment in HH:MM format)
        - description: string (a brief description of the appointment)
    """
    #    create_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(create_template))
    #    res = create_chain.invoke(details)
    client = MongoClient("mongodb+srv://shivani2311k:1234@cluster0.zv9ja.mongodb.net/")
    db = client["chatbot"] 
    collection = db["details"] 
    collection.insert_one({
            "name": f"{name}",
            "date": f"{date}",
            "time": f"{time}",
            "description": f"{description}"
    })
    return "Document creation and insertion successful."

def fetch_document(query: dict):
    """ Fetches the relevant appointment records based on a query. The query should include atleast one of the following fields:
        - name: string (the name of the patient, if specified)
        - date: string (the date of the appointment in YYYY-MM-DD format, if specified)
        - time: string (the time of the appointment in HH:MM format, if specified)
        - description: string (a brief description of the appointment, if specified)

        For example:
        To fetch a document using the name "joe" the following query is used:
        {"name" : "joe"}

        NOTE: All the value should be in lowercase.
    """
    client = MongoClient("mongodb+srv://shivani2311k:1234@cluster0.zv9ja.mongodb.net/")
    db = client["chatbot"] 
    collection = db["details"] 
    print(query)
    docs = [doc for doc in collection.find(dict(query))]
    return str(docs)

def delete_document(filter: dict):
    """ Removes the relevant appointment records based on a delete query. The query should include:
        - A filter to identify which document(s) to delete (e.g., by name, date, or other criteria).

        Respond with the delete query in JSON format, for example:
        {
        "filter": { "name": "john doe", "date": "2024-09-15" }
        }

        NOTE: All the value should be in lowercase.
    """
    client = MongoClient("mongodb+srv://shivani2311k:1234@cluster0.zv9ja.mongodb.net/")
    db = client["chatbot"] 
    collection = db["details"] 
    print(filter)
    collection.delete_many(dict(filter))
    return "Document deletion successful."

def update_document(filter: dict, update: dict):
    """ Modifies the relevant appointment records based on a query. The query should include:
        - A filter to identify which document(s) to update (e.g., by name, date, or other criteria).
        - The fields to be updated along with their new values.

        Respond with the update query in JSON format, for example:
        {{
        "filter": { "name": "John Doe", "date": "2024-09-15" },
        "update": { "$set": { "time": "15:00", "description": "Updated routine check-up" } }
        }}

        Make sure the query is valid and reflects the changes specified in the user message.

        NOTE: All the value should be in lowercase.
    """
    client = MongoClient("mongodb+srv://shivani2311k:1234@cluster0.zv9ja.mongodb.net/")
    db = client["chatbot"] 
    collection = db["details"] 
    # print(query)
    collection.update_one(dict(filter), dict(update))
    return "Document updation successful."


create_tool = StructuredTool.from_function(
    func=create_appointment
)

fetch_tool = StructuredTool.from_function(
    func=fetch_document
)

update_tool = StructuredTool.from_function(
    func=update_document
)

delete_tool = StructuredTool.from_function(
    func=delete_document
)

# python_tool = PythonREPLTool()

python_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=PythonREPL().run,
)