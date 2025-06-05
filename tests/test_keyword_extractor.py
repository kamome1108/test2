from ai_research_agent import KeywordExtractor

def test_generate_keywords():
    extractor = KeywordExtractor()
    result = extractor.generate("機械学習")
    assert result == ["機械学習"]
