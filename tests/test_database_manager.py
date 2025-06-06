from ai_research_agent import DatabaseManager, PageInfo


def test_save_and_get_page(tmp_path):
    db_file = tmp_path / "test.db"
    with DatabaseManager(str(db_file)) as db:
        page = PageInfo(
            url="http://example.com", title="Example", screenshot_path="ex.png"
        )
        db.save_page(page)
        retrieved = db.get_page("http://example.com")
        assert retrieved is not None
        assert retrieved.url == page.url
        assert retrieved.title == page.title
