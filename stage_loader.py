from pico2d import *
import game_world
import play_mode
import game_framework

class Background:
    def __init__(self, image_file_name, scroll_speed):
        # 배경에 사용할 이미지 로드 (파일 이름을 인자로 받음)
        self.image = load_image(image_file_name)
        self.scroll_speed = scroll_speed
        self.image_width = self.image.w
        self.x = 0
        self.y = 0

    def update(self):
        # 스크롤 속도에 따라 x 좌표 업데이트
        self.x = (self.x + self.scroll_speed * game_framework.frame_time) % self.image.w

    def draw(self):
        # 카메라 위치 가져오기
        camera_x = play_mode.cam.x

        # 카메라 위치 기준으로 시작 인덱스 계산
        start_index = int(camera_x // self.image_width) - 1

        # 화면을 덮을 만큼 그리기 (보통 3~4개면 충분)
        for i in range(start_index, start_index + 4):
            bg_x = i * self.image_width - self.x
            screen_x, screen_y = game_world.render(self, bg_x, self.y)

            if i % 2 == 0:
                self.image.draw(int(screen_x), int(screen_y) + 250)
            else:
                self.image.clip_composite_draw(
                    0, 0,
                    self.image_width, self.image.h,
                    0, 'h',
                    int(screen_x), int(screen_y) + 250,
                    self.image_width, self.image.h
                )


class Grass:
    def __init__(self):
        self.image = load_image('background/grass.png')
        self.platforms = [
            (400, 30, 800, 60),  # 바닥 플랫폼
            (200, 80, 400, 60),  # 왼쪽 중간 플랫폼
            (600, 100, 400, 60),  # 오른쪽 중간 플랫폼
            (400, 200, 300, 60),  # 상단 플랫폼
        ]

    def update(self):
        pass

    def draw(self):
        # 각 발판마다 카메라 좌표 변환
        for x, y, w, h in self.platforms:
            screen_x, screen_y = game_world.render(self, x, y)
            self.image.clip_draw(0, 0, w, h, screen_x, screen_y)