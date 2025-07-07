from typing import List, Dict
from .base_agent import BaseAgent
from models.schemas import BusinessAnalysisState, ResearchData, SearchResult
from tools.search import SearchTool
from tools.scraper import WebScraperTool


class ResearchAgent(BaseAgent):
    """Agent responsible for web research and data gathering"""
    
    def __init__(self):
        super().__init__("Research")
        self.search_tool = SearchTool()
        self.scraper_tool = WebScraperTool()
    
    def process(self, state: BusinessAnalysisState) -> ResearchData:
        """
        Conduct comprehensive web research based on the analysis plan
        
        Args:
            state: Current business analysis state
            
        Returns:
            ResearchData with search results and analysis
        """
        # Generate search queries
        search_queries = self._generate_search_queries(state)
        
        # Perform searches
        search_results = self._perform_searches(search_queries)
        
        # Scrape detailed content from top results
        scraped_content = self._scrape_content(search_results)
        
        # Analyze the gathered data
        market_insights = self._analyze_market_insights(scraped_content, state.user_prompt)
        competitor_analysis = self._analyze_competitors(scraped_content, state.user_prompt)
        industry_trends = self._analyze_industry_trends(scraped_content, state.user_prompt)
        
        return ResearchData(
            search_queries=search_queries,
            search_results=search_results,
            scraped_content=scraped_content,
            market_insights=market_insights,
            competitor_analysis=competitor_analysis,
            industry_trends=industry_trends
        )
    
    def _generate_search_queries(self, state: BusinessAnalysisState) -> List[str]:
        """Generate targeted search queries based on the analysis plan"""
        
        # Use planner output if available, otherwise generate basic queries
        if state.planner_output and state.planner_output.research_focus_areas:
            focus_areas = state.planner_output.research_focus_areas
            queries = []
            
            for area in focus_areas:
                queries.extend([
                    f"{state.user_prompt} {area}",
                    f"{area} market analysis",
                    f"{area} industry trends"
                ])
        else:
            # Fallback to basic query generation
            queries = self.search_tool.generate_business_queries(
                state.user_prompt, 
                state.company_name
            )
        
        return queries[:8]  # Limit to 8 queries to avoid rate limiting
    
    def _perform_searches(self, queries: List[str]) -> List[SearchResult]:
        """Perform searches for all queries and collect results"""
        all_results = []
        
        for query in queries:
            try:
                results = self.search_tool.search(query, max_results=5)
                all_results.extend(results)
            except Exception as e:
                logger.warning(f"Search failed for query '{query}': {str(e)}")
                continue
        
        # Remove duplicates based on URL
        unique_results = []
        seen_urls = set()
        
        for result in all_results:
            if result.url not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result.url)
        
        return unique_results[:20]  # Limit to top 20 results
    
    def _scrape_content(self, search_results: List[SearchResult]) -> List[str]:
        """Scrape detailed content from search results"""
        
        # Filter and prioritize URLs for scraping
        urls_to_scrape = []
        for result in search_results[:10]:  # Limit to top 10 for scraping
            if self.scraper_tool.is_valid_url(result.url):
                urls_to_scrape.append(result.url)
        
        # Scrape content
        scraped_content = self.scraper_tool.scrape_multiple_urls(urls_to_scrape)
        
        return scraped_content
    
    def _analyze_market_insights(self, content_list: List[str], user_prompt: str) -> str:
        """Analyze scraped content for market insights"""
        
        # Combine content for analysis
        combined_content = "\n\n".join(content_list[:5])  # Limit content for prompt size
        
        prompt = f"""
Based on the following research content, provide comprehensive market insights related to: {user_prompt}

RESEARCH CONTENT:
{combined_content[:4000]}  # Limit content size

Please analyze and provide insights on:
1. Market size and potential
2. Market growth trends
3. Key market drivers
4. Customer segments and needs
5. Market barriers and challenges
6. Regulatory environment

Focus on actionable insights that would be valuable for business decision-making. Be specific and cite relevant data points when available.

MARKET INSIGHTS:
"""
        
        try:
            response = self.invoke_llm(prompt)
            return response.strip()
        except Exception as e:
            return f"Market insights analysis unavailable due to: {str(e)}"
    
    def _analyze_competitors(self, content_list: List[str], user_prompt: str) -> str:
        """Analyze scraped content for competitor information"""
        
        combined_content = "\n\n".join(content_list[:5])
        
        prompt = f"""
Based on the following research content, provide a comprehensive competitor analysis related to: {user_prompt}

RESEARCH CONTENT:
{combined_content[:4000]}

Please analyze and provide insights on:
1. Key competitors and market leaders
2. Competitor strengths and weaknesses
3. Competitive positioning
4. Pricing strategies
5. Market share distribution
6. Competitive advantages and differentiators

Focus on actionable competitive intelligence that would inform strategic decisions.

COMPETITOR ANALYSIS:
"""
        
        try:
            response = self.invoke_llm(prompt)
            return response.strip()
        except Exception as e:
            return f"Competitor analysis unavailable due to: {str(e)}"
    
    def _analyze_industry_trends(self, content_list: List[str], user_prompt: str) -> str:
        """Analyze scraped content for industry trends"""
        
        combined_content = "\n\n".join(content_list[:5])
        
        prompt = f"""
Based on the following research content, identify and analyze key industry trends related to: {user_prompt}

RESEARCH CONTENT:
{combined_content[:4000]}

Please analyze and provide insights on:
1. Emerging industry trends
2. Technology innovations and disruptions
3. Consumer behavior changes
4. Regulatory changes and implications
5. Economic factors affecting the industry
6. Future outlook and predictions

Focus on trends that would significantly impact business strategy and decision-making.

INDUSTRY TRENDS:
"""
        
        try:
            response = self.invoke_llm(prompt)
            return response.strip()
        except Exception as e:
            return f"Industry trends analysis unavailable due to: {str(e)}"