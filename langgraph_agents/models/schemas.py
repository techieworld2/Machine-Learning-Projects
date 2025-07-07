from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class SearchResult(BaseModel):
    """Model for individual search results"""
    title: str
    url: str
    snippet: str
    source: str


class ResearchData(BaseModel):
    """Model for research agent output"""
    search_queries: List[str] = Field(default_factory=list)
    search_results: List[SearchResult] = Field(default_factory=list)
    scraped_content: List[str] = Field(default_factory=list)
    market_insights: str = ""
    competitor_analysis: str = ""
    industry_trends: str = ""


class SWOTAnalysis(BaseModel):
    """Model for SWOT analysis output"""
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    threats: List[str] = Field(default_factory=list)
    summary: str = ""


class StrategyRecommendations(BaseModel):
    """Model for strategy agent output"""
    go_to_market_strategy: str = ""
    business_model: str = ""
    target_market: str = ""
    value_proposition: str = ""
    competitive_advantage: str = ""
    marketing_channels: List[str] = Field(default_factory=list)
    implementation_timeline: str = ""


class FinancialAnalysis(BaseModel):
    """Model for finance agent output"""
    pricing_strategy: str = ""
    revenue_model: str = ""
    cost_structure: str = ""
    financial_projections: str = ""
    funding_requirements: str = ""
    break_even_analysis: str = ""
    roi_analysis: str = ""


class PlannerOutput(BaseModel):
    """Model for planner agent output"""
    task_breakdown: List[str] = Field(default_factory=list)
    research_focus_areas: List[str] = Field(default_factory=list)
    analysis_depth: str = "standard"
    priority_areas: List[str] = Field(default_factory=list)
    estimated_timeline: str = ""


class BusinessAnalysisState(BaseModel):
    """Main state model for the entire business analysis workflow"""
    # Input
    user_prompt: str
    company_name: Optional[str] = None
    
    # Planner output
    planner_output: Optional[PlannerOutput] = None
    
    # Research phase
    research_data: Optional[ResearchData] = None
    
    # Analysis phases
    swot_analysis: Optional[SWOTAnalysis] = None
    strategy_recommendations: Optional[StrategyRecommendations] = None
    financial_analysis: Optional[FinancialAnalysis] = None
    
    # Final output
    final_report: str = ""
    pdf_report_path: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    processing_time: Optional[float] = None
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    
    # Status tracking
    current_step: str = "initialized"
    completed_steps: List[str] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True


class AgentResponse(BaseModel):
    """Generic model for agent responses"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    processing_time: Optional[float] = None


class ModelConfig(BaseModel):
    """Configuration for LLM models"""
    model_name: str = "mistral:7b"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 30


class ToolConfig(BaseModel):
    """Configuration for tools"""
    search_max_results: int = 10
    search_region: str = "wt-wt"
    search_safesearch: str = "moderate"
    scraper_timeout: int = 10
    pdf_output_dir: str = "./reports"
    pdf_template_dir: str = "./templates"