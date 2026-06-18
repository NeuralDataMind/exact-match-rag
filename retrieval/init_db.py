# Before Running this Create an PgSQL from docker file given for easy work or use local PgAdim4. If u are Rich then use cloud Storage.
# If u are not using the Docker PgSQL then change the password and DB_URL
# Check ReadME.md for more info... And IDH(I don't have -for Millennials) any ytc (youtube channel) But ih (i have) LinkedIn Go and like the post 

import psycopg
from pgvector.psycopg import register_vector

DB_URL = "postgresql://admin:adminpassword@localhost:5433/rag_system" # local docker pgvector storage want to hack. Best of luck

# Schema of the code is my own but written by Gemini-Pro
# I dont want to make typo errors in it 

SCHEMA_SQL = """
-- 1. Enable the vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create the updated table for Gemini (768 dimensions)
CREATE TABLE technical_docs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    metadata JSONB NOT NULL,
    embedding VECTOR(768), 
    fts_vector TSVECTOR GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
);

-- 3. Recreate the indexes
CREATE INDEX IF NOT EXISTS embedding_hnsw_idx ON technical_docs USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS fts_idx ON technical_docs USING GIN (fts_vector);
"""

def initialize_database():
    print("Connecting to PostgreSQL...")
    try:
        with psycopg.connect(DB_URL, autocommit=True) as conn:
            with conn.cursor() as cur:
                print("Executing schema update for Gemini (768 dimensions)...")
                cur.execute(SCHEMA_SQL)
            
            print("Registering pgvector extension with psycopg...")
            register_vector(conn)
                
        print("Database initialized successfully. Ready for Gemini vectors.")
    except Exception as e:
        print(f"Database connection failed: {e}")
    
if __name__ == "__main__":
    initialize_database()   
