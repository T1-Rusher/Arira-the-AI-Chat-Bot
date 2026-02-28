"""
🧮 Math/Logic Processor - AI के लिए Mathematical और Logical Operations
Calculations, equations, और logical operations perform करता है
"""

import math
import re
from datetime import datetime

class MathLogicProcessor:
    def __init__(self):
        """Math/Logic Processor को initialize करें"""
        self.calculation_history = []
        self.variables = {}
        
    def calculate(self, expression):
        """Mathematical expression को evaluate करें"""
        try:
            # Replace variables
            for var, value in self.variables.items():
                expression = expression.replace(var, str(value))
            
            result = eval(expression, {"__builtins__": {}, "math": math})
            
            self.calculation_history.append({
                'expression': expression,
                'result': result,
                'timestamp': datetime.now().isoformat()
            })
            
            return {'success': True, 'result': result, 'expression': expression}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def solve_equation(self, equation, variable='x'):
        """Simple linear equation solve करें"""
        # For demonstration: ax + b = c format
        return {'solution': f"Solving for {variable}", 'steps': []}
    
    def statistics(self, data):
        """Statistical calculations"""
        if not data:
            return None
        
        return {
            'mean': sum(data) / len(data),
            'median': sorted(data)[len(data)//2],
            'max': max(data),
            'min': min(data),
            'sum': sum(data),
            'count': len(data)
        }
    
    def logical_operation(self, operation, *args):
        """Logical operations: AND, OR, NOT, XOR"""
        operations = {
            'AND': lambda a, b: a and b,
            'OR': lambda a, b: a or b,
            'NOT': lambda a: not a,
            'XOR': lambda a, b: (a or b) and not (a and b)
        }
        
        if operation in operations:
            if operation == 'NOT':
                return operations[operation](args[0])
            return operations[operation](args[0], args[1])
        return None
    
    def set_variable(self, name, value):
        """Variable store करें"""
        self.variables[name] = value
        return f"✓ {name} = {value}"
    
    def get_history(self, limit=10):
        """Calculation history"""
        return self.calculation_history[-limit:]

if __name__ == "__main__":
    print("🧮 MATH/LOGIC PROCESSOR DEMO")
    mlp = MathLogicProcessor()
    
    print("\n1. Basic Calculations:")
    print(f"   5 + 3 = {mlp.calculate('5 + 3')['result']}")
    print(f"   10 * 7 = {mlp.calculate('10 * 7')['result']}")
    
    print("\n2. Statistics:")
    data = [10, 20, 30, 40, 50]
    stats = mlp.statistics(data)
    print(f"   Mean: {stats['mean']}")
    print(f"   Median: {stats['median']}")
