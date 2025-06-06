import sys
import threading

from ai_research_agent import ResearchAgent

try:
    from PyQt6.QtWidgets import (
        QApplication,
        QWidget,
        QVBoxLayout,
        QLineEdit,
        QPushButton,
        QTextEdit,
    )
except Exception:  # pragma: no cover - PyQt6 may not be installed
    print("PyQt6 is required to run the GUI. Please install it and try again.")
    sys.exit(1)


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("AI Research Agent")
        self.agent = ResearchAgent()
        self.worker: threading.Thread | None = None

        self.input = QLineEdit()
        self.input.setPlaceholderText("調査テーマを入力")
        self.start_button = QPushButton("Start")
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.log)
        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_agent)

    def start_agent(self) -> None:
        theme = self.input.text().strip()
        if not theme:
            self.log.append("テーマを入力してください。")
            return
        self.start_button.setEnabled(False)

        def run_agent() -> None:
            self.log.append(f"テーマ '{theme}' で調査を開始します")
            try:
                self.agent.run(theme)
                self.log.append("調査が完了しました")
            except Exception as e:  # pragma: no cover - runtime errors
                self.log.append(f"エラー: {e}")
            self.start_button.setEnabled(True)

        self.worker = threading.Thread(target=run_agent, daemon=True)
        self.worker.start()

    def closeEvent(self, event) -> None:  # pragma: no cover - GUI interaction
        self.agent.close()
        super().closeEvent(event)


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":  # pragma: no cover - manual launch
    main()
