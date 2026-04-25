import streamlit as st
from transformers import T5Tokenizer, T5ForConditionalGeneration
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
import re

# Download NLTK punkt tokenizer
import nltk
nltk.download('punkt_tab')

# Step 1: Load and chunk the knowledge base (text file)
def load_and_chunk_knowledge_base(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    # Split the text into chunks (e.g., paragraphs)
    chunks = text.split("\n\n")  # Adjust this based on how the text is structured
    return chunks

# Step 2: Implement BM25 for retrieval (Advanced)
def retrieve_with_bm25(question, chunks):
    # Tokenize the question and chunks
    question_tokens = word_tokenize(question.lower())
    chunk_tokens = [word_tokenize(chunk.lower()) for chunk in chunks]

    # Initialize BM25 model
    bm25 = BM25Okapi(chunk_tokens)

    # Get BM25 scores for each chunk based on the question
    scores = bm25.get_scores(question_tokens)
    
    # Find the chunk with the highest score
    best_chunk_index = scores.argmax()
    best_chunk = chunks[best_chunk_index]

    return best_chunk

# Step 3: Generate the answer using T5 model
def generate_answer(question, model, tokenizer, knowledge_base_chunks, method='bm25'):
    # Retrieve the relevant chunk using the chosen retrieval method
    if method == 'bm25':
        relevant_chunk = retrieve_with_bm25(question, knowledge_base_chunks)

    # Combine the question with the relevant chunk to generate the answer
    inputs = tokenizer.encode(question + " " + relevant_chunk, return_tensors="pt", truncation=True, padding=True)

    # Generate the answer
    outputs = model.generate(inputs, max_length=200, num_beams=4, early_stopping=True)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return answer

# Step 4: Streamlit app
def main():
    # Title of the app
    st.title("Breast Cancer Care Chatbot")

    # Load and chunk the knowledge base from the text file
    text_file_path = "homeopathy_data.txt"  # Make sure this file is in your working directory
    knowledge_base_chunks = load_and_chunk_knowledge_base(text_file_path)

    # Load the T5 model and tokenizer
    model_name = "t5-small"  # Use a larger model if needed
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    # User input for asking questions
    question = st.text_input("Ask a question related to Breast Cancer:")

    if question:
        # Generate the answer using the retrieval method of choice (e.g., 'bm25')
        answer = generate_answer(question, model, tokenizer, knowledge_base_chunks, method='bm25')
        st.write(f"Answer: {answer}")

if __name__ == "__main__":
    main()
