#Tools(Agent Capabilities)
from langchain_core.tools import Tool #Tool abstraction in LangChain, Lets agent call functions


def check_safe_process(process_name: str) -> str: #Function agent can call
    """
    Checks whether a process is safe to terminate.
    """
    unsafe = ["systemd", "bash", "python", "gnome-shell"] #List of protected processes

    if process_name in unsafe: #Safety logic
        return f"{process_name} is NOT safe to terminate" #Returns natural language(important for LLM)
    else:
        return f"{process_name} is safe to terminate"


def get_system_thresholds() -> str: #Gives system limits. Limit for cpu usage, memory usage
    """
    Returns system thresholds.
    """
    return "CPU threshold: 80%, Memory threshold: 75%, Process CPU threshold: 50%"


tools = [ #List of tools available to agent
    Tool(
        name="ProcessSafetyChecker", #Tool name(used by agent)
        func=check_safe_process, #Function to execute
        description="Check if a process is safe to terminate" #Very important->helps agent decide when to use tool
    ),
    Tool(
        name="SystemThresholds",
        func=get_system_thresholds,
        description="Get system thresholds for CPU and memory"
    )
]