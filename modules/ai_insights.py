"""
AI Insights Generator
Generates natural language insights using GenAI models
"""

import os
from typing import Dict, List, Any
import json

class AIInsightsGenerator:
    """
    Generate business insights using AI models (OpenAI GPT or Google Gemini)
    """
    
    def __init__(self, model: str = "OpenAI GPT-4"):
        """
        Initialize AI Insights Generator
        
        Args:
            model: AI model to use ("OpenAI GPT-4", "Google Gemini", "OpenAI GPT-3.5")
        """
        self.model = model
        self.api_key = self._get_api_key()
    
    def _get_api_key(self) -> str:
        """Retrieve API key from environment variables"""
        if "OpenAI" in self.model:
            return os.getenv('OPENAI_API_KEY', '')
        elif "Gemini" in self.model:
            return os.getenv('GEMINI_API_KEY', '')
        return ''
    
    def generate_insights(self, eda_results: Dict, df) -> Dict[str, Any]:
        """
        Generate comprehensive AI-powered insights
        
        Args:
            eda_results: Results from EDA engine
            df: Original DataFrame for context
        
        Returns:
            Dictionary containing executive summary, findings, and recommendations
        """
        # Prepare data summary for AI
        data_summary = self._prepare_data_summary(eda_results, df)
        
        # Check if API key is available
        if not self.api_key:
            return self._generate_fallback_insights(eda_results, df)
        
        # Generate insights using AI
        try:
            if "OpenAI" in self.model:
                return self._generate_with_openai(data_summary)
            elif "Gemini" in self.model:
                return self._generate_with_gemini(data_summary)
        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_fallback_insights(eda_results, df)
    
    def _prepare_data_summary(self, eda_results: Dict, df) -> str:
        """Prepare structured data summary for AI prompt"""
        summary_parts = []
        
        # Dataset overview
        summary_parts.append(f"Dataset Overview:")
        summary_parts.append(f"- Total rows: {len(df):,}")
        summary_parts.append(f"- Total columns: {len(df.columns)}")
        summary_parts.append(f"- Columns: {', '.join(df.columns.tolist()[:10])}")
        summary_parts.append("")
        
        # Key statistics
        if 'descriptive_stats' in eda_results and not eda_results['descriptive_stats'].empty:
            summary_parts.append("Key Statistics:")
            stats_df = eda_results['descriptive_stats']
            for col in stats_df.columns[:5]:  # First 5 columns
                summary_parts.append(f"\n{col}:")
                summary_parts.append(f"  - Mean: {stats_df.loc['mean', col]:.2f}")
                summary_parts.append(f"  - Median: {stats_df.loc['50%', col]:.2f}")
                summary_parts.append(f"  - Std Dev: {stats_df.loc['std', col]:.2f}")
            summary_parts.append("")
        
        # KPIs
        if 'kpis' in eda_results:
            summary_parts.append("Key Performance Indicators:")
            for kpi_name, kpi_value in eda_results['kpis'].items():
                summary_parts.append(f"- {kpi_name}: {kpi_value}")
            summary_parts.append("")
        
        # Correlations
        if 'correlations' in eda_results and 'strong_correlations' in eda_results['correlations']:
            strong_corrs = eda_results['correlations']['strong_correlations']
            if strong_corrs:
                summary_parts.append("Strong Correlations Detected:")
                for corr in strong_corrs[:5]:  # Top 5
                    summary_parts.append(f"- {corr['var1']} and {corr['var2']}: {corr['correlation']} ({corr['strength']})")
                summary_parts.append("")
        
        # Trends
        if 'trends' in eda_results:
            summary_parts.append("Detected Trends:")
            for trend in eda_results['trends'][:5]:  # Top 5 trends
                summary_parts.append(f"- {trend}")
            summary_parts.append("")
        
        # Time series insights
        if 'time_series' in eda_results:
            summary_parts.append("Time Series Analysis:")
            for key, value in eda_results['time_series'].items():
                if isinstance(value, dict) and 'percentage_change' in value:
                    summary_parts.append(f"- {key}: {value['percentage_change']}% change ({value['direction']})")
        
        return "\n".join(summary_parts)
    
    def _generate_with_openai(self, data_summary: str) -> Dict:
        """Generate insights using OpenAI API"""
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = self._create_prompt(data_summary)
            
            response = openai.ChatCompletion.create(
                model="gpt-4" if "GPT-4" in self.model else "gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a senior business analyst expert at extracting actionable insights from data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            return self._parse_ai_response(content)
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            raise
    
    def _generate_with_gemini(self, data_summary: str) -> Dict:
        """Generate insights using Google Gemini API"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            
            model = genai.GenerativeModel('gemini-pro')
            prompt = self._create_prompt(data_summary)
            
            response = model.generate_content(prompt)
            return self._parse_ai_response(response.text)
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            raise
    
    def _create_prompt(self, data_summary: str) -> str:
        """Create structured prompt for AI model"""
        prompt = f"""You are a senior business analyst. Analyze the following dataset statistics and provide comprehensive insights.

{data_summary}

Please provide:

1. **Executive Summary** (3-4 sentences highlighting the most critical insights)

2. **Key Findings** (5-7 bullet points with specific numbers and percentages)

3. **Notable Patterns** (Describe important trends, correlations, or anomalies)

4. **Actionable Recommendations** (3-5 strategic suggestions based on the data)

Use professional business language. Be specific with numbers. Focus on actionable insights that drive business decisions.

Format your response clearly with headers for each section."""

        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Dict:
        """Parse AI response into structured format"""
        insights = {
            'executive_summary': '',
            'key_findings': [],
            'patterns': '',
            'recommendations': []
        }
        
        # Simple parsing logic (can be enhanced with more sophisticated NLP)
        sections = response_text.split('\n\n')
        
        current_section = None
        for section in sections:
            section_lower = section.lower()
            
            if 'executive summary' in section_lower:
                current_section = 'executive_summary'
                insights['executive_summary'] = section.split('\n', 1)[-1].strip()
            
            elif 'key finding' in section_lower:
                current_section = 'key_findings'
                findings = section.split('\n')[1:]
                insights['key_findings'] = [f.strip('- ').strip() for f in findings if f.strip()]
            
            elif 'pattern' in section_lower or 'trend' in section_lower:
                current_section = 'patterns'
                insights['patterns'] = section.split('\n', 1)[-1].strip()
            
            elif 'recommendation' in section_lower:
                current_section = 'recommendations'
                recs = section.split('\n')[1:]
                insights['recommendations'] = [r.strip('- ').strip() for r in recs if r.strip()]
        
        return insights
    
    def _generate_fallback_insights(self, eda_results: Dict, df) -> Dict:
        """Generate rule-based insights when AI is not available"""
        insights = {
            'executive_summary': self._generate_fallback_summary(eda_results, df),
            'key_findings': self._generate_fallback_findings(eda_results, df),
            'patterns': self._generate_fallback_patterns(eda_results),
            'recommendations': self._generate_fallback_recommendations(eda_results, df)
        }
        
        return insights
    
    def _generate_fallback_summary(self, eda_results: Dict, df) -> str:
        """Generate executive summary without AI"""
        kpis = eda_results.get('kpis', {})
        
        summary = f"Analysis of dataset with {len(df):,} records across {len(df.columns)} variables. "
        
        if kpis:
            kpi_items = list(kpis.items())[:3]
            kpi_text = ", ".join([f"{k}: {v}" for k, v in kpi_items])
            summary += f"Key metrics include {kpi_text}. "
        
        if 'correlations' in eda_results and eda_results['correlations'].get('strong_correlations'):
            num_corrs = len(eda_results['correlations']['strong_correlations'])
            summary += f"Identified {num_corrs} strong correlations between variables. "
        
        summary += "Detailed statistical analysis and visualizations provide comprehensive insights into data patterns and trends."
        
        return summary
    
    def _generate_fallback_findings(self, eda_results: Dict, df) -> List[str]:
        """Generate key findings without AI"""
        findings = []
        
        # Dataset size finding
        findings.append(f"Dataset contains {len(df):,} records with {len(df.columns)} variables")
        
        # KPI findings
        kpis = eda_results.get('kpis', {})
        for kpi_name, kpi_value in list(kpis.items())[:3]:
            findings.append(f"{kpi_name}: {kpi_value}")
        
        # Correlation findings
        if 'correlations' in eda_results:
            strong_corrs = eda_results['correlations'].get('strong_correlations', [])
            for corr in strong_corrs[:2]:
                findings.append(f"{corr['strength']} correlation ({corr['correlation']}) between {corr['var1']} and {corr['var2']}")
        
        # Trend findings
        trends = eda_results.get('trends', [])
        findings.extend(trends[:3])
        
        return findings
    
    def _generate_fallback_patterns(self, eda_results: Dict) -> str:
        """Generate pattern description without AI"""
        patterns = []
        
        if 'distributions' in eda_results:
            for col, dist_info in list(eda_results['distributions'].items())[:3]:
                if dist_info.get('is_normal'):
                    patterns.append(f"{col} follows a normal distribution")
                elif abs(dist_info.get('skewness', 0)) > 1:
                    direction = "right" if dist_info['skewness'] > 0 else "left"
                    patterns.append(f"{col} is skewed to the {direction}")
        
        return ". ".join(patterns) if patterns else "Various statistical patterns detected in the data."
    
    def _generate_fallback_recommendations(self, eda_results: Dict, df) -> List[str]:
        """Generate recommendations without AI"""
        recommendations = []
        
        # Check for missing data
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_pct > 5:
            recommendations.append(f"Address data quality: {missing_pct:.1f}% of values are missing")
        
        # Check for correlations
        if 'correlations' in eda_results:
            strong_corrs = eda_results['correlations'].get('strong_correlations', [])
            if strong_corrs:
                recommendations.append(f"Investigate {len(strong_corrs)} strong correlations for potential causal relationships")
        
        # General recommendations
        recommendations.append("Continue monitoring key metrics to track performance trends")
        recommendations.append("Consider segmentation analysis for deeper insights into categorical variables")
        recommendations.append("Implement automated reporting to track changes over time")
        
        return recommendations[:5]
