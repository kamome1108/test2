from ai_research_agent import KeywordExtractor


def test_generate_returns_keywords():
    extractor = KeywordExtractor()
    result = extractor.generate("test")
    assert result[0] == "test"
    assert len(result) >= 2
