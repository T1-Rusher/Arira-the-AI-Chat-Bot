"""
📋 Planning System - Step-by-step Planning
"""

from datetime import datetime, timedelta

class Task:
    def __init__(self, task_id, description, duration_minutes=30):
        self.id = task_id
        self.description = description
        self.duration = duration_minutes
        self.dependencies = []
        self.status = 'pending'
        self.priority = 1

class Plan:
    def __init__(self, plan_id, goal):
        self.id = plan_id
        self.goal = goal
        self.tasks = []
        self.created_at = datetime.now()
        self.estimated_duration = 0

class PlanningSystem:
    def __init__(self):
        self.plans = {}
        self.plan_counter = 0

    def create_plan(self, goal_description):
        self.plan_counter += 1
        plan_id = f"plan_{self.plan_counter}"
        self.plans[plan_id] = Plan(plan_id, goal_description)
        return {'plan_id': plan_id, 'goal': goal_description, 'status': 'Plan created'}

    def add_task(self, plan_id, task_description, duration_minutes=30, dependencies=None):
        if plan_id not in self.plans: return {'error': 'Plan not found'}
        task_id = f"{plan_id}_task_{len(self.plans[plan_id].tasks) + 1}"
        task = Task(task_id, task_description, duration_minutes)
        if dependencies: task.dependencies = dependencies
        self.plans[plan_id].tasks.append(task)
        self.plans[plan_id].estimated_duration += duration_minutes
        return {'task_id': task_id, 'description': task_description, 'duration': duration_minutes}

    def decompose_goal(self, goal, complexity='medium'):
        plan = self.create_plan(goal)
        plan_id = plan['plan_id']
        task_templates = {
            'simple': [f"Research: {goal}", f"Execute: {goal}", f"Review: {goal}"],
            'medium': [f"Research: {goal}", f"Plan details: {goal}", f"Gather resources: {goal}",
                       f"Execute: {goal}", f"Review & refine: {goal}"],
            'complex': [f"Research: {goal}", f"Define requirements: {goal}", f"Plan: {goal}",
                        f"Gather resources: {goal}", f"Execute phase 1: {goal}",
                        f"Execute phase 2: {goal}", f"Test/validate: {goal}", f"Final review: {goal}"]
        }
        tasks = task_templates.get(complexity, task_templates['medium'])
        for i, t in enumerate(tasks):
            self.add_task(plan_id, t, duration_minutes=30*(i+1))
        return {'plan_id': plan_id, 'goal': goal,
                'tasks_created': len(tasks),
                'estimated_time': self.plans[plan_id].estimated_duration}

    def create_timeline(self, plan_id, start_time=None):
        if plan_id not in self.plans: return {'error': 'Plan not found'}
        if start_time is None: start_time = datetime.now()
        plan = self.plans[plan_id]
        timeline = []
        current = start_time
        for task in plan.tasks:
            timeline.append({'task': task.description,
                             'start': current.isoformat(),
                             'end': (current + timedelta(minutes=task.duration)).isoformat(),
                             'duration_minutes': task.duration})
            current += timedelta(minutes=task.duration)
        return {'plan_id': plan_id, 'timeline': timeline,
                'total_duration_minutes': plan.estimated_duration}

    def get_next_task(self, plan_id):
        if plan_id not in self.plans: return {'error': 'Plan not found'}
        for task in self.plans[plan_id].tasks:
            if task.status == 'pending':
                return {'task_id': task.id, 'description': task.description, 'duration': task.duration}
        return {'message': 'No pending tasks'}

    def complete_task(self, plan_id, task_id):
        if plan_id not in self.plans: return {'error': 'Plan not found'}
        for task in self.plans[plan_id].tasks:
            if task.id == task_id:
                task.status = 'completed'
                progress = self._calc_progress(plan_id)
                return {'task_id': task_id, 'status': 'completed', 'plan_progress': progress}
        return {'error': 'Task not found'}

    def _calc_progress(self, plan_id):
        plan = self.plans[plan_id]
        if not plan.tasks: return 0
        done = sum(1 for t in plan.tasks if t.status == 'completed')
        return (done / len(plan.tasks)) * 100

    def get_plan_status(self, plan_id):
        if plan_id not in self.plans: return {'error': 'Plan not found'}
        plan = self.plans[plan_id]
        return {'plan_id': plan_id, 'goal': plan.goal,
                'total_tasks': len(plan.tasks),
                'completed_tasks': sum(1 for t in plan.tasks if t.status == 'completed'),
                'progress': self._calc_progress(plan_id),
                'estimated_duration': plan.estimated_duration}

    def get_all_plans(self):
        return [self.get_plan_status(pid) for pid in self.plans]

    def get_statistics(self):
        if not self.plans: return {'total_plans': 0}
        total_tasks = sum(len(p.tasks) for p in self.plans.values())
        completed = sum(sum(1 for t in p.tasks if t.status=='completed') for p in self.plans.values())
        return {'total_plans': len(self.plans), 'total_tasks': total_tasks,
                'completed_tasks': completed,
                'completion_rate': (completed/total_tasks*100) if total_tasks else 0}
