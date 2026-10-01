import time
import httpx
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from app.tools.base import BaseTool, ToolResult

class GeocodeInput(BaseModel):
    query: str = Field(..., description="Address, city, district, or place name in India (e.g. 'Jaipur, Rajasthan' or 'Panchayat Bhavan, Varanasi')")

class OpenStreetMapTool(BaseTool):
    name = "geocode_location"
    description = "Geocodes an Indian location, district, or public building to latitude, longitude, and structured address using OpenStreetMap Nominatim."
    input_schema = GeocodeInput
    risk_level = "LOW"
    requires_approval = False

    async def execute(self, **kwargs) -> ToolResult:
        start_time = time.time()
        params = self.input_schema(**kwargs)
        
        url = "https://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "BharatResolveAI/1.0 (contact@bharatresolve.in)"}
        query_params = {
            "q": params.query + ", India",
            "format": "json",
            "addressdetails": 1,
            "limit": 3
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=headers, params=query_params)
                duration = int((time.time() - start_time) * 1000)
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        first = data[0]
                        address = first.get("address", {})
                        return ToolResult(
                            success=True,
                            tool_name=self.name,
                            output={
                                "display_name": first.get("display_name"),
                                "latitude": float(first.get("lat")),
                                "longitude": float(first.get("lon")),
                                "district": address.get("state_district") or address.get("county") or address.get("city"),
                                "state": address.get("state"),
                                "postcode": address.get("postcode"),
                                "country": address.get("country")
                            },
                            execution_time_ms=duration,
                            source_attribution="OpenStreetMap Nominatim (https://nominatim.openstreetmap.org)",
                            is_real_data=True
                        )
                    else:
                        return ToolResult(
                            success=False,
                            tool_name=self.name,
                            output={"query": params.query},
                            error_message=f"No geographic results found for location query '{params.query}'",
                            execution_time_ms=duration,
                            source_attribution="OpenStreetMap Nominatim",
                            is_real_data=True
                        )
                else:
                    return ToolResult(
                        success=False,
                        tool_name=self.name,
                        output={},
                        error_message=f"Nominatim returned status code {response.status_code}",
                        execution_time_ms=duration,
                        is_real_data=False
                    )
        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            return ToolResult(
                success=False,
                tool_name=self.name,
                output={},
                error_message=f"Geocoding service error: {str(e)}",
                execution_time_ms=duration,
                is_real_data=False
            )
