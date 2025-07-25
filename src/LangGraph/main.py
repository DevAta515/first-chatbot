from src.LangGraph.graph.graph_builder import GraphBuilder
from src.LangGraph.ui.streamlitui.loadui import LoadStreamUi

import streamlit as st
from src.LangGraph.llms.groqllm import GroqLLM

from src.LangGraph.ui.streamlitui.display_result import DisplayResultStreamlit

def load_agentic_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.
    
    """

    ui=LoadStreamUi()
    user_input=ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    

    if st.session_state.IsFetchButtonClicked:
        user_message=st.session_state.timeframe
    else:
        user_message=st.chat_input("Enter your message:")


    if user_message:
        try:
            obj_llm_config=GroqLLM(user_controls_input=user_input)
            model=obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialised.")
                return
            
            usecase=user_input.get('Selected_Usecases')
            if not usecase:
                st.error("Error: no usecase is selected")
                return

            graph_builder=GraphBuilder(model)
            try:
                graph=graph_builder.setup_graph(usecase)
                # print(usecase,graph,user_message)
                print("Hello about to display")
                print("Usecase",usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()

            except Exception as e:
                st.error(f"Error: In setting up the graph {e}")
                return
        except Exception as e:
            st.error(f"Error: Inside main.py")