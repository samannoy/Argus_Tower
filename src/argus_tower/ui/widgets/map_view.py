from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QPushButton
from PySide6.QtCore import Signal
from PySide6.QtWebEngineWidgets import QWebEngineView

from argus_tower.ui.widgets.hud_widget import HUDWidget

class MapWidget(QWidget):
    """Modular Leaflet OpenStreetMap widget."""
    def __init__(self, lat=34.0522, lon=-118.2437, zoom=13, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.webview = QWebEngineView()
        self.update_map(lat, lon, zoom)
        layout.addWidget(self.webview)

    def update_map(self, lat, lon, zoom):
        self.webview.setHtml(self._get_leaflet_html(lat, lon, zoom))

    def _get_leaflet_html(self, lat, lon, zoom):
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
            <style>
                body {{ padding: 0; margin: 0; background-color: #18181b; }}
                html, body, #map {{ height: 100%; width: 100%; }}
                .leaflet-control-attribution {{ display: none !important; }}
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                var map = L.map('map', {{zoomControl: false}}).setView([{lat}, {lon}], {zoom});
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
                var marker = L.circleMarker([{lat}, {lon}], {{
                    color: '#ef4444', fillColor: '#ef4444', fillOpacity: 0.8, radius: 6
                }}).addTo(map);
            </script>
        </body>
        </html>
        """

class MiniMapContainer(QFrame):
    """Container for individual mini-maps with interactive header."""
    clicked = Signal(int)
    
    def __init__(self, drone_id, lat, lon):
        super().__init__()
        self.drone_id = drone_id
        self.setObjectName("MiniMap")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        self.btn_header = QPushButton(f"DRONE {drone_id}")
        self.btn_header.setObjectName("MiniMapHeader")
        self.btn_header.clicked.connect(lambda: self.clicked.emit(self.drone_id))
        layout.addWidget(self.btn_header)
        
        self.map_widget = MapWidget(lat=lat, lon=lon, zoom=12)
        layout.addWidget(self.map_widget)


class MapView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # --- Mock Telemetry Data (Structured for MAVLink dynamic updates later) ---
        self.drone_telemetry = {
            1: {"pitch": 5.0,  "roll": 15.0,  "hdg": 45,  "lat": 34.0622, "lon": -118.2337, "alt": 120.5, "sats": 14},
            2: {"pitch": -3.0, "roll": -20.0, "hdg": 180, "lat": 34.0722, "lon": -118.2237, "alt": 95.0,  "sats": 12},
            3: {"pitch": 12.0, "roll": 35.0,  "hdg": 270, "lat": 34.0822, "lon": -118.2137, "alt": 150.2, "sats": 10},
            4: {"pitch": 2.0,  "roll": -5.0,  "hdg": 90,  "lat": 34.0922, "lon": -118.2037, "alt": 110.0, "sats": 15},
            5: {"pitch": -8.0, "roll": 8.0,   "hdg": 15,  "lat": 34.1022, "lon": -118.1937, "alt": 80.4,  "sats": 11},
            6: {"pitch": 18.0, "roll": -40.0, "hdg": 310, "lat": 34.1122, "lon": -118.1837, "alt": 210.0, "sats": 13},
            7: {"pitch": 0.0,  "roll": 0.0,   "hdg": 0,   "lat": 34.1222, "lon": -118.1737, "alt": 100.0, "sats": 16},
            8: {"pitch": -5.0, "roll": -18.0, "hdg": 135, "lat": 34.1322, "lon": -118.1637, "alt": 130.8, "sats": 9},
        }
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # --- LEFT PANEL: HUD + Enlarged Map (50% Width) ---
        self.left_panel = QFrame()
        self.left_panel.setProperty("class", "CardWidget")
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(6, 6, 6, 6)
        self.left_layout.setSpacing(8)
        
        # 1. Top HUD Display
        self.hud = HUDWidget()
        self.left_layout.addWidget(self.hud)
        
        # 2. Bottom Enlarged Map
        self.large_map = MapWidget(lat=34.0622, lon=-118.2337, zoom=14)
        self.left_layout.addWidget(self.large_map)
        
        main_layout.addWidget(self.left_panel, stretch=1)
        
        # Initialize Left Panel with Drone 1 Data
        self._update_left_panel(1)

        # --- RIGHT PANEL: 8 Mini Maps Grid (50% Width) ---
        self.right_panel = QWidget()
        self.grid_layout = QGridLayout(self.right_panel)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(10)
        
        self.mini_maps = {}
        for i in range(1, 9):
            data = self.drone_telemetry[i]
            mini = MiniMapContainer(i, data["lat"], data["lon"])
            mini.clicked.connect(self._on_minimap_clicked)
            
            row = (i - 1) // 2
            col = (i - 1) % 2
            self.grid_layout.addWidget(mini, row, col)
            self.mini_maps[i] = mini
            
        main_layout.addWidget(self.right_panel, stretch=1)

    def _on_minimap_clicked(self, drone_id: int):
        """Called when any mini-map header is clicked."""
        self._update_left_panel(drone_id)

    def _update_left_panel(self, drone_id: int):
        """Updates both HUD and Enlarged Map to reflect selected drone's telemetry."""
        data = self.drone_telemetry.get(drone_id)
        if not data:
            return

        # 1. Update HUD Artificial Horizon
        self.hud.set_telemetry(
            drone_id=drone_id,
            pitch=data["pitch"],
            roll=data["roll"],
            heading=data["hdg"],
            lat=data["lat"],
            lon=data["lon"],
            alt=data["alt"],
            sats=data["sats"]
        )

        # 2. Update Enlarged Map Position
        self.large_map.update_map(lat=data["lat"], lon=data["lon"], zoom=15)