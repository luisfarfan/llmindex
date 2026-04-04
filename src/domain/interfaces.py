from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import LLMModel

class IModelRepository(ABC):
    """Port: Interface for LLMModel persistence."""

    @abstractmethod
    async def get_by_id(self, model_id: str) -> Optional[LLMModel]: ...

    @abstractmethod
    async def get_all(self) -> List[LLMModel]: ...

    @abstractmethod
    async def save(self, model: LLMModel) -> LLMModel: ...

    @abstractmethod
    async def save_batch(self, models: List[LLMModel]) -> None: ...

class IFetcherGateway(ABC):
    """Port: Interface for fetching data from external APIs."""

    @abstractmethod
    async def fetch_catalog(self) -> List[dict]: ...

    @abstractmethod
    async def fetch_benchmarks(self) -> List[dict]: ...
