import json
from typing import List, Optional
from sqlalchemy import desc, asc
from sqlmodel import SQLModel, Field, Session, create_engine, select
from src.domain.entities import LLMModel, Pricing, Benchmarks
from src.domain.interfaces import IModelRepository
from src.infrastructure.config import get_settings

class LLMModelORM(SQLModel, table=True):
    """SQLModel representation for SQLite persistence."""
    __tablename__ = "models"

    id: str = Field(primary_key=True)
    name: str = Field(index=True)
    provider: str = Field(index=True)
    context_length: int = Field(default=0)
    pricing_input: float = Field(default=0.0)
    pricing_output: float = Field(default=0.0)
    modalities: str = Field(default="[]") # JSON string
    
    # Benchmarks (flattened for easy filtering)
    intelligence_score: Optional[float] = Field(default=None, index=True)
    speed_score: Optional[float] = Field(default=None)
    reasoning_score: Optional[float] = Field(default=None)
    coding_score: Optional[float] = Field(default=None)
    elo_score: Optional[float] = Field(default=None, index=True) # Multimodal ELO
    
    # Pre-calculated tags for faster API queries
    best_for: str = Field(default="[]") # JSON string of tags

class SQLiteModelRepository(IModelRepository):
    """Implementation of IModelRepository using SQLModel and SQLite."""

    def __init__(self, database_url: str = None):
        if not database_url:
            settings = get_settings()
            database_url = settings.DATABASE_URL
        
        self.engine = create_engine(database_url)
        # Ensure table is created
        SQLModel.metadata.create_all(self.engine)

    def _to_orm(self, m: LLMModel) -> LLMModelORM:
        return LLMModelORM(
            id=m.id,
            name=m.name,
            provider=m.provider,
            context_length=m.context_length,
            pricing_input=m.pricing.input,
            pricing_output=m.pricing.output,
            modalities=json.dumps(m.modalities),
            intelligence_score=m.benchmarks.intelligence_score if m.benchmarks else None,
            speed_score=m.benchmarks.speed_score if m.benchmarks else None,
            reasoning_score=m.benchmarks.reasoning_score if m.benchmarks else None,
            coding_score=m.benchmarks.coding_score if m.benchmarks else None,
            elo_score=m.benchmarks.elo_score if m.benchmarks else None,
            best_for=json.dumps(m.best_for)
        )

    async def save(self, model: LLMModel) -> None:
        with Session(self.engine) as session:
            orm = self._to_orm(model)
            session.merge(orm)
            session.commit()

    async def save_batch(self, models: List[LLMModel]) -> None:
        with Session(self.engine) as session:
            for m in models:
                session.merge(self._to_orm(m))
            session.commit()

    async def get_all(
        self, 
        provider: Optional[str] = None,
        best_for: Optional[str] = None,
        is_free: bool = False,
        min_intelligence: Optional[float] = None,
        sort_by: Optional[str] = None
    ) -> List[LLMModel]:
        with Session(self.engine) as session:
            query = session.query(LLMModelORM)
            
            if provider:
                query = query.filter(LLMModelORM.provider == provider)
            if is_free:
                query = query.filter(LLMModelORM.pricing_input == 0)
            if min_intelligence:
                query = query.filter(LLMModelORM.intelligence_score >= min_intelligence)
            if best_for:
                query = query.filter(LLMModelORM.best_for.like(f'%"{best_for}"%'))

            # Sorting
            if sort_by == "price":
                query = query.order_by(asc(LLMModelORM.pricing_input + LLMModelORM.pricing_output))
            elif sort_by == "intelligence":
                query = query.order_by(desc(LLMModelORM.intelligence_score))
            elif sort_by == "speed":
                query = query.order_by(desc(LLMModelORM.speed_score))
            elif sort_by == "elo":
                query = query.order_by(desc(LLMModelORM.elo_score))

            results = query.all()
            return [self._to_entity(r) for r in results]

    async def get_by_id(self, model_id: str) -> Optional[LLMModel]:
        with Session(self.engine) as session:
            orm = session.get(LLMModelORM, model_id)
            return self._to_entity(orm) if orm else None

    def _to_entity(self, orm: LLMModelORM) -> LLMModel:
        benchmarks = None
        # Use hasattr for safety on Row objects
        if hasattr(orm, 'intelligence_score') or hasattr(orm, 'elo_score'):
            benchmarks = Benchmarks(
                intelligence_score=getattr(orm, 'intelligence_score', None),
                speed_score=getattr(orm, 'speed_score', None),
                reasoning_score=getattr(orm, 'reasoning_score', None),
                coding_score=getattr(orm, 'coding_score', None),
                elo_score=getattr(orm, 'elo_score', None)
            )
            
        return LLMModel(
            id=orm.id,
            name=orm.name,
            provider=orm.provider,
            context_length=orm.context_length,
            pricing=Pricing(input=orm.pricing_input, output=orm.pricing_output),
            modalities=json.loads(orm.modalities),
            benchmarks=benchmarks
        )
