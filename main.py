from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import tempfile
import shutil

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import (
    document_verification, 
    analyze_financial_document, 
    investment_analysis, 
    risk_assessment, 
    final_summary
)

app = FastAPI(
    title="Financial Document Analyzer",
    description="Professional financial document analysis and investment insights",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_financial_crew():
    """Create and configure the financial analysis crew"""
    return Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[
            document_verification,
            analyze_financial_document,
            investment_analysis,
            risk_assessment,
            final_summary
        ],
        process=Process.sequential,
        verbose=True
    )

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Financial Document Analyzer API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "document_processor": "ready",
            "financial_analyzer": "ready",
            "risk_assessor": "ready"
        }
    }

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(..., description="Financial document (PDF format)"),
    query: str = Form(
        default="Provide comprehensive financial analysis and investment insights", 
        description="Specific analysis request or question"
    )
):
    """
    Analyze uploaded financial document and provide comprehensive insights
    
    - **file**: PDF financial document to analyze
    - **query**: Specific question or analysis request
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are supported"
        )
    
    # Create unique file identifier
    file_id = str(uuid.uuid4())
    temp_file_path = None
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', prefix=f'financial_{file_id}_') as temp_file:
            temp_file_path = temp_file.name
            
            # Copy uploaded file content to temporary file
            shutil.copyfileobj(file.file, temp_file)
        
        # Validate query
        if not query or query.strip() == "":
            query = "Provide comprehensive financial analysis and investment insights"
        
        # Update the global variable used by tools (temporary workaround)
        os.environ['CURRENT_DOCUMENT_PATH'] = temp_file_path
        
        # Create and run the financial analysis crew
        financial_crew = create_financial_crew()
        
        # Execute the analysis
        result = financial_crew.kickoff({
            'query': query.strip(),
            'file_path': temp_file_path
        })
        
        return {
            "status": "success",
            "file_processed": file.filename,
            "query": query.strip(),
            "analysis": {
                "summary": str(result)
            },
            "metadata": {
                "document_id": file_id,
                "processing_type": "comprehensive_analysis"
            }
        }
        
    except Exception as e:
        error_message = f"Error processing financial document: {str(e)}"
        
        # Log the error
        print(f"Analysis error: {error_message}")
        
        raise HTTPException(
            status_code=500, 
            detail={
                "error": error_message,
                "file_processed": file.filename,
                "suggestions": [
                    "Ensure the PDF contains readable text",
                    "Check if the document is a valid financial report",
                    "Try with a different PDF file",
                    "Make sure your OpenAI API key is set correctly"
                ]
            }
        )
    
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {temp_file_path}: {e}")
        
        # Clean up environment variable
        if 'CURRENT_DOCUMENT_PATH' in os.environ:
            del os.environ['CURRENT_DOCUMENT_PATH']

@app.post("/quick-analysis")
async def quick_analysis(
    file: UploadFile = File(..., description="Financial document (PDF format)"),
    query: str = Form(
        default="Provide key financial metrics and basic analysis", 
        description="Specific analysis request"
    )
):
    """
    Quick financial document analysis (faster, less comprehensive)
    """
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    file_id = str(uuid.uuid4())
    temp_file_path = None
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', prefix=f'quick_{file_id}_') as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
        
        if not query or query.strip() == "":
            query = "Provide key financial metrics and basic analysis"
        
        os.environ['CURRENT_DOCUMENT_PATH'] = temp_file_path
        
        # Create simplified crew with fewer tasks
        quick_crew = Crew(
            agents=[verifier, financial_analyst],
            tasks=[document_verification, analyze_financial_document],
            process=Process.sequential,
            verbose=False
        )
        
        result = quick_crew.kickoff({
            'query': query.strip(),
            'file_path': temp_file_path
        })
        
        return {
            "status": "success",
            "analysis_type": "quick",
            "file_processed": file.filename,
            "query": query.strip(),
            "analysis": str(result),
            "metadata": {
                "document_id": file_id,
                "processing_type": "quick_analysis"
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in quick analysis: {str(e)}"
        )
    
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as e:
                print(f"Warning: Could not remove temporary file: {e}")
        
        if 'CURRENT_DOCUMENT_PATH' in os.environ:
            del os.environ['CURRENT_DOCUMENT_PATH']

if __name__ == "__main__":
    import uvicorn
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not found in environment variables!")
        print("Please set your OpenAI API key in the .env file")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )