# from src.LangGraph.node.chatbot_web import ChatBotWithWeb
from src.LangGraph.tools.search_tool import create_tool_node, get_tools
from src.LangGraph.node.chatbot_node import BasicChatBotNode
from src.LangGraph.state.state import State
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from src.LangGraph.node.chatbot_web import ChatBotWithWeb
from src.LangGraph.node.ai_news_node import AINewsNode


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

    def chatbot_with_web_tool(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node 
        and a tool node. It defines tools, initializes the chatbot with tool 
        capabilities, and sets up conditional and direct edges between nodes. 
        The chatbot node is set as the entry point.
        """
        llm = self.llm
        tools = get_tools()
        tool_node = create_tool_node(tools)

        chatbot_web_node = ChatBotWithWeb(llm)

        self.graph_builder.add_node("chatbot", chatbot_web_node.create_chatbot(tools))
        self.graph_builder.add_node("tools", tool_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")

    def ai_news_graph(self):
        ai_node=AINewsNode(self.llm)

        self.graph_builder.add_node("fetch_news",ai_node.fetch_news)
        self.graph_builder.add_node("summarise_news",ai_node.summarize_news)
        self.graph_builder.add_node("save_result",ai_node.save_result)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarise_news")
        self.graph_builder.add_edge("summarise_news","save_result")
        self.graph_builder.add_edge("save_result",END)

    def setup_graph(self, usecase:str):
        """
        Sets up graph for the selected use case.
        """
        if usecase=="Basic ChatBot":
            self.basic_chatbot()
        if usecase=="ChatBot with Web":
            self.chatbot_with_web_tool()
        if usecase=="AI News Summariser":
            self.ai_news_graph()

        return self.graph_builder.compile()