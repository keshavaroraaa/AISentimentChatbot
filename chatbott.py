import re
from collections import deque
import random

class SentimentAnalyzer:
    """Simple rule-based sentiment analyzer"""
    
    def __init__(self):
        self.positive_words = {
            'happy', 'joy', 'love', 'excellent', 'good', 'great', 'amazing',
            'wonderful', 'fantastic', 'perfect', 'thank', 'thanks', 'awesome',
            'brilliant', 'nice', 'beautiful', 'excited', 'pleasure'
        }
        self.negative_words = {
            'sad', 'angry', 'hate', 'terrible', 'bad', 'awful', 'horrible',
            'worst', 'annoying', 'frustrated', 'disappointed', 'upset', 'mad',
            'furious', 'depressed', 'unhappy', 'miserable'
        }
        
    def analyze(self, text):
        """Analyze sentiment and return score (-1 to 1) and label"""
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        
        pos_count = sum(1 for word in words if word in self.positive_words)
        neg_count = sum(1 for word in words if word in self.negative_words)
        
        # Calculate sentiment score
        total = pos_count + neg_count
        if total == 0:
            score = 0
        else:
            score = (pos_count - neg_count) / total
            
        # Determine label
        if score > 0.2:
            label = "positive"
        elif score < -0.2:
            label = "negative"
        else:
            label = "neutral"
            
        return {"score": score, "label": label}


class EmotionalChatbot:
    """AI Chatbot that responds based on sentiment"""
    
    def __init__(self):
        self.analyzer = SentimentAnalyzer()
        self.conversation_history = deque(maxlen=5)
        self.user_name = None
        
        self.responses = {
            "positive": [
                "That's wonderful to hear! Tell me more!",
                "I'm so glad you're feeling positive! What else is on your mind?",
                "Your enthusiasm is contagious! Keep going!",
                "Love the positive energy! How can I help you further?"
            ],
            "negative": [
                "I'm sorry you're feeling this way. Want to talk about it?",
                "That sounds tough. I'm here to listen if you need.",
                "I understand this is frustrating. How can I support you?",
                "Let's see if we can work through this together."
            ],
            "neutral": [
                "Interesting. Tell me more about that.",
                "I see. What else would you like to discuss?",
                "Got it. How can I help you today?",
                "I'm listening. What's on your mind?"
            ]
        }
        
    def get_response(self, user_input):
        """Generate response based on sentiment"""
        # Analyze sentiment
        sentiment = self.analyzer.analyze(user_input)
        
        # Store in history
        self.conversation_history.append({
            "input": user_input,
            "sentiment": sentiment
        })
        
        # Generate contextual response
        response = random.choice(self.responses[sentiment["label"]])
        
        # Add personalization if name is known
        if self.user_name and random.random() > 0.7:
            response = f"{self.user_name}, {response.lower()}"
            
        return response, sentiment
    
    def get_sentiment_trend(self):
        """Analyze sentiment trend over conversation"""
        if len(self.conversation_history) < 2:
            return "Not enough data yet"
        
        scores = [msg["sentiment"]["score"] for msg in self.conversation_history]
        avg_score = sum(scores) / len(scores)
        
        if avg_score > 0.2:
            return "Overall positive conversation (trending up)"
        elif avg_score < -0.2:
            return "Overall negative conversation (trending down)"
        else:
            return "Neutral conversation (stable)"


def main():
    """Main chatbot loop"""
    print("=" * 60)
    print("AI SENTIMENT CHATBOT")
    print("=" * 60)
    print("I analyze your emotions and respond accordingly!")
    print("Type 'quit' to exit, 'trend' to see sentiment analysis")
    print("=" * 60)
    
    chatbot = EmotionalChatbot()
    
    # Get user name
    name = input("\nWhat's your name? ")
    if name.strip():
        chatbot.user_name = name
        print(f"\nNice to meet you, {name}! Let's chat.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            print("\nThanks for chatting! Have a great day!")
            break
            
        if user_input.lower() == 'trend':
            trend = chatbot.get_sentiment_trend()
            print(f"\nSentiment Analysis: {trend}\n")
            continue
        
        # Get response
        response, sentiment = chatbot.get_response(user_input)
        
        # Display sentiment info
        print(f"\n[Sentiment: {sentiment['label'].upper()} | Score: {sentiment['score']:.2f}]")
        print(f"Bot: {response}\n")


if __name__ == "__main__":
    main()