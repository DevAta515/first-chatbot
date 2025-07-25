import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
import json

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        print(user_message)

        if usecase == "Basic ChatBot":
            for event in graph.stream({'messages': ("user", user_message)}):
                for value in event.values():
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)

        elif usecase == "ChatBot with Web":
            st.markdown("## 🌐 Web-Enabled ChatBot")

            initial_state = {"messages": [user_message]}

            try:
                res = graph.invoke(initial_state)

                # Inline message rendering logic
                for message in res.get("messages", []):
                    if isinstance(message, HumanMessage):
                        with st.chat_message("user"):
                            st.write(message.content)

                    elif isinstance(message, ToolMessage):
                        with st.chat_message("ai"):
                            st.markdown("🔧 **Tool Call Start**")
                            try:
                                parsed = json.loads(message.content)
                                st.json(parsed)
                            except Exception:
                                st.write(message.content)
                            st.markdown("🔧 **Tool Call End**")

                    elif isinstance(message, AIMessage):
                        if message.content:
                            with st.chat_message("assistant"):
                                st.write(message.content)

                    else:
                        with st.chat_message("assistant"):
                            st.markdown("⚠️ Unrecognized message type")
                            st.write(str(message))

            except Exception as e:
                st.error(f"❌ Error while invoking chatbot: {e}")

        elif usecase == "AI News Summariser":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing news... ⏳"):
                result = graph.invoke({"messages": frequency})
                try:
                    # Read the markdown file
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()

                    # Display the markdown content in Streamlit
                    st.markdown(markdown_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")