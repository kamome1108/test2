# AI Research Agent

このリポジトリには、個人用AI研究エージェントの簡易プロトタイプ `ai_research_agent.py` が含まれています。
WebクロールやOCR処理などの流れを確認するためのサンプル実装です。

## セットアップ

Python 3.9 以上を推奨します。依存パッケージは `requirements.txt` に記載していますので、次のコマンドでまとめてインストールしてください。

```bash
pip install -r requirements.txt
```

`pytesseract` や `selenium` を利用する際は、Tesseract OCR の本体や WebDriver など、外部ツールのインストールも必要になります。

### OS 依存の注意点
- **macOS/Linux**: Tesseract OCR は各種パッケージマネージャーから導入できます。
  - macOS の例: `brew install tesseract`
  - Ubuntu の例: `sudo apt-get install tesseract-ocr`
- **Windows**: Tesseract をインストールしたら、環境変数 `TESSDATA_PREFIX` を設定してください。
- Selenium で Chrome を操作する場合は、各 OS 向けの ChromeDriver をダウンロードし `PATH` に追加します。

## 使い方

依存パッケージをそろえたら、以下のように実行できます。

```bash
python ai_research_agent.py
```

テスト用のテーマがあらかじめスクリプトに書かれているので、必要に応じて `agent.run("テスト")` の部分を変更してください。

## 実行例

環境に外部ツールを用意していない場合は、次のようにページ数 0 件で終了します。

```
Saved 0 pages to database.
```

実際にクロールや OCR を行う際は、上記の外部ツールをそれぞれ準備する必要があります。
