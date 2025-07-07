import os
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
import weasyprint
from utils.logger import logger
from utils.config import Config
from models.schemas import BusinessAnalysisState


class PDFGenerator:
    """PDF generation tool using WeasyPrint"""
    
    def __init__(self):
        self.output_dir = Path(Config.PDF_OUTPUT_DIR)
        self.template_dir = Path(Config.PDF_TEMPLATE_DIR)
        
        # Ensure directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.template_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_business_report(self, state: BusinessAnalysisState) -> Optional[str]:
        """
        Generate a comprehensive business analysis PDF report
        
        Args:
            state: BusinessAnalysisState containing all analysis data
            
        Returns:
            Path to generated PDF file or None if failed
        """
        logger.log_tool_usage("PDFGenerator", "Generating business analysis report")
        
        try:
            # Generate HTML content
            html_content = self._generate_html_content(state)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            company_name = state.company_name or "Business_Analysis"
            filename = f"{company_name}_{timestamp}_{str(uuid.uuid4())[:8]}.pdf"
            pdf_path = self.output_dir / filename
            
            # Generate PDF
            css_content = self._get_css_styles()
            weasyprint.HTML(string=html_content).write_pdf(
                str(pdf_path),
                stylesheets=[weasyprint.CSS(string=css_content)]
            )
            
            logger.log_tool_usage("PDFGenerator", f"PDF generated successfully: {pdf_path}")
            return str(pdf_path)
            
        except Exception as e:
            logger.error(f"Failed to generate PDF: {str(e)}")
            return None
    
    def _generate_html_content(self, state: BusinessAnalysisState) -> str:
        """
        Generate HTML content for the business report
        
        Args:
            state: BusinessAnalysisState containing analysis data
            
        Returns:
            HTML content string
        """
        # Extract data from state
        company_name = state.company_name or "Target Company"
        user_prompt = state.user_prompt
        
        # Safe access to nested objects
        planner = state.planner_output
        research = state.research_data
        swot = state.swot_analysis
        strategy = state.strategy_recommendations
        finance = state.financial_analysis
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Business Analysis Report - {company_name}</title>
        </head>
        <body>
            <div class="header">
                <h1>Business Analysis Report</h1>
                <h2>{company_name}</h2>
                <p class="date">Generated on {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <div class="executive-summary">
                <h2>Executive Summary</h2>
                <div class="prompt-box">
                    <h3>Analysis Request</h3>
                    <p>{user_prompt}</p>
                </div>
            </div>
            
            {self._generate_planner_section(planner)}
            {self._generate_research_section(research)}
            {self._generate_swot_section(swot)}
            {self._generate_strategy_section(strategy)}
            {self._generate_finance_section(finance)}
            
            <div class="footer">
                <p>This report was generated using AI-powered business analysis tools.</p>
                <p>Report ID: {str(uuid.uuid4())[:8]}</p>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _generate_planner_section(self, planner) -> str:
        """Generate HTML for planner section"""
        if not planner:
            return ""
        
        return f"""
        <div class="section">
            <h2>📋 Analysis Planning</h2>
            <div class="subsection">
                <h3>Task Breakdown</h3>
                <ul>
                    {self._generate_list_items(planner.task_breakdown)}
                </ul>
            </div>
            <div class="subsection">
                <h3>Research Focus Areas</h3>
                <ul>
                    {self._generate_list_items(planner.research_focus_areas)}
                </ul>
            </div>
            <div class="subsection">
                <h3>Priority Areas</h3>
                <ul>
                    {self._generate_list_items(planner.priority_areas)}
                </ul>
            </div>
        </div>
        """
    
    def _generate_research_section(self, research) -> str:
        """Generate HTML for research section"""
        if not research:
            return ""
        
        return f"""
        <div class="section">
            <h2>🔍 Market Research</h2>
            <div class="subsection">
                <h3>Market Insights</h3>
                <p>{research.market_insights or 'No market insights available.'}</p>
            </div>
            <div class="subsection">
                <h3>Competitor Analysis</h3>
                <p>{research.competitor_analysis or 'No competitor analysis available.'}</p>
            </div>
            <div class="subsection">
                <h3>Industry Trends</h3>
                <p>{research.industry_trends or 'No industry trends available.'}</p>
            </div>
            <div class="subsection">
                <h3>Research Sources</h3>
                <p>Based on analysis of {len(research.search_results)} web sources and {len(research.scraped_content)} detailed content reviews.</p>
            </div>
        </div>
        """
    
    def _generate_swot_section(self, swot) -> str:
        """Generate HTML for SWOT section"""
        if not swot:
            return ""
        
        return f"""
        <div class="section">
            <h2>📊 SWOT Analysis</h2>
            <div class="swot-grid">
                <div class="swot-item strengths">
                    <h3>💪 Strengths</h3>
                    <ul>
                        {self._generate_list_items(swot.strengths)}
                    </ul>
                </div>
                <div class="swot-item weaknesses">
                    <h3>⚠️ Weaknesses</h3>
                    <ul>
                        {self._generate_list_items(swot.weaknesses)}
                    </ul>
                </div>
                <div class="swot-item opportunities">
                    <h3>🚀 Opportunities</h3>
                    <ul>
                        {self._generate_list_items(swot.opportunities)}
                    </ul>
                </div>
                <div class="swot-item threats">
                    <h3>⚡ Threats</h3>
                    <ul>
                        {self._generate_list_items(swot.threats)}
                    </ul>
                </div>
            </div>
            <div class="subsection">
                <h3>SWOT Summary</h3>
                <p>{swot.summary or 'No SWOT summary available.'}</p>
            </div>
        </div>
        """
    
    def _generate_strategy_section(self, strategy) -> str:
        """Generate HTML for strategy section"""
        if not strategy:
            return ""
        
        return f"""
        <div class="section">
            <h2>🎯 Strategic Recommendations</h2>
            <div class="subsection">
                <h3>Go-to-Market Strategy</h3>
                <p>{strategy.go_to_market_strategy or 'No go-to-market strategy available.'}</p>
            </div>
            <div class="subsection">
                <h3>Business Model</h3>
                <p>{strategy.business_model or 'No business model available.'}</p>
            </div>
            <div class="subsection">
                <h3>Target Market</h3>
                <p>{strategy.target_market or 'No target market analysis available.'}</p>
            </div>
            <div class="subsection">
                <h3>Value Proposition</h3>
                <p>{strategy.value_proposition or 'No value proposition available.'}</p>
            </div>
            <div class="subsection">
                <h3>Competitive Advantage</h3>
                <p>{strategy.competitive_advantage or 'No competitive advantage analysis available.'}</p>
            </div>
            <div class="subsection">
                <h3>Marketing Channels</h3>
                <ul>
                    {self._generate_list_items(strategy.marketing_channels)}
                </ul>
            </div>
        </div>
        """
    
    def _generate_finance_section(self, finance) -> str:
        """Generate HTML for finance section"""
        if not finance:
            return ""
        
        return f"""
        <div class="section">
            <h2>💰 Financial Analysis</h2>
            <div class="subsection">
                <h3>Pricing Strategy</h3>
                <p>{finance.pricing_strategy or 'No pricing strategy available.'}</p>
            </div>
            <div class="subsection">
                <h3>Revenue Model</h3>
                <p>{finance.revenue_model or 'No revenue model available.'}</p>
            </div>
            <div class="subsection">
                <h3>Cost Structure</h3>
                <p>{finance.cost_structure or 'No cost structure analysis available.'}</p>
            </div>
            <div class="subsection">
                <h3>Financial Projections</h3>
                <p>{finance.financial_projections or 'No financial projections available.'}</p>
            </div>
            <div class="subsection">
                <h3>Funding Requirements</h3>
                <p>{finance.funding_requirements or 'No funding requirements analysis available.'}</p>
            </div>
        </div>
        """
    
    def _generate_list_items(self, items: list) -> str:
        """Generate HTML list items from a list of strings"""
        if not items:
            return "<li>No items available</li>"
        
        return "\n".join([f"<li>{item}</li>" for item in items])
    
    def _get_css_styles(self) -> str:
        """Get CSS styles for the PDF"""
        return """
        @page {
            margin: 2cm;
            @top-center {
                content: "Business Analysis Report";
                font-size: 10pt;
                color: #666;
            }
            @bottom-center {
                content: counter(page);
                font-size: 10pt;
                color: #666;
            }
        }
        
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            font-size: 11pt;
        }
        
        .header {
            text-align: center;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 24pt;
            margin-bottom: 10px;
        }
        
        .header h2 {
            color: #34495e;
            font-size: 18pt;
            margin-bottom: 10px;
        }
        
        .date {
            color: #7f8c8d;
            font-style: italic;
        }
        
        .section {
            margin-bottom: 25px;
            page-break-inside: avoid;
        }
        
        .section h2 {
            color: #2c3e50;
            font-size: 16pt;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
            margin-bottom: 15px;
        }
        
        .subsection {
            margin-bottom: 15px;
        }
        
        .subsection h3 {
            color: #34495e;
            font-size: 13pt;
            margin-bottom: 8px;
        }
        
        .prompt-box {
            background-color: #ecf0f1;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin-bottom: 20px;
        }
        
        .swot-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .swot-item {
            padding: 15px;
            border-radius: 5px;
        }
        
        .strengths {
            background-color: #d5f4e6;
            border-left: 4px solid #27ae60;
        }
        
        .weaknesses {
            background-color: #fdeaea;
            border-left: 4px solid #e74c3c;
        }
        
        .opportunities {
            background-color: #e8f5e8;
            border-left: 4px solid #2ecc71;
        }
        
        .threats {
            background-color: #fff3cd;
            border-left: 4px solid #f39c12;
        }
        
        ul {
            margin-bottom: 10px;
        }
        
        li {
            margin-bottom: 5px;
        }
        
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #bdc3c7;
            text-align: center;
            color: #7f8c8d;
            font-size: 9pt;
        }
        """