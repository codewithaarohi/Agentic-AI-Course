import asyncio
from agno.tools.mcp import MCPTools

# client.py
import asyncio
import os
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MultiMCPTools

# Load .env
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# Remote MCP server (your VPS math server)
math_server_url = "http://31.97.233.200:8080/mcp"


async def run_agent(message: str):

    multi_mcp_tools = MultiMCPTools(
        commands=[],                                # no local stdio MCPs
        urls=[math_server_url],                     # only remote MCP
        urls_transports=["streamable-http"],
    )

    # Connect to all MCP servers
    await multi_mcp_tools.connect()

    # Create the agent
    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini", api_key=openai_key),
        tools=[multi_mcp_tools],
        description="Agent that can use both local and remote MCP servers.",
        markdown=True,
    )

    # Ask the agent something
    print("\n🤖 Agent Response:\n")
    await agent.aprint_response(message, stream=True)

    # Close connections
    await multi_mcp_tools.close()


if __name__ == "__main__":
    asyncio.run(
        run_agent("Calculate factorial of 6 and also tell me about Python from Wikipedia.")
    )
