import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from src.agents import AgentManager

# Load environment variables
load_dotenv()

# Get environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Log to check if environment variables are loaded properly
if not OPENAI_API_KEY or not GROQ_API_KEY:
    raise ValueError("API keys not found in environment variables.")
                           
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

@app.get("/env")
async def get_env_vars():
    import os
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    }

# ------------------- Summarization Endpoint -------------------

@app.post("/summarize/")
async def summarize_text(request: SummarizationRequest):
    """API for summarizing medical text."""
    main_agent = agent_manager.get_agent("summarize")
    validator_agent = agent_manager.get_agent("summarize_validator")

    main_agent.llm_provider = request.llm_provider.lower()
    validator_agent.llm_provider = request.llm_provider.lower()

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# import os
# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from src.agents import AgentManager

# # Load environment variables (if any)
# load_dotenv()

# # Initialize FastAPI app
# app = FastAPI(title="Multi-Agent AI System API", version="1.5")

# # ------------------- Request Models -------------------

# class APIKeyRequest(BaseModel):
#     openai_api_key: str
#     groq_api_key: str

# class SummarizationRequest(BaseModel):
#     text: str
#     llm_provider: str

# class WritingRequest(BaseModel):
#     topic: str
#     outline: str = None
#     llm_provider: str

# class SanitizationRequest(BaseModel):
#     medical_data: str
#     llm_provider: str

# # ------------------- API Key Management -------------------

# @app.post("/set_api_keys/")
# async def set_api_keys(request: APIKeyRequest):
#     """Stores OpenAI and Groq API keys securely and returns a success response."""
#     os.environ["OPENAI_API_KEY"] = request.openai_api_key
#     os.environ["GROQ_API_KEY"] = request.groq_api_key

#     return {"message": "✅ API keys have been verified and are ready to use."}

# @app.get("/get_api_keys/")
# async def get_api_keys():
#     """Returns masked versions of stored API keys from environment variables."""
#     def mask_key(key):
#         return key[:3] + "*" * (len(key) - 3) if key else "Not Set"

#     return {
#         "openai_api_key": mask_key(os.getenv("OPENAI_API_KEY", "")),
#         "groq_api_key": mask_key(os.getenv("GROQ_API_KEY", ""))
#     }

# # ------------------- Agent Manager Setup -------------------

# def get_agent_manager():
#     """Ensures API keys are set before allowing agent access."""
#     openai_key = os.getenv("OPENAI_API_KEY")
#     groq_key = os.getenv("GROQ_API_KEY")

#     if not openai_key or not groq_key:
#         raise HTTPException(status_code=401, detail="🚫 API keys not set. Use /set_api_keys/ first.")

#     return AgentManager(max_retries=3, verbose=True)

# # ------------------- AI Processing Endpoints -------------------

# @app.post("/summarize/")
# async def summarize_text(request: SummarizationRequest, agent_manager=Depends(get_agent_manager)):
#     """API for summarizing medical text."""
#     main_agent = agent_manager.get_agent("summarize")
#     validator_agent = agent_manager.get_agent("summarize_validator")

#     main_agent.llm_provider = request.llm_provider.lower()
#     validator_agent.llm_provider = request.llm_provider.lower()

#     try:
#         summary = main_agent.execute(request.text)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Summarization Error: {str(e)}")

#     try:
#         validation = validator_agent.execute(original_text=request.text, summary=summary)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Validation Error: {str(e)}")

#     return {"summary": summary, "validation": validation}

# # ------------------- Summarization Endpoint -------------------

# @app.post("/summarize/")
# async def summarize_text(request: SummarizationRequest, agent_manager=Depends(get_agent_manager)):
#     """API for summarizing medical text."""
#     main_agent = agent_manager.get_agent("summarize")
#     validator_agent = agent_manager.get_agent("summarize_validator")

#     main_agent.llm_provider = request.llm_provider.lower()
#     validator_agent.llm_provider = request.llm_provider.lower()

#     try:
#         summary = main_agent.execute(request.text)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Summarization Error: {str(e)}")

#     try:
#         validation = validator_agent.execute(original_text=request.text, summary=summary)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Validation Error: {str(e)}")

#     return {
#         "summary": summary,
#         "validation": validation
#     }

# # ------------------- Writing & Refining Endpoint -------------------

# @app.post("/write_and_refine/")
# async def write_and_refine_article(request: WritingRequest, agent_manager=Depends(get_agent_manager)):
#     """API for writing and refining research articles."""
#     writer_agent = agent_manager.get_agent("write_article")
#     refiner_agent = agent_manager.get_agent("refiner")
#     validator_agent = agent_manager.get_agent("validator")

#     writer_agent.llm_provider = request.llm_provider.lower()
#     refiner_agent.llm_provider = request.llm_provider.lower()
#     validator_agent.llm_provider = request.llm_provider.lower()

#     try:
#         draft = writer_agent.execute(request.topic, request.outline)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Writing Error: {str(e)}")

#     try:
#         refined_article = refiner_agent.execute(draft)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Refinement Error: {str(e)}")

#     try:
#         validation = validator_agent.execute(topic=request.topic, article=refined_article)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Validation Error: {str(e)}")

#     return {
#         "draft_article": draft,
#         "refined_article": refined_article,
#         "validation": validation
#     }

# # ------------------- Sanitization Endpoint -------------------

# @app.post("/sanitize/")
# async def sanitize_medical_data(request: SanitizationRequest, agent_manager=Depends(get_agent_manager)):
#     """API for sanitizing medical data (PHI removal)."""
#     main_agent = agent_manager.get_agent("sanitize_data")
#     validator_agent = agent_manager.get_agent("sanitize_data_validator")

#     main_agent.llm_provider = request.llm_provider.lower()
#     validator_agent.llm_provider = request.llm_provider.lower()

#     try:
#         sanitized_data = main_agent.execute(request.medical_data)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Sanitization Error: {str(e)}")

#     try:
#         validation = validator_agent.execute(original_data=request.medical_data, sanitized_data=sanitized_data)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Validation Error: {str(e)}")

#     return {
#         "sanitized_data": sanitized_data,
#         "validation": validation
#     }

# # ------------------- Run the API -------------------

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
