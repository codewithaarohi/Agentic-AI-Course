from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import re

load_dotenv()


llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# from langchain_ollama.llms import OllamaLLM
# # Initialize LLM
# llm = LLM(
    # model="ollama/llama3.2",
    # base_url="http://localhost:11434"
# )


# Head to https://ai.google.dev/gemini-api/docs/api-key to generate a Google AI API key. 

#from langchain_google_genai import GoogleGenerativeAI
# Initialize LLM
#llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=os.environ["GOOGLE_API_KEY"])




memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


application_info = {
    "name": None,
    "email": None,
    "skills": None
}




def extract_application_info(text: str) -> str: 
    name_match = re.search(r"(?:my name is|i am)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", text, re.IGNORECASE) 
    email_match = re.search(r"\b[\w.-]+@[\w.-]+\.\w+\b", text)  
    skills_match = re.search(r"(?:skills are|i know|i can use)\s+(.+)", text, re.IGNORECASE) 

    response = [] 

    if name_match: 
        application_info["name"] = name_match.group(1).title()
        response.append("✅ Name saved.") 


    if email_match:
        application_info["email"] = email_match.group(0)
        response.append("✅ Email saved.")
    if skills_match:
        application_info["skills"] = skills_match.group(1).strip()
        response.append("✅ Skills saved.")

    if not any([name_match, email_match, skills_match]):
        return "❓ I couldn't extract any info. Could you please provide your name, email, or skills?"

    return " ".join(response) + " Let me check what else I need."



def check_application_goal(_: str) -> str:
    if all(application_info.values()):
        return f"✅ You're ready! Name: {application_info['name']}, Email: {application_info['email']}, Skills: {application_info['skills']}."
    else:
        missing = [k for k, v in application_info.items() if not v]
        return f"⏳ Still need: {', '.join(missing)}. Please ask the user to provide this."




tools = [
    Tool(
        name="extract_application_info",
        func=extract_application_info,
        description="Use this to extract name, email, and skills from the user's message."
    ),
    Tool(
        name="check_application_goal",
        func=check_application_goal,
        description="Check if name, email, and skills are provided. If not, tell the user what is missing.",
        return_direct=True  # ⬅️ Important!
    )

]


SYSTEM_PROMPT = """You are a helpful job application assistant. 
Your goal is to collect the user's name, email, and skills. 
Use the tools provided to extract this information and check whether all required data is collected.
Once everything is collected, inform the user that the application info is complete and stop.
"""


agent = initialize_agent(
    tools=tools,
    llm=llm,
    memory=memory,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"system_message": SYSTEM_PROMPT}
)


print("📝 Hi! I'm your job application assistant. Please tell me your name, email, and skills.")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Bye! Good luck.")
        break

    response = agent.invoke({"input": user_input})
    print("Bot:", response["output"])

    # If goal achieved, stop
    if "you're ready" in response["output"].lower():
        print("🎉 Application info complete!")
        break
