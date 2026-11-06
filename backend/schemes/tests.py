from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Scheme


class SchemeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.scheme1 = Scheme.objects.create(
            slug="pm-kisan-test",
            name="PM Kisan Samman Nidhi",
            short_name="PM-KISAN",
            tagline="Income support for farmers",
            category="Agriculture",
            level="Central",
            covered_states=["All India"],
            short_description="Financial benefit of Rs 6000 per year to farmers.",
            detailed_description="Detailed guidelines for PM Kisan Samman Nidhi.",
            eligibility={"minAge": 18, "maxAge": 100},
            benefits=[{"title": "Rs 6000/year", "amount": 6000}],
            documents=[{"name": "Aadhaar Card"}],
            application_steps=[{"stepNumber": 1, "title": "Apply online"}],
            verification={"isOfficialVerified": True},
            popular_score=95.0,
            tags=["farmer", "agriculture", "financial assistance"],
        )

        self.scheme2 = Scheme.objects.create(
            slug="odisha-kalia-test",
            name="KALIA Scheme",
            short_name="KALIA",
            tagline="Livelihood support for farmers in Odisha",
            category="Agriculture",
            level="State",
            covered_states=["Odisha"],
            short_description="Financial assistance for farmers in Odisha state.",
            detailed_description="Detailed guidelines for KALIA scheme.",
            eligibility={"minAge": 18, "maxAge": 100},
            benefits=[{"title": "Financial aid", "amount": 10000}],
            documents=[{"name": "Ration Card"}],
            application_steps=[{"stepNumber": 1, "title": "Visit portal"}],
            verification={"isOfficialVerified": True},
            popular_score=80.0,
            tags=["farmer", "odisha"],
        )

        self.scheme3 = Scheme.objects.create(
            slug="post-matric-scholarship-test",
            name="Post Matric Scholarship",
            short_name="PMS",
            tagline="Scholarship for higher education",
            category="Education",
            level="Central",
            covered_states=["All India"],
            short_description="Scholarships for students pursuing post-matric courses.",
            detailed_description="Education support for college students.",
            eligibility={"minAge": 15, "maxAge": 30},
            benefits=[{"title": "Tuition waiver"}],
            documents=[{"name": "Mark sheet"}],
            application_steps=[{"stepNumber": 1, "title": "National Scholarship Portal"}],
            verification={"isOfficialVerified": True},
            popular_score=75.0,
            tags=["student", "education", "scholarship"],
        )

    @patch("schemes.views._fetch_live_apimitra", return_value=None)
    def test_list_all_schemes(self, mock_fetch):
        """GET /api/schemes/ should return paginated schemes and category counts."""
        res = self.client.get("/api/schemes/?limit=10")
        self.assertEqual(res.status_code, 200)
        data = res.data
        self.assertIn("schemes", data)
        self.assertIn("categoryCounts", data)
        self.assertGreaterEqual(len(data["schemes"]), 3)

    @patch("schemes.views._fetch_live_apimitra", return_value=None)
    def test_filter_by_category(self, mock_fetch):
        """GET /api/schemes/?category=Education should return only Education schemes."""
        res = self.client.get("/api/schemes/?category=Education")
        self.assertEqual(res.status_code, 200)
        schemes = res.data.get("schemes", [])
        self.assertTrue(all(s["category"] == "Education" for s in schemes))

    @patch("schemes.views._fetch_live_apimitra", return_value=None)
    def test_filter_by_state(self, mock_fetch):
        """GET /api/schemes/?state=Odisha should include All India and Odisha-specific schemes."""
        res = self.client.get("/api/schemes/?state=Odisha")
        self.assertEqual(res.status_code, 200)
        slugs = [s["slug"] for s in res.data.get("schemes", [])]
        self.assertIn("pm-kisan-test", slugs)
        self.assertIn("odisha-kalia-test", slugs)

    def test_scheme_detail_by_slug(self):
        """GET /api/schemes/<slug>/ should return scheme details."""
        res = self.client.get("/api/schemes/pm-kisan-test/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.get("slug"), "pm-kisan-test")
        self.assertEqual(res.data.get("name"), "PM Kisan Samman Nidhi")

    def test_scheme_detail_nonexistent(self):
        """GET /api/schemes/<unknown>/ should return 404."""
        res = self.client.get("/api/schemes/this-scheme-does-not-exist-at-all/")
        self.assertEqual(res.status_code, 404)
