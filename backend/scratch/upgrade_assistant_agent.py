import re
import os

target_path = r"C:\Users\Simran\Downloads\SchemeNavigator\SchemeNavigator\Scheme-Navigator-App-master\backend\agents\assistant_agent.py"

with open(target_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update SYSTEM_PROMPT_TEMPLATE with trained structured answering guidelines
old_prompt_marker = 'SYSTEM_PROMPT_TEMPLATE = """You are Mitra (मित्र / মিত্র / متر / ਮਿੱਤਰ)'
prompt_start = code.find(old_prompt_marker)
prompt_end = code.find('LANGUAGE_NAMES = {', prompt_start)

if prompt_start != -1 and prompt_end != -1:
    new_prompt = '''SYSTEM_PROMPT_TEMPLATE = """You are Mitra (मित्र / মিত্র / متر / ਮਿੱਤਰ), the elite, compassionate, and highly knowledgeable AI Welfare Counselor & Scheme Advisor on SchemeNavigator (भारत सरकार कल्याण सलाहकार).

CRITICAL MISSION & CITIZEN CENTRIC TRAINING:
Your sole mission is to guide Indian citizens to the exact welfare schemes they qualify for, demystifying government procedures, deadlines, exact financial benefits (₹ amounts), eligibility criteria, required documents, and application steps.

CRITICAL MULTILINGUAL MANDATE (HIGHEST PRIORITY):
The user's query language is determined to be: {target_language} ({target_language_name}).
YOU MUST GENERATE YOUR ENTIRE RESPONSE STRICTLY IN {target_language_name}.
- If the user asks in Hindi (हिंदी) or Hinglish: Reply 100% in natural, polite, respectful Hindi using Devanagari script (e.g. "नमस्ते! मैं मित्र AI हूँ...").
- If the user asks in Bengali (বাংলা) or Banglish: Reply 100% in fluent, polite Bengali script.
- If the user asks in Urdu (اردو) or Roman Urdu: Reply 100% in fluent, respectful Urdu script.
- If the user asks in Punjabi (ਪੰਜਾਬੀ) or Roman Punjabi: Reply 100% in warm, fluent Punjabi (Gurmukhi script).
- If the user asks in Odia (ଓଡ଼ିଆ): Respond 100% in fluent Odia script.
- If the user asks in Marathi (मराठी): Respond 100% in fluent Marathi (Devanagari script).
- If the user asks in Telugu (తెలుగు): Respond 100% in fluent Telugu script.
- If the user asks in Tamil (தமிழ்): Respond 100% in fluent Tamil script.
- If the user asks in Gujarati (ગુજરાતી): Respond 100% in fluent Gujarati script.
- If the user asks in Kannada (ಕನ್ನಡ): Respond 100% in fluent Kannada script.
- If the user asks in Malayalam (മലയാളം): Respond 100% in fluent Malayalam script.
- If the user asks strictly in English: Respond in clean, professional English.

STRUCTURED RESPONSE BLUEPRINT (MANDATORY FOR ALL SCHEME QUERIES):
Whenever explaining or recommending schemes, format your answer clearly with markdown bullet points and emojis:
1. 🎯 **योजना का नाम और मुख्य उद्देश्य (Scheme Name & Purpose)**: 1-2 direct lines on who it helps and what problem it solves.
2. 💰 **वित्तीय लाभ और सहायता राशि (Financial Assistance / Subsidy)**: State the exact amount (e.g. ₹6,000/year for PM-KISAN, ₹5 लाख तक कैशलेस इलाज for Ayushman Bharat, ₹50,000 से ₹10 लाख for Mudra Loan, ₹15,000 टूलकिट सहायता for PM Vishwakarma, etc.).
3. 📋 **पात्रता मानदंड (Eligibility Criteria)**: Specific conditions: Age limits, Income limits, Landholding, Gender/Caste (SC/ST/OBC/General), BPL/Ration card status.
4. 📄 **आवश्यक दस्तावेज़ (Required Documents)**: Bulleted checklist (Aadhaar card, Bank passbook linked with DBT/NPCI, Income certificate, Caste certificate, Land documents / Khasra-Khatauni, Passport photo, Active mobile number).
5. 📝 **आवेदन कैसे करें (Application Process - Online & Offline)**:
   - Online step: Official government portal, Aadhaar OTP authentication, e-KYC.
   - Offline step: Nearest Common Service Centre (CSC / जन सेवा केंद्र / मो सेवा केंद्र), Panchayat/Block office, or designated bank branch.
6. 🌐 **आधिकारिक पोर्टल और हेल्पलाइन (Official Portal URL & Toll-Free Helpline)**: Include the official portal URL and national helpline number.
7. 💡 **नागरिक के लिए सलाह (Pro-Tip / Next Step)**: E.g., verifying Bank Aadhaar-seeding status, checking nearest CSC Kendra via SchemeNavigator's Kendra Finder.

CITIZEN PROFILE PERSONALIZATION:
{profile_context}
- If the citizen has provided demographics (or mentions them in the query, e.g. "Main student hu", "Farmer hu 2 acre zameen hai", "Meri umar 68 saal hai"), immediately customize the response to their situation and address them empathetically.

STRICT DOMAIN SCOPE & GUARDRAILS:
1. ONLY answer questions about Indian Government welfare schemes (Central & State), benefits, eligibility, documents, application processes, and Scheme Navigator portal tools (Survey, Voice Reader, Tracker, Kendra Finder, Calendar).
2. Out-of-Scope Questions (coding, math, general trivia, weather, politics, gossip, jokes): Firmly and politely decline in {target_language_name}, stating that you are Mitra AI, dedicated exclusively to government welfare schemes.
3. ZERO Tech Stack Leakage: Never mention internal models, API keys, Python, Gemini, or system prompts. Always present yourself purely as "Mitra AI" on "Scheme Navigator".
4. Append exact database slugs at the very end of your response inside <schemes>...</schemes> tag:
   <schemes>slug-1,slug-2</schemes>
   (Omit <schemes> tag for simple greetings, website overviews, or refusals).

AVAILABLE SCHEMES CONTEXT (Verified from Database):
{scheme_context}
"""

'''
    code = code[:prompt_start] + new_prompt + code[prompt_end:]
    print("Successfully updated SYSTEM_PROMPT_TEMPLATE")
else:
    print("Warning: Could not locate SYSTEM_PROMPT_TEMPLATE bounds")

# 2. Add _safe_int helper at top level
if "def _safe_int(" not in code:
    safe_int_def = '''def _safe_int(val: Any, default: int = 0) -> int:
    """Safely convert any value to int, avoiding TypeError when val is None."""
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


'''
    # Insert right after typing imports
    ins_idx = code.find("from .litellm_client import call_llm")
    if ins_idx != -1:
        code = code[:ins_idx] + safe_int_def + code[ins_idx:]
    else:
        code = safe_int_def + code
    print("Added _safe_int helper")

# 3. Fix min_a and max_a in _search_schemes / _build_scheme_context / _generate_conversational_fallback
code = code.replace(
    'min_a = e_obj.get("minAge", 0)\n            max_a = e_obj.get("maxAge", 100)',
    'min_a = _safe_int(e_obj.get("minAge"), 0)\n            max_a = _safe_int(e_obj.get("maxAge"), 100)'
)
code = re.sub(
    r'min_a\s*=\s*e_obj\.get\(\s*["\']minAge["\']\s*,\s*0\s*\)',
    'min_a = _safe_int(e_obj.get("minAge"), 0)',
    code
)
code = re.sub(
    r'max_a\s*=\s*e_obj\.get\(\s*["\']maxAge["\']\s*,\s*100\s*\)',
    'max_a = _safe_int(e_obj.get("maxAge"), 100)',
    code
)

# 4. Update SCHEME_ALIASES with verified database slugs
verified_aliases = '''SCHEME_ALIASES = [
    # Healthcare
    (["ayushman", "pmjay", "pm-jay", "jan arogya", "ayushman card", "health card", "swasthya card", "ilaj card", "5 lakh muft ilaj", "free ilaj", "मुफ्त इलाज", "স্বাস্থ্য কার্ড", "صحت کارڈ", "ਆਯੁਸ਼ਮਾਨ"], "ayushman-bharat-pmjay"),
    (["vaya vandana", "ayushman senior", "70+", "70 plus", "70 saal", "70 varsh", "senior citizen health"], "ayushman-vaya-vandana-senior-citizens"),
    (["janaushadhi", "jan aushadhi", "generic medicine", "dawa kendra", "pmbjp", "sasti dawa"], "pmbjp"),

    # Agriculture & Farmers
    (["kisan samman", "pm kisan", "pm-kisan", "samman nidhi", "6000 kisan", "kisan 6000", "kisan samman nidhi", "pmkisan", "কৃষক সম্মান", "کسان سمان", "ਪੀਐੱਮ ਕਿਸਾਨ"], "pm-kisan-samman-nidhi"),
    (["kusum", "solar pump", "solar kisan", "solar panel khet", "pm kusum", "সৌর পাম্প", "ਸੋਲਰ ਪੰਪ"], "pm-kusum-solar-pump-scheme"),
    (["fasal bima", "pmfby", "crop insurance", "fasal nuksan", "ফসল বিমা", "فصل بیمہ", "ਫ਼ਸਲ ਬੀਮਾ"], "pradhan-mantri-fasal-bima-yojana"),
    (["kisan credit card", "kcc", "kheti loan", "crop loan", "kcc loan", "ਕੇਸੀਸੀ", "کے سی سی"], "kcc"),

    # Business, MSME & Livelihood Loans
    (["mudra", "mudra loan", "shishu", "kishor", "tarun", "tarun plus", "dukan loan", "chhota business loan", "vyapar loan", "মুদ্রা ঋণ", "مدرا لون", "ਮੁਦਰਾ ਕਰਜ਼ਾ"], "pradhan-mantri-mudra-yojana"),
    (["svanidhi", "street vendor", "pm-svanidhi", "rehdi", "patri", "thela loan", "vendor loan", "10000 loan", "স্বনিধি", "سوانیدھی"], "pm-svanidhi"),
    (["vishwakarma", "pm-vishwakarma", "artisan", "karigar", "silai machine", "darzi", "mistri", "lohar", "badhai", "sonar", "15000 toolkit", "toolkit yojana", "বিশ্বকর্মা", "وشوکرما"], "pm-vishwakarma-scheme"),
    (["stand up india", "stand-up", "women entrepreneur loan", "sc st business loan"], "stand-up-india-scheme"),
    (["pmegp", "prime minister employment generation", "pme gp", "khadi loan", "factory subsidy", "business subsidy"], "prime-minister-employment-generation-programme"),

    # Education & Scholarships
    (["post matric", "post-matric", "nsp", "scholarship", "chhatravritti", "college scholarship", "12th pass scholarship", "sc scholarship", "obc scholarship", "minority scholarship", "স্কলারশিপ", "اسکالرشپ", "ਵਜ਼ੀਫ਼ਾ"], "post-matric-scholarship-sc-obc-minority"),
    (["pm-usp", "pm usp", "uchchatar shiksha", "higher education scholarship", "degree scholarship", "college fees"], "pm-uchchatar-shiksha-protsahan-yojana"),
    (["free coaching", "upsc coaching", "ias coaching", "competitive exam coaching"], "scheme-for-free-coaching-for-sc-and-obc-students"),
    (["kaushal vikas", "pmkvy", "skill india", "rozgar training", "free training", "skill certificate"], "pradhan-mantri-kaushal-vikas-yojana"),
    (["apprenticeship", "naps", "naps-2", "stipend training"], "national-apprenticeship-promotion-scheme"),

    # Housing
    (["awas yojana", "pmay", "pm awas", "pradhan mantri awas", "makan yojana", "ghar yojana", "pucca ghar", "gramin awas", "pmay-g", "আবাস যোজনা", "آواس یوجنا", "ਆਵਾਸ ਯੋਜਨਾ"], "pradhan-mantri-awas-yojana-gramin"),

    # Social Security & Pensions
    (["atal pension", "apy", "60 ke baad pension", "budhapa pension", "অটল পেনশন", "اٹل پنشن", "ਅਟਲ ਪੈਨਸ਼ਨ"], "atal-pension-yojana"),
    (["old age pension", "vridha pension", "vriddha pension", "ignoaps", "senior citizen pension", "bujurg pension"], "indira-gandhi-national-old-age-pension-scheme"),
    (["suraksha bima", "pmsby", "20 rupaye bima", "accident insurance", "durghatna bima"], "pmsby"),
    (["jeevan jyoti", "pmjjby", "436 bima", "life insurance", "jeevan bima"], "pmjjby"),
    (["divyang", "viklang", "disability", "handicapped", "wheelchair", "hearing aid", "adip", "prosthetic"], "adip-scheme-for-persons-with-disabilities"),

    # Women & Child
    (["sukanya", "ssy", "sukanya samriddhi", "beti bachat", "kanya yojana", "ladki yojana", "girl child scheme", "সুকন্যা সমৃদ্ধি", "سکنیا سمردھی"], "sukanya-samriddhi-yojana"),
    (["matru vandana", "pmmvy", "maternity", "garbhavati", "delivery sahayata", "5000 pregnant", "মাতৃ বন্দনা", "ماترو وندنا"], "pradhan-mantri-matru-vandana-yojana"),
    (["ujjwala", "pmuy", "pmuy2", "free gas", "lpg subsidy", "gas cylinder", "उज्ज्वला", "উজ্জ্বলা", "اجولا"], "pmuy"),
]'''

code = re.sub(r'SCHEME_ALIASES\s*=\s*\[.*?\]\n\nINTENT_CATEGORY_MAP', verified_aliases + '\n\nINTENT_CATEGORY_MAP', code, flags=re.DOTALL)
print("Updated SCHEME_ALIASES")

# 5. Expand INTENT_CATEGORY_MAP with rich Hindi/Hinglish terms
intent_cat_block = '''INTENT_CATEGORY_MAP = {
    # Agriculture & Farming
    "kisan": ["Agriculture", "Financial Assistance"],
    "kheti": ["Agriculture", "Financial Assistance"],
    "farmer": ["Agriculture", "Financial Assistance"],
    "farming": ["Agriculture", "Financial Assistance"],
    "crop": ["Agriculture"],
    "tractor": ["Agriculture", "Financial Assistance"],
    "fertilizer": ["Agriculture"],
    "fasal": ["Agriculture"],
    "beej": ["Agriculture"],
    "sinchai": ["Agriculture"],
    "irrigation": ["Agriculture"],
    "krishi": ["Agriculture"],
    "krishok": ["Agriculture"],
    "kassano": ["Agriculture"],
    "kashtkar": ["Agriculture"],
    "khet": ["Agriculture"],
    "zameen": ["Agriculture"],
    "anaj": ["Agriculture"],
    "mandi": ["Agriculture"],
    "kusum": ["Agriculture"],
    "kcc": ["Agriculture", "Financial Assistance"],

    # Education & Skills
    "student": ["Education", "Skill Development"],
    "scholarship": ["Education", "Financial Assistance"],
    "chhatravritti": ["Education", "Financial Assistance"],
    "study": ["Education", "Skill Development"],
    "padhai": ["Education", "Skill Development"],
    "shiksha": ["Education", "Skill Development"],
    "college": ["Education"],
    "school": ["Education"],
    "fee": ["Education", "Financial Assistance"],
    "fees": ["Education", "Financial Assistance"],
    "skill": ["Skill Development", "Employment"],
    "training": ["Skill Development"],
    "coaching": ["Education"],
    "pariksha": ["Education"],
    "wazifa": ["Education", "Financial Assistance"],
    "chhatro": ["Education"],
    "vidyarthi": ["Education"],
    "degree": ["Education"],
    "diploma": ["Education"],
    "btech": ["Education"],
    "bca": ["Education"],
    "iti": ["Skill Development", "Education"],
    "10th": ["Education"],
    "12th": ["Education"],

    # Loans & Business
    "loan": ["Business", "Financial Assistance"],
    "business": ["Business", "Financial Assistance"],
    "startup": ["Business"],
    "dukaan": ["Business", "Financial Assistance"],
    "dukan": ["Business", "Financial Assistance"],
    "shop": ["Business", "Financial Assistance"],
    "karobar": ["Business", "Financial Assistance"],
    "vyapar": ["Business", "Financial Assistance"],
    "mudra": ["Business", "Financial Assistance"],
    "subsidy": ["Financial Assistance", "Agriculture", "Business"],
    "svanidhi": ["Business", "Financial Assistance"],
    "vishwakarma": ["Business", "Skill Development"],
    "pmegp": ["Business", "Financial Assistance"],
    "qarz": ["Business", "Financial Assistance"],
    "karza": ["Business", "Financial Assistance"],
    "rin": ["Business", "Financial Assistance"],
    "vendor": ["Business", "Financial Assistance"],
    "rehdi": ["Business", "Financial Assistance"],
    "thela": ["Business", "Financial Assistance"],
    "karigar": ["Skill Development", "Business"],
    "artisan": ["Skill Development", "Business"],
    "silai": ["Skill Development", "Women & Child"],
    "toolkit": ["Skill Development", "Business"],
    "msme": ["Business", "Financial Assistance"],
    "udyam": ["Business", "Financial Assistance"],

    # Women & Child
    "woman": ["Women & Child", "Social Security"],
    "women": ["Women & Child", "Social Security"],
    "mahila": ["Women & Child", "Social Security"],
    "girl": ["Women & Child", "Education"],
    "beti": ["Women & Child", "Education"],
    "kanya": ["Women & Child", "Education"],
    "ladki": ["Women & Child", "Education"],
    "maternity": ["Women & Child", "Healthcare"],
    "matru": ["Women & Child", "Healthcare"],
    "garbhavati": ["Women & Child", "Healthcare"],
    "sukanya": ["Women & Child", "Financial Assistance"],
    "lakhpati": ["Women & Child", "Financial Assistance"],
    "widow": ["Women & Child", "Social Security"],
    "vidhwa": ["Women & Child", "Social Security"],
    "khatoon": ["Women & Child", "Social Security"],
    "aurat": ["Women & Child", "Social Security"],
    "bahu": ["Women & Child"],
    "ladli": ["Women & Child", "Financial Assistance"],
    "vivah": ["Women & Child", "Financial Assistance"],
    "shadi": ["Women & Child", "Financial Assistance"],
    "gas": ["Women & Child", "Social Security"],
    "cylinder": ["Women & Child", "Social Security"],
    "ujjwala": ["Women & Child", "Social Security"],

    # Healthcare
    "health": ["Healthcare"],
    "hospital": ["Healthcare"],
    "illness": ["Healthcare"],
    "ilaj": ["Healthcare"],
    "treatment": ["Healthcare"],
    "ayushman": ["Healthcare"],
    "medicine": ["Healthcare"],
    "dawa": ["Healthcare"],
    "dawai": ["Healthcare"],
    "swasthya": ["Healthcare"],
    "card": ["Healthcare", "Social Security"],
    "sehat": ["Healthcare"],
    "doctor": ["Healthcare"],
    "bimari": ["Healthcare"],
    "bimar": ["Healthcare"],
    "cashless": ["Healthcare"],
    "operation": ["Healthcare"],
    "pmjay": ["Healthcare"],

    # Housing
    "house": ["Housing"],
    "housing": ["Housing"],
    "ghar": ["Housing"],
    "makan": ["Housing"],
    "makaan": ["Housing"],
    "awas": ["Housing"],
    "pmay": ["Housing"],
    "bari": ["Housing"],
    "pucca": ["Housing"],
    "chhat": ["Housing"],

    # Social Security & Pensions
    "pension": ["Social Security"],
    "elderly": ["Social Security"],
    "senior": ["Social Security"],
    "old age": ["Social Security"],
    "vriddha": ["Social Security"],
    "vridha": ["Social Security"],
    "bujurg": ["Social Security"],
    "suraksha": ["Social Security"],
    "divyang": ["Social Security", "Financial Assistance"],
    "viklang": ["Social Security", "Financial Assistance"],
    "handicap": ["Social Security", "Financial Assistance"],
    "disability": ["Social Security", "Financial Assistance"],
    "bima": ["Social Security", "Financial Assistance"],
    "insurance": ["Social Security"],
    "atal pension": ["Social Security"],
    "apy": ["Social Security"],

    # Employment
    "job": ["Employment", "Skill Development"],
    "naukri": ["Employment"],
    "employment": ["Employment"],
    "berojgar": ["Employment", "Skill Development"],
    "berojgari": ["Employment", "Skill Development"],
    "unemployed": ["Employment", "Skill Development"],
    "rozgar": ["Employment"],
    "mgnrega": ["Employment"],
    "shramik": ["Employment", "Social Security"],
    "majdoor": ["Employment", "Social Security"],
}'''

code = re.sub(r'INTENT_CATEGORY_MAP\s*=\s*\{.*?\n\}\n\ndef detect_message_language', intent_cat_block + '\n\ndef detect_message_language', code, flags=re.DOTALL)
print("Updated INTENT_CATEGORY_MAP")

# 6. Replace detect_message_language cleanly using string search and slice
d_start = code.find("def detect_message_language(")
d_end = code.find("def _detect_query_intent(", d_start)

if d_start != -1 and d_end != -1:
    new_detect_lang = '''def detect_message_language(message: str, fallback_lang: str = "en-IN") -> str:
    """
    Intelligently detects whether the user is typing/speaking in:
    - Urdu (Perso-Arabic script or Romanized Urdu) -> 'ur-IN'
    - Bengali (Bengali script or Banglish) -> 'bn-IN'
    - Punjabi (Gurmukhi script or Romanized Punjabi) -> 'pa-IN'
    - Hindi (Devanagari script or Hinglish) -> 'hi-IN'
    - Odia (Odia script) -> 'or-IN'
    - Telugu (Telugu script) -> 'te-IN'
    - Tamil (Tamil script) -> 'ta-IN'
    - Marathi (Devanagari script with Marathi signals) -> 'mr-IN'
    - Gujarati (Gujarati script) -> 'gu-IN'
    - Kannada (Kannada script) -> 'kn-IN'
    - Malayalam (Malayalam script) -> 'ml-IN'
    - English
    """
    text = (message or "").strip()
    if not text:
        return fallback_lang or "en-IN"

    lower = text.lower()

    # 1. Unicode Script Detection (Strongest Signal)
    if re.search(r"[\\u0600-\\u06FF]", text):
        return "ur-IN"
    if re.search(r"[\\u0980-\\u09FF]", text):
        return "bn-IN"
    if re.search(r"[\\u0A00-\\u0A7F]", text):
        return "pa-IN"
    if re.search(r"[\\u0B00-\\u0B7F]", text):
        return "or-IN"
    if re.search(r"[\\u0C00-\\u0C7F]", text):
        return "te-IN"
    if re.search(r"[\\u0B80-\\u0BFF]", text):
        return "ta-IN"
    if re.search(r"[\\u0A80-\\u0AFF]", text):
        return "gu-IN"
    if re.search(r"[\\u0C80-\\u0CFF]", text):
        return "kn-IN"
    if re.search(r"[\\u0D00-\\u0D7F]", text):
        return "ml-IN"
    if re.search(r"[\\u0900-\\u097F]", text):
        marathi_words = ["आहे", "आहेत", "कसे", "मिळेल", "योजनांची", "माहिती", "द्या", "शेतकरी", "अर्ज", "माझे"]
        if any(w in text for w in marathi_words):
            return "mr-IN"
        return "hi-IN"

    # 2. Romanized Script / Keyword Detection
    # Distinctive Punjabi (NOT generic Hindi words like kisan/kheti/sarkari)
    if re.search(r"\\b(mainu|assi|tussi|chahida|chahidi|daso|kivve|kive|dasso|vadhiya|kujh|jatt|hove|hovan)\\b", lower):
        return "pa-IN"

    # Distinctive Bengali
    if re.search(r"\\b(amar|amake|prokolpo|jonno|chhatrobritti|kivabe|dorkar|bhalo|dhonnobad|krishok|shunchen)\\b", lower):
        return "bn-IN"

    # Distinctive Odia
    if re.search(r"\\b(mate|amara|kipari|jojana|kahantu|sahayata|darkar|janni)\\b", lower):
        return "or-IN"

    # Distinctive Marathi
    if re.search(r"\\b(majhe|kasa|karava|yojna|aahe|dya|shasan|sang|sanga)\\b", lower):
        return "mr-IN"

    # Distinctive Urdu
    if any(w in lower for w in ["wazifa", "qarz", "qard", "dastawiz", "hukumat", "janab", "shukriya"]):
        return "ur-IN"

    # Standard Hindi / Hinglish keywords (covers most conversational queries)
    hindi_keywords = [
        "kya", "hai", "hain", "kaise", "kese", "batao", "bataiye", "batayein", "chahiye",
        "namaste", "mere", "meri", "mera", "mujhe", "liye", "kisko", "kitna", "kitne",
        "milega", "milegi", "dastavej", "patrata", "labh", "fayde", "fayda", "kare",
        "karein", "karna", "aavedan", "kisan", "kheti", "sarkari", "yojana", "paise",
        "paisa", "rupaye", "ghar", "makan", "dukan", "naukri", "chhatravritti", "shiksha",
        "swasthya", "ilaj", "dawa", "bima", "berojgar", "silai", "karigar", "beti", "ladki"
    ]
    if any(re.search(r"\\b" + re.escape(w) + r"\\b", lower) for w in hindi_keywords):
        return "hi-IN"

    if fallback_lang and fallback_lang not in ("en", "en-IN", "en-US"):
        return fallback_lang

    return "en-IN"


'''
    code = code[:d_start] + new_detect_lang + code[d_end:]
    print("Updated detect_message_language cleanly")

# 7. Update _search_schemes with HINDI_HINGLISH_STOPWORDS
stop_words_block = '''HINDI_HINGLISH_STOPWORDS = {
    "the", "for", "and", "about", "yojana", "scheme", "sarkari", "govt", "government",
    "meri", "mera", "mere", "mujhe", "mujhko", "hum", "hume", "apna", "apne", "apni",
    "aap", "aapka", "aapki", "aapke", "tum", "tumhara", "kya", "hai", "hain", "ho", "hoon", "hu",
    "tha", "thee", "the", "hoga", "hogi", "hoge", "batao", "bataiye", "batayein", "batana",
    "chahiye", "chaho", "saal", "sal", "umar", "aayu", "age", "kaise", "kese", "liye", "ko", "se", "me", "mein",
    "par", "pe", "tak", "aur", "bhi", "ya", "na", "nahi", "wala", "wali", "wale", "waliyo",
    "kare", "karein", "karna", "karne", "konsi", "kaunsi", "koun", "kaun", "kisko", "kise",
    "kitna", "kitne", "kitni", "milega", "milegi", "milege", "milta", "milti", "milte",
    "namaste", "hello", "sir", "madam", "ji", "kripya", "please", "help", "jankari", "info",
    "details", "de", "do", "dijiye", "bata", "pata", "kaunsa", "bhi", "batado"
}

'''

if "HINDI_HINGLISH_STOPWORDS" not in code:
    code = code.replace("def _search_schemes(", stop_words_block + "def _search_schemes(")

code = code.replace(
    'noise = {"the", "for", "and", "about", "yojana", "scheme", "sarkari", "govt", "government"}',
    'noise = HINDI_HINGLISH_STOPWORDS'
)
print("Updated noise filtering in _search_schemes")

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved updated assistant_agent.py")
