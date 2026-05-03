from fastapi import FastAPI
from app.models.schemas import Analysis, Decision
from app.agent.agent import run_agent

app = FastAPI()


@app.get("/")
def root():
    return {"message": "AI System Manager Agent is running"}


@app.post("/decide", response_model=Decision)
def decide(analysis: Analysis):
    print("\n===== NEW REQUEST =====")
    print("RAW REQUEST:", analysis)

    try:
        analysis_dict = analysis.model_dump()

        # Direct structured output
        result = run_agent(analysis_dict)

        print("FINAL RESULT:", result)

        # FINAL SAFETY GUARD (still keep this)
        if result["action"] == "KILL_PROCESS":
            proc = result.get("target_process")

            if proc and proc["name"] in ["systemd", "bash", "python", "gnome-shell"]:
                return {
                    "action": "REVIEW",
                    "target_process": proc,
                    "reason": ["Blocked unsafe process termination"]
                }

        return result

    except Exception as e:
        print("🔥 SERVER ERROR:", str(e))

        return {
            "action": "NONE",
            "target_process": None,
            "reason": [f"Agent execution failed: {str(e)}"]
        }