# AI-Powered ServiceNow Incident Decision System

An AI-powered system that analyzes ServiceNow incidents, uses a knowledge base to make decisions, and automatically updates the incident.

---

## Overview

This project integrates **ServiceNow**, **FastAPI**, **LangChain**, and an **LLM** to create an automated incident decision workflow.

When an incident is created in ServiceNow, the system receives the incident data through a webhook endpoint, validates the payload using Pydantic, analyzes the incident using an AI agent and a knowledge base, generates a decision, and sends the result back to ServiceNow.

The system also includes **duplicate webhook handling** to prevent the same incident from being processed multiple times during the application runtime.

### Workflow

```text
ServiceNow
    |
    v
FastAPI Webhook
    |
    v
Duplicate / Idempotency Check
    |
    v
Pydantic Validation
    |
    v
AI Agent
    |
    v
Knowledge Base
    |
    v
Decision
    |
    v
ServiceNow Update
```

---

## Features

* ServiceNow incident integration
* FastAPI REST API
* AI-powered incident analysis
* LangChain-based AI agent
* Knowledge-base-assisted decision making
* Automatic ServiceNow incident updates
* Pydantic request validation
* Duplicate webhook / idempotency handling
* Local development with ngrok
* Environment-based configuration
* Swagger API documentation

---

## Tech Stack

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Main programming language |
| FastAPI    | REST API backend          |
| Pydantic   | Request validation        |
| LangChain  | AI agent orchestration    |
| Gemini LLM | Incident reasoning        |
| ServiceNow | Incident management       |
| JSON       | Knowledge base            |
| ngrok      | Expose local API          |

---

## Project Structure

```text
project/
│
├── APP/
│   └── app.py
│
├── Agent/
│   └── agent.py
│
├── ServiceNow/
│   └── serviceNow.py
│
├── Model/
│   └── data.py
│
├── kb_articles.json
├── requirements.txt
├── .gitignore
├── README.md
└── REFLECTION.md
```

### Components

### `APP/app.py`

Contains the FastAPI application and `/webhook` endpoint.

It is responsible for:

* Receiving incident payloads
* Checking for duplicate incidents
* Calling the AI decision agent
* Updating ServiceNow
* Returning the generated decision

### `Agent/agent.py`

Contains the AI decision logic using LangChain and the configured Gemini LLM.

The agent evaluates the incident against the knowledge base and generates one of three decisions:

```text
ask
respond
escalate
```

### `ServiceNow/serviceNow.py`

Handles communication with the ServiceNow REST API and updates incidents based on the generated decision.

### `Model/data.py`

Contains the Pydantic models used to validate incoming incidents and AI decisions.

### `kb_articles.json`

Contains the local knowledge base used by the AI agent during incident analysis.

---

# Installation

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <PROJECT_FOLDER>
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_GEMINI_API_KEY=your_gemini_api_key
SERVICENOW_URL=https://your-instance.service-now.com
SERVICENOW_USERNAME=your_username
SERVICENOW_PASSWORD=your_password
```

The application uses the following environment variables:

| Variable                | Purpose                 |
| ----------------------- | ----------------------- |
| `GOOGLE_GEMINI_API_KEY` | Gemini LLM API key      |
| `SERVICENOW_URL`        | ServiceNow instance URL |
| `SERVICENOW_USERNAME`   | ServiceNow username     |
| `SERVICENOW_PASSWORD`   | ServiceNow password     |

Do not commit `.env` to GitHub.

Make sure `.gitignore` contains:

```gitignore
.env
.venv/
__pycache__/
```

---

# Knowledge Base

The system uses `kb_articles.json` as its local knowledge base.

Example:

```json
[
  {
    "title": "Printer Not Working",
    "description": "Basic troubleshooting steps for printer issues.",
    "solution": "Check the printer connection, restart the printer, and verify the configured printer."
  }
]
```

The AI agent uses these articles as supporting information when analyzing incidents.

The agent does not invent solutions outside the provided knowledge base when generating a `respond` decision.

---

# Running the API

Start the FastAPI server from the project root:

```bash
uvicorn APP.app:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# Webhook Endpoint

The main endpoint is:

```text
POST /webhook
```

The endpoint accepts an incident payload validated using the `Incident` Pydantic model.

### Request Example

```json
{
  "incident_sys_id": "YOUR_INCIDENT_SYS_ID",
  "number": "INC0010001",
  "short_description": "Printer not printing after office move",
  "description": "The printer was working yesterday. I tried turning it off and on.",
  "priority": 3
}
```

### Incident Model

```text
incident_sys_id  : string
number            : string
short_description : string
description       : string | optional
priority          : integer
```

---

# Decision Logic

The AI agent generates one of three decisions:

```text
ask
respond
escalate
```

### `ask`

Used when the incident is vague or missing important information.

The AI generates a contextual question requesting the missing information.

The question is sent to ServiceNow as a comment.

### `respond`

Used when the incident clearly matches a solution in the knowledge base.

The system:

* Adds the response to work notes
* Adds the response to close notes
* Sets the incident state to `6`
* Sets the close code to `Solved (Permanently)`

### `escalate`

Used when the incident is clear but does not have a suitable knowledge-base solution or requires human intervention.

The system adds the escalation message to the incident work notes.

---

# Duplicate Webhook Handling

The webhook includes an idempotency check using the incident `incident_sys_id`.

Before processing an incident, the system checks whether it has already been processed:

```text
Incoming Webhook
       |
       v
Is incident already processed?
       |
   +---+---+
   |       |
  Yes      No
   |       |
   v       v
 Stop    Process
           |
           v
    Update ServiceNow
           |
           v
    Mark as processed
```

If the same incident is received again during the application runtime, the system returns:

```json
{
  "Message": "Incident already processed",
  "incident_sys_id": "YOUR_INCIDENT_SYS_ID"
}
```

This prevents repeated webhook requests from triggering multiple AI analyses and ServiceNow updates.

> Note: The current implementation stores processed incident IDs in application memory. The set is reset if the FastAPI application is restarted.

---

# Testing the API

The system should be tested using the three required incident scenarios.

For each test, verify the complete flow:

```text
Incident
   |
   v
FastAPI Webhook
   |
   v
AI Decision
   |
   v
ServiceNow Update
```

### Test 1 — Respond

Expected decision:

```text
respond
```

Expected ServiceNow behavior:

```text
Work Notes  → AI response
Close Notes → AI response
State       → 6
Close Code  → Solved (Permanently)
```

### Test 2 — Ask

Expected decision:

```text
ask
```

Expected ServiceNow behavior:

```text
Comments → Clarifying question
```

### Test 3 — Annual Leave Escalation

Expected decision:

```text
escalate
```

Expected ServiceNow behavior:

```text
Work Notes → Escalation message
```

The annual leave scenario should be verified end-to-end to confirm that the incident is correctly routed to human support.

---

# ServiceNow Integration

The application can be connected to a ServiceNow Personal Developer Instance.

The integration allows the system to:

1. Receive incident information.
2. Validate the incoming payload.
3. Analyze the incident using the AI agent.
4. Generate an appropriate decision.
5. Update the corresponding ServiceNow incident.

The ServiceNow integration is handled by:

```text
ServiceNow/serviceNow.py
```

---

# Local Development with ngrok

ServiceNow cannot directly access:

```text
http://localhost:8000
```

because the address is only accessible from the local machine.

Use ngrok to expose the FastAPI application.

Start FastAPI:

```bash
uvicorn APP.app:app --reload
```

Then run:

```bash
ngrok http 8000
```

ngrok will generate a public HTTPS URL similar to:

```text
https://example.ngrok-free.app
```

Use the generated HTTPS URL when configuring the ServiceNow webhook/request.

The final architecture becomes:

```text
ServiceNow
     |
     v
ngrok Public URL
     |
     v
FastAPI localhost:8000
     |
     v
Duplicate Check
     |
     v
AI Agent
     |
     v
Knowledge Base
     |
     v
Decision
     |
     v
ServiceNow Update
```

---

# End-to-End Example

A typical workflow looks like this:

```text
1. Incident is created in ServiceNow
                |
                v
2. ServiceNow sends the incident to FastAPI
                |
                v
3. FastAPI validates the request
                |
                v
4. Duplicate check is performed
                |
                v
5. AI Agent analyzes the incident
                |
                v
6. Knowledge Base is consulted
                |
                v
7. AI generates a decision
                |
                v
8. ServiceNow incident is updated
```

---

# Architecture

```text
                  +------------------+
                  |    ServiceNow    |
                  +--------+---------+
                           |
                           v
                  +------------------+
                  |      ngrok       |
                  +--------+---------+
                           |
                           v
                  +------------------+
                  |     FastAPI      |
                  +--------+---------+
                           |
                           v
                  +------------------+
                  | Duplicate Check  |
                  +--------+---------+
                           |
                           v
                  +------------------+
                  |    AI Agent      |
                  |    LangChain     |
                  +--------+---------+
                           |
               +-----------+-----------+
               |                       |
               v                       v
        +----------------+     +----------------+
        | Knowledge Base |     |      LLM       |
        +----------------+     +----------------+
               |                       |
               +-----------+-----------+
                           |
                           v
                  +------------------+
                  |     Decision      |
                  +--------+---------+
                           |
                           v
                  +------------------+
                  |    ServiceNow    |
                  |      Update      |
                  +------------------+
```

---

# Security

Never commit sensitive credentials to the repository.

Use environment variables for:

```text
Google Gemini API Key
ServiceNow URL
ServiceNow Username
ServiceNow Password
```

Your `.gitignore` should contain:

```gitignore
.env
.venv/
__pycache__/
```

Use the minimum required permissions for the ServiceNow integration.

---

# Troubleshooting

## FastAPI is not starting

Make sure the virtual environment is activated:

```bash
.venv\Scripts\activate
```

Then reinstall dependencies:

```bash
pip install -r requirements.txt
```

Start the application with:

```bash
uvicorn APP.app:app --reload
```

---

## ServiceNow cannot reach the API

Make sure FastAPI is running:

```bash
uvicorn APP.app:app --reload
```

Then start ngrok:

```bash
ngrok http 8000
```

Use the HTTPS ngrok URL instead of `localhost`.

---

## AI Agent is not responding

Check that the following environment variable is configured correctly:

```text
GOOGLE_GEMINI_API_KEY
```

Also make sure the required LangChain and Gemini dependencies are installed.

---

## Duplicate Incident Is Not Processed

The duplicate check uses the incident `incident_sys_id`.

If the same incident is sent again while the application is running, it should return:

```text
Incident already processed
```

Restarting the FastAPI application clears the in-memory processed incident set.

---

# Development Workflow

```text
Clone Repository
       |
       v
Create Virtual Environment
       |
       v
Install Dependencies
       |
       v
Configure .env
       |
       v
Run FastAPI
       |
       v
Run ngrok
       |
       v
Configure ServiceNow
       |
       v
Create Test Incident
       |
       v
Verify Duplicate Check
       |
       v
Verify AI Decision
       |
       v
Verify ServiceNow Update
       |
       v
Verify All Three Scenarios
```

---

# Project Goal

The goal of this project is to demonstrate how an AI agent can be integrated with an enterprise incident-management platform to automate incident analysis and decision making.

The system combines:

```text
ServiceNow
+
FastAPI
+
LangChain
+
Gemini LLM
+
Knowledge Base
+
Idempotency Check
=
Automated Incident Decision System
```

---

# Getting Started for Contributors

After cloning the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd <PROJECT_FOLDER>

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

Configure the `.env` file, then start the application:

```bash
uvicorn APP.app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

You can now test the webhook using Swagger UI.

---

# License

This project is intended for educational and development purposes.
