from dataclasses import dataclass
from typing import List, Tuple
from PIL import Image, ImageDraw
import numpy as np
import os
import config
from src.entities.hole import Hole
from src.entities.obstacles import Obstacle
from src.courses.course_data import CourseData

@dataclass
class TerrainTile:
    type: str
    friction: float
    image: Image.Image

class Course:
    def __init__(self, course_data: CourseData):
        self.data = course_data
        self.hole = Hole(*course_data.hole_position)
        self.obstacles = [
            Obstacle(
                obs.type,
                obs.position[0],
                obs.position[1],
                obs.size[0],
                obs.size[1]
            ) for obs in course_data.obstacles
        ]
        
        self.terrain_tiles = {}
        self._load_terrain_images()
        
    def _load_terrain_images(self):
        terrain_path = os.path.join(config.ASSETS_DIR, 'images', 'terrain-elements.png')
        terrain_sheet = Image.open(terrain_path)
        
        # Terrain 이미지를 100x100 크기로 분할
        self.terrain_tiles = {
            'green': TerrainTile('green', 0.95, terrain_sheet.crop((0, 0, 100, 100))),
            'rough': TerrainTile('rough', 0.80, terrain_sheet.crop((100, 0, 200, 100))),
            'sand': TerrainTile('sand', 0.70, terrain_sheet.crop((200, 0, 300, 100)))
        }
        
    def get_terrain_at(self, x: float, y: float) -> str:
        grid_x = int(x / 24)  # 240/10 = 24픽셀당 1그리드
        grid_y = int(y / 24)
        
        if 0 <= grid_y < len(self.data.terrain_map) and \
           0 <= grid_x < len(self.data.terrain_map[0]):
            return self.data.terrain_map[grid_y][grid_x]
        return 'out'
        
    def draw(self, draw_surface: Image.Image):
        draw = ImageDraw.Draw(draw_surface)
        
        # Draw terrain
        for y, row in enumerate(self.data.terrain_map):
            for x, terrain_type in enumerate(row):
                if terrain_type in self.terrain_tiles:
                    tile = self.terrain_tiles[terrain_type]
                    draw_surface.paste(
                        tile.image.resize((24, 24)),
                        (x * 24, y * 24)
                    )
        
        # Draw obstacles and hole
        for obstacle in self.obstacles:
            obstacle.draw(draw_surface)
        self.hole.draw(draw_surface)
        
    def check_collision(self, x: float, y: float) -> Tuple[bool, str]:
        for obstacle in self.obstacles:
            if obstacle.contains_point(x, y):
                return True, obstacle.type
        return False, None
        
    def is_out_of_bounds(self, x: float, y: float) -> bool:
        return not (0 <= x < config.SCREEN_WIDTH and 0 <= y < config.SCREEN_HEIGHT)