from pico2d import *
import game_framework

class Background:
    def __init__(self, image_file_name, scroll_speed):
        # 배경에 사용할 이미지 로드 (파일 이름을 인자로 받음)
        self.image = load_image(image_file_name)
        self.scroll_speed = scroll_speed
        self.x = 0

    def update(self):
        # 스크롤 속도에 따라 x 좌표 업데이트
        self.x = (self.x + self.scroll_speed * game_framework.frame_time) % self.image.w

    def draw(self):
        self.image.draw(400, 300, self.image.w/2+600, 600)
        pass

class Grass:
    def __init__(self):
        self.image = load_image('background/grass.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 10)