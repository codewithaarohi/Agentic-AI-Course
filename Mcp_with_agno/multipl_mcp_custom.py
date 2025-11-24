import asyncio
import os
from dotenv import load_dotenv

from agno.tools.mcp import MCPTools
from agno.agent import Agent
from agno.models.openai import OpenAIChat

load_dotenv()

async def main():
    openai_key = os.getenv("OPENAI_API_KEY")

    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini", api_key=openai_key),
        tools=[
            MCPTools("python -m mcp_server_calculator"),  
            MCPTools("python -m mcp_wikipedia"),          
            MCPTools("python custom_mcp_server.py"),            
        ],
        description="AI agent that can calculate, search Wikipedia, and use custom math tools.",
        markdown=True
    )

    # Example query using all MCPs
    agent.print_response(
        "Use your custom math MCP to calculate factorial of 6, "
        "then confirm on Wikipedia who introduced factorial notation, "
        "and finally multiply 12 * 7 using the calculator MCP.",
        stream=True
    )

if __name__ == "__main__":
    asyncio.run(main())
