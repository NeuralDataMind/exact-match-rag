## System Architecture & Aims

This repository is a fully decoupled Retrieval-Augmented Generation (RAG) pipeline built without bloated abstractions. It is engineered to solve the hallucination and precision limits of standard LLMs when querying complex technical documentation (specifically the Docker Compose SDK).

The architecture is driven by three core aims:

* **1. Absolute Accuracy (Zero Hallucinations):** The reasoning layer (Llama 3.3 70B via Groq) operates at strict `temperature=0.0`. It is explicitly constrained to synthesize answers only from injected database chunks, completely decoupling factual knowledge from the LLM's generative weights.
* **2. Pinpoint Retrieval (Hybrid Search):** Standard vector search fails on explicit code syntax. This system implements Reciprocal Rank Fusion (RRF) directly inside PostgreSQL to mathematically merge dense semantic embeddings (Gemini 768-dim) with sparse full-text keyword matching (BM25).
* **3. Production-Ready Developer Tooling:** Built as a raw, state-managed backend tool. The ingestion pipeline features automated PII scrubbing, structural markdown chunking, and Matryoshka vector truncation to optimize database memory overhead.