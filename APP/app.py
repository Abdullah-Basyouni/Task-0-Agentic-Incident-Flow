from fastapi import FastAPI
from Agent.agent import agentDecision
from ServiceNow.serviceNow import update_incident
from Model.data import Incident
import json

# Load Knowledge Base
with open("kb_articles.json", "r", encoding="utf-8") as file:
    knowledge = json.load(file)

app = FastAPI()

# Store processed incidents to prevent duplicate processing
processed_incidents = set()


@app.post("/webhook")
def handleTicket(incident: Incident):

    # Idempotency / Duplicate Check
    if incident.incident_sys_id in processed_incidents:
        print("====================")
        print("DUPLICATE INCIDENT")
        print("INCIDENT:", incident.incident_sys_id)
        print("====================")

        return {
            "Message": "Incident already processed",
            "incident_sys_id": incident.incident_sys_id
        }

    # Analyze the incident
    result = agentDecision(knowledge, incident)

    print("====================")
    print("INCIDENT:", incident.number)
    print("DECISION:", result.decision)
    print("RESPONSE:", result.response)
    print("====================")

    # Update ServiceNow
    update_incident(incident.incident_sys_id, result)

    # Mark as processed only after successful ServiceNow update
    processed_incidents.add(incident.incident_sys_id)

    return {
        "Message": result
    }