import psycopg
from pgvector.psycopg import register_vector
from langchain_google_genai import GoogleGenerativeAIEmbeddings

DB_URL = "postgresql://admin:adminpassword@localhost:5433/rag_system" # local docker pgvector storage want to hack. Best of luck

HYBRID_SEARCH_SQL = """
WITH vector_search AS (
    SELECT id, content, metadata,
           ROW_NUMBER() OVER (ORDER BY embedding <=> %s::vector) as rank
    FROM technical_docs
    ORDER BY embedding <=> %s::vector
    LIMIT 20
),
keyword_search AS (
    SELECT id, content, metadata,
           ROW_NUMBER() OVER (ORDER BY ts_rank_cd(fts_vector, plainto_tsquery('english', %s)) DESC) as rank
    FROM technical_docs
    WHERE fts_vector @@ plainto_tsquery('english', %s)
    ORDER BY ts_rank_cd(fts_vector, plainto_tsquery('english', %s)) DESC
    LIMIT 20
)
SELECT 
    COALESCE(v.id, k.id) as id,
    COALESCE(v.content, k.content) as content,
    COALESCE(v.metadata, k.metadata) as metadata,
    (COALESCE(1.0 / (60 + v.rank), 0.0) + COALESCE(1.0 / (60 + k.rank), 0.0)) as rrf_score
FROM vector_search v
FULL OUTER JOIN keyword_search k ON v.id = k.id
ORDER BY rrf_score DESC
LIMIT %s;
"""

def hybrid_query(query_text: str, top_k: int = 5):
    embedding_model = GoogleGenerativeAIEmbeddings(
        model='models/gemini-embedding-001',
        output_dimensionality=768
    )

    query_vector = embedding_model.embed_query(query_text)

    try:
        with psycopg.connect(DB_URL) as conn:
            register_vector(conn)
            with conn.cursor() as cur:
                cur.execute(
                    HYBRID_SEARCH_SQL,
                    (
                        query_vector,
                        query_vector,
                        query_text,
                        query_text,
                        query_text,
                        top_k
                    )
                )
                results = cur.fetchall()

                retrieved_chunks = []
                for row in results:
                    retrieved_chunks.append({
                        "id": row[0],
                        "content": row[1],
                        "metadata": row[2],
                        "rrf_score": float(row[3])
                    })
                    
                return retrieved_chunks

    except Exception as e:
        print(f"Retrieval query failed: {e}")
        return []