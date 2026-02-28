"""
🗣️ Speech Generation System - AI के लिए Text-to-Speech
Text को natural speech में convert करता है
"""

from datetime import datetime
import json
import re

class SpeechGenerator:
    def __init__(self):
        """Speech Generator को initialize करें"""
        self.speech_history = []
        self.voice_settings = {
            'voice': 'neutral',
            'speed': 1.0,
            'pitch': 1.0,
            'volume': 0.8,
            'language': 'hi-IN'  # Hindi India
        }
        self.emotion_modifiers = {
            'happy': {'pitch': 1.2, 'speed': 1.1},
            'sad': {'pitch': 0.8, 'speed': 0.9},
            'angry': {'pitch': 1.3, 'speed': 1.2},
            'calm': {'pitch': 0.9, 'speed': 0.95},
            'excited': {'pitch': 1.4, 'speed': 1.3}
        }
        
    def generate_speech(self, text, emotion='neutral', voice_params=None):
        """
        Text को speech में convert करें
        
        Args:
            text: बोलने के लिए text
            emotion: कौन सा emotion express करना है
            voice_params: Custom voice parameters
        """
        if voice_params is None:
            voice_params = self.voice_settings.copy()
        
        # Emotion-based modifications
        if emotion in self.emotion_modifiers:
            for param, value in self.emotion_modifiers[emotion].items():
                voice_params[param] = value
        
        # Text preprocessing
        processed_text = self._preprocess_text(text)
        
        # Prosody (rhythm और intonation) generate करें
        prosody = self._generate_prosody(processed_text, emotion)
        
        # Speech synthesis simulation
        speech_output = {
            'text': text,
            'processed_text': processed_text,
            'emotion': emotion,
            'voice_params': voice_params,
            'prosody': prosody,
            'duration_estimate': len(text.split()) * 0.4,  # ~0.4 sec per word
            'timestamp': datetime.now().isoformat(),
            'status': 'generated'
        }
        
        self.speech_history.append(speech_output)
        
        return speech_output
    
    def _preprocess_text(self, text):
        """Text को speech के लिए prepare करना"""
        # Numbers को words में convert करें
        processed = self._numbers_to_words(text)
        
        # Abbreviations expand करें
        processed = self._expand_abbreviations(processed)
        
        # Punctuation के लिए pauses add करें
        processed = self._add_pauses(processed)
        
        return processed
    
    def _numbers_to_words(self, text):
        """Numbers को words में convert करें"""
        # Simple implementation
        number_words = {
            '0': 'शून्य', '1': 'एक', '2': 'दो', '3': 'तीन',
            '4': 'चार', '5': 'पाँच', '6': 'छह', '7': 'सात',
            '8': 'आठ', '9': 'नौ', '10': 'दस'
        }
        
        result = text
        for num, word in number_words.items():
            result = result.replace(num, word)
        
        return result
    
    def _expand_abbreviations(self, text):
        """Common abbreviations को expand करें"""
        abbreviations = {
            'Dr.': 'Doctor',
            'Mr.': 'Mister',
            'Mrs.': 'Misses',
            'etc.': 'et cetera',
            'e.g.': 'for example',
            'i.e.': 'that is'
        }
        
        result = text
        for abbr, full in abbreviations.items():
            result = result.replace(abbr, full)
        
        return result
    
    def _add_pauses(self, text):
        """Punctuation के basis पर pauses add करें"""
        # Comma = short pause
        text = text.replace(',', ' <pause:short> ')
        # Period = medium pause
        text = text.replace('.', ' <pause:medium> ')
        # Question/Exclamation = long pause
        text = text.replace('?', ' <pause:long> ')
        text = text.replace('!', ' <pause:long> ')
        
        return text
    
    def _generate_prosody(self, text, emotion):
        """Prosody (intonation pattern) generate करें"""
        words = text.split()
        
        prosody = {
            'intonation_pattern': [],
            'stress_points': [],
            'pause_locations': []
        }
        
        for i, word in enumerate(words):
            # Stress important words
            if len(word) > 6 or word.isupper():
                prosody['stress_points'].append(i)
            
            # Intonation (rising या falling)
            if '?' in word:
                prosody['intonation_pattern'].append('rising')
            elif '!' in word:
                prosody['intonation_pattern'].append('emphatic')
            else:
                prosody['intonation_pattern'].append('neutral')
            
            # Pause locations
            if '<pause' in word:
                prosody['pause_locations'].append(i)
        
        return prosody
    
    def speak_with_emotion(self, text, emotion):
        """Specific emotion के साथ बोलना"""
        return self.generate_speech(text, emotion=emotion)
    
    def change_voice_settings(self, **kwargs):
        """Voice settings को modify करें"""
        for key, value in kwargs.items():
            if key in self.voice_settings:
                self.voice_settings[key] = value
        
        return f"✓ Voice settings updated: {kwargs}"
    
    def synthesize_phonemes(self, text):
        """Text को phonemes (sound units) में break करें"""
        # Simplified phoneme breakdown
        phonemes = []
        
        for char in text.lower():
            if char.isalpha():
                phonemes.append(f"/{char}/")
        
        return {
            'text': text,
            'phonemes': phonemes,
            'phoneme_count': len(phonemes)
        }
    
    def generate_ssml(self, text, emotion='neutral'):
        """
        SSML (Speech Synthesis Markup Language) generate करें
        Standard format for TTS systems
        """
        voice_params = self.voice_settings.copy()
        
        if emotion in self.emotion_modifiers:
            for param, value in self.emotion_modifiers[emotion].items():
                voice_params[param] = value
        
        ssml = f"""<speak version="1.0" xml:lang="{voice_params['language']}">
    <prosody rate="{voice_params['speed']}" pitch="{voice_params['pitch']}" volume="{voice_params['volume']}">
        <emotion name="{emotion}">
            {text}
        </emotion>
    </prosody>
</speak>"""
        
        return ssml
    
    def multilingual_speech(self, text, target_language):
        """Multi-language support"""
        language_codes = {
            'hindi': 'hi-IN',
            'english': 'en-US',
            'spanish': 'es-ES',
            'french': 'fr-FR',
            'german': 'de-DE'
        }
        
        old_lang = self.voice_settings['language']
        self.voice_settings['language'] = language_codes.get(target_language, 'en-US')
        
        speech = self.generate_speech(text)
        
        # Restore original language
        self.voice_settings['language'] = old_lang
        
        return speech
    
    def get_speech_history(self, limit=10):
        """Recent speech history"""
        return self.speech_history[-limit:]
    
    def estimate_duration(self, text):
        """Speech की estimated duration calculate करें"""
        word_count = len(text.split())
        avg_words_per_minute = 150 / self.voice_settings['speed']
        
        duration_minutes = word_count / avg_words_per_minute
        
        return {
            'text': text,
            'word_count': word_count,
            'estimated_duration_seconds': duration_minutes * 60,
            'estimated_duration_readable': f"{int(duration_minutes)} min {int((duration_minutes % 1) * 60)} sec"
        }
    
    def get_statistics(self):
        """Speech generation statistics"""
        if not self.speech_history:
            return {'total_speeches': 0}
        
        total_words = sum(len(s['text'].split()) for s in self.speech_history)
        emotions_used = [s['emotion'] for s in self.speech_history]
        
        return {
            'total_speeches': len(self.speech_history),
            'total_words_spoken': total_words,
            'emotions_used': dict((e, emotions_used.count(e)) for e in set(emotions_used)),
            'average_speech_length': total_words / len(self.speech_history)
        }


# Example Usage
if __name__ == "__main__":
    print("=" * 70)
    print("🗣️ SPEECH GENERATION DEMO")
    print("=" * 70)
    
    sg = SpeechGenerator()
    
    # Basic speech generation
    print("\n1. Basic Speech Generation:")
    speech = sg.generate_speech("नमस्ते! मैं एक AI assistant हूं। आपकी कैसे मदद कर सकता हूं?")
    print(f"   Text: {speech['text']}")
    print(f"   Duration: {speech['duration_estimate']:.1f} seconds")
    print(f"   Status: {speech['status']}")
    
    # Emotion-based speech
    print("\n2. Emotion-based Speech:")
    emotions = ['happy', 'sad', 'excited']
    for emotion in emotions:
        speech = sg.speak_with_emotion(f"यह {emotion} emotion के साथ बोला जा रहा है", emotion)
        print(f"   {emotion.capitalize()}: Pitch={speech['voice_params']['pitch']}, Speed={speech['voice_params']['speed']}")
    
    # SSML generation
    print("\n3. SSML Generation:")
    ssml = sg.generate_ssml("यह SSML format में है", emotion='calm')
    print(f"   SSML Preview:")
    print(f"   {ssml[:100]}...")
    
    # Phoneme synthesis
    print("\n4. Phoneme Breakdown:")
    phonemes = sg.synthesize_phonemes("Hello")
    print(f"   Text: {phonemes['text']}")
    print(f"   Phonemes: {' '.join(phonemes['phonemes'][:10])}")
    
    # Duration estimation
    print("\n5. Duration Estimation:")
    long_text = "आज मौसम बहुत अच्छा है। चलिए बाहर घूमने चलते हैं।"
    duration = sg.estimate_duration(long_text)
    print(f"   Text: {long_text}")
    print(f"   Words: {duration['word_count']}")
    print(f"   Duration: {duration['estimated_duration_readable']}")
    
    # Multilingual
    print("\n6. Multilingual Support:")
    languages = ['hindi', 'english']
    for lang in languages:
        speech = sg.multilingual_speech("Hello World", lang)
        print(f"   {lang.capitalize()}: {speech['voice_params']['language']}")
    
    # Statistics
    print("\n7. Statistics:")
    stats = sg.get_statistics()
    print(f"   Total speeches: {stats['total_speeches']}")
    print(f"   Total words: {stats['total_words_spoken']}")
    print(f"   Emotions used: {stats['emotions_used']}")
