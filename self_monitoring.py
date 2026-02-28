"""
📊 Self-Monitoring System - AI के लिए Performance Tracking
अपने performance को monitor और improve करना
"""

from datetime import datetime
from collections import defaultdict

class SelfMonitoring:
    def __init__(self):
        """Self-Monitoring System को initialize करें"""
        self.performance_log = []
        self.metrics = defaultdict(list)
        self.benchmarks = {}
        
    def record_performance(self, task, metrics_dict):
        """Performance को record करें"""
        entry = {
            'task': task,
            'metrics': metrics_dict,
            'timestamp': datetime.now().isoformat()
        }
        
        self.performance_log.append(entry)
        
        # Store individual metrics
        for metric_name, value in metrics_dict.items():
            self.metrics[metric_name].append(value)
        
        return {
            'task': task,
            'metrics_recorded': len(metrics_dict),
            'status': 'Performance recorded'
        }
    
    def set_benchmark(self, metric_name, target_value):
        """Performance benchmark set करें"""
        self.benchmarks[metric_name] = target_value
        return f"✓ Benchmark set: {metric_name} = {target_value}"
    
    def check_performance(self, metric_name):
        """Specific metric की performance check करें"""
        if metric_name not in self.metrics:
            return {'error': 'Metric not found'}
        
        values = self.metrics[metric_name]
        avg_performance = sum(values) / len(values)
        
        result = {
            'metric': metric_name,
            'current_average': avg_performance,
            'total_recordings': len(values)
        }
        
        # Compare with benchmark
        if metric_name in self.benchmarks:
            benchmark = self.benchmarks[metric_name]
            result['benchmark'] = benchmark
            result['meeting_benchmark'] = avg_performance >= benchmark
            result['gap'] = benchmark - avg_performance
        
        return result
    
    def identify_weaknesses(self):
        """Weaknesses identify करें"""
        weaknesses = []
        
        for metric_name, benchmark in self.benchmarks.items():
            if metric_name in self.metrics:
                avg = sum(self.metrics[metric_name]) / len(self.metrics[metric_name])
                if avg < benchmark:
                    weaknesses.append({
                        'metric': metric_name,
                        'current': avg,
                        'target': benchmark,
                        'improvement_needed': benchmark - avg
                    })
        
        return weaknesses
    
    def track_improvement(self, metric_name, window=5):
        """Improvement को track करें"""
        if metric_name not in self.metrics:
            return {'error': 'Metric not found'}
        
        values = self.metrics[metric_name]
        
        if len(values) < window:
            return {'message': 'Insufficient data'}
        
        recent = values[-window:]
        older = values[-2*window:-window] if len(values) >= 2*window else values[:-window]
        
        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older) if older else recent_avg
        
        improvement = recent_avg - older_avg
        
        return {
            'metric': metric_name,
            'recent_average': recent_avg,
            'older_average': older_avg,
            'improvement': improvement,
            'trend': 'improving' if improvement > 0 else 'declining' if improvement < 0 else 'stable'
        }
    
    def get_statistics(self):
        """Overall monitoring statistics"""
        return {
            'total_recordings': len(self.performance_log),
            'metrics_tracked': len(self.metrics),
            'benchmarks_set': len(self.benchmarks)
        }


if __name__ == "__main__":
    print("📊 SELF-MONITORING DEMO")
    sm = SelfMonitoring()
    
    print("\n1. Record performance:")
    sm.record_performance("Task 1", {'accuracy': 0.85, 'speed': 120})
    sm.record_performance("Task 2", {'accuracy': 0.90, 'speed': 110})
    print("   ✓ Performance recorded")
    
    print("\n2. Set benchmarks:")
    sm.set_benchmark('accuracy', 0.88)
    
    print("\n3. Check performance:")
    result = sm.check_performance('accuracy')
    print(f"   Accuracy: {result['current_average']:.2f}")
    print(f"   Meeting benchmark: {result.get('meeting_benchmark', 'N/A')}")
