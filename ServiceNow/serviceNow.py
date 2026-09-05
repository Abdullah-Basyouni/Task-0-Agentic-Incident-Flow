import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# ServiceNow configuration
SERVICENOW_URL = os.getenv("SERVICENOW_URL")
S_USERNAME = os.getenv("SERVICENOW_USERNAME")
S_PASSWORD = os.getenv("SERVICENOW_PASSWORD")


def update_incident(sys_id, result):

    # Check the decision
    if result.decision == "respond":

        data = {
            "work_notes": result.response,
            "state": "6",
            "close_notes": result.response,
            "close_code": "Solved (Permanently)"
        }

    elif result.decision == "ask":

        data = {
            "comments": result.response
        }

    elif result.decision == "escalate":

        data = {
            "work_notes": result.response
        }

    else:
        raise ValueError(
            f"Invalid decision: {result.decision}"
        )

    # ServiceNow incident endpoint
    url = (
        f"{SERVICENOW_URL}"
        f"/api/now/table/incident/{sys_id}"
    )

    response = requests.patch(
        url,
        auth=(S_USERNAME, S_PASSWORD),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        json=data,
        timeout=30
    )

    response.raise_for_status()

    return response.json()