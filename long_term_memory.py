"""
🗄️ Long-term Memory System - AI के लिए
Permanent knowledge storage के लिए
Organized categories और efficient retrieval के साथ
"""

import json
import pickle
from datetime import datetime
from collections import defaultdict
import os

class LongTermMemory:
    def __init__(self, storage_path="long_term_memory.pkl"):
        """
        Long-term Memory को initialize करें
        
        Args:
            storage_path: File path जहाँ memory persist होगी
        """
        self.storage_path = storage_path
        self.knowledge_base = defaultdict(dict)
        self.categories = set()
        self.metadata = {
            'created': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'total_entries': 0
        }
        
        # पहले से saved memory load करें
        self.load()
    
    def store(self, key, value, category="general", tags=None, metadata=None):
        """
        Long-term memory में permanently store करें
        
        Args:
            key: unique identifier
            value: knowledge/information
            category: knowledge का category (e.g., "facts", "preferences", "skills")
            tags: search के लिए tags (list)
            metadata: additional information (dict)
        """
        if tags is None:
            tags = []
        if metadata is None:
            metadata = {}
        
        entry = {
            'value': value,
            'category': category,
            'tags': tags,
            'stored_at': datetime.now().isoformat(),
            'access_count': 0,
            'last_accessed': None,
            'metadata': metadata
        }
        
        self.knowledge_base[category][key] = entry
        self.categories.add(category)
        self.metadata['total_entries'] += 1
        self.metadata['last_updated'] = datetime.now().isoformat()
        
        self.save()
        return f"✓ Permanently stored in long-term memory: {key} (Category: {category})"
    
    def retrieve(self, key, category=None):
        """
        Long-term memory से retrieve करें
        
        Args:
            key: identifier
            category: specific category में search करें (optional)
        """
        # Specific category में search करें
        if category and category in self.knowledge_base:
            if key in self.knowledge_base[category]:
                entry = self.knowledge_base[category][key]
                entry['access_count'] += 1
                entry['last_accessed'] = datetime.now().isoformat()
                self.save()
                return {
                    'found': True,
                    'value': entry['value'],
                    'category': category,
                    'tags': entry['tags'],
                    'stored_at': entry['stored_at']
                }
        
        # सभी categories में search करें
        for cat, items in self.knowledge_base.items():
            if key in items:
                entry = items[key]
                entry['access_count'] += 1
                entry['last_accessed'] = datetime.now().isoformat()
                self.save()
                return {
                    'found': True,
                    'value': entry['value'],
                    'category': cat,
                    'tags': entry['tags'],
                    'stored_at': entry['stored_at']
                }
        
        return {'found': False, 'message': f"'{key}' long-term memory में नहीं मिला"}
    
    def search_by_tag(self, tag):
        """Tag के basis पर search करें"""
        results = []
        
        for category, items in self.knowledge_base.items():
            for key, entry in items.items():
                if tag in entry['tags']:
                    results.append({
                        'key': key,
                        'value': entry['value'],
                        'category': category,
                        'tags': entry['tags']
                    })
        
        return results
    
    def search_by_text(self, query):
        """Text content में search करें"""
        results = []
        query_lower = query.lower()
        
        for category, items in self.knowledge_base.items():
            for key, entry in items.items():
                # Key, value, और tags में search करें
                searchable_text = f"{key} {str(entry['value'])} {' '.join(entry['tags'])}".lower()
                if query_lower in searchable_text:
                    results.append({
                        'key': key,
                        'value': entry['value'],
                        'category': category,
                        'tags': entry['tags'],
                        'access_count': entry['access_count']
                    })
        
        # Access count के basis पर sort करें
        return sorted(results, key=lambda x: x['access_count'], reverse=True)
    
    def get_category(self, category):
        """Specific category की सभी entries"""
        if category in self.knowledge_base:
            return dict(self.knowledge_base[category])
        return {}
    
    def get_all_categories(self):
        """सभी available categories"""
        return list(self.categories)
    
    def get_frequently_accessed(self, top_n=10):
        """सबसे ज्यादा access की गई entries"""
        all_entries = []
        
        for category, items in self.knowledge_base.items():
            for key, entry in items.items():
                all_entries.append({
                    'key': key,
                    'value': entry['value'],
                    'category': category,
                    'access_count': entry['access_count']
                })
        
        return sorted(all_entries, key=lambda x: x['access_count'], reverse=True)[:top_n]
    
    def update(self, key, value=None, category=None, new_tags=None):
        """Existing entry को update करें"""
        found = False
        target_category = category
        
        # अगर category नहीं दी गई, तो key को ढूंढें
        if not target_category:
            for cat, items in self.knowledge_base.items():
                if key in items:
                    target_category = cat
                    found = True
                    break
        else:
            found = key in self.knowledge_base.get(target_category, {})
        
        if not found:
            return f"❌ '{key}' नहीं मिला"
        
        entry = self.knowledge_base[target_category][key]
        
        if value is not None:
            entry['value'] = value
        if new_tags is not None:
            entry['tags'] = new_tags
        
        entry['last_accessed'] = datetime.now().isoformat()
        self.metadata['last_updated'] = datetime.now().isoformat()
        
        self.save()
        return f"✓ Updated: {key}"
    
    def delete(self, key, category=None):
        """Entry को delete करें"""
        if category and category in self.knowledge_base:
            if key in self.knowledge_base[category]:
                del self.knowledge_base[category][key]
                self.metadata['total_entries'] -= 1
                self.save()
                return f"✓ Deleted: {key} from {category}"
        
        # सभी categories में search करें
        for cat, items in self.knowledge_base.items():
            if key in items:
                del items[key]
                self.metadata['total_entries'] -= 1
                self.save()
                return f"✓ Deleted: {key} from {cat}"
        
        return f"❌ '{key}' नहीं मिला"
    
    def save(self):
        """Memory को disk पर save करें"""
        data = {
            'knowledge_base': dict(self.knowledge_base),
            'categories': list(self.categories),
            'metadata': self.metadata
        }
        
        try:
            with open(self.storage_path, 'wb') as f:
                pickle.dump(data, f)
            return True
        except Exception as e:
            print(f"❌ Save error: {e}")
            return False
    
    def load(self):
        """Disk से memory load करें"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'rb') as f:
                    data = pickle.load(f)
                
                self.knowledge_base = defaultdict(dict, data['knowledge_base'])
                self.categories = set(data['categories'])
                self.metadata = data['metadata']
                
                return True
            except Exception as e:
                print(f"❌ Load error: {e}")
                return False
        return False
    
    def export_to_json(self, filepath="long_term_memory.json"):
        """Memory को JSON format में export करें"""
        data = {
            'knowledge_base': dict(self.knowledge_base),
            'categories': list(self.categories),
            'metadata': self.metadata
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return f"✓ Exported to {filepath}"
    
    def get_statistics(self):
        """Memory की detailed statistics"""
        total_entries = 0
        category_counts = {}
        
        for category, items in self.knowledge_base.items():
            count = len(items)
            total_entries += count
            category_counts[category] = count
        
        return {
            'total_entries': total_entries,
            'total_categories': len(self.categories),
            'category_breakdown': category_counts,
            'created': self.metadata['created'],
            'last_updated': self.metadata['last_updated']
        }


# उदाहरण उपयोग
if __name__ == "__main__":
    print("=" * 60)
    print("🗄️ LONG-TERM MEMORY DEMO")
    print("=" * 60)
    
    # Long-term Memory create करें
    ltm = LongTermMemory(storage_path="demo_ltm.pkl")
    
    # विभिन्न categories में knowledge store करें
    print("\n1. Knowledge store कर रहे हैं:")
    print(ltm.store("user_name", "Rajesh Kumar", category="user_profile", tags=["user", "identity"]))
    print(ltm.store("favorite_food", "Pizza", category="preferences", tags=["food", "likes"]))
    print(ltm.store("python_skill", "Advanced", category="skills", tags=["programming", "python"]))
    print(ltm.store("birthday", "15 August", category="user_profile", tags=["date", "personal"]))
    print(ltm.store("favorite_color", "Blue", category="preferences", tags=["color", "likes"]))
    
    # Retrieve करें
    print("\n2. Information retrieve कर रहे हैं:")
    result = ltm.retrieve("user_name")
    if result['found']:
        print(f"   ✓ {result['value']} (Category: {result['category']})")
    
    # Tag से search करें
    print("\n3. Tag 'likes' से search:")
    tag_results = ltm.search_by_tag("likes")
    for result in tag_results:
        print(f"   • {result['key']}: {result['value']}")
    
    # Text search
    print("\n4. 'python' text search:")
    search_results = ltm.search_by_text("python")
    for result in search_results:
        print(f"   • {result['key']}: {result['value']}")
    
    # Categories देखें
    print("\n5. Available Categories:")
    for cat in ltm.get_all_categories():
        print(f"   • {cat}")
    
    # Frequently accessed
    print("\n6. Frequently Accessed Entries:")
    for entry in ltm.get_frequently_accessed(3):
        print(f"   • {entry['key']}: {entry['value']} (accessed {entry['access_count']} times)")
    
    # Statistics
    print("\n7. Memory Statistics:")
    stats = ltm.get_statistics()
    print(f"   Total Entries: {stats['total_entries']}")
    print(f"   Categories: {stats['total_categories']}")
    print(f"   Category Breakdown:")
    for cat, count in stats['category_breakdown'].items():
        print(f"      - {cat}: {count} entries")
    
    # Export
    print("\n8. Exporting to JSON:")
    print(ltm.export_to_json("demo_ltm_export.json"))
    
    # Cleanup demo files
    if os.path.exists("demo_ltm.pkl"):
        os.remove("demo_ltm.pkl")
    if os.path.exists("demo_ltm_export.json"):
        os.remove("demo_ltm_export.json")
