from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QComboBox
from PySide6.QtCore import Signal

class Sidebar(QWidget):
    # Signals to switch main display views
    screen_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setMinimumWidth(180)
        self.setMaximumWidth(240)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Title / Status
        title = QLabel("CONTROL PANEL")
        title.setStyleSheet("font-weight: bold; color: #60a5fa; margin-bottom: 5px;")
        layout.addWidget(title)

        # Navigation Buttons
        self.btn_map = QPushButton("🗺️ Map View")
        self.btn_map.setCheckable(True)
        self.btn_map.setChecked(True)
        self.btn_map.clicked.connect(lambda: self._select_tab(self.btn_map, "map"))
        layout.addWidget(self.btn_map)

        self.btn_dashboard = QPushButton("🛸 Drone Dashboards")
        self.btn_dashboard.setCheckable(True)
        self.btn_dashboard.clicked.connect(lambda: self._select_tab(self.btn_dashboard, "dashboards"))
        layout.addWidget(self.btn_dashboard)

        # Separator Line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # Connection Controls (Per-drone or Global connection launcher)
        conn_label = QLabel("Connection Interface")
        conn_label.setStyleSheet("color: #888888; font-size: 11px;")
        layout.addWidget(conn_label)

        self.port_select = QComboBox()
        self.port_select.addItems(["COM1", "COM3", "/dev/ttyUSB0", "Auto-Detect"])
        layout.addWidget(self.port_select)

        self.btn_connect = QPushButton("Connect Serial")
        self.btn_connect.setStyleSheet("background-color: #0284c7; color: white;")
        layout.addWidget(self.btn_connect)

        layout.addStretch()

        # System Status Footer
        self.lbl_status = QLabel("System Ready")
        self.lbl_status.setStyleSheet("color: #4ade80; font-size: 11px;")
        layout.addWidget(self.lbl_status)

        self.buttons = [self.btn_map, self.btn_dashboard]

    def _select_tab(self, active_btn, screen_name):
        for btn in self.buttons:
            btn.setChecked(btn == active_btn)
        self.screen_changed.emit(screen_name)