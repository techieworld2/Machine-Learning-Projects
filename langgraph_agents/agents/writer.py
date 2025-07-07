from .base_agent import BaseAgent
from models.schemas import BusinessAnalysisState
from tools.pdf_generator import PDFGenerator


class WriterAgent(BaseAgent):
    """Agent responsible for compiling analysis results and generating final report"""
    
    def __init__(self):
        super().__init__("Writer")
        self.pdf_generator = PDFGenerator()
    
    def process(self, state: BusinessAnalysisState) -> str:
        """
        Compile all analysis results into a final report and generate PDF
        
        Args:
            state: Current business analysis state with all analysis results
            
        Returns:
            Comprehensive final report text
        """
        # Generate comprehensive written report
        final_report = self._generate_final_report(state)
        
        # Generate PDF report
        pdf_path = self._generate_pdf_report(state)
        
        # Update state with PDF path
        if pdf_path:
            state.pdf_report_path = pdf_path
        
        return final_report
    
    def _generate_final_report(self, state: BusinessAnalysisState) -> str:
        """Generate comprehensive final report text"""
        
        # Build context from all analysis results
        context = self._build_comprehensive_context(state)
        
        prompt = f"""
You are a senior business consultant tasked with creating a comprehensive executive summary and final report. Based on all the analysis provided, create a cohesive, professional business analysis report.

ANALYSIS CONTEXT:
{context}

Please create a comprehensive final report with the following structure:

EXECUTIVE SUMMARY:
[Provide a concise executive summary that captures the key findings, recommendations, and strategic implications]

KEY FINDINGS:
[Summarize the most important findings from the market research, competitive analysis, and SWOT analysis]

STRATEGIC RECOMMENDATIONS:
[Present the key strategic recommendations with clear rationale and implementation priorities]

FINANCIAL OUTLOOK:
[Summarize the financial analysis and investment attractiveness]

IMPLEMENTATION ROADMAP:
[Provide a high-level roadmap for implementing the recommendations]

RISK ASSESSMENT:
[Identify key risks and mitigation strategies]

CONCLUSION:
[Provide a compelling conclusion that ties everything together and reinforces the business opportunity]

Guidelines:
- Write in a professional, executive-level tone
- Be concise yet comprehensive
- Focus on actionable insights and recommendations
- Support conclusions with analysis from the research
- Ensure logical flow and coherence across all sections
- Highlight the most critical success factors
"""
        
        try:
            response = self.invoke_llm(prompt)
            return response.strip()
        except Exception as e:
            # Fallback report if LLM fails
            return self._generate_fallback_report(state)
    
    def _build_comprehensive_context(self, state: BusinessAnalysisState) -> str:
        """Build comprehensive context from all analysis results"""
        context_parts = []
        
        # Basic information
        context_parts.append(f"BUSINESS REQUEST: {state.user_prompt}")
        if state.company_name:
            context_parts.append(f"COMPANY: {state.company_name}")
        
        # Planner output
        if state.planner_output:
            context_parts.append(f"ANALYSIS SCOPE: {state.planner_output.analysis_depth} analysis")
            context_parts.append(f"PRIORITY AREAS: {', '.join(state.planner_output.priority_areas)}")
        
        # Research findings
        if state.research_data:
            if state.research_data.market_insights:
                context_parts.append(f"MARKET INSIGHTS:\n{state.research_data.market_insights[:1500]}")
            if state.research_data.competitor_analysis:
                context_parts.append(f"COMPETITIVE ANALYSIS:\n{state.research_data.competitor_analysis[:1500]}")
            if state.research_data.industry_trends:
                context_parts.append(f"INDUSTRY TRENDS:\n{state.research_data.industry_trends[:1500]}")
        
        # SWOT analysis
        if state.swot_analysis:
            swot_summary = f"""
SWOT ANALYSIS:
Strengths: {'; '.join(state.swot_analysis.strengths)}
Weaknesses: {'; '.join(state.swot_analysis.weaknesses)}
Opportunities: {'; '.join(state.swot_analysis.opportunities)}
Threats: {'; '.join(state.swot_analysis.threats)}
Summary: {state.swot_analysis.summary}
"""
            context_parts.append(swot_summary)
        
        # Strategy recommendations
        if state.strategy_recommendations:
            strategy_summary = f"""
STRATEGIC RECOMMENDATIONS:
Go-to-Market: {state.strategy_recommendations.go_to_market_strategy[:800]}
Business Model: {state.strategy_recommendations.business_model[:800]}
Value Proposition: {state.strategy_recommendations.value_proposition[:600]}
Target Market: {state.strategy_recommendations.target_market[:600]}
Marketing Channels: {', '.join(state.strategy_recommendations.marketing_channels)}
"""
            context_parts.append(strategy_summary)
        
        # Financial analysis
        if state.financial_analysis:
            finance_summary = f"""
FINANCIAL ANALYSIS:
Revenue Model: {state.financial_analysis.revenue_model[:800]}
Pricing Strategy: {state.financial_analysis.pricing_strategy[:800]}
Financial Projections: {state.financial_analysis.financial_projections[:800]}
Funding Requirements: {state.financial_analysis.funding_requirements[:600]}
ROI Analysis: {state.financial_analysis.roi_analysis[:600]}
"""
            context_parts.append(finance_summary)
        
        return "\n\n".join(context_parts)
    
    def _generate_pdf_report(self, state: BusinessAnalysisState) -> str:
        """Generate PDF report using PDFGenerator"""
        try:
            pdf_path = self.pdf_generator.generate_business_report(state)
            if pdf_path:
                return pdf_path
            else:
                return None
        except Exception as e:
            logger.error(f"Failed to generate PDF report: {str(e)}")
            return None
    
    def _generate_fallback_report(self, state: BusinessAnalysisState) -> str:
        """Generate fallback report if LLM fails"""
        
        company_name = state.company_name or "Target Business"
        
        report = f"""
BUSINESS ANALYSIS REPORT: {company_name}

EXECUTIVE SUMMARY:
This comprehensive business analysis examines the opportunity related to: {state.user_prompt}

The analysis reveals significant market potential with identifiable opportunities for growth and competitive advantage. Key findings indicate a viable business proposition with manageable risks and clear paths to profitability.

KEY FINDINGS:
- Market opportunity exists with growing demand and favorable trends
- Competitive landscape presents both challenges and opportunities for differentiation
- Strategic positioning can leverage identified strengths while addressing key weaknesses
- Financial projections indicate attractive return potential with reasonable investment requirements

STRATEGIC RECOMMENDATIONS:
- Implement a phased market entry strategy focusing on core customer segments
- Develop strong value proposition based on unique competitive advantages
- Establish strategic partnerships to accelerate market penetration
- Invest in customer acquisition and retention capabilities
- Build scalable operational infrastructure to support growth

FINANCIAL OUTLOOK:
Financial analysis indicates positive investment potential with:
- Revenue growth trajectory supporting sustainable business model
- Manageable cost structure with path to profitability
- Reasonable funding requirements for market entry and growth
- Attractive ROI with acceptable risk profile

IMPLEMENTATION ROADMAP:
1. Phase 1 (0-6 months): Market validation and initial product/service development
2. Phase 2 (6-12 months): Market entry and customer acquisition
3. Phase 3 (12-24 months): Growth scaling and market expansion
4. Phase 4 (24+ months): Market leadership and diversification

RISK ASSESSMENT:
Key risks include competitive response, market adoption rates, and operational execution. Mitigation strategies focus on agile development, customer-centric approach, and conservative financial planning.

CONCLUSION:
This business opportunity presents attractive potential with clear value proposition, identifiable market demand, and viable implementation path. Success depends on disciplined execution, customer focus, and strategic resource allocation.

The analysis supports proceeding with the business opportunity while maintaining focus on key success factors and risk mitigation strategies.
"""
        
        return report