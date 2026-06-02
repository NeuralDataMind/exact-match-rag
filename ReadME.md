# Exact-Match RAG: Deterministic Document Interrogation Engine

A fully decoupled Retrieval-Augmented Generation (RAG) pipeline built without bloated abstractions. This system is engineered to solve the hallucination and precision limits of standard LLMs when querying complex technical documentation.

## System Architecture & Aims

The architecture abandons the standard "blind vector search" approach and is driven by three core aims:

1. **Absolute Accuracy (Zero Hallucinations):** The reasoning layer (Llama 3.3 70B via Groq) operates at strict `temperature=0.0`. It is explicitly constrained to synthesize answers only from injected database chunks, completely decoupling factual knowledge from the LLM's generative weights.
2. **Pinpoint Retrieval (Hybrid Search):** Standard semantic vector search fails on explicit code syntax. This system implements Reciprocal Rank Fusion (RRF) directly inside PostgreSQL to mathematically merge dense semantic embeddings (Gemini 768-dim) with sparse full-text keyword matching (BM25).
3. **Production-Ready Data Pipeline:** Built as a raw, state-managed backend tool. The ingestion pipeline features automated PII scrubbing, structural markdown chunking, and Matryoshka vector truncation to optimize database memory overhead.

## Tech Stack

* **Vector Database:** PostgreSQL with `pgvector` extension
* **Embedding Model:** Google `gemini-embedding-001` (Truncated to 768 dimensions via Matryoshka Representation Learning)
* **Inference Engine:** Groq (`llama-3.3-70b-versatile`)
* **Orchestration:** Python, LangChain (strictly for Document structuring)
* **Frontend:** Streamlit 

## Prerequisites

Before running this system, ensure you have the following installed:
* Docker & Docker Compose (for the local Postgres database)
* Python 3.10+
* Valid API keys for Google Gemini and Groq

## Environment Setup

1. Clone the repository:
```bash
   git clone [https://github.com/NeuralDataMind/exact-match-rag.git](https://github.com/NeuralDataMind/exact-match-rag.git)
   cd exact-match-rag

```

2. Create and activate a virtual environment:

```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate

```

3. Install dependencies:

```bash
   pip install -r requirements.txt

```

4. Configure environment variables:
Copy `.env.example` to `.env` and insert your exact credentials.

```bash
   cp .env.example .env

```

*Required Keys:*

* `GOOGLE_API_KEY`
* `GROQ_API_KEY`

## Execution Pipeline

### 1. Initialize the Vector Database

The PostgreSQL database runs locally via Docker on port 5433 to avoid host collisions.

```bash
cd Docker
docker compose up -d

```

### 2. Ingest Data

Run the ingestion pipeline. This process will parse the raw Markdown files in the `data/` directory, scrub PII, chunk the text, generate 768-dimensional embeddings via Google GenAI, and commit them to PostgreSQL.

```bash
python main.py

```

### 3. Launch the Application

Start the Streamlit interface to execute RRF hybrid queries against the database and generate deterministic technical responses.

```bash
streamlit run streamlit_app.py

```

## Repository Structure

* `/data` - Raw technical markdown files (Docker Compose SDK).
* `/Docker` - `docker-compose.yml` for PostgreSQL/pgvector initialization.
* `/ingestion` - Data loading, PII scrubbing, and chunking logic.
* `/retrieval` - Hybrid search (RRF) and Groq LLM generation logic.
* `main.py` - CLI entry point for testing and data ingestion.
* `streamlit_app.py` - Interactive frontend application.

```

### Your Next Action
Commit this file. Then confirm if you successfully bypassed the Git rejection error (using the force or merge command I gave you earlier) and pushed your code to GitHub.

```