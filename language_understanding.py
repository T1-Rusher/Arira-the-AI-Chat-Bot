"""
📖 Language Understanding - AI के लिए NLU Engine
Text को analyze करके meaning निकालता है
"""

from datetime import datetime
import re

class LanguageUnderstanding:
    def __init__(self):
        """NLU Engine को initialize करें"""
        self.parsing_history = []
        
    def tokenize(self, text):
        """Text को tokens में break करना"""
        tokens = text.split()
        return {'tokens': tokens, 'count': len(tokens)}
    
    def extract_entities(self, text):
        """Named entities extract करना"""
        entities = {
            'dates': re.findall(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', text),
            'emails': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
            'phone': re.findall(r'\b\d{10}\b', text),
            'urls': re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        }
        return entities
    
    def detect_intent(self, text):
        """User intent detect करना"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['what', 'where', 'when', 'who', 'how', 'क्या', 'कहाँ', 'कब']):
            return {'intent': 'question', 'confidence': 0.8}
        elif any(word in text_lower for word in ['please', 'can you', 'could you', 'कृपया']):
            return {'intent': 'request', 'confidence': 0.7}
        elif any(word in text_lower for word in ['thanks', 'thank you', 'धन्यवाद']):
            return {'intent': 'gratitude', 'confidence': 0.9}
        else:
            return {'intent': 'statement', 'confidence': 0.6}
    
    def sentiment_analysis(self, text):
        """Sentiment analyze करना"""
        positive_words = ['good', 'great', 'excellent', 'happy', 'love', 'best', 'अच्छा', 'बढ़िया']
        negative_words = ['bad', 'worst', 'hate', 'terrible', 'sad', 'poor', 'खराब', 'बुरा']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return {'sentiment': 'positive', 'score': 0.7}
        elif neg_count > pos_count:
            return {'sentiment': 'negative', 'score': -0.7}
        else:
            return {'sentiment': 'neutral', 'score': 0.0}
    
    def parse_sentence(self, text):
        """Complete sentence parsing"""
        result = {
            'original_text': text,
            'tokens': self.tokenize(text),
            'entities': self.extract_entities(text),
            'intent': self.detect_intent(text),
            'sentiment': self.sentiment_analysis(text),
            'timestamp': datetime.now().isoformat()
        }
        
        self.parsing_history.append(result)
        return result

if __name__ == "__main__":
    print("📖 LANGUAGE UNDERSTANDING DEMO")
    lu = LanguageUnderstanding()
    
    text = "Can you help me find a good restaurant in Delhi? Thanks!"
    
    print(f"\nAnalyzing: '{text}'")
    result = lu.parse_sentence(text)
    print(f"   Intent: {result['intent']['intent']}")
    print(f"   Sentiment: {result['sentiment']['sentiment']}")
    print(f"   Tokens: {result['tokens']['count']}")
