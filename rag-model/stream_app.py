import faiss
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load pre-trained models
st.title("Retrieval-Augmented Generation (RAG) Model")

# Step 1: Load and preprocess text file
text_file = st.file_uploader("horoscope.txt", type=["txt"])

if text_file is not None:
    # Read text from uploaded file
    document = text_file.read().decode("utf-8").splitlines()

    # Step 2: Initialize the Sentence-Transformer for embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Create embeddings for each paragraph in the document
    embeddings = model.encode(document)

    # Step 3: Create a FAISS index for fast similarity search
    embeddings = np.array(embeddings).astype(np.float32)
    index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 distance metric
    index.add(embeddings)  # Add embeddings to the index

    # Step 4: Load the T5 model and tokenizer
    generator_model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')

    # Step 5: Function to retrieve relevant passages
    def retrieve_passages(query, k=3):
        query_embedding = model.encode([query]).astype(np.float32)
        D, I = index.search(query_embedding, k)  # Search for top-k passages
        return [document[i] for i in I[0]]  # Return top-k passages

    # Step 6: Function to generate an answer based on retrieved passages
    def generate_answer(query, retrieved_passages):
        # Combine question with retrieved passages
        context = " ".join(retrieved_passages)
        input_text = f"question: {query} context: {context}"

        # Tokenize and generate the answer
        inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
        summary_ids = generator_model.generate(inputs['input_ids'], max_length=150, num_beams=3, early_stopping=True)
        answer = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return answer

    # Step 7: User input for question
    query = st.text_input("Ask a question")

    if query:
        # Retrieve relevant passages from the document
        retrieved_passages = retrieve_passages(query)
        
        # Generate an answer based on retrieved passages
        answer = generate_answer(query, retrieved_passages)
        
        # Display the answer
        st.write(f"**Answer:** {answer}")

    else:
        st.write("Please ask a question to get an answer.")
