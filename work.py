import importlib
from sympy import true
from typer import prompt
import model
from system_prompt import SYSTEM_PROMPT
from pydantic import BaseModel, Field
from enum import Enum 
import json


#---------------------------------------model----------------------------------------------------------------------

model = importlib.reload(model)
llm = model.get_llm()

#----------------------------------structured output ---------------------------------------------------------------
class WaterLevelStatus(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    FULL = "FULL"
    UNKNOWN = "UNKNOWN"


class PumpAction(str, Enum):
    START_PUMP = "START_PUMP"
    CONTINUE_PUMPING = "CONTINUE_PUMPING"
    STOP_PUMP = "STOP_PUMP"
    KEEP_OFF = "KEEP_OFF"
    INSPECT_SYSTEM = "INSPECT_SYSTEM"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AquaSenseDecision(BaseModel):
    water_level_status: WaterLevelStatus
    recommended_action: PumpAction
    risk_level: RiskLevel
    anomaly_detected: bool
    anomaly_details: list[str] = Field(default_factory=list)
    reasoning: str
    alert_message: str
    next_step: str

structured_llm = llm.with_structured_output(AquaSenseDecision)
#-------------------------------------------------------sample json input ---------------------------------------------------------------
sensor_data = {
  "water_level_percent": 15,
  "pump_status": "OFF",
  "source_water_available": true,
  "sensor_status": "NORMAL",
  "pump_temperature_celsius": 32.5,
  "pump_runtime_minutes": 0,
  "previous_water_level_percent": 25
}
#-------------------------------------------------invoke with sysytem prompt and get response --------------------------------------------------------------
decision = structured_llm.invoke([
    ("system", SYSTEM_PROMPT),
    ("human", json.dumps(sensor_data))
])
print(decision.model_dump_json(indent=2))
