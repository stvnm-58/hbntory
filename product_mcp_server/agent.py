import asyncio
<<<<<<< HEAD
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

async def run_agent(user_query: str):
    # 1. Configuration du serveur MCP
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
=======
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

async def run_agent(user_query: str):
    # 1. Spécifier la commande pour lancer ton serveur MCP
    server_params = {
        "command": "python3",
        "args": ["server.py"], # Chemin vers ton server.py
        "transport": "stdio"
    }

    # 2. Charger automatiquement les outils exposés par ton MCP (ex: get_external_product)
    tools = await load_mcp_tools(server_params)

    # 3. Initialiser le LLM (ex: GPT-4o, Claude, etc.)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # 4. Définir le prompt de l'Agent
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un assistant virtuel. Utilise les outils à ta disposition pour répondre aux questions sur les produits."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 5. Créer l'agent et son exécuteur
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # 6. Exécuter la requête
    response = await agent_executor.ainvoke({"input": user_query})
    return response["output"]

# Test rapide
if __name__ == "__main__":
    query = "Donne-moi les caractéristiques du produit HB-LAP-1001"
    result = asyncio.run(run_agent(query))
    print("\n🤖 Réponse de l'Agent :\n", result)
>>>>>>> f5f7b3d9f92c744ad012a004e82c915576c27244
