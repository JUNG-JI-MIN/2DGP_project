from pico2d import *
import game_framework

class Background:
    def __init__(self, image_file_name, scroll_speed):
        # 배경에 사용할 이미지 로드 (파일 이름을 인자로 받음)
        self.image = load_image(image_file_name)
        self.scroll_speed = scroll_speed
        self.x = 0

    def update(self, frame_time):
        # 스크롤 속도에 따라 x 좌표 업데이트
        self.x = (self.x + self.scroll_speed * frame_time) % self.image.w

    def draw(self):
        # 배경 이미지 그리기
        # self.image.draw_tile(self.x, 0, ...)
        pass

