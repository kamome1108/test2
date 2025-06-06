from ai_research_agent import Summarizer


def test_summarize_first_sentences():
    s = Summarizer()
    text = "これはテストです。次の文です。最後です。"
    summary = s.summarize(text, max_sentences=2)
    assert "テスト" in summary
    assert "次の文" in summary
    assert "最後" not in summary


def test_summarize_empty_text():
    s = Summarizer()
    assert s.summarize("", max_sentences=2) == ""
