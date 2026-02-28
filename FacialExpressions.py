"""
😀 Facial Expressions System - AI के लिए Emotions Display
Face पर emotions को express करना
"""

from datetime import datetime
import json

class FacialExpressions:
    def __init__(self):
        """Facial Expressions System को initialize करें"""
        self.expression_history = []
        self.current_expression = 'neutral'
        self.facial_features = {
            'eyebrows': {'left': 0, 'right': 0},
            'eyes': {'left_openness': 1.0, 'right_openness': 1.0},
            'mouth': {'openness': 0.0, 'corners': 0.0},
            'head': {'tilt': 0, 'nod': 0}
        }
        
        # Pre-defined expressions
        self.expressions = {
            'happy': {
                'eyebrows': {'left': 0.3, 'right': 0.3},
                'eyes': {'left_openness': 0.8, 'right_openness': 0.8},
                'mouth': {'openness': 0.5, 'corners': 0.8},
                'description': 'मुस्कान, आंखें थोड़ी बंद'
            },
            'sad': {
                'eyebrows': {'left': -0.5, 'right': -0.5},
                'eyes': {'left_openness': 0.6, 'right_openness': 0.6},
                'mouth': {'openness': 0.1, 'corners': -0.6},
                'description': 'नीचे की ओर भौहें, मुंह नीचे'
            },
            'angry': {
                'eyebrows': {'left': -0.8, 'right': -0.8},
                'eyes': {'left_openness': 0.9, 'right_openness': 0.9},
                'mouth': {'openness': 0.3, 'corners': -0.4},
                'description': 'भौहें नीचे, तनाव'
            },
            'surprised': {
                'eyebrows': {'left': 0.8, 'right': 0.8},
                'eyes': {'left_openness': 1.0, 'right_openness': 1.0},
                'mouth': {'openness': 0.7, 'corners': 0.0},
                'description': 'भौहें ऊपर, आंखें खुली, मुंह खुला'
            },
            'neutral': {
                'eyebrows': {'left': 0.0, 'right': 0.0},
                'eyes': {'left_openness': 0.8, 'right_openness': 0.8},
                'mouth': {'openness': 0.0, 'corners': 0.0},
                'description': 'आराम की स्थिति'
            },
            'confused': {
                'eyebrows': {'left': 0.4, 'right': -0.2},
                'eyes': {'left_openness': 0.7, 'right_openness': 0.9},
                'mouth': {'openness': 0.2, 'corners': -0.2},
                'description': 'असमान भौहें, हल्का संशय'
            },
            'thinking': {
                'eyebrows': {'left': 0.2, 'right': 0.2},
                'eyes': {'left_openness': 0.6, 'right_openness': 0.6},
                'mouth': {'openness': 0.0, 'corners': -0.1},
                'head': {'tilt': 15},
                'description': 'सिर झुका, सोच रहा'
            }
        }
    
    def set_expression(self, expression_name, intensity=1.0):
        """
        Facial expression set करें
        
        Args:
            expression_name: Expression का नाम
            intensity: Expression की intensity (0.0 to 1.0)
        """
        if expression_name not in self.expressions:
            return {'error': f'Unknown expression: {expression_name}'}
        
        base_expression = self.expressions[expression_name]
        
        # Apply intensity
        for feature, values in base_expression.items():
            if feature != 'description' and isinstance(values, dict):
                for key, value in values.items():
                    if feature in self.facial_features:
                        self.facial_features[feature][key] = value * intensity
        
        self.current_expression = expression_name
        
        expression_data = {
            'expression': expression_name,
            'intensity': intensity,
            'features': self.facial_features.copy(),
            'description': base_expression.get('description', ''),
            'timestamp': datetime.now().isoformat()
        }
        
        self.expression_history.append(expression_data)
        return expression_data
    
    def blend_expressions(self, expression1, expression2, blend_factor=0.5):
        """
        दो expressions को blend करें
        
        Args:
            expression1: पहला expression
            expression2: दूसरा expression
            blend_factor: Blend ratio (0.0 = exp1, 1.0 = exp2)
        """
        if expression1 not in self.expressions or expression2 not in self.expressions:
            return {'error': 'Invalid expressions'}
        
        exp1 = self.expressions[expression1]
        exp2 = self.expressions[expression2]
        
        blended = {}
        
        for feature in exp1:
            if feature != 'description' and isinstance(exp1[feature], dict):
                blended[feature] = {}
                for key in exp1[feature]:
                    val1 = exp1[feature][key]
                    val2 = exp2[feature].get(key, val1)
                    blended[feature][key] = val1 * (1 - blend_factor) + val2 * blend_factor
        
        return {
            'blended_features': blended,
            'expression1': expression1,
            'expression2': expression2,
            'blend_factor': blend_factor
        }
    
    def micro_expression(self, expression_name, duration=0.2):
        """
        Micro-expression (बहुत quick expression)
        
        Args:
            expression_name: Expression
            duration: Duration in seconds
        """
        micro = {
            'type': 'micro_expression',
            'expression': expression_name,
            'duration': duration,
            'intensity': 0.6,  # Micro-expressions are subtle
            'timestamp': datetime.now().isoformat()
        }
        
        self.expression_history.append(micro)
        return micro
    
    def animate_transition(self, from_expression, to_expression, duration=1.0):
        """
        एक expression से दूसरे में smooth transition
        
        Args:
            from_expression: Starting expression
            to_expression: Ending expression
            duration: Transition duration in seconds
        """
        frames = 10  # Number of intermediate frames
        frame_duration = duration / frames
        
        animation = {
            'type': 'transition',
            'from': from_expression,
            'to': to_expression,
            'duration': duration,
            'frames': []
        }
        
        for i in range(frames + 1):
            blend_factor = i / frames
            frame = self.blend_expressions(from_expression, to_expression, blend_factor)
            frame['time'] = i * frame_duration
            animation['frames'].append(frame)
        
        return animation
    
    def eye_contact(self, looking_at='forward'):
        """
        Eye contact या gaze direction
        
        Args:
            looking_at: Direction (forward, left, right, up, down)
        """
        gaze_directions = {
            'forward': {'left': 0, 'right': 0},
            'left': {'left': -30, 'right': -30},
            'right': {'left': 30, 'right': 30},
            'up': {'left': 15, 'right': 15},
            'down': {'left': -15, 'right': -15}
        }
        
        return {
            'gaze_direction': looking_at,
            'eye_angles': gaze_directions.get(looking_at, gaze_directions['forward'])
        }
    
    def blink(self, duration=0.2):
        """Eye blink"""
        blink_action = {
            'type': 'blink',
            'duration': duration,
            'sequence': [
                {'time': 0, 'eyes': {'left_openness': 0.8, 'right_openness': 0.8}},
                {'time': duration/2, 'eyes': {'left_openness': 0.0, 'right_openness': 0.0}},
                {'time': duration, 'eyes': {'left_openness': 0.8, 'right_openness': 0.8}}
            ]
        }
        
        self.expression_history.append(blink_action)
        return blink_action
    
    def lip_sync(self, phoneme, duration=0.1):
        """
        Lip synchronization for speech
        
        Args:
            phoneme: Sound unit being spoken
            duration: Duration of phoneme
        """
        mouth_shapes = {
            'A': {'openness': 0.8, 'corners': 0.0},
            'E': {'openness': 0.4, 'corners': 0.6},
            'I': {'openness': 0.2, 'corners': 0.8},
            'O': {'openness': 0.6, 'corners': -0.2},
            'U': {'openness': 0.3, 'corners': -0.4},
            'M': {'openness': 0.0, 'corners': 0.0},
            'F': {'openness': 0.1, 'corners': 0.0}
        }
        
        shape = mouth_shapes.get(phoneme.upper(), mouth_shapes['A'])
        
        return {
            'phoneme': phoneme,
            'mouth_shape': shape,
            'duration': duration
        }
    
    def express_emotion_intensity(self, base_emotion, intensity_level):
        """
        Emotion की intensity को vary करें
        
        Args:
            base_emotion: Base emotion
            intensity_level: Intensity (0.0 to 2.0)
        """
        return self.set_expression(base_emotion, intensity=intensity_level)
    
    def get_current_expression(self):
        """Current expression state"""
        return {
            'expression': self.current_expression,
            'features': self.facial_features,
            'available_expressions': list(self.expressions.keys())
        }
    
    def get_statistics(self):
        """Expression statistics"""
        if not self.expression_history:
            return {'total_expressions': 0}
        
        expressions = [e.get('expression', 'unknown') for e in self.expression_history if 'expression' in e]
        
        return {
            'total_expressions': len(self.expression_history),
            'expressions_used': dict((e, expressions.count(e)) for e in set(expressions)),
            'current_expression': self.current_expression
        }


# Example Usage
if __name__ == "__main__":
    print("=" * 70)
    print("😀 FACIAL EXPRESSIONS DEMO")
    print("=" * 70)
    
    fe = FacialExpressions()
    
    # Set basic expressions
    print("\n1. Basic Expressions:")
    for emotion in ['happy', 'sad', 'surprised']:
        expr = fe.set_expression(emotion)
        print(f"   {emotion.capitalize()}: {expr['description']}")
    
    # Blend expressions
    print("\n2. Blended Expression:")
    blend = fe.blend_expressions('happy', 'surprised', blend_factor=0.5)
    print(f"   Blending: {blend['expression1']} + {blend['expression2']}")
    print(f"   Factor: {blend['blend_factor']}")
    
    # Micro-expression
    print("\n3. Micro-expression:")
    micro = fe.micro_expression('confused', duration=0.2)
    print(f"   Type: {micro['expression']}")
    print(f"   Duration: {micro['duration']}s")
    
    # Eye contact
    print("\n4. Eye Contact:")
    gaze = fe.eye_contact('left')
    print(f"   Looking: {gaze['gaze_direction']}")
    
    # Blink
    print("\n5. Blink Animation:")
    blink = fe.blink(duration=0.3)
    print(f"   Duration: {blink['duration']}s")
    print(f"   Frames: {len(blink['sequence'])}")
    
    # Lip sync
    print("\n6. Lip Sync:")
    lip = fe.lip_sync('A')
    print(f"   Phoneme: {lip['phoneme']}")
    print(f"   Mouth openness: {lip['mouth_shape']['openness']}")
