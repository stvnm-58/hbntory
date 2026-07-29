from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_agent

app = FastAPI(title="HBntory Chat API")

# Configuration du middleware CORS (Cross-Origin Resource Sharing)
# Permet au front-end d'interagir avec l'API depuis n'importe quelle origine ("*")
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
    """
    Endpoint HTTP POST recevant une question, la transmettant à un agent IA,
    puis retournant sa réponse sous forme structurée.

    Args:
        payload (ChatRequest): Contient le corps de la requête JSON validé par Pydantic, 
                               avec le champ `question`.

    Raises:
        HTTPException (400 Bad Request): Si la question soumise est vide ou ne contient que des espaces.
        HTTPException (500 Internal Server Error): Si l'exécution de l'agent rencontre un échec inattendu.

    Returns:
        ChatResponse: Objet contenant la réponse textuelle générée par l'agent.
    """
    # Validation du contenu : Vérification que la question n'est pas vide ou composée uniquement d'espaces
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="La question ne peut pas être vide.")
    
    try:
        # Appelle de manière asynchrone la fonction d'exécution de l'agent avec la question nettoyée/validée
        response_text = await run_agent(payload.question)
        return ChatResponse(answer=response_text)
        
    except Exception as e:
        # EXCEPT (Erreur Globale/Système) :
        # Interrompt l'exécution et renvoie un statut 500 Internal Server Error contenant le détail du problème.
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement par l'agent : {str(e)}")