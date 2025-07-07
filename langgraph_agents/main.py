#!/usr/bin/env python3
"""
LangGraph Multi-Agent Business Analysis System
Main entry point for the business analysis workflow
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))

from graph import run_business_analysis
from utils.logger import get_logger
from utils.config import Config


def main():
    """Main function to run business analysis from command line"""
    parser = argparse.ArgumentParser(
        description="LangGraph Multi-Agent Business Analysis System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "Analyze the market opportunity for AI-powered customer service chatbots"
  python main.py "Market analysis for electric vehicle charging stations" --company "EV Charge Co"
  python main.py "Business opportunity assessment for drone delivery services" --company "SkyDeliver" --log-level DEBUG
        """
    )
    
    parser.add_argument(
        "prompt",
        help="Business analysis request or prompt"
    )
    
    parser.add_argument(
        "--company",
        "-c",
        help="Company name (optional)"
    )
    
    parser.add_argument(
        "--log-level",
        "-l",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--output-dir",
        "-o",
        help="Output directory for reports (default: ./reports)"
    )
    
    parser.add_argument(
        "--no-pdf",
        action="store_true",
        help="Skip PDF generation"
    )
    
    parser.add_argument(
        "--validate-config",
        action="store_true",
        help="Validate configuration and exit"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    logger = get_logger(
        name="business_analysis_main",
        log_file=Config.LOG_FILE,
        log_level=args.log_level
    )
    
    # Validate configuration if requested
    if args.validate_config:
        validate_configuration()
        return
    
    # Override output directory if specified
    if args.output_dir:
        Config.PDF_OUTPUT_DIR = args.output_dir
    
    # Ensure directories exist
    try:
        Config.ensure_directories()
    except Exception as e:
        logger.error(f"Failed to create required directories: {str(e)}")
        sys.exit(1)
    
    # Print startup information
    print_startup_info(args)
    
    try:
        # Run the business analysis
        logger.info("Starting business analysis workflow")
        
        result = run_business_analysis(
            user_prompt=args.prompt,
            company_name=args.company
        )
        
        # Print results
        print_results(result, args.no_pdf)
        
        # Exit with appropriate code
        if result.errors:
            logger.warning("Analysis completed with errors")
            sys.exit(1)
        else:
            logger.info("Analysis completed successfully")
            sys.exit(0)
            
    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        print("\nAnalysis interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"\nFatal error: {str(e)}")
        sys.exit(1)


def validate_configuration():
    """Validate system configuration"""
    print("Validating configuration...")
    
    status = Config.validate_config()
    
    print(f"Environment loaded: {'✓' if status['environment_loaded'] else '✗'}")
    print(f"Directories created: {'✓' if status['directories_created'] else '✗'}")
    
    print(f"\nConfiguration:")
    print(f"  Ollama URL: {Config.OLLAMA_BASE_URL}")
    print(f"  Ollama Model: {Config.OLLAMA_MODEL}")
    print(f"  PDF Output Dir: {Config.PDF_OUTPUT_DIR}")
    print(f"  Log File: {Config.LOG_FILE}")
    print(f"  Log Level: {Config.LOG_LEVEL}")
    
    # Check if all critical components are available
    all_good = all(status.values())
    
    if all_good:
        print("\n✓ Configuration validation passed")
    else:
        print("\n✗ Configuration validation failed")
        print("\nPlease check:")
        print("1. Create a .env file based on .env.example")
        print("2. Ensure Ollama is installed and running")
        print("3. Check file permissions for log and output directories")


def print_startup_info(args):
    """Print startup information"""
    print("=" * 80)
    print("LangGraph Multi-Agent Business Analysis System")
    print("=" * 80)
    print(f"Business Request: {args.prompt}")
    if args.company:
        print(f"Company: {args.company}")
    print(f"Log Level: {args.log_level}")
    print(f"Output Directory: {Config.PDF_OUTPUT_DIR}")
    print("=" * 80)


def print_results(result, no_pdf: bool):
    """Print analysis results"""
    print("\n" + "=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)
    
    print(f"Status: {result.current_step}")
    print(f"Processing Time: {result.processing_time:.2f} seconds")
    print(f"Completed Steps: {', '.join(result.completed_steps)}")
    
    if result.errors:
        print(f"\nErrors ({len(result.errors)}):")
        for i, error in enumerate(result.errors, 1):
            print(f"  {i}. {error}")
    
    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for i, warning in enumerate(result.warnings, 1):
            print(f"  {i}. {warning}")
    
    if not no_pdf and result.pdf_report_path:
        print(f"\nPDF Report: {result.pdf_report_path}")
    
    if result.final_report:
        print("\n" + "-" * 80)
        print("EXECUTIVE SUMMARY")
        print("-" * 80)
        
        # Print first 1000 characters of the report
        summary = result.final_report[:1000]
        if len(result.final_report) > 1000:
            summary += "\n\n... (See full report in PDF)"
        
        print(summary)
    
    print("\n" + "=" * 80)


def interactive_mode():
    """Run in interactive mode for multiple analyses"""
    print("LangGraph Business Analysis - Interactive Mode")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            prompt = input("Enter business analysis request: ").strip()
            if prompt.lower() in ['quit', 'exit', 'q']:
                break
            
            if not prompt:
                continue
            
            company = input("Company name (optional): ").strip() or None
            
            print("\nRunning analysis...")
            result = run_business_analysis(prompt, company)
            
            print(f"\nCompleted in {result.processing_time:.2f} seconds")
            if result.pdf_report_path:
                print(f"Report saved to: {result.pdf_report_path}")
            
            if result.errors:
                print(f"Errors: {len(result.errors)}")
            
            print("\n" + "-" * 50 + "\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}\n")
    
    print("Goodbye!")


if __name__ == "__main__":
    # Check if running in interactive mode
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        main()