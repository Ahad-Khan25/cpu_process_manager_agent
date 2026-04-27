# AGENT CORE
from langchain_openai import ChatOpenAI #LLM interface
from langchain.agents import initialize_agent #Creates agent with tools
from langchain.agents import AgentType #Defines agent behavior
from app.agent.tools import tools #Loads tools
from app.agent.prompt import prompt #Loads prompt
import os #Used to get API key from .env file


def create_agent(): #Factory Function
    llm = ChatOpenAI( #Creates LLM
        model="openrouter/mistral-7b-instruct", #Using OpenRouter model
        openai_api_key=os.getenv("OPENROUTER_API_KEY"), #Reads key from .env
        openai_api_base="https://openrouter.ai/api/v1", #Connects to OpenRouter
        default_headers={ #Required for OpenRouter
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI System Manager"
        }
    )

    agent = initialize_agent( #Builds actual agent
        tools=tools, #Gives capabilities
        llm=llm, #Gives brain
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, #Enables: Thought->Action->Observation->Final Answer
        verbose=True #Prints reasoning (great for debugging)
    )

    return agent


def run_agent(agent, analysis): #Executes agent
    """
    Runs the agent with system analysis input.
    """

    input_text = prompt.format(analysis=analysis) #Injects system data into prompt

    response = agent.run(input_text) #Agent thinks+uses tools

    return response #Returns raw LLM output