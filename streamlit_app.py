# Majority design made by Claude sonnet 4.6 LOW on thinking mode
# Finished by Gemini-Pro why idh(i don't have) claude paid verison
# Dont press run button to run this use cmd = "streamlit run streamlit_app.py" in terminal few guys commented in my linkedIn it wont work(Idiots)
# To stop Control + C in terminal (windows) rest, Ask ChatGPT
# If u came then give a star to project it is "FREE"  

import html
import streamlit as st

from main import search_query
from retrieval.generate import generate_rag_response


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DocBot",
    page_icon="⬡",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Sora:wght@300;400;500;600&display=swap');

:root {
    --bg:          #0d0f14;
    --surface:     #141720;
    --surface2:    #1c2030;
    --border:      #252a3a;
    --accent:      #00e5c3;
    --accent2:     #5b8aff;
    --text:        #e2e8f7;
    --text-dim:    #6b7a99;
    --user-bubble: #1a2240;
    --bot-bubble:  #111827;
    --radius:      14px;
    --font-ui:     'Sora', sans-serif;
    --font-mono:   'IBM Plex Mono', monospace;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-ui) !important;
}

[data-testid="stHeader"],
[data-testid="stDecoration"],
[data-testid="stToolbar"] {
    display: none;
}

footer {
    display: none !important;
}

::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: var(--bg);
}

::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 4px;
}

[data-testid="stMain"] > div {
    padding-top: 0 !important;
}


/* ── Header ── */
.chat-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 22px 0 18px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 28px;
}

.chat-header-icon {
    width: 42px;
    height: 42px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: 0 0 20px rgba(0,229,195,0.25);
}

.chat-header-title {
    font-size: 1.2rem;
    font-weight: 600;
    letter-spacing: -0.02em;
}

.chat-header-sub {
    font-size: 0.72rem;
    color: var(--text-dim);
    font-family: var(--font-mono);
    margin-top: 2px;
}

.status-dot {
    width: 7px;
    height: 7px;
    background: var(--accent);
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
    box-shadow: 0 0 6px var(--accent);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: .4; }
}


/* ── Bubbles ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 4px 0 !important;
}

[data-testid="stChatMessageContent"] {
    font-size: 0.92rem;
    line-height: 1.65;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    flex-direction: row-reverse !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
    background: var(--user-bubble) !important;
    border: 1px solid rgba(91,138,255,0.3) !important;
    border-radius: var(--radius) var(--radius) 4px var(--radius) !important;
    padding: 12px 16px !important;
    color: var(--text) !important;
    margin-left: auto;
    max-width: 80%;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"] {
    background: var(--bot-bubble) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) var(--radius) var(--radius) 4px !important;
    padding: 14px 18px !important;
    color: var(--text) !important;
    max-width: 90%;
}

[data-testid="chatAvatarIcon-user"] > div,
[data-testid="chatAvatarIcon-assistant"] > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--accent) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
}

[data-testid="chatAvatarIcon-assistant"] > div {
    color: var(--accent2) !important;
}


/* ── Code ── */
code {
    font-family: var(--font-mono) !important;
    background: var(--surface2) !important;
    color: var(--accent) !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    font-size: 0.83em !important;
}

pre code {
    background: transparent !important;
    padding: 0 !important;
}

pre {
    background: #0a0c10 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 14px !important;
    overflow-x: auto !important;
}


/* ══════════════════════════════════════════════════
   RETRIEVAL CONTEXT DRAWER
   ══════════════════════════════════════════════════ */

[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    margin: 8px 0 12px !important;
}

[data-testid="stExpander"] summary {
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    color: var(--text-dim) !important;
    padding: 8px 12px !important;
}

[data-testid="stExpander"] summary:hover {
    color: var(--text) !important;
}

[data-testid="stExpander"] > div > div {
    padding: 8px 12px 12px !important;
}

.chunk-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 11px 14px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}

.chunk-card:hover {
    border-color: rgba(91,138,255,0.45);
}

.chunk-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 7px;
    flex-wrap: wrap;
}

.rank-badge {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 2px 8px;
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--accent2);
    font-weight: 500;
    white-space: nowrap;
}

.rrf-badge {
    background: rgba(0,229,195,0.07);
    border: 1px solid rgba(0,229,195,0.2);
    border-radius: 6px;
    padding: 2px 8px;
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--accent);
    white-space: nowrap;
}

.src-badge {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2px 9px;
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-dim);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 260px;
}

.chunk-snippet {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: #8896b3;
    line-height: 1.6;
    border-left: 2px solid var(--border);
    padding-left: 10px;
    margin: 0;
    white-space: pre-wrap;
    word-break: break-word;
}


/* ── Chat input ── */
[data-testid="stChatInput"] {
    border-top: 1px solid var(--border) !important;
    padding-top: 16px !important;
    background: var(--bg) !important;
}

[data-testid="stChatInput"] > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    transition: border-color .2s, box-shadow .2s;
}

[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,229,195,.08) !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text) !important;
    font-family: var(--font-ui) !important;
    font-size: 0.9rem !important;
    caret-color: var(--accent) !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-dim) !important;
}

[data-testid="stChatInput"] button {
    background: var(--accent) !important;
    border-radius: 8px !important;
    color: #0d0f14 !important;
}

[data-testid="stChatInput"] button:hover {
    background: var(--accent2) !important;
    box-shadow: 0 0 10px rgba(91,138,255,.4) !important;
}


/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

[data-testid="stSidebar"] label {
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    color: var(--text-dim) !important;
    text-transform: uppercase;
    letter-spacing: .06em;
}

[data-testid="stSidebar"] .stButton > button {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
    font-size: .78rem !important;
    width: 100%;
    transition: border-color .2s;
}

[data-testid="stSidebar"] .stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}


/* ── Welcome card ── */
.welcome-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px 36px;
    text-align: center;
    margin: 24px 0 32px;
}

.welcome-card h2 {
    font-size: 1.4rem;
    font-weight: 600;
    letter-spacing: -.02em;
    margin-bottom: 8px;
}

.welcome-card p {
    color: var(--text-dim);
    font-size: .88rem;
    line-height: 1.6;
    max-width: 420px;
    margin: 0 auto 20px;
}

.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 16px;
}

.chip {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 13px;
    font-size: .78rem;
    font-family: var(--font-mono);
    color: var(--text-dim);
    cursor: default;
}

.chip span {
    color: var(--accent);
    margin-right: 5px;
}


/* ── Thinking dots ── */
.thinking {
    display: flex;
    gap: 5px;
    align-items: center;
    padding: 4px 0;
}

.thinking span {
    width: 6px;
    height: 6px;
    background: var(--accent);
    border-radius: 50%;
    animation: bounce 1.2s infinite;
    opacity: .7;
}

.thinking span:nth-child(2) {
    animation-delay: .2s;
}

.thinking span:nth-child(3) {
    animation-delay: .4s;
}

@keyframes bounce {
    0%, 80%, 100% {
        transform: translateY(0);
        opacity: .4;
    }

    40% {
        transform: translateY(-6px);
        opacity: 1;
    }
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render retrieval context drawer ─────────────────────────────────────
def render_retrieval_drawer(hits: list, key: str) -> None:
    """
    Shows the chunks retrieved by search_query().

    This is NOT model thinking.
    This is the retrieval evidence/context used before generating the answer.
    """

    if not hits:
        return

    n_chunks = len(hits)

    n_sources = len(set(
        hit.get("metadata", {}).get("source", "unknown")
        for hit in hits
    ))

    with st.expander(
        f"▾ Show retrieval context · {n_chunks} chunks · {n_sources} source{'s' if n_sources != 1 else ''}",
        expanded=False
    ):
        for rank, hit in enumerate(hits, start=1):
            metadata = hit.get("metadata", {})
            source = metadata.get("source", "unknown")
            rrf_score = hit.get("rrf_score", 0)
            content = hit.get("content", "")

            snippet = content[:500]
            if len(content) > 500:
                snippet += "..."

            safe_source = html.escape(str(source))
            safe_snippet = html.escape(str(snippet))

            st.markdown(f"""
<div class="chunk-card">
    <div class="chunk-header">
        <span class="rank-badge">Rank {rank}</span>
        <span class="rrf-badge">RRF {rrf_score:.4f}</span>
        <span class="src-badge">◈ {safe_source}</span>
    </div>
    <pre class="chunk-snippet">{safe_snippet}</pre>
</div>
""", unsafe_allow_html=True)


# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:18px 0 10px;'>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:0.7rem;
                    color:#6b7a99;letter-spacing:.1em;text-transform:uppercase;
                    margin-bottom:18px;'>⬡ DocBot Settings</div>
    </div>
    """, unsafe_allow_html=True)

    top_k = st.slider(
        "TOP_K  (chunks retrieved)",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        help="Number of document chunks retrieved per query",
    )

    st.markdown("""
    <div style='margin:20px 0 8px;font-family:IBM Plex Mono,monospace;
                font-size:0.7rem;color:#6b7a99;letter-spacing:.08em;
                text-transform:uppercase;'>Session</div>
    """, unsafe_allow_html=True)

    if st.button("🗑  Clear chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
    <div style='margin-top:32px;padding:14px;background:#141720;border:1px solid #252a3a;
                border-radius:10px;font-family:"IBM Plex Mono",monospace;font-size:0.7rem;
                color:#6b7a99;line-height:1.7;'>
        <div style='color:#e2e8f7;font-weight:500;margin-bottom:6px;'>Pipeline</div>
        <div>① hybrid_query</div>
        <div>② rerank (RRF)</div>
        <div>③ generate_rag_response</div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state ───────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
    <div class="chat-header-icon">⬡</div>
    <div>
        <div class="chat-header-title">DocBot</div>
        <div class="chat-header-sub">
            <span class="status-dot"></span>RAG · hybrid search · Groq LLM
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Welcome card ───────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <h2>Ask your docs anything</h2>
        <p>
            Powered by hybrid semantic search and retrieval-augmented generation.
            Queries are matched against your embedded knowledge base in real-time.
        </p>
        <div class="chip-row">
            <div class="chip"><span>⬡</span>Docker Compose SDK</div>
            <div class="chip"><span>⬡</span>Go initialization</div>
            <div class="chip"><span>⬡</span>API reference</div>
            <div class="chip"><span>⬡</span>Configuration</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Render chat history ────────────────────────────────────────────────────────
for idx, msg in enumerate(st.session_state.messages):
    role = msg.get("role", "assistant")

    avatar = "👤" if role == "user" else "🤖"

    with st.chat_message(role, avatar=avatar):
        if role == "assistant" and msg.get("chunks"):
            render_retrieval_drawer(msg["chunks"], key=f"hist_{idx}")

        st.markdown(msg.get("content", ""))


# ── Chat input ─────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Ask something about your docs…"):

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
    })

    # Render user message immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant", avatar="🤖"):

        thinking_slot = st.empty()

        thinking_slot.markdown(
            """
            <div class="thinking">
                <span></span>
                <span></span>
                <span></span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            # Retrieval
            hits = search_query(user_input, top_k)

            # Generation
            answer = generate_rag_response(user_input, hits)

        except Exception as e:
            thinking_slot.empty()

            hits = []
            answer = f"""
Something failed while processing your query.

```text
{type(e).__name__}: {e}
```
"""
            st.error(answer)

        else:
            thinking_slot.empty()

            # Show retrieval context before answer
            render_retrieval_drawer(
                hits,
                key=f"new_{len(st.session_state.messages)}"
            )

            # Show final answer
            st.markdown(answer)

        # Save assistant message with chunks
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "chunks": hits,
        })