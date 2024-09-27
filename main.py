# app/main.py


from document_parser import extract_text_from_pdf
from embedding_indexer import chunk_text, create_embeddings, index_embeddings
from retrieval import retrieve_relevant_chunks
from gpt_generator import generate_answer
from sentence_transformers import SentenceTransformer


def process_pdf_query(file_path, query, use_web_search=False):
    # Step 1: Parse the PDF file
    print("Extracting text from PDF...")
    file_text = extract_text_from_pdf(file_path)
    
    # Step 2: Chunk the text and create embeddings
    print("Creating text chunks and embeddings...")
    text_chunks = chunk_text(file_text)
    embeddings = create_embeddings(text_chunks)
    
    # Step 3: Index embeddings with FAISS
    print("Indexing the embeddings...")
    index = index_embeddings(embeddings)
    
    # Step 4: Retrieve relevant chunks from the document
    print("Retrieving relevant document chunks...")
    relevant_chunks = retrieve_relevant_chunks(query, index, model=SentenceTransformer('all-mpnet-base-v2'), chunks=text_chunks, top_k=3)
    
    
    
    # Step 6: Combine relevant chunks into context and generate an answer
    context = "\n".join(relevant_chunks)
    print("Generating the answer using GPT-3...")
    answer = generate_answer(query, context)
    
    print("Answer:")
    print(answer)


if __name__ == '__main__':
    # Replace this with the path to your PDF and the query
    file_path = './uploads/biology_paper.pdf'
    query = "What is the function of DNA?"
    
    # Run the process with the uploaded PDF and query
    process_pdf_query(file_path, query, use_web_search=False)
