from dataclasses import dataclass
from typing import List, Dict
import numpy as np

@dataclass
class Obstacle:
    type: str  # 'water', 'rock', 'log'
    position: tuple[float, float]
    size: tuple[float, float]

@dataclass
class CourseData:
    id: int
    name: str
    par: int
    start_position: tuple[float, float]
    hole_position: tuple[float, float]
    terrain_map: List[List[str]]  # 2D grid of terrain types
    obstacles: List[Obstacle]
    
# 코스 데이터 정의
COURSES = [
    CourseData(
        id=1,
        name="First Steps",
        par=3,
        start_position=(30, 200),
        hole_position=(120, 40),
        terrain_map=[
            ['green'] * 10 for _ in range(10)  # 10x10 grid of green
        ],
        obstacles=[
            Obstacle('log', (100, 100), (40, 10))
        ]
    ),
    CourseData(
        id=2,
        name="Water Challenge",
        par=3,
        start_position=(30, 200),
        hole_position=(200, 40),
        terrain_map=[
            ['green', 'water', 'green', 'rough'] * 3,
            ['green', 'green', 'sand', 'green'] * 3,
            ['rough', 'green', 'green', 'water'] * 3
        ],
        obstacles=[
            Obstacle('rock', (150, 100), (20, 20)),
            Obstacle('water', (100, 50), (40, 40))
        ]
    ),
    # 추가 코스는 이어서 정의
]