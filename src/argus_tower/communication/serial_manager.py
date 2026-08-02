class SerialManager:
    """
    Manages serial connections to ESP32 flight boards.
    Can operate globally or per vehicle.
    """
    def __init__(self):
        self.active_connections = {}

    def connect_port(self, identifier: str, port_name: str, baudrate: int = 115200) -> bool:
        # Serial connection logic (pyserial) will be attached here
        print(f"[Serial] Connecting to {port_name} at {baudrate} baud for {identifier}...")
        self.active_connections[identifier] = port_name
        return True

    def disconnect_port(self, identifier: str):
        if identifier in self.active_connections:
            print(f"[Serial] Disconnecting {identifier}...")
            del self.active_connections[identifier]

    def read_data(self, identifier: str):
        # Raw bytes stream read logic placeholder
        pass