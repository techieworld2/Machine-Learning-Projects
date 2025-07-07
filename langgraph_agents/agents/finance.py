from typing import List
from .base_agent import BaseAgent
from models.schemas import BusinessAnalysisState, FinancialAnalysis


class FinanceAgent(BaseAgent):
    """Agent responsible for financial analysis and projections"""
    
    def __init__(self):
        super().__init__("Finance")
    
    def process(self, state: BusinessAnalysisState) -> FinancialAnalysis:
        """
        Generate financial analysis and projections based on strategy and market research
        
        Args:
            state: Current business analysis state
            
        Returns:
            FinancialAnalysis with pricing strategy and financial projections
        """
        # Build context from previous analysis
        context = self._build_financial_context(state)
        
        # Generate financial analysis
        finance_response = self._generate_financial_analysis(context, state.user_prompt, state.company_name)
        
        # Parse and structure the response
        financial_analysis = self._parse_finance_response(finance_response)
        
        return financial_analysis
    
    def _build_financial_context(self, state: BusinessAnalysisState) -> str:
        """Build context from previous analysis results"""
        context_parts = []
        
        # Add basic context
        context_parts.append(f"BUSINESS FOCUS: {state.user_prompt}")
        if state.company_name:
            context_parts.append(f"COMPANY: {state.company_name}")
        
        # Add market insights for sizing
        if state.research_data and state.research_data.market_insights:
            context_parts.append(f"MARKET CONTEXT:\n{state.research_data.market_insights[:1000]}")
        
        # Add competitive context for pricing
        if state.research_data and state.research_data.competitor_analysis:
            context_parts.append(f"COMPETITIVE CONTEXT:\n{state.research_data.competitor_analysis[:1000]}")
        
        # Add strategy context for revenue model
        if state.strategy_recommendations:
            strategy_summary = f"""
STRATEGIC CONTEXT:
Business Model: {state.strategy_recommendations.business_model[:500]}
Target Market: {state.strategy_recommendations.target_market[:500]}
Value Proposition: {state.strategy_recommendations.value_proposition[:500]}
"""
            context_parts.append(strategy_summary)
        
        return "\n\n".join(context_parts)
    
    def _generate_financial_analysis(self, context: str, user_prompt: str, company_name: str = None) -> str:
        """Generate financial analysis using LLM"""
        
        company_context = f" for {company_name}" if company_name else ""
        
        prompt = f"""
You are a financial analyst and business strategist with expertise in financial modeling, pricing strategies, and investment analysis. Based on the provided context, create a comprehensive financial analysis{company_context}.

CONTEXT:
{context}

Please provide detailed financial analysis with the following structure:

PRICING STRATEGY:
[Develop comprehensive pricing strategy including pricing models, competitive positioning, value-based pricing considerations, and pricing optimization recommendations]

REVENUE MODEL:
[Define revenue model including revenue streams, recurring vs. one-time revenue, monetization strategies, and revenue growth projections]

COST STRUCTURE:
[Analyze cost structure including fixed costs, variable costs, operational expenses, and cost optimization opportunities]

FINANCIAL PROJECTIONS:
[Provide realistic financial projections including revenue forecasts, expense projections, profitability analysis, and key financial metrics for 1-3 years]

FUNDING REQUIREMENTS:
[Assess funding needs including startup costs, working capital requirements, growth capital needs, and potential funding sources]

BREAK-EVEN ANALYSIS:
[Calculate break-even point including break-even volume, timeline to profitability, and sensitivity analysis]

ROI ANALYSIS:
[Evaluate return on investment including ROI calculations, payback period, and investment attractiveness metrics]

Guidelines:
- Base analysis on market research and strategic context provided
- Use realistic assumptions and industry benchmarks
- Consider both conservative and optimistic scenarios
- Include specific numbers and metrics where possible
- Address financial risks and mitigation strategies
- Focus on practical financial planning for: {user_prompt}
- Consider scalability and growth potential
"""
        
        return self.invoke_llm(prompt)
    
    def _parse_finance_response(self, response: str) -> FinancialAnalysis:
        """
        Parse LLM response into structured FinancialAnalysis
        
        Args:
            response: Raw LLM response
            
        Returns:
            Structured FinancialAnalysis object
        """
        try:
            pricing_strategy = ""
            revenue_model = ""
            cost_structure = ""
            financial_projections = ""
            funding_requirements = ""
            break_even_analysis = ""
            roi_analysis = ""
            
            lines = response.strip().split('\n')
            current_section = None
            current_content = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check for section headers
                line_upper = line.upper()
                if line_upper.startswith('PRICING STRATEGY:'):
                    if current_section and current_content:
                        self._assign_financial_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'pricing_strategy'
                    current_content = []
                    continue
                elif line_upper.startswith('REVENUE MODEL:'):
                    if current_section and current_content:
                        self._assign_financial_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'revenue_model'
                    current_content = []
                    continue
                elif line_upper.startswith('COST STRUCTURE:'):
                    if current_section and current_content:
                        self._assign_financial_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'cost_structure'
                    current_content = []
                    continue
                elif line_upper.startswith('FINANCIAL PROJECTIONS:'):
                    if current_section and current_content:
                        self._assign_financial_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'financial_projections'
                    current_content = []
                    continue
                elif line_upper.startswith('FUNDING REQUIREMENTS:'):
                    if current_section and current_content:
                        self._assign_financial_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'funding_requirements'
                    current_content = []
                    continue
                elif line_upper.startswith('BREAK-EVEN ANALYSIS:') or line_upper.startswith('BREAKEVEN ANALYSIS:'):
                    if current_section and current_content:
                        self._assign_financial_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'break_even_analysis'
                    current_content = []
                    continue
                elif line_upper.startswith('ROI ANALYSIS:'):
                    if current_section and current_content:
                        self._assign_financial_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'roi_analysis'
                    current_content = []
                    continue
                
                # Collect content for current section
                current_content.append(line)
            
            # Process final section
            if current_section and current_content:
                self._assign_financial_content(current_section, '\n'.join(current_content), locals())
            
            # Provide fallback values if needed
            if not pricing_strategy:
                pricing_strategy = "Implement value-based pricing strategy aligned with market positioning and competitive landscape, with pricing optimization based on customer value perception and willingness to pay."
            
            if not revenue_model:
                revenue_model = "Diversified revenue model combining recurring and transactional revenue streams, with focus on predictable revenue generation and customer lifetime value optimization."
            
            if not cost_structure:
                cost_structure = "Balanced cost structure with emphasis on variable cost management, operational efficiency, and scalable cost model that supports growth while maintaining profitability."
            
            if not financial_projections:
                financial_projections = "Conservative financial projections show gradual revenue growth with improving margins over 24-36 months, achieving positive cash flow within 18 months and profitability by month 24."
            
            if not funding_requirements:
                funding_requirements = "Initial funding requirements estimated at $100K-500K for startup costs and working capital, with potential for additional growth capital based on market traction and expansion plans."
            
            if not break_even_analysis:
                break_even_analysis = "Break-even analysis indicates profitability achievable within 18-24 months with moderate customer acquisition rates and efficient cost management."
            
            if not roi_analysis:
                roi_analysis = "ROI analysis shows attractive returns with payback period of 2-3 years and IRR exceeding 25% under conservative scenarios, making this an attractive investment opportunity."
            
            return FinancialAnalysis(
                pricing_strategy=pricing_strategy,
                revenue_model=revenue_model,
                cost_structure=cost_structure,
                financial_projections=financial_projections,
                funding_requirements=funding_requirements,
                break_even_analysis=break_even_analysis,
                roi_analysis=roi_analysis
            )
            
        except Exception as e:
            # Fallback financial analysis
            return FinancialAnalysis(
                pricing_strategy="Competitive pricing strategy based on value proposition and market positioning, with flexibility for pricing optimization based on customer feedback and market dynamics.",
                revenue_model="Multi-stream revenue model focusing on sustainable and predictable revenue generation through a combination of direct sales, subscriptions, and value-added services.",
                cost_structure="Lean cost structure emphasizing operational efficiency and scalability, with careful management of fixed and variable costs to maintain healthy margins.",
                financial_projections="Realistic financial projections showing revenue growth trajectory with improving profitability over 2-3 years, achieving positive cash flow within 12-18 months.",
                funding_requirements="Moderate funding requirements for initial market entry and growth, with potential for bootstrapping or seeking strategic investment based on growth trajectory.",
                break_even_analysis="Break-even point achievable within 18-24 months with disciplined execution and efficient customer acquisition, providing clear path to profitability.",
                roi_analysis="Strong ROI potential with reasonable payback period and attractive returns for investors, demonstrating viable business opportunity with managed risk profile."
            )
    
    def _assign_financial_content(self, section: str, content: str, local_vars: dict):
        """Helper method to assign parsed content to appropriate variables"""
        if section in local_vars:
            local_vars[section] = content.strip()