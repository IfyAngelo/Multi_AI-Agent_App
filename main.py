import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from src.agents import AgentManager

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Multi-Agent AI System API", version="1.0")

# Initialize Agent Manager
agent_manager = AgentManager(max_retries=3, verbose=True)

# ------------------- Request Models -------------------

class SummarizationRequest(BaseModel):
    text: str
    llm_provider: str = "openai"

class WritingRequest(BaseModel):
    topic: str
    outline: str = None
    llm_provider: str = "openai"

class SanitizationRequest(BaseModel):
    medical_data: str
    llm_provider: str = "openai"

# ------------------- Summarization Endpoint -------------------

@app.post("/summarize/")
async def summarize_text(request: SummarizationRequest):
    """API for summarizing medical text."""
    main_agent = agent_manager.get_agent("summarize")
    validator_agent = agent_manager.get_agent("summarize_validator")

    main_agent.llm_provider = request.llm_provider.lower()

    try:
        summary = main_agent.execute(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization Error: {str(e)}")

    try:
        validation = validator_agent.execute(original_text=request.text, summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation Error: {str(e)}")

    return {
        "summary": summary,
        "validation": validation
    }

# ------------------- Writing & Refining Endpoint -------------------

@app.post("/write_and_refine/")
async def write_and_refine_article(request: WritingRequest):
    """API for writing and refining research articles."""
    writer_agent = agent_manager.get_agent("write_article")
    refiner_agent = agent_manager.get_agent("refiner")
    validator_agent = agent_manager.get_agent("validator")

    writer_agent.llm_provider = request.llm_provider.lower()
    refiner_agent.llm_provider = request.llm_provider.lower()
    validator_agent.llm_provider = request.llm_provider.lower()

    try:
        draft = writer_agent.execute(request.topic, request.outline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Writing Error: {str(e)}")

    try:
        refined_article = refiner_agent.execute(draft)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refinement Error: {str(e)}")

    try:
        validation = validator_agent.execute(topic=request.topic, article=refined_article)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation Error: {str(e)}")

    return {
        "draft_article": draft,
        "refined_article": refined_article,
        "validation": validation
    }

# ------------------- Sanitization Endpoint -------------------

@app.post("/sanitize/")
async def sanitize_medical_data(request: SanitizationRequest):
    """API for sanitizing medical data (PHI removal)."""
    main_agent = agent_manager.get_agent("sanitize_data")
    validator_agent = agent_manager.get_agent("sanitize_data_validator")

    main_agent.llm_provider = request.llm_provider.lower()
    validator_agent.llm_provider = request.llm_provider.lower()

    try:
        sanitized_data = main_agent.execute(request.medical_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sanitization Error: {str(e)}")

    try:
        validation = validator_agent.execute(original_data=request.medical_data, sanitized_data=sanitized_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation Error: {str(e)}")

    return {
        "sanitized_data": sanitized_data,
        "validation": validation
    }

# ------------------- Run the API -------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
