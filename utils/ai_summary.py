import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get Gemini API key from .env
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API only if key exists
if api_key:
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"⚠️ Error configuring Gemini API: {e}")
        api_key = None
else:
    print("⚠️ GEMINI_API_KEY not found. AI summaries will be disabled.")
    api_key = None


def safe_dumps(obj, **kwargs):
    """Safe JSON dump that converts non-serializable objects to strings."""
    return json.dumps(obj, default=str, **kwargs)


def generate_ai_summary(eda_results, kpis):
    """
    Generate an AI-powered summary using Google Gemini API.
    Falls back to a safe message if no valid API key is configured.
    """
    if not api_key:
        return "⚠️ AI Summary disabled (no valid API key configured)."

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Build the prompt
        prompt = f"""
        Analyze the following dataset and KPIs to provide an executive summary.

        Dataset Shape: {eda_results.get('shape', 'N/A')}

        Key Statistics:
        {safe_dumps(eda_results.get('describe', {}), indent=2)}

        Key Performance Indicators (KPIs):
        {safe_dumps(kpis, indent=2)}

        Please summarize:
        1. Key trends and patterns
        2. Significant correlations
        3. Potential concerns or opportunities
        4. Actionable recommendations
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"⚠️ Error generating AI summary: {e}"


def calculate_kpis(df):
    """
    Calculate basic KPIs from the dataset.
    """
    kpis = {}
    try:
        if "Quantity" in df.columns:
            kpis["Total quantity"] = float(df["Quantity"].sum())
            kpis["Average quantity"] = float(df["Quantity"].mean())

        if "UnitPrice" in df.columns:
            kpis["Total unitprice"] = float(df["UnitPrice"].sum())
            kpis["Average unitprice"] = float(df["UnitPrice"].mean())

        if "CustomerID" in df.columns:
            kpis["Total customerid"] = float(df["CustomerID"].sum())
            kpis["Average customerid"] = float(df["CustomerID"].mean())

        # Date range check
        for col in df.columns:
            if "date" in col.lower() or "time" in col.lower():
                try:
                    kpis[f"Date range for {col}"] = f"{str(df[col].min())} to {str(df[col].max())}"
                except Exception:
                    pass

    except Exception as e:
        kpis["error"] = f"Error calculating KPIs: {e}"

    return kpis
