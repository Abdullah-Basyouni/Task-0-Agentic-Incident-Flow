from fastapi import FastAPI
from Agent.agent import agentDecision
from ServiceNow.serviceNow import update_incident
from Model.data import Incident
import json

with open("kb_articles.json", "r", encoding="utf-8") as file:
    knowledge = json.load(file)

app = FastAPI()

@app.post("/webhook")
def handleTicket(incident: Incident):

    result = agentDecision(knowledge, incident)

    print("====================")
    print("DECISION:", result.decision)
    print("RESPONSE:", result.response)
    print("====================")

    update_incident(incident.incident_sys_id, result)

    return {"Message": result}