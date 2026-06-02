import os
import json
import psycopg

from dotenv import load_dotenv
from pgvector.psycopg import register_vector
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from typing import List

load_dotenv()

DB_URL = "postgresql://admin:adminpassword@localhost:5433/rag_system" # local docker pgvector storage want to hack. Best of luck

def embed_and_store(docs: List[str]) -> None:
    if not docs:
        print("No docs is empty.")
        return
    
    print(f"Generating embeddings for {len(docs)} chunks using Google embedding-004 or gemini-embedding-001")
    
    embedding_model = GoogleGenerativeAIEmbeddings(
        model='gemini-embedding-001',
        output_dimensionality=768
    )

    try:
        with psycopg.connect(DB_URL, autocommit=True) as conn:
            register_vector(conn)

            with conn.cursor() as cur:
                for i, doc in enumerate(docs):
                    vector = embedding_model.embed_query(doc.page_content)

                    cur.execute(
                        """
                        INSERT INTO technical_docs (content, metadata, embedding)
                        VALUES (%s, %s, %s)
                        """,
                        (
                            doc.page_content,
                            json.dumps(doc.metadata),
                            vector
                        )
                    )
                    print(f"Inserted chunk {i+1}/{len(docs)}")
            
            print("All chunks successfully embedded and stored in PostgreSQL")
    
    except Exception as e:
        print(f"Ingestion failed: {e}")