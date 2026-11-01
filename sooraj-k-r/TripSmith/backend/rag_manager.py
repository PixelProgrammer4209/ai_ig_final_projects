# backend/rag_manager.py
import os
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

class RAGManager:
    def __init__(self, db_path="./chroma_db", data_folder="./data"):
        self.data_folder = data_folder
        
        # 1. Initialize Persistent ChromaDB
        # Persistent means the database is saved to a folder on your hard drive, 
        # so we don't lose data when the server restarts.
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Create or load a "table" (collection) for our tourism data
        self.collection = self.client.get_or_create_collection(name="kerala_tourism")
        
        # 2. Load the Sentence Transformer model
        # all-MiniLM-L6-v2 is a fast, lightweight, and highly popular embedding model.
        print("Loading Sentence Transformer model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded.")

    def chunk_text(self, text, chunk_size=200):
        """Splits long text into smaller paragraphs/chunks."""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks

    def process_and_store_documents(self):
        """Reads all PDFs and TXT files in the data folder and stores them in ChromaDB."""
        if not os.path.exists(self.data_folder):
            print(f"Data folder '{self.data_folder}' not found.")
            return

        for filename in os.listdir(self.data_folder):
            file_path = os.path.join(self.data_folder, filename)
            text = ""

            # Extract text based on file type
            if filename.endswith(".pdf"):
                reader = PdfReader(file_path)
                for page in reader.pages:
                    text += page.extract_text() + " "
            elif filename.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            else:
                continue

            if not text.strip():
                continue

            print(f"Processing {filename}...")
            
            # Chunk the text
            chunks = self.chunk_text(text)
            
            # Generate embeddings (turning text into numbers)
            embeddings = self.embedding_model.encode(chunks).tolist()
            
            # Generate unique IDs for each chunk
            ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
            
            # Store in ChromaDB
            self.collection.add(
                documents=chunks,
                embeddings=embeddings,
                ids=ids
            )
        print("All documents processed and stored in ChromaDB!")

    def query(self, search_text, n_results=2):
        """Searches the database for the most relevant information."""
        # Convert the search query into numbers using the exact same model
        query_embedding = self.embedding_model.encode([search_text]).tolist()
        
        # Search the database for the closest mathematical matches
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        # Return the actual text documents found
        if results['documents']:
            return results['documents'][0]
        return []