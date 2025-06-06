from ai_research_agent import ResearchAgent, PageInfo


def test_run_with_threads(monkeypatch, tmp_path):
    agent = ResearchAgent()

    dummy_page = PageInfo(url="http://a", title="A", screenshot_path="a.png")

    def fake_crawl(keywords, limit=5):
        return [dummy_page]

    def fake_extract_text(page):
        return "text"

    def fake_summarize(text, max_sentences=3):
        return "summary"

    monkeypatch.setattr(agent.crawler, "crawl", fake_crawl)
    monkeypatch.setattr(agent.ocr, "extract_text", fake_extract_text)
    monkeypatch.setattr(agent.summarizer, "summarize", fake_summarize)

    db_file = tmp_path / "db.sqlite"
    agent.db = agent.db.__class__(str(db_file))

    try:
        agent.run("theme", use_threads=True)
    finally:
        agent.close()

    with agent.db.__class__(str(db_file)) as db:
        pages = db.list_pages()
        assert len(pages) == 1
