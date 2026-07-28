from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama
from langchain.agents import create_agent # ou la fonction que tu utilises dans agent.py

# 1. Initialisation de l'API FastAPI
app = FastAPI(title="HBntory Agent API")

# 2. Activation du CORS (pour que le Front-end puisse requêter sans blocage de navigateur)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En dev, on autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Structure de la requête envoyée par le Front
class PromptRequest(BaseModel):
    message: str

# 4. Route HTTP POST /api/chat
@app.post("/api/chat")
async def chat_with_agent(req: PromptRequest):
    """Reçoit la question du Front, interroge le serveur MCP + LLM, et renvoie la réponse."""
    
    server_params = StdioServerParameters(
        command="python3",
        args=["server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Charger les outils MCP
            tools = await load_mcp_tools(session)
            
            # Initialiser le modèle Ollama local
            llm = ChatOllama(model="qwen2.5:latest")
            
            # Créer l'agent
            agent = create_agent(llm, tools)
            
            # Exécuter la demande reçue du Front-end
            response = await agent.ainvoke({
                "messages": [("user", req.message)]
            })
            
            # Extraire le message final de l'agent
            final_answer = response["messages"][-1].content
            
            return {"response": final_answer}
