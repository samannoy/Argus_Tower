from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
    QListWidgetItem, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)

class TargetApprovalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        
        # Left Panel: Unapproved Targets
        unapproved_box = QWidget()
        unapproved_box.setProperty("class", "CardWidget")
        u_layout = QVBoxLayout(unapproved_box)
        u_layout.addWidget(QLabel("<b>Detected Targets (Pending Approval)</b>"))
        
        self.target_list = QListWidget()
        u_layout.addWidget(self.target_list)
        
        btn_layout = QHBoxLayout()
        self.btn_approve = QPushButton("Approve Target")
        self.btn_approve.setObjectName("ApproveBtn")
        self.btn_reject = QPushButton("Reject")
        self.btn_reject.setObjectName("RejectBtn")
        btn_layout.addWidget(self.btn_approve)
        btn_layout.addWidget(self.btn_reject)
        u_layout.addLayout(btn_layout)
        
        # Right Panel: Approved Targets Table
        approved_box = QWidget()
        approved_box.setProperty("class", "CardWidget")
        a_layout = QVBoxLayout(approved_box)
        a_layout.addWidget(QLabel("<b>Approved Target Coordinates</b>"))
        
        self.approved_table = QTableWidget(0, 3)
        self.approved_table.setHorizontalHeaderLabels(["Target ID", "Latitude", "Longitude"])
        self.approved_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        a_layout.addWidget(self.approved_table)

        layout.addWidget(unapproved_box)
        layout.addWidget(approved_box)
        
        self._load_sample_data()

    def _load_sample_data(self):
        # Sample detected target
        item = QListWidgetItem("Target #1 - Lat: 34.0522, Lon: -118.2437")
        self.target_list.addItem(item)