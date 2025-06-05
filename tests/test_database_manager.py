from ai_research_agent import DatabaseManager, PageInfo


def test_save_and_load_page(tmp_path):
    db_path = tmp_path / "test.db"
    db = DatabaseManager(str(db_path))
    page = PageInfo(
        url="http://example.com",
        title="Example",
        screenshot_path="path/to/screenshot.png",
        text="sample text",
        parent_url=None,
    )
    db.save_page(page)

    cur = db.conn.cursor()
    cur.execute(
        "SELECT url, title, screenshot_path, text, parent_url FROM pages WHERE url=?",
        (page.url,),
    )
    row = cur.fetchone()
    assert row == (
        page.url,
        page.title,
        page.screenshot_path,
        page.text,
        page.parent_url,
    )
