# coding: utf-8
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from product_viewer.actions import ExitAction
from product_viewer.actions import UploadAction
from product_viewer.settings import SettingsAction
from product_viewer.store import RedisStore


class MainToolBar(QToolBar):
    """Fixed toolbar with app name and a few buttons."""

    def __init__(self, *args):
        super(MainToolBar, self).__init__(*args)
        self.setFloatable(False)
        self.setMovable(False)
        self.addWidget(QLabel('Product Viewer'))
        self.addSeparator()

        main_window = self.parent()

        self.addActions((
            UploadAction('Upload', main_window),
            SettingsAction('Settings', main_window),
            ExitAction('Exit', main_window),
        ))


class ProductTable(QTableWidget):
    """Table widget filled with data from store."""

    def __init__(self, *args):
        super(ProductTable, self).__init__(*args)

        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(('Model', 'Category', 'Price'))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def reload(self, data):
        """Redrawing table."""

        # Cleaning up old data
        self.setRowCount(15)

        for row_count, row in enumerate(data):
            for cell_count, cell in enumerate(row):
                self.setItem(row_count, cell_count, QTableWidgetItem(cell))


class MainWindow(QMainWindow):
    """App window."""

    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.store = RedisStore()

        self.addToolBar(MainToolBar(self))
        self.setStatusBar(QStatusBar(self))
        self.resize(400, 600)
        self.move(300, 300)
        self.setWindowTitle('Product Viewer')

        self.table = ProductTable()
        self.table.reload(data=self.store.load())

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.table)
        self.setCentralWidget(self.central_widget)

        self.show()


if __name__ == '__main__':
    import sys

    app = QApplication([])
    window = MainWindow()

    sys.exit(app.exec_())
