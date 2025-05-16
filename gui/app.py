import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QCheckBox,
                             QPushButton, QVBoxLayout, QMessageBox, QListWidget)
from PyQt5.QtGui import QDoubleValidator
from core.book import Book
from core.library import DigitalLibrary

class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.library = DigitalLibrary()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 500, 500)

        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.isbn_input = QLineEdit()
        self.size_input = QLineEdit()
        self.size_input.setValidator(QDoubleValidator(0.0, 10000.0, 2))
        self.size_input.setDisabled(True)

        self.ebook_check = QCheckBox("eBook?")
        self.ebook_check.stateChanged.connect(self.toggle_size)

        self.list_widget = QListWidget()

        add_btn = QPushButton("Add Book")
        add_btn.clicked.connect(self.add_book)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Title"))
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Author"))
        layout.addWidget(self.author_input)
        layout.addWidget(QLabel("ISBN"))
        layout.addWidget(self.isbn_input)
        layout.addWidget(self.ebook_check)
        layout.addWidget(QLabel("Download Size (MB)"))
        layout.addWidget(self.size_input)
        layout.addWidget(add_btn)
        layout.addWidget(QLabel("Available Books"))
        layout.addWidget(self.list_widget)

        self.setLayout(layout)
        self.update_list()

    def toggle_size(self):
        self.size_input.setDisabled(not self.ebook_check.isChecked())

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        isbn = self.isbn_input.text()
        size = self.size_input.text()
        is_ebook = self.ebook_check.isChecked()

        if not title or not author or not isbn:
            QMessageBox.warning(self, "Error", "All fields except size are required.")
            return

        try:
            if is_ebook:
                if not size:
                    QMessageBox.warning(self, "Error", "Download size is required.")
                    return
                self.library.add_ebook(Book(title, author, isbn), float(size))
            else:
                self.library.add_book(Book(title, author, isbn))
            self.update_list()
            QMessageBox.information(self, "Success", "Book added successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_list(self):
        self.list_widget.clear()
        for book in self.library:
            self.list_widget.addItem(str(book))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LibraryApp()
    win.show()
    sys.exit(app.exec_())
