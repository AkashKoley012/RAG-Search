from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

import json

load_dotenv()

# Define structured output schema
class Section(BaseModel):
    subtitle: str = Field(..., description="Subtitle of the section")
    summary: str = Field(..., description="2-3 sentence summary of the section")
    source_url: str = Field(..., description="URL where the information came from")

class StructuredSummary(BaseModel):
    title: str = Field(..., description="Main title summarizing the query")
    sections: List[Section] = Field(..., description="List of key subtopics with summaries and sources")

# Initialize Gemini model
model = ChatGoogleGenerativeAI(
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    model="gemini-1.5-flash",
    temperature=0.7,
)

# Use Pydantic parser
parser = PydanticOutputParser(pydantic_object=StructuredSummary)

# Prompt Template
template = PromptTemplate(
    template="""
You are a structured summarizer AI that produces clean, article-style answers.

Given the user's query and web context, do the following:

1. Generate a main title summarizing the entire topic.
2. Generate 3 to 4 subtopics as clear subtitles.
3. For each subtitle:
    - Provide 2 to 3 bullet points.
    - Each bullet should be 3–4 sentences long, informative, and well-structured.
    - At the end of each subtitle section, include a source URL in the format: Source: [link]
4. End with a "Conclusion" section that summarizes the topic and its broader significance.

Keep the language informative, neutral, and objective. Format the content with clean markdown (use # for titles if needed, or keep plain text).

{format_instructions}

User Query: {query}
Web Context: {context}
""",
    input_variables=["query", "context"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Create graph once at module level
memory = MemorySaver()
workflow = StateGraph(state_schema=MessagesState)

# Core logic node: Returns pure JSON
def call_model(state: MessagesState) -> dict:
    user_query = state["messages"][-1].content
    context = state.get("context", "")
    
    # Format prompt
    formatted_prompt = template.format(query=user_query, context=context)
    
    # Invoke model
    raw_response = model.invoke(formatted_prompt)
    
    # Parse structured output
    parsed = parser.parse(raw_response.content)
    
    # Return parsed object as JSON string
    return {
        "messages": state["messages"] + [SystemMessage(content=parsed.model_dump_json(indent=2))]
    }

# Build and compile graph
workflow.add_node("model", call_model)
workflow.set_entry_point("model")
workflow.set_finish_point("model")
app = workflow.compile(checkpointer=memory)

# Main function: Returns JSON string
def generate_response_with_memory(query, context, session_id):
    # print(context)
    input_data = {
        "messages": [HumanMessage(content=query)],
        "context": context
    }

    result = app.invoke(
        input=input_data,
        config={"configurable": {"thread_id": session_id}}
    )
    return result["messages"][-1].content
