# Machine Learning Projects

This repository contains various machine learning projects and implementations, ranging from traditional ML algorithms to advanced AI agent systems.

## 🤖 LangGraph Multi-Agent Business Analysis System

**NEW**: Complete production-ready multi-agent system for comprehensive business analysis using LangGraph and open-source LLMs.

### Features:
- 🎯 **Multi-Agent Architecture**: Coordinated AI agents for planning, research, SWOT analysis, strategy, and finance
- 🔍 **Automated Research**: Web scraping with DuckDuckGo search integration
- 📊 **Professional Reports**: High-quality PDF generation with comprehensive business analysis
- 🌐 **Open Source**: Uses Ollama for local LLM hosting (Mistral 7B/LLaMA3)
- ⚡ **Production Ready**: Error handling, logging, and configurable deployment

📁 **Location**: `langgraph_agents/`  
📖 **Documentation**: [LangGraph Agents README](langgraph_agents/README.md)

### Quick Start:
```bash
cd langgraph_agents
pip install -r requirements.txt
python main.py "Analyze the market opportunity for AI-powered customer service chatbots"
```

---

## 📊 Traditional Machine Learning Projects

### 1. **Credit Risk Modelling**
- **Files**: Case_Study1.xlsx, Case_Study2.xlsx, Credit Risk Modelling.ipynb
- **Description**: Comprehensive credit risk assessment using machine learning models
- **Techniques**: Data preprocessing, feature engineering, model evaluation

### 2. **Laptop Sales Analysis and Prediction Modelling**
- **Files**: Laptop_data.csv, Laptop_Sales_Analysis.ipynb, New_Dashboard.pdf
- **Description**: Sales prediction and market analysis for laptop products
- **Techniques**: EDA, predictive modeling, dashboard creation

### 3. **Linear and Logistic Regression From Scratch**
- **Files**: 
  - Linear_Reg_from_scratch_Implementation.ipynb
  - Logistic_Reg_from_scratch_implementation.ipynb
  - salary_data.csv, diabetes.csv
- **Description**: Implementation of regression algorithms from fundamental principles
- **Techniques**: Gradient descent, cost functions, mathematical implementation

### 4. **Sentiment Analysis With LSTM**
- **Files**: Sentiment Analysis With LSTM.ipynb
- **Description**: Deep learning approach for sentiment classification
- **Features**:
  - Training LSTM on IMDB movie reviews dataset
  - Visualization of accuracy and loss metrics
  - Model export for deployment on unseen datasets

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Notebook (for traditional ML projects)
- Ollama (for LangGraph agents)

### Installation
```bash
# Clone repository
git clone https://github.com/techieworld2/Machine-Learning-Projects.git
cd Machine-Learning-Projects

# For traditional ML projects
pip install pandas numpy scikit-learn matplotlib seaborn jupyter

# For LangGraph agents (see dedicated README)
cd langgraph_agents
pip install -r requirements.txt
```

## 🎯 Project Structure
```
Machine-Learning-Projects/
├── langgraph_agents/              # Multi-agent business analysis system
│   ├── agents/                    # AI agent implementations
│   ├── tools/                     # Search, scraping, PDF tools
│   ├── models/                    # Data models and schemas
│   ├── utils/                     # Configuration and logging
│   └── templates/                 # PDF report templates
├── Credit Risk Modelling.ipynb    # Credit risk analysis
├── Laptop_Sales_Analysis.ipynb    # Sales prediction model
├── Linear_Reg_from_scratch_Implementation.ipynb
├── Logistic_Reg_from_scratch_implementation.ipynb
├── Sentiment Analysis With LSTM.ipynb
└── datasets/                      # Various CSV and Excel files
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).