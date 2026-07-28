import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

async def run_agent(user_query: str):
    # 1. Indiquer comment lancer le serveur MCP (situé au même endroit)
    server_params = {
        "command": "python3",
        "args": ["server.py"],
        "transport": "stdio"
    }

    # 2. Charger l'outil get_external_product depuis server.py
    tools = await load_mcp_tools(server_params)

    # 3. Initialiser LLM (OpenAI)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # 4. Prompt de base pour l'agent
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un assistant IA d'inventaire. Utilise tes outils pour chercher des produits."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 5. Assembler l'agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # 6. Exécuter la requête
    response = await agent_executor.ainvoke({"input": user_query})
    return response["output"]

# Bloc pour tester le fichier directement dans le terminal
if __name__ == "__main__":
    test_query = "Donne-moi les détails du produit HB-LAP-1001"
    
    print("🚀 Lancement de l'agent...")
    resultat = asyncio.run(run_agent(test_query))
    
    print("\n🤖 Réponse de l'Agent :\n")
    print(resultat)
