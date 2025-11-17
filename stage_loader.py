from pico2d import *
import game_world
import play_mode
import game_framework

def get_stage_platform(theme, stage_num):
    #테마와 스테이지 별 발판 위치
    stage_platforms = {
        'forest': {  # 숲 테마 (3개 스테이지)
            1: [(400, 30, 800, 60), (200, 80, 400, 60), (600, 100, 400, 60), (400, 200, 300, 60)],
            2: [(500, 30, 900, 60), (300, 100, 500, 60), (700, 150, 400, 60), (450, 250, 350, 60)],
            3: [(600, 30, 1000, 60), (400, 120, 600, 60), (800, 180, 500, 60), (500, 300, 400, 60)]
        },
        'desert': {  # 사막 테마 (4개 스테이지)
            1: [(400, 30, 800, 60), (250, 90, 450, 60), (650, 110, 450, 60), (400, 220, 350, 60)],
            2: [(450, 30, 850, 60), (300, 100, 500, 60), (700, 130, 450, 60), (500, 250, 400, 60)],
            3: [(500, 30, 900, 60), (350, 110, 550, 60), (750, 150, 500, 60), (600, 280, 450, 60)],
            4: [(550, 30, 950, 60), (400, 120, 600, 60), (800, 170, 550, 60), (700, 300, 500, 60)]
        },
        'castle': {  # 성 테마 (3개 스테이지)
            1: [(400, 30, 800, 60), (200, 80, 400, 60), (600, 100, 400, 60), (400, 200, 300, 60)],
            2: [(500, 30, 900, 60), (300, 100, 500, 60), (700, 150, 400, 60), (450, 250, 350, 60)],
            3: [(600, 30, 1000, 60), (400, 120, 600, 60), (800, 180, 500, 60), (500, 300, 400, 60)]
        },
        'snow': {  # 눈 테마 (2개 스테이지)
            1: [(300, 50, 700, 60), (150, 200, 400, 60), (500, 400, 400, 60)],
            2: [(400, 70, 800, 60), (250, 250, 500, 60), (600, 450, 500, 60)]
        }
    }
    return stage_platforms.get(theme, {}).get(stage_num, [])
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

def get_max_stages(theme):
    """테마별 최대 스테이지 수 반환"""
    max_stages = {'forest': 3, 'desert': 4, 'castle': 3, 'snow': 2}
    return max_stages.get(theme, 1)

class Background:
    def __init__(self, image_file_name):
        # 배경에 사용할 이미지 로드 (파일 이름을 인자로 받음)
        self.image = load_image(image_file_name)
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


class platform:
    image = None
    def __init__(self, theme, stage):
        if platform.image is None:
            platform.image = load_image(theme)
        self.platforms = get_stage_platform(theme, stage)
    def update(self):
        pass

    def draw(self):
        # 각 발판마다 카메라 좌표 변환
        for x, y, w, h in self.platforms:
            screen_x, screen_y = game_world.render(self, x, y)
            self.image.clip_draw(0, 0, platform.image.w, platform.image.h, screen_x, screen_y, w, h)
            left = screen_x - w // 2
            bottom = screen_y - h // 2
            right = screen_x + w // 2
            top = screen_y + h // 2
            draw_rectangle(left, bottom, right, top,0,255,0)