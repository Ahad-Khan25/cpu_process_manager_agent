from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from app.agent.tools import tools
from app.agent.prompt import prompt
import os
from dotenv import load_dotenv

load_dotenv()

def create_agent():
    """
    Initializes the LLM and creates a ReAct-based agent with tools.
    """
    raw_key = os.getenv("OPENROUTER_API_KEY")
    if not raw_key:
        raise ValueError("OPENROUTER_API_KEY not found!")

    api_key = raw_key.strip().replace('"', '').replace("'", "").replace('\r', '')

    llm = ChatOpenAI( #Connects to OpenRouter
        model="mistralai/mistral-7b-instruct", #Uses mistral model
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers = { #OpenRouter requires specific headers like a Referer for security and routing which the standard OpenAI library used by LangChain doesn't include by default
            "HTTP-Referer": "http://localhost", #The "Referer" Header: OpenRouter uses this to rank apps and prevent bot abuse. For some models, if this header is missing, their firewall returns a generic 401 User not found instead of a "Missing Header" error.
            "X-Title": "CPU-Process-Manager-Agent", #The Model ID: While openrouter/mistral-7b-instruct sometimes works, mistralai/mistral-7b-instruct is the canonical ID that ensures your request is routed to the correct compute provider.
        },
        temperature = 0,  # temperature=0->deterministic decisions(important for OS systems)
    )

    # Create ReAct agent (reasoning + tool usage)
    agent = create_react_agent( #This enables: Thought → Action → Observation → Final Answer
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    # Wrap agent in executor
    agent_executor = AgentExecutor( #Handles tools execution, loop control, logging because verbose=true
        agent=agent,
        tools=tools,
        verbose=True
    )

    return agent_executor


def run_agent(agent_executor, analysis):
    """
    Runs the agent on system analysis input.
    """

    # Convert analysis to string for prompt injection
    response = agent_executor.invoke({ #Sends system state into the agent
        "analysis": str(analysis)
    })

    # Extract final output from agent response
    return response.get("output", "")