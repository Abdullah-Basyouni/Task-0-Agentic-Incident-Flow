from pydantic import BaseModel
from typing import Literal
from typing import Optional


#Incident Model
class Incident(BaseModel):
    incident_sys_id: str
    number: str
    short_description: str
    description: Optional[str] = None
    priority: int
    
    
#Decision Model
class Decision(BaseModel):
    decision : Literal[ "ask" , "respond" , "escalate"]
    response : str
