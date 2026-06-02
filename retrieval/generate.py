# model = "llama-3.3-70b-versatile" by META u can download and run locally also an option then u dont need Groq API key (Groq is Fast)
# RAG_SYSTEM_PROMPT gen by Gemini-pro verified by human 

import os
from typing import List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

RAG_SYSTEM_PROMPT = """
You are a precise, technical system assistant tasked with answering user questions using only the verified documentation context blocks provided below.

CRITICAL INSTRUCTIONS:
1. Base your answer strictly on the provided context chunks. If the context does not contain enough information to answer, state clearly that the information is unavailable in the current documentation.
2. Maintain high technical accuracy. Do not alter package names, variables, syntax, or initialization steps.
3. If code blocks are available in the context, output them cleanly using proper formatting.
"""

RAG_USER_TEMPLATE = """
CONTEXT CHUNKS:
{context_text}

USER QUESTION: 
{query}

TECHNICAL ANSWER:
"""

def generate_rag_response(user_query: str, retrieved_chunks: List[str]) -> List[str]:
    print(f"Retrieving candidate documents for: '{user_query}'...")

    if not retrieved_chunks:
        return "System Error: No relevant context could be found in the vector database."
    
    context_segments = []
    for idx, chunk in enumerate(retrieved_chunks):
        formatted_chunk = f"--- Chunk {idx+1} (Source: {chunk['metadata'].get('source', 'Unknow')}) ---\n{chunk['content']}"
        context_segments.append(formatted_chunk)
    
    compile_context = "\n\n".join(context_segments)

    print("Invoking gen model for localized response synthesis...")
    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.0
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", RAG_SYSTEM_PROMPT),
            ("human", RAG_USER_TEMPLATE)
        ])

        chain = prompt | llm # The | symbol is the pipe operator lot fellows don't know
        response = chain.invoke({
            "context_text": compile_context,
            "query": user_query
        })

        return response.content
    except Exception as e:
        return f"Groq Generation Failed: {e}"
    
