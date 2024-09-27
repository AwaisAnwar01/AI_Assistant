# app/embedding_indexer.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-mpnet-base-v2')

def chunk_text(text, chunk_size=200):
    """
    Splits the text into chunks of a given size.
    :param text: The input text.
    :param chunk_size: Number of words per chunk.
    :return: List of text chunks.
    """
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def create_embeddings(text_chunks):
    """
    Converts text chunks into embeddings using Sentence Transformers.
    :param text_chunks: List of text chunks.
    :return: Numpy array of embeddings.
    """
    embeddings = model.encode(text_chunks)
    return embeddings

def index_embeddings(embeddings):
    """
    Indexes the embeddings using FAISS.
    :param embeddings: Numpy array of embeddings.
    :return: FAISS index.
    """
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index
