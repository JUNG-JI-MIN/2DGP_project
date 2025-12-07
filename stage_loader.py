from pico2d import *
import game_world
import nommor
import play_mode
import item
import game_framework
import quest_center

PIXEL_PER_METER = (10.0 / 0.3)

thema = ('forest', 'snow', 'desert')
def get_next_theme(current_theme):
    if current_theme == 'forest':
        return 'snow'
    elif current_theme == 'snow':
        return 'desert'
    elif current_theme == 'desert':
        return 'forest'
def get_back_theme(current_theme):
    if current_theme == 'forest':
        return 'desert'
    elif current_theme == 'snow':
        return 'forest'
    elif current_theme == 'desert':
        return 'snow'
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
            1: [
                # Ground
                (0, 0, 800, 50),
                (800, 0, 800, 50),
                (1600, 0, 800, 50),
                (2400, 0, 800, 50),

                # 랜덤 발판 10개
                (200, 250, 220, 30),
                (600, 180, 180, 30),
                (950, 320, 270, 30),
                (1300, 210, 300, 30),
                (1500, 380, 190, 30),
                (1850, 270, 260, 30),
                (2100, 150, 200, 30),
                (2400, 340, 180, 30),
                (2600, 220, 300, 30),
                (2800, 300, 250, 30),
            ],

            2: [
                # Ground
                (0, 0, 800, 50),
                (800, 0, 800, 50),
                (1600, 0, 800, 50),
                (2400, 0, 800, 50),
                (3200, 0, 800, 50),

                # 랜덤 발판 10개
                (180, 240, 200, 30),
                (500, 180, 260, 30),
                (900, 300, 180, 30),
                (1200, 220, 300, 30),
                (1500, 350, 190, 30),
                (1800, 260, 250, 30),
                (2050, 140, 210, 30),
                (2400, 310, 300, 30),
                (2700, 200, 180, 30),
                (3000, 280, 260, 30),
            ],

            3: [
                # Ground
                (0, 0, 800, 50),
                (800, 0, 800, 50),
                (1600, 0, 800, 50),
                (2400, 0, 800, 50),
                (3200, 0, 800, 50),

                # 랜덤 발판 10개
                (150, 200, 300, 30),
                (550, 180, 210, 30),
                (900, 320, 250, 30),
                (1250, 270, 290, 30),
                (1550, 340, 160, 30),
                (1900, 250, 260, 30),
                (2150, 150, 200, 30),
                (2500, 300, 280, 30),
                (2850, 220, 300, 30),
                (3200, 310, 180, 30),
            ],

            4: [
                # Ground
                (0, 0, 800, 50),
                (800, 0, 800, 50),
                (1600, 0, 800, 50),
                (2400, 0, 800, 50),
                (3200, 0, 800, 50),
                (4000, 0, 800, 50),

                # 랜덤 발판 10개
                (200, 250, 220, 30),
                (650, 160, 300, 30),
                (1050, 300, 200, 30),
                (1400, 210, 260, 30),
                (1750, 360, 190, 30),
                (2100, 270, 300, 30),
                (2450, 150, 180, 30),
                (2800, 330, 260, 30),
                (3200, 210, 300, 30),
                (3600, 290, 200, 30),
            ],
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
def get_stage_tree(theme, stage_num):
    """테마와 스테이지 번호로 나무 위치 반환"""
    stage_trees = {
        'forest': {  # 숲 테마 (플랫폼 h=40 → +95)
            1: [
                (1700, 410 + 95, 280, 40),  # 플랫폼 (1700, 410, 280, 40)
                (1900, 260 + 95, 260, 40),  # 플랫폼 (1900, 260, 260, 40)
                (700, 140 + 95, 220, 40),   # 플랫폼 (700, 140, 220, 40)
                (2200, 460 + 95, 300, 40),  # 플랫폼 (2200, 460, 300, 40)
            ],
            2: [
                (1800, 250 + 95, 300, 40),  # 플랫폼 (1800, 250, 300, 40)
                (1100, 170 + 95, 260, 40),  # 플랫폼 (1100, 170, 260, 40)
                (150, 80 + 95, 300, 40),    # 플랫폼 (150, 80, 300, 40)
                (2500, 440 + 95, 260, 40),  # 플랫폼 (2500, 440, 260, 40)
            ],
            3: [
                (600, 120 + 95, 260, 40),   # 플랫폼 (600, 120, 260, 40)
                (1600, 200 + 95, 240, 40),  # 플랫폼 (1600, 200, 240, 40)
                (400, 300 + 95, 200, 40),   # 플랫폼 (400, 300, 200, 40)
                (1800, 400 + 95, 280, 40),  # 플랫폼 (1800, 400, 280, 40)
            ]
        },
        'desert': {  # 사막 테마 (플랫폼 h=30 → +90)
            1: [
                (2600, 220 + 90, 300, 30),  # 플랫폼 (2600, 220, 300, 30)
                (2400, 340 + 90, 180, 30),  # 플랫폼 (2400, 340, 180, 30)
                (1400, 210 + 90, 260, 30),  # 플랫폼 (1300, 210, 300, 30)
                (650, 160 + 90, 300, 30),   # 플랫폼 (650, 160, 300, 30) 추정
            ],
            2: [
                (2500, 310 + 90, 280, 30),  # 플랫폼 (2400, 310, 300, 30)
                (1900, 260 + 90, 260, 30),  # 플랫폼 (1800, 260, 250, 30)
                (1250, 220 + 90, 290, 30),  # 플랫폼 (1200, 220, 300, 30)
                (550, 180 + 90, 210, 30),   # 플랫폼 (500, 180, 260, 30)
            ],
            3: [
                (2400, 300 + 90, 300, 30),  # 플랫폼 (2500, 300, 280, 30)
                (2050, 150 + 90, 210, 30),  # 플랫폼 (2150, 150, 200, 30)
                (1200, 270 + 90, 300, 30),  # 플랫폼 (1250, 270, 290, 30)
                (180, 200 + 90, 200, 30),   # 플랫폼 (150, 200, 300, 30)
            ],
            4: [
                (2600, 220 + 90, 300, 30),  # 플랫폼 (2600, 220, 300, 30) 추정
                (1850, 270 + 90, 260, 30),  # 플랫폼 (1750, 360, 190, 30) 근처
                (950, 300 + 90, 270, 30),   # 플랫폼 (1050, 300, 200, 30)
                (200, 250 + 90, 220, 30),   # 플랫폼 (200, 250, 220, 30)
            ]
        },
        'snow': {  # 눈 테마 (플랫폼 h=60 → +105)
            1: [(200, 2900 + 105, 300, 60)],  # 플랫폼 (200, 2900, 300, 60)
            2: [(300, 3350 + 105, 500, 60)]   # 플랫폼 (300, 3350, 500, 60)
        }
    }
    return stage_trees.get(theme, {}).get(stage_num, [])

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
        'snow': {  # 눈 테마 (2개 스테이지)
            1: (1000, 3000),
            2: (1500, 3500)
        }
    }
    # 테마가 없으면 기본값, 스테이지가 없으면 해당 테마의 1번
    return stage_sizes.get(theme, {})[stage_num]
def get_tree_count(theme, stage):
    """테마와 스테이지 번호로 나무 개수 반환"""
    stage_trees = {
        'forest': {  # 숲 테마 (3개 스테이지)
            1: 3,
            2: 4,
            3: 3
        },
        'desert': {  # 사막 테마 (4개 스테이지)
            1: 4,
            2: 4,
            3: 4,
            4: 4
        },
        'snow': {  # 눈 테마 (2개 스테이지)
            1: 1,
            2: 1
        }
    }
    return stage_trees.get(theme, {}).get(stage, 0)
def get_max_stages(theme):
    """테마별 최대 스테이지 수 반환"""
    max_stages = {'forest': 3, 'desert': 4, 'snow': 2}
    return max_stages.get(theme, 1)

class Background:
    def __init__(self, image_file_name, thema):
        # 배경에 사용할 이미지 로드 (파일 이름을 인자로 받음)
        self.name = image_file_name
        self.image = load_image(image_file_name)
        self.image_width = self.image.w
        self.x = 0
        self.y = 0
        self.thema = thema
        self.bgm = load_music(f'sound/{thema}_bgm.mp3')
        self.bgm.set_volume(16)
        self.bgm.repeat_play()

    def update(self):
        pass
    def draw(self):
        # 카메라 위치 가져오기

        camera_x = play_mode.cam.x

        # 카메라 위치 기준으로 시작 인덱스 계산
        start_index = int(camera_x // self.image_width) - 1

        # 화면을 덮을 만큼 그리기 (5개로 확장)
        for i in range(start_index, start_index + 5):
            bg_x = i * self.image_width - self.x
            screen_x, screen_y = game_world.render(self, bg_x, self.y)

            if i % 2 == 0:
                self.image.draw(int(screen_x), int(screen_y) + 250, self.image_width, get_canvas_height() + 250)
            else:
                self.image.clip_composite_draw(
                    0, 0,
                    self.image_width, self.image.h,
                    0, 'h',
                    int(screen_x), int(screen_y) + 250,
                    self.image_width, get_canvas_height() + 250
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

    def get_bb(self):
        bb_list = []
        for x, y, w, h in self.platforms:
            left = x - w // 2
            bottom = y - h // 2
            right = x + w // 2
            top = y + h // 2
            bb_list.append((left, bottom, right, top))
        return bb_list


class Tree:
    tree_hit = None
    tree_die = None
    def __init__(self, theme_image, theme, stage, index):
        if Tree.tree_hit is None:
            Tree.tree_hit = load_wav('sound/tree_hit.wav')
            Tree.tree_hit.set_volume(16)
        if Tree.tree_die is None:
            Tree.tree_die = load_wav('sound/tree_die.wav')
            Tree.tree_die.set_volume(16)

        self.image = load_image(theme_image)
        self.tree = get_stage_tree(theme, stage)
        self.thema = theme
        self.stage = stage

        self.x, self.y, self.w, self.h = self.tree[index]
        self.hp = 5
    def update(self):
        pass

    def draw(self):
        # 카메라 좌표 변환
        screen_x, screen_y = game_world.render(self, self.x, self.y)

        # 나무 이미지 그리기 (자신의 크기 사용)
        self.image.draw(screen_x, screen_y, 5 * PIXEL_PER_METER, 5 * PIXEL_PER_METER)

    def get_bb(self):
        left = self.x - 75  # 300 // 2
        bottom = self.y - 75
        right = self.x + 75
        top = self.y + 75
        return (left, bottom, right, top)
    def get_attack_bb(self):
        left = self.x - 75  # 300 // 2
        bottom = self.y - 75
        right = self.x + 75
        top = self.y + 75
        return (left, bottom, right, top)
    def handle_collision(self, group, other):
        pass

    def handle_attack_collision(self, group, other):
        if group == 'viego:tree':
            if nommor.viego.is_attacking and not nommor.viego.attack_hit_done:
                nommor.viego.attack_hit_done = True
                self.hp -= 1
                Tree.tree_hit.play()
                if self.hp <= 0:
                    Tree.tree_die.play()
                    if self.thema == 'snow' and self.stage == 2:

                        quest_center.update_quest('gold_tree')
                    else:
                        quest_center.update_quest(f'{self.thema}_tree')
                    game_world.remove_object(self)
                    ITEM = item.Item(self.x + 10, self.y - 50, f'{self.thema}_tree')
                    ITEM.value = 500
                    game_world.add_object(ITEM)
                    game_world.add_collision_pair('viego:item', None, ITEM)
                    if self.thema == 'forest':
                        nommor.viego.forest_tree_item += 1
                    elif self.thema == 'desert':
                        nommor.viego.desert_tree_item += 1
                    elif self.thema == 'snow':
                        if self.stage == 1:
                            nommor.viego.snow_tree_item += 1
                        else:
                            nommor.viego.gold_tree_item += 1

    def handle_monster_attack_collision(self, group, other):
        pass