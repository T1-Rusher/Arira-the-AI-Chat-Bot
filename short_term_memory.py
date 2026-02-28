"""
💾 Short-term Memory System - AI के लिए
Recent conversations और events को याद रखता है
Time-based decay के साथ (पुरानी information धीरे-धीरे भूल जाती है)
"""

from datetime import datetime, timedelta
from collections import OrderedDict
import time

class ShortTermMemory:
    def __init__(self, retention_time=3600, max_items=50):
        """
        Short-term Memory को initialize करें
        
        Args:
            retention_time (int): Seconds में - कितनी देर तक items याद रहेंगे (default: 1 hour)
            max_items (int): Maximum items जो store हो सकते हैं
        """
        self.retention_time = retention_time
        self.max_items = max_items
        self.memory = OrderedDict()
        self.interaction_count = 0
    
    def store(self, key, value, importance=1.0):
        """
        Short-term memory में information store करें
        
        Args:
            key: unique identifier
            value: store करने वाली information
            importance (float): 0.0 to 1.0, जितना ज्यादा उतना ज्यादा समय तक याद रहेगा
        """
        self.interaction_count += 1
        
        # पुराने items remove करें अगर limit exceed हो गई
        if len(self.memory) >= self.max_items:
            self.memory.popitem(last=False)
        
        memory_entry = {
            'value': value,
            'timestamp': datetime.now(),
            'importance': importance,
            'access_count': 0,
            'last_accessed': datetime.now(),
            'interaction_id': self.interaction_count
        }
        
        self.memory[key] = memory_entry
        return f"✓ Stored in short-term memory: {key}"
    
    def recall(self, key):
        """
        Information को recall करें
        
        Args:
            key: retrieve करने के लिए identifier
        """
        self._cleanup_expired()
        
        if key in self.memory:
            entry = self.memory[key]
            entry['access_count'] += 1
            entry['last_accessed'] = datetime.now()
            
            # Recently accessed items को age के basis पर priority दें
            self.memory.move_to_end(key)
            
            return {
                'found': True,
                'value': entry['value'],
                'age': (datetime.now() - entry['timestamp']).seconds,
                'access_count': entry['access_count']
            }
        
        return {'found': False, 'message': f"'{key}' short-term memory में नहीं मिला"}
    
    def _cleanup_expired(self):
        """Expired items को automatically remove करें"""
        current_time = datetime.now()
        expired_keys = []
        
        for key, entry in self.memory.items():
            # Importance के basis पर retention time adjust करें
            adjusted_retention = self.retention_time * entry['importance']
            age = (current_time - entry['timestamp']).seconds
            
            if age > adjusted_retention:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.memory[key]
        
        if expired_keys:
            return f"🗑️ Removed {len(expired_keys)} expired items"
        return None
    
    def get_recent_memories(self, count=10):
        """सबसे recent memories को retrieve करें"""
        self._cleanup_expired()
        items = list(self.memory.items())[-count:]
        return [
            {
                'key': key,
                'value': entry['value'],
                'age_seconds': (datetime.now() - entry['timestamp']).seconds,
                'importance': entry['importance']
            }
            for key, entry in items
        ]
    
    def search(self, query):
        """
        Memory में search करें
        
        Args:
            query: search करने के लिए text
        """
        self._cleanup_expired()
        results = []
        
        for key, entry in self.memory.items():
            if query.lower() in str(entry['value']).lower() or query.lower() in key.lower():
                results.append({
                    'key': key,
                    'value': entry['value'],
                    'relevance': entry['importance'],
                    'age_seconds': (datetime.now() - entry['timestamp']).seconds
                })
        
        return sorted(results, key=lambda x: x['relevance'], reverse=True)
    
    def get_conversation_context(self, turns=5):
        """Recent conversation turns को retrieve करें"""
        self._cleanup_expired()
        conversation_items = [
            (k, v) for k, v in self.memory.items() 
            if k.startswith('turn_') or k.startswith('msg_')
        ]
        return conversation_items[-turns:]
    
    def consolidate(self):
        """
        Frequently accessed items को identify करें
        (ये items long-term memory में transfer हो सकते हैं)
        """
        self._cleanup_expired()
        
        candidates = []
        for key, entry in self.memory.items():
            if entry['access_count'] >= 3 or entry['importance'] >= 0.8:
                candidates.append({
                    'key': key,
                    'value': entry['value'],
                    'access_count': entry['access_count'],
                    'importance': entry['importance']
                })
        
        return {
            'consolidation_candidates': candidates,
            'message': f"Found {len(candidates)} items suitable for long-term storage"
        }
    
    def get_stats(self):
        """Memory की statistics"""
        self._cleanup_expired()
        
        if not self.memory:
            return {'total_items': 0}
        
        ages = [(datetime.now() - entry['timestamp']).seconds for entry in self.memory.values()]
        
        return {
            'total_items': len(self.memory),
            'capacity_used': f"{len(self.memory)}/{self.max_items}",
            'oldest_item_age': max(ages) if ages else 0,
            'newest_item_age': min(ages) if ages else 0,
            'average_age': sum(ages) / len(ages) if ages else 0,
            'total_interactions': self.interaction_count
        }
    
    def clear(self):
        """सभी short-term memories को clear करें"""
        count = len(self.memory)
        self.memory.clear()
        return f"🗑️ Cleared {count} items from short-term memory"


# उदाहरण उपयोग
if __name__ == "__main__":
    print("=" * 60)
    print("💾 SHORT-TERM MEMORY DEMO")
    print("=" * 60)
    
    # Short-term Memory create करें (10 minutes retention)
    stm = ShortTermMemory(retention_time=600, max_items=20)
    
    # Conversation store करें
    print("\n1. Conversation store कर रहे हैं:")
    print(stm.store("turn_1", "User: मुझे pizza चाहिए", importance=0.7))
    print(stm.store("turn_2", "AI: कौन सा pizza लेना है?", importance=0.6))
    print(stm.store("turn_3", "User: Margherita pizza", importance=0.8))
    print(stm.store("user_preference", "Pizza type: Margherita", importance=0.9))
    print(stm.store("delivery_address", "123 Main Street", importance=0.9))
    
    # Recent memories देखें
    print("\n2. Recent Memories:")
    for mem in stm.get_recent_memories(5):
        print(f"   • {mem['key']}: {mem['value']} (Age: {mem['age_seconds']}s)")
    
    # Specific item recall करें
    print("\n3. Recalling specific item:")
    result = stm.recall("user_preference")
    if result['found']:
        print(f"   ✓ Found: {result['value']}")
        print(f"   Age: {result['age']} seconds")
    
    # Search करें
    print("\n4. Searching for 'pizza':")
    search_results = stm.search("pizza")
    for result in search_results:
        print(f"   • {result['key']}: {result['value']}")
    
    # Conversation context
    print("\n5. Recent Conversation Context:")
    context = stm.get_conversation_context(3)
    for key, entry in context:
        print(f"   [{key}] {entry['value']}")
    
    # Statistics
    print("\n6. Memory Statistics:")
    stats = stm.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Consolidation candidates
    print("\n7. Consolidation Analysis:")
    consolidation = stm.consolidate()
    print(f"   {consolidation['message']}")
    for candidate in consolidation['consolidation_candidates']:
        print(f"   • {candidate['key']} (accessed {candidate['access_count']} times)")
