from PIL import Image
import os
from dataclasses import dataclass
import config

@dataclass
class Bounds:
    x1: float
    y1: float
    x2: float
    y2: float

class Obstacle:
    def __init__(self, type: str, x: float, y: float, width: float, height: float):
        self.type = type
        self.bounds = Bounds(x, y, x + width, y + height)
        self.effect = self.get_effect(type)
        
        image_path = os.path.join(config.ASSETS_DIR, 'images', 'obstacles.png')
        self.image = Image.open(image_path)
        
    def get_effect(self, type: str) -> dict:
        effects = {
            'water': {'reset': True},
            'rock': {'bounce': 0.8},
            'log': {'bounce': 0.5, 'slow': 0.7}
        }
        return effects.get(type, {})
        
    def contains_point(self, x: float, y: float) -> bool:
        return (self.bounds.x1 <= x <= self.bounds.x2 and 
                self.bounds.y1 <= y <= self.bounds.y2)
                
    def apply_effect(self, ball) -> None:
        if self.effect.get('reset'):
            ball.reset(ball.position.x, ball.position.y)
        if self.effect.get('bounce'):
            ball.velocity.x *= -self.effect['bounce']
            ball.velocity.y *= -self.effect['bounce']
            
    def draw(self, draw_surface):
        size = (int(self.bounds.x2 - self.bounds.x1), 
                int(self.bounds.y2 - self.bounds.y1))
        draw_surface.paste(
            self.image.resize(size),
            (int(self.bounds.x1), int(self.bounds.y1))
        )