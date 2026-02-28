"""
⏰ Time Perception - AI के लिए Temporal Reasoning
Time-related reasoning और scheduling
"""

from datetime import datetime, timedelta
import calendar

class TimePerception:
    def __init__(self):
        """Time Perception को initialize करें"""
        self.events = []
        
    def parse_temporal_expression(self, expression):
        """Temporal expressions को parse करना"""
        now = datetime.now()
        
        if 'today' in expression.lower() or 'आज' in expression:
            return {'date': now.date(), 'type': 'today'}
        elif 'tomorrow' in expression.lower() or 'कल' in expression:
            return {'date': (now + timedelta(days=1)).date(), 'type': 'tomorrow'}
        elif 'yesterday' in expression.lower() or 'बीता कल' in expression:
            return {'date': (now - timedelta(days=1)).date(), 'type': 'yesterday'}
        elif 'next week' in expression.lower():
            return {'date': (now + timedelta(weeks=1)).date(), 'type': 'next_week'}
        
        return {'date': None, 'type': 'unknown'}
    
    def calculate_duration(self, start_time, end_time):
        """Duration calculate करना"""
        duration = end_time - start_time
        
        return {
            'total_seconds': duration.total_seconds(),
            'hours': duration.total_seconds() / 3600,
            'minutes': duration.total_seconds() / 60,
            'days': duration.days
        }
    
    def is_business_day(self, date):
        """Business day check करना"""
        return date.weekday() < 5  # Monday=0, Sunday=6
    
    def get_relative_time(self, timestamp):
        """Relative time expression"""
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days == 0:
            if diff.seconds < 60:
                return 'just now'
            elif diff.seconds < 3600:
                return f'{diff.seconds // 60} minutes ago'
            else:
                return f'{diff.seconds // 3600} hours ago'
        elif diff.days == 1:
            return 'yesterday'
        elif diff.days < 7:
            return f'{diff.days} days ago'
        else:
            return timestamp.strftime('%Y-%m-%d')
    
    def schedule_event(self, event_name, start_time, duration_minutes):
        """Event schedule करना"""
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        event = {
            'name': event_name,
            'start': start_time,
            'end': end_time,
            'duration_minutes': duration_minutes
        }
        
        self.events.append(event)
        return event

if __name__ == "__main__":
    print("⏰ TIME PERCEPTION DEMO")
    tp = TimePerception()
    
    print("\n1. Temporal Expression:")
    result = tp.parse_temporal_expression("What about tomorrow?")
    print(f"   Expression: 'tomorrow'")
    print(f"   Date: {result['date']}")
    
    print("\n2. Relative Time:")
    past = datetime.now() - timedelta(hours=2)
    rel_time = tp.get_relative_time(past)
    print(f"   Relative: {rel_time}")
