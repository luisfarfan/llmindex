import pytest
from unittest.mock import AsyncMock, patch
from src.adapters.gateways.openrouter_fetcher import OpenRouterFetcher
from src.adapters.gateways.artificial_analysis_fetcher import ArtificialAnalysisFetcher

@pytest.mark.asyncio
async def test_openrouter_fetcher_success():
    """Verify that OpenRouter fetcher parses the 'data' field."""
    fetcher = OpenRouterFetcher()
    mock_response = {"data": [{"id": "meta-llama/llama-3-70b", "name": "Llama 3 70B"}]}
    
    with patch("src.adapters.gateways.http_fetcher.BaseHTTPFetcher.get", new_callable=AsyncMock) as mocked_get:
        mocked_get.return_value = mock_response
        result = await fetcher.fetch_catalog()
        
        assert len(result) == 1
        assert result[0]["id"] == "meta-llama/llama-3-70b"

@pytest.mark.asyncio
async def test_artificial_analysis_fetcher_success():
    """Verify that ArtificialAnalysis fetcher handles JSON arrays."""
    fetcher = ArtificialAnalysisFetcher()
    mock_response = [{"model_id": "llama-3-70b-instruct", "intelligence_score": 90.0}]
    
    with patch("src.adapters.gateways.http_fetcher.BaseHTTPFetcher.get", new_callable=AsyncMock) as mocked_get:
        mocked_get.return_value = mock_response
        result = await fetcher.fetch_benchmarks()
        
        assert len(result) == 1
        assert result[0]["model_id"] == "llama-3-70b-instruct"

@pytest.mark.asyncio
async def test_artificial_analysis_fetcher_handles_error():
    """Verify that fetcher returns an empty list on error (Partial Sync behavior)."""
    fetcher = ArtificialAnalysisFetcher()
    
    with patch("src.adapters.gateways.http_fetcher.BaseHTTPFetcher.get", new_callable=AsyncMock) as mocked_get:
        mocked_get.return_value = None # Simulating an error
        result = await fetcher.fetch_benchmarks()
        
        assert result == []
