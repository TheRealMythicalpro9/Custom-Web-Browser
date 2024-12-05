import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Styled Browser")
        self.setGeometry(200, 200, 1200, 800)
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        self.bookmarks = []

        # Create the initial tab
        self.add_tab()

        # URL input field
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter URL or Search")
        self.url_input.returnPressed.connect(self.load_url_from_input)

        # Bookmark button
        self.bookmark_button = QPushButton("Bookmark", self)
        self.bookmark_button.clicked.connect(self.add_bookmark)

        # Layout for URL input and bookmark button
        url_layout = QHBoxLayout()
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.bookmark_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(url_layout)
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        # Apply custom styles
        self.apply_styles()

    def add_tab(self, url=None):
        """Adds a new tab."""
        tab = QWidget()
        tab_layout = QVBoxLayout()

        # Create the web engine view for the tab
        webview = QWebEngineView()
        webview.setUrl(QUrl(url or "https://www.google.com"))
        tab_layout.addWidget(webview)

        tab.setLayout(tab_layout)
        tab_index = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(tab_index)

        # Update the URL input field when the tab URL changes
        webview.urlChanged.connect(lambda url: self.url_input.setText(url.toString()))

    def load_url_from_input(self):
        """Loads the URL entered in the input field."""
        url = self.url_input.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.add_tab(url)

    def add_bookmark(self):
        """Adds the current URL to the bookmark list."""
        current_url = self.url_input.text()
        if current_url not in self.bookmarks:
            self.bookmarks.append(current_url)
            print(f"Bookmarked: {current_url}")

    def apply_styles(self):
        """Applies custom styles to the browser."""
        style = """
            QMainWindow {
                background-color: #2E2E2E;
                color: #F0F0F0;
                font-size: 14px;
            }
            QTabWidget {
                background-color: #1D1D1D;
                border: 1px solid #444;
            }
            QTabBar::tab {
                background-color: #333;
                color: #FFF;
                padding: 5px;
                border: 1px solid #444;
            }
            QTabBar::tab:selected {
                background-color: #444;
            }
            QLineEdit {
                background-color: #333;
                color: #FFF;
                border: 1px solid #555;
                padding: 5px;
            }
            QPushButton {
                background-color: #444;
                color: #FFF;
                border: 1px solid #666;
                padding: 5px;
                margin: 3px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #666;
            }
        """
        self.setStyleSheet(style)

    def closeEvent(self, event):
        """Prompts the user to save bookmarks before closing."""
        if self.bookmarks:
            print("Bookmarks saved:", self.bookmarks)
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
