# 02 - LLMModel: Merged Data Schema

## `LLMModel` (Unified Object)
The `LLMModel` is the core data structure of **LLMIndex**. It contains normalized metadata from **OpenRouter** and benchmarking data from **ArtificialAnalysis**.

```json
{
  "id": "openai/gpt-4.5-preview",
  "name": "GPT-4.5 Preview",
  "provider": "OpenAI",
  "context_length": 128000,
  "pricing": {
    "input": 0.00001,
    "output": 0.00003
  },
  "modalities": ["text", "image"],
  "benchmarks": {
    "reasoning_score": 98.2,
    "coding_score": 94.5,
    "intelligence_score": 96.1,
    "speed_score": 82.0,
    "cost_efficiency": 0.5
  },
  "best_for": ["coding", "reasoning", "multimodal"],
  "cost_level": "high",
  "performance_tier": "frontier",
  "efficiency_score": 0.72,
  "last_synced": "2024-04-03T12:00:00Z"
}
```

## Fields Breakdown

### 1. Catalog Fields (OpenRouter)
- **`id`**: Unique identifier from OpenRouter (e.g., `anthropic/claude-3.5-sonnet`).
- **`provider`**: Company (e.g., `Anthropic`, `OpenAI`, `Meta`).
- **`context_length`**: Maximum token input.
- **`pricing`**: Normalized price per 1M tokens.
- **`modalities`**: Array of supported media types (`text`, `image`, `audio`).

### 2. Benchmark Fields (ArtificialAnalysis)
- **`reasoning_score`**: Cognitive benchmarks.
- **`coding_score`**: HumanEval/MBPP-style performance.
- **`intelligence_score`**: Overall ranking.
- **`speed_score`**: Normalized tokens per second.

### 3. Computed / Derived Fields (LLMIndex Engine)
- **`best_for`**: Tags assigned based on the **Classification Logic** (`coding`, `rag`, `chat`, `real-time`).
- **`cost_level`**: Classification into `low`, `mid`, `high` based on the pricing distribution.
- **`performance_tier`**: Categorization into `low`, `mid`, `high`, `frontier` (top 5%).
- **`efficiency_score`**: A value from 0 to 1 calculated as: `(Intelligence Score / Cost per 1M Output Tokens)`.

## Schema Constraints
- **Validation**: Enforced via **Pydantic** in the Python backend.
- **Null Safety**: Benchmarking fields are optional (`null`) if the model hasn't been tested yet.
- **SQLite Mapping**: The flat fields and nested objects (`pricing`, `benchmarks`) are mapped to the SQLite database with `JSON` columns or relational normalization.
