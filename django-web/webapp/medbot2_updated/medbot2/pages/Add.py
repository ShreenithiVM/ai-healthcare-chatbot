import streamlit as st
from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb+srv://shivani2311k:1234@cluster0.zv9ja.mongodb.net/") 
db = client["chatbot"] 
collection = db["details"] 

# @st.cache_resource
# def init_connection():
#     return pymongo.MongoClient(**st.secrets["mongo"])

# client = init_connection()


st.title("Appointment Registration", anchor=False)

with st.form("add_appointment"):
    name = st.text_input("Name")
    date = st.date_input("Date", datetime.now().date())
    # default_time = datetime.now().time().replace(microsecond=0)
    time = st.time_input("Time", value=None)
    description = st.text_area("Description")

    if st.form_submit_button("Submit"):
        patient_data = {
        "name": name,
        "date": str(date),
        "time": str(time), 
        "description": description
    }
        collection.insert_one(patient_data)

        st.success("submitted successfully!")