# Excel-to-Insights Bot - Setup Guide

## Quick Start (5 Minutes)

### Step 1: Install Python Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 2: (Optional) Configure AI API Keys

If you want to use AI-powered insights:

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your API keys:
   - Get OpenAI API key from: https://platform.openai.com/api-keys
   - Get Gemini API key from: https://makersuite.google.com/app/apikey

**Note**: The app works without API keys using rule-based insights!

### Step 3: Generate Sample Data (Optional)

To test with sample data:

```bash
python generate_sample_data.py
```

This creates `sample_data/sales_data_2023.xlsx` with 1000 sample records.

### Step 4: Run the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## Detailed Setup Instructions

### For Windows Users

1. **Install Python 3.9+**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Open Command Prompt or PowerShell**
   ```powershell
   cd E:\excel-insight-generator
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

### For macOS/Linux Users

1. **Install Python 3.9+**
   ```bash
   # macOS (using Homebrew)
   brew install python@3.9
   
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install python3.9 python3-pip
   ```

2. **Setup and Run**
   ```bash
   cd /path/to/excel-insight-generator
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Troubleshooting

### Issue: "streamlit: command not found"

**Solution**: Make sure virtual environment is activated and Streamlit is installed:
```bash
pip install streamlit
```

### Issue: "ModuleNotFoundError: No module named 'pandas'"

**Solution**: Install all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "API key not found" warning

**Solution**: Either:
1. Add API keys to `.env` file (for AI insights)
2. Ignore the warning (app uses rule-based insights instead)

### Issue: Port 8501 already in use

**Solution**: Use a different port:
```bash
streamlit run app.py --server.port 8502
```

## Testing the Application

1. **Upload Sample Data**
   - Use the generated `sample_data/sales_data_2023.xlsx`
   - Or upload your own Excel/CSV file

2. **Expected Results**
   - Data preview shows first 10 rows
   - Analysis completes in 30-60 seconds
   - Charts are generated automatically
   - Insights appear in the AI Insights tab

3. **Download Reports**
   - PDF report with all insights
   - Cleaned data as CSV

## Configuration Options

### Streamlit Configuration

Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"

[server]
maxUploadSize = 200
port = 8501
```

### Application Settings

Edit these variables in `app.py`:

```python
MAX_FILE_SIZE_MB = 200  # Maximum upload size
DEFAULT_ANALYSIS_DEPTH = "Standard"  # Quick, Standard, or Deep
DEFAULT_VISUALIZATION_STYLE = "Professional"  # Professional, Colorful, or Minimal
```

## Deployment

### Deploy to Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your GitHub repository
4. Add secrets (API keys) in Streamlit Cloud dashboard
5. Deploy!

### Deploy to Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Deploy with Docker

```bash
# Build image
docker build -t excel-insights .

# Run container
docker run -p 8501:8501 excel-insights
```

## Next Steps

1. ✅ Test with sample data
2. ✅ Upload your own Excel files
3. ✅ Explore different visualization styles
4. ✅ Configure AI API keys for enhanced insights
5. ✅ Customize the app for your specific use case

## Support

- **Documentation**: See README.md
- **Issues**: Open an issue on GitHub
- **Questions**: Contact support@example.com

---

**Happy Analyzing! 📊**
