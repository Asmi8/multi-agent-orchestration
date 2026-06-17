# Multi‑Agent Orchestration System

What is a Multi‑Agent System?
A multi‑agent system (MAS) is a setup where multiple independent agents (small programs, models, or components) work together to solve a task.
Each agent has one job, and the system becomes powerful because these agents collaborate.

Think of it like a team:

One agent gathers information

One agent retrieves documents

One agent summarizes

One agent analyzes sentiment

One agent extracts keywords

One agent plans the workflow

One agent coordinates everything

Instead of one big model doing everything, you break the task into specialized parts.

Why multi‑agent systems matter?

1. They allow you to build:

2. More modular AI systems

3. More explainable pipelines

4. More scalable workflows

5. More reliable reasoning (because each agent focuses on one thing)

This is exactly how modern agentic AI frameworks work (like AutoGPT, CrewAI, LangGraph, etc.).
This project is a simple, modular **multi‑agent system** built using **Python** and **Streamlit**. It demonstrates how multiple specialized agents can collaborate to process a user query step‑by‑step — similar to modern agentic AI workflows.

The goal is to understand **agent orchestration**, **task routing**, **knowledge retrieval**, and **context passing** between agents.

---

## Features

### 1. Planning Agent
Defines the workflow for solving a query.  

### 2. Knowledge Agent (Wikipedia API)
Fetches external information by:
- Cleaning the user query  
- Trying direct Wikipedia summary  
- Falling back to Wikipedia search  
- Returning extracted knowledge  

### 3. RAG Agent (Document Retrieval)
Searches a small in‑memory document store for relevant lines.  
Demonstrates the basics of **retrieval‑augmented generation (RAG)**.

### 4. Summarizer Agent
Creates a short summary of the text (first 200 characters).

### 5. Keyword Extractor Agent
Extracts meaningful keywords (words longer than 5 characters).

### 6. Sentiment Analyzer
Simple rule‑based sentiment:
- Contains “love” → Positive  
- Otherwise → Neutral  

### 7. Coordinator Agent
Executes each agent in sequence and integrates their outputs into a final response.

---

## Architecture

The system follows a linear multi‑agent pipeline:

1. Planning Agent decides the workflow  
2. Coordinator executes each agent step‑by‑step  
3. Knowledge Agent retrieves external info  
4. RAG Agent retrieves internal context  
5. Summarizer condenses the text  
6. Keyword Extractor identifies important terms  
7. Sentiment Analyzer classifies tone  
8. Coordinator returns the final combined output  

---

## Streamlit App

The UI allows users to:
- Enter a topic for Wikipedia search  
- Or paste their own text  
- View outputs from all agents  
- See the full multi‑agent pipeline in action  

---

## Installation

```bash
pip install -r requirements.txt
streamlit run app.py

