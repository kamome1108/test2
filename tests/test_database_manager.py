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


def test_list_and_export_csv(tmp_path):
    db_file = tmp_path / "test.db"
    export_file = tmp_path / "out.csv"
    with DatabaseManager(str(db_file)) as db:
        db.save_page(
            PageInfo(url="http://a", title="A", screenshot_path="a.png")
        )
        db.save_page(
            PageInfo(url="http://b", title="B", screenshot_path="b.png")
        )
        pages = db.list_pages()
        assert len(pages) == 2
        db.export_csv(str(export_file))
    assert export_file.exists()


def test_export_markdown(tmp_path):
    db_file = tmp_path / "test.db"
    md_file = tmp_path / "out.md"
    with DatabaseManager(str(db_file)) as db:
        db.save_page(
            PageInfo(
                url="http://a", title="A", screenshot_path="a.png", text="txt"
            )
        )
        db.export_markdown(str(md_file))
    assert md_file.exists()
