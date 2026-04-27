from fastapi import FastAPI #FastAPI to wrap our agent into an API for deployment
from app.models.schemas import Analysis, Decision #Connects API with data models

app = FastAPI() #app initializes the web server


@app.get("/") #GET Request
def root(): #Simple health check
    return {"message": "AI Agent is running"}


@app.post("/decide", response_model=Decision) #POST Request. "response_model=Decision" forces output format and validates response.
def decide(analysis: Analysis): #Input automatically validated as analysis
    """
    Temporary placeholder agent logic.
    Will be replaced with LangChain agent.
    """

    # Dummy response (for testing)
    return Decision( #Returns structured output
        action="NONE",
        target_process=None,
        reason=["Agent not initialized yet"]
    )