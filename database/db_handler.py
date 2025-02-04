from typing import Dict, Any
import json
import os
from datetime import datetime

class DatabaseHandler:
    def __init__(self):
        self.conversations_file = "conversations.json"
        self._initialize_storage()

    def _initialize_storage(self):
        """Initialize local storage file if it doesn't exist"""
        if not os.path.exists(self.conversations_file):
            with open(self.conversations_file, 'w') as f:
                json.dump([], f)

    def store_conversation(self, user_id: str, message: str, 
                         response: str, metadata: Dict[str, Any]):
        """Store conversation in local JSON file"""
        conversation = {
            "user_id": user_id,
            "message": message,
            "response": response,
            "metadata": metadata,
            "timestamp": datetime.now().isoformat()
        }
        
        # Read existing conversations
        with open(self.conversations_file, 'r') as f:
            conversations = json.load(f)
        
        # Add new conversation
        conversations.append(conversation)
        
        # Save updated conversations
        with open(self.conversations_file, 'w') as f:
            json.dump(conversations, f, indent=2)

    def get_recent_conversations(self, limit: int = 10) -> list:
        """Get recent conversations"""
        with open(self.conversations_file, 'r') as f:
            conversations = json.load(f)
        return conversations[-limit:] 