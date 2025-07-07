import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain_ollama import ChatOllama
from models.schemas import BusinessAnalysisState, AgentResponse
from utils.logger import logger
from utils.config import Config


class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.model_config = Config.get_model_config()
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the LLM with retry logic"""
        max_retries = Config.MAX_RETRIES
        
        for attempt in range(max_retries):
            try:
                self.llm = ChatOllama(
                    model=self.model_config["model"],
                    base_url=self.model_config["base_url"],
                    temperature=self.model_config["temperature"],
                    num_predict=self.model_config["num_predict"],
                )
                logger.debug(f"LLM initialized for {self.agent_name}")
                return
            except Exception as e:
                logger.warning(f"LLM initialization attempt {attempt + 1} failed for {self.agent_name}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to initialize LLM for {self.agent_name} after {max_retries} attempts")
                    raise
    
    def invoke_llm(self, prompt: str) -> str:
        """
        Invoke the LLM with error handling and retries
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            Response from the LLM
        """
        if not self.llm:
            raise RuntimeError(f"LLM not initialized for {self.agent_name}")
        
        max_retries = Config.MAX_RETRIES
        
        for attempt in range(max_retries):
            try:
                response = self.llm.invoke(prompt)
                if hasattr(response, 'content'):
                    return response.content
                else:
                    return str(response)
            except Exception as e:
                logger.warning(f"LLM invocation attempt {attempt + 1} failed for {self.agent_name}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"LLM invocation failed for {self.agent_name} after {max_retries} attempts")
                    raise
    
    def execute(self, state: BusinessAnalysisState) -> AgentResponse:
        """
        Execute the agent with comprehensive error handling
        
        Args:
            state: Current state of the business analysis
            
        Returns:
            AgentResponse with success status and data/error
        """
        start_time = time.time()
        
        try:
            logger.log_agent_start(self.agent_name, state.user_prompt[:100])
            
            # Call the specific agent implementation
            result = self.process(state)
            
            processing_time = time.time() - start_time
            logger.log_agent_complete(self.agent_name, processing_time)
            
            return AgentResponse(
                success=True,
                data=result,
                processing_time=processing_time
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = f"Error in {self.agent_name}: {str(e)}"
            logger.log_agent_error(self.agent_name, error_msg)
            
            return AgentResponse(
                success=False,
                error=error_msg,
                processing_time=processing_time
            )
    
    @abstractmethod
    def process(self, state: BusinessAnalysisState) -> Any:
        """
        Process the state and return results
        
        Args:
            state: Current state of the business analysis
            
        Returns:
            Processed results specific to the agent
        """
        pass
    
    def create_prompt(self, template: str, **kwargs) -> str:
        """
        Create a prompt from template with variable substitution
        
        Args:
            template: Prompt template string
            **kwargs: Variables to substitute in the template
            
        Returns:
            Formatted prompt string
        """
        try:
            return template.format(**kwargs)
        except KeyError as e:
            logger.error(f"Missing template variable in {self.agent_name}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error formatting prompt in {self.agent_name}: {str(e)}")
            raise