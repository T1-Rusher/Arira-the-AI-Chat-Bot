"""
📝 Working Memory System - AI के लिए
Current task के लिए temporary information store करता है
Limited capacity के साथ (जैसे human working memory में 7±2 items होते हैं)
"""

from collections import deque
from datetime import datetime
import json

class WorkingMemory:
    def __init__(self, capacity=7):
        """
        Working Memory को initialize करें
        
        Args:
            capacity (int): Maximum items जो एक साथ याद रख सकते हैं (default: 7)
        """
        self.capacity = capacity
        self.memory = deque(maxlen=capacity)
        self.attention_focus = None
        
    def add_item(self, item, priority=0):
        """
        Working memory में नया item add करें
        
        Args:
            item: कोई भी information (string, dict, list, etc.)
            priority: item की importance (higher = more important)
        """
        memory_item = {
            'content': item,
            'priority': priority,
            'timestamp': datetime.now().isoformat(),
            'access_count': 0
        }
        self.memory.append(memory_item)
        return f"✓ Item added to working memory. Current capacity: {len(self.memory)}/{self.capacity}"
    
    def get_current_items(self):
        """सभी current items को देखें"""
        return list(self.memory)
    
    def focus_attention(self, index):
        """
        किसी specific item पर attention focus करें
        
        Args:
            index: item का index (0 से start होता है)
        """
        if 0 <= index < len(self.memory):
            self.attention_focus = index
            self.memory[index]['access_count'] += 1
            return f"🎯 Attention focused on: {self.memory[index]['content']}"
        return "❌ Invalid index"
    
    def get_focused_item(self):
        """Currently focused item को retrieve करें"""
        if self.attention_focus is not None and self.attention_focus < len(self.memory):
            return self.memory[self.attention_focus]
        return None
    
    def clear(self):
        """Working memory को पूरी तरह clear करें"""
        self.memory.clear()
        self.attention_focus = None
        return "🗑️ Working memory cleared"
    
    def get_high_priority_items(self):
        """High priority items को filter करें"""
        sorted_items = sorted(self.memory, key=lambda x: x['priority'], reverse=True)
        return sorted_items
    
    def rehearse(self, index):
        """
        Item को rehearse करें (access count बढ़ाएं)
        यह item को working memory में ज्यादा देर तक रखने में मदद करता है
        """
        if 0 <= index < len(self.memory):
            self.memory[index]['access_count'] += 1
            return f"🔄 Rehearsed: {self.memory[index]['content']}"
        return "❌ Invalid index"
    
    def get_status(self):
        """Working memory की current status"""
        return {
            'capacity': self.capacity,
            'current_items': len(self.memory),
            'available_space': self.capacity - len(self.memory),
            'focused_item': self.attention_focus,
            'items': self.get_current_items()
        }


# उदाहरण उपयोग
if __name__ == "__main__":
    print("=" * 60)
    print("📝 WORKING MEMORY DEMO")
    print("=" * 60)
    
    # Working Memory create करें
    wm = WorkingMemory(capacity=5)
    
    # Items add करें
    print("\n1. Items add कर रहे हैं:")
    print(wm.add_item("User ने pizza order करना है", priority=3))
    print(wm.add_item("Delivery address: 123 Main Street", priority=2))
    print(wm.add_item("Payment method: Credit Card", priority=1))
    print(wm.add_item("Special instructions: Extra cheese", priority=1))
    
    # Current items देखें
    print("\n2. Current Working Memory:")
    for idx, item in enumerate(wm.get_current_items()):
        print(f"   [{idx}] {item['content']} (Priority: {item['priority']})")
    
    # Attention focus करें
    print("\n3. Attention focus:")
    print(wm.focus_attention(0))
    
    # High priority items
    print("\n4. High Priority Items:")
    for item in wm.get_high_priority_items()[:3]:
        print(f"   • {item['content']} (Priority: {item['priority']})")
    
    # Status check करें
    print("\n5. Memory Status:")
    status = wm.get_status()
    print(f"   Capacity: {status['current_items']}/{status['capacity']}")
    print(f"   Available space: {status['available_space']}")
