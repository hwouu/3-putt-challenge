import os
import sys
from src.core.game import Game

def check_environment():
    """Check if all required directories and files exist"""
    required_dirs = [
        'assets/fonts',
        'assets/images',
        'src/core',
        'src/entities',
        'src/ui',
        'src/courses',
        'src/hardware'
    ]
    
    for directory in required_dirs:
        os.makedirs(directory, exist_ok=True)

def main():
    try:
        check_environment()
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()