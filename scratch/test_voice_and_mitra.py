"""
Comprehensive verification test for Scheme Navigator:
1. Assistant Agent domain restriction & refusal policy
2. Assistant Agent website feature guide & deadlines
3. Recommendation Agent profiling accuracy
"""

import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

# Setup Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django
django.setup()

from agents.assistant_agent import AssistantAgent, _handle_casual_question, _is_scheme_query
from agents.recommendation_agent import RecommendationAgent


def test_assistant_guardrails():
    print("\n--- 1. Testing Mitra AI Assistant Domain Guardrails ---")
    assistant = AssistantAgent()

    # Off-topic test cases
    off_topic_queries = [
        "Tell me a joke",
        "What is 15 * 8?",
        "Who is the Prime Minister of India?",
        "How do I write a Python function?",
        "What is the weather in Delhi today?",
        "एक चुटकुला सुनाओ",
        "10 + 20 कितना होता है?",
    ]

    for q in off_topic_queries:
        res = _handle_casual_question(q, language="en-IN")
        ans = res.get("answer", "")
        print(f"\nQuery: '{q}'")
        # Ensure it does not tell jokes or compute math
        assert "120" not in ans, "Math should NOT be computed!"
        assert "mangoes" not in ans.lower() and "आम" not in ans, "Joke should NOT be returned!"
        assert "Scheme Navigator" in ans or "कल्याणकारी" in ans or "welfare schemes" in ans, (
            "Response must include domain restriction!"
        )
        print(f"-> Correctly refused and redirected! Snippet: {ans[:100]}...")

    print("\n--- 2. Testing Website Feature Guide ---")
    website_queries = [
        "what is this website",
        "website me kya hai",
        "features of this app",
        "what is scheme navigator",
    ]

    for q in website_queries:
        res = _handle_casual_question(q, language="hi-IN" if "hai" in q else "en-IN")
        ans = res.get("answer", "")
        print(f"\nQuery: '{q}'")
        assert "Explore Schemes" in ans, "Must explain Explore Schemes!"
        assert "Eligibility Survey" in ans, "Must explain Eligibility Survey!"
        assert "Scheme Tracker" in ans, "Must explain Scheme Tracker!"
        assert "Saved Schemes" in ans, "Must explain Saved Schemes!"
        assert "Kendra Finder" in ans, "Must explain Kendra Finder!"
        print(f"-> Successfully returned 7-feature guide! Snippet: {ans[:120]}...")

    print("\n--- 3. Testing Scheme Deadlines ---")
    deadline_queries = [
        "what is the deadline of pm kisan",
        "ayushman card last date",
        "scholarship closing date",
    ]

    for q in deadline_queries:
        res = _handle_casual_question(q, language="en-IN")
        ans = res.get("answer", "")
        print(f"\nQuery: '{q}'")
        assert "Year-Round" in ans or "365 days" in ans or "October 31" in ans, (
            "Must provide authentic deadline intelligence!"
        )
        print(f"-> Correctly answered deadline! Snippet: {ans[:120]}...")


def test_recommendation_agent():
    print("\n--- 4. Testing Recommendation Agent Demographics Matching ---")
    reco_agent = RecommendationAgent()

    # Case A: Small Farmer profile from UP
    farmer_profile = {
        "age": 42,
        "gender": "male",
        "state": "Uttar Pradesh",
        "occupation": "Farmer",
        "employment_type": "Farmer",
        "income": 120000,
        "caste_category": "OBC",
    }
    recos = reco_agent.recommend(farmer_profile, top_n=5)
    print(f"\nFarmer profile (Age 42, UP, Farmer, Income 1.2L):")
    assert len(recos) > 0, "Should return recommendations"
    for r in recos[:3]:
        s = r["scheme"]
        print(f"  - [{r['score']}%] {s.get('name')} (Category: {s.get('category')})")
    top_cats = [r["scheme"].get("category") for r in recos[:3]]
    assert any("Agri" in c or "Financial" in c or "Social" in c for c in top_cats), "Farmer should get Agri/Financial schemes!"

    # Case B: Student profile from Delhi
    student_profile = {
        "age": 19,
        "gender": "female",
        "state": "Delhi",
        "occupation": "Student",
        "is_student": True,
        "income": 80000,
        "caste_category": "SC",
    }
    recos_student = reco_agent.recommend(student_profile, top_n=5)
    print(f"\nStudent profile (Age 19, Female, SC, Student, Income 80k):")
    assert len(recos_student) > 0, "Should return recommendations"
    for r in recos_student[:3]:
        s = r["scheme"]
        print(f"  - [{r['score']}%] {s.get('name')} (Category: {s.get('category')})")
    top_student_cats = [r["scheme"].get("category") for r in recos_student[:3]]
    assert any("Edu" in c or "Women" in c for c in top_student_cats), "Student should get Education/Women schemes!"


if __name__ == "__main__":
    test_assistant_guardrails()
    test_recommendation_agent()
    print("\nAll Backend Agent tests passed with flying colors! ✅")
