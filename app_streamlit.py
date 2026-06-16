import streamlit as st
from chromadb import PersistentClient

# -----------------------------
# Logging helper
# -----------------------------
def log(agent, message):
    print(f"[{agent}] {message}")

# -----------------------------
# Worker Agents
# -----------------------------
def summarize(text):
    return f"Summary: {text[:80]}..."

def extract_keywords(text):
    words = text.split()
    return [w for w in words if len(w) > 5]

def sentiment_analysis(text):
    if "love" in text.lower():
        return "Positive"
    return "Neutral"

# -----------------------------
# RAG Setup (Persistent Chroma)
# -----------------------------
client = PersistentClient(path="./db")
collection = client.get_or_create_collection("rag_docs")

# Add sample docs (only once)
documents = [
    "Multi-agent orchestration coordinates multiple AI agents.",
    "Agents can specialize in planning, research, coding, or analysis.",
    "A coordinator agent manages task delegation and integration.",
    "RAG improves accuracy by grounding responses in documents."
]

# Avoid duplicate inserts
existing = collection.count()
if existing == 0:
    collection.add(
        documents=documents,
        ids=[str(i) for i in range(len(documents))]
    )

def rag_agent(query):
    results = collection.query(query_texts=[query], n_results=2)
    return results.get("documents", [[]])[0]

# -----------------------------
# Planning Agent
# -----------------------------
def planning_agent(task):
    plan = ["rag", "summarize", "keywords", "sentiment"]
    log("Planner", f"Plan: {plan}")
    return plan

# -----------------------------
# Router
# -----------------------------
def agent_router(step, task):
    log("Router", f"Dispatching step '{step}'")

    if step == "rag":
        return rag_agent(task)
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
    log("Coordinator", f"Starting task: {task}")

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
    if user_input.strip() == "":
        st.warning("Please enter a query.")
    else:
        result = agentic_coordinator(user_input)

        st.subheader("Plan")
        st.write(result["plan"])

        st.subheader("Results")
        st.json(result["results"])
