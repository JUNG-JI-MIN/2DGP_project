from pico2d import *
import game_world
import play_mode
import game_framework
thema = ('forest', 'snow', 'desert', 'castle')
def get_next_theme(current_theme):
    if current_theme == 'forest':
        return 'snow'
    elif current_theme == 'snow':
        return 'desert'
    elif current_theme == 'desert':
        return 'castle'
    else:
        return 'forest'
def get_back_theme(current_theme):
    if current_theme == 'forest':
        return 'castle'
    elif current_theme == 'snow':
        return 'forest'
    elif current_theme == 'desert':
        return 'snow'
    else:
        return 'desert'
def get_stage_platform(theme, stage_num):
    #테마와 스테이지 별 발판 위치
    stage_platforms = {
        'village': {
            1: [(0,0,0,0)]
        },
        'forest': {  # 숲 테마 (3개 스테이지)
            # 스테이지 1: map size (2400, 600)
            1: [
                # ground (반전 없음: 이미 맨 아래라 y=0 고정)
                (0, 0, 800, 50),
                (800, 0, 800, 50),
                (1600, 0, 800, 50),
                (2400, 0, 800, 50),
                (2800, 0, 800, 50),
                # inverted Y platforms
                (200, 600 - 480 - 40, 220, 40),  # → y=80
                (600, 600 - 420 - 40, 260, 40),  # → y=140
                (1100, 600 - 380 - 40, 300, 40),  # → y=180
                (1500, 600 - 340 - 40, 220, 40),  # → y=220
                (1900, 600 - 300 - 40, 260, 40),  # → y=260
                (400, 600 - 260 - 40, 200, 40),  # → y=300
                (900, 600 - 200 - 40, 240, 40),  # → y=360
                (1700, 600 - 150 - 40, 280, 40),  # → y=410
                (2200, 600 - 100 - 40, 300, 40),  # → y=460
            ],
            # 스테이지 2: map size (2800, 600)
            2: [
                # ground
                (0, 0, 800, 50),
                (800, 0, 800, 50),
                (1600, 0, 800, 50),
                (2400, 0, 800, 50),
                (2800, 0, 800, 50),
                # inverted Y
                (150, 600 - 480 - 40, 300, 40),  # y=80
                (700, 600 - 430 - 40, 240, 40),  # y=130
                (1100, 600 - 390 - 40, 260, 40),  # y=170
                (1400, 600 - 350 - 40, 220, 40),  # y=210
                (1800, 600 - 310 - 40, 300, 40),  # y=250
                (2200, 600 - 270 - 40, 240, 40),  # y=290
                (600, 600 - 210 - 40, 200, 40),  # y=350
                (2000, 600 - 170 - 40, 280, 40),  # y=390
                (2500, 600 - 120 - 40, 260, 40),  # y=440
            ],
            # 스테이지 3: map size (3200, 600)
            3: [
                # ground
                (0, 0, 800, 50),
                (800, 0, 800, 50),
                (1600, 0, 800, 50),
                (2400, 0, 800, 50),
                (3200, 0, 800, 50),

                # inverted Y
                (300, 600 - 480 - 40, 260, 40),  # y=80
                (700, 600 - 440 - 40, 220, 40),  # y=120
                (1200, 600 - 400 - 40, 300, 40),  # y=160
                (1600, 600 - 360 - 40, 240, 40),  # y=200
                (2000, 600 - 320 - 40, 260, 40),  # y=240
                (400, 600 - 260 - 40, 200, 40),  # y=300
                (900, 600 - 210 - 40, 220, 40),  # y=350
                (1800, 600 - 160 - 40, 280, 40),  # y=400
                (2600, 600 - 110 - 40, 300, 40),  # y=450
            ]
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
            1: [ # 1000 x 3000

                # gound
                (0, 0, 800, 60),
                (800, 0, 800, 60),

                # inverted Y
                (200, 2900, 300, 60),
                (600, 2750, 250, 60),
                (100, 2600, 350, 60),
                (450, 2450, 400, 60),
                (750, 2300, 200, 60),
                (300, 2150, 300, 60),
                (50, 2000, 250, 60),
                (500, 1850, 350, 60),
                (800, 1700, 180, 60),
                (250, 1550, 320, 60),
                (600, 1400, 300, 60),
                (100, 1250, 350, 60),
                (450, 1100, 380, 60),
                (700, 950, 250, 60),
                (300, 800, 300, 60),
                (550, 650, 350, 60),
                (150, 500, 280, 60),
                (700, 350, 250, 60),
                (350, 200, 300, 60),
            ],
            2: [ # 1500 x 3500
                # gound
                (0, 0, 800, 60),
                (800, 0, 800, 60),
                (1500, 0, 800, 60),

                # inverted Y
                (300, 3350, 500, 60),
                (900, 3200, 450, 60),
                (150, 3050, 400, 60),
                (700, 2900, 500, 60),
                (1200, 2750, 300, 60),
                (400, 2600, 450, 60),
                (1000, 2450, 350, 60),
                (200, 2300, 400, 60),
                (850, 2150, 500, 60),
                (1300, 2000, 250, 60),
                (500, 1850, 450, 60),
                (50, 1700, 350, 60),
                (1000, 1550, 400, 60),
                (300, 1400, 500, 60),
                (1200, 1250, 300, 60),
                (600, 1100, 450, 60),
                (150, 950, 350, 60),
                (900, 800, 500, 60),
                (1300, 650, 250, 60),
                (400, 500, 450, 60),
                (1000, 350, 350, 60),
                (200, 200, 400, 60),
            ]
        }
    }
    return stage_platforms[theme][stage_num]
def get_stage_size(theme, stage_num):
    """테마와 스테이지 번호로 맵 크기 반환"""
    stage_sizes = {
        'village': {
            1: (1344, 768)
        },
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
    return stage_sizes.get(theme, {})[stage_num]

def get_max_stages(theme):
    """테마별 최대 스테이지 수 반환"""
    max_stages = {'forest': 3, 'desert': 4, 'castle': 3, 'snow': 2}
    return max_stages.get(theme, 1)

class Background:
    def __init__(self, image_file_name):
        # 배경에 사용할 이미지 로드 (파일 이름을 인자로 받음)
        self.name = image_file_name
        self.image = load_image(image_file_name)
        self.image_width = self.image.w
        self.x = 0
        self.y = 0

    def update(self):
        pass
    def draw(self):
        # 카메라 위치 가져오기

        if self.name == 'background/snow.png':
            draw_rectangle(0, 0, 1500, 3500, 185, 189, 221, 1, True)

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
    def __init__(self, theme_image,theme, stage):
        self.image = load_image(theme_image)
        self.platforms = get_stage_platform(theme, stage)
    def update(self):
        pass

    def draw(self):
        # 각 발판마다 카메라 좌표 변환
        for x, y, w, h in self.platforms:
            screen_x, screen_y = game_world.render(self, x, y)
            self.image.clip_draw(0, 0, self.image.w, self.image.h, screen_x, screen_y, w, h)
            left = screen_x - w // 2
            bottom = screen_y - h // 2
            right = screen_x + w // 2
            top = screen_y + h // 2
            draw_rectangle(left, bottom, right, top,0,255,0)

    def get_bb_list(self):
        bb_list = []
        for x, y, w, h in self.platforms:
            left = x - w // 2
            bottom = y - h // 2
            right = x + w // 2
            top = y + h // 2
            bb_list.append((left, bottom, right, top))
        return bb_list