# LLMIndex

A unified, open-source LLM registry merging **OpenRouter** (catalog) and **ArtificialAnalysis** (benchmarks).

## Vision
LLMIndex provides a "Single Source of Truth" for LLM metadata and performance tiers. It uses a **Git-Ops** approach, where the data is updated daily via GitHub Actions and stored in portable **JSON** and **SQLite** formats.

## Key Features
- **Normalized Registry**: Standardized model IDs across providers.
- **Computed Metrics**: Intelligence/Cost efficiency scores and performance tiers.
- **Lite & Portable**: No complex DB setup required.
- **Ready for Agents**: Designed with "AI-Friendly" documentation (SDD).

## Documentation
See the [docs/](docs/) folder for detailed specifications:
- [Architecture](docs/01-architecture.md)
- [Data Schema](docs/02-data-schema.md)
- [Matching Engine](docs/03-matching-engine.md)
- [Classification Logic](docs/05-classification-logic.md)

## Development
This project follows **Clean Architecture**.
- **Domain**: Pure business logic (matching, scoring).
- **Use Cases**: Orchestration of sync and queries.
- **Adapters**: FastAPI, SQLite, and external API clients.

### Setup
```bash
poetry install
poetry shell
```

### Run Tests
```bash
PYTHONPATH=. pytest tests/
```

### Start API
```bash
uvicorn src.adapters.api.main:app --reload
```

---
*Open Source for the AI Community.*
