from app.agent.tools import check_safe_process, get_system_thresholds


def run_agent(analysis: dict):
    # Structured deterministic agent: Input → Tools → Logic → JSON output

    status = analysis.get("status")
    alerts = analysis.get("alerts", [])
    process = analysis.get("high_cpu_process")

    # Default response
    result = {
        "action": "NONE",
        "target_process": None,
        "reason": []
    }

    # If no process → nothing to do
    if not process:
        result["reason"] = ["No high CPU process detected"]
        return result

    process_name = process.get("name")
    cpu_usage = process.get("cpu_percent")

    # TOOL 1 → Safety check
    safety = check_safe_process(process_name)

    # TOOL 2 → Thresholds
    thresholds = get_system_thresholds()
    cpu_limit = thresholds["PROC_CPU_LIMIT"]

    # DECISION LOGIC

    # HIGH CPU case
    if status == "HIGH_CPU":

        # If process exceeds threshold
        if cpu_usage > cpu_limit:

            # Safe → kill
            if safety["safe"]:
                result["action"] = "KILL_PROCESS"
                result["target_process"] = process
                result["reason"] = [
                    f"{process_name} exceeds CPU limit ({cpu_usage}% > {cpu_limit}%)",
                    "Process is safe to terminate"
                ]
                return result

            # Unsafe → review
            else:
                result["action"] = "REVIEW"
                result["target_process"] = process
                result["reason"] = [
                    f"{process_name} exceeds CPU limit",
                    "Process is NOT safe to terminate"
                ]
                return result

        # Below threshold → ignore
        else:
            result["action"] = "NONE"
            result["reason"] = [
                f"{process_name} CPU usage ({cpu_usage}%) is within limit ({cpu_limit}%)"
            ]
            return result

    # NORMAL state
    if status == "NORMAL":
        result["action"] = "NONE"
        result["reason"] = ["System operating normally"]
        return result

    # Fallback
    result["action"] = "REVIEW"
    result["reason"] = ["Unhandled system state"]
    return result