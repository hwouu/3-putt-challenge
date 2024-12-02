from dataclasses import dataclass
from PIL import ImageDraw

@dataclass
class PowerGaugeConfig:
    x: int = 20
    y: int = 180
    width: int = 10
    height: int = 50
    max_power: float = 100.0
    oscillation_speed: float = 2.0

class PowerGauge:
    def __init__(self, config: PowerGaugeConfig = PowerGaugeConfig()):
        self.config = config
        self.power = 0.0
        self.increasing = True
        self.active = False
        
    def update(self):
        if not self.active:
            return
            
        if self.increasing:
            self.power += self.config.oscillation_speed
            if self.power >= self.config.max_power:
                self.increasing = False
        else:
            self.power -= self.config.oscillation_speed
            if self.power <= 0:
                self.increasing = True
                
    def start(self):
        self.active = True
        self.power = 0.0
        self.increasing = True
        
    def stop(self) -> float:
        self.active = False
        return self.power
        
    def draw(self, draw: ImageDraw.Draw):
        # 외곽선
        draw.rectangle(
            [(self.config.x, self.config.y),
             (self.config.x + self.config.width, 
              self.config.y + self.config.height)],
            outline='white'
        )
        
        # 파워 레벨
        power_height = (self.power / self.config.max_power) * self.config.height
        draw.rectangle(
            [(self.config.x, self.config.y + self.config.height - power_height),
             (self.config.x + self.config.width, self.config.y + self.config.height)],
            fill='red'
        )