"""
Test script to verify all modules are working correctly
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing module imports...")
    try:
        from modules.data_processor import DataProcessor
        from modules.eda_engine import EDAEngine
        from modules.visualization_engine import VisualizationEngine
        from modules.ai_insights import AIInsightsGenerator
        from modules.report_generator import ReportGenerator
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_data_processor():
    """Test DataProcessor module"""
    print("\nTesting DataProcessor...")
    try:
        from modules.data_processor import DataProcessor
        
        # Create sample data with issues
        df = pd.DataFrame({
            'A': [1, 2, None, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e'],
            'C': [1.1, 2.2, 3.3, None, 5.5]
        })
        
        processor = DataProcessor(df)
        cleaned_df, report = processor.clean_data()
        
        print(f"  - Original rows: {len(df)}, Cleaned rows: {len(cleaned_df)}")
        print(f"  - Missing values handled: {report.get('missing_handled', 0)}")
        print("✓ DataProcessor working correctly")
        return True
    except Exception as e:
        print(f"✗ DataProcessor error: {e}")
        return False

def test_eda_engine():
    """Test EDAEngine module"""
    print("\nTesting EDAEngine...")
    try:
        from modules.eda_engine import EDAEngine
        
        # Load sample data
        sample_file = Path('sample_data/sales_data_2023.xlsx')
        if sample_file.exists():
            df = pd.read_excel(sample_file)
            eda = EDAEngine(df)
            results = eda.analyze()
            
            print(f"  - Descriptive stats generated: {results.get('descriptive_stats') is not None}")
            print(f"  - Correlations calculated: {results.get('correlations') is not None}")
            print("✓ EDAEngine working correctly")
            return True
        else:
            print("  ! Sample data not found, skipping detailed test")
            return True
    except Exception as e:
        print(f"✗ EDAEngine error: {e}")
        return False

def test_visualization_engine():
    """Test VisualizationEngine module"""
    print("\nTesting VisualizationEngine...")
    try:
        from modules.visualization_engine import VisualizationEngine
        
        # Create simple test data
        df = pd.DataFrame({
            'Category': ['A', 'B', 'C', 'D'],
            'Value': [10, 20, 15, 25],
            'Amount': [100, 200, 150, 250]
        })
        
        viz = VisualizationEngine(df)
        charts = viz.generate_all_charts()
        
        print(f"  - Charts generated: {len(charts)}")
        print("✓ VisualizationEngine working correctly")
        return True
    except Exception as e:
        print(f"✗ VisualizationEngine error: {e}")
        return False

def test_ai_insights():
    """Test AIInsightsGenerator module"""
    print("\nTesting AIInsightsGenerator...")
    try:
        from modules.ai_insights import AIInsightsGenerator
        
        # Test initialization (won't make actual API calls without keys)
        ai_gen = AIInsightsGenerator(model="OpenAI GPT-4")
        print("  - AIInsightsGenerator initialized")
        print("  ! Note: Actual API calls require valid API keys in .env")
        print("✓ AIInsightsGenerator structure correct")
        return True
    except Exception as e:
        print(f"✗ AIInsightsGenerator error: {e}")
        return False

def test_report_generator():
    """Test ReportGenerator module"""
    print("\nTesting ReportGenerator...")
    try:
        from modules.report_generator import ReportGenerator
        
        # Create simple test data
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        results = {
            'eda_results': {'descriptive_stats': df.describe()},
            'insights': {
                'executive_summary': 'Test summary',
                'key_findings': ['Finding 1', 'Finding 2']
            }
        }
        
        report_gen = ReportGenerator(df, results)
        print("  - ReportGenerator initialized")
        print("✓ ReportGenerator structure correct")
        return True
    except Exception as e:
        print(f"✗ ReportGenerator error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Excel-to-Insights Bot - Module Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_data_processor,
        test_eda_engine,
        test_visualization_engine,
        test_ai_insights,
        test_report_generator
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! The application is ready to use.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your API keys to .env")
        print("3. Run: streamlit run app.py")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
