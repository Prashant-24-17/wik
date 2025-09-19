import os
import re
from typing import Dict, List
from dotenv import load_dotenv
load_dotenv()

from crewai_tools.tools.serper_dev_tool import serper_dev_tool
import pypdf

# Creating search tool
search_tool = serper_dev_tool

def read_financial_document(path: str = None) -> str:
    """Read and extract text from financial PDF document
    
    Args:
        path (str): Path to the PDF file
        
    Returns:
        str: Extracted text content from the PDF
    """
    try:
        # Use the path from environment variable if not provided
        if path is None:
            path = os.getenv('CURRENT_DOCUMENT_PATH', 'data/sample.pdf')
        
        if not os.path.exists(path):
            return f"Error: File not found at path: {path}"
        
        # Read PDF using pypdf
        with open(path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            text_content = ""
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text = page.extract_text()
                    if text.strip():
                        text_content += f"\n--- Page {page_num + 1} ---\n{text}\n"
                except Exception as e:
                    print(f"Warning: Could not extract text from page {page_num + 1}: {e}")
                    continue
        
        if not text_content.strip():
            return "Error: No readable content found in the PDF"
        
        # Clean the extracted text
        cleaned_text = clean_text(text_content)
        return cleaned_text
        
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def clean_text(text: str) -> str:
    """Clean and format extracted text"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n ', '\n', text)
    
    return text.strip()

def analyze_investment(financial_document_data: str) -> Dict:
    """Analyze financial document for investment insights
    
    Args:
        financial_document_data (str): The financial document content
        
    Returns:
        Dict: Investment analysis results
    """
    if not financial_document_data or financial_document_data.startswith("Error:"):
        return {"error": "No valid financial data provided for analysis"}
    
    analysis = {
        "document_summary": extract_document_info(financial_document_data),
        "financial_metrics": extract_financial_metrics(financial_document_data),
        "key_highlights": extract_highlights(financial_document_data),
        "investment_recommendation": generate_recommendation(financial_document_data)
    }
    
    return analysis

def extract_document_info(text: str) -> Dict:
    """Extract basic document information"""
    info = {
        "document_type": "Financial Document",
        "company_name": "Not identified",
        "reporting_period": "Not specified"
    }
    
    # Try to identify document type
    text_lower = text.lower()
    if "annual report" in text_lower or "10-k" in text_lower:
        info["document_type"] = "Annual Report"
    elif "quarterly" in text_lower or "10-q" in text_lower:
        info["document_type"] = "Quarterly Report"
    elif "earnings" in text_lower:
        info["document_type"] = "Earnings Report"
    
    # Try to extract company name
    company_pattern = r'([A-Z][A-Za-z\s&]+(?:Inc|Corp|Corporation|Ltd|Limited|LLC)\.?)'
    match = re.search(company_pattern, text[:2000])
    if match:
        info["company_name"] = match.group(1).strip()
    
    return info

def extract_financial_metrics(text: str) -> Dict:
    """Extract key financial metrics"""
    metrics = {}
    
    # Common financial terms to look for
    financial_terms = {
        "revenue": ["revenue", "net sales", "total revenue"],
        "net_income": ["net income", "net profit", "net earnings"],
        "total_assets": ["total assets"],
        "cash": ["cash", "cash and equivalents"]
    }
    
    for metric, keywords in financial_terms.items():
        values = find_monetary_values(text, keywords)
        if values:
            metrics[metric] = values[0]  # Take first found value
    
    return metrics

def find_monetary_values(text: str, keywords: List[str]) -> List[str]:
    """Find monetary values associated with keywords"""
    values = []
    
    for keyword in keywords:
        pattern = rf'{re.escape(keyword)}[:\s]*\$?\s*([\d,]+(?:\.\d+)?)\s*(?:million|billion|M|B)?'
        matches = re.finditer(pattern, text, re.IGNORECASE)
        
        for match in matches:
            value = match.group(1)
            context = match.group(0)
            if 'million' in context.lower() or 'M' in context:
                value = f"${value}M"
            elif 'billion' in context.lower() or 'B' in context:
                value = f"${value}B"
            else:
                value = f"${value}"
            values.append(value)
    
    return values

def extract_highlights(text: str) -> List[str]:
    """Extract key highlights from the document"""
    highlights = []
    
    # Look for positive indicators
    positive_patterns = [
        r'(?:growth|increased|improved|strong).{0,100}',
        r'(?:expansion|acquisition|new product).{0,100}',
        r'(?:dividend|share repurchase).{0,100}'
    ]
    
    for pattern in positive_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            highlight = match.group(0).strip()
            if len(highlight) > 20 and len(highlight) < 200:
                highlights.append(highlight)
    
    return highlights[:5]  # Return top 5 highlights

def generate_recommendation(text: str) -> str:
    """Generate a basic investment recommendation"""
    text_lower = text.lower()
    
    positive_indicators = ['growth', 'increased', 'improved', 'strong', 'expansion']
    negative_indicators = ['declined', 'decreased', 'loss', 'challenging', 'restructuring']
    
    positive_count = sum(text_lower.count(term) for term in positive_indicators)
    negative_count = sum(text_lower.count(term) for term in negative_indicators)
    
    if positive_count > negative_count * 1.2:
        return "POSITIVE - Document shows favorable indicators for investment consideration"
    elif negative_count > positive_count * 1.2:
        return "CAUTIOUS - Document shows some concerning factors requiring careful analysis"
    else:
        return "NEUTRAL - Mixed indicators suggest further analysis needed"

def assess_risks(financial_document_data: str) -> Dict:
    """Assess risks in the financial document
    
    Args:
        financial_document_data (str): The financial document content
        
    Returns:
        Dict: Risk assessment results
    """
    if not financial_document_data or financial_document_data.startswith("Error:"):
        return {"error": "No valid financial data provided for risk assessment"}
    
    risk_assessment = {
        "overall_risk_level": "MEDIUM",
        "identified_risks": identify_risks(financial_document_data),
        "financial_stability": assess_financial_stability(financial_document_data),
        "market_risks": assess_market_risks(financial_document_data),
        "recommendations": generate_risk_recommendations(financial_document_data)
    }
    
    # Determine overall risk level
    risk_assessment["overall_risk_level"] = calculate_overall_risk(risk_assessment)
    
    return risk_assessment

def identify_risks(text: str) -> List[str]:
    """Identify explicit risk factors mentioned in the document"""
    risks = []
    text_lower = text.lower()
    
    risk_keywords = [
        'debt', 'liquidity', 'competition', 'regulatory', 'market volatility',
        'credit risk', 'operational risk', 'litigation', 'compliance'
    ]
    
    for keyword in risk_keywords:
        if keyword in text_lower:
            risks.append(keyword.title() + " concerns mentioned")
    
    # Look for risk factors section
    risk_section = re.search(r'risk factors?:?(.*?)(?:item|section|\n\n)', text, re.IGNORECASE | re.DOTALL)
    if risk_section:
        risks.append("Dedicated risk factors section identified")
    
    return risks[:10]  # Limit to top 10 risks

def assess_financial_stability(text: str) -> str:
    """Assess financial stability based on document content"""
    text_lower = text.lower()
    
    stability_indicators = {
        'positive': ['strong cash', 'profitable', 'stable revenue', 'low debt'],
        'negative': ['cash shortage', 'loss', 'high debt', 'declining revenue']
    }
    
    positive_score = sum(text_lower.count(term) for term in stability_indicators['positive'])
    negative_score = sum(text_lower.count(term) for term in stability_indicators['negative'])
    
    if positive_score > negative_score:
        return "STABLE - Positive financial stability indicators"
    elif negative_score > positive_score:
        return "CONCERNING - Several financial stability concerns"
    else:
        return "MIXED - Balanced financial stability indicators"

def assess_market_risks(text: str) -> List[str]:
    """Assess market-related risks"""
    market_risks = []
    text_lower = text.lower()
    
    market_risk_terms = {
        'competition': 'Competitive pressure identified',
        'market volatility': 'Market volatility concerns',
        'economic uncertainty': 'Economic uncertainty factors',
        'regulatory changes': 'Regulatory change risks'
    }
    
    for term, description in market_risk_terms.items():
        if term in text_lower:
            market_risks.append(description)
    
    return market_risks

def generate_risk_recommendations(text: str) -> List[str]:
    """Generate risk management recommendations"""
    recommendations = [
        "Monitor financial metrics regularly",
        "Diversify investment portfolio",
        "Stay informed about industry trends",
        "Review risk tolerance periodically"
    ]
    
    # Add specific recommendations based on identified risks
    text_lower = text.lower()
    if 'debt' in text_lower:
        recommendations.append("Pay attention to debt levels and coverage ratios")
    if 'competition' in text_lower:
        recommendations.append("Monitor competitive landscape changes")
    
    return recommendations[:6]

def calculate_overall_risk(assessment: Dict) -> str:
    """Calculate overall risk level"""
    risk_factors = len(assessment.get('identified_risks', []))
    financial_stability = assessment.get('financial_stability', '')
    market_risks = len(assessment.get('market_risks', []))
    
    total_risk_score = risk_factors + market_risks
    
    if 'CONCERNING' in financial_stability:
        total_risk_score += 3
    elif 'STABLE' in financial_stability:
        total_risk_score -= 1
    
    if total_risk_score <= 3:
        return "LOW"
    elif total_risk_score <= 7:
        return "MEDIUM"
    else:
        return "HIGH"