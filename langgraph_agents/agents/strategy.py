from typing import List
from .base_agent import BaseAgent
from models.schemas import BusinessAnalysisState, StrategyRecommendations


class StrategyAgent(BaseAgent):
    """Agent responsible for strategic recommendations and go-to-market planning"""
    
    def __init__(self):
        super().__init__("Strategy")
    
    def process(self, state: BusinessAnalysisState) -> StrategyRecommendations:
        """
        Generate strategic recommendations based on research and SWOT analysis
        
        Args:
            state: Current business analysis state
            
        Returns:
            StrategyRecommendations with go-to-market strategy and business model
        """
        # Build context from previous analysis
        context = self._build_strategy_context(state)
        
        # Generate strategy recommendations
        strategy_response = self._generate_strategy_recommendations(context, state.user_prompt, state.company_name)
        
        # Parse and structure the response
        strategy_recommendations = self._parse_strategy_response(strategy_response)
        
        return strategy_recommendations
    
    def _build_strategy_context(self, state: BusinessAnalysisState) -> str:
        """Build context from previous analysis results"""
        context_parts = []
        
        # Add basic context
        context_parts.append(f"BUSINESS FOCUS: {state.user_prompt}")
        if state.company_name:
            context_parts.append(f"COMPANY: {state.company_name}")
        
        # Add research insights
        if state.research_data:
            if state.research_data.market_insights:
                context_parts.append(f"MARKET INSIGHTS:\n{state.research_data.market_insights[:1200]}")
            
            if state.research_data.competitor_analysis:
                context_parts.append(f"COMPETITIVE LANDSCAPE:\n{state.research_data.competitor_analysis[:1200]}")
        
        # Add SWOT analysis
        if state.swot_analysis:
            swot_summary = f"""
SWOT ANALYSIS:
Strengths: {', '.join(state.swot_analysis.strengths[:3])}
Weaknesses: {', '.join(state.swot_analysis.weaknesses[:3])}
Opportunities: {', '.join(state.swot_analysis.opportunities[:3])}
Threats: {', '.join(state.swot_analysis.threats[:3])}
Summary: {state.swot_analysis.summary}
"""
            context_parts.append(swot_summary)
        
        return "\n\n".join(context_parts)
    
    def _generate_strategy_recommendations(self, context: str, user_prompt: str, company_name: str = None) -> str:
        """Generate strategic recommendations using LLM"""
        
        company_context = f" for {company_name}" if company_name else ""
        
        prompt = f"""
You are a strategic business consultant with expertise in go-to-market strategies and business model development. Based on the provided analysis, create comprehensive strategic recommendations{company_context}.

ANALYSIS CONTEXT:
{context}

Please provide detailed strategic recommendations with the following structure:

GO-TO-MARKET STRATEGY:
[Provide a comprehensive go-to-market strategy including market entry approach, launch timeline, and key milestones]

BUSINESS MODEL:
[Define the business model including value creation, delivery mechanisms, and revenue generation approach]

TARGET MARKET:
[Identify and describe the primary target market segments, customer personas, and market sizing]

VALUE PROPOSITION:
[Articulate the unique value proposition and key differentiators that address customer needs]

COMPETITIVE ADVANTAGE:
[Define sustainable competitive advantages and differentiation strategies]

MARKETING CHANNELS:
- [List specific marketing and distribution channels]
- [Include both digital and traditional channels as appropriate]
- [Consider channel partnerships and strategic alliances]

IMPLEMENTATION TIMELINE:
[Provide a realistic timeline for strategy implementation with key phases and milestones]

Guidelines:
- Be specific and actionable in all recommendations
- Base strategies on the provided research and SWOT analysis
- Focus on practical implementation considerations
- Consider resource requirements and constraints
- Align strategies with identified market opportunities
- Address competitive threats and market challenges
- Ensure recommendations are relevant to: {user_prompt}
"""
        
        return self.invoke_llm(prompt)
    
    def _parse_strategy_response(self, response: str) -> StrategyRecommendations:
        """
        Parse LLM response into structured StrategyRecommendations
        
        Args:
            response: Raw LLM response
            
        Returns:
            Structured StrategyRecommendations object
        """
        try:
            go_to_market_strategy = ""
            business_model = ""
            target_market = ""
            value_proposition = ""
            competitive_advantage = ""
            marketing_channels = []
            implementation_timeline = ""
            
            lines = response.strip().split('\n')
            current_section = None
            current_content = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check for section headers
                line_upper = line.upper()
                if line_upper.startswith('GO-TO-MARKET STRATEGY:'):
                    if current_section and current_content:
                        self._assign_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'go_to_market_strategy'
                    current_content = []
                    continue
                elif line_upper.startswith('BUSINESS MODEL:'):
                    if current_section and current_content:
                        self._assign_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'business_model'
                    current_content = []
                    continue
                elif line_upper.startswith('TARGET MARKET:'):
                    if current_section and current_content:
                        self._assign_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'target_market'
                    current_content = []
                    continue
                elif line_upper.startswith('VALUE PROPOSITION:'):
                    if current_section and current_content:
                        self._assign_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'value_proposition'
                    current_content = []
                    continue
                elif line_upper.startswith('COMPETITIVE ADVANTAGE:'):
                    if current_section and current_content:
                        self._assign_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'competitive_advantage'
                    current_content = []
                    continue
                elif line_upper.startswith('MARKETING CHANNELS:'):
                    if current_section and current_content:
                        self._assign_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'marketing_channels'
                    current_content = []
                    continue
                elif line_upper.startswith('IMPLEMENTATION TIMELINE:'):
                    if current_section and current_content:
                        self._assign_content(current_section, '\n'.join(current_content), locals())
                    current_section = 'implementation_timeline'
                    current_content = []
                    continue
                
                # Collect content for current section
                if current_section == 'marketing_channels' and (line.startswith('-') or line.startswith('•')):
                    marketing_channels.append(line[1:].strip())
                else:
                    current_content.append(line)
            
            # Process final section
            if current_section and current_content:
                self._assign_content(current_section, '\n'.join(current_content), locals())
            
            # Provide fallback values if needed
            if not go_to_market_strategy:
                go_to_market_strategy = "Implement a phased market entry approach focusing on customer validation, product-market fit, and scalable growth strategies."
            
            if not business_model:
                business_model = "Value-driven business model focusing on customer needs, sustainable revenue generation, and scalable operations."
            
            if not target_market:
                target_market = "Primary target market consists of early adopters and organizations seeking innovative solutions in the identified market segment."
            
            if not value_proposition:
                value_proposition = "Unique value proposition based on market research insights, addressing key customer pain points and unmet needs."
            
            if not competitive_advantage:
                competitive_advantage = "Sustainable competitive advantage through innovation, customer focus, and operational excellence."
            
            if not marketing_channels:
                marketing_channels = [
                    "Digital marketing and online presence",
                    "Content marketing and thought leadership",
                    "Strategic partnerships and alliances",
                    "Direct sales and customer outreach"
                ]
            
            if not implementation_timeline:
                implementation_timeline = "Phased implementation over 6-12 months with key milestones for market entry, customer acquisition, and growth scaling."
            
            return StrategyRecommendations(
                go_to_market_strategy=go_to_market_strategy,
                business_model=business_model,
                target_market=target_market,
                value_proposition=value_proposition,
                competitive_advantage=competitive_advantage,
                marketing_channels=marketing_channels,
                implementation_timeline=implementation_timeline
            )
            
        except Exception as e:
            # Fallback strategy recommendations
            return StrategyRecommendations(
                go_to_market_strategy="Develop a comprehensive market entry strategy focusing on customer validation, iterative product development, and strategic partnerships to establish market presence.",
                business_model="Implement a sustainable business model that balances value creation for customers with profitable revenue generation through multiple revenue streams.",
                target_market="Focus on early adopters and market segments with clear pain points that align with the proposed solution, prioritizing customers with high willingness to pay.",
                value_proposition="Create compelling value proposition that clearly differentiates from competitors while addressing core customer needs and delivering measurable benefits.",
                competitive_advantage="Build sustainable competitive advantages through innovation, customer relationships, operational efficiency, and strategic market positioning.",
                marketing_channels=[
                    "Digital marketing and social media engagement",
                    "Content marketing and educational resources",
                    "Strategic partnerships and channel development",
                    "Direct sales and customer relationship building",
                    "Industry events and networking opportunities"
                ],
                implementation_timeline="Execute strategy over 9-12 months with quarterly milestones for market validation, product development, customer acquisition, and scaling operations."
            )
    
    def _assign_content(self, section: str, content: str, local_vars: dict):
        """Helper method to assign parsed content to appropriate variables"""
        if section in local_vars:
            local_vars[section] = content.strip()