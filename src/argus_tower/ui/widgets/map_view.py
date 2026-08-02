from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class MapView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        lbl = QLabel("Multi-Drone Map & Waypoint Planning View")
        lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #888888;")
        layout.addWidget(lbl)