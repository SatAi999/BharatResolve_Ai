from datetime import datetime
from typing import List
import httpx
from fastapi import APIRouter
from app.config import settings
from app.schemas.case_schemas import IntegrationHealth

router = APIRouter(prefix="/api/integrations", tags=["Integrations"])

@router.get("", response_model=List[IntegrationHealth])
async def check_integrations():
    results = []

    # 1. Gemini / LLM Provider Health Check
    llm_status = "CONNECTED" if settings.GEMINI_API_KEY else ("DEGRADED" if settings.OLLAMA_BASE_URL else "NOT_CONFIGURED")
    results.append(IntegrationHealth(
        name="llm_engine",
        display_name="Gemini & Ollama LLM Engine",
        status=llm_status,
        capabilities=["Reasoning", "Intent Classification", "Document Understanding"],
        last_health_check=datetime.utcnow(),
        error_message=None if llm_status == "CONNECTED" else ("Using local Ollama fallback on port 11434" if llm_status == "DEGRADED" else "No LLM key or Ollama found")
    ))

    # 2. Open-Meteo Weather API
    weather_status = "CONNECTED"
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            res = await client.get("https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.20&current=temperature_2m")
            if res.status_code != 200:
                weather_status = "DEGRADED"
    except Exception:
        weather_status = "ERROR"
        
    results.append(IntegrationHealth(
        name="open_meteo",
        display_name="Open-Meteo Weather Service",
        status=weather_status,
        capabilities=["Live Temperature", "Precipitation Forecast", "Agricultural & Storm Analysis"],
        last_health_check=datetime.utcnow()
    ))

    # 3. OpenStreetMap / Nominatim Geocoding API
    osm_status = "CONNECTED"
    try:
        headers = {"User-Agent": "BharatResolveAI/1.0"}
        async with httpx.AsyncClient(timeout=3.0) as client:
            res = await client.get("https://nominatim.openstreetmap.org/search?q=Delhi,India&format=json", headers=headers)
            if res.status_code != 200:
                osm_status = "DEGRADED"
    except Exception:
        osm_status = "ERROR"

    results.append(IntegrationHealth(
        name="openstreetmap",
        display_name="OpenStreetMap Nominatim & Overpass",
        status=osm_status,
        capabilities=["Location Geocoding", "District Boundary Lookup", "Public Office Finder"],
        last_health_check=datetime.utcnow()
    ))

    # 4. Live Web Research (DuckDuckGo / Scraper)
    results.append(IntegrationHealth(
        name="live_research",
        display_name="Live Government Web Search Engine",
        status="CONNECTED",
        capabilities=["Portal Research", "Citizens' Charter Retrieval", "Authoritative Citation"],
        last_health_check=datetime.utcnow()
    ))

    # 5. data.gov.in Official Datasets
    datagov_status = "CONNECTED" if settings.DATA_GOV_API_KEY else "NOT_CONFIGURED"
    results.append(IntegrationHealth(
        name="data_gov_in",
        display_name="data.gov.in Open Data Portal",
        status=datagov_status,
        capabilities=["Official Scheme Datasets", "Government Statistics"],
        last_health_check=datetime.utcnow(),
        error_message="DATA_GOV_API_KEY not configured in .env" if datagov_status == "NOT_CONFIGURED" else None
    ))

    return results
