import asyncio
import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
import django
django.setup()

from assistant.tts_service import synthesize_neural_speech

async def test():
    test_cases = [
        ("hi-IN", "सरकारी योजनाओं में आपका स्वागत है"),
        ("or-IN", "ସରକାରୀ ଯୋଜନାରେ ଆପଣଙ୍କୁ ସ୍ୱାଗତ"),
        ("bn-IN", "সরকারি প্রকল্পে আপনাকে স্বাগতম"),
        ("pa-IN", "ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ"),
        ("ta-IN", "அரசு திட்டங்களுக்கு உங்களை வரவேற்கிறோம்"),
        ("te-IN", "ప్రభుత్వ పథకాలకు స్వాగతం"),
    ]
    for lang, text in test_cases:
        try:
            audio = await synthesize_neural_speech(text, lang=lang)
            print(f"[{lang}] Success: generated {len(audio)} bytes of MP3 audio")
        except Exception as e:
            print(f"[{lang}] FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test())
