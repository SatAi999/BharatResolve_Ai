import logging
from typing import Dict, List, Optional, Any
from app.tools.base import BaseTool, ToolResult
from app.tools.open_meteo import OpenMeteoTool
from app.tools.openstreetmap import OpenStreetMapTool
from app.tools.live_research import LiveResearchTool
from app.tools.document_ocr import DocumentOCRTool
from app.tools.grievance_builder import GrievanceBuilderTool
from app.tools.notification import NotificationTool

logger = logging.getLogger("bharatresolve.tools")

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        default_tools = [
            OpenMeteoTool(),
            OpenStreetMapTool(),
            LiveResearchTool(),
            DocumentOCRTool(),
            GrievanceBuilderTool(),
            NotificationTool()
        ]
        for tool in default_tools:
            self.register(tool)

    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name} (Risk: {tool.risk_level})")

    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        return self._tools.get(tool_name)

    def list_tools(self) -> List[Dict[str, Any]]:
        return [tool.to_mcp_schema() for tool in self._tools.values()]

    async def execute_tool(self, tool_name: str, kwargs: Dict[str, Any]) -> ToolResult:
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolResult(
                success=False,
                tool_name=tool_name,
                output={},
                error_message=f"Tool '{tool_name}' is not registered in ToolRegistry.",
                is_real_data=False
            )
        
        try:
            return await tool.execute(**kwargs)
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return ToolResult(
                success=False,
                tool_name=tool_name,
                output={},
                error_message=f"Execution error in {tool_name}: {str(e)}",
                is_real_data=False
            )

# Global tool registry singleton
tool_registry = ToolRegistry()
