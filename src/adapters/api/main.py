from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.domain.entities import LLMModel
from src.adapters.persistence.sqlite_repository import SQLiteModelRepository
from src.use_cases.sync_registry import SyncRegistryUseCase
from src.adapters.gateways.openrouter_fetcher import OpenRouterFetcher
from src.adapters.gateways.artificial_analysis_fetcher import ArtificialAnalysisFetcher
from src.domain.services.matching_engine import MatchingEngine
from src.adapters.persistence.json_exporter import JSONExporter
from src.infrastructure.config import get_settings

app = FastAPI(
    title="LLMIndex API",
    description="The Unified Open-Source LLM Registry API.",
    version="0.1.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency Injection Setup
def get_repository():
    return SQLiteModelRepository()

@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "LLMIndex API is live."}

@app.get("/api/v1/models", response_model=List[LLMModel], tags=["Models"])
async def get_models(
    provider: Optional[str] = Query(None, description="Filter by provider (e.g., OpenAI, Anthropic)"),
    best_for: Optional[str] = Query(None, description="Filter by strength (coding, rag, real-time, multimodal)"),
    is_free: bool = Query(False, description="Show only free models"),
    min_intelligence: Optional[float] = Query(None, description="Minimum benchmark score"),
    sort_by: Optional[str] = Query(None, description="Sort order (price, intelligence, speed)"),
    repo: SQLiteModelRepository = Depends(get_repository)
):
    """
    Query the unified LLM registry with high-fidelity filters.
    
    Examples:
    - /api/v1/models?best_for=coding&sort_by=price (Cheapest for coding)
    - /api/v1/models?is_free=true&min_intelligence=30 (Strongest free models)
    """
    return await repo.get_all(
        provider=provider,
        best_for=best_for,
        is_free=is_free,
        min_intelligence=min_intelligence,
        sort_by=sort_by
    )

@app.get("/api/v1/models/{model_id:path}", response_model=LLMModel, tags=["Models"])
async def get_model_detail(
    model_id: str,
    repo: SQLiteModelRepository = Depends(get_repository)
):
    """Get a detailed view of a specific model in the registry."""
    model = await repo.get_by_id(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found in registry.")
    return model

@app.post("/api/v1/sync", tags=["Admin"])
async def trigger_sync(repo: SQLiteModelRepository = Depends(get_repository)):
    """
    Trigger a manual synchronization of the registry.
    Usually managed by a Daily Cron Job (GitHub Actions).
    """
    fetchers = [OpenRouterFetcher(), ArtificialAnalysisFetcher()]
    engine = MatchingEngine(threshold=85.0)
    exporter = JSONExporter("llmindex.json")
    
    use_case = SyncRegistryUseCase(
        repository=repo,
        gateways=fetchers,
        matching_engine=engine,
        exporter=exporter
    )
    
    models = await use_case.execute()
    return {"status": "success", "synced_models": len(models)}
