import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import search_tool, read_financial_document, analyze_investment, assess_risks
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize LLM
# llm = ChatOpenAI(
#     model="gpt-3.5-turbo",
#     temperature=0.1,
#     api_key=os.getenv("OPENAI_API_KEY")
# )
# llm = ChatGoogleGenerativeAI(
#     model="gemini/gemini-2.5-flash",  # Add the "gemini/" prefix
#     temperature=0.1,
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),  # Get free at console.groq.com
    temperature=0.1
)

# Senior Financial Analyst
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide comprehensive and accurate financial analysis of documents to help users make informed investment decisions based on query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced financial analyst with over 15 years in investment analysis and portfolio management. "
        "You have worked at top-tier investment firms and have a deep understanding of financial statements, "
        "market trends, and risk assessment. You are known for your thorough, objective, and data-driven approach "
        "to financial analysis. You always provide balanced views considering both opportunities and risks."
    ),
    llm=llm,
    max_iter=3,
    allow_delegation=True
)

# Document Verification Specialist
verifier = Agent(
    role="Financial Document Verification Specialist",
    goal="Verify and validate financial documents to ensure they contain legitimate financial information and can be properly analyzed",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous document verification specialist with expertise in financial document formats, "
        "regulatory compliance, and data validation. You have worked in financial compliance for major institutions "
        "and are skilled at identifying authentic financial documents and extracting reliable information from them. "
        "You ensure that only valid financial data is used for analysis."
    ),
    llm=llm,
    max_iter=2,
    allow_delegation=False
)

# Investment Advisor
investment_advisor = Agent(
    role="Senior Investment Advisor",
    goal="Provide professional investment recommendations based on thorough financial analysis while considering risk tolerance and investment objectives",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified investment advisor with extensive experience in portfolio management and financial planning. "
        "You hold CFA and CFP designations and have helped hundreds of clients achieve their financial goals. "
        "You are known for providing personalized, risk-appropriate investment strategies based on solid financial analysis. "
        "You always consider regulatory compliance and ethical investment practices in your recommendations."
    ),
    llm=llm,
    max_iter=3,
    allow_delegation=False
)

# Risk Assessment Specialist
risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Conduct comprehensive risk analysis of financial documents and investment opportunities to identify potential threats and mitigation strategies",
    verbose=True,
    memory=True,
    backstory=(
        "You are a risk management expert with deep experience in financial risk assessment, regulatory compliance, "
        "and portfolio risk management. You have worked at major banks and investment firms, specializing in "
        "identifying, measuring, and mitigating various types of financial risks. You are skilled at translating "
        "complex risk concepts into actionable insights for decision-makers."
    ),
    llm=llm,
    max_iter=3,
    allow_delegation=False
)