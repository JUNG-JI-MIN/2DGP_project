from pico2d import *
import game_world
import play_mode
import game_framework


def get_stage_size(theme, stage_num):
    """테마와 스테이지 번호로 맵 크기 반환"""
    stage_sizes = {
        'forest': {  # 숲 테마 (3개 스테이지)
            1: (2400, 600),
            2: (2800, 600),
            3: (3200, 600)
        },
        'desert': {  # 사막 테마 (4개 스테이지)
            1: (3000, 800),
            2: (3200, 800),
            3: (3500, 800),
            4: (4000, 800)
        },
        'castle': {  # 성 테마 (3개 스테이지)
            1: (3500, 600),
            2: (4000, 600),
            3: (4500, 600)
        },
        'snow': {  # 눈 테마 (2개 스테이지)
            1: (1000, 3000),
            2: (1500, 3500)
        }
    }
    # 테마가 없으면 기본값, 스테이지가 없으면 해당 테마의 1번
    return stage_sizes.get(theme, {}).get(stage_num, (2400, 600))

class Background:
    def __init__(self, image_file_name, scroll_speed):
        # 배경에 사용할 이미지 로드 (파일 이름을 인자로 받음)
        self.image = load_image(image_file_name)
        self.scroll_speed = scroll_speed
        self.image_width = self.image.w
        self.x = 0
        self.y = 0

    def update(self):
        pass
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