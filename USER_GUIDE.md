# 📖 User Guide - Excel-to-Insights Bot

## 🎯 Quick Start (3 Steps)

### Step 1: Setup
```bash
# 1. Navigate to project directory
cd excel-insight-generator

# 2. Run the startup script
run_app.bat
```

The script will:
- ✅ Create/activate virtual environment
- ✅ Install dependencies
- ✅ Check for .env file
- ✅ Launch the application

### Step 2: Configure (First Time Only)
1. Open `.env` file in a text editor
2. Add your API keys:
   ```
   OPENAI_API_KEY=sk-your-key-here
   GEMINI_API_KEY=your-gemini-key-here
   ```
3. Save the file

### Step 3: Analyze
1. Upload your Excel/CSV file
2. Click "Analyze Data"
3. Explore insights in tabs
4. Download reports

---

## 🖥️ Application Interface Guide

### Main Screen

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Excel-to-Insights Bot                                   │
│  Transform your Excel data into actionable insights         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [📁 Upload Excel File]                                     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Drag and drop or click to upload                    │  │
│  │  Supported: .xlsx, .xls, .csv (Max 200MB)            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Sidebar Settings

```
┌─────────────────────┐
│ ⚙️ Settings         │
├─────────────────────┤
│ AI Model:           │
│ [OpenAI GPT-4  ▼]  │
│                     │
│ Analysis Depth:     │
│ ●─────●─────○       │
│ Quick Standard Deep │
│                     │
│ Visualization:      │
│ [Professional  ▼]  │
└─────────────────────┘
```

### After Upload

```
┌─────────────────────────────────────────────────────────────┐
│ 📁 File Information                                         │
├─────────────────────────────────────────────────────────────┤
│  Filename: sales_data.xlsx                                  │
│  File Size: 125.5 KB                                        │
│  Upload Time: 2023-12-12 14:30:00                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 📋 Data Preview                                             │
├─────────────────────────────────────────────────────────────┤
│  Date       │ Product   │ Region  │ Sales_Amount │ ...      │
│  2023-01-01 │ Widget A  │ North   │ $1,234.56   │ ...      │
│  2023-01-02 │ Widget B  │ South   │ $2,345.67   │ ...      │
│  ...        │ ...       │ ...     │ ...         │ ...      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Total Rows: 1,000  │  Columns: 10  │  Missing: 50          │
└─────────────────────────────────────────────────────────────┘

                    [🔍 Analyze Data]
```

### Analysis Progress

```
┌─────────────────────────────────────────────────────────────┐
│ 🧹 Cleaning and preprocessing data...                       │
│ ████████████████████░░░░░░░░░░░░░░░░░░░░ 40%              │
└─────────────────────────────────────────────────────────────┘
```

### Results Tabs

```
┌─────────────────────────────────────────────────────────────┐
│ 📊 Analysis Results                                         │
├─────────────────────────────────────────────────────────────┤
│ [🧹 Data Quality] [📈 Statistics] [📊 Visualizations]       │
│ [🤖 AI Insights] [📥 Download Report]                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  (Tab content appears here)                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Understanding the Results

### Tab 1: Data Quality 🧹

Shows what was cleaned in your data:

- **Rows Processed**: Total number of records
- **Columns Cleaned**: How many columns were processed
- **Missing Values Handled**: Number of missing values filled
- **Transformations Applied**: List of cleaning operations

**Example Output:**
```
✓ Removed 5 duplicate rows
✓ Filled 50 missing values using median
✓ Detected and capped 12 outliers
✓ Converted 3 columns to appropriate data types
```

### Tab 2: Statistics 📈

Displays statistical analysis:

- **Descriptive Statistics**: Mean, median, std dev, min, max
- **Key Performance Indicators**: Important metrics
- **Distribution Information**: Data spread and patterns

**Example KPIs:**
```
Total Revenue: $1,234,567
Average Order: $1,234.56
Growth Rate: +15.3%
Top Product: Widget A
```

### Tab 3: Visualizations 📊

Interactive charts showing:

1. **Distribution Plots**: How data is spread
2. **Correlation Heatmap**: Relationships between variables
3. **Time Series**: Trends over time
4. **Category Analysis**: Breakdown by categories
5. **Top Performers**: Best products/regions/etc.

**Chart Types:**
- 📊 Bar charts for categories
- 📈 Line charts for trends
- 🔥 Heatmaps for correlations
- 📉 Histograms for distributions

### Tab 4: AI Insights 🤖

AI-generated analysis including:

**Executive Summary**
```
Your sales data shows strong performance in Q3 2023 with 
a 15% increase compared to Q2. Widget A is the top 
performer, accounting for 35% of total revenue...
```

**Key Findings**
- ✓ Sales peaked in September 2023
- ✓ North America is the strongest region (45% of revenue)
- ✓ Electronics category has highest profit margin (28%)
- ⚠️ South America shows declining trend (-5%)

**Recommendations**
- 💡 Increase inventory for Widget A in Q4
- 💡 Investigate South America performance decline
- 💡 Focus marketing on Electronics category
- 💡 Consider seasonal promotions in Q1

### Tab 5: Download Report 📥

Export your analysis:

**PDF Report**
- Complete analysis report
- All charts and visualizations
- Executive summary
- Recommendations

**Cleaned Data (CSV)**
- Processed dataset
- Missing values filled
- Outliers handled
- Ready for further analysis

---

## 🎨 Customization Options

### AI Model Selection

**OpenAI GPT-4** (Recommended)
- ✅ Most accurate insights
- ✅ Best recommendations
- ⚠️ Requires OpenAI API key
- 💰 Costs ~$0.03 per analysis

**Google Gemini**
- ✅ Fast processing
- ✅ Good quality insights
- ⚠️ Requires Gemini API key
- 💰 Free tier available

**OpenAI GPT-3.5**
- ✅ Faster than GPT-4
- ✅ Lower cost
- ⚠️ Less detailed insights
- 💰 Costs ~$0.002 per analysis

### Analysis Depth

**Quick** (~30 seconds)
- Basic statistics
- Essential charts
- Brief insights

**Standard** (~1-2 minutes) - Recommended
- Full statistics
- All visualizations
- Detailed insights

**Deep** (~2-5 minutes)
- Advanced statistics
- Additional correlations
- Comprehensive insights
- Pattern detection

### Visualization Style

**Professional**
- Clean, business-ready charts
- Neutral colors
- Print-friendly

**Colorful**
- Vibrant, engaging charts
- High contrast
- Presentation-ready

**Minimal**
- Simple, clean design
- Grayscale palette
- Distraction-free

---

## 💡 Tips for Best Results

### Data Preparation

✅ **DO:**
- Use clear column names (e.g., "Sales_Amount" not "Col1")
- Include date columns for time series analysis
- Keep data in tabular format (rows and columns)
- Use consistent data types in each column

❌ **DON'T:**
- Merge cells in Excel
- Use multiple header rows
- Include summary rows in the data
- Mix data types in columns

### File Size Optimization

For large files (>50MB):
- Remove unnecessary columns before upload
- Filter to relevant date ranges
- Remove duplicate records
- Consider splitting into multiple analyses

### Getting Better Insights

1. **Include Context**: Name columns descriptively
2. **Time Data**: Include date/time columns for trends
3. **Categories**: Include categorical columns (Region, Product, etc.)
4. **Metrics**: Include both quantity and value columns

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: "Module not found" error
```bash
Solution:
pip install -r requirements.txt
```

**Issue**: "API key not found" error
```bash
Solution:
1. Check .env file exists
2. Verify API keys are correct
3. No spaces around = sign
```

**Issue**: Analysis takes too long
```bash
Solution:
1. Reduce file size
2. Use "Quick" analysis depth
3. Close other applications
```

**Issue**: Charts not displaying
```bash
Solution:
1. Clear browser cache
2. Try different browser
3. Update Streamlit: pip install streamlit --upgrade
```

### Getting Help

1. Check `README.md` for setup instructions
2. Review `PROJECT_DOCUMENTATION.md` for technical details
3. Check `QUICK_REFERENCE.md` for command reference
4. Review error messages in the terminal

---

## 📚 Example Workflow

### Analyzing Sales Data

1. **Upload** `sales_data_2023.xlsx`
2. **Review** data preview (1,000 rows, 10 columns)
3. **Configure** settings:
   - AI Model: OpenAI GPT-4
   - Analysis Depth: Standard
   - Visualization: Professional
4. **Click** "Analyze Data"
5. **Wait** ~1-2 minutes for analysis
6. **Review** results:
   - Data Quality: 50 missing values handled
   - Statistics: $1.2M total revenue
   - Visualizations: 5 interactive charts
   - AI Insights: 8 key findings, 5 recommendations
7. **Download** PDF report and cleaned data

### Time Investment

- Setup (first time): 5 minutes
- Upload and configure: 1 minute
- Analysis: 1-2 minutes
- Review results: 5-10 minutes
- **Total**: ~15-20 minutes for complete analysis

---

## 🎓 Advanced Features

### Custom Analysis

Edit `modules/eda_engine.py` to add custom metrics:
```python
def calculate_custom_kpi(self):
    # Your custom calculation
    return result
```

### Custom Visualizations

Edit `modules/visualization_engine.py` to add charts:
```python
def create_custom_chart(self):
    # Your custom chart
    return fig
```

### Custom AI Prompts

Edit `modules/ai_insights.py` to customize AI analysis:
```python
prompt = "Analyze this data focusing on..."
```

---

## 📞 Support

For issues or questions:
1. Check this user guide
2. Review project documentation
3. Check error logs in terminal
4. Verify API keys and configuration

---

**Happy Analyzing! 📊✨**
