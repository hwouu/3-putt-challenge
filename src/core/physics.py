import numpy as np
from dataclasses import dataclass

@dataclass
class Vector2D:
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

class PhysicsEngine:
    def __init__(self):
        self.gravity = 9.81
        self.friction_coefficients = {
            'green': 0.95,  # 일반 잔디
            'rough': 0.80,  # 러프
            'fairway': 0.90,  # 페어웨이
            'sand': 0.70,   # 벙커
        }
    
    def calculate_shot(self, start_pos: Vector2D, power: float, angle: float, terrain: str) -> list[Vector2D]:
        """Calculate ball trajectory based on initial conditions"""
        trajectory = []
        pos = start_pos
        velocity = Vector2D(
            power * np.cos(np.radians(angle)),
            power * np.sin(np.radians(angle))
        )
        
        while abs(velocity.x) > 0.01 or abs(velocity.y) > 0.01:
            # 위치 업데이트
            pos = pos + velocity
            trajectory.append(pos)
            
            # 마찰력 적용
            friction = self.friction_coefficients.get(terrain, 0.95)
            velocity = velocity * friction
            
            if len(trajectory) > 1000:  # 무한 루프 방지
                break
                
        return trajectory

    def check_collision(self, ball_pos: Vector2D, obstacles: list) -> bool:
        """Check collision between ball and obstacles"""
        for obstacle in obstacles:
            if obstacle.contains_point(ball_pos):
                return True
        return False