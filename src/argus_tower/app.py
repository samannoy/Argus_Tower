import sys
from PySide6.QtWidgets import QApplication
from argus_tower.ui.main_window import MainWindow

class ArgusApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()

    def run(self):
        self.main_window.show()
        return self.app.exec()