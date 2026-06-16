import streamlit as st

# -----------------------------
# Simple In-Memory RAG
# -----------------------------
DOCUMENTS = [
    "Multi-agent orchestration coordinates multiple AI agents.",
    "Agents can specialize in planning, research, coding, or analysis.",
    "A coordinator agent manages task delegation and integration.",
    "RAG improves accuracy by grounding responses in documents."
]

def simple_rag(query):
    query = query.lower()
    return [doc for doc in DOCUMENTS if any(word in doc.lower() for word in query.split())]

# -----------------------------
# Worker Agents
# -----------------------------
def summarize(text):
    return f"Summary: {text[:80]}..."

def extract_keywords(text):
    return [w for w in text.split() if len(w) > 5]

def sentiment_analysis(text):
    if "love" in text.lower():
        return "Positive"
    return "Neutral"

# -----------------------------
# Planning Agent
# -----------------------------
def planning_agent(task):
    return ["rag", "summarize", "keywords", "sentiment"]

# -----------------------------
# Router
# -----------------------------
def agent_router(step, task):
    if step == "rag":
        docs = simple_rag(task)
        return docs if docs else ["No relevant documents found."]
    if step == "summarize":
        return summarize(task)
    if step == "keywords":
        return extract_keywords(task)
    if step == "sentiment":
        return sentiment_analysis(task)

# -----------------------------
# Coordinator
# -----------------------------
def agentic_coordinator(task):
    plan = planning_agent(task)
    results = {}
    context = task

    for step in plan:
        output = agent_router(step, context)
        results[step] = output

        if isinstance(output, list):
            context = " ".join(output)
        else:
            context = str(output)

    return {"plan": plan, "results": results}

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🤖 Multi-Agent Orchestrator (Streamlit Version)")

user_input = st.text_area("Enter your query:")

if st.button("Run Agents"):
    if not user_input.strip():
        st.warning("Please enter a query.")
    else:
        result = agentic_coordinator(user_input)
        st.subheader("Plan")
        st.write(result["plan"])
        st.subheader("Results")
        st.json(result["results"])
