from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget
from argus_tower.ui.widgets.target_approval import TargetApprovalWidget

class DroneDashboardWidget(QWidget):
    def __init__(self, vehicle_id: int, parent=None):
        super().__init__(parent)
        self.vehicle_id = vehicle_id

        layout = QVBoxLayout(self)
        
        # Header Info
        self.lbl_title = QLabel(f"<b>Drone #{vehicle_id} Dashboard</b>")
        self.lbl_title.setStyleSheet("font-size: 15px; color: #60a5fa;")
        layout.addWidget(self.lbl_title)

        # Telemetry display summary (updated occasionally)
        self.lbl_telemetry = QLabel("Telemetry: Lat: 0.0000 | Lon: 0.0000 | Alt: 0m | Pitch: 0° | Roll: 0° | Press: 1013 hPa")
        self.lbl_telemetry.setStyleSheet("color: #a0a0b0; background: #26262e; padding: 6px; border-radius: 4px;")
        layout.addWidget(self.lbl_telemetry)

        # Sub-tabs for target management and live plots
        self.tabs = QTabWidget()
        self.target_widget = TargetApprovalWidget()
        self.tabs.addTab(self.target_widget, "Target Approval")
        
        # Telemetry plot tab placeholder
        self.plot_placeholder = QLabel("Live Telemetry Plot Area (IMU / Pressure)")
        self.plot_placeholder.setStyleSheet("color: #666; font-style: italic;")
        self.tabs.addTab(self.plot_placeholder, "Telemetry Data Plots")

        layout.addWidget(self.tabs)