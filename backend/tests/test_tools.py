import pytest
import asyncio
from app.tools.registry import tool_registry

@pytest.mark.asyncio
async def test_tool_registry():
    tools = tool_registry.list_tools()
    assert len(tools) >= 5

@pytest.mark.asyncio
async def test_open_meteo_tool():
    res = await tool_registry.execute_tool("get_weather", {
        "latitude": 28.6139,
        "longitude": 77.2090,
        "location_name": "Delhi"
    })
    assert res.success is True
    assert "temperature" in res.output
