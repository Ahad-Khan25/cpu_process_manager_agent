from app.agent.tools import check_safe_process, get_system_thresholds


def run_agent(analysis: dict):
    """
    Structured deterministic agent:
    Input → Tools → Logic → JSON output
    """

    # 🔹 Extract inputs safely
    status = analysis.get("status", "UNKNOWN")
    alerts = analysis.get("alerts", [])
    process = analysis.get("high_cpu_process")

    # 🔹 Default response
    result = {
        "action": "NONE",
        "target_process": None,
        "reason": [],
        "confidence": 0.5  # optional but useful
    }

    # 🔹 Get thresholds
    thresholds = get_system_thresholds()
    cpu_limit = thresholds.get("PROC_CPU_LIMIT", 50)

    # 🔹 If no process available
    if not process:
        if status == "HIGH_MEMORY":
            result["action"] = "WARN"
            result["reason"] = ["High memory usage detected"]
            result["confidence"] = 0.8
            return result

        result["reason"] = ["No high CPU process detected"]
        result["confidence"] = 0.9
        return result

    # 🔹 Extract process info safely
    process_name = process.get("name", "unknown")
    cpu_usage = process.get("cpu_percent", 0)

    # 🔹 TOOL 1 → Safety check
    safety = check_safe_process(process_name)
    is_safe = safety.get("safe", False)

    # =========================================================
    # 🔥 CORE DECISION LOGIC
    # =========================================================

    # ---------------------------------------------------------
    # 🔴 CASE 1: HIGH CPU SYSTEM
    # ---------------------------------------------------------
    if status == "HIGH_CPU":

        if cpu_usage > cpu_limit:

            if is_safe:
                return {
                    "action": "KILL_PROCESS",
                    "target_process": process,
                    "reason": [
                        f"{process_name} exceeds CPU limit ({cpu_usage}% > {cpu_limit}%)",
                        "System CPU is high",
                        "Process is safe to terminate"
                    ],
                    "confidence": 0.95
                }

            else:
                return {
                    "action": "REVIEW",
                    "target_process": process,
                    "reason": [
                        f"{process_name} exceeds CPU limit",
                        "System CPU is high",
                        "Process is NOT safe to terminate"
                    ],
                    "confidence": 0.85
                }

        else:
            return {
                "action": "NONE",
                "target_process": None,
                "reason": [
                    f"{process_name} CPU usage ({cpu_usage}%) is within limit",
                    "No critical action needed"
                ],
                "confidence": 0.9
            }

    # ---------------------------------------------------------
    # 🟠 CASE 2: HIGH MEMORY SYSTEM
    # ---------------------------------------------------------
    if status == "HIGH_MEMORY":

        # If heavy process also exists → optional action
        if cpu_usage > cpu_limit:

            if is_safe:
                return {
                    "action": "KILL_PROCESS",
                    "target_process": process,
                    "reason": [
                        "Memory usage is high",
                        f"{process_name} is also CPU heavy",
                        "Process is safe to terminate"
                    ],
                    "confidence": 0.85
                }

            else:
                return {
                    "action": "REVIEW",
                    "target_process": process,
                    "reason": [
                        "Memory usage is high",
                        f"{process_name} is heavy but unsafe to kill"
                    ],
                    "confidence": 0.75
                }

        # No strong process candidate → warn only
        return {
            "action": "WARN",
            "target_process": None,
            "reason": [
                "High memory usage detected",
                "No safe process identified for termination"
            ],
            "confidence": 0.8
        }

    # ---------------------------------------------------------
    # 🟢 CASE 3: NORMAL SYSTEM (IMPORTANT FIX)
    # ---------------------------------------------------------
    if status == "NORMAL":

        # 🔥 NEW: Process-level decision even in NORMAL state
        if cpu_usage > cpu_limit:

            if is_safe:
                return {
                    "action": "KILL_PROCESS",
                    "target_process": process,
                    "reason": [
                        f"{process_name} exceeds CPU limit ({cpu_usage}% > {cpu_limit}%)",
                        "Process-level optimization"
                    ],
                    "confidence": 0.8
                }

            else:
                return {
                    "action": "REVIEW",
                    "target_process": process,
                    "reason": [
                        f"{process_name} is heavy but unsafe to kill"
                    ],
                    "confidence": 0.7
                }

        return {
            "action": "NONE",
            "target_process": None,
            "reason": ["System operating normally"],
            "confidence": 0.95
        }

    # ---------------------------------------------------------
    # ⚠️ FALLBACK
    # ---------------------------------------------------------
    return {
        "action": "REVIEW",
        "target_process": process,
        "reason": ["Unhandled system state"],
        "confidence": 0.6
    }