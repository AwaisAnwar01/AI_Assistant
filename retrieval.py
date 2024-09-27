# app/retrieval.py

import numpy as np

def retrieve_relevant_chunks(query, index, model, chunks, top_k=3):
    """
    Retrieves the most relevant text chunks from the FAISS index.
    :param query: The user query.
    :param index: The FAISS index.
    :param model: The sentence transformer model.
    :param chunks: List of document text chunks.
    :param top_k: Number of top relevant chunks to retrieve.
    :return: List of most relevant chunks.
    """
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    return [chunks[i] for i in indices[0]]
