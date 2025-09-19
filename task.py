from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, read_financial_document, analyze_investment, assess_risks

# Document Verification Task
document_verification = Task(
    description="""
    Verify and validate the uploaded financial document to ensure it contains legitimate financial information.
    
    Your tasks:
    1. Read and extract content from the financial document using read_financial_document function
    2. Verify it contains actual financial data (statements, reports, filings, etc.)
    3. Identify the document type (annual report, quarterly filing, earnings report, etc.)
    4. Extract basic company information if available
    5. Confirm the document is suitable for financial analysis
    
    Use the read_financial_document function to extract the document content.
    User query: {query}
    """,
    expected_output="""
    A verification report containing:
    - Document validation status (Valid/Invalid)
    - Document type identification
    - Company name and basic information (if available)
    - Brief summary of document contents
    - Recommendation on whether document can proceed to analysis
    """,
    agent=verifier,
    async_execution=False,
)

# Financial Analysis Task
analyze_financial_document = Task(
    description="""
    Conduct comprehensive financial analysis of the verified financial document based on the user's query: {query}
    
    Your analysis should include:
    1. Extract and analyze key financial metrics (revenue, profit, assets, liabilities, cash flow)
    2. Identify financial trends and patterns
    3. Assess company's financial health and performance
    4. Highlight significant financial events or changes
    5. Provide context for the financial data presented
    6. Compare metrics to industry standards where possible
    
    Use the read_financial_document and analyze_investment functions to perform the analysis.
    Focus on providing accurate, data-driven insights based on the actual document content.
    """,
    expected_output="""
    A comprehensive financial analysis report including:
    - Executive summary of financial performance
    - Key financial metrics with explanations
    - Identified trends and patterns
    - Financial strengths and areas of concern
    - Significant observations from the financial data
    - Professional assessment of company's financial position
    """,
    agent=financial_analyst,
    async_execution=False,
    context=[document_verification]
)

# Investment Analysis Task
investment_analysis = Task(
    description="""
    Based on the financial analysis, provide professional investment insights and recommendations.
    
    Consider the user's query: {query}
    
    Your analysis should cover:
    1. Investment attractiveness based on financial metrics
    2. Growth potential and market opportunities  
    3. Competitive positioning
    4. Valuation considerations
    5. Investment timeline considerations
    6. Sector-specific factors affecting investment potential
    
    Use the analyze_investment function to support your analysis.
    Provide balanced, objective investment perspective based on the financial data.
    """,
    expected_output="""
    Professional investment analysis containing:
    - Investment thesis summary
    - Key investment highlights (positive factors)
    - Investment concerns (risk factors)
    - Growth drivers and catalysts
    - Competitive advantages/disadvantages
    - Investment recommendation with rationale
    - Suitable investor profile for this investment
    """,
    agent=investment_advisor,
    async_execution=False,
    context=[analyze_financial_document]
)

# Risk Assessment Task
risk_assessment = Task(
    description="""
    Conduct thorough risk assessment of the financial document and investment opportunity.
    
    Focus on the user's specific concerns: {query}
    
    Analyze:
    1. Financial risks (liquidity, solvency, profitability)
    2. Market risks (competition, industry trends, economic factors)
    3. Operational risks (business model, management, operations)
    4. Regulatory and compliance risks
    5. Risk mitigation factors already in place
    6. Overall risk profile assessment
    
    Use the assess_risks function to support your analysis.
    Provide practical risk management recommendations.
    """,
    expected_output="""
    Comprehensive risk assessment report including:
    - Overall risk rating (Low/Medium/High)
    - Detailed breakdown of identified risks by category
    - Risk impact and probability assessments
    - Existing risk mitigation measures
    - Recommended risk management strategies
    - Key risk monitoring metrics
    - Risk tolerance considerations for investors
    """,
    agent=risk_assessor,
    async_execution=False,
    context=[analyze_financial_document]
)

# Final Summary Task
final_summary = Task(
    description="""
    Synthesize all previous analyses into a comprehensive final report addressing the user's query: {query}
    
    Combine insights from:
    - Document verification
    - Financial analysis  
    - Investment analysis
    - Risk assessment
    
    Provide actionable conclusions and recommendations.
    """,
    expected_output="""
    Executive summary report containing:
    - Key findings from all analyses
    - Overall investment recommendation
    - Critical risk factors to monitor
    - Action items for the user
    - Next steps for further analysis if needed
    - Clear, concise conclusions addressing the user's original query
    """,
    agent=financial_analyst,
    async_execution=False,
    context=[document_verification, analyze_financial_document, investment_analysis, risk_assessment]
)