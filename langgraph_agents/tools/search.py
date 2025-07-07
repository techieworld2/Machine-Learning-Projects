import asyncio
import time
from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS
from models.schemas import SearchResult
from utils.logger import logger
from utils.config import Config


class SearchTool:
    """DuckDuckGo search tool for web research"""
    
    def __init__(self):
        self.config = Config.get_search_config()
        self.rate_limit_delay = Config.RATE_LIMIT_DELAY
        
    def search(self, query: str, max_results: Optional[int] = None) -> List[SearchResult]:
        """
        Search for information using DuckDuckGo
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of SearchResult objects
        """
        if max_results is None:
            max_results = self.config["max_results"]
            
        logger.log_tool_usage("SearchTool", f"Searching for: {query}")
        
        try:
            with DDGS() as ddgs:
                # Add rate limiting
                time.sleep(self.rate_limit_delay)
                
                # Perform search
                results = list(ddgs.text(
                    keywords=query,
                    region=self.config["region"],
                    safesearch=self.config["safesearch"],
                    max_results=max_results
                ))
                
                # Convert to SearchResult objects
                search_results = []
                for result in results:
                    search_result = SearchResult(
                        title=result.get("title", ""),
                        url=result.get("href", ""),
                        snippet=result.get("body", ""),
                        source="DuckDuckGo"
                    )
                    search_results.append(search_result)
                
                logger.log_tool_usage("SearchTool", f"Found {len(search_results)} results", f"First result: {search_results[0].title if search_results else 'None'}")
                return search_results
                
        except Exception as e:
            logger.error(f"Search error for query '{query}': {str(e)}")
            return []
    
    def search_multiple_queries(self, queries: List[str], max_results_per_query: Optional[int] = None) -> Dict[str, List[SearchResult]]:
        """
        Search for multiple queries
        
        Args:
            queries: List of search query strings
            max_results_per_query: Maximum results per query
            
        Returns:
            Dictionary mapping queries to their search results
        """
        results = {}
        
        for query in queries:
            logger.debug(f"Searching for query: {query}")
            results[query] = self.search(query, max_results_per_query)
            
            # Rate limiting between queries
            if len(queries) > 1:
                time.sleep(self.rate_limit_delay)
        
        return results
    
    def generate_business_queries(self, user_prompt: str, company_name: Optional[str] = None) -> List[str]:
        """
        Generate relevant search queries for business analysis
        
        Args:
            user_prompt: Original user prompt
            company_name: Optional company name
            
        Returns:
            List of generated search queries
        """
        base_queries = [
            user_prompt,
            f"{user_prompt} market analysis",
            f"{user_prompt} industry trends",
            f"{user_prompt} competitors",
            f"{user_prompt} market size",
        ]
        
        if company_name:
            company_queries = [
                f"{company_name} business model",
                f"{company_name} competitors",
                f"{company_name} market position",
            ]
            base_queries.extend(company_queries)
        
        # Extract key terms from prompt for more specific searches
        prompt_keywords = user_prompt.lower().split()
        key_terms = [word for word in prompt_keywords if len(word) > 3 and word not in ['the', 'and', 'for', 'with', 'that', 'this']]
        
        if key_terms:
            base_queries.extend([
                f"{' '.join(key_terms[:3])} market research",
                f"{' '.join(key_terms[:3])} investment opportunities",
                f"{' '.join(key_terms[:3])} business opportunities",
            ])
        
        # Remove duplicates while preserving order
        unique_queries = []
        seen = set()
        for query in base_queries:
            if query.lower() not in seen:
                unique_queries.append(query)
                seen.add(query.lower())
        
        logger.debug(f"Generated {len(unique_queries)} search queries")
        return unique_queries[:10]  # Limit to 10 queries to avoid rate limiting