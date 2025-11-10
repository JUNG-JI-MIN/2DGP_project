from pico2d import *
import random
import game_framework
import sheet_list
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

animation_names = ['Idle']

class Ghost:
    img = None
    def __init__(self):
        if Ghost.img is None:
            Ghost.img = load_image('monster/dark_ghost.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.HP = 5

        self.int = 10

        self.IDLE_FRAME_PER_ACTION = 1

        self.x = random.randint(0,800)
        self.y = 70
        self.dir = 0
        self.frame = 0
        self.face_dir = 1

    def update(self):
        self.frame = (self.frame + self.IDLE_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

    def draw(self):
        f = sheet_list.dark_ghost_idle[int(self.frame)]
        if self.face_dir == 1:  # right
            Ghost.img.clip_draw(f[0], 949 - f[1] - f[3], f[2], f[3], self.x, self.y)
        else:  # face_dir == -1: # left
            Ghost.img.clip_composite_draw(
                f[0], 949 - f[1] - f[3], f[2], f[3], 0, 'h', self.x - 25 / 2 + f[2] / 2,
                      self.y - 45 / 2 + f[3] / 2, f[2], f[3])
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        # 바운딩 박스 (left, bottom, right, top)
        return (self.x - 30,
                self.y - 45,
                self.x + 30,
                self.y + 45)
    def handle_collision(self, group, other):
        pass
