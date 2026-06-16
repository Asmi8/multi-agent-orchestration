import gradio as gr
import chromadb
from chromadb.config import Settings

# -----------------------------
# Logging
# -----------------------------
def log(agent, message):
    print(f"[{agent}] {message}")

# -----------------------------
# Worker Agents
# -----------------------------
def summarize(text):
    return f"Summary: {text[:50]}..."

def extract_keywords(text):
    words = text.split()
    return [w for w in words if len(w) > 5]

def sentiment_analysis(text):
    if "love" in text.lower():
        return "Positive"
    return "Neutral"

# -----------------------------
# RAG Setup
# -----------------------------
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./db"))
collection = client.get_or_create_collection("rag_docs")

# Add sample docs (you can replace these)
documents = [
    "Multi-agent orchestration coordinates multiple AI agents.",
    "Agents can specialize in planning, research, coding, or analysis.",
    "A coordinator agent manages task delegation and integration.",
    "RAG improves accuracy by grounding responses in documents."
]

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
        elif isinstance(output, dict):
            context = output.get("result", task)
        else:
            context = str(output)

    return {"plan": plan, "results": results}

# -----------------------------
# Gradio UI
# -----------------------------
def run_agents(user_input):
    result = agentic_coordinator(user_input)
    return (
        f"Plan: {result['plan']}\n\n"
        f"Results:\n{result['results']}"
    )

with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Multi-Agent Orchestrator")
    inp = gr.Textbox(label="Enter your query")
    out = gr.Textbox(label="Agent Output")
    btn = gr.Button("Run Agents")
    btn.click(run_agents, inp, out)

demo.launch(server_name="0.0.0.0", server_port=7860)
