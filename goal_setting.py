"""
🎯 Goal Setting System - AI के लिए
"""

from datetime import datetime, timedelta

class GoalStatus:
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ON_HOLD = "on_hold"

class GoalPriority:
    LOW = 1; MEDIUM = 2; HIGH = 3; CRITICAL = 4

class Goal:
    def __init__(self, goal_id, description, priority=GoalPriority.MEDIUM):
        self.id = goal_id
        self.description = description
        self.priority = priority
        self.status = GoalStatus.NOT_STARTED
        self.created_at = datetime.now()
        self.deadline = None
        self.progress = 0.0
        self.sub_goals = []
        self.success_criteria = []
        self.obstacles = []

    def to_dict(self):
        return {
            'id': self.id, 'description': self.description,
            'priority': self.priority, 'status': self.status,
            'progress': self.progress,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'sub_goals': [sg.to_dict() for sg in self.sub_goals],
            'created_at': self.created_at.isoformat()
        }

class GoalSetting:
    def __init__(self):
        self.goals = {}
        self.goal_counter = 0

    def set_goal(self, description, priority=GoalPriority.MEDIUM, deadline=None):
        self.goal_counter += 1
        goal_id = f"goal_{self.goal_counter}"
        goal = Goal(goal_id, description, priority)
        if deadline:
            if isinstance(deadline, str):
                if 'day' in deadline:
                    goal.deadline = datetime.now() + timedelta(days=int(deadline.split()[0]))
                elif 'week' in deadline:
                    goal.deadline = datetime.now() + timedelta(weeks=int(deadline.split()[0]))
        self.goals[goal_id] = goal
        return {'goal_id': goal_id, 'description': description,
                'priority': priority, 'status': 'Goal set successfully',
                'deadline': goal.deadline.isoformat() if goal.deadline else None}

    def add_sub_goal(self, parent_id, description, priority=GoalPriority.MEDIUM):
        if parent_id not in self.goals:
            return {'error': 'Parent goal not found'}
        self.goal_counter += 1
        sub_id = f"goal_{self.goal_counter}"
        sub = Goal(sub_id, description, priority)
        self.goals[parent_id].sub_goals.append(sub)
        self.goals[sub_id] = sub
        return {'sub_goal_id': sub_id, 'parent_goal_id': parent_id, 'description': description}

    def update_progress(self, goal_id, progress_value):
        if goal_id not in self.goals: return {'error': 'Goal not found'}
        goal = self.goals[goal_id]
        goal.progress = max(0.0, min(1.0, progress_value))
        if goal.progress == 0.0: goal.status = GoalStatus.NOT_STARTED
        elif goal.progress < 1.0: goal.status = GoalStatus.IN_PROGRESS
        else: goal.status = GoalStatus.COMPLETED
        return {'goal_id': goal_id, 'progress': goal.progress * 100, 'status': goal.status}

    def complete_goal(self, goal_id):
        if goal_id not in self.goals: return {'error': 'Goal not found'}
        goal = self.goals[goal_id]
        goal.status = GoalStatus.COMPLETED
        goal.progress = 1.0
        return {'goal_id': goal_id, 'status': 'completed',
                'completed_at': datetime.now().isoformat()}

    def get_all_goals(self):
        return [g.to_dict() for g in self.goals.values() if '_' not in g.id[5:] or True]

    def get_active_goals(self):
        return [g.to_dict() for g in self.goals.values()
                if g.status in [GoalStatus.IN_PROGRESS, GoalStatus.NOT_STARTED]]

    def get_goal_status(self, goal_id):
        if goal_id not in self.goals: return {'error': 'Goal not found'}
        goal = self.goals[goal_id]
        return {'goal_id': goal_id, 'description': goal.description,
                'status': goal.status, 'progress': goal.progress * 100,
                'priority': goal.priority,
                'deadline': goal.deadline.isoformat() if goal.deadline else None,
                'sub_goals': len(goal.sub_goals)}

    def get_statistics(self):
        if not self.goals: return {'total_goals': 0}
        goals_list = list(self.goals.values())
        completed = sum(1 for g in goals_list if g.status == GoalStatus.COMPLETED)
        in_progress = sum(1 for g in goals_list if g.status == GoalStatus.IN_PROGRESS)
        avg_progress = sum(g.progress for g in goals_list) / len(goals_list)
        return {'total_goals': len(goals_list), 'completed': completed,
                'in_progress': in_progress,
                'completion_rate': (completed / len(goals_list)) * 100,
                'average_progress': avg_progress * 100}
