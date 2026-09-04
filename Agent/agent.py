from dotenv import load_dotenv
from pydantic import BaseModel                                  
from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
from Model.data import Decision

#load Data
load_dotenv()
def agentDecision(knowledge , ticket):
    #Create Gemini Model
    llm = ChatGoogleGenerativeAI(
        model = "gemini-3.6-flash",
        api_key=os.getenv("GOOGLE_GEMINI_API_KEY")
    )
    
    #Create the Prompt and Put the Placeholders
    prompt = ChatPromptTemplate.from_template("""
        You are an advanced AI support operations router. Analyze the incoming support ticket and the provided knowledge base to determine the correct routing decision.
        
        ### Valid Decisions:
        1. ask
        2. respond
        3. escalate
        
        ### Strict Evaluation Logic:
        Evaluate the ticket against the rules below in exact sequential order:
        
        - **Rule 1 (Vulnerability / Ambiguity Check):** If the ticket text lacks specific details, contains vague descriptions, or is missing essential context needed to diagnose the root cause, output **ask**. (Note: This rule takes absolute precedence over any matching knowledge base article).
        - **Rule 2 (Knowledge Base Match Check):** If the ticket clearly and specifically defines a technical or functional problem, and the provided Knowledge Base contains an explicit, direct solution addressing that exact problem, output **respond**.
        - **Rule 3 (Fallback / Manual Intervention):** If the ticket is clear and specific, but the Knowledge Base lacks a matching article or the issue requires administrative/human intervention, output **escalate**.
        
        ### Execution Instructions:
        1. **Analyze the Ticket:** Identify if the user's core issue is concrete or ambiguous.
        2. **Scan the Knowledge Base:** Search for a direct alignment between the identified issue and the provided knowledge text. Never extrapolate, assume, or invent facts not explicitly written in the knowledge base.
        3. **Formulate the Output:**
           - If the decision is **ask**, generate a smart, contextual clarifying question that points out what is missing from the vague description and asks the user to provide the specific technical details, error codes, or context needed to proceed.
           - If the decision is **respond**, construct the reply strictly using the verified solution from the knowledge base.
           - If the decision is **escalate**, state clearly and professionally that the query has been routed to a human support agent.
        
        ### Input Data:
        Ticket:
        {ticket}
        
        Knowledge Base:
        {knowledge}
        """
        )
    #Told Gemini That Response is be like Decision (Pydantic Class)
    structured_llm = llm.with_structured_output(Decision)
    
    #chain the Components
    chain = prompt | structured_llm
    
    #Excute Process
    result = chain.invoke({
        "ticket" : ticket,
        "knowledge" : knowledge
    })
    
    return result
    
    