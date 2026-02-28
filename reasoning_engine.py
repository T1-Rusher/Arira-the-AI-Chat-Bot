"""
🤔 Reasoning Engine - AI के लिए Logical Thinking
"""

from datetime import datetime
from collections import defaultdict

class ReasoningEngine:
    def __init__(self):
        self.knowledge_base = {}
        self.rules = []
        self.reasoning_history = []

    def add_rule(self, rule_id, condition, conclusion, confidence=1.0):
        self.rules.append({
            'id': rule_id, 'condition': condition, 'conclusion': conclusion,
            'confidence': confidence, 'created_at': datetime.now().isoformat(), 'usage_count': 0
        })
        return f"✓ Rule added: {rule_id}"

    def add_fact(self, fact_id, statement, confidence=1.0):
        self.knowledge_base[fact_id] = {
            'statement': statement, 'confidence': confidence,
            'added_at': datetime.now().isoformat()
        }
        return f"✓ Fact added: {fact_id}"

    def deductive_reasoning(self, premises):
        conclusions = []
        for rule in self.rules:
            if self._check_condition(rule['condition'], premises):
                conclusions.append({
                    'conclusion': rule['conclusion'],
                    'confidence': rule['confidence'],
                    'rule_used': rule['id'],
                    'reasoning_type': 'deductive',
                    'premises': premises
                })
                rule['usage_count'] += 1
                self._log('deductive', premises, rule['conclusion'])
        return conclusions

    def inductive_reasoning(self, observations):
        patterns = self._find_patterns(observations)
        generalizations = []
        for pattern in patterns:
            confidence = min(0.95, pattern['occurrences'] / len(observations))
            generalizations.append({
                'pattern': pattern['description'],
                'confidence': confidence,
                'reasoning_type': 'inductive'
            })
            self._log('inductive', observations, pattern['description'])
        return generalizations

    def abductive_reasoning(self, observation, possible_explanations):
        ranked = []
        for exp in possible_explanations:
            score = 0.5
            if 'evidence' in exp: score += len(exp['evidence']) * 0.1
            if 'prior_probability' in exp: score *= exp['prior_probability']
            ranked.append({'explanation': exp['hypothesis'],
                           'plausibility_score': min(1.0, score),
                           'reasoning_type': 'abductive'})
        ranked.sort(key=lambda x: x['plausibility_score'], reverse=True)
        if ranked: self._log('abductive', observation, ranked[0]['explanation'])
        return ranked

    def problem_decomposition(self, problem, max_depth=3):
        decomposition = {'main_problem': problem, 'sub_problems': [], 'reasoning_type': 'decomposition'}
        sub_problems = [
            {'problem': f"पहले समझें: {problem}", 'depth': 1},
            {'problem': f"resources इकट्ठा करें: {problem}", 'depth': 1},
            {'problem': f"execute करें: {problem}", 'depth': 1},
            {'problem': f"review करें: {problem}", 'depth': 1}
        ]
        decomposition['sub_problems'] = sub_problems[:max_depth]
        decomposition['solution_strategy'] = {
            'steps': [sp['problem'] for sp in decomposition['sub_problems']],
            'order': 'sequential'
        }
        self._log('decomposition', problem, decomposition)
        return decomposition

    def _check_condition(self, condition, premises):
        return isinstance(condition, str) and condition.lower() in str(premises).lower()

    def _find_patterns(self, observations):
        if len(observations) >= 2:
            return [{'description': f"{len(observations)} observations में pattern मिला",
                     'occurrences': len(observations)}]
        return []

    def _log(self, reasoning_type, input_data, output):
        self.reasoning_history.append({
            'type': reasoning_type,
            'input': str(input_data)[:100],
            'output': str(output)[:100],
            'timestamp': datetime.now().isoformat()
        })

    def get_reasoning_history(self, limit=10):
        return self.reasoning_history[-limit:]

    def get_statistics(self):
        type_counts = defaultdict(int)
        for entry in self.reasoning_history:
            type_counts[entry['type']] += 1
        return {
            'total_reasoning_steps': len(self.reasoning_history),
            'reasoning_types_used': dict(type_counts),
            'total_rules': len(self.rules),
            'total_facts': len(self.knowledge_base)
        }
