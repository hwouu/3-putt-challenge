from PIL import Image, ImageDraw
import time
from src.hardware.display import Display
from src.hardware.input import InputHandler, Event
from src.entities.ball import Ball
from src.courses.course import Course
from src.courses.course_data import COURSES
from src.ui.power_gauge import PowerGauge
from src.ui.angle_meter import AngleMeter
from src.ui.scoreboard import Scoreboard
import config

class Game:
    def __init__(self):
        self.display = Display()
        self.input_handler = InputHandler()
        self.buffer = Image.new('RGB', (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.draw = ImageDraw.Draw(self.buffer)
        
        self.current_course = 0
        self.load_course(self.current_course)
        
        self.power_gauge = PowerGauge()
        self.angle_meter = AngleMeter()
        self.scoreboard = Scoreboard()
        
        self.game_state = 'aiming'  # 'aiming', 'power', 'moving', 'finished'
        self.running = False
        
    def load_course(self, course_index: int):
        course_data = COURSES[course_index]
        self.course = Course(course_data)
        self.ball = Ball(*course_data.start_position)
        
    def handle_input(self):
        events = self.input_handler.get_events()
        for event in events:
            if event.type == 'QUIT':
                self.running = False
                return
                
            if self.game_state == 'aiming':
                if event.key in ['LEFT', 'RIGHT', 'UP', 'DOWN']:
                    dx = 1 if event.key == 'RIGHT' else (-1 if event.key == 'LEFT' else 0)
                    dy = 1 if event.key == 'DOWN' else (-1 if event.key == 'UP' else 0)
                    self.angle_meter.update(dx, dy)
                elif event.key == 'A':
                    self.game_state = 'power'
                    self.power_gauge.start()
                    
            elif self.game_state == 'power':
                if event.key == 'A':
                    power = self.power_gauge.stop()
                    angle = self.angle_meter.angle
                    terrain = self.course.get_terrain_at(self.ball.position.x, self.ball.position.y)
                    self.ball.hit(power, angle, terrain)
                    self.game_state = 'moving'
                    
    def update(self):
        if self.game_state == 'power':
            self.power_gauge.update()
            
        elif self.game_state == 'moving':
            self.ball.update()
            
            # 충돌 검사
            collision, obstacle_type = self.course.check_collision(
                self.ball.position.x, self.ball.position.y
            )
            
            if collision:
                self.handle_collision(obstacle_type)
                
            # 홀컵 진입 검사
            if self.ball.check_hole_collision((self.course.hole.x, self.course.hole.y)):
                self.handle_hole_in()
                
            # 공이 멈추면 다음 샷 준비
            if self.ball.state == 'idle':
                self.game_state = 'aiming'
                self.angle_meter.start()
                
    def handle_collision(self, obstacle_type: str):
        if obstacle_type == 'water':
            self.ball.reset(*COURSES[self.current_course].start_position)
            self.game_state = 'aiming'
            
    def handle_hole_in(self):
        if self.ball.shots_taken <= self.course.data.par:
            self.current_course += 1
            if self.current_course < len(COURSES):
                self.load_course(self.current_course)
            else:
                self.game_state = 'finished'
                
    def render(self):
        # 배경과 코스 그리기
        self.draw.rectangle((0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT), 
                          fill=config.BACKGROUND_COLOR)
        self.course.draw(self.buffer)
        
        # UI 요소 그리기
        if self.game_state in ['aiming', 'power']:
            self.angle_meter.draw(self.draw)
        if self.game_state == 'power':
            self.power_gauge.draw(self.draw)
            
        # 볼 그리기
        self.ball.draw(self.buffer)
        
        # 스코어보드
        self.scoreboard.update(self.ball.shots_taken, self.course.data.par, 
                             self.current_course + 1)
        self.scoreboard.draw(self.draw)
        
        # 디스플레이 업데이트
        self.display.update(self.buffer)
        
    def run(self):
        self.running = True
        last_time = time.time()
        
        while self.running:
            current_time = time.time()
            if current_time - last_time >= 1/config.FPS:
                self.handle_input()
                self.update()
                self.render()
                last_time = current_time