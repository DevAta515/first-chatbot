from typing import Annotated, list
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represent the structure of state used in the Graph.
    """
    messages:Annotated[list, add_messages]