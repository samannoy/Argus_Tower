from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtCore import Qt, QPointF, QRectF

class HUDWidget(QWidget):
    """
    A modern, vector-drawn HUD / Artificial Horizon widget.
    State parameters are updated via functions so MAVLink streams can easily drive it.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(180)
        self.setMaximumHeight(240)
        
        # State variables (Will be driven by MAVLink telemetry later)
        self.drone_id = 1
        self.pitch = 0.0     # Degrees
        self.roll = 0.0      # Degrees
        self.heading = 0.0   # Degrees (0-360)
        self.lat = 0.0
        self.lon = 0.0
        self.alt = 0.0
        self.sats = 12

    def set_telemetry(self, drone_id: int, pitch: float, roll: float, heading: float, lat: float, lon: float, alt: float, sats: int = 12):
        """Updates internal telemetry state and triggers a redraw."""
        self.drone_id = drone_id
        self.pitch = pitch
        self.roll = roll
        self.heading = heading
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.sats = sats
        self.update()  # Request PySide6 repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width / 2.0
        center_y = height / 2.0

        # --- 1. Background ---
        painter.fillRect(self.rect(), QColor("#141418"))

        # --- 2. Artificial Horizon Painting ---
        painter.save()
        
        # Translate origin to widget center and rotate for Roll angle
        painter.translate(center_x, center_y)
        painter.rotate(-self.roll)
        
        # Calculate pitch vertical shift (3 pixels per degree)
        pitch_offset = self.pitch * 3.0
        
        # Sky and Ground polygons
        sky_rect = QRectF(-width, -height * 2 + pitch_offset, width * 2, height * 2)
        ground_rect = QRectF(-width, pitch_offset, width * 2, height * 2)
        
        painter.fillRect(sky_rect, QColor("#1e293b"))    # Dark Slate Sky
        painter.fillRect(ground_rect, QColor("#2d1a10")) # Dark Earth Ground

        # Horizon Line (Cyan vector line)
        painter.setPen(QPen(QColor("#00ffcc"), 2))
        painter.drawLine(QPointF(-width, pitch_offset), QPointF(width, pitch_offset))

        # Pitch Ladder Marks (+/- 30 degrees)
        painter.setPen(QPen(QColor("#00ffcc"), 1, Qt.DashLine))
        for p in range(-30, 31, 10):
            if p == 0:
                continue
            y_pos = pitch_offset - (p * 3.0)
            painter.drawLine(QPointF(-25, y_pos), QPointF(25, y_pos))

        painter.restore()

        # --- 3. Fixed Aircraft Reticle (Amber Crosshair) ---
        painter.setPen(QPen(QColor("#f59e0b"), 2))
        painter.drawEllipse(QPointF(center_x, center_y), 3, 3) # Center dot
        painter.drawLine(QPointF(center_x - 30, center_y), QPointF(center_x - 10, center_y))
        painter.drawLine(QPointF(center_x + 10, center_y), QPointF(center_x + 30, center_y))
        painter.drawLine(QPointF(center_x - 10, center_y), QPointF(center_x - 10, center_y + 6))
        painter.drawLine(QPointF(center_x + 10, center_y), QPointF(center_x + 10, center_y + 6))

        # --- 4. Tactical Data Overlays ---
        painter.setPen(QPen(QColor("#00ffcc")))
        font = QFont("Consolas", 9, QFont.Bold)
        painter.setFont(font)

        # Top-Left Header
        painter.drawText(12, 22, f"HUD // DRONE #{self.drone_id}")
        
        # Top-Right GPS Coordinates & Satellites
        gps_str = f"GPS: {self.lat:.4f} N, {self.lon:.4f} E | SATS: {self.sats}"
        painter.drawText(width - 290, 22, gps_str)

        # Bottom Telemetry Bar
        telemetry_str = f"ROLL: {self.roll:+.1f}°   PITCH: {self.pitch:+.1f}°   HDG: {self.heading:03.0f}°   ALT: {self.alt:.1f}m"
        painter.drawText(12, height - 12, telemetry_str)

        # Border Frame
        painter.setPen(QPen(QColor("#27272a"), 1))
        painter.drawRect(0, 0, width - 1, height - 1)