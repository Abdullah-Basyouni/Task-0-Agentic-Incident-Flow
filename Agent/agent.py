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
        You classify support tickets into exactly one decision:
        
        respond, ask, escalate.
        
        Rules:
        
        - ask: Choose this FIRST whenever the ticket is vague or lacks enough
          information to identify the exact problem. This rule overrides a
          potentially relevant knowledge-base article.
        - respond: Choose ONLY when the ticket clearly identifies the problem
          AND the knowledge base directly provides a solution for that exact
          problem.
        - escalate: Choose when no knowledge-base article covers the request
          or human intervention is required.
        
        Never guess or invent information.
        
        For "ask", response MUST be a question requesting the missing details.
        For "respond", response MUST use the solution from the knowledge base.
        For "escalate", response MUST explain that human assistance is required.
        
        Decision priority:
        vague/incomplete ticket → ask
        clear ticket + matching article → respond
        no matching article → escalate
        
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
    
    