from typing import Dict, Any
import os

class RAGSystem:
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = knowledge_base_path
        self.knowledge_base = self._load_knowledge_base()

    def _load_knowledge_base(self) -> Dict[str, str]:
        """Load knowledge base from text file"""
        knowledge = {}
        with open(os.path.join(self.knowledge_base_path, 'product_info.txt'), 'r') as f:
            current_product = None
            current_info = []
            
            for line in f:
                line = line.strip()
                if line.endswith(':'):
                    if current_product:
                        knowledge[current_product] = '\n'.join(current_info)
                    current_product = line[:-1]
                    current_info = []
                elif line.startswith('- '):
                    current_info.append(line[2:])
            
            if current_product:
                knowledge[current_product] = '\n'.join(current_info)
                
        return knowledge

    def query(self, question: str) -> Dict[str, Any]:
        """Simple keyword-based query"""
        response = {"answer": "I couldn't find specific information about that."}
        
        # Extract product name from question
        for product in self.knowledge_base:
            if product.lower() in question.lower():
                response["answer"] = f"Here's what I know about {product}:\n{self.knowledge_base[product]}"
                break
                
        return response 