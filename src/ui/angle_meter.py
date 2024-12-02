import math
from PIL import ImageDraw

class AngleMeter:
    def __init__(self, x: int = 120, y: int = 200, radius: int = 30):
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = 0  # 각도 (0-360)
        self.active = False
        
    def update(self, dx: float, dy: float):
        if not self.active:
            return
            
        if dx == 0 and dy == 0:
            return
            
        self.angle = math.degrees(math.atan2(-dy, dx)) % 360
        
    def start(self):
        self.active = True
        
    def stop(self) -> float:
        self.active = False
        return self.angle
        
    def draw(self, draw: ImageDraw.Draw):
        # 방향 표시선
        end_x = self.x + self.radius * math.cos(math.radians(self.angle))
        end_y = self.y - self.radius * math.sin(math.radians(self.angle))
        
        draw.line(
            [(self.x, self.y), (end_x, end_y)],
            fill='white',
            width=2
        )
        
        # 각도 원호
        draw.arc(
            [(self.x - self.radius, self.y - self.radius),
             (self.x + self.radius, self.y + self.radius)],
            0,
            -self.angle,
            fill='white'
        )
        
        # 각도 텍스트
        text_x = self.x + self.radius * 1.2
        text_y = self.y - 10
        draw.text(
            (text_x, text_y),
            f"{int(self.angle)}°",
            fill='white'
        )