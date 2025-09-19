#!/usr/bin/env python3
"""
Simple test script for the Financial Document Analyzer API
"""

import requests
import json
import os

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_analyze_endpoint(pdf_file_path, query="Analyze this financial document"):
    """Test the analyze endpoint with a PDF file"""
    if not os.path.exists(pdf_file_path):
        print(f"❌ Test file not found: {pdf_file_path}")
        return False
    
    try:
        with open(pdf_file_path, 'rb') as f:
            files = {'file': (os.path.basename(pdf_file_path), f, 'application/pdf')}
            data = {'query': query}
            
            print(f"🔄 Analyzing {pdf_file_path}...")
            print(f"Query: {query}")
            
            response = requests.post(
                "http://localhost:8000/analyze",
                files=files,
                data=data,
                timeout=300  # 5 minute timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Analysis completed successfully!")
                print(f"Status: {result.get('status')}")
                print(f"File processed: {result.get('file_processed')}")
                
                # Print first 500 characters of analysis
                analysis = result.get('analysis', {}).get('summary', 'No analysis found')
                print(f"Analysis preview: {str(analysis)[:500]}...")
                
                return True
            else:
                print(f"❌ Analysis failed: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"Error details: {json.dumps(error_detail, indent=2)}")
                except:
                    print(f"Error response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def test_quick_analysis(pdf_file_path, query="Quick analysis"):
    """Test the quick analysis endpoint"""
    if not os.path.exists(pdf_file_path):
        print(f"❌ Test file not found: {pdf_file_path}")
        return False
    
    try:
        with open(pdf_file_path, 'rb') as f:
            files = {'file': (os.path.basename(pdf_file_path), f, 'application/pdf')}
            data = {'query': query}
            
            print(f"🔄 Quick analyzing {pdf_file_path}...")
            
            response = requests.post(
                "http://localhost:8000/quick-analysis",
                files=files,
                data=data,
                timeout=120  # 2 minute timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Quick analysis completed!")
                print(f"Status: {result.get('status')}")
                
                # Print first 300 characters of analysis
                analysis = result.get('analysis', 'No analysis found')
                print(f"Analysis preview: {str(analysis)[:300]}...")
                
                return True
            else:
                print(f"❌ Quick analysis failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Quick analysis error: {e}")
        return False

def create_sample_pdf():
    """Create a simple sample PDF for testing if none exists"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        filename = "sample_financial_report.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        # Add sample financial content
        c.drawString(100, 750, "SAMPLE FINANCIAL REPORT")
        c.drawString(100, 720, "Company: Sample Corp Inc")
        c.drawString(100, 690, "Annual Report 2023")
        c.drawString(100, 650, "")
        c.drawString(100, 620, "FINANCIAL HIGHLIGHTS:")
        c.drawString(100, 590, "Revenue: $1,250 million")
        c.drawString(100, 560, "Net Income: $156 million")
        c.drawString(100, 530, "Total Assets: $2,500 million")
        c.drawString(100, 500, "Cash and Equivalents: $300 million")
        c.drawString(100, 470, "")
        c.drawString(100, 440, "The company showed strong growth in revenue")
        c.drawString(100, 410, "and improved operational efficiency.")
        c.drawString(100, 380, "Market competition remains challenging.")
        
        c.save()
        print(f"✅ Created sample PDF: {filename}")
        return filename
        
    except ImportError:
        print("⚠️  reportlab not installed. Cannot create sample PDF.")
        print("Install with: pip install reportlab")
        return None
    except Exception as e:
        print(f"❌ Error creating sample PDF: {e}")
        return None

def main():
    """Main test function"""
    print("🧪 Testing Financial Document Analyzer API")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    if not test_health_check():
        print("API is not running. Please start it with: python main.py")
        return
    
    # Check if we have a test PDF file
    test_files = [
        "sample_financial_report.pdf",
        "test_financial_document.pdf",
        "annual_report.pdf"
    ]
    
    test_file = None
    for filename in test_files:
        if os.path.exists(filename):
            test_file = filename
            break
    
    if not test_file:
        print("\n📄 No test PDF found. Creating sample PDF...")
        test_file = create_sample_pdf()
        
        if not test_file:
            print("❌ Cannot create test file. Please provide a PDF file to test with.")
            return
    
    # Test 2: Quick analysis
    print(f"\n2. Testing quick analysis with {test_file}...")
    test_quick_analysis(test_file, "Provide key financial metrics")
    
    # Test 3: Full analysis
    print(f"\n3. Testing full analysis with {test_file}...")
    test_analyze_endpoint(
        test_file, 
        "Analyze this company's financial performance and investment potential"
    )
    
    print("\n🎉 Testing completed!")
    print("\nTo test with your own PDF file:")
    print("python test_api.py path/to/your/financial_report.pdf")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Use provided PDF file
        pdf_path = sys.argv[1]
        if os.path.exists(pdf_path):
            print(f"🧪 Testing with provided file: {pdf_path}")
            print("=" * 50)
            
            test_health_check()
            test_quick_analysis(pdf_path)
            test_analyze_endpoint(pdf_path)
        else:
            print(f"❌ File not found: {pdf_path}")
    else:
        # Run standard tests
        main()