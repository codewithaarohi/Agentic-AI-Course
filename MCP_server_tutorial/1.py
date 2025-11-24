
import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()


async def main():
    # Get keys from environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    owm_key = os.getenv("OWM_API_KEY")

    if not openai_key:
        raise ValueError("OPENAI_API_KEY not found in .env or environment variables.")
    if not owm_key:
        raise ValueError("OWM_API_KEY not found in .env or environment variables.")


    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "stdio",
                "command": "E:/langraph_mcp-demo/mcp-openweather/mcp-weather.exe",
                "args": [],
                "env": {"OWM_API_KEY": owm_key}  
            },
            "calculator": {
                "transport": "stdio",
                "command": "python",
                "args": ["-m", "mcp_server_calculator"]
            }
            
        }
    )
    
    tools = await client.get_tools()  
    
    model = ChatOpenAI(model="gpt-4o-mini", api_key=openai_key)    
    

    def call_model(state: MessagesState):
        response = model.bind_tools(tools).invoke(state["messages"])
        return {"messages": response}
        
        
    # Building the LangGraph workflow 
    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools", ToolNode(tools))
    
    builder.add_edge(START, "call_model")
    
    builder.add_conditional_edges("call_model", tools_condition)
    builder.add_edge("tools", "call_model")
    
    # building the graph
    graph = builder.compile()

    print("\n--- Weather Query ---")
    
    while True:
        user_question = input("\nAsk me anything (weather or calculation) → ")
        if user_question.strip().lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        print("\n--- Agent is thinking... ---")
        result = await graph.ainvoke({"messages": user_question})
        print("\n--- Answer ---")
        print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())  