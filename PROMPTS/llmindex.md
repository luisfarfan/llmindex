You are a senior AI systems architect.

Your task is to design a unified LLM registry system that merges data from two sources:

1) OpenRouter Models API (catalog + pricing + capabilities)
2) ArtificialAnalysis API (benchmarks + performance + rankings)

---

## STEP 1: ANALYZE DATA SOURCES

First, analyze and clearly define:

### OpenRouter provides:
- model id (e.g. openai/gpt-4.1)
- name
- provider
- context_length
- pricing (input/output tokens)
- modalities (text, image, audio)
- supported parameters (tools, reasoning, etc.)
- architecture info

### ArtificialAnalysis provides:
- reasoning_score
- coding_score
- intelligence_score
- speed
- cost_efficiency
- ranking per category (text, image, multimodal)

---

## STEP 2: DESIGN UNIFIED SCHEMA

Create a normalized JSON schema called `LLMModel` that merges both sources.

Requirements:
- must include ALL OpenRouter fields relevant for usage
- must include ALL ArtificialAnalysis performance metrics
- must include derived fields

Derived fields MUST include:
- best_for (array): ["coding", "reasoning", "chat", "agents", "multimodal", etc.]
- cost_level: ["low", "medium", "high"]
- performance_tier: ["low", "mid", "high", "frontier"]
- efficiency_score (combine cost + performance)

---

## STEP 3: MODEL MATCHING STRATEGY

Design a strategy to match models between OpenRouter and ArtificialAnalysis.

Problems to solve:
- different naming conventions
- version mismatches
- providers naming differences

Solution must include:
- normalization rules
- fuzzy matching strategy
- fallback mapping table

---

## STEP 4: DATA PIPELINE DESIGN

Design a pipeline that:

1. Fetches models from OpenRouter API
2. Fetches benchmark data from ArtificialAnalysis API
3. Merges both datasets
4. Stores results in a unified JSON or database

Include:
- sync strategy (cron / batch)
- caching
- update frequency
- error handling

---

## STEP 5: CLASSIFICATION ENGINE

Design logic to automatically assign:

best_for based on:
- high coding_score → "coding"
- high reasoning_score → "reasoning"
- high speed → "real-time"
- high context_length → "rag" or "long-context"

Define thresholds clearly.

---

## STEP 6: OUTPUT EXAMPLE

Return a final JSON example like:

{
  "id": "openai/gpt-4.1",
  "provider": "OpenAI",
  "context_length": 128000,
  "pricing": {
    "input": 0.00001,
    "output": 0.00003
  },
  "benchmarks": {
    "reasoning_score": 95,
    "coding_score": 92,
    "speed_score": 80
  },
  "best_for": ["coding", "reasoning"],
  "cost_level": "high",
  "performance_tier": "frontier"
}

---

## STEP 7: DESIGN DECISIONS

Explain:
- tradeoffs
- limitations
- assumptions

---

IMPORTANT:
- Do NOT be generic
- Be precise and system-level
- Think like a production-ready architecture