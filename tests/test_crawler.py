from ai_research_agent import WebCrawler


def test_sanitize_filename() -> None:
    name = WebCrawler._sanitize_filename("https://example.com/a?b=1")
    assert "https:" not in name
    assert "/" not in name


def test_crawl_no_driver(monkeypatch):
    crawler = WebCrawler()
    # Force driver to None to simulate missing Selenium
    crawler.driver = None
    pages = crawler.crawl(["test"], limit=1)
    assert pages == []
