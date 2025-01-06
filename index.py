from dotenv import load_dotenv
import getpass
import os
from typing import Annotated
from typing_extensions import TypedDict
# langgraph imports
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

load_dotenv()

def _set_env(var: str):
  if not os.environ.get(var):
    print(os.environ)
    os.environ[var] = getpass.getpass(f"Enter {var}: ")
  else :
    print(f"{var} already set")

# State of the graph using TypedDict
class State(TypedDict):
  # Messages have the type "list".
  messages: Annotated[list, add_messages]

def chatbot(state: State):
  return { "messages": llm.invoke(state["messages"]) }

def stream_graph_updates(user_input: str):
  for event in graph.stream({"messages": [("user", user_input)]}):
    for value in event.values():
      print("Assistant", value["messages"][-1].content)

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# --- Executions --- #
_set_env("OPENAI_API_KEY")

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

while True:
  try:
    user_input = input("User:")
    if user_input.lower() in ["quit", "q", "exit"]:
      print("Goodbye!")
      break
    
    stream_graph_updates(user_input)
  except:
    # fallback if input() in not available
    user_input = "What do you know about LangGraph?"
    print("User: " + user_input)
    stream_graph_updates(user_input)
    break