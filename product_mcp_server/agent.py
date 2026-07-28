import asyncio
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
