# !pip install -U agno
# !pip install python-dotenv

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = api_key


from agno.agent import Agent
from agno.models.openai import OpenAIChat
agno_agent = Agent(
    model=OpenAIChat(id="gpt-3.5-turbo"),  #"gpt-4o-mini"
    description="Agno Q&A agent",
    markdown=False
)

agno_agent.print_response("What is the capital of India?", stream=True)
