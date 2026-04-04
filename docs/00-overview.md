# 00 - LLMIndex: Overview

## Vision
**LLMIndex** is an open-source, lightweight "Single Source of Truth" for Large Language Models (LLMs). It automates the discovery, benchmarking, and classification of models by merging institutional-grade data from **OpenRouter** and **ArtificialAnalysis**.

The project is designed with a **"Git-Ops"** and **"Lite & Portable"** philosophy:
- **Git-Ops**: Database results are version-controlled in the repository as JSON and SQLite files.
- **Portability**: No heavy infrastructure (like PostgreSQL) is required. Developers can use the data by simply importing a JSON file or querying a local SQLite DB.
- **Transparency**: Clear, mathematical classification for what models are "best for" (Coding, Reasoning, Agents, etc.).

## Core Objectives
1. **Model Discovery**: Track all models available via OpenRouter (Context length, Pricing, Modalities).
2. **Performance Benchmarking**: Link these models to ArtificialAnalysis performance metrics (Reasoning, Coding, Speed scores).
3. **Automated Classification**: Use an engine to categorize models by "Efficiency", "Performance Tier", and "Best Use Case".
4. **Public Registry**: Provide a globally accessible JSON file and a lightweight FastAPI query engine for consumption.

## Data Sources
### 1. OpenRouter API
Provides the "Catalog" data:
- `model_id`, `name`, `provider`.
- `context_length`.
- `pricing` (tokens: input/output).
- `modalities` (text, image, audio).
- `parameters` (tools, reasoning support).

### 2. ArtificialAnalysis API/Dataset
Provides the "Metrics" data:
- `reasoning_score`.
- `coding_score`.
- `intelligence_score`.
- `speed` (tokens/sec).
- `cost_efficiency`.

## Value Proposition
For developers and AI companies, **LLMIndex** solves the "which model to use?" problem by providing a verifiable, data-driven index that balances cost vs. intelligence.
