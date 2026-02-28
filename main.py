"""
🧠 मॉड्यूलर वर्चुअल असिस्टेंट — Python FastAPI Backend v3.0
================================================================
NO LLM — 100% Local Python modules!

Features:
  • Rule-based + ReasoningEngine + Memory → Chat responses
  • WorkingMemory + ShortTermMemory + LongTermMemory → Persistent context
  • GoalSetting + PlanningSystem → Goal/Task management
  • Whisper → Speech-to-text
  • gTTS → Text-to-speech
  • BeautifulSoup → Web scraping
  • Rule-based vision analysis (LLM नहीं)

Setup:
  pip install -r requirements.txt
  python main.py
  → http://localhost:8000
"""

import os, io, re, json, base64, tempfile
from pathlib import Path
from datetime import datetime

import httpx
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List

# ── AI Modules ────────────────────────────────────────────────────────────────
from working_memory      import WorkingMemory
from short_term_memory   import ShortTermMemory
from long_term_memory    import LongTermMemory
from reasoning_engine    import ReasoningEngine
from decision_making     import DecisionMaker
from language_understanding import LanguageUnderstanding
from math_logic_processor   import MathLogicProcessor
from pattern_recognition    import PatternRecognition
from goal_setting           import GoalSetting, GoalPriority
from planning_system        import PlanningSystem
from self_monitoring        import SelfMonitoring
from task_switching         import TaskSwitching
from time_perception        import TimePerception
from SpeechGenerator   import SpeechGenerator
from TextOutputSystem  import TextOutputSystem
from FacialExpressions import FacialExpressions
from VisualCreation    import VisualCreation

# ── Optional imports ──────────────────────────────────────────────────────────
try:
    import whisper as _whisper
    _whisper_model = _whisper.load_model("base")
    WHISPER_OK = True
    print("✅ Whisper STT लोड हुआ")
except Exception as e:
    WHISPER_OK = False
    print(f"⚠️  Whisper नहीं मिला: {e}")

try:
    from gtts import gTTS
    GTTS_OK = True
    print("✅ gTTS तैयार")
except ImportError:
    GTTS_OK = False
    print("⚠️  gTTS नहीं मिला")

try:
    from bs4 import BeautifulSoup
    BS4_OK = True
    print("✅ BeautifulSoup तैयार")
except ImportError:
    BS4_OK = False
    print("⚠️  bs4 नहीं मिला")

# ── Initialize all AI modules ─────────────────────────────────────────────────
print("\n🧠 AI Modules initialize हो रहे हैं...")
working_mem   = WorkingMemory(capacity=7)
short_mem     = ShortTermMemory(retention_time=7200, max_items=100)
long_mem      = LongTermMemory(storage_path="assistant_ltm.pkl")
reasoning     = ReasoningEngine()
decision      = DecisionMaker()
language      = LanguageUnderstanding()
math_proc     = MathLogicProcessor()
pattern_rec   = PatternRecognition()
goal_sys      = GoalSetting()
planner       = PlanningSystem()
monitor       = SelfMonitoring()
task_switch   = TaskSwitching()
time_perc     = TimePerception()
speech_gen    = SpeechGenerator()
text_out      = TextOutputSystem()
face_expr     = FacialExpressions()
visual_create = VisualCreation()

# ── Pre-load reasoning rules ──────────────────────────────────────────────────
reasoning.add_rule("greet_rule",       "नमस्ते", "नमस्ते! मैं आपकी मदद करने को तैयार हूँ।", 0.95)
reasoning.add_rule("help_rule",        "मदद",    "मैं इन कामों में मदद कर सकता हूँ: चैट, मेमोरी, गोल, प्लानिंग, गणित, वेब स्क्रैपिंग।", 0.9)
reasoning.add_rule("memory_rule",      "याद",    "मुझे याद है जो आपने बताया था।", 0.85)
reasoning.add_rule("python_rule",      "python", "Python एक high-level programming language है। Variables, functions, classes से बनती है।", 0.9)
reasoning.add_rule("ai_rule",          "AI",     "Artificial Intelligence machines को सोचने की क्षमता देता है।", 0.9)
reasoning.add_rule("bye_rule",         "अलविदा", "अलविदा! अगली बार फिर मिलेंगे 😊", 0.95)

reasoning.add_fact("fact_python",  "Python एक interpreted, high-level programming language है।")
reasoning.add_fact("fact_ai",      "AI = Artificial Intelligence — मशीनों को सोचने की क्षमता।")
reasoning.add_fact("fact_ml",      "Machine Learning AI का एक subset है।")
reasoning.add_fact("fact_india",   "भारत की राजधानी नई दिल्ली है।")
reasoning.add_fact("fact_sun",     "सूरज एक तारा है, पृथ्वी से ~15 करोड़ km दूर।")

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="मॉड्यूलर असिस्टेंट API v3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.get("/")
async def serve_index():
    p = Path(__file__).parent / "index.html"
    if p.exists():
        return FileResponse(str(p))
    return {"message": "index.html नहीं मिला"}

# ── Pydantic Models ───────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    history: Optional[list] = []

class VisionRequest(BaseModel):
    image_base64: str
    prompt: Optional[str] = ""

class TTSRequest(BaseModel):
    text: str
    lang: Optional[str] = "hi"

class ScrapeRequest(BaseModel):
    url: str

class GoalRequest(BaseModel):
    description: str
    priority: Optional[str] = "medium"
    deadline: Optional[str] = None

class PlanRequest(BaseModel):
    goal: str
    complexity: Optional[str] = "medium"

class MemoryRequest(BaseModel):
    key: str
    value: str
    category: Optional[str] = "general"

# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "mode": "no-llm (rule-based + reasoning engine)",
        "modules": {
            "working_memory":   True,
            "short_term_memory": True,
            "long_term_memory":  True,
            "reasoning_engine":  True,
            "goal_setting":      True,
            "planning_system":   True,
            "whisper_stt":       WHISPER_OK,
            "gtts_tts":          GTTS_OK,
            "bs4_scrape":        BS4_OK,
            "math_processor":    True,
            "pattern_recognition": True,
        }
    }

# ── CHAT (Rule-based + Reasoning Engine + Memory) ─────────────────────────────
@app.post("/api/chat")
async def chat(req: ChatRequest):
    msg = req.message.strip()
    if not msg:
        raise HTTPException(400, "Message खाली है")

    # 1. Working memory में add करें
    working_mem.add_item(f"User: {msg}", priority=3)

    # 2. Short-term में store करें
    turn_key = f"turn_{datetime.now().strftime('%H%M%S%f')}"
    short_mem.store(turn_key, {'user': msg, 'time': datetime.now().isoformat()}, importance=0.7)

    # 3. Language understanding — intent detect करें
    parsed = language.parse_sentence(msg)
    intent = parsed['intent']['intent']
    sentiment = parsed['sentiment']['sentiment']
    keywords = parsed.get('keywords', [])
    msg_lower = msg.lower()

    reply = None

    # ── Math intent ───────────────────────────────────────────────────────────
    if intent == 'math' or re.search(r'\d+\s*[\+\-\*\/×÷]\s*\d+', msg):
        result = math_proc.extract_and_calculate(msg)
        if result['success']:
            reply = f"🧮 **{result['expression']}** = **{result['result']}**"
            face_expr.set_expression('happy')
        else:
            reply = "❌ गणना नहीं हो पाई। जैसे: '5 + 3', '10 * 7'"

    # ── Time/Date ─────────────────────────────────────────────────────────────
    elif any(w in msg_lower for w in ['time','समय','टाइम','वक्त','date','तारीख','आज','today']):
        dt = time_perc.get_current_datetime()
        if any(w in msg_lower for w in ['time','समय','टाइम','वक्त']):
            reply = f"⏰ अभी का समय: **{dt['time']}**"
        else:
            reply = f"📅 आज की तारीख: **{dt['date']}** ({dt['day']})"

    # ── Memory store intent ───────────────────────────────────────────────────
    elif intent == 'store_memory' or any(w in msg_lower for w in ['याद रखो','remember','save this','store']):
        # Important info को long-term में save करें
        key = '_'.join(keywords[:3]) if keywords else f"info_{turn_key}"
        long_mem.store(key, msg, category="user_info", tags=["important", "user_request"])
        short_mem.store(f"remember_{key}", msg, importance=1.0)
        reply = f"✅ याद कर लिया! मैंने यह long-term memory में save कर दिया है।\n🗝️ Key: `{key}`"
        face_expr.set_expression('happy')

    # ── Memory recall ─────────────────────────────────────────────────────────
    elif intent == 'recall_memory' or any(w in msg_lower for w in ['what do you remember','याद है क्या','recall','बताओ याद']):
        recent = short_mem.get_recent_memories(5)
        ltm_results = long_mem.search_by_text(msg)[:3]
        if recent or ltm_results:
            parts = []
            if recent:
                parts.append("📝 हाल की बातें:")
                for r in recent[-3:]:
                    val = r['value']
                    if isinstance(val, dict): val = val.get('user', str(val))
                    parts.append(f"  • {str(val)[:80]}")
            if ltm_results:
                parts.append("🗄️ Long-term memory:")
                for r in ltm_results:
                    parts.append(f"  • [{r['category']}] {str(r['value'])[:80]}")
            reply = '\n'.join(parts)
        else:
            reply = "🤔 अभी तक कोई खास बात याद नहीं है। कुछ बताएं तो याद कर लूंगा!"

    # ── Goal intent ───────────────────────────────────────────────────────────
    elif any(w in msg_lower for w in ['goal set','लक्ष्य','goal add','मेरा goal']) and any(w in msg_lower for w in ['set','add','बनाओ','create']):
        # Extract goal from message
        goal_text = re.sub(r'(goal set|goal add|लक्ष्य|set a goal|मेरा goal)', '', msg, flags=re.IGNORECASE).strip()
        if not goal_text:
            goal_text = msg
        result = goal_sys.set_goal(goal_text, priority=GoalPriority.MEDIUM)
        reply = f"🎯 Goal set हो गया!\n📌 **{result['description']}**\n🆔 ID: `{result['goal_id']}`"
        face_expr.set_expression('happy')

    # ── Goals list ────────────────────────────────────────────────────────────
    elif any(w in msg_lower for w in ['my goals','मेरे goals','goals दिखाओ','show goals','सभी goals']):
        goals = goal_sys.get_active_goals()
        if goals:
            parts = ["🎯 आपके active goals:"]
            for g in goals:
                bar = '█' * int(g['progress']//10) + '░' * (10 - int(g['progress']//10))
                parts.append(f"  • **{g['description']}**\n    [{bar}] {g['progress']:.0f}%")
            reply = '\n'.join(parts)
        else:
            reply = "📭 अभी कोई active goal नहीं है। Goal set करने के लिए कहें: 'goal set: Python सीखना'"

    # ── Plan intent ───────────────────────────────────────────────────────────
    elif any(w in msg_lower for w in ['plan','प्लान','planning','steps','कदम']) and any(w in msg_lower for w in ['बनाओ','create','make','for','के लिए']):
        plan_text = re.sub(r'(plan बनाओ|plan for|create plan|planning)', '', msg, flags=re.IGNORECASE).strip()
        if not plan_text:
            plan_text = msg
        result = planner.decompose_goal(plan_text, complexity='medium')
        plan_status = planner.get_plan_status(result['plan_id'])
        parts = [f"📋 Plan बना दिया: **{plan_text}**",
                 f"📊 {result['tasks_created']} tasks | ⏱️ ~{result['estimated_time']} minutes"]
        for i, t in enumerate(planner.plans[result['plan_id']].tasks, 1):
            parts.append(f"  {i}. {t.description}")
        reply = '\n'.join(parts)
        face_expr.set_expression('thinking')

    # ── Pattern analysis ──────────────────────────────────────────────────────
    elif any(w in msg_lower for w in ['pattern','trend','sequence','क्रम']) and re.search(r'\d', msg):
        nums = [float(x) for x in re.findall(r'\d+\.?\d*', msg)]
        if len(nums) >= 3:
            pattern = pattern_rec.find_sequence_pattern([int(n) if n.is_integer() else n for n in nums])
            trend = pattern_rec.detect_trend(nums)
            reply = f"🔍 **Pattern Analysis:**\n"
            reply += f"  • Numbers: {nums}\n"
            reply += f"  • Pattern type: {pattern.get('type', 'unknown')}\n"
            if pattern.get('pattern'):
                reply += f"  • Pattern: {pattern['pattern']}\n"
            if pattern.get('next_value'):
                reply += f"  • अगला value: **{pattern['next_value']}**\n"
            reply += f"  • Trend: {trend['trend']}"
        else:
            reply = "🔍 Pattern देखने के लिए कम से कम 3 numbers दें। जैसे: '2, 4, 6, 8'"

    # ── Greeting ──────────────────────────────────────────────────────────────
    elif any(w in msg_lower for w in ['नमस्ते','hello','hi','हाय','हेलो','namaskar','namaste']):
        face_expr.set_expression('happy')
        # Check if we remember user name
        user_info = long_mem.search_by_tag("user_name")
        if user_info:
            name = str(user_info[0]['value'])[:30]
            reply = f"नमस्ते {name}! 😊 आपसे फिर मिलकर खुशी हुई। आज क्या करें?"
        else:
            reply = "नमस्ते! 😊 मैं आपका local AI assistant हूँ — बिना किसी internet या API के!\n\nमैं कर सकता हूँ:\n🧮 गणित\n🎯 Goal setting\n📋 Planning\n💾 Memory\n🔍 Pattern analysis\n🌐 Web scraping\n⏰ Time & Date"

    # ── About me ──────────────────────────────────────────────────────────────
    elif any(w in msg_lower for w in ['who are you','तुम कौन','आप क्या','about you','तुम्हारे बारे']):
        stats = {
            'wm': working_mem.get_status()['current_items'],
            'stm': short_mem.get_stats().get('total_items', 0),
            'ltm': long_mem.get_statistics()['total_entries'],
            'goals': goal_sys.get_statistics().get('total_goals', 0),
            'reasoning': reasoning.get_statistics()['total_reasoning_steps']
        }
        reply = f"""🤖 **मैं मॉड्यूलर AI असिस्टेंट हूँ!**

कोई LLM नहीं — सब कुछ Python modules से!

**Active Modules:**
• 🧠 Working Memory: {stats['wm']}/7 slots
• 💾 Short-term Memory: {stats['stm']} items
• 🗄️ Long-term Memory: {stats['ltm']} entries
• 🤔 Reasoning Steps: {stats['reasoning']}
• 🎯 Goals tracked: {stats['goals']}
• ⚖️ Decision Maker: Active
• 📖 Language Understanding: Active
• 🧮 Math Processor: Active"""

    # ── Thanks ────────────────────────────────────────────────────────────────
    elif any(w in msg_lower for w in ['धन्यवाद','thanks','thank','शुक्रिया','shukriya']):
        face_expr.set_expression('happy')
        reply = "आपका स्वागत है! 😊 कोई और काम हो तो बताएं।"

    # ── Deductive reasoning fallback ──────────────────────────────────────────
    else:
        face_expr.set_expression('thinking')
        # Try deductive reasoning with rules
        conclusions = reasoning.deductive_reasoning([msg])
        if conclusions:
            reply = conclusions[0]['conclusion']
            face_expr.set_expression('happy')
        else:
            # Try inductive from history
            recent = short_mem.get_recent_memories(10)
            recent_texts = [str(r['value']) for r in recent]
            if recent_texts:
                generalizations = reasoning.inductive_reasoning(recent_texts)
                if generalizations:
                    reply = f"🤔 मेरी समझ: {generalizations[0]['pattern']}"

        # LTM search
        if not reply:
            ltm_hits = long_mem.search_by_text(msg)
            if ltm_hits:
                reply = f"📚 Long-term memory से: {str(ltm_hits[0]['value'])[:200]}"

        # Final fallback
        if not reply:
            # Abductive reasoning — guess best explanation
            possible = [
                {'hypothesis': f"आप '{' '.join(keywords[:3])}' के बारे में जानना चाहते हैं।",
                 'prior_probability': 0.6},
                {'hypothesis': f"यह एक {intent} है।", 'prior_probability': 0.4}
            ]
            abductive = reasoning.abductive_reasoning(msg, possible)
            best = abductive[0]['explanation'] if abductive else ""
            reply = (f"🤖 {best}\n\n"
                     f"मैं rule-based AI हूँ — complex questions के लिए specific commands try करें:\n"
                     f"• 'goal set: [लक्ष्य]' — नया goal\n"
                     f"• 'plan बनाओ: [काम]' — planning\n"
                     f"• '[number] + [number]' — गणित\n"
                     f"• 'याद रखो: [जानकारी]' — memory\n"
                     f"• 'समय क्या है?' — time/date\n"
                     f"• '2,4,6,8 pattern?' — pattern analysis")

    # 4. Working memory में response add करें
    working_mem.add_item(f"AI: {reply[:50]}...", priority=2)

    # 5. Performance monitor करें
    monitor.record_performance("chat", {
        'response_length': len(reply) if reply else 0,
        'intent_confidence': parsed['intent']['confidence']
    })

    # 6. Short-term में response store करें
    short_mem.store(f"response_{turn_key}", {'ai': reply, 'intent': intent}, importance=0.6)

    return {
        'reply': reply,
        'intent': intent,
        'sentiment': sentiment,
        'expression': face_expr.current_expression,
        'memory_stats': {
            'working': working_mem.get_status()['current_items'],
            'short_term': short_mem.get_stats().get('total_items', 0),
            'long_term': long_mem.get_statistics()['total_entries']
        }
    }

# ── VISION (Rule-based — LLM नहीं) ───────────────────────────────────────────
@app.post("/api/vision")
async def vision(req: VisionRequest):
    """
    Rule-based image analysis — LLM नहीं, pure Python
    Base64 image से basic properties detect करें
    """
    try:
        # Base64 decode करें
        img_data = req.image_base64
        if "," in img_data:
            img_data = img_data.split(",", 1)[1]

        img_bytes = base64.b64decode(img_data)
        img_size_kb = len(img_bytes) / 1024

        # Basic analysis — pixel sampling से
        analysis = _rule_based_image_analysis(img_bytes, img_size_kb)

        # Face expression update
        face_expr.set_expression('thinking')

        # Short-term में store करें
        short_mem.store("last_image", analysis, importance=0.8)

        return {'reply': analysis}

    except Exception as e:
        return {'reply': f"❌ Image analysis error: {e}"}

def _rule_based_image_analysis(img_bytes: bytes, size_kb: float) -> str:
    """
    Pure rule-based image analysis
    Pixel sampling से brightness, colors, और basic properties detect करें
    """
    try:
        # PIL available है तो use करें
        from PIL import Image
        import io as _io

        img = Image.open(_io.BytesIO(img_bytes)).convert('RGB')
        width, height = img.size
        aspect = width / height

        # Sample pixels (100 random points)
        import random
        pixels = []
        for _ in range(200):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            pixels.append(img.getpixel((x, y)))

        # Average color
        avg_r = sum(p[0] for p in pixels) / len(pixels)
        avg_g = sum(p[1] for p in pixels) / len(pixels)
        avg_b = sum(p[2] for p in pixels) / len(pixels)
        brightness = (avg_r + avg_g + avg_b) / 3

        # Color dominance
        dominant = "लाल" if avg_r > avg_g and avg_r > avg_b else \
                   "हरा" if avg_g > avg_r and avg_g > avg_b else \
                   "नीला" if avg_b > avg_r and avg_b > avg_g else "मिश्रित"

        brightness_label = "बहुत उजला" if brightness > 200 else \
                           "उजला" if brightness > 150 else \
                           "सामान्य" if brightness > 100 else \
                           "अंधेरा" if brightness > 50 else "बहुत अंधेरा"

        orientation = "Landscape" if aspect > 1.2 else \
                      "Portrait" if aspect < 0.8 else "Square"

        # Color diversity (unique colors roughly)
        unique_rough = len(set((p[0]//50, p[1]//50, p[2]//50) for p in pixels))
        colorfulness = "बहुत रंगीन" if unique_rough > 30 else \
                       "रंगीन" if unique_rough > 15 else \
                       "कम रंग" if unique_rough > 5 else "monochrome"

        result = f"""📸 **Image Analysis (Rule-based)**

📐 **Size:** {width}×{height} pixels ({orientation})
💾 **File size:** {size_kb:.1f} KB
☀️ **Brightness:** {brightness_label} ({brightness:.0f}/255)
🎨 **Dominant color:** {dominant}
🌈 **Colorfulness:** {colorfulness}

📊 **Color Values:**
  • Red average: {avg_r:.0f}
  • Green average: {avg_g:.0f}
  • Blue average: {avg_b:.0f}

💡 **Note:** यह rule-based analysis है। LLM नहीं है, इसलिए objects/faces identify नहीं होते।
   PIL (Pillow) से basic color और size analysis होती है।"""

        return result

    except ImportError:
        # PIL नहीं है — basic analysis
        return f"""📸 **Image Analysis (Basic)**

💾 File size: {size_kb:.1f} KB
📊 Raw bytes: {len(img_bytes)}

🔧 बेहतर analysis के लिए install करें:
   pip install Pillow

💡 Note: यह rule-based analysis है — LLM नहीं।"""

    except Exception as e:
        return f"❌ Analysis error: {e}"

# ── SPEECH-TO-TEXT (Whisper) ──────────────────────────────────────────────────
@app.post("/api/stt")
async def stt(audio: UploadFile = File(...)):
    if not WHISPER_OK:
        raise HTTPException(503, "Whisper install करें: pip install openai-whisper")

    audio_bytes = await audio.read()
    suffix = Path(audio.filename or "audio.webm").suffix or ".webm"

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        result = _whisper_model.transcribe(tmp_path, language="hi")
        text = result.get("text", "").strip()
        # Short-term में store करें
        if text:
            short_mem.store(f"speech_{datetime.now().strftime('%H%M%S')}", text, importance=0.8)
        return {"text": text}
    except Exception as e:
        raise HTTPException(500, f"Transcription failed: {e}")
    finally:
        os.unlink(tmp_path)

# ── TEXT-TO-SPEECH (gTTS) ─────────────────────────────────────────────────────
@app.post("/api/tts")
async def tts(req: TTSRequest):
    if not GTTS_OK:
        raise HTTPException(503, "gTTS install करें: pip install gtts")
    if not req.text.strip():
        raise HTTPException(400, "Text खाली है।")

    # Speech generation module use करें
    speech_gen.generate_speech(req.text, emotion='calm')

    try:
        tts_obj = gTTS(text=req.text, lang=req.lang, slow=False)
        buf = io.BytesIO()
        tts_obj.write_to_fp(buf)
        buf.seek(0)
        return StreamingResponse(buf, media_type="audio/mpeg",
                                 headers={"Content-Disposition": "inline; filename=speech.mp3"})
    except Exception as e:
        raise HTTPException(500, f"TTS failed: {e}")

# ── WEB SCRAPING ──────────────────────────────────────────────────────────────
@app.post("/api/scrape")
async def scrape(req: ScrapeRequest):
    headers = {"User-Agent": "Mozilla/5.0 Chrome/120"}
    try:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as c:
            r = await c.get(req.url, headers=headers)

        ct = r.headers.get("content-type", "")

        if "json" in ct:
            try:
                data = r.json()
                # Long-term में cache करें
                long_mem.store(f"scrape_{req.url[:30]}", data, category="scraped_data", tags=["web"])
                return {"type": "json", "data": data}
            except Exception:
                pass

        if BS4_OK and "html" in ct:
            soup = BeautifulSoup(r.text, "html.parser")
            for tag in soup(["script","style","nav","footer","head"]):
                tag.decompose()
            text = re.sub(r'\n{3,}', '\n\n', soup.get_text("\n")).strip()
            short_mem.store(f"scraped_{req.url[:20]}", text[:200], importance=0.6)
            return {"type": "html", "data": text[:5000]}

        return {"type": "text", "data": r.text[:5000]}

    except httpx.ConnectError:
        raise HTTPException(502, f"Connect नहीं हुआ: {req.url}")
    except Exception as e:
        raise HTTPException(500, str(e))

# ── GOAL APIs ─────────────────────────────────────────────────────────────────
@app.post("/api/goal")
async def create_goal(req: GoalRequest):
    priority_map = {'low': GoalPriority.LOW, 'medium': GoalPriority.MEDIUM,
                    'high': GoalPriority.HIGH, 'critical': GoalPriority.CRITICAL}
    priority = priority_map.get(req.priority.lower(), GoalPriority.MEDIUM)
    result = goal_sys.set_goal(req.description, priority=priority, deadline=req.deadline)
    # Long-term में save करें
    long_mem.store(result['goal_id'], req.description, category="goals", tags=["goal","active"])
    return result

@app.get("/api/goals")
async def get_goals():
    return {"goals": goal_sys.get_active_goals(), "stats": goal_sys.get_statistics()}

@app.put("/api/goal/{goal_id}/progress")
async def update_goal_progress(goal_id: str, progress: float):
    return goal_sys.update_progress(goal_id, progress / 100.0)

@app.put("/api/goal/{goal_id}/complete")
async def complete_goal(goal_id: str):
    return goal_sys.complete_goal(goal_id)

# ── PLAN APIs ─────────────────────────────────────────────────────────────────
@app.post("/api/plan")
async def create_plan(req: PlanRequest):
    result = planner.decompose_goal(req.goal, complexity=req.complexity)
    plan_status = planner.get_plan_status(result['plan_id'])
    timeline = planner.create_timeline(result['plan_id'])
    return {**result, 'tasks': [t.description for t in planner.plans[result['plan_id']].tasks],
            'timeline': timeline['timeline'][:5]}

@app.get("/api/plans")
async def get_plans():
    return {"plans": planner.get_all_plans(), "stats": planner.get_statistics()}

# ── MEMORY APIs ───────────────────────────────────────────────────────────────
@app.get("/api/memory/status")
async def memory_status():
    return {
        "working_memory": working_mem.get_status(),
        "short_term": short_mem.get_stats(),
        "long_term": long_mem.get_statistics(),
        "recent_items": [
            {**r, 'value': str(r['value'])[:100]}
            for r in short_mem.get_recent_memories(5)
        ]
    }

@app.post("/api/memory/store")
async def store_memory(req: MemoryRequest):
    long_mem.store(req.key, req.value, category=req.category, tags=["manual"])
    short_mem.store(req.key, req.value, importance=0.9)
    return {"status": "stored", "key": req.key}

@app.get("/api/memory/search/{query}")
async def search_memory(query: str):
    return {
        "short_term": [dict(**r, value=str(r['value'])[:100]) for r in short_mem.search(query)],
        "long_term": [dict(**r, value=str(r['value'])[:100]) for r in long_mem.search_by_text(query)[:5]]
    }

# ── STATS API ─────────────────────────────────────────────────────────────────
@app.get("/api/stats")
async def get_all_stats():
    return {
        "working_memory": working_mem.get_status(),
        "short_term_memory": short_mem.get_stats(),
        "long_term_memory": long_mem.get_statistics(),
        "reasoning_engine": reasoning.get_statistics(),
        "decision_maker": decision.get_statistics(),
        "goal_setting": goal_sys.get_statistics(),
        "planning_system": planner.get_statistics(),
        "self_monitoring": monitor.get_statistics(),
        "task_switching": task_switch.get_statistics(),
        "speech_generator": speech_gen.get_statistics(),
        "visual_creation": visual_create.get_statistics(),
        "facial_expression": face_expr.get_statistics(),
    }

# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    print("\n🚀 मॉड्यूलर असिस्टेंट v3.0 शुरू हो रहा है...")
    print("🧠 Mode: NO-LLM (Rule-based + Reasoning Engine)")
    print("📌 Frontend : http://localhost:8000")
    print("📌 API Docs : http://localhost:8000/docs\n")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
