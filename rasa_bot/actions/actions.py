from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionTechnicalSupport(Action):
    def name(self) -> Text:
        return "action_technical_support"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        product = tracker.get_slot("product")
        response = f"I understand you're having issues with your {product}. Let me help you troubleshoot that."
        dispatcher.utter_message(text=response)
        return []

class ActionProductInfo(Action):
    def name(self) -> Text:
        return "action_product_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        product = tracker.get_slot("product")
        response = f"Here's the information about {product}. What specific details would you like to know?"
        dispatcher.utter_message(text=response)
        return [] 