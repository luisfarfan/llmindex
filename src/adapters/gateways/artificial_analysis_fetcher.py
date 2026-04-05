import aiohttp
import asyncio
import logging
from typing import List, Dict, Any, Optional
from src.domain.interfaces import IFetcherGateway
from src.infrastructure.config import get_settings
from rapidfuzz import process, fuzz

logger = logging.getLogger(__name__)

class ArtificialAnalysisFetcher(IFetcherGateway):
    """
    Gateway Adapter for ArtificialAnalysis API v2.
    Fetches both LLM models and specialized Multimodal Media ratings.
    """

    def __init__(self):
        settings = get_settings()
        self.api_key = settings.ARTIFICIAL_ANALYSIS_API_KEY
        self.base_url = "https://artificialanalysis.ai/api/v2/data"
        self.endpoints = {
            "models": f"{self.base_url}/llms/models",
            "image": f"{self.base_url}/media/text-to-image",
            "video": f"{self.base_url}/media/text-to-video",
            "speech": f"{self.base_url}/media/text-to-speech",
            "editing": f"{self.base_url}/media/image-editing"
        }

    async def fetch_catalog(self) -> List[Dict[str, Any]]:
        return []

    async def fetch_benchmarks(self) -> List[Dict[str, Any]]:
        """
        Aggregate and INTERNALLY unifty specialized benchmarks.
        """
        if not self.api_key:
            return []

        async with aiohttp.ClientSession() as session:
            all_raw: Dict[str, List[Dict[str, Any]]] = {}
            for name, url in self.endpoints.items():
                all_raw[name] = await self._fetch_endpoint(session, name, url)
                await asyncio.sleep(2.0) # Respectful Anti-429

            # 1. Start with the Master LLM list
            unified: Dict[str, Dict[str, Any]] = {}
            names_index: List[str] = []
            
            for item in all_raw["models"]:
                name = item.get("name") or item.get("id") or item.get("slug")
                if name:
                    unified[name] = item
                    names_index.append(name)

            # 2. Fuzzy Merge Media Data (Images, Video, etc.)
            for category in ["image", "video", "speech", "editing"]:
                for m_item in all_raw[category]:
                    m_name = m_item.get("name") or m_item.get("id") or m_item.get("slug")
                    if not m_name: continue
                    
                    # Search for existing model in unified list
                    match = process.extractOne(m_name, names_index, scorer=fuzz.WRatio)
                    if match and match[1] > 90:
                        target_name = match[0]
                        unified[target_name].update(m_item)
                    else:
                        # New Multimodal Model?
                        unified[m_name] = m_item
                        names_index.append(m_name)
            
            logger.info(f"Unfied AA data into {len(unified)} profiles.")
            return list(unified.values())

    async def _fetch_endpoint(self, session: aiohttp.ClientSession, name: str, url: str) -> List[Dict[str, Any]]:
        headers = {"x-api-key": self.api_key}
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                return []
        except Exception:
            return []
