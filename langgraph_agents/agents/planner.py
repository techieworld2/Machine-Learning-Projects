from typing import List
from .base_agent import BaseAgent
from models.schemas import BusinessAnalysisState, PlannerOutput


class PlannerAgent(BaseAgent):
    """Agent responsible for task decomposition and workflow coordination"""
    
    def __init__(self):
        super().__init__("Planner")
    
    def process(self, state: BusinessAnalysisState) -> PlannerOutput:
        """
        Analyze the user prompt and create a comprehensive analysis plan
        
        Args:
            state: Current business analysis state
            
        Returns:
            PlannerOutput with task breakdown and analysis plan
        """
        prompt = self._create_planning_prompt(state.user_prompt, state.company_name)
        
        response = self.invoke_llm(prompt)
        
        # Parse the response into structured output
        planner_output = self._parse_planning_response(response, state.user_prompt)
        
        return planner_output
    
    def _create_planning_prompt(self, user_prompt: str, company_name: str = None) -> str:
        """Create planning prompt for the LLM"""
        
        company_context = f" for {company_name}" if company_name else ""
        
        prompt = f"""
You are a strategic business planning expert. Your role is to analyze the following business request and create a comprehensive analysis plan.

BUSINESS REQUEST: {user_prompt}
COMPANY: {company_name or "Not specified"}

Please create a detailed analysis plan that includes:

1. TASK BREAKDOWN - Break down the analysis into specific, actionable tasks
2. RESEARCH FOCUS AREAS - Identify key areas that need research and investigation
3. ANALYSIS DEPTH - Determine the appropriate level of analysis (basic, standard, comprehensive)
4. PRIORITY AREAS - Identify the most critical aspects to focus on
5. ESTIMATED TIMELINE - Provide a realistic timeline for completion

Consider the following aspects in your planning:
- Market analysis requirements
- Competitive landscape investigation
- Financial considerations
- Strategic planning needs
- Risk assessment requirements
- Implementation considerations

Format your response as follows:

TASK BREAKDOWN:
- [List specific tasks]

RESEARCH FOCUS AREAS:
- [List research areas]

ANALYSIS DEPTH: [basic/standard/comprehensive]

PRIORITY AREAS:
- [List priority areas]

ESTIMATED TIMELINE: [Timeline estimate]

Be specific and actionable in your recommendations. Focus on what will provide the most value for this particular business request{company_context}.
"""
        
        return prompt
    
    def _parse_planning_response(self, response: str, user_prompt: str) -> PlannerOutput:
        """
        Parse the LLM response into structured PlannerOutput
        
        Args:
            response: Raw LLM response
            user_prompt: Original user prompt for fallback
            
        Returns:
            Structured PlannerOutput
        """
        try:
            # Initialize with defaults
            task_breakdown = []
            research_focus_areas = []
            analysis_depth = "standard"
            priority_areas = []
            estimated_timeline = "2-3 hours"
            
            # Parse the response
            lines = response.strip().split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check for section headers
                if line.upper().startswith('TASK BREAKDOWN:'):
                    current_section = 'tasks'
                    continue
                elif line.upper().startswith('RESEARCH FOCUS AREAS:'):
                    current_section = 'research'
                    continue
                elif line.upper().startswith('ANALYSIS DEPTH:'):
                    depth_value = line.split(':', 1)[1].strip().lower()
                    if depth_value in ['basic', 'standard', 'comprehensive']:
                        analysis_depth = depth_value
                    current_section = None
                    continue
                elif line.upper().startswith('PRIORITY AREAS:'):
                    current_section = 'priority'
                    continue
                elif line.upper().startswith('ESTIMATED TIMELINE:'):
                    estimated_timeline = line.split(':', 1)[1].strip()
                    current_section = None
                    continue
                
                # Parse list items
                if line.startswith('-') or line.startswith('•'):
                    item = line[1:].strip()
                    if current_section == 'tasks':
                        task_breakdown.append(item)
                    elif current_section == 'research':
                        research_focus_areas.append(item)
                    elif current_section == 'priority':
                        priority_areas.append(item)
            
            # Fallback values if parsing failed
            if not task_breakdown:
                task_breakdown = [
                    "Conduct market research and analysis",
                    "Analyze competitive landscape",
                    "Perform SWOT analysis",
                    "Develop strategic recommendations",
                    "Create financial analysis and projections",
                    "Compile comprehensive report"
                ]
            
            if not research_focus_areas:
                research_focus_areas = [
                    "Market size and growth trends",
                    "Competitive analysis",
                    "Industry trends and dynamics",
                    "Customer needs and preferences",
                    "Regulatory environment"
                ]
            
            if not priority_areas:
                priority_areas = [
                    "Market opportunity assessment",
                    "Competitive positioning",
                    "Financial viability"
                ]
            
            return PlannerOutput(
                task_breakdown=task_breakdown,
                research_focus_areas=research_focus_areas,
                analysis_depth=analysis_depth,
                priority_areas=priority_areas,
                estimated_timeline=estimated_timeline
            )
            
        except Exception as e:
            # Fallback to default planning structure
            return PlannerOutput(
                task_breakdown=[
                    "Conduct comprehensive market research",
                    "Analyze competitive landscape and positioning",
                    "Perform detailed SWOT analysis",
                    "Develop strategic recommendations and go-to-market strategy",
                    "Create financial analysis and projections",
                    "Compile and generate comprehensive business report"
                ],
                research_focus_areas=[
                    "Market size, growth, and trends",
                    "Competitive analysis and benchmarking",
                    "Customer segments and needs",
                    "Industry dynamics and regulations",
                    "Technology trends and innovations"
                ],
                analysis_depth="standard",
                priority_areas=[
                    "Market opportunity assessment",
                    "Competitive advantage identification",
                    "Financial viability and projections"
                ],
                estimated_timeline="2-3 hours for comprehensive analysis"
            )