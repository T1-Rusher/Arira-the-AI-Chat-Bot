"""
⚖️ Decision Making Center - AI के लिए Decision Making
Options को evaluate करके best choice select करता है
"""

from datetime import datetime
import json

class DecisionMaker:
    def __init__(self):
        """Decision Maker को initialize करें"""
        self.decisions = []
        self.criteria_weights = {}
        
    def make_decision(self, options, criteria, weights=None, method='weighted_sum'):
        """
        Options में से best decision लेना
        
        Args:
            options: Available options (list of dicts)
            criteria: Decision criteria
            weights: Importance weights for each criterion
            method: Decision making method
        """
        if weights is None:
            weights = {c: 1.0 for c in criteria}
        
        decision = {
            'options': options,
            'criteria': criteria,
            'weights': weights,
            'method': method,
            'timestamp': datetime.now().isoformat()
        }
        
        if method == 'weighted_sum':
            result = self._weighted_sum_method(options, criteria, weights)
        elif method == 'maximin':
            result = self._maximin_method(options, criteria)
        elif method == 'maximax':
            result = self._maximax_method(options, criteria)
        else:
            result = self._weighted_sum_method(options, criteria, weights)
        
        decision['result'] = result
        self.decisions.append(decision)
        
        return result
    
    def _weighted_sum_method(self, options, criteria, weights):
        """Weighted sum of all criteria"""
        scores = []
        
        for option in options:
            total_score = 0
            criterion_scores = {}
            
            for criterion in criteria:
                value = option.get(criterion, 0)
                weight = weights.get(criterion, 1.0)
                score = value * weight
                total_score += score
                criterion_scores[criterion] = score
            
            scores.append({
                'option': option.get('name', 'Unknown'),
                'total_score': total_score,
                'criterion_scores': criterion_scores
            })
        
        scores.sort(key=lambda x: x['total_score'], reverse=True)
        
        return {
            'method': 'weighted_sum',
            'ranked_options': scores,
            'best_option': scores[0] if scores else None
        }
    
    def _maximin_method(self, options, criteria):
        """Maximize the minimum - pessimistic approach"""
        scores = []
        
        for option in options:
            values = [option.get(c, 0) for c in criteria]
            min_value = min(values) if values else 0
            
            scores.append({
                'option': option.get('name', 'Unknown'),
                'min_score': min_value,
                'all_scores': values
            })
        
        scores.sort(key=lambda x: x['min_score'], reverse=True)
        
        return {
            'method': 'maximin',
            'ranked_options': scores,
            'best_option': scores[0] if scores else None
        }
    
    def _maximax_method(self, options, criteria):
        """Maximize the maximum - optimistic approach"""
        scores = []
        
        for option in options:
            values = [option.get(c, 0) for c in criteria]
            max_value = max(values) if values else 0
            
            scores.append({
                'option': option.get('name', 'Unknown'),
                'max_score': max_value,
                'all_scores': values
            })
        
        scores.sort(key=lambda x: x['max_score'], reverse=True)
        
        return {
            'method': 'maximax',
            'ranked_options': scores,
            'best_option': scores[0] if scores else None
        }
    
    def cost_benefit_analysis(self, option, costs, benefits):
        """Cost-Benefit Analysis करना"""
        total_cost = sum(costs.values())
        total_benefit = sum(benefits.values())
        net_benefit = total_benefit - total_cost
        benefit_cost_ratio = total_benefit / total_cost if total_cost > 0 else 0
        
        return {
            'option': option,
            'total_cost': total_cost,
            'total_benefit': total_benefit,
            'net_benefit': net_benefit,
            'benefit_cost_ratio': benefit_cost_ratio,
            'recommendation': 'Accept' if net_benefit > 0 else 'Reject'
        }
    
    def risk_assessment(self, option, risks, probabilities):
        """Risk assessment करना"""
        risk_score = 0
        risk_details = []
        
        for risk, probability in zip(risks, probabilities):
            impact = risk.get('impact', 0.5)
            risk_value = probability * impact
            risk_score += risk_value
            
            risk_details.append({
                'risk': risk.get('name', 'Unknown'),
                'probability': probability,
                'impact': impact,
                'risk_value': risk_value
            })
        
        return {
            'option': option,
            'total_risk_score': risk_score,
            'risk_level': 'High' if risk_score > 0.7 else 'Medium' if risk_score > 0.4 else 'Low',
            'risk_details': risk_details
        }
    
    def multi_criteria_decision(self, options, criteria_scores):
        """Multi-criteria decision analysis"""
        return self.make_decision(options, list(criteria_scores.keys()), criteria_scores)
    
    def get_decision_history(self, limit=10):
        """Recent decisions"""
        return self.decisions[-limit:]
    
    def get_statistics(self):
        """Decision statistics"""
        return {
            'total_decisions': len(self.decisions),
            'methods_used': list(set(d.get('method', 'unknown') for d in self.decisions))
        }


# Example Usage
if __name__ == "__main__":
    print("=" * 60)
    print("⚖️ DECISION MAKING DEMO")
    print("=" * 60)
    
    dm = DecisionMaker()
    
    # Options for buying a laptop
    options = [
        {'name': 'Laptop A', 'price': 8, 'performance': 9, 'battery': 7},
        {'name': 'Laptop B', 'price': 9, 'performance': 7, 'battery': 9},
        {'name': 'Laptop C', 'price': 6, 'performance': 8, 'battery': 8}
    ]
    
    criteria = ['price', 'performance', 'battery']
    weights = {'price': 0.3, 'performance': 0.5, 'battery': 0.2}
    
    # Make decision
    print("\n1. Weighted Sum Decision:")
    result = dm.make_decision(options, criteria, weights)
    print(f"   Best option: {result['best_option']['option']}")
    print(f"   Score: {result['best_option']['total_score']:.2f}")
    
    # Cost-Benefit Analysis
    print("\n2. Cost-Benefit Analysis:")
    cba = dm.cost_benefit_analysis(
        "Project X",
        {'development': 50000, 'marketing': 20000},
        {'revenue': 100000, 'reputation': 30000}
    )
    print(f"   Net benefit: ₹{cba['net_benefit']}")
    print(f"   Recommendation: {cba['recommendation']}")
