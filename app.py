import streamlit as st
import requests

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
# Knowledge Agent (Wikipedia + Search Fallback)
# -----------------------------
def knowledge_agent(query):
    # Clean the query (remove question words)
    cleaned = (
        query.lower()
        .replace("what is", "")
        .replace("who is", "")
        .replace("explain", "")
        .replace("tell me about", "")
        .replace("define", "")
        .strip()
    )

    # 1. Try direct Wikipedia summary
    try:
        direct_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{cleaned.replace(' ', '_')}"
        response = requests.get(direct_url).json()

        if "extract" in response and response["extract"]:
            return response["extract"]

        if "description" in response and response["description"]:
            return response["description"]

    except Exception:
        pass

    # 2. Fallback: Wikipedia search
    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={cleaned}&format=json"
        search_results = requests.get(search_url).json()

        if "query" in search_results and search_results["query"]["search"]:
            top_title = search_results["query"]["search"][0]["title"]

            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{top_title.replace(' ', '_')}"
            summary_response = requests.get(summary_url).json()

            if "extract" in summary_response and summary_response["extract"]:
                return summary_response["extract"]

            if "description" in summary_response and summary_response["description"]:
                return summary_response["description"]

    except Exception:
        pass

    return "No Wikipedia information found."

# -----------------------------
# Worker Agents
# -----------------------------
def summarize(text):
    return f"Summary: {text[:200]}..."

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
    return ["knowledge", "rag", "summarize", "keywords", "sentiment"]

# -----------------------------
# Router
# -----------------------------
def agent_router(step, task):
    if step == "knowledge":
        return knowledge_agent(task)
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
st.title("🤖 Multi-Agent Orchestrator (Enhanced with Knowledge Agent)")

mode = st.selectbox(
    "Choose input type:",
    ["Search topic (Wikipedia)", "Paste your own text"]
)

user_input = st.text_area("Enter your query or text:")

if st.button("Run Agents"):
    if not user_input.strip():
        st.warning("Please enter a query.")
    else:
        if mode == "Search topic (Wikipedia)":
            result = agentic_coordinator(user_input)
            st.subheader("Plan")
            st.write(result["plan"])
            st.subheader("Results")
            st.json(result["results"])
        else:
            st.subheader("Results (Custom Text Mode)")
            st.write({
                "summarize": summarize(user_input),
                "keywords": extract_keywords(user_input),
                "sentiment": sentiment_analysis(user_input)
            })
