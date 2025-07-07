import logging
import os
import sys
from datetime import datetime
from typing import Optional
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output for different log levels"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA,
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


class BusinessAnalysisLogger:
    """Logger class for the Business Analysis System"""
    
    def __init__(self, name: str = "business_analysis", log_file: Optional[str] = None, log_level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatters
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (if log_file is provided)
        if log_file:
            # Ensure log directory exists
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message, **kwargs)
    
    def log_agent_start(self, agent_name: str, input_data: str = ""):
        """Log agent execution start"""
        self.info(f"🚀 Starting {agent_name} agent" + (f" with input: {input_data[:100]}..." if input_data else ""))
    
    def log_agent_complete(self, agent_name: str, processing_time: float = None):
        """Log agent execution completion"""
        time_str = f" (took {processing_time:.2f}s)" if processing_time else ""
        self.info(f"✅ Completed {agent_name} agent{time_str}")
    
    def log_agent_error(self, agent_name: str, error: str):
        """Log agent execution error"""
        self.error(f"❌ Error in {agent_name} agent: {error}")
    
    def log_tool_usage(self, tool_name: str, action: str, result: str = ""):
        """Log tool usage"""
        result_str = f" - {result[:100]}..." if result else ""
        self.debug(f"🔧 {tool_name}: {action}{result_str}")
    
    def log_workflow_start(self, prompt: str):
        """Log workflow start"""
        self.info(f"🎯 Starting business analysis workflow for: {prompt[:100]}...")
    
    def log_workflow_complete(self, total_time: float, pdf_path: str = ""):
        """Log workflow completion"""
        path_str = f" - PDF saved to: {pdf_path}" if pdf_path else ""
        self.info(f"🎉 Business analysis workflow completed in {total_time:.2f}s{path_str}")


# Global logger instance
logger = BusinessAnalysisLogger()


def get_logger(name: str = "business_analysis", log_file: Optional[str] = None, log_level: str = "INFO") -> BusinessAnalysisLogger:
    """Get a logger instance with specified configuration"""
    return BusinessAnalysisLogger(name=name, log_file=log_file, log_level=log_level)