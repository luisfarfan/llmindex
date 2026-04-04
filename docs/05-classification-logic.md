# 05 - LLMIndex: Classification Logic

## The Classification Engine
**LLMIndex** calculates several derived fields from the raw **OpenRouter** and **ArtificialAnalysis** data to help users find the "best" model for their specific needs.

### 1. `best_for` (Array)
A model is tagged based on its benchmarking scores and context length:
- **`coding`**: `coding_score` >= 90 OR `intelligence_score` >= 95.
- **`reasoning`**: `reasoning_score` >= 92.
- **`rag`**: `context_length` >= 128,000 AND `intelligence_score` >= 80.
- **`real-time`**: `speed_score` >= 150 AND `intelligence_score` >= 70.
- **`multimodal`**: Supports `image` or `audio` AND `intelligence_score` >= 85.

### 2. `cost_level` (String)
The system calculates the distribution of input pricing (1M tokens) across all models:
- **`low`**: Bottom 33% (e.g., `< $0.1`).
- **`mid`**: Middle 33% (e.g., `$0.1` to `$5.0`).
- **`high`**: Top 33% (e.g., `> $5.0`).

### 3. `performance_tier` (String)
Computed relative to all models in the index:
- **`frontier`**: Top 5% of `intelligence_score` (e.g., GPT-4.5, Claude 3.5 Sonnet).
- **`high`**: Next 15%.
- **`mid`**: Next 30%.
- **`low`**: Remaining 50%.

### 4. `efficiency_score` (Float 0-1)
A combined metric of performance and cost:
- **Formula**: `(Intelligence Score / Cost per 1M Output Tokens)`
- **Normalized**: The result is scaled from 0 to 1 based on the min/max values in the entire registry.
- **Usage**: Perfect for finding "The smartest model for my budget".

## Algorithm Recalculation
- **Global Context**: Classification logic is executed **after** all models are fetched and merged.
- **Automatic Thresholds**: Fields like `cost_level` and `performance_tier` use dynamic percentiles, so they stay accurate even as the market prices drop or new tier-1 models are released.
