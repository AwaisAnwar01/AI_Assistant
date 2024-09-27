import streamlit as st
import os
from document_parser import extract_text_from_pdf
from embedding_indexer import chunk_text, create_embeddings, index_embeddings
from retrieval import retrieve_relevant_chunks
from gpt_generator import generate_answer

from sentence_transformers import SentenceTransformer

# Initialize the sentence transformer model
model = SentenceTransformer('all-mpnet-base-v2')

# Streamlit UI
st.title("AI Assistant with RAG")
st.write("Upload a PDF file, ask a question, and get answers from the document and/or the web.")

# File upload widget
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Input query widget
query = st.text_input("Enter your question")

# Checkbox to enable web search
use_web_search = st.checkbox("Include web search results")

# Process the PDF and query when the button is clicked
if st.button("Submit Query"):
    if uploaded_file is not None and query:
        # Ensure the 'uploads/' directory exists
        uploads_dir = './uploads/'
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        # Save the uploaded file temporarily
        file_path = os.path.join(uploads_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.write("Extracting text from the PDF...")
        file_text = extract_text_from_pdf(file_path)
        
        # Step 1: Chunk the text and create embeddings
        st.write("Creating text chunks and embeddings...")
        text_chunks = chunk_text(file_text)
        embeddings = create_embeddings(text_chunks)
        
        # Step 2: Index embeddings with FAISS
        st.write("Indexing the embeddings...")
        index = index_embeddings(embeddings)
        
        # Step 3: Retrieve relevant document chunks based on the query
        st.write("Retrieving relevant chunks from the document...")
        relevant_chunks = retrieve_relevant_chunks(query, index, model, text_chunks, top_k=3)
        
       
        
        # Step 5: Combine relevant chunks and generate an answer
        context = "\n".join(relevant_chunks)
        st.write("Generating the answer using GPT-3...")
        answer = generate_answer(query, context)
        
        # Display the final answer
        st.subheader("Answer")
        st.write(answer)
        
    else:
        st.write("Please upload a PDF file and enter a query.")
