# IF you came this page to run the code then u are an Idiot.
# Go to streamlit_app.py run that instructions are in ReadME.md check that first
# This file purpose is to initial stage backend 
# In "Future" i may deploy this in cloud with properly for now this much is Good  

from ingestion.pii_scrubber import load_docs, pii
from ingestion.chunking import chunk_raw_markdown
from retrieval.ingest import embed_and_store
from retrieval.search import hybrid_query
from retrieval.generate import generate_rag_response
from typing import List

def raw_to_storing_embedding() -> None:
    print("=="*50)
    print("PII SCRUBBER")
    print("=="*50)

    docs = load_docs()

    for i, doc in enumerate(docs):
        doc.page_content = pii(doc.page_content)

        print("==" * 50) # This is inspride by my teacher(Thai mam) not ChatGPT generated.
        print(f"Document {i+1}")
        # print(doc.page_content[:500])

    # print("=="*50)
    # print("Chunking Data")
    # print("=="*50)
    
    chunked_docs = chunk_raw_markdown(docs)
    for i, chunked_doc in enumerate(chunked_docs):
        print('--'*50)
        print(f'chunk {i+1}')
        # print(chunked_doc)
    
    embed_and_store(chunked_docs)

def test() -> None:
    docs = load_docs(['_index.md'])
    doc = docs[0]

    print("=="* 50)
    doc.page_content = pii(doc.page_content)
    print(doc.page_content)

    print("=="*50)
    chunked_docs = chunk_raw_markdown(docs)
    for i, chunk in enumerate(chunked_docs):
        print("--"*50)
        print(f"Chunk {i+1}")
        print(chunk)

    embed_and_store(chunked_docs)


def search_query(test_query: str = None, top_k: int = None) -> List[str]:
    if test_query == None:
        test_query = "How to handle Docker Compose SDK initialization in Go?"
    
    if top_k == None:
        top_k = 3

    print(f"Executing hybrid search for: '{test_query}'")
    hits = hybrid_query(test_query, top_k)

    for rank, hit in enumerate(hits):
        print("_"*150)
        print(f"[Rank {rank+1}] RRF Score: {hit['rrf_score']:.4f}")
        print(f"Source: {hit['metadata']['source']}")
        print(f"Content Snippet:\n{hit['content'][:200]}...")
        print()

    return hits

def gen_chat(user_query: str, hits: List[str]) -> None:
    llm_result = generate_rag_response(user_query, hits)

    print(f"Groq Reply: \n{llm_result}")

if __name__ == "__main__":
    user_query: str = "How to handle Docker Compose SDK initialization in Go?"
    top_k: int = 5

    hits = search_query(user_query, top_k)
    gen_chat(user_query, hits)