# AI-Powered ServiceNow Incident Decision System

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=24&duration=3000&pause=800&color=00FF9C&center=true&vCenter=true&width=850&lines=Initializing+AI+Incident+Decision+System...;Connecting+to+ServiceNow...;Receiving+Incident+Data...;Analyzing+Incident+with+AI+Agent...;Searching+Knowledge+Base...;Generating+Decision...;Updating+ServiceNow...;Workflow+Completed+Successfully." alt="AI Incident Decision System Animation" />
</p>

<p align="center">
  An AI-powered system that analyzes ServiceNow incidents, uses a knowledge base to make decisions, and automatically updates the incident.
</p>

---

## Overview

This project integrates **ServiceNow**, **FastAPI**, **LangChain**, and an **LLM** to create an automated incident decision workflow.

When an incident is created in ServiceNow, the system receives the incident data through an API endpoint, analyzes it using an AI agent and a knowledge base, generates a decision, and sends the result back to ServiceNow.

### Workflow

```text
ServiceNow
    |
    v
FastAPI
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
* Automatic incident updates
* Pydantic request validation
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
| LLM API    | Incident reasoning        |
| ServiceNow | Incident management       |
| JSON       | Knowledge base            |
| ngrok      | Expose local API          |

---

## Project Structure

```text
project/
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
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### Components

**`main.py`**

Contains the FastAPI application and API endpoints.

**`Agent/agent.py`**

Contains the AI decision logic using LangChain and the configured LLM.

**`ServiceNow/serviceNow.py`**

Handles communication with the ServiceNow API.

**`Model/data.py`**

Contains Pydantic models used to validate incoming incident data.

**`kb_articles.json`**

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
LLM_API_KEY=your_api_key

SERVICENOW_INSTANCE=https://your-instance.service-now.com
SERVICENOW_USERNAME=your_username
SERVICENOW_PASSWORD=your_password
```

Do not commit `.env` to GitHub.

Make sure it is included in `.gitignore`:

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

---

# Running the API

Start the FastAPI server:

```bash
uvicorn main:app --reload
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

# Testing the API

Example request:

```json
{
  "short_description": "Printer not printing after office move",
  "description": "The printer was working yesterday. I tried turning it off and on."
}
```

The API processes the incident and sends it to the AI decision system.

The general processing flow is:

```text
Incident Request
       |
       v
Pydantic Validation
       |
       v
AI Agent
       |
       v
Knowledge Base Search
       |
       v
Decision Generation
       |
       v
ServiceNow Update
```

---

# ServiceNow Integration

The application can be connected to a ServiceNow Personal Developer Instance.

The integration allows the system to:

1. Receive incident information.
2. Analyze the incident.
3. Generate an AI-based decision.
4. Update the corresponding incident in ServiceNow.

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

because the address is only accessible from your local machine.

Use ngrok to expose the FastAPI application.

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Then run:

```bash
ngrok http 8000
```

ngrok will generate a public HTTPS URL similar to:

```text
https://example.ngrok-free.app
```

Use this public URL when configuring the ServiceNow request.

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
AI Agent
     |
     v
Knowledge Base
     |
     v
Decision
     |
     v
ServiceNow
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
4. AI Agent analyzes the incident
                 |
                 v
5. Knowledge Base is consulted
                 |
                 v
6. AI generates a decision
                 |
                 v
7. ServiceNow incident is updated
```

---

# Decision Example

An incident such as:

```text
Short Description:
Printer not printing after office move

Description:
It was working yesterday. I tried turning it off and on.
```

can be analyzed by the AI agent using the available knowledge base.

The generated decision can then be used to determine the appropriate incident action, such as:

```text
Resolve
Escalate
Investigate
```

The final result can be sent back to ServiceNow automatically.

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
                   |    AI Agent      |
                   |    LangChain     |
                   +--------+---------+
                            |
                 +----------+----------+
                 |                     |
                 v                     v
        +----------------+    +----------------+
        | Knowledge Base |    |      LLM       |
        +----------------+    +----------------+
                 |                     |
                 +----------+----------+
                            |
                            v
                   +------------------+
                   |     Decision     |
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
LLM API Keys
ServiceNow Username
ServiceNow Password
ServiceNow Credentials
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

---

## ServiceNow cannot reach the API

Make sure FastAPI is running:

```bash
uvicorn main:app --reload
```

Then start ngrok:

```bash
ngrok http 8000
```

Use the HTTPS ngrok URL instead of `localhost`.

---

## AI Agent is not responding

Check:

```text
LLM_API_KEY
```

and make sure the required LangChain/LLM dependencies are installed.

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
Verify AI Decision
       |
       v
Verify ServiceNow Update
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
LLM
+
Knowledge Base
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
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

You can now test the API using Swagger UI.

---

# License

This project is intended for educational and development purposes.
