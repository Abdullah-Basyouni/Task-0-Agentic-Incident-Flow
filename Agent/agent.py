from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os

from Model.data import Decision


# Load environment variables
load_dotenv()


def agentDecision(knowledge, ticket):

    # Create Gemini Model
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        api_key=os.getenv("GOOGLE_GEMINI_API_KEY")
    )

    # Load prompt from prompt.txt
    with open("prompt.txt", "r", encoding="utf-8") as file:
        prompt_text = file.read()

    # Create prompt template
    prompt = ChatPromptTemplate.from_template(prompt_text)

    # Tell Gemini to return the Decision Pydantic model
    structured_llm = llm.with_structured_output(Decision)

    # Chain prompt + LLM
    chain = prompt | structured_llm

    # Execute the chain
    result = chain.invoke({
        "ticket": ticket,
        "knowledge": knowledge
    })

    return result