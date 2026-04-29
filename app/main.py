from fastapi import FastAPI #Web framework from FastAPI
from app.models.schemas import Analysis, Decision #Import schemas. Ensures input is structured(Analysis) and Output is validated(Decision)
from app.agent.agent import create_agent, run_agent #Import Agent Functions. Brings the AI brain into API layer
import json #JSON handling. Used to safely parse LLM output

app = FastAPI() #Create App. Starts server instance

# Initialize agent ONCE (important for performance)
agent = create_agent() #Agent is created once. Not recreated per request. Saves latency+cost


@app.get("/") #Root endpoint. Health check route
def root():
    return {"message": "AI System Manager Agent is running"} #Confirms system is live


@app.post("/decide", response_model=Decision) #Main decision endpoint
def decide(analysis: Analysis): #Function input. Automatically validates incoming JSON using schema
    """
    Main endpoint:
    Receives system state → sends to AI agent → returns decision
    """

    # Convert Pydantic model → dict → string
    analysis_dict = analysis.model_dump()

    # Run agent
    response = run_agent(agent, analysis_dict) #This triggers: Prompt->LLM->Tools->Reasoning->Output

    # Try to enforce JSON output safety
    try:
        result = json.loads(response) #Converts string->JSON
    except Exception as e: #Fallback Safety
        result = {
            "action": "NONE",
            "target_process": None,
            "reason": [f"Parsing error: {str(e)}"]
        }

    return result #Sends decision back to linux system