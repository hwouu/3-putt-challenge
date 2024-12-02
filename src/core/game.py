import time
from src.hardware.display import Display
from src.hardware.input import InputHandler
import config

class Game:
    def __init__(self):
        self.display = Display()
        self.input_handler = InputHandler()
        self.running = False
        self.frame_time = 1.0 / config.FPS
        self.last_time = time.time()
        
    def run(self):
        self.running = True
        while self.running:
            current_time = time.time()
            if current_time - self.last_time >= self.frame_time:
                self.handle_input()
                self.update()
                self.render()
                self.last_time = current_time
            
    def handle_input(self):
        events = self.input_handler.get_events()
        for event in events:
            if event.type == 'QUIT':
                self.running = False
            
    def update(self):
        pass  # Will be implemented with game logic
        
    def render(self):
        self.display.clear(config.BACKGROUND_COLOR)
        # Will add rendering logic here
        self.display.update()