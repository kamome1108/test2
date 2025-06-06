"""
Personal AI Research Agent
-------------------------
Skeleton implementation based on design document.
This script is not fully functional without additional setup.
"""

import os
import re
import sqlite3
from dataclasses import dataclass
from typing import List, Optional

# Placeholder imports for external libraries
try:
    from PyQt6 import QtWidgets
except ImportError:  # pragma: no cover - not installed in this environment
    QtWidgets = None

try:
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
except ImportError:  # pragma: no cover - not installed in this environment
    requests = None
    BeautifulSoup = None
    webdriver = None

try:
    import pytesseract
    from PIL import Image
except ImportError:  # pragma: no cover - not installed in this environment
    pytesseract = None
    Image = None


@dataclass
class PageInfo:
    url: str
    title: str
    screenshot_path: str
    text: str = ""
    parent_url: Optional[str] = None


class KeywordExtractor:
    def __init__(self, model_path: str = "path_to_local_llm"):
        self.model_path = model_path
        # TODO: Load local LLM here
        # e.g., transformers.AutoModel.from_pretrained(model_path)

    def generate(self, theme: str) -> List[str]:
        """Generate keyword candidates from a theme."""
        base = theme.strip()
        if not base:
            return []
        # Very simple placeholder generation. Real implementation would
        # use a local LLM to propose related keywords.
        return [base, f"{base} 研究", f"{base} ニュース"]


class WebCrawler:
    def __init__(self, output_dir: str = "captures"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.driver = None
        if webdriver:
            try:
                self.driver = webdriver.Chrome()
            except Exception:  # pragma: no cover - runtime setup may fail
                self.driver = None

    @staticmethod
    def _sanitize_filename(text: str) -> str:
        """Return a filesystem-safe representation of ``text``."""
        text = text.strip().replace("\\", "_").replace("/", "_")
        return re.sub(r"[^A-Za-z0-9_.-]", "_", text)

    def crawl(self, keywords: List[str], limit: int = 5) -> List[PageInfo]:
        """Search the web for each keyword and capture pages."""
        pages: List[PageInfo] = []
        if not self.driver or not requests:
            return pages

        for kw in keywords:
            resp = requests.get(f"https://www.google.com/search?q={kw}")
            soup = BeautifulSoup(resp.text, "html.parser")
            results = [a for a in soup.select("a") if a.get("href")][:limit]
            for link in results:
                url = link.get("href")
                title = link.text.strip() or url
                self.driver.get(url)
                filename = self._sanitize_filename(url) + ".png"
                screenshot_path = os.path.join(self.output_dir, filename)
                try:
                    self.driver.save_screenshot(screenshot_path)
                except Exception:  # pragma: no cover - webdriver failure
                    continue
                pages.append(
                    PageInfo(
                        url=url,
                        title=title,
                        screenshot_path=screenshot_path,
                        parent_url=None,
                    )
                )
        return pages

    def close(self) -> None:
        if self.driver:
            try:
                self.driver.quit()
            except Exception:  # pragma: no cover - driver may be dead
                pass


class OCRProcessor:
    def extract_text(self, page: PageInfo) -> str:
        """Run OCR on the screenshot and return text."""
        if pytesseract is None or Image is None:
            return ""
        img = Image.open(page.screenshot_path)
        text = pytesseract.image_to_string(img)
        return text


class Summarizer:
    def summarize(self, text: str, max_sentences: int = 3) -> str:
        """Return a naive summary using the first few sentences."""
        sentences = re.split(r"[。.!?]\s*", text)
        cleaned = [s.strip() for s in sentences if s.strip()]
        return "。".join(cleaned[:max_sentences])


class DatabaseManager:
    def __init__(self, db_path: str = "agent.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pages (
                url TEXT PRIMARY KEY,
                title TEXT,
                screenshot_path TEXT,
                text TEXT,
                parent_url TEXT
            )
            """
        )
        self.conn.commit()

    def list_pages(self) -> List[PageInfo]:
        """Return all stored pages."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT url, title, screenshot_path, text, parent_url FROM pages"
        )
        rows = cur.fetchall()
        return [PageInfo(*row) for row in rows]

    def export_csv(self, file_path: str) -> None:
        """Export all page records to a CSV file."""
        import csv

        pages = self.list_pages()
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["url", "title", "screenshot_path", "text", "parent_url"]
            )
            for p in pages:
                writer.writerow(
                    [p.url, p.title, p.screenshot_path, p.text, p.parent_url]
                )

    def export_markdown(self, file_path: str) -> None:
        """Export all page records to a Markdown file."""
        pages = self.list_pages()
        with open(file_path, "w", encoding="utf-8") as f:
            for p in pages:
                f.write(f"## {p.title}\n")
                f.write(f"[{p.url}]({p.url})\n\n")
                if p.text:
                    f.write(f"{p.text}\n\n")

    def get_page(self, url: str) -> Optional[PageInfo]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT url, title, screenshot_path, text, parent_url FROM pages WHERE url=?",
            (url,),
        )
        row = cur.fetchone()
        if row:
            return PageInfo(*row)
        return None

    def save_page(self, page: PageInfo) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT OR REPLACE INTO pages (url, title, screenshot_path, text, parent_url)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                page.url,
                page.title,
                page.screenshot_path,
                page.text,
                page.parent_url,
            ),
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "DatabaseManager":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


class ResearchAgent:
    def __init__(self) -> None:
        self.keyword_extractor = KeywordExtractor()
        self.crawler = WebCrawler()
        self.ocr = OCRProcessor()
        self.summarizer = Summarizer()
        self.db = DatabaseManager()

    def close(self) -> None:
        self.crawler.close()
        self.db.close()

    def run(
        self,
        theme: str,
        export_csv: Optional[str] = None,
        export_md: Optional[str] = None,
    ) -> None:
        keywords = self.keyword_extractor.generate(theme)
        pages = self.crawler.crawl(keywords)
        for page in pages:
            full_text = self.ocr.extract_text(page)
            page.text = self.summarizer.summarize(full_text)
            self.db.save_page(page)
        print(f"Saved {len(pages)} pages to database.")
        if export_csv:
            self.db.export_csv(export_csv)
            print(f"Exported results to {export_csv}")
        if export_md:
            self.db.export_markdown(export_md)
            print(f"Exported markdown to {export_md}")


if __name__ == "__main__":  # pragma: no cover - manual execution
    import argparse

    parser = argparse.ArgumentParser(description="Run research agent")
    parser.add_argument(
        "theme", nargs="?", default="テスト", help="Research theme"
    )
    parser.add_argument(
        "--export-csv", metavar="PATH", help="Export results to CSV"
    )
    parser.add_argument(
        "--export-md",
        metavar="PATH",
        help="Export results to a Markdown file",
    )
    args = parser.parse_args()

    agent = ResearchAgent()
    try:
        agent.run(
            args.theme,
            export_csv=args.export_csv,
            export_md=args.export_md,
        )
    finally:
        agent.close()
