"""
🔄 Task Switching System - AI के लिए Multitasking
Multiple tasks के बीच efficiently switch करना
"""

from datetime import datetime
from collections import deque

class TaskSwitching:
    def __init__(self, max_concurrent_tasks=3):
        """Task Switching System को initialize करें"""
        self.max_concurrent = max_concurrent_tasks
        self.active_tasks = {}
        self.task_stack = deque()
        self.switch_history = []
        self.context_saves = {}
        
    def start_task(self, task_id, task_description):
        """नया task start करें"""
        if len(self.active_tasks) >= self.max_concurrent:
            return {'error': 'Max concurrent tasks reached'}
        
        self.active_tasks[task_id] = {
            'description': task_description,
            'started_at': datetime.now(),
            'status': 'active',
            'context': {}
        }
        
        self.task_stack.append(task_id)
        
        return {
            'task_id': task_id,
            'status': 'Task started',
            'active_tasks': len(self.active_tasks)
        }
    
    def switch_task(self, from_task, to_task):
        """एक task से दूसरे में switch करें"""
        # Save context of current task
        if from_task in self.active_tasks:
            self.save_context(from_task)
        
        # Switch to new task
        if to_task in self.active_tasks:
            self.restore_context(to_task)
        
        self.switch_history.append({
            'from': from_task,
            'to': to_task,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'switched_from': from_task,
            'switched_to': to_task,
            'switch_cost': 'Context saved and restored'
        }
    
    def save_context(self, task_id):
        """Task का context save करें"""
        if task_id in self.active_tasks:
            self.context_saves[task_id] = {
                'state': self.active_tasks[task_id].copy(),
                'saved_at': datetime.now()
            }
            return f"✓ Context saved for {task_id}"
        return "Task not found"
    
    def restore_context(self, task_id):
        """Task का context restore करें"""
        if task_id in self.context_saves:
            return {
                'task_id': task_id,
                'context': self.context_saves[task_id]['state'],
                'status': 'Context restored'
            }
        return {'message': 'No saved context'}
    
    def complete_task(self, task_id):
        """Task को complete करें"""
        if task_id in self.active_tasks:
            del self.active_tasks[task_id]
            if task_id in self.context_saves:
                del self.context_saves[task_id]
            
            return {
                'task_id': task_id,
                'status': 'Task completed and removed'
            }
        return {'error': 'Task not found'}
    
    def get_active_tasks(self):
        """सभी active tasks की list"""
        return [
            {'task_id': tid, 'description': task['description']}
            for tid, task in self.active_tasks.items()
        ]
    
    def get_statistics(self):
        """Task switching statistics"""
        return {
            'active_tasks': len(self.active_tasks),
            'max_concurrent': self.max_concurrent,
            'total_switches': len(self.switch_history),
            'contexts_saved': len(self.context_saves)
        }


if __name__ == "__main__":
    print("🔄 TASK SWITCHING DEMO")
    ts = TaskSwitching()
    
    print("\n1. Start tasks:")
    ts.start_task("task1", "Write code")
    ts.start_task("task2", "Review PR")
    print(f"   Active: {len(ts.get_active_tasks())}")
    
    print("\n2. Switch task:")
    result = ts.switch_task("task1", "task2")
    print(f"   Switched to: {result['switched_to']}")
