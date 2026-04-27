from pydantic import BaseModel #BaseModel from pydantic is used to define structured data models
from typing import List, Optional, Dict #List for array(like alerts), Optional(Field can be null)


class Process(BaseModel): #Defines a process object
    pid: int #Process ID
    name: str #Process Name
    cpu_percent: float #CPU usage percentage


class Analysis(BaseModel): #Object for analysis. This is the output of the analysis module in my cpu manager project which will be passed as input to my agent
    status: str #Status of the system: NORMAL,HIGH_CPU,HIGH_MEMORY
    alerts: List[str] #List of warnings
    high_cpu_process: Optional[Process] = None #Can be a process or none. A process which has high usage of CPU


class Decision(BaseModel): #An object according to the format that Decision module of my module takes as input. Output produced by agent is used as input for decision module
    action: str #Action to be takes: NONE,REVIEW,WARN,KILL_PROCESS
    target_process: Optional[Process] = None #Which process to act upon
    reason: List[str] #Reasin for action(Important for AI)