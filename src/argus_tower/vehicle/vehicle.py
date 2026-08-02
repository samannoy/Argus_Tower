class Vehicle:
    def __init__(self, vehicle_id: int, name: str = ""):
        self.id = vehicle_id
        self.name = name if name else f"Drone {vehicle_id}"
        
        # Connection info (for per-vehicle serial links)
        self.port = ""
        self.baudrate = 115200
        self.is_connected = False
        
        # Telemetry state
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0
        self.pressure = 0.0
        
        # Target lists
        self.detected_targets = []  # List of unapproved target dicts
        self.approved_targets = []  # List of approved target dicts