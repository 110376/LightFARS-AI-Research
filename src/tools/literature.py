"""文献检索工具（LangChain 1.0+ 正确实现）"""

import arxiv
import json
from typing import List

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class SearchArxivInput(BaseModel):
    """arXiv 搜索输入参数"""

    query: str = Field(description="搜索查询词（例如：'prompt engineering'）")
    max_results: int = Field(default=10, description="最大返回结果数")


@tool(args_schema=SearchArxivInput)
def search_arxiv(query: str, max_results: int = 10) -> str:
    """在 arXiv 上搜索学术论文。

    使用此工具在 arXiv 上查找相关的研究论文。

    参数:
        query: 搜索查询词（例如："prompt engineering code generation"）
        max_results: 最大返回结果数（默认：10）

    返回:
        包含论文信息的 JSON 字符串
    """
    search = arxiv.Search(
        query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []
    for result in search.results():
        papers.append(
            {
                "title": result.title,
                "authors": [a.name for a in result.authors],
                "summary": result.summary,
                "published": result.published.isoformat(),
                "arxiv_id": result.entry_id,
                "pdf_url": str(result.pdf_url),
            }
        )

    return json.dumps(papers, indent=2, ensure_ascii=False)
