# Excel-to-Insights Bot

An intelligent automation tool that transforms raw Excel spreadsheets into actionable business insights through automated data cleaning, statistical analysis, visualization generation, and AI-powered narrative summaries.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Problem Statement

Organizations generate massive amounts of data in Excel spreadsheets, but extracting meaningful insights requires significant time, technical expertise, and manual effort. The Excel-to-Insights Bot democratizes data analysis by automating the entire analytics pipeline—from data cleaning to AI-powered insights—making advanced analytics accessible to non-technical users.

## ✨ Features

- **📤 Easy Upload**: Drag-and-drop Excel/CSV files
- **🧹 Automated Cleaning**: Handle missing values, duplicates, and data type conversions
- **📊 Statistical Analysis**: Comprehensive EDA with descriptive statistics, correlations, and KPIs
- **📈 Smart Visualizations**: Auto-generated charts (histograms, bar charts, time series, heatmaps)
- **🤖 AI-Powered Insights**: Natural language summaries using GPT-4 or Gemini
- **📄 Professional Reports**: Export to PDF and Excel formats
- **⚡ Fast Processing**: Analyze datasets with 100,000+ rows in minutes

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.9+**: Primary programming language
- **Streamlit**: Interactive web application framework
- **Pandas & NumPy**: Data manipulation and numerical computing
- **Plotly**: Interactive data visualizations
- **Matplotlib & Seaborn**: Statistical visualizations

### AI Integration
- **OpenAI GPT-4/3.5**: Advanced insights generation
- **Google Gemini**: Alternative AI engine
- **LangChain**: Prompt engineering (optional)

### Report Generation
- **FPDF**: PDF report creation
- **openpyxl**: Excel file handling

## 📋 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/excel-insight-generator.git
cd excel-insight-generator
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API Keys** (Optional - for AI insights)

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

> **Note**: The application works without API keys using rule-based insights generation.

5. **Run the application**
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 🚀 Usage

### Quick Start

1. **Upload File**: Click "Browse files" or drag-and-drop your Excel/CSV file
2. **Preview Data**: Review the data preview and dataset statistics
3. **Configure Settings**: (Optional) Select AI model, analysis depth, and visualization style
4. **Analyze**: Click "🔍 Analyze Data" button
5. **Explore Results**: Navigate through tabs to view insights, charts, and statistics
6. **Download Report**: Export PDF report or cleaned data

### Supported File Formats
- `.xlsx` - Excel 2007+ format
- `.xls` - Excel 97-2003 format
- `.csv` - Comma-separated values

### Maximum File Size
- 200 MB (configurable)

## 📊 Workflow Architecture

```mermaid
graph LR
    A[Upload Excel] --> B[Data Ingestion]
    B --> C[Data Cleaning]
    C --> D[EDA Analysis]
    D --> E[Visualization]
    E --> F[AI Insights]
    F --> G[Report Generation]
    G --> H[Download PDF/Excel]
```

### Detailed Workflow

1. **Data Ingestion**: Validate and load Excel/CSV files
2. **Data Cleaning**: 
   - Remove duplicates
   - Handle missing values (mean/median/mode imputation)
   - Standardize column names
   - Infer and convert data types
   - Detect outliers
3. **Exploratory Data Analysis**:
   - Descriptive statistics (mean, median, std, etc.)
   - Correlation analysis
   - Distribution analysis
   - KPI calculation
   - Trend detection
4. **Visualization Generation**:
   - Histograms for distributions
   - Bar/pie charts for categorical data
   - Line charts for time series
   - Heatmaps for correlations
   - Box plots for outlier detection
5. **AI Insight Generation**:
   - Executive summary
   - Key findings
   - Pattern identification
   - Actionable recommendations
6. **Report Generation**:
   - Professional PDF reports
   - Excel exports with multiple sheets

## 📁 Project Structure

```
excel-insight-generator/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env                           # API keys (not in repo)
├── README.md                      # This file
│
├── modules/                       # Core modules
│   ├── __init__.py
│   ├── data_processor.py         # Data cleaning pipeline
│   ├── eda_engine.py             # Statistical analysis
│   ├── visualization_engine.py   # Chart generation
│   ├── ai_insights.py            # AI insights generator
│   └── report_generator.py       # PDF/Excel reports
│
├── reports/                       # Generated reports (auto-created)
├── sample_data/                   # Sample datasets for testing
└── docs/                          # Additional documentation
```

## 🔑 Key Performance Indicators (KPIs)

The system automatically detects and calculates relevant KPIs based on your data:

### Sales & Revenue
- Total Revenue
- Average Order Value (AOV)
- Revenue Growth Rate
- Top/Bottom Performers

### Customer Metrics
- Unique Customers
- Customer Retention Rate
- Churn Rate

### Operational Metrics
- Inventory Turnover
- Fulfillment Rate
- Average Processing Time

### Financial Metrics
- Profit Margin
- Return on Investment (ROI)

## 🤖 AI Insights Example

**Sample Executive Summary**:
> "The company experienced strong growth in 2023, with total revenue reaching $2.45M, representing an 18% increase from Q1 to Q4. Customer acquisition efforts were highly successful, growing the customer base by 28% while simultaneously improving retention (churn decreased from 12% to 8%). North America remains the dominant market, contributing 42% of total revenue."

**Sample Recommendations**:
1. Diversify product portfolio to reduce dependency on top-selling items
2. Investigate seasonal patterns for optimized inventory management
3. Expand international presence in high-growth markets
4. Implement targeted retention strategies for at-risk customer segments

## 🔮 Future Enhancements

### Phase 1: Advanced Analytics
- Predictive forecasting (ARIMA, Prophet)
- Customer segmentation (K-means clustering)
- Anomaly detection (Isolation Forest)
- Sentiment analysis for text columns

### Phase 2: Enhanced AI
- Conversational AI interface ("Ask questions about your data")
- Multi-language report generation
- Custom AI training for industry-specific insights

### Phase 3: Integration
- Google Sheets integration
- Database connectivity (PostgreSQL, MongoDB)
- Power BI / Tableau export
- REST API for programmatic access

### Phase 4: Collaboration
- User authentication
- Team workspaces
- Collaborative annotations
- Scheduled automated reports

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- OpenAI and Google for AI capabilities
- The open-source community for excellent libraries

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: support@example.com
- Documentation: [Link to docs]

## 📊 Demo

[Live Demo Link] | [Video Walkthrough]

---

**Made with ❤️ for data enthusiasts**
