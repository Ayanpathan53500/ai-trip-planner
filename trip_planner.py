import os
import requests
from dotenv import load_dotenv
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage
# from langchain_core.pydantic_v1 import BaseModel
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
generator_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
# tavily_tool = TavilySearchResults(max_results=3)
tavily_tool = TavilySearch(max_results=3)


def detect_intent(user_input):
    user_input = user_input.lower()

    intent = {
        "destination": None,
        "duration": None,
        "budget": "moderate"
    }

    # Extract days
    import re
    days = re.search(r'(\d+)\s*days?', user_input)
    if days:
        intent["duration"] = int(days.group(1))

    # Extract destination (simple logic)
    words = user_input.split()
    if "to" in words:
        idx = words.index("to")
        if idx + 1 < len(words):
            intent["destination"] = words[idx + 1].capitalize()

    # Budget detection
    if "low" in user_input:
        intent["budget"] = "low"
    elif "high" in user_input:
        intent["budget"] = "high"

    return intent



class TripPlan(BaseModel):
    trip_title: str
    destination: str
    duration_days: int
    daily_itinerary: List[str]
    budget_notes: str

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    trip_data: dict
    next_task: str
    plan_finalized: bool




class TripInput(BaseModel):
    destination: str
    duration_days: int
    interests: list
    budget: str



def planner_node(state):
    user_input = state["messages"][-1].content

    intent = detect_intent(user_input)

    data = {
        "destination": intent["destination"] or "Manali",
        "duration_days": intent["duration"] or 3,
        "budget": intent["budget"]
    }

    return {
        "trip_data": data,
        "next_task": "research",
        "messages": [HumanMessage(content="planned")]
    }

def research_node(state):
    data = state["trip_data"]
    results = tavily_tool.invoke({"query": data["destination"]})
    data["research_context"] = results
    return {"trip_data": data, "next_task": "weather", "messages": [HumanMessage(content="researched")]}





def weather_node(state):
    import os
    import requests

    data = state["trip_data"]
    city = data["destination"]

    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url).json()

    if response.get("main"):
        weather = {
            "temp": response["main"]["temp"],
            "condition": response["weather"][0]["description"]
        }
    else:
        weather = {"error": "Weather not found"}

    data["weather"] = weather

    return {
        "trip_data": data,
        "next_task": "hotel",
        "messages": [HumanMessage(content="weather added")]
    }


def hotel_node(state):
    data = state["trip_data"]

    query = f"best budget hotels in {data['destination']}"

    results = tavily_tool.invoke({"query": query})

    data["hotels"] = results

    return {
        "trip_data": data,
        "next_task": "cab",
        "messages": [HumanMessage(content="hotels added")]
    }


def cab_node(state):
    data = state["trip_data"]
    city = data["destination"]

    data["transport"] = {
        "options": ["Uber", "Ola", "Local Taxi"],
        "estimated_cost": "₹500 - ₹2000 per day"
    }

    return {
        "trip_data": data,
        "next_task": "generate",
        "messages": [HumanMessage(content="cab added")]
    }


def generator_node(state):
    data = state["trip_data"]

    prompt = f"""
    Create a detailed trip plan:
    Destination: {data['destination']}
    Days: {data['duration_days']}
    Budget: {data['budget']}
    Weather: {data.get('weather')}
    Hotels: {data.get('hotels')}
    Transport: {data.get('transport')}
    """

    response = generator_llm.invoke(prompt)

    data["final_plan"] = response.content

    return {
        "trip_data": data,
        "next_task": "finalize",
        "plan_finalized": True
    }

def route(state):
    return state["next_task"]

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("planner", planner_node)
    graph.add_node("research", research_node)
    graph.add_node("weather", weather_node)
    graph.add_node("hotel", hotel_node)
    graph.add_node("cab", cab_node)
    graph.add_node("generate", generator_node)

    graph.set_entry_point("planner")
    graph.add_conditional_edges("planner", route, {"research": "research"})
    graph.add_edge("research", "weather")
    graph.add_edge("weather", "hotel")
    graph.add_edge("hotel", "cab")
    graph.add_edge("cab", "generate")
    graph.add_edge("generate", END)

    return graph.compile()

if __name__ == "__main__":
    app = build_graph()
    user_input = input("Enter trip: ")
    state = {"messages": [HumanMessage(content=user_input)], "trip_data": {}, "next_task": "planner", "plan_finalized": False}
    result = app.invoke(state)
    print(result["trip_data"].get("final_plan"))
