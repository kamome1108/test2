from ai_research_agent import KeywordExtractor


def test_generate_returns_theme():
    extractor = KeywordExtractor()
    result = extractor.generate("test")
    assert "test" in result
