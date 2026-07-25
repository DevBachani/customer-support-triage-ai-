# 🛠️ Customer Support Triage AI

An automated, local-first customer message classification and routing engine powered by local LLM inference (Llama 3.1), strict Pydantic schema validation, and rule-based escalation logic. 

## 📌 Problem Statement & Philosophy

Modern customer support queues are overwhelmed with high-volume, varying-priority messages. While LLMs are excellent at understanding intent, integrating them into production pipelines often leads to over-engineering. **No LangChain or other orchestration frameworks are used in this project. They aren't necessary here and would add complexity without much benefit.** 

The goal of this project was to build a deterministic, highly reliable parsing engine using raw Python and local models to prove that structured AI data extraction can be achieved without bloated dependencies or expensive cloud APIs.

## 🚀 The Solution

This system uses a lightweight, pure-Python pipeline to route messages. By combining **Ollama (Llama 3.1)** with **Pydantic v2**, the system guarantees structured JSON outputs (Category, Priority, Summary, Suggested Action) while maintaining a local, privacy-first architecture. 

When answering how to build scalable AI pipelines, my approach is simple: **No LangChain or other orchestration frameworks. They aren't necessary here and would add complexity without much benefit.** Instead, this architecture relies on robust exception handling, retry logic, and fallback mechanisms built natively in Python.

---

## 🏗️ Architecture Flow

```text
Customer Messages
       │
       ▼
Data Loader (JSON/CSV)
       │
       ▼
Input Preprocessing
       │
       ▼
Prompt Builder (System Prompt with Expected JSON Schema)
       │
       ▼
Ollama (Llama 3.1 Local Engine via CPU)
       │
       ▼
Regex JSON Cleaning & Extraction
       │
       ▼
Pydantic Schema Validation ───[ Invalid JSON ]──► Retry / Safe Fallback
       │
  [ Valid JSON ]
       │
       ▼
Confidence Check & Rule-Based Human Escalation (Safety Guardrails)
       │
       ▼
Evaluation Metrics & Streamlit UI Dashboard



## 🧠 AI Decisions & Design Strategy

1. **Handling Uncertainty & Bad Input:** The system relies on a two-tier safety net. First, if the LLM confidence score is below 0.85, the `needs_human` flag is forced to `True`. Second, if the input is pure garbage and causes a Pydantic `ValidationError` (i.e., failed JSON generation), the system catches the error and gracefully routes to a structured `generate_fallback()` function. It never crashes.
2. **Defeating Prompt Injection / Hijacking:** The system prompt aggressively frames the LLM as a data-extraction parser, not a conversational agent. By strictly enforcing a JSON-only output via Pydantic schema validation, any attempt by the user to "hijack" the prompt (e.g., "Ignore previous instructions") results in an invalid schema, which is immediately caught by the fallback mechanism and escalated to a human.
3. **Cost, Tokens, & Latency:** 
   * **Cost:** $0.00 (100% local inference).
   * **Tokens:** Capped context (`num_ctx: 1024`) and max generation (`num_predict: 200`) to prevent token-spewing.
   * **Latency:** ~45-60 seconds per message on CPU.
4. **How to Cut Latency & Scale:** To cut latency in production, I would deploy the model using **vLLM** with Continuous Batching on a GPU. Furthermore, I would implement **Semantic Caching** (Redis) to bypass the LLM entirely for repeat questions, and eventually **Distill** the 8B model into a 1.5B parameter SLM specialized strictly for classification.
5. **No Framework Bloat:** Kept the orchestration deterministic and lightweight (pure Python) to eliminate unnecessary library abstraction (like LangChain), which adds complexity without benefit for this specific use case.


Enhancement:

## 🚀 Path to Production: Scaling the Inference Engine

While this architecture serves as a robust, privacy-first local prototype, deploying this to a high-volume production environment (e.g., thousands of tickets per minute) requires shifting from synchronous CPU inference to an optimized, async GPU pipeline. 

To maintain the "zero-bloat" philosophy while scaling, I would implement the following inference and architectural upgrades:

### 1. High-Throughput Inference Engine (vLLM)
Ollama is excellent for local development, but in production, I would migrate the inference backend to **vLLM** or **TensorRT-LLM**.
* **Continuous Batching:** Instead of processing messages sequentially, vLLM dynamically batches incoming requests at the iteration level, maximizing GPU utilization and drastically reducing queue latency.
* **PagedAttention:** Efficiently manages KV cache memory, allowing for much higher throughput on concurrent requests.

### 2. Constrained Decoding (Guaranteed JSON)
Currently, the pipeline uses prompt engineering, regex cleaning, and Pydantic validation/retries to ensure valid JSON. In production, I would use **Constrained Decoding** (via libraries like `Outlines` or vLLM's native guided decoding).
* By masking logits at the inference level, we can mathematically force the LLM to *only* generate tokens that conform to the exact Pydantic schema. This eliminates the need for regex cleaning and retry loops, saving compute and ensuring 0% JSON parse failures.

### 3. Event-Driven Architecture (Async Processing)
Customer support ingestion is highly bursty. The synchronous `analyze_message` function would be decoupled into an event-driven system:
* **Message Broker:** Incoming tickets are pushed to a queue (Kafka, RabbitMQ, or AWS SQS).
* **Async Workers:** A FastAPI backend utilizing `asyncio` consumes the queue, processes tickets via the vLLM endpoint, and writes the routed metadata back to the ticketing CRM (e.g., Zendesk/Jira).

### 4. Semantic Caching & Model Distillation
To drastically reduce compute costs and latency:
* **Semantic Caching:** Implement Redis with a fast embedding model. If a customer asks "Where is my package?" and another asks "Where's my order?", the embedding similarity triggers a cache hit, bypassing the LLM entirely.
* **Distillation:** Once the Llama 3.1 model routes ~50,000 tickets successfully, I would use that data to fine-tune a much smaller, lightning-fast model (like DeBERTa or a 1.5B parameter SLM) specifically for this classification task, moving away from a 8B+ parameter generalist model.