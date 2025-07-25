from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represent the structure of state used in the Graph.
    """
    messages:Annotated[List, add_messages]