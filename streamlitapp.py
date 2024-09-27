import streamlit as st
import os
import json
from datetime import datetime
from document_parser import parse_document
from embedding_indexer import chunk_text, create_embeddings, index_embeddings
from retrieval import retrieve_relevant_chunks
from gpt_generator import generate_answer
from sentence_transformers import SentenceTransformer

# Initialize the sentence transformer model
model = SentenceTransformer('all-mpnet-base-v2')

# Function to load chat history from a JSON file
def load_chat_history():
    if os.path.exists("chat_history.json"):
        with open("chat_history.json", "r") as f:
            return json.load(f)
    return []

# Function to save chat history to a JSON file
def save_chat_history(chat_history):
    with open("chat_history.json", "w") as f:
        json.dump(chat_history, f)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = load_chat_history()

# Function to update chat name after first query
def update_chat_name(chat):
    if "what" in chat["question"].lower():
        return f"Question about '{chat['question'][:50]}...'"
    elif chat["document_name"]:
        return f"Document Analysis for '{chat['document_name']}'"
    else:
        return f"Chat from {datetime.now().strftime('%Y-%m-%d %H:%M')}"

# Streamlit UI
st.title("AI Assistant with RAG")
st.write("Upload a document (PDF, DOCX, TXT, CSV, or image), ask a question, and get answers from the document and/or the web.")

# Sidebar to display chat history and start a new chat
with st.sidebar:
    st.title("Chat History")

    # Option to start a new chat
    new_chat_started = st.button("New Chat")

    # If a new chat is started, add a placeholder to chat history
    if new_chat_started:
        st.session_state.chat_history.append({
            "name": "New Chat",
            "question": "",
            "answer": "",
            "document_name": ""
        })
        save_chat_history(st.session_state.chat_history)
        st.experimental_rerun()  # Rerun to immediately reflect the new chat

    # If chat history exists, display only chat names in the sidebar
    selected_chat = None
    if st.session_state.chat_history:
        selected_chat = st.radio(
            "Select a Chat", 
            options=[chat["name"] for chat in st.session_state.chat_history]
        )

# File upload widget
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt", "csv", "jpg", "jpeg", "png"])

# Input query widget
query = st.text_input("Enter your question")

# Process the document and query when the input changes
if selected_chat and query:
    # Get the index of the selected chat in history
    chat_index = next((i for i, chat in enumerate(st.session_state.chat_history) if chat["name"] == selected_chat), None)
    
    if uploaded_file:
        # Ensure the 'uploads/' directory exists
        uploads_dir = './uploads/'
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        # Save the uploaded file temporarily
        file_path = os.path.join(uploads_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.write(f"Extracting text from the {uploaded_file.type} file...")
        
        # Use the unified document parsing function
        file_text = parse_document(file_path)

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
        
        # Step 4: Combine relevant chunks and generate an answer
        context = "\n".join(relevant_chunks)
        st.write("Generating the answer using GPT-3...")
        answer = generate_answer(query, context)

        # Save the question, answer, and document name in the selected chat
        st.session_state.chat_history[chat_index]["question"] = query
        st.session_state.chat_history[chat_index]["answer"] = answer
        st.session_state.chat_history[chat_index]["document_name"] = uploaded_file.name

    # Assign a more meaningful name to the chat after the first query
    st.session_state.chat_history[chat_index]["name"] = update_chat_name(st.session_state.chat_history[chat_index])

    save_chat_history(st.session_state.chat_history)  # Save to file

   

# Main section only displaying the selected chat (no automatic last chat display)
if selected_chat:
    # Find the selected chat by name
    for chat in st.session_state.chat_history:
        if chat["name"] == selected_chat:
            st.subheader(f"Chat: {chat['name']}")
            st.write(f"**Q:** {chat['question']}")
            st.write(f"**A:** {chat['answer']}")
