import chromadb
from chromadb.config import Settings
from datetime import datetime
import uuid

# Initialize ChromaDB client and collection
client = chromadb.Client(Settings(
    persist_directory="chroma_db",  # You can change this path
    anonymized_telemetry=False
))
collection = client.get_or_create_collection(name="book_chapters")

def add_to_chroma(rewritten_text, metadata):
    """
    Adds a rewritten chapter to ChromaDB with relevant metadata.
    """
    doc_id = f"chapter_{uuid.uuid4()}"
    collection.add(
        documents=[rewritten_text],
        metadatas=[metadata],
        ids=[doc_id]
    )
    print(f"✅ Chapter added to ChromaDB with ID: {doc_id}")

def search_similar(query_text, top_k=3):
    """
    Perform semantic search to find similar rewritten chapters.
    """
    results = collection.query(query_texts=[query_text], n_results=top_k)
    similar = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        similar.append({
            "text": doc,
            "metadata": meta
        })
    return similar

def get_next_version(url):
    """
    Determines the next version number for a given chapter URL.
    """
    # Search all documents related to the URL
    results = collection.get(
        include=['metadatas'],
    )

    # Filter entries by matching URL
    versions = [
        int(item["version"])
        for item in results["metadatas"]
        if item.get("url") == url and "version" in item
    ]
    
    next_version = max(versions) + 1 if versions else 1
    return next_version
