"""
Unit tests for api/intent_router.py
"""

import pytest
from api.intent_router import classify, route_message
from api.config_loader import load_site_config


@pytest.fixture
def kkr_config():
    """Load KKR site config for testing."""
    return load_site_config("kkr")


class TestClassify:
    """Tests for intent classification."""

    def test_classify_greeting_hello(self, kkr_config):
        """Test greeting classification."""
        result = classify("Hello", kkr_config)
        assert result["type"] == "greeting"

    def test_classify_greeting_hi(self, kkr_config):
        """Test greeting classification."""
        result = classify("Hi there", kkr_config)
        assert result["type"] == "greeting"

    def test_classify_greeting_good_morning(self, kkr_config):
        """Test greeting classification."""
        result = classify("Good morning", kkr_config)
        assert result["type"] == "greeting"

    def test_classify_dynamic_careers(self, kkr_config):
        """Test dynamic classification - careers."""
        result = classify("Are there any open positions?", kkr_config)
        assert result["type"] == "dynamic"
        assert result["category"] == "careers"

    def test_classify_dynamic_jobs(self, kkr_config):
        """Test dynamic classification - jobs."""
        result = classify("Are you hiring?", kkr_config)
        assert result["type"] == "dynamic"
        assert result["category"] == "careers"

    def test_classify_dynamic_news(self, kkr_config):
        """Test dynamic classification - news."""
        result = classify("What's the latest news?", kkr_config)
        assert result["type"] == "dynamic"
        assert result["category"] == "news"

    def test_classify_stable_default(self, kkr_config):
        """Test stable classification (default)."""
        result = classify("What is KKR's investment approach?", kkr_config)
        assert result["type"] == "stable"

    def test_classify_empty_message(self, kkr_config):
        """Test empty message classification."""
        result = classify("", kkr_config)
        assert result["type"] == "stable"

    def test_classify_case_insensitive(self, kkr_config):
        """Test case-insensitive classification."""
        result = classify("HELLO", kkr_config)
        assert result["type"] == "greeting"


class TestRouteMessage:
    """Tests for message routing."""

    def test_route_greeting(self, kkr_config):
        """Test routing for greeting."""
        classification = {"type": "greeting"}
        routing = route_message("Hello", classification, kkr_config)
        assert routing["handler"] == "canned"
        assert "reply" in routing

    def test_route_dynamic(self, kkr_config):
        """Test routing for dynamic message."""
        classification = {
            "type": "dynamic",
            "category": "careers",
            "url": "/careers",
            "selector": ".job-listing, .career-card, [data-job-item], .job-item",
        }
        routing = route_message("Are you hiring?", classification, kkr_config)
        assert routing["handler"] == "tool"
        # "careers" category maps to the actual registered tool, get_open_positions
        assert routing["tool_name"] == "get_open_positions"
        assert "tool_config" in routing

    def test_route_stable(self, kkr_config):
        """Test routing for stable message."""
        classification = {"type": "stable"}
        routing = route_message("What is KKR's investment approach?", classification, kkr_config)
        assert routing["handler"] == "rag"
        assert routing["query"] == "What is KKR's investment approach?"

    def test_route_preserves_dynamic_config(self, kkr_config):
        """Test that routing preserves dynamic page config."""
        classification = {
            "type": "dynamic",
            "category": "news",
            "url": "/insights",
            "selector": ".article-card, .blog-post, [data-article-item], .news-item, .insight-card",
        }
        routing = route_message("News?", classification, kkr_config)
        tool_config = routing["tool_config"]
        assert tool_config["url"] == "/insights"
        assert tool_config["selector"] == ".article-card, .blog-post, [data-article-item], .news-item, .insight-card"
        assert tool_config["category"] == "news"
