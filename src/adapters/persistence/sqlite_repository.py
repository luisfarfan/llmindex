from typing import List, Optional
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.domain.entities import LLMModel, Pricing, Benchmarks
from src.domain.interfaces import IModelRepository
from src.adapters.persistence.models import LLMModelORM

class SQLiteModelRepository(IModelRepository):
    """Adapter: SQLite implementation of IModelRepository using SQLModel."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, model_id: str) -> Optional[LLMModel]:
        statement = select(LLMModelORM).where(LLMModelORM.id == model_id)
        result = await self.session.execute(statement)
        orm_model = result.scalars().first()
        return self._to_entity(orm_model) if orm_model else None

    async def get_all(self) -> List[LLMModel]:
        statement = select(LLMModelORM)
        result = await self.session.execute(statement)
        orm_models = result.scalars().all()
        return [self._to_entity(orm) for orm in orm_models]

    async def save(self, model: LLMModel) -> LLMModel:
        orm_model = self._to_orm(model)
        self.session.add(orm_model)
        await self.session.flush()
        return model

    async def save_batch(self, models: List[LLMModel]) -> None:
        for model in models:
            orm_model = self._to_orm(model)
            self.session.add(orm_model)
        await self.session.flush()

    def _to_entity(self, orm: LLMModelORM) -> LLMModel:
        """Map ORM model to Domain Entity."""
        return LLMModel(
            id=orm.id,
            name=orm.name,
            provider=orm.provider,
            context_length=orm.context_length,
            pricing=Pricing(**orm.pricing),
            modalities=orm.modalities,
            benchmarks=Benchmarks(**orm.benchmarks) if orm.benchmarks else None,
            last_synced=orm.last_synced
        )

    def _to_orm(self, entity: LLMModel) -> LLMModelORM:
        """Map Domain Entity to ORM Model."""
        return LLMModelORM(
            id=entity.id,
            name=entity.name,
            provider=entity.provider,
            context_length=entity.context_length,
            pricing=entity.pricing.model_dump(),
            modalities=entity.modalities,
            benchmarks=entity.benchmarks.model_dump() if entity.benchmarks else None,
            last_synced=entity.last_synced
        )
