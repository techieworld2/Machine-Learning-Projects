import time
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langgraph.graph.graph import CompiledGraph

from models.schemas import BusinessAnalysisState
from agents import (
    PlannerAgent,
    ResearchAgent,
    SWOTAgent,
    StrategyAgent,
    FinanceAgent,
    WriterAgent
)
from utils.logger import logger
from utils.config import Config


def planner_node(state: BusinessAnalysisState) -> Dict[str, Any]:
    """Planner agent node - decomposes tasks and plans analysis"""
    agent = PlannerAgent()
    
    try:
        response = agent.execute(state)
        if response.success:
            state.planner_output = response.data
            state.current_step = "planning_complete"
            state.completed_steps.append("planner")
        else:
            state.errors.append(f"Planner failed: {response.error}")
            
    except Exception as e:
        error_msg = f"Planner node error: {str(e)}"
        logger.error(error_msg)
        state.errors.append(error_msg)
    
    return {"state": state}


def research_node(state: BusinessAnalysisState) -> Dict[str, Any]:
    """Research agent node - conducts web research and data gathering"""
    agent = ResearchAgent()
    
    try:
        response = agent.execute(state)
        if response.success:
            state.research_data = response.data
            state.current_step = "research_complete"
            state.completed_steps.append("research")
        else:
            state.errors.append(f"Research failed: {response.error}")
            
    except Exception as e:
        error_msg = f"Research node error: {str(e)}"
        logger.error(error_msg)
        state.errors.append(error_msg)
    
    return {"state": state}


def swot_node(state: BusinessAnalysisState) -> Dict[str, Any]:
    """SWOT agent node - generates SWOT analysis"""
    agent = SWOTAgent()
    
    try:
        response = agent.execute(state)
        if response.success:
            state.swot_analysis = response.data
            state.current_step = "swot_complete"
            state.completed_steps.append("swot")
        else:
            state.errors.append(f"SWOT analysis failed: {response.error}")
            
    except Exception as e:
        error_msg = f"SWOT node error: {str(e)}"
        logger.error(error_msg)
        state.errors.append(error_msg)
    
    return {"state": state}


def strategy_node(state: BusinessAnalysisState) -> Dict[str, Any]:
    """Strategy agent node - generates strategic recommendations"""
    agent = StrategyAgent()
    
    try:
        response = agent.execute(state)
        if response.success:
            state.strategy_recommendations = response.data
            state.current_step = "strategy_complete"
            state.completed_steps.append("strategy")
        else:
            state.errors.append(f"Strategy analysis failed: {response.error}")
            
    except Exception as e:
        error_msg = f"Strategy node error: {str(e)}"
        logger.error(error_msg)
        state.errors.append(error_msg)
    
    return {"state": state}


def finance_node(state: BusinessAnalysisState) -> Dict[str, Any]:
    """Finance agent node - generates financial analysis"""
    agent = FinanceAgent()
    
    try:
        response = agent.execute(state)
        if response.success:
            state.financial_analysis = response.data
            state.current_step = "finance_complete"
            state.completed_steps.append("finance")
        else:
            state.errors.append(f"Financial analysis failed: {response.error}")
            
    except Exception as e:
        error_msg = f"Finance node error: {str(e)}"
        logger.error(error_msg)
        state.errors.append(error_msg)
    
    return {"state": state}


def writer_node(state: BusinessAnalysisState) -> Dict[str, Any]:
    """Writer agent node - compiles final report and generates PDF"""
    agent = WriterAgent()
    
    try:
        response = agent.execute(state)
        if response.success:
            state.final_report = response.data
            state.current_step = "analysis_complete"
            state.completed_steps.append("writer")
        else:
            state.errors.append(f"Report generation failed: {response.error}")
            
    except Exception as e:
        error_msg = f"Writer node error: {str(e)}"
        logger.error(error_msg)
        state.errors.append(error_msg)
    
    return {"state": state}


def should_continue_to_research(state: BusinessAnalysisState) -> str:
    """Conditional edge to determine if research should proceed"""
    if "planner" in state.completed_steps and not state.errors:
        return "research"
    else:
        return "end"


def should_continue_to_analysis(state: BusinessAnalysisState) -> str:
    """Conditional edge to determine if analysis phases should proceed"""
    if "research" in state.completed_steps and not state.errors:
        return "swot"
    else:
        return "end"


def should_continue_to_strategy(state: BusinessAnalysisState) -> str:
    """Conditional edge from SWOT to strategy"""
    if "swot" in state.completed_steps:
        return "strategy"
    else:
        return "end"


def should_continue_to_finance(state: BusinessAnalysisState) -> str:
    """Conditional edge from strategy to finance"""
    if "strategy" in state.completed_steps:
        return "finance"
    else:
        return "end"


def should_continue_to_writer(state: BusinessAnalysisState) -> str:
    """Conditional edge from finance to writer"""
    if "finance" in state.completed_steps:
        return "writer"
    else:
        return "end"


def create_business_analysis_graph() -> CompiledGraph:
    """
    Create and configure the LangGraph workflow for business analysis
    
    Returns:
        Compiled LangGraph workflow
    """
    logger.info("Creating business analysis workflow graph")
    
    # Create the graph
    workflow = StateGraph(BusinessAnalysisState)
    
    # Add nodes for each agent
    workflow.add_node("planner", planner_node)
    workflow.add_node("research", research_node)
    workflow.add_node("swot", swot_node)
    workflow.add_node("strategy", strategy_node)
    workflow.add_node("finance", finance_node)
    workflow.add_node("writer", writer_node)
    
    # Set entry point
    workflow.set_entry_point("planner")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "planner",
        should_continue_to_research,
        {
            "research": "research",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "research",
        should_continue_to_analysis,
        {
            "swot": "swot",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "swot",
        should_continue_to_strategy,
        {
            "strategy": "strategy",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "strategy",
        should_continue_to_finance,
        {
            "finance": "finance",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "finance",
        should_continue_to_writer,
        {
            "writer": "writer",
            "end": END
        }
    )
    
    # Writer always goes to end
    workflow.add_edge("writer", END)
    
    # Compile the graph
    try:
        compiled_graph = workflow.compile()
        logger.info("Business analysis workflow graph compiled successfully")
        return compiled_graph
    except Exception as e:
        logger.error(f"Failed to compile workflow graph: {str(e)}")
        raise


def run_business_analysis(user_prompt: str, company_name: str = None) -> BusinessAnalysisState:
    """
    Run complete business analysis workflow
    
    Args:
        user_prompt: User's business analysis request
        company_name: Optional company name
        
    Returns:
        Completed BusinessAnalysisState with all analysis results
    """
    start_time = time.time()
    
    # Initialize configuration
    Config.ensure_directories()
    
    # Create initial state
    initial_state = BusinessAnalysisState(
        user_prompt=user_prompt,
        company_name=company_name,
        current_step="initialized"
    )
    
    logger.log_workflow_start(user_prompt)
    
    try:
        # Create and run the workflow
        graph = create_business_analysis_graph()
        
        # Execute the workflow
        result = graph.invoke(initial_state)
        
        # Extract final state
        if isinstance(result, dict) and "state" in result:
            final_state = result["state"]
        else:
            final_state = result
        
        # Calculate processing time
        processing_time = time.time() - start_time
        final_state.processing_time = processing_time
        
        # Log completion
        logger.log_workflow_complete(
            processing_time, 
            final_state.pdf_report_path or ""
        )
        
        return final_state
        
    except Exception as e:
        processing_time = time.time() - start_time
        error_msg = f"Workflow execution failed: {str(e)}"
        logger.error(error_msg)
        
        initial_state.errors.append(error_msg)
        initial_state.processing_time = processing_time
        initial_state.current_step = "failed"
        
        return initial_state


if __name__ == "__main__":
    # Test the workflow
    test_prompt = "Analyze the market opportunity for AI-powered customer service chatbots"
    test_company = "ChatBot Solutions Inc."
    
    result = run_business_analysis(test_prompt, test_company)
    
    print("Workflow completed!")
    print(f"Status: {result.current_step}")
    print(f"Completed steps: {result.completed_steps}")
    print(f"Processing time: {result.processing_time:.2f} seconds")
    print(f"Errors: {result.errors}")
    print(f"PDF report: {result.pdf_report_path}")
    
    if result.final_report:
        print("\nFinal Report Preview:")
        print(result.final_report[:500] + "...")