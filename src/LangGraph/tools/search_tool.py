from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Return the tools to be used in the chatbot
    """
    tavily_tool=TavilySearch(max_results=2, topic="general") 
    tools=[tavily_tool]
    return tools

def create_tool_node(tools):
    """
    Create and returns a tool node for the graph
    """
    return ToolNode(tools=tools)