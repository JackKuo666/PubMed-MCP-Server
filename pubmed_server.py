from typing import Any, List, Dict, Optional, Union
import asyncio
import logging
from mcp.server.fastmcp import FastMCP
from pubmed_web_search import search_key_words, search_advanced, get_pubmed_metadata, download_full_text_pdf, deep_paper_analysis

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FastMCP server
mcp = FastMCP("pubmed")

@mcp.tool()
async def search_pubmed_key_words(key_words: str, num_results: int = 10) -> List[Dict[str, Any]]:
    logging.info(f"Searching for articles with key words: {key_words}, num_results: {num_results}")
    """
    Search for articles on PubMed using key words.

    Args:
        key_words: Search query string
        num_results: Number of results to return (default: 10)

    Returns:
        List of dictionaries containing article information
    """
    try:
        results = await asyncio.to_thread(search_key_words, key_words, num_results)
        return results
    except Exception as e:
        return [{"error": f"An error occurred while searching: {str(e)}"}]

@mcp.tool()
async def search_pubmed_advanced(
    term: Optional[str] = None,
    title: Optional[str] = None,
    author: Optional[str] = None,
    journal: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    num_results: int = 10
) -> List[Dict[str, Any]]:
    logging.info(f"Performing advanced search with parameters: {locals()}")
    """
    Perform an advanced search for articles on PubMed.

    Args:
        term: General search term
        title: Search in title
        author: Author name
        journal: Journal name
        start_date: Start date for search range (format: YYYY/MM/DD)
        end_date: End date for search range (format: YYYY/MM/DD)
        num_results: Number of results to return (default: 10)

    Returns:
        List of dictionaries containing article information
    """
    try:
        results = await asyncio.to_thread(
            search_advanced,
            term, title, author, journal, start_date, end_date, num_results
        )
        return results
    except Exception as e:
        return [{"error": f"An error occurred while performing advanced search: {str(e)}"}]

@mcp.tool()
async def get_pubmed_article_metadata(pmid: Union[str, int]) -> Dict[str, Any]:
    logging.info(f"Fetching metadata for PMID: {pmid}")
    """
    Fetch metadata for a PubMed article using its PMID.

    Args:
        pmid: PMID of the article (can be string or integer)

    Returns:
        Dictionary containing article metadata
    """
    try:
        pmid_str = str(pmid)
        metadata = await asyncio.to_thread(get_pubmed_metadata, pmid_str)
        return metadata if metadata else {"error": f"No metadata found for PMID: {pmid_str}"}
    except Exception as e:
        return {"error": f"An error occurred while fetching metadata: {str(e)}"}

@mcp.tool()
async def download_pubmed_pdf(pmid: Union[str, int]) -> str:
    logging.info(f"Attempting to download PDF for PMID: {pmid}")
    """
    Attempt to download the full text PDF for a PubMed article.

    Args:
        pmid: PMID of the article (can be string or integer)

    Returns:
        String indicating the result of the download attempt
    """
    try:
        pmid_str = str(pmid)
        result = await asyncio.to_thread(download_full_text_pdf, pmid_str)
        return result
    except Exception as e:
        return f"An error occurred while attempting to download the PDF: {str(e)}"

@mcp.prompt()
async def deep_paper_analysis(pmid: Union[str, int]) -> str:
    logging.info(f"Performing deep paper analysis for PMID: {pmid}")
    """
    Perform a comprehensive analysis of a PubMed article.

    Args:
        pmid: PMID of the article

    Returns:
        A prompt string for deep analysis of the paper
    """
    try:
        pmid_str = str(pmid)
        metadata = await asyncio.to_thread(get_pubmed_metadata, pmid_str)
        if not metadata:
            return f"No metadata found for PMID: {pmid_str}"

        # 使用导入的 deep_paper_analysis 函数生成分析提示
        # 为避免递归调用，我们需要明确指定导入的函数
        from pubmed_web_search import deep_paper_analysis as web_deep_paper_analysis
        analysis_prompt = await asyncio.to_thread(web_deep_paper_analysis, metadata)
        return analysis_prompt
    except Exception as e:
        return f"An error occurred while performing the deep paper analysis: {str(e)}"

if __name__ == "__main__":
    logging.info("Starting PubMed MCP server")
    # Initialize and run the server
    mcp.run(transport='stdio')
