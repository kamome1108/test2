# AI Research Agent

This repository contains a prototype implementation of the personal AI research agent.
For an overview of the planned features, see [design.md](design.md).

Captured pages are processed with OCR and a simple summarizer extracts the first
few sentences for storage.

The script is not fully functional by default. To try it locally, first set up a
Python virtual environment.

## Setup

Windows 環境では `setup.bat` を実行すると、`venv` フォルダーに仮想環境が作成され、
`requirements.txt` に記載された依存パッケージがインストールされます。

## Usage

セットアップ後は `run.bat` を実行してください。仮想環境を有効化した状態で
`ai_research_agent.py` を起動します。調査テーマは引数で指定できます。
GUI を使う場合は `run.bat gui` を実行するか、`python gui.py` を直接起動してください。

```cmd
run.bat "人工知能"
```

## Development

The following commands run formatting and tests:

```bash
ruff check .
black ai_research_agent.py tests/*.py --line-length 79 --check
pytest -q
```
