"""
🔍 Pattern Recognition - AI के लिए Pattern Detection
Data में patterns और trends identify करता है
"""

from datetime import datetime
from collections import Counter

class PatternRecognition:
    def __init__(self):
        """Pattern Recognition को initialize करें"""
        self.detected_patterns = []
        
    def find_sequence_pattern(self, sequence):
        """Sequence में pattern ढूंढना"""
        if len(sequence) < 2:
            return {'pattern': None}
        
        # Check for arithmetic progression
        differences = [sequence[i+1] - sequence[i] for i in range(len(sequence)-1)]
        if len(set(differences)) == 1:
            return {
                'type': 'arithmetic_progression',
                'pattern': f'+{differences[0]}',
                'next_value': sequence[-1] + differences[0]
            }
        
        # Check for geometric progression
        if all(sequence[i] != 0 for i in range(len(sequence)-1)):
            ratios = [sequence[i+1] / sequence[i] for i in range(len(sequence)-1)]
            if all(abs(r - ratios[0]) < 0.01 for r in ratios):
                return {
                    'type': 'geometric_progression',
                    'pattern': f'×{ratios[0]:.2f}',
                    'next_value': sequence[-1] * ratios[0]
                }
        
        return {'type': 'no_clear_pattern'}
    
    def find_frequency_pattern(self, data):
        """Frequency patterns"""
        freq = Counter(data)
        return {
            'most_common': freq.most_common(5),
            'unique_items': len(freq),
            'total_items': len(data)
        }
    
    def detect_trend(self, time_series):
        """Trend detection in time series"""
        if len(time_series) < 2:
            return {'trend': 'insufficient_data'}
        
        increasing = sum(1 for i in range(len(time_series)-1) if time_series[i+1] > time_series[i])
        decreasing = sum(1 for i in range(len(time_series)-1) if time_series[i+1] < time_series[i])
        
        if increasing > len(time_series) * 0.6:
            return {'trend': 'increasing', 'strength': increasing / (len(time_series)-1)}
        elif decreasing > len(time_series) * 0.6:
            return {'trend': 'decreasing', 'strength': decreasing / (len(time_series)-1)}
        else:
            return {'trend': 'stable', 'strength': 0.5}
    
    def find_outliers(self, data):
        """Outliers detect करना"""
        if len(data) < 3:
            return {'outliers': []}
        
        mean = sum(data) / len(data)
        std_dev = (sum((x - mean) ** 2 for x in data) / len(data)) ** 0.5
        
        outliers = [x for x in data if abs(x - mean) > 2 * std_dev]
        
        return {
            'outliers': outliers,
            'count': len(outliers),
            'mean': mean,
            'std_dev': std_dev
        }

if __name__ == "__main__":
    print("🔍 PATTERN RECOGNITION DEMO")
    pr = PatternRecognition()
    
    print("\n1. Sequence Pattern:")
    seq = [2, 4, 6, 8, 10]
    pattern = pr.find_sequence_pattern(seq)
    print(f"   Sequence: {seq}")
    print(f"   Pattern: {pattern.get('pattern', 'None')}")
    
    print("\n2. Trend Detection:")
    series = [10, 12, 15, 18, 22, 25]
    trend = pr.detect_trend(series)
    print(f"   Series: {series}")
    print(f"   Trend: {trend['trend']}")
