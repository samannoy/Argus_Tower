import tomllib
from pathlib import Path

# Path to pyproject.toml at project root
_toml_path = Path(__file__).resolve().parents[3] / "pyproject.toml"
try:
    with open(_toml_path, "rb") as f:
        _project = tomllib.load(f)["project"]
    
    APP_VERSION=_project.get("version")
    APP_AUTHORS=", ".join(a["name"] for a in _project.get("authors", []))
    
        
except Exception:
    APP_VERSION = ""
    APP_AUTHORS = ""