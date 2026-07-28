from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_agent

app = FastAPI(title="HBntory Chat API")

# Configuration des CORS pour autoriser le Front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="La question ne peut pas être vide.")
    
    try:
        response_text = await run_agent(payload.question)
        return ChatResponse(answer=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement par l'agent : {str(e)}")