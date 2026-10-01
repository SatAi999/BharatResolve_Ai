import time
import httpx
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from app.tools.base import BaseTool, ToolResult

class OpenMeteoInput(BaseModel):
    latitude: float = Field(..., description="Latitude of location (e.g. 28.6139 for Delhi)")
    longitude: float = Field(..., description="Longitude of location (e.g. 77.2090 for Delhi)")
    location_name: Optional[str] = Field(default="Location", description="Human readable name of location")

class OpenMeteoTool(BaseTool):
    name = "get_weather"
    description = "Retrieves live weather, rainfall, and temperature from Open-Meteo API for agricultural, storm damage, or logistics investigation."
    input_schema = OpenMeteoInput
    risk_level = "LOW"
    requires_approval = False

    async def execute(self, **kwargs) -> ToolResult:
        start_time = time.time()
        params = self.input_schema(**kwargs)
        
        url = "https://api.open-meteo.com/v1/forecast"
        query_params = {
            "latitude": params.latitude,
            "longitude": params.longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,precipitation",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "Asia/Kolkata"
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=query_params)
                if response.status_code == 200:
                    data = response.json()
                    current = data.get("current", {})
                    daily = data.get("daily", {})
                    duration = int((time.time() - start_time) * 1000)
                    
                    return ToolResult(
                        success=True,
                        tool_name=self.name,
                        output={
                            "location_name": params.location_name,
                            "latitude": params.latitude,
                            "longitude": params.longitude,
                            "temperature": current.get("temperature_2m"),
                            "humidity": current.get("relative_humidity_2m"),
                            "wind_speed": current.get("wind_speed_10m"),
                            "precipitation": current.get("precipitation"),
                            "daily_max_temp": daily.get("temperature_2m_max", [])[:3],
                            "daily_precipitation": daily.get("precipitation_sum", [])[:3],
                            "retrieved_at": current.get("time")
                        },
                        execution_time_ms=duration,
                        source_attribution="Open-Meteo Live API (https://open-meteo.com)",
                        is_real_data=True
                    )
                else:
                    duration = int((time.time() - start_time) * 1000)
                    return ToolResult(
                        success=False,
                        tool_name=self.name,
                        output={"error": f"HTTP {response.status_code}"},
                        error_message=f"Open-Meteo API returned status code {response.status_code}",
                        execution_time_ms=duration,
                        source_attribution="Open-Meteo Live API",
                        is_real_data=False
                    )
        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            return ToolResult(
                success=False,
                tool_name=self.name,
                output={},
                error_message=f"Network error querying Open-Meteo: {str(e)}",
                execution_time_ms=duration,
                source_attribution="Open-Meteo Live API",
                is_real_data=False
            )
