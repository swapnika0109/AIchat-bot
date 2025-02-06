import streamlit as st
import asyncio

class Dashboard:
    def __init__(self):
        self.rasa_agent = None
        self.setup_streamlit()

    def setup_streamlit(self):
        st.title("Rasa Chatbot")
        # Initialize session state for chat history if it doesn't exist
        if 'messages' not in st.session_state:
            st.session_state.messages = []

    def set_rasa_agent(self, agent):
        self.rasa_agent = agent

    async def get_bot_response(self, user_message):
        try:
            if self.rasa_agent:
                response = await self.rasa_agent.handle_text(user_message)
                if response and len(response) > 0:
                    return response[0]['text']
                return "I'm not sure how to respond to that."
            return "Bot is not initialized"
        except Exception as e:
            st.error(f"Error getting response: {str(e)}")
            return "Error processing your request"

    def run_server(self, debug=False, port=8501):
        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("What's your message?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = asyncio.run(self.get_bot_response(prompt))
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

    # ... rest of your dashboard code ...