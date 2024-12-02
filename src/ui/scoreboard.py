from PIL import ImageDraw
from dataclasses import dataclass

@dataclass
class ScoreData:
    shots: int
    par: int
    current_hole: int
    total_holes: int

class Scoreboard:
    def __init__(self, x: int = 5, y: int = 5):
        self.x = x
        self.y = y
        self.data = ScoreData(0, 3, 1, 9)
        self.total_score = 0
        
    def update(self, shots: int, par: int, current_hole: int):
        self.data.shots = shots
        self.data.par = par
        self.data.current_hole = current_hole
        
    def draw(self, draw: ImageDraw.Draw):
        # 스코어보드 배경
        draw.rectangle(
            [(self.x, self.y), (self.x + 60, self.y + 30)],
            fill='black',
            outline='white'
        )
        
        # 홀 정보
        draw.text(
            (self.x + 5, self.y + 2),
            f"Hole: {self.data.current_hole}/{self.data.total_holes}",
            fill='white'
        )
        
        # 샷 정보
        draw.text(
            (self.x + 5, self.y + 15),
            f"Shot: {self.data.shots}/{self.data.par}",
            fill='white' if self.data.shots <= self.data.par else 'red'
        )
        
    def add_score(self, final_shots: int):
        self.total_score += final_shots
        return final_shots <= self.data.par