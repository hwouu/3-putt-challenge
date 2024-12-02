import config
from collections import namedtuple

Event = namedtuple('Event', ['type', 'key', 'pressed'])

class InputHandler:
    def __init__(self):
        if config.IS_RASPBERRY_PI:
            import digitalio
            import board
            
            self.button_A = digitalio.DigitalInOut(board.D5)
            self.button_B = digitalio.DigitalInOut(board.D6)
            self.button_L = digitalio.DigitalInOut(board.D27)
            self.button_R = digitalio.DigitalInOut(board.D23)
            self.button_U = digitalio.DigitalInOut(board.D17)
            self.button_D = digitalio.DigitalInOut(board.D22)
            
            for button in [self.button_A, self.button_B, self.button_L, 
                         self.button_R, self.button_U, self.button_D]:
                button.direction = digitalio.Direction.INPUT
        else:
            import pygame
            pygame.init()
            pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            
    def get_events(self):
        events = []
        if config.IS_RASPBERRY_PI:
            # Check hardware buttons
            if not self.button_U.value:
                events.append(Event('KEYDOWN', 'UP', True))
            if not self.button_D.value:
                events.append(Event('KEYDOWN', 'DOWN', True))
            if not self.button_L.value:
                events.append(Event('KEYDOWN', 'LEFT', True))
            if not self.button_R.value:
                events.append(Event('KEYDOWN', 'RIGHT', True))
            if not self.button_A.value:
                events.append(Event('KEYDOWN', 'A', True))
            if not self.button_B.value:
                events.append(Event('KEYDOWN', 'B', True))
        else:
            import pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    events.append(Event('QUIT', None, None))
                elif event.type == pygame.KEYDOWN:
                    key_map = {
                        pygame.K_w: 'UP',
                        pygame.K_s: 'DOWN',
                        pygame.K_a: 'LEFT',
                        pygame.K_d: 'RIGHT',
                        pygame.K_SPACE: 'A',
                        pygame.K_RETURN: 'B'
                    }
                    if event.key in key_map:
                        events.append(Event('KEYDOWN', key_map[event.key], True))
                        
        return events