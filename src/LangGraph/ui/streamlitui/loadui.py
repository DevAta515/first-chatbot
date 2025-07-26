import streamlit as st
import os


from src.LangGraph.ui.uiconfigfile import Config

class LoadStreamUi:
    def __init__(self):
        self.config=Config()
        self.user_controls={}
    
    def load_streamlit_ui(self):
        st.set_page_config(page_title= "🤖 " + self.config.get_title(), layout="wide")
        st.header("🤖 " + self.config.get_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False

        with st.sidebar:
            llm_options=self.config.get_llms()
            usecase_options=self.config.get_usecase()   

            self.user_controls["selected_llm"]=st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"]=="Groq":
                model_options=self.config.get_models()
                self.user_controls["selected_groq_model"]=st.selectbox("Select Model",model_options)
                self.user_controls["GROQ_API_KEY"]=st.session_state["GROQ_API_KEY"]=st.text_input("GROQ API Key", type="password")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your Groq as well as Tavily Api Key.")
            
            self.user_controls["Selected_Usecases"]=st.selectbox("Select Usecases", usecase_options)
            
            if self.user_controls["Selected_Usecases"]=="ChatBot with Web" or self.user_controls["Selected_Usecases"]=="AI News Summariser":
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]=st.text_input("Tavily API Key", type="password")

            if self.user_controls["Selected_Usecases"]=='AI News Summariser':
                st.subheader("📰 AI News Explorer ")
                
                with st.sidebar:
                    time_frame = st.selectbox(
                        "📅 Select Time Frame",
                        ["Daily", "Weekly", "Monthly"],
                        index=0
                    )
                if st.button("🔍 Fetch Latest AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame

        return self.user_controls