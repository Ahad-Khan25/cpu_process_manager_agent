# 🧠 CPU Process Manager Agent

An intelligent, modular system management agent designed to monitor system health, analyze resource usage, and make safe, structured decisions about process-level actions in a Linux environment.

The system is built with a clean separation of concerns across monitoring, analysis, decision-making (agent), execution, and logging — making it both production-friendly and easily extensible.

---

## 🚀 Overview

This project simulates a lightweight AI-driven system administrator that can:

- Detect abnormal system behavior (CPU spikes, high memory usage)
- Identify resource-heavy processes
- Evaluate process safety before taking action
- Generate structured decisions (JSON-based)
- Execute safe system-level operations via a dedicated executor module
- Log and track system decisions

---

## 🏗️ System Architecture
Monitor → Analyzer → Agent → Executor → Logger


### 🔄 Workflow

1. **Monitor**
   - Collects raw system metrics (CPU, memory, processes)

2. **Analyzer**
   - Detects anomalies (e.g., HIGH_CPU, HIGH_MEMORY)

3. **Agent**
   - Applies structured decision logic
   - Evaluates process safety
   - Produces a JSON decision

4. **Executor**
   - Executes system actions (kill, review, warn, ignore)
   - Enforces safety checks before performing operations

5. **Logger**
   - Records all decisions and actions for audit/debugging

---

## 📦 Tech Stack

- Python 3.10+
- FastAPI
- Pydantic (data validation)
- psutil (system monitoring)
- Linux OS process control
- Modular service-based architecture

---

## 🌐 API Interface

### 📍 Base URL

http://localhost:8000


---

### 🔹 GET `/`

Health check endpoint.

#### Response:
```json
{
  "message": "AI System Manager Agent is running"
}
```

🔹 POST /decide

Processes system analysis and returns a structured decision.

Request Body
```
{
  "status": "HIGH_CPU",
  "alerts": ["High CPU usage detected in chrome"],
  "high_cpu_process": {
    "pid": 5555,
    "name": "chrome",
    "cpu_percent": 95.0
  }
}
```

Response Format

```
{
  "action": "KILL_PROCESS",
  "target_process": {
    "pid": 5555,
    "name": "chrome",
    "cpu_percent": 95.0
  },
  "reason": [
    "CPU usage exceeds safe threshold",
    "Process is safe to terminate"
  ]
}
```

Decision Types

| Action         | Description                 |
| -------------- | --------------------------- |
| `NONE`         | No action required          |
| `REVIEW`       | Manual/system review needed |
| `WARN`         | Warning condition detected  |
| `KILL_PROCESS` | Safe process termination    |


Safety Mechanisms

This system is designed with strict safety-first principles:

🔒 Protected Processes

These processes will NEVER be terminated:

systemd,
bash,
python,
gnome-shell

📊 Threshold Rules

| Metric            | Limit |
| ----------------- | ----- |
| CPU usage         | 80%   |
| Process CPU usage | 50%   |
| Memory usage      | 75%   |

Safety Enforcement Layers
Agent-level validation (decision filtering)
Executor-level safety checks (final gate before execution)
Structured JSON enforcement

app/
│
├── agent/
│   ├── agent.py        # Core decision engine (rule-based logic)
│   ├── tools.py        # System utility functions
│
├── executor/
│   └── executor.py     # Executes safe system actions
│
├── models/
│   └── schemas.py      # Pydantic data models
│
├── main.py             # FastAPI entry point

⚙️ How It Works
1. System Monitoring

System metrics are collected and passed to the analyzer.

2. Analysis Stage

Detects conditions such as:

HIGH_CPU
NORMAL
HIGH_MEMORY
3. Agent Decision Engine

The agent:

Evaluates system status
Checks process safety
Compares against thresholds
Produces structured JSON output
4. Execution Layer

The executor:

Receives structured decision
Validates safety rules
Executes OS-level actions (if allowed)
5. Logging Layer

All actions are logged for debugging and auditing.


Future Improvements

This system is designed to be extended into a full AI-powered infrastructure manager:

🔮 Planned Upgrades
🤖 LLM-based reasoning layer (hybrid AI agent)
📊 Adaptive thresholds based on system behavior history
⚡ Real-time streaming decision engine
🧠 Anomaly detection using ML models
🌍 Distributed agent architecture (multi-node systems)
🔁 Auto-recovery and process restart mechanisms


Important Notes
Requires Linux environment for full functionality
Process termination requires elevated permissions
Designed for controlled system environments (not production-critical servers without safeguards)


Author

A modular AI-driven system management agent designed to explore intelligent automation in operating systems, combining rule-based AI with structured decision-making principles.