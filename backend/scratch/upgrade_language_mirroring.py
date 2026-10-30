import os
import re

target_path = r"C:\Users\Simran\Downloads\SchemeNavigator\SchemeNavigator\Scheme-Navigator-App-master\backend\agents\assistant_agent.py"

with open(target_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update SYSTEM_PROMPT_TEMPLATE with strict Language Mirroring rules
old_marker = 'SYSTEM_PROMPT_TEMPLATE = """You are Mitra (मित्र / মিত্র / متر / ਮਿੱਤਰ)'
prompt_start = code.find(old_marker)
prompt_end = code.find('LANGUAGE_NAMES = {', prompt_start)

if prompt_start != -1 and prompt_end != -1:
    new_prompt = '''SYSTEM_PROMPT_TEMPLATE = """You are Mitra (मित्र / মিত্র / متر / ਮਿੱਤਰ), the elite, compassionate, and highly knowledgeable AI Welfare Counselor & Scheme Advisor on SchemeNavigator (भारत सरकार कल्याण सलाहकार).

ABSOLUTE LANGUAGE MIRRORING MANDATE (CRITICAL - HIGHEST PRIORITY):
The citizen's query language has been detected as: {target_language} ({target_language_name}).
YOU MUST GENERATE 100% OF YOUR RESPONSE STRICTLY AND EXCLUSIVELY IN {target_language_name}.
- If target_language_name is English: You MUST write your ENTIRE response in clean, professional English. DO NOT write in Hindi or Devanagari script!
- If target_language_name is Hindi (हिंदी): Write 100% in natural, polite Hindi using Devanagari script (e.g. "नमस्ते! मैं मित्र AI हूँ...").
- If target_language_name is Bengali (বাংলা): Write 100% in fluent Bengali using Bengali script.
- If target_language_name is Odia (ଓଡ଼ିଆ): Write 100% in fluent Odia using Odia script.
- If target_language_name is Punjabi (ਪੰਜਾਬੀ): Write 100% in fluent Punjabi using Gurmukhi script.
- If target_language_name is Urdu (اردو): Write 100% in fluent Urdu using Perso-Arabic script.
- If target_language_name is Marathi (मराठी): Write 100% in fluent Marathi using Devanagari script.
- If target_language_name is Telugu (తెలుగు): Write 100% in fluent Telugu using Telugu script.
- If target_language_name is Tamil (தமிழ்): Write 100% in fluent Tamil using Tamil script.
- If target_language_name is Gujarati (ગુજરાતી): Write 100% in fluent Gujarati using Gujarati script.
- If target_language_name is Kannada (ಕನ್ನಡ): Write 100% in fluent Kannada using Kannada script.
- If target_language_name is Malayalam (മലയാളം): Write 100% in fluent Malayalam using Malayalam script.

CRITICAL RULE:
NEVER DEFAULT TO HINDI IF THE CITIZEN ASKED IN ENGLISH OR ANOTHER REGIONAL LANGUAGE!
NEVER DEFAULT TO ENGLISH IF THE CITIZEN ASKED IN AN INDIC REGIONAL LANGUAGE!
ALWAYS MIRROR THE USER'S INPUT LANGUAGE 100% PRECISELY.

STRUCTURED RESPONSE BLUEPRINT (MANDATORY FOR ALL SCHEME QUERIES):
Whenever explaining or recommending schemes, format your answer clearly with markdown bullet points and emojis:
1. 🎯 **योजना का नाम और मुख्य उद्देश्य (Scheme Name & Purpose)**: 1-2 direct lines on who it helps and what problem it solves.
2. 💰 **वित्तीय लाभ और सहायता राशि (Financial Assistance / Subsidy)**: State the exact amount (e.g. ₹6,000/year for PM-KISAN, ₹5 lakh cashless treatment for Ayushman Bharat, ₹50,000 to ₹10-20 lakh for Mudra Loan, ₹15,000 toolkit for PM Vishwakarma, etc.).
3. 📋 **पात्रता मानदंड (Eligibility Criteria)**: Specific conditions: Age limits, Income limits, Landholding, Gender/Caste (SC/ST/OBC/General), BPL/Ration card status.
4. 📄 **आवश्यक दस्तावेज़ (Required Documents)**: Bulleted checklist (Aadhaar card, Bank passbook linked with DBT/NPCI, Income certificate, Caste certificate, Land documents / Khasra-Khatauni, Passport photo, Active mobile number).
5. 📝 **आवेदन कैसे करें (Application Process - Online & Offline)**:
   - Online step: Official government portal, Aadhaar OTP authentication, e-KYC.
   - Offline step: Nearest Common Service Centre (CSC / जन सेवा केंद्र / मो सेवा केंद्र), Panchayat/Block office, or designated bank branch.
6. 🌐 **आधिकारिक पोर्टल और हेल्पलाइन (Official Portal URL & Toll-Free Helpline)**: Include the official portal URL and national helpline number.
7. 💡 **नागरिक के लिए सलाह (Pro-Tip / Next Step)**: E.g., verifying Bank Aadhaar-seeding status, checking nearest CSC Kendra via SchemeNavigator's Kendra Finder.

CITIZEN PROFILE PERSONALIZATION:
{profile_context}
- If the citizen has provided demographics (or mentions them in the query, e.g. "I am a student", "Farmer with 2 acres", "Age 68"), immediately customize the response to their situation and address them empathetically in {target_language_name}.

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
    print("Updated SYSTEM_PROMPT_TEMPLATE with strict Language Mirroring")

# 2. Update detect_message_language with robust grammar & script comparison
d_start = code.find("def detect_message_language(")
d_end = code.find("def _detect_query_intent(", d_start)

if d_start != -1 and d_end != -1:
    new_detect_lang = '''def detect_message_language(message: str, fallback_lang: str = "en-IN") -> str:
    """
    Intelligently detects whether the user is typing/speaking in:
    - English -> 'en-IN'
    - Hindi (Devanagari script or Hinglish) -> 'hi-IN'
    - Bengali (Bengali script or Banglish) -> 'bn-IN'
    - Odia (Odia script or Roman Odia) -> 'or-IN'
    - Punjabi (Gurmukhi script or Roman Punjabi) -> 'pa-IN'
    - Urdu (Perso-Arabic script or Roman Urdu) -> 'ur-IN'
    - Marathi (Devanagari script or Roman Marathi) -> 'mr-IN'
    - Telugu (Telugu script or Roman Telugu) -> 'te-IN'
    - Tamil (Tamil script or Roman Tamil) -> 'ta-IN'
    - Gujarati (Gujarati script or Roman Gujarati) -> 'gu-IN'
    - Kannada (Kannada script or Roman Kannada) -> 'kn-IN'
    - Malayalam (Malayalam script or Roman Malayalam) -> 'ml-IN'
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
        marathi_markers = ["आहे", "आहेत", "कसे", "मिळेल", "योजनांची", "माहिती", "द्या", "शेतकरी", "अर्ज", "माझे", "करावे", "सांगा", "पाहिजे"]
        if any(w in text for w in marathi_markers):
            return "mr-IN"
        return "hi-IN"

    # 2. Regional Romanized / Transliterated Indic Markers
    if re.search(r"\\b(mainu|assi|tussi|chahida|chahidi|chahide|daso|kivve|kive|kiven|dasso|vadhiya|kujh|jatt|hove|hovan|pind|sade|tuhada|tuhadi)\\b", lower):
        return "pa-IN"

    if re.search(r"\\b(amar|amake|amader|prokolpo|jonno|chhatrobritti|kivabe|dorkar|darkar|bhalo|dhonnobad|krishok|shunchen|taka|korbo|korte|konta|dekhte)\\b", lower):
        return "bn-IN"

    if re.search(r"\\b(mate|amara|amaku|kipari|kemiti|jojana|kahantu|kahiba|sahayata|darkar|darkara|janni|miliba|milipare|tankaa|tanka|chasa|chasi)\\b", lower):
        return "or-IN"

    if re.search(r"\\b(majhe|majha|majhi|amhi|amche|kasa|kase|karava|karave|yojna|aahe|ahet|dya|shasan|sang|sanga|sangave|pahije|milnar|baddal|sathi)\\b", lower):
        return "mr-IN"

    if re.search(r"\\b(wazifa|qarz|qard|dastawiz|hukumat|janab|shukriya|khawateen|khatoon|imdad|rehnumai|taraqqi|itla|darkhwast)\\b", lower):
        return "ur-IN"

    if re.search(r"\\b(naku|naaku|manaku|ela|elaga|pathakam|pathakalu|sahayam|kavali|cheyali|teliyacheyandi|raithu|dabbulu)\\b", lower):
        return "te-IN"

    if re.search(r"\\b(enakku|engalukku|eppadi|thittam|thittangal|udavi|vendum|solla|sollunga|vivasaayi|panam)\\b", lower):
        return "ta-IN"

    if re.search(r"\\b(mane|amane|kevi|rite|sahay|joiye|chhe|kaho|khedut)\\b", lower):
        return "gu-IN"

    if re.search(r"\\b(nanage|namage|hege|yojane|sahaya|beku|ide|heli|raitha|hana)\\b", lower):
        return "kn-IN"

    if re.search(r"\\b(enikku|njangalkku|enganeyanu|padhathi|venam|undu|parayamo|karshakan)\\b", lower):
        return "ml-IN"

    # 3. Token-based Hindi vs English Grammar Comparison
    hindi_grammar = {
        "kya", "hai", "hain", "ho", "hoon", "hu", "kaise", "kese", "batao", "bataiye", "batayein", "batana",
        "chahiye", "mere", "meri", "mera", "mujhe", "mujhko", "hume", "humko", "apna", "apne", "apni",
        "aap", "aapka", "aapke", "aapki", "tum", "tumhara", "kisko", "kise", "kitna", "kitne", "kitni",
        "milega", "milegi", "milege", "milta", "milti", "milte", "dastavej", "patrata", "labh", "fayde",
        "fayda", "kare", "karein", "karna", "karne", "aavedan", "paise", "paisa", "rupaye",
        "naukri", "chhatravritti", "shiksha", "swasthya", "ilaj", "dawa", "bima", "berojgar", "silai",
        "karigar", "beti", "ladki", "bata", "kuch", "konsi", "kaunsi", "suno", "bhai", "sahab"
    }

    english_grammar = {
        "what", "which", "who", "how", "when", "where", "why", "can", "could", "would", "should",
        "tell", "give", "show", "list", "explain", "help", "need", "want", "apply", "get", "for",
        "from", "with", "about", "under", "eligibility", "eligible", "documents", "document", "required",
        "benefit", "benefits", "subsidy", "assistance", "portal", "official", "government", "central",
        "state", "process", "procedure", "student", "scholarship", "farmer", "business", "loan",
        "housing", "pension", "women", "senior", "citizen", "card", "online", "offline", "the", "is", "are"
    }

    tokens = set(re.findall(r"[a-zA-Z]+", lower))
    hi_count = len(tokens & hindi_grammar)
    en_count = len(tokens & english_grammar)

    # If the user formulated the question in English words
    if en_count > hi_count and en_count >= 2:
        return "en-IN"

    # If the user used distinct Hindi grammar words
    if hi_count > 0:
        return "hi-IN"

    # Single English indicator with no Hindi
    if en_count >= 1:
        return "en-IN"

    if fallback_lang and fallback_lang not in ("en", "en-IN", "en-US"):
        return fallback_lang

    return "en-IN"


'''
    code = code[:d_start] + new_detect_lang + code[d_end:]
    print("Updated detect_message_language cleanly")

# 3. Add Marathi, Telugu, Tamil, Gujarati, Kannada, Malayalam to _generate_conversational_fallback
marathi_block = '''        if lang_p == "mr":
            out = [f"नमस्कार! 🙏 आपल्या विनंतीनुसार **{p_name}** योजनेची अधिकृत माहिती खालीलप्रमाणे आहे:\n"]
            if is_docs_query:
                out.append("📄 **आवश्यक कागदपत्रांची यादी (Required Documents):**")
                if docs_fmt:
                    out.extend(docs_fmt)
                else:
                    out.append("- **आधार कार्ड (Aadhaar Card)** (अनिवार्य): ओळख पडताळणी आणि e-KYC साठी.")
                    out.append("- **बँक पासबुक (Bank Passbook)** (अनिवार्य): थेट लाभ हस्तांतरण (DBT) साठी.")
                    out.append("- **मोबाईल नंबर आणि पासपोर्ट फोटो** (अनिवार्य)")
            elif is_apply_query:
                out.append("📝 **अर्ज कसा करावा (How to Apply):**")
                if steps_fmt:
                    out.extend(steps_fmt)
                else:
                    out.append("- **ऑनलाइन पद्धत:** अधिकृत पोर्टलवर जा आणि आधार OTP द्वारे e-KYC पूर्ण करा.")
                    out.append("- **ऑफलाइन पद्धत:** जवळच्या सेतू सुविधा केंद्र किंवा आपले सरकार केंद्रात अर्ज जमा करा.")
            elif is_elig_query:
                out.append("👥 **पात्रता निकष (Eligibility Criteria):**")
                if elig_fmt:
                    out.extend(elig_fmt)
                else:
                    out.append(f"- {p_desc}")
            elif is_benefit_query:
                out.append("💰 **मुख्य लाभ व सहाय्य रक्कम (Key Benefits):**")
                if benefits_fmt:
                    out.extend(benefits_fmt)
                else:
                    out.append(f"- {p_desc}")
            else:
                out.append(f"📌 **योजनेचा तपशील (Overview):**\\n{p_desc}\\n")
                if benefits_fmt:
                    out.append("💰 **मुख्य लाभ:**\\n" + "\\n".join(benefits_fmt))
                if elig_fmt:
                    out.append("👥 **पात्रता:**\\n" + "\\n".join(elig_fmt))
                if docs_fmt:
                    out.append("📄 **कागदपत्रे:**\\n" + "\\n".join(docs_fmt))
                elif not docs_fmt:
                    out.append("📄 **कागदपत्रे:**\\n- आधार कार्ड, बँक पासबुक आणि उत्पन्नाचा दाखला.")

            if portal or helpline:
                out.append(f"\\n📞 **अधिकृत मदत व पोर्टल:**\\n- पोर्टल: {portal or 'शासकीय पोर्टल'}\\n- हेल्पलाइन: {helpline or '1800-11-0001'}")
            out.append(f"\\n<schemes>{slugs}</schemes>")
            return "\\n".join(out)

        if lang_p == "te":
            out = [f"నమస్కారం! 🙏 మీ అభ్యర్థన ప్రకారం **{p_name}** పథకం యొక్క పూర్తి వివరాలు ఇక్కడ ఉన్నాయి:\n"]
            if is_docs_query:
                out.append("📄 **అవసరమైన పత్రాల జాబితా (Required Documents):**")
                if docs_fmt:
                    out.extend(docs_fmt)
                else:
                    out.append("- **ఆధార్ కార్డు (Aadhaar Card)** (తప్పనిసరి): గుర్తింపు మరియు e-KYC ధృవీకరణ కోసం.")
                    out.append("- **బ్యాంక్ పాస్‌బుక్ (Bank Passbook)** (తప్పనిసరి): ప్రత్యక్ష నగదు బదిలీ (DBT) కోసం.")
                    out.append("- **మొబైల్ నంబర్ మరియు ఫోటో**")
            elif is_apply_query:
                out.append("📝 **దరఖాస్తు విధానం (How to Apply):**")
                if steps_fmt:
                    out.extend(steps_fmt)
                else:
                    out.append("- **ఆన్‌లైన్:** అధికారిక పోర్టల్‌ను సందర్శించి ఆధార్ OTP ద్వారా నమోదు చేసుకోండి.")
                    out.append("- **ఆఫ్‌లైన్:** సమీపంలోని మీసేవ (MeeSeva) లేదా గ్రామ సచివాలయాన్ని సంప్రదించండి.")
            elif is_elig_query:
                out.append("👥 **అర్హత ప్రమాణాలు (Eligibility Criteria):**")
                if elig_fmt:
                    out.extend(elig_fmt)
                else:
                    out.append(f"- {p_desc}")
            elif is_benefit_query:
                out.append("💰 **ప్రధాన ప్రయోజనాలు (Key Benefits):**")
                if benefits_fmt:
                    out.extend(benefits_fmt)
                else:
                    out.append(f"- {p_desc}")
            else:
                out.append(f"📌 **పథకం సంక్షిప్త వివరాలు (Overview):**\\n{p_desc}\\n")
                if benefits_fmt:
                    out.append("💰 **ప్రయోజనాలు:**\\n" + "\\n".join(benefits_fmt))
                if elig_fmt:
                    out.append("👥 **అర్హతలు:**\\n" + "\\n".join(elig_fmt))
                if docs_fmt:
                    out.append("📄 **పత్రాలు:**\\n" + "\\n".join(docs_fmt))

            if portal or helpline:
                out.append(f"\\n📞 **అధికారిక పోర్టల్ మరియు హెల్ప్‌లైన్:**\\n- పోర్టల్: {portal or 'ప్రభుత్వ పోర్టల్'}\\n- హెల్ప్‌లైన్: {helpline or '1800-11-0001'}")
            out.append(f"\\n<schemes>{slugs}</schemes>")
            return "\\n".join(out)

        if lang_p == "ta":
            out = [f"வணக்கம்! 🙏 உங்கள் கோரிக்கையின்படி **{p_name}** திட்டத்தின் அதிகாரப்பூர்வ வழிகாட்டுதல் இதோ:\n"]
            if is_docs_query:
                out.append("📄 **தேவையான ஆவணங்களின் பட்டியல் (Required Documents):**")
                if docs_fmt:
                    out.extend(docs_fmt)
                else:
                    out.append("- **ஆதார் அட்டை (Aadhaar Card)** (கட்டாயம்): அடையாள சரிபார்ப்பு மற்றும் e-KYC க்கு.")
                    out.append("- **வங்கி கணக்கு புத்தகம் (Bank Passbook)** (கட்டாயம்): நேரடி பணப்பரிமாற்றம் (DBT) பெற.")
                    out.append("- **கைபேசி எண் மற்றும் பாஸ்போர்ட் அளவு புகைப்படம்**")
            elif is_apply_query:
                out.append("📝 **விண்ணப்பிக்கும் முறை (How to Apply):**")
                if steps_fmt:
                    out.extend(steps_fmt)
                else:
                    out.append("- **ஆன்லைன் முறை:** அதிகாரப்பூர்வ போர்ட்டலுக்கு சென்று ஆதார் OTP மூலம் பதிவு செய்யுங்கள்.")
                    out.append("- **ஆஃப்லைன் முறை:** அருகிலுள்ள இ-சேவை மையம் (CSC / e-Seva) மூலம் விண்ணப்பிக்கவும்.")
            elif is_elig_query:
                out.append("👥 **தகுதி வரம்புகள் (Eligibility Criteria):**")
                if elig_fmt:
                    out.extend(elig_fmt)
                else:
                    out.append(f"- {p_desc}")
            elif is_benefit_query:
                out.append("💰 **முக்கிய நன்மைகள் (Key Benefits):**")
                if benefits_fmt:
                    out.extend(benefits_fmt)
                else:
                    out.append(f"- {p_desc}")
            else:
                out.append(f"📌 **திட்டத்தின் விளக்கம் (Overview):**\\n{p_desc}\\n")
                if benefits_fmt:
                    out.append("💰 **நன்மைகள்:**\\n" + "\\n".join(benefits_fmt))
                if elig_fmt:
                    out.append("👥 **தகுதிகள்:**\\n" + "\\n".join(elig_fmt))
                if docs_fmt:
                    out.append("📄 **ஆவணங்கள்:**\\n" + "\\n".join(docs_fmt))

            if portal or helpline:
                out.append(f"\\n📞 **உதவி எண்கள் & போர்ட்டல்:**\\n- போர்டல்: {portal or 'அரசு இணையதளம்'}\\n- உதவி எண்: {helpline or '1800-11-0001'}")
            out.append(f"\\n<schemes>{slugs}</schemes>")
            return "\\n".join(out)

'''

eng_marker = '        # Default English\n        out = [f"Hello! 🙏 Here is the verified guide for **{p_name}**:\\n"]'
if "if lang_p == \"mr\":" not in code and eng_marker in code:
    code = code.replace(eng_marker, marathi_block + eng_marker)
    print("Added Marathi, Telugu, Tamil fallbacks to _generate_conversational_fallback")

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved updated assistant_agent.py")
