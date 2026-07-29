import asyncio
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

async def run_agent(user_query: str):
    """
    Exécute un agent ReAct (LangGraph + Ollama) capable d'utiliser les outils 
    exposés par un serveur MCP (Model Context Protocol) via STDIO.

    Args:
        user_query (str): La requête ou question posée par l'utilisateur.

    Returns:
        str: Le contenu textuel du dernier message généré par l'agent (la réponse finale).
        
    Note (Gestion des exceptions) :
        Cette fonction ne contient pas de bloc `try...except` explicite. En cas d'erreur
        (ex: serveur MCP introuvable, échec d'initialisation Ollama, délai dépassé),
        l'exception est directement levée et propagée vers l'appelant (comme l'API FastAPI).
    """
    server_params = StdioServerParameters(
        command="python3",
        args=["server.py"]
    )

    # 2. Connexion STDIO & Ouverture de session MCP
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Chargement des outils du serveur MCP
            tools = await load_mcp_tools(session)

            # 3. Initialisation du LLM local (Qwen 1.5B)
            llm = ChatOllama(model="qwen2.5:1.5b", temperature=0)

            # 4. Création de l'agent ReAct
            agent = create_react_agent(llm, tools)

            # 5. Exécution de la requête
            response = await agent.ainvoke({
                "messages": [("user", user_query)]
            })

            return response["messages"][-1].content

if __name__ == "__main__":
    test_query = "Donne-moi les détails du produit HB-LAP-1001"
    
    print("🚀 Lancement de l'agent (Qwen 2.5 local)...")
    resultat = asyncio.run(run_agent(test_query))
    
    print("\n🤖 Réponse de l'Agent :\n")
    print(resultat)
