from dataclasses import dataclass
from src.core.physics import PhysicsEngine, Vector2D
from PIL import Image
import config
import os

class Ball:
    def __init__(self, x: float, y: float):
        self.position = Vector2D(x, y)
        self.velocity = Vector2D(0, 0)
        self.state = 'idle'  # 'idle', 'moving', 'in_hole'
        self.trajectory = []
        self.shots_taken = 0
        
        # 이미지 로드
        image_path = os.path.join(config.ASSETS_DIR, 'images', 'golf-ball.png')
        self.image = Image.open(image_path)
        self.physics = PhysicsEngine()
        
    def hit(self, power: float, angle: float, terrain: str):
        if self.state != 'idle':
            return
            
        self.shots_taken += 1
        self.state = 'moving'
        self.trajectory = self.physics.calculate_shot(
            self.position, power, angle, terrain
        )
        
    def update(self):
        if self.state == 'moving' and self.trajectory:
            next_pos = self.trajectory.pop(0)
            self.position = next_pos
            
            if not self.trajectory:
                self.state = 'idle'
                
    def reset(self, x: float, y: float):
        self.position = Vector2D(x, y)
        self.velocity = Vector2D(0, 0)
        self.state = 'idle'
        self.trajectory = []
        self.shots_taken = 0
        
    def draw(self, draw_surface):
        # 공 이미지 그리기 (8x8 픽셀)
        x, y = int(self.position.x), int(self.position.y)
        draw_surface.paste(self.image.resize((8, 8)), (x-4, y-4))
        
        # 궤적 표시 (moving 상태일 때만)
        if self.state == 'moving' and self.trajectory:
            for pos in self.trajectory[::5]:  # 5단위로 점 표시
                draw_surface.point((int(pos.x), int(pos.y)), fill='black')
                
    def check_hole_collision(self, hole_position: tuple[float, float]) -> bool:
        """홀컵과의 충돌 검사"""
        hole_x, hole_y = hole_position
        dx = self.position.x - hole_x
        dy = self.position.y - hole_y
        distance = (dx * dx + dy * dy) ** 0.5
        return distance < 5  # 홀컵 반경을 5픽셀로 가정