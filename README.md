## Schemas and API Module

This module defines the data structures and API endpoints for the AI Agent service. It acts as the interface between the local system manager and the deployed AI decision engine.

### Schemas

The system uses Pydantic models to enforce structured communication between components:

- **Process**: Represents a system process with PID, name, and CPU usage.
- **Analysis**: Represents the analyzed system state received from the local monitoring system.
- **Decision**: Represents the output of the AI agent, including the recommended action, target process, and reasoning.

These schemas ensure type safety, validation, and consistency in API communication.

### API Endpoints

The FastAPI framework is used to expose the AI agent as a web service.

- **GET /**  
  Health check endpoint to verify that the agent service is running.

- **POST /decide**  
  Accepts system analysis data and returns an AI-generated decision.

### Purpose

This module provides a structured and scalable interface for integrating the AI agent with external systems. It ensures reliable communication and serves as the foundation for deploying the agent as a cloud-based service.

## Agent Core Module

The Agent Core module implements the intelligent decision-making component of the system using LangChain and a large language model.

### Prompt Design

A structured prompt template is used to define the agent’s role, responsibilities, and constraints. The prompt ensures that the agent behaves as a Linux system administrator, prioritizing safety and stability while making decisions.

### Tools Integration

The agent is equipped with tools that allow it to interact with external logic:

- **ProcessSafetyChecker**: Determines whether a process is safe to terminate.
- **SystemThresholds**: Provides system resource thresholds for informed decision-making.

These tools enable the agent to perform reasoning beyond simple text generation.

### Agent Architecture

The system uses a zero-shot ReAct-based agent, which follows a reasoning loop:

1. Thought: Analyze the problem
2. Action: Call a tool if needed
3. Observation: Interpret tool output
4. Final Answer: Generate a structured decision

### Model Integration

The agent uses an LLM accessed through OpenRouter, allowing flexible model selection and external API-based reasoning.

### Purpose

This module transforms the system from a rule-based engine into an intelligent, adaptive agent capable of reasoning, tool usage, and dynamic decision-making.