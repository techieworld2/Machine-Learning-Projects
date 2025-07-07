# LangGraph Multi-Agent Business Analysis System

A comprehensive, production-ready multi-agent system built with LangGraph that processes user prompts through specialized AI agents to generate detailed business analysis reports in PDF format.

## 🚀 Features

- **Multi-Agent Architecture**: Coordinated agents for planning, research, analysis, strategy, finance, and reporting
- **Open-Source LLMs**: Integration with Ollama for local LLM hosting (Mistral 7B/LLaMA3)
- **Web Research**: Automated web scraping with DuckDuckGo search and BeautifulSoup
- **Professional Reports**: High-quality PDF generation with CSS styling
- **SWOT Analysis**: Structured strengths, weaknesses, opportunities, and threats analysis
- **Strategic Planning**: Go-to-market strategies and business model recommendations
- **Financial Analysis**: Pricing strategies and financial projections
- **Error Resilience**: Robust error handling and fallback mechanisms
- **Configurable**: Environment-based configuration for easy deployment

## 🏗️ Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Planner   │───▶│   Research   │───▶│    SWOT     │
│    Agent    │    │    Agent     │    │   Agent     │
└─────────────┘    └──────────────┘    └─────────────┘
                                              │
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Writer    │◀───│   Finance    │◀───│  Strategy   │
│    Agent    │    │    Agent     │    │   Agent     │
└─────────────┘    └──────────────┘    └─────────────┘
```

## 📋 Prerequisites

### System Requirements
- Python 3.8+
- 4GB+ RAM recommended
- Internet connection for web research

### Required Software
1. **Ollama** - For local LLM hosting
   ```bash
   # Install Ollama (macOS/Linux)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama service
   ollama serve
   
   # Pull required models
   ollama pull mistral:7b
   # or
   ollama pull llama3:8b
   ```

2. **WeasyPrint Dependencies** (for PDF generation)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
   
   # macOS
   brew install pango
   
   # Windows - Use WSL or install GTK+ manually
   ```

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/techieworld2/Machine-Learning-Projects.git
cd Machine-Learning-Projects/langgraph_agents
```

### 2. Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### 3. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

### Example .env Configuration
```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b

# Search Configuration
SEARCH_MAX_RESULTS=10
SEARCH_REGION=wt-wt
SEARCH_SAFESEARCH=moderate

# PDF Configuration
PDF_OUTPUT_DIR=./reports
PDF_TEMPLATE_DIR=./templates

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/business_analysis.log
```

## 🚀 Quick Start

### Command Line Usage
```bash
# Basic analysis
python main.py "Analyze the market opportunity for AI-powered customer service chatbots"

# With company name
python main.py "Market analysis for electric vehicle charging stations" --company "EV Charge Co"

# Custom output directory
python main.py "Business opportunity for drone delivery" --output-dir "./my_reports"

# Debug mode
python main.py "SaaS platform analysis" --log-level DEBUG
```

### Interactive Mode
```bash
# Run without arguments for interactive mode
python main.py
```

### Programmatic Usage
```python
from graph import run_business_analysis

# Run analysis
result = run_business_analysis(
    user_prompt="Analyze the market opportunity for AI-powered customer service chatbots",
    company_name="ChatBot Solutions Inc."
)

# Access results
print(f"Status: {result.current_step}")
print(f"PDF Report: {result.pdf_report_path}")
print(f"Processing Time: {result.processing_time:.2f} seconds")

# Access detailed analysis
if result.swot_analysis:
    print(f"Strengths: {result.swot_analysis.strengths}")
    print(f"Opportunities: {result.swot_analysis.opportunities}")

if result.strategy_recommendations:
    print(f"Go-to-Market: {result.strategy_recommendations.go_to_market_strategy}")
```

## 📊 System Components

### Agents

#### 1. Planner Agent (`agents/planner.py`)
- **Purpose**: Task decomposition and workflow coordination
- **Input**: User prompt and company name
- **Output**: Structured analysis plan with task breakdown and priorities

#### 2. Research Agent (`agents/research.py`)
- **Purpose**: Web research and data gathering
- **Tools**: DuckDuckGo search, BeautifulSoup scraping
- **Output**: Market insights, competitor analysis, industry trends

#### 3. SWOT Agent (`agents/swot.py`)
- **Purpose**: Structured SWOT analysis generation
- **Input**: Research data and planning context
- **Output**: Categorized strengths, weaknesses, opportunities, threats

#### 4. Strategy Agent (`agents/strategy.py`)
- **Purpose**: Strategic recommendations and go-to-market planning
- **Input**: Research and SWOT analysis
- **Output**: Business model, target market, value proposition

#### 5. Finance Agent (`agents/finance.py`)
- **Purpose**: Financial analysis and projections
- **Input**: Strategy and market context
- **Output**: Pricing strategy, revenue model, financial projections

#### 6. Writer Agent (`agents/writer.py`)
- **Purpose**: Report compilation and PDF generation
- **Input**: All previous analysis results
- **Output**: Final report text and PDF document

### Tools

#### 1. Search Tool (`tools/search.py`)
- DuckDuckGo integration for web search
- Rate limiting and error handling
- Query generation and optimization

#### 2. Web Scraper (`tools/scraper.py`)
- BeautifulSoup-based content extraction
- Multiple retry mechanisms
- Content filtering and cleaning

#### 3. PDF Generator (`tools/pdf_generator.py`)
- WeasyPrint-based PDF generation
- Professional styling with CSS
- Template-based layout system

### Models

#### State Management (`models/schemas.py`)
- **BusinessAnalysisState**: Main workflow state
- **PlannerOutput**: Planning results
- **ResearchData**: Research findings
- **SWOTAnalysis**: SWOT analysis results
- **StrategyRecommendations**: Strategic plans
- **FinancialAnalysis**: Financial projections

## 🎯 Usage Examples

### 1. Market Opportunity Analysis
```bash
python main.py "Analyze the market opportunity for sustainable packaging solutions in e-commerce"
```

### 2. Competitive Analysis
```bash
python main.py "Competitive analysis for meal kit delivery services" --company "Fresh Meals Co"
```

### 3. Business Model Evaluation
```bash
python main.py "Evaluate the business model for subscription-based fitness apps"
```

### 4. Investment Opportunity Assessment
```bash
python main.py "Investment opportunity analysis for renewable energy storage systems"
```

## 📈 Output Structure

### Generated PDF Report Includes:
1. **Executive Summary** - Key findings and recommendations
2. **Analysis Planning** - Task breakdown and methodology
3. **Market Research** - Industry insights and trends
4. **SWOT Analysis** - Visual grid with detailed analysis
5. **Strategic Recommendations** - Go-to-market strategy
6. **Financial Analysis** - Pricing and projections
7. **Implementation Roadmap** - Action steps and timeline

### Console Output:
- Real-time progress updates
- Processing time and status
- Error and warning messages
- Executive summary preview

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | LLM model name | `mistral:7b` |
| `SEARCH_MAX_RESULTS` | Max search results per query | `10` |
| `PDF_OUTPUT_DIR` | PDF output directory | `./reports` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `MAX_RETRIES` | Max retry attempts | `3` |
| `REQUEST_TIMEOUT` | Request timeout (seconds) | `30` |

### Model Options
- `mistral:7b` - Fast, efficient (recommended)
- `llama3:8b` - Balanced performance
- `llama3:70b` - High quality (requires more resources)

## 🐛 Troubleshooting

### Common Issues

#### 1. Ollama Connection Error
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve
```

#### 2. PDF Generation Fails
```bash
# Install WeasyPrint dependencies
sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0

# Or on macOS
brew install pango
```

#### 3. Search Rate Limiting
- Increase `RATE_LIMIT_DELAY` in configuration
- Reduce `SEARCH_MAX_RESULTS`

#### 4. Memory Issues
- Use smaller models (`mistral:7b` instead of `llama3:70b`)
- Reduce content processing limits in agents

### Validation
```bash
# Validate configuration
python main.py --validate-config

# Test with simple prompt
python main.py "Test analysis" --log-level DEBUG
```

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black .

# Linting
flake8 .

# Type checking
mypy .
```

### Adding New Agents
1. Create agent class inheriting from `BaseAgent`
2. Implement `process()` method
3. Add to workflow in `graph.py`
4. Update state models if needed

### Extending Tools
1. Add tool class in `tools/` directory
2. Implement core functionality
3. Add error handling and logging
4. Update agent to use new tool

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangGraph** - For the agent orchestration framework
- **Ollama** - For local LLM hosting
- **WeasyPrint** - For PDF generation
- **DuckDuckGo** - For web search capabilities
- **BeautifulSoup** - For web content extraction

## 📞 Support

- **Documentation**: [GitHub Repository](https://github.com/techieworld2/Machine-Learning-Projects)
- **Issues**: [GitHub Issues](https://github.com/techieworld2/Machine-Learning-Projects/issues)
- **Discussions**: [GitHub Discussions](https://github.com/techieworld2/Machine-Learning-Projects/discussions)

---

**Built with ❤️ using LangGraph and open-source AI technologies**