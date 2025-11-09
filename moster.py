from pico2d import *
import game_framework

class Ghost:
    img = None
    def __init__(self, image_file_name, position, speed):
        if Ghost.img is None:
            Ghost.img = load_image('monster/dark_ghost.png')
        self.image = Ghost.img
        self.x, self.y = position
        self.speed = speed

    def update(self):
        self.x += self.speed * game_framework.frame_time
        if self.x > 800:  # Assuming the canvas width is 800
            self.x = 0

    def draw(self):
        self.image.draw(self.x, self.y)

    def handle_event(self, event):
        pass  # Implement event handling if necessary