from src.LangGraph.node.chatbot_node import BasicChatBotNode
from src.LangGraph.state.state import State
from langgraph.graph import StateGraph, START, END

class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """

        self.basic_chatbot_node=BasicChatBotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def setup_graph(self, usecase:str):
        """
        Sets up graph for the selected use case.
        """
        if usecase=="Basic ChatBot":
            self.basic_chatbot()

        return self.graph_builder.compile()