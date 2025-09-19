AI Financial Document Analyzer 🤖

---

## Overview

This project enables users to upload financial PDF documents and receive AI-generated analysis, including key insights, investment recommendations, and risk assessments. The backend is built with FastAPI and leverages CrewAI, LangChain, and OpenAI for advanced document understanding.

---

## ✨ Features

- **PDF Upload:** Accepts financial reports in PDF format.
- **AI-Powered Analysis:** Uses advanced language models (via LangChain and OpenAI) to interpret complex financial data.
- **Structured Reporting:** Automatically generates a report with:
    - Key Financial Insights
    - Investment Recommendations
    - Risk Assessment
- **Agentic Workflow:** Employs a custom financial analyst agent with specialized tools for document analysis.
- **REST API:** Simple, robust API for integration and testing.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Uvicorn
- **AI Framework:** CrewAI
- **LLM Integration:** LangChain, OpenAI
- **PDF Processing:** PyPDFLoader (LangChain)
- **Dependencies:** Python 3.9+, Pip, python-dotenv

---

## ⚙️ Setup & Installation

1. **Clone the Repository**
     ```bash
     git clone <your-repo-url>
     cd <your-repo-name>
     ```

2. **Create and Activate a Virtual Environment**
     - **macOS/Linux:**
         ```bash
         python3 -m venv venv
         source venv/bin/activate
         ```
     - **Windows:**
         ```bash
         python -m venv venv
         venv\Scripts\activate
         ```

3. **Install Dependencies**
     - Create a `requirements.txt` file with:
         ```
         fastapi
         uvicorn
         python-multipart
         python-dotenv
         crewai
         crewai-tools
         langchain-openai
         pypdf
         ```
     - Install with:
         ```bash
         pip install -r requirements.txt
         ```

4. **Configure Environment Variables**
     - Create a `.env` file in your project root:
         ```
         OPENAI_API_KEY="sk-..."
         ```

---

## 🚀 Usage

Start the API server:
```bash
uvicorn main:app --reload
```
The server will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## 📖 API Documentation

### Analyze Financial Document

- **Endpoint:** `/analyze`
- **Method:** `POST`
- **Request Body:** `multipart/form-data`
    - `file` (UploadFile, required): The PDF document to analyze.
    - `query` (str, optional): Your question or instruction for the analysis.

#### Example cURL Request

```bash
curl -X 'POST' \
    'http://127.0.0.1:8000/analyze' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'file=@/path/to/your/financial_report.pdf' \
    -F 'query=What are the main risks and investment opportunities in this report?'
```

#### Success Response (`200 OK`)

```json
{
    "status": "success",
    "query": "What are the main risks and investment opportunities in this report?",
    "analysis": "...",
    "file_processed": "financial_report.pdf"
}
```

---

## 🐛 Debugging Journey: Bugs & Fixes
---

## 🐞 Notable Bugs & Fixes

### **1. requirements.txt: Dependency Conflicts**
**Bug:**  
The file specified a very old `crewai` version (`0.130.0`), which used a completely different API than modern versions. It also pinned an outdated `pydantic` version, causing installation failures and conflicts.

**Fix:**  
The `requirements.txt` file was updated to use current, stable versions of `crewai` and `crewai-tools`. The rigid version pin for `pydantic` was removed, and the file was cleaned up to include only the essential packages, ensuring a stable installation.

---

### **2. tools.py: Incorrect Tool Definitions**
**Bug:**  
The tools were defined as methods inside simple classes, which is not a valid structure for CrewAI. The PDF reader used an undefined class, and the methods were incorrectly marked as `async`.

**Fix:**  
All tools were refactored into standalone Python functions and decorated with the `@tool` decorator from `crewai_tools` for proper registration. The PDF loading logic was fixed by implementing the standard `PyPDFLoader` from the LangChain library.

---

### **3. agents.py: Flawed Agent & LLM Configuration**
**Bug:**  
The Language Model (LLM) was never properly initialized (due to the `llm = llm` circular reference). The Agent constructor used the wrong parameter name (`tool=[]` instead of `tools=[]`), and the agent's instructions (goal, backstory) were satirical and non-functional.

**Fix:**  
The LLM is now correctly initialized using `ChatOpenAI` and loads the API key from the `.env` file. The parameter was corrected to `tools=[...]`. Most importantly, the role, goal, and backstory were rewritten to provide clear, direct, and professional instructions to the AI.

---

### **4. task.py: Ineffective Task Definitions**
**Bug:**  
The task's `description` and `expected_output` were vague and would have led to poor, unpredictable results. Tools were also incorrectly assigned at the task level.

**Fix:**  
The logic was consolidated into a single, comprehensive task. The `description` was rewritten to be a clear, multi-step plan for the agent. The `expected_output` now instructs the AI on the exact format of the final report, ensuring a structured and reliable response.

---

### **5. main.py: Broken Crew Execution Logic**
**Bug:**  
The function responsible for running the crew had a hardcoded file path and did not pass the path of the newly uploaded file to the agent. The `kickoff` method was only given the query, so the agent had no context for which file to analyze.

**Fix:**  
The `run_crew` function was modified to accept the dynamic `file_path` as a parameter. The `financial_crew.kickoff` call was updated to pass a dictionary containing both the `query` and the `file_path`, making this critical context available to the agent and its tools.

/**
 * Note:
 * - All identified bugs have been fixed and the code runs correctly.
 * - The only remaining issue is running out of API calls from the LLM due to quota limits.
 */
---
