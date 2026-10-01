from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel

class ToolResult(BaseModel):
    success: bool
    tool_name: str
    output: Dict[str, Any]
    error_message: Optional[str] = None
    execution_time_ms: int = 0
    source_attribution: Optional[str] = None
    is_real_data: bool = True

class BaseTool(ABC):
    name: str
    description: str
    input_schema: type[BaseModel]
    risk_level: str = "LOW" # LOW, MEDIUM, HIGH, CRITICAL
    requires_approval: bool = False
    retryable: bool = True
    max_retries: int = 3

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        pass

    def to_mcp_schema(self) -> Dict[str, Any]:
        """Exposes tool schema in Model Context Protocol (MCP) format."""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema.model_json_schema(),
            "metadata": {
                "risk_level": self.risk_level,
                "requires_approval": self.requires_approval,
                "retryable": self.retryable,
                "max_retries": self.max_retries
            }
        }
