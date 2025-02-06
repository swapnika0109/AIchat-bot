import streamlit as st
import asyncio

class Dashboard:
    def __init__(self):
        self.agent = None
        self.nlp_processor = None
        self.setup_streamlit()

    def setup_streamlit(self):
        st.title("Rasa Chatbot")
        # Initialize session state for chat history if it doesn't exist
        if 'messages' not in st.session_state:
            st.session_state.messages = []

    def set_rasa_agent(self, agent):
        self.agent = agent

    def set_nlp_processor(self, processor):
        self.nlp_processor = processor

    async def process_message(self, message: str):
        # Get NLP insights first
        nlp_insights = self.nlp_processor.process_text(message)
        
        # Get Rasa response
        rasa_response = await self.agent.handle_text(message)
        response_text = rasa_response[0]['text'] if rasa_response else "I'm not sure how to respond to that."
        
        # Enhance response based on NLP insights
        enhanced_response = self._enhance_response(response_text, nlp_insights)
        
        return {
            'rasa_response': [{'text': enhanced_response}],
            'nlp_insights': nlp_insights
        }

    def _enhance_response(self, response_text, nlp_insights):
        # Enhance response based on sentiment
        sentiment = nlp_insights['sentiment']['polarity']
        if sentiment < -0.3:
            response_text = f"I sense you're feeling frustrated. {response_text}"
        elif sentiment > 0.3:
            response_text = f"I'm glad you're feeling positive! {response_text}"
        
        # Enhance response based on entities
        entities = nlp_insights['entities']
        if entities:
            for entity_text, entity_type in entities:
                if entity_type == 'PERSON':
                    response_text = f"Regarding {entity_text}, {response_text}"
                elif entity_type == 'ORG':
                    response_text = f"About {entity_text}, {response_text}"
                elif entity_type == 'LOC':
                    response_text = f"Speaking of {entity_text}, {response_text}"
        
        # Use key phrases to add context
        key_phrases = nlp_insights['key_phrases']
        if key_phrases and len(key_phrases) > 0:
            response_text += f" I notice you mentioned {key_phrases[0]}."
            
        return response_text

    async def get_bot_response(self, user_message):
        try:
            if self.agent:
                response = await self.agent.handle_text(user_message)
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
                # Display NLP insights if they exist
                if "nlp_insights" in message:
                    with st.expander("Message Analysis"):
                        st.write("📊 Sentiment:", self._format_sentiment(message["nlp_insights"]["sentiment"]))
                        st.write("🏷️ Entities:", self._format_entities(message["nlp_insights"]["entities"]))
                        st.write("🔑 Key Phrases:", message["nlp_insights"]["key_phrases"])

        # Accept user input
        if prompt := st.chat_input("What's your message?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response_data = asyncio.run(self.process_message(prompt))
                    response_text = response_data['rasa_response'][0]['text'] if response_data['rasa_response'] else "I'm not sure how to respond to that."
                    
                    # Store both response and insights
                    message_data = {
                        "role": "assistant",
                        "content": response_text,
                        "nlp_insights": response_data['nlp_insights']
                    }
                    st.session_state.messages.append(message_data)
                    
                    # Display response
                    st.markdown(response_text)
                    
                    # Display NLP insights in an expander
                    with st.expander("Message Analysis"):
                        st.write("📊 Sentiment:", self._format_sentiment(response_data['nlp_insights']['sentiment']))
                        st.write("🏷️ Entities:", self._format_entities(response_data['nlp_insights']['entities']))
                        st.write("🔑 Key Phrases:", response_data['nlp_insights']['key_phrases'])

    def _format_sentiment(self, sentiment):
        polarity = sentiment['polarity']
        if polarity > 0:
            return "😊 Positive"
        elif polarity < 0:
            return "😟 Negative"
        return "😐 Neutral"

    def _format_entities(self, entities):
        if not entities:
            return "No entities found"
        return ", ".join([f"{text} ({label})" for text, label in entities])

    # ... rest of your dashboard code ...