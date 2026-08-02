class WaypointPlanner:
    def __init__(self):
        self.waypoints = []

    def add_waypoint(self, lat: float, lon: float, alt: float):
        self.waypoints.append({"lat": lat, "lon": lon, "alt": alt})