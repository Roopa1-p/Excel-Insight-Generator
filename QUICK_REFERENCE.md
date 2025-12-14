# Excel-to-Insights Bot - Quick Reference

## 🚀 Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Generate sample data
python generate_sample_data.py

# Run application
streamlit run app.py
```

## 📂 File Overview

| File | Purpose | Lines |
|------|---------|-------|
| `app.py` | Main Streamlit application | 500+ |
| `modules/data_processor.py` | Data cleaning pipeline | 250+ |
| `modules/eda_engine.py` | Statistical analysis | 350+ |
| `modules/visualization_engine.py` | Chart generation | 250+ |
| `modules/ai_insights.py` | AI insights generator | 300+ |
| `modules/report_generator.py` | PDF/Excel reports | 200+ |

## 🎯 Key Features Checklist

- ✅ File upload (Excel/CSV)
- ✅ Automated data cleaning
- ✅ Missing value handling
- ✅ Outlier detection
- ✅ Descriptive statistics
- ✅ Correlation analysis
- ✅ KPI calculation
- ✅ Time series analysis
- ✅ 8+ chart types
- ✅ AI-powered insights (GPT-4/Gemini)
- ✅ Rule-based fallback insights
- ✅ PDF report generation
- ✅ Excel export
- ✅ Interactive dashboard

## 🔧 Configuration

### API Keys (.env file)
```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
```

### Streamlit Settings
- Port: 8501 (default)
- Max upload: 200 MB
- Theme: Professional blue

## 📊 Supported Data Types

- **Numeric**: Sales, revenue, quantities, prices
- **Categorical**: Products, regions, categories
- **Datetime**: Dates, timestamps
- **Text**: Names, descriptions

## 🎨 Visualization Types

1. Histograms (distributions)
2. Bar charts (comparisons)
3. Pie charts (proportions)
4. Line charts (trends)
5. Scatter plots (correlations)
6. Heatmaps (correlation matrix)
7. Box plots (outliers)

## 🤖 AI Models Supported

- OpenAI GPT-4 (best quality)
- OpenAI GPT-3.5 Turbo (faster)
- Google Gemini Pro (alternative)
- Rule-based (no API key needed)

## 📈 Auto-Detected KPIs

- Total Revenue
- Average Order Value
- Unique Customers
- Total Units Sold
- Profit Margins
- Growth Rates

## 🐛 Common Issues

**Issue**: Module not found  
**Fix**: `pip install -r requirements.txt`

**Issue**: Port in use  
**Fix**: `streamlit run app.py --server.port 8502`

**Issue**: API key warning  
**Fix**: Add keys to `.env` or ignore (uses fallback)

## 📥 Output Files

- `reports/insights_report_YYYYMMDD_HHMMSS.pdf`
- `reports/data_analysis_YYYYMMDD_HHMMSS.xlsx`
- Cleaned CSV (download from UI)

## 🎓 Academic Use

**Suitable For**:
- Final year projects
- Internship portfolios
- Hackathon submissions
- Graduate applications

**Skills Demonstrated**:
- Data science
- Web development
- AI integration
- Software engineering

## 📚 Documentation

- `README.md` - Full documentation
- `SETUP_GUIDE.md` - Installation guide
- `PROJECT_DOCUMENTATION.md` - Detailed explanation
- `walkthrough.md` - Implementation walkthrough

## 🌐 Deployment Options

- Streamlit Cloud (free)
- Heroku
- AWS/Azure/GCP
- Docker container

## ⚡ Performance

- Handles 100,000+ rows
- Analysis time: 30-60 seconds
- Memory efficient
- Responsive UI

## 🔐 Security

- No data retention
- Encrypted file transfer (HTTPS)
- API keys in .env (not committed)
- Session-based processing

---

**Need Help?**  
See `SETUP_GUIDE.md` for detailed instructions!
