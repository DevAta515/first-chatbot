import streamlit as st
import os


from src.LangGraph.ui.uiconfigfile import Config

class LoadStreamUi:
    def __init__(self):
        self.config=Config()
        self.user_controls={}
    
    def load_streamlit_ui(self):
        st.set_page_config(page_title="I am " + self.config.get_title(), layout='wide')
        st.header("*"+self.config.get_title())

        with st.sidebar:
            llm_options=self.config.get_llms()
            usecase_options=self.config.get_usecase()   

            self.user_controls["selected_llm"]=st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"]=="Groq":
                model_options=self.config.get_models()
                self.user_controls["selected_groq_model"]=st.selectbox("Select Model",model_options)
                self.user_controls["GROQ_API_KEY"]=st.session_state["GROQ_API_KEY"]=st.text_input("API Key", type="password")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your Groq Api Key.")
            
            self.user_controls["Selected_Usecases"]=st.selectbox("Select Usecases", usecase_options)

        return self.user_controls