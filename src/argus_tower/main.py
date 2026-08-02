import sys
import os

# 1. Calculate the absolute path to the 'src' directory
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# 2. Add 'src' to the system path so Python can find 'argus_tower'
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# 3. Now the imports will work perfectly
from argus_tower.app import ArgusApp

def main():
    app = ArgusApp()
    sys.exit(app.run())

if __name__ == "__main__":
    main()