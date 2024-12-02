from PIL import Image, ImageDraw
import config

class Display:
    def __init__(self):
        self.width = config.SCREEN_WIDTH
        self.height = config.SCREEN_HEIGHT
        
        if config.IS_RASPBERRY_PI:
            from adafruit_rgb_display import st7789
            import board
            import digitalio
            
            cs_pin = digitalio.DigitalInOut(board.CE0)
            dc_pin = digitalio.DigitalInOut(board.D25)
            reset_pin = digitalio.DigitalInOut(board.D24)
            
            spi = board.SPI()
            self.disp = st7789.ST7789(
                spi,
                height=240,
                y_offset=80,
                rotation=180,
                cs=cs_pin,
                dc=dc_pin,
                rst=reset_pin,
                baudrate=24000000
            )
        
        # Create image buffer
        self.image = Image.new('RGB', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        
    def clear(self, color=(255, 255, 255)):
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)
        
    def update(self):
        if config.IS_RASPBERRY_PI:
            self.disp.image(self.image)
        else:
            self.image.show()  # For desktop development
            
    def get_draw(self):
        return self.draw