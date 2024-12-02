from PIL import Image
import os
import config

class Hole:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        image_path = os.path.join(config.ASSETS_DIR, 'images', 'hole.png')
        self.image = Image.open(image_path)
        
        # 깃발 이미지 로드
        flag_path = os.path.join(config.ASSETS_DIR, 'images', 'flag.png')
        self.flag = Image.open(flag_path)
        
    def draw(self, draw_surface):
        hole_size = (16, 16)
        flag_size = (12, 24)
        
        draw_surface.paste(
            self.image.resize(hole_size),
            (int(self.x - hole_size[0]/2), int(self.y - hole_size[1]/2))
        )
        draw_surface.paste(
            self.flag.resize(flag_size),
            (int(self.x - flag_size[0]/2), int(self.y - flag_size[1])),
            self.flag.resize(flag_size)
        )