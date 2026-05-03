def check_safe_process(process_name: str) -> dict:
    """
    Returns structured safety info
    """
    unsafe = ["systemd", "bash", "python", "gnome-shell"]

    if process_name in unsafe:
        return {
            "safe": False,
            "reason": "Critical system process"
        }
    else:
        return {
            "safe": True,
            "reason": "User-level process"
        }


def get_system_thresholds() -> dict:
    """
    Returns structured thresholds
    """
    return {
        "CPU_LIMIT": 80,
        "MEM_LIMIT": 75,
        "PROC_CPU_LIMIT": 50
    }