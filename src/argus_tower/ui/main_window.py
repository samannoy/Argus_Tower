import os
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QMenuBar, QMenu, QTabWidget, QLabel, QPushButton, QDialog, QVBoxLayout
from PySide6.QtGui import QAction

from argus_tower.ui.widgets.sidebar import Sidebar
from argus_tower.ui.widgets.map_view import MapView
from argus_tower.ui.widgets.drone_dashboard import DroneDashboardWidget
from argus_tower.vehicle.vehicle_manager import VehicleManager
from argus_tower.config.settings import APP_VERSION, APP_AUTHORS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ARGUS TOWER - Ground Control Station")
        self.resize(1280, 800)

        self.vehicle_manager = VehicleManager(max_vehicles=8)

        # Apply CSS Stylesheet
        self._load_stylesheet()

        # Build UI
        self._create_navbar()
        self._setup_layout()

    def _load_stylesheet(self):
        style_path = os.path.join(os.path.dirname(__file__), "styles.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())

    def _create_navbar(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View Menu
        view_menu = menu_bar.addMenu("View")
        
        # Tools Menu
        tools_menu = menu_bar.addMenu("Tools")

        # Help Menu
        help_menu = menu_bar.addMenu("Help")

        # 1. Contact Us
        action_contact = QAction("Contact Us", self)
        help_menu.addAction(action_contact)

        # 2. About Us
        action_about = QAction("About Us", self)
        action_about.triggered.connect(self._show_about_dialog)
        help_menu.addAction(action_about)

        # 3. Check for Updates (Sub-menu)
        update_menu = help_menu.addMenu("Check for Updates")
        
        action_update_sw = QAction("Check for software update", self)
        action_update_fw = QAction("Check for firmware update", self)
        
        update_menu.addAction(action_update_sw)
        update_menu.addAction(action_update_fw)
    def _show_about_dialog(self):
        # Create a custom popup dialog for About Us
        dialog = QDialog(self)
        dialog.setWindowTitle("About Us")
        dialog.setFixedSize(350, 200)
        
        # We inherit the main dark stylesheet so the popup doesn't look out of place
        dialog.setStyleSheet(self.styleSheet())
        
        layout = QVBoxLayout(dialog)
        
        info_text = (
            "<h2 style='color: #60a5fa;'>ARGUS TOWER</h2>"
            f"<p><b>Version:</b> {APP_VERSION}</p>"
            f"<p><b>Developed by:</b> {APP_AUTHORS}</p>"
            "<p><i>Advanced Combat Planning & Multi-Vehicle Platform.</i></p>"
        )
        
        lbl_info = QLabel(info_text)
        lbl_info.setWordWrap(True)
        layout.addWidget(lbl_info)
        
        # Add stretch to push the button to the bottom
        layout.addStretch()
        
        # Custom Close Button
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
        
        # exec() blocks the main window until the popup is closed
        dialog.exec()
        
        
    def _setup_layout(self):
        main_container = QWidget()
        self.setCentralWidget(main_container)

        layout = QHBoxLayout(main_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Left Panel (Sidebar: 10-20% width)
        self.sidebar = Sidebar()
        layout.addWidget(self.sidebar)

        # Main Display Area
        self.stacked_widget = QStackedWidget()
        
        # Screen 1: Map View
        self.map_view = MapView()
        self.stacked_widget.addWidget(self.map_view)

        # Screen 2: Multi-Drone Dashboards Tab View
        self.drone_tabs = QTabWidget()
        for v_id in range(1, 9):
            dash = DroneDashboardWidget(vehicle_id=v_id)
            self.drone_tabs.addTab(dash, f"Drone {v_id}")
        self.stacked_widget.addWidget(self.drone_tabs)

        layout.addWidget(self.stacked_widget, stretch=1)

        # Connect Sidebar signals
        self.sidebar.screen_changed.connect(self._on_screen_changed)

    def _on_screen_changed(self, screen_name: str):
        if screen_name == "map":
            self.stacked_widget.setCurrentWidget(self.map_view)
        elif screen_name == "dashboards":
            self.stacked_widget.setCurrentWidget(self.drone_tabs)