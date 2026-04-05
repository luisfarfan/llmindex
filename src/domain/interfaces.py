from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import LLMModel

class IModelRepository(ABC):
    """Port: Interface for LLMModel persistence."""

    @abstractmethod
    async def get_by_id(self, model_id: str) -> Optional[LLMModel]: ...

    @abstractmethod
    async def get_all(
        self, 
        provider: Optional[str] = None,
        best_for: Optional[str] = None,
        is_free: bool = False,
        min_intelligence: Optional[float] = None,
        sort_by: Optional[str] = None
    ) -> List[LLMModel]: ...

    @abstractmethod
    async def save(self, model: LLMModel) -> None: ...

    @abstractmethod
    async def save_batch(self, models: List[LLMModel]) -> None: ...

class IFetcherGateway(ABC):
    """Port: Interface for fetching data from external APIs."""

    @abstractmethod
    async def fetch_catalog(self) -> List[dict]: ...

    @abstractmethod
    async def fetch_benchmarks(self) -> List[dict]: ...

class IStaticExporter(ABC):
    """Port: Interface for exporting to a static file format."""
    
    @abstractmethod
    async def export(self, models: List[LLMModel]) -> None: ...
