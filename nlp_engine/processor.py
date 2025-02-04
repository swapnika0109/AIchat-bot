import spacy
from textblob import TextBlob
from typing import Dict, List
import openai
import os

class NLPProcessor:
    def __init__(self):
        # Load SpaCy model
        self.nlp = spacy.load("en_core_web_md")
        
        # Initialize OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def process_text(self, text: str) -> Dict:
        """Process text through multiple NLP pipelines"""
        # SpaCy processing
        doc = self.nlp(text)
        
        # TextBlob sentiment
        blob = TextBlob(text)
        
        # Basic NLP results
        results = {
            'entities': [(ent.text, ent.label_) for ent in doc.ents],
            'tokens': [token.text for token in doc],
            'sentiment': {'polarity': blob.sentiment.polarity},
            'key_phrases': self.extract_key_phrases(doc)
        }
        
        return results

    def extract_key_phrases(self, doc) -> List[str]:
        """Extract important phrases using dependency parsing"""
        key_phrases = []
        for chunk in doc.noun_chunks:
            if chunk.root.dep_ in ['nsubj', 'dobj']:
                key_phrases.append(chunk.text)
        return key_phrases 