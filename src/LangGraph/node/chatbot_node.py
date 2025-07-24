from src.LangGraph.state.state import State

class BasicChatBotNode:

    def __init__(self,model):
        self.llm=model

    def process(self, state:State)->dict:
        """
        Process the input and generate a chatbot reference
        """

        return {"messages":self.llm(state['messages'])}