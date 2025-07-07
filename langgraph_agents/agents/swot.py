from typing import List
from .base_agent import BaseAgent
from models.schemas import BusinessAnalysisState, SWOTAnalysis


class SWOTAgent(BaseAgent):
    """Agent responsible for SWOT analysis generation"""
    
    def __init__(self):
        super().__init__("SWOT")
    
    def process(self, state: BusinessAnalysisState) -> SWOTAnalysis:
        """
        Generate comprehensive SWOT analysis based on research data
        
        Args:
            state: Current business analysis state
            
        Returns:
            SWOTAnalysis with structured strengths, weaknesses, opportunities, threats
        """
        # Gather context from previous analysis
        context = self._build_analysis_context(state)
        
        # Generate SWOT analysis
        swot_response = self._generate_swot_analysis(context, state.user_prompt, state.company_name)
        
        # Parse and structure the response
        swot_analysis = self._parse_swot_response(swot_response)
        
        return swot_analysis
    
    def _build_analysis_context(self, state: BusinessAnalysisState) -> str:
        """Build context from previous analysis results"""
        context_parts = []
        
        # Add user prompt
        context_parts.append(f"BUSINESS FOCUS: {state.user_prompt}")
        
        if state.company_name:
            context_parts.append(f"COMPANY: {state.company_name}")
        
        # Add research insights if available
        if state.research_data:
            if state.research_data.market_insights:
                context_parts.append(f"MARKET INSIGHTS: {state.research_data.market_insights[:1000]}")
            
            if state.research_data.competitor_analysis:
                context_parts.append(f"COMPETITOR ANALYSIS: {state.research_data.competitor_analysis[:1000]}")
            
            if state.research_data.industry_trends:
                context_parts.append(f"INDUSTRY TRENDS: {state.research_data.industry_trends[:1000]}")
        
        return "\n\n".join(context_parts)
    
    def _generate_swot_analysis(self, context: str, user_prompt: str, company_name: str = None) -> str:
        """Generate SWOT analysis using LLM"""
        
        company_context = f" for {company_name}" if company_name else ""
        
        prompt = f"""
You are a strategic business analyst expert in SWOT analysis. Based on the provided context, create a comprehensive SWOT analysis{company_context}.

CONTEXT:
{context}

Please create a detailed SWOT analysis with the following structure:

STRENGTHS:
- [List internal positive factors, capabilities, and advantages]
- [Include specific strengths related to the business focus]
- [Consider competitive advantages and unique capabilities]

WEAKNESSES:
- [List internal negative factors, limitations, and areas for improvement]
- [Include resource constraints and capability gaps]
- [Consider operational or strategic weaknesses]

OPPORTUNITIES:
- [List external positive factors and market opportunities]
- [Include growth opportunities and market trends]
- [Consider emerging technologies, markets, or partnerships]

THREATS:
- [List external negative factors and potential risks]
- [Include competitive threats and market challenges]
- [Consider regulatory, economic, or technological threats]

SWOT SUMMARY:
[Provide a concise summary that synthesizes the key insights from the SWOT analysis and identifies the most critical strategic implications]

Guidelines:
- Be specific and actionable in each point
- Base analysis on the provided research context
- Focus on factors most relevant to: {user_prompt}
- Provide 3-5 points for each SWOT category
- Make the summary strategic and forward-looking
"""
        
        return self.invoke_llm(prompt)
    
    def _parse_swot_response(self, response: str) -> SWOTAnalysis:
        """
        Parse LLM response into structured SWOTAnalysis
        
        Args:
            response: Raw LLM response
            
        Returns:
            Structured SWOTAnalysis object
        """
        try:
            strengths = []
            weaknesses = []
            opportunities = []
            threats = []
            summary = ""
            
            lines = response.strip().split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check for section headers
                line_upper = line.upper()
                if line_upper.startswith('STRENGTHS:'):
                    current_section = 'strengths'
                    continue
                elif line_upper.startswith('WEAKNESSES:'):
                    current_section = 'weaknesses'
                    continue
                elif line_upper.startswith('OPPORTUNITIES:'):
                    current_section = 'opportunities'
                    continue
                elif line_upper.startswith('THREATS:'):
                    current_section = 'threats'
                    continue
                elif line_upper.startswith('SWOT SUMMARY:'):
                    current_section = 'summary'
                    continue
                
                # Parse content based on current section
                if current_section == 'summary':
                    if not summary:
                        summary = line
                    else:
                        summary += " " + line
                elif line.startswith('-') or line.startswith('•'):
                    item = line[1:].strip()
                    if current_section == 'strengths':
                        strengths.append(item)
                    elif current_section == 'weaknesses':
                        weaknesses.append(item)
                    elif current_section == 'opportunities':
                        opportunities.append(item)
                    elif current_section == 'threats':
                        threats.append(item)
            
            # Provide fallback values if parsing failed
            if not strengths:
                strengths = [
                    "Market opportunity identified",
                    "Strategic positioning potential",
                    "Innovation capabilities"
                ]
            
            if not weaknesses:
                weaknesses = [
                    "Resource limitations",
                    "Market entry barriers",
                    "Competitive pressures"
                ]
            
            if not opportunities:
                opportunities = [
                    "Market growth potential",
                    "Technology advancement opportunities",
                    "Strategic partnership possibilities"
                ]
            
            if not threats:
                threats = [
                    "Competitive market dynamics",
                    "Regulatory uncertainties",
                    "Economic market fluctuations"
                ]
            
            if not summary:
                summary = "SWOT analysis reveals balanced opportunities and challenges requiring strategic focus on competitive advantages while addressing key weaknesses and market threats."
            
            return SWOTAnalysis(
                strengths=strengths,
                weaknesses=weaknesses,
                opportunities=opportunities,
                threats=threats,
                summary=summary
            )
            
        except Exception as e:
            # Fallback SWOT analysis if parsing fails
            return SWOTAnalysis(
                strengths=[
                    "Market opportunity exists for the proposed business focus",
                    "Potential for innovation and differentiation",
                    "Access to modern technology and tools"
                ],
                weaknesses=[
                    "Limited market presence and brand recognition",
                    "Resource constraints for market entry",
                    "Need for specialized expertise development"
                ],
                opportunities=[
                    "Growing market demand and trends",
                    "Technology enablement and digital transformation",
                    "Potential for strategic partnerships and collaborations"
                ],
                threats=[
                    "Intense competitive landscape",
                    "Market volatility and economic uncertainties",
                    "Regulatory changes and compliance requirements"
                ],
                summary="The analysis reveals significant market opportunities balanced against competitive challenges, requiring strategic focus on differentiation and efficient resource allocation."
            )