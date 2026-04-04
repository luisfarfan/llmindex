from typing import List
from src.domain.entities import LLMModel
from src.domain.interfaces import IModelRepository, IFetcherGateway

class SyncRegistryUseCase:
    """
    Use Case: Synchronize the LLM Registry.
    Orchestrates fetching from OpenRouter and ArtificialAnalysis, 
    merging the data, and persisting to the repository.
    """

    def __init__(
        self, 
        repository: IModelRepository, 
        fetcher: IFetcherGateway
    ):
        self.repository = repository
        self.fetcher = fetcher

    async def execute(self) -> List[LLMModel]:
        """
        Main execution flow for the sync pipeline.
        Steps:
        1. Fetch Catalog (OpenRouter).
        2. Fetch Benchmarks (ArtificialAnalysis).
        3. Merge (Matching Logic).
        4. Classify (Step 5 logic).
        5. Persist (Save to SQLite/JSON).
        """
        # TODO: Implement full matching and merging logic
        # For now, it's a skeleton to define the layers.
        catalog_raw = await self.fetcher.fetch_catalog()
        benchmarks_raw = await self.fetcher.fetch_benchmarks()
        
        # Placeholder for transformed entities
        models: List[LLMModel] = [] 
        
        await self.repository.save_batch(models)
        return models
