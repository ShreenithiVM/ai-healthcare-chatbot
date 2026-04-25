import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.title("Appointment Dashboard", anchor=False)

client = MongoClient("mongodb+srv://shivani2311k:1234@cluster0.zv9ja.mongodb.net/") 
db = client["chatbot"] 
collection = db["details"] 

docs = [ doc for doc in collection.find()]

df = pd.DataFrame.from_records(docs)

st.dataframe(df,
             width=1000)

st.button("re-run")
