import time
import re
import httpx
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from bs4 import BeautifulSoup
from app.tools.base import BaseTool, ToolResult
from app.security.prompt_injection import sanitize_untrusted_content

class LiveResearchInput(BaseModel):
    query: str = Field(..., description="Web search query e.g. 'DBT scholarship portal grievance email India' or 'electricity bill dispute guidelines UP'")
    domain_filter: Optional[str] = Field(default=None, description="Optional domain restriction e.g. 'gov.in' or 'nic.in'")

class LiveResearchTool(BaseTool):
    name = "search_official_information"
    description = "Searches live official government portals, public knowledge sources, and legal guidelines for authoritative procedures and resolutions."
    input_schema = LiveResearchInput
    risk_level = "LOW"
    requires_approval = False

    async def execute(self, **kwargs) -> ToolResult:
        start_time = time.time()
        params = self.input_schema(**kwargs)
        
        search_query = params.query
        if params.domain_filter:
            search_query += f" site:{params.domain_filter}"

        results = []
        try:
            # Use DuckDuckGo HTML search endpoint for real live web search without requiring paid API key
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            search_url = "https://html.duckduckgo.com/html/"
            data = {"q": search_query}

            async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
                response = await client.post(search_url, headers=headers, data=data)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    links = soup.find_all("a", class_="result__url")
                    snippets = soup.find_all("a", class_="result__snippet")
                    titles = soup.find_all("a", class_="result__title")

                    for i in range(min(5, len(links))):
                        href = links[i].get("href", "")
                        # DuckDuckGo wraps links in /l/?uddg=...
                        clean_url = href
                        if "/l/?uddg=" in href:
                            match = re.search(r"uddg=([^&]+)", href)
                            if match:
                                import urllib.parse
                                clean_url = urllib.parse.unquote(match.group(1))

                        title_text = titles[i].get_text(strip=True) if i < len(titles) else "Public Knowledge Result"
                        snippet_text = snippets[i].get_text(strip=True) if i < len(snippets) else ""
                        
                        # Identify source type
                        source_type = "official_government" if any(g in clean_url for g in [".gov.in", ".nic.in", ".edu.in", ".org.in"]) else "public_knowledge"

                        results.append({
                            "title": title_text,
                            "url": clean_url,
                            "snippet": sanitize_untrusted_content(snippet_text),
                            "source_type": source_type,
                            "is_authoritative": ".gov.in" in clean_url or ".nic.in" in clean_url
                        })

            duration = int((time.time() - start_time) * 1000)
            if results:
                return ToolResult(
                    success=True,
                    tool_name=self.name,
                    output={
                        "query": search_query,
                        "total_results": len(results),
                        "results": results
                    },
                    execution_time_ms=duration,
                    source_attribution=f"Live Web Search (Results count: {len(results)})",
                    is_real_data=True
                )
            else:
                return ToolResult(
                    success=True,
                    tool_name=self.name,
                    output={
                        "query": search_query,
                        "total_results": 0,
                        "results": [],
                        "note": "No direct search snippets returned; fallback policy advice applicable."
                    },
                    execution_time_ms=duration,
                    is_real_data=True
                )
        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            return ToolResult(
                success=False,
                tool_name=self.name,
                output={},
                error_message=f"Live search query failed: {str(e)}",
                execution_time_ms=duration,
                is_real_data=False
            )
