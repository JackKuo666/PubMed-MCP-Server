import pytest

import pubmed_server
from pubmed_web_search import deep_paper_analysis as web_deep_paper_analysis


@pytest.fixture
def fake_metadata():
    return {
        "Title": "A Test Article",
        "Authors": ["Test Author"],
        "Abstract": "Test abstract.",
        "Journal": "Test Journal",
        "Publication Date": "2025-01-01",
    }


@pytest.mark.asyncio
async def test_deep_paper_analysis_prompt_renders(monkeypatch, fake_metadata):
    """Happy path: the prompt must render to valid MCP messages."""
    monkeypatch.setattr(
        pubmed_server, "get_pubmed_metadata", lambda pmid: fake_metadata
    )
    monkeypatch.setattr(
        "pubmed_server.web_deep_paper_analysis",
        lambda metadata: web_deep_paper_analysis(metadata),
        raising=False,
    )

    result = await pubmed_server.mcp.get_prompt(
        "deep_paper_analysis", {"pmid": "106755"}
    )

    assert result.messages, "expected at least one message"


@pytest.mark.asyncio
async def test_deep_paper_analysis_prompt_missing_pmid_renders(monkeypatch):
    """Error path: a missing PMID must also render to valid MCP messages."""
    monkeypatch.setattr(
        pubmed_server, "get_pubmed_metadata", lambda pmid: None
    )

    result = await pubmed_server.mcp.get_prompt(
        "deep_paper_analysis", {"pmid": "0"}
    )

    assert result.messages, "expected at least one message"
