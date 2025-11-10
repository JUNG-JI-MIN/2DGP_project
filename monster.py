from pico2d import *
import random
import game_framework
import game_world
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
    def __init__(self, viego=None):
        if Ghost.img is None:
            Ghost.img = load_image('monster/dark_ghost.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.viego = viego

        self.HP = 5
        self.die = False
        self.is_attacking = False
        self.int = 10

        self.IDLE_FRAME_PER_ACTION = 1
        ATTACK_FRAME_PER_ACTION = 3
        self.DIE_FRAME_PER_ACTION = 10

        self.x = random.randint(0,800)
        self.y = 70
        self.dir = 0
        self.frame = 0
        self.face_dir = 1

    def update(self):
        if self.die == True:
            if (self.frame <8):
                self.frame = (self.frame + self.DIE_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            else:
                game_world.remove_object(self)
        elif self.is_attacking:
            if (self.frame <5):
                self.frame = (self.frame + self.ATTACK_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            else:
                game_world.remove_object(self)
        else:
            self.frame = (self.frame + self.IDLE_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

    def draw(self):
        f = sheet_list.dark_ghost_idle[min(int(self.frame),5)]
        if self.die == True:
            f = sheet_list.dark_ghost_die[int(self.frame)]
        self.font.draw(self.x - 70, self.y + 70, f'(HP : {self.HP:.2f})', (255, 255, 0))
        if self.face_dir == 1:  # right
            Ghost.img.clip_draw(f[0], 949 - f[1] - f[3], f[2], f[3], self.x, self.y)
        else:  # face_dir == -1: # left
            Ghost.img.clip_composite_draw(
                f[0], 949 - f[1] - f[3], f[2], f[3], 0, 'h', self.x - 25 / 2 + f[2] / 2,
                      self.y - 45 / 2 + f[3] / 2, f[2], f[3])
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_attack_bb(),0,0,255)

    def handle_event(self, event):
        pass

    def get_bb(self):
        # 바운딩 박스 (left, bottom, right, top)
        return (self.x - 30,
                self.y - 45,
                self.x + 30,
                self.y + 45)
    def get_attack_bb(self):
        return (self.x - 100,
                self.y - 100,
                self.x + 100,
                self.y + 100)

    def handle_collision(self, group, other):
        if group == 'viego:monster':
            pass

    def handle_attack_collision(self, group, other):
        if group == 'viego:monster':
            if self.viego.is_attacking:
                self.HP -= self.viego.int / 10
                if self.HP <= 0:
                    self.die = True
                    self.frame = 0
                    for a in game_world.collision_pairs['viego:monster'][1]:
                        if a == self:
                            game_world.collision_pairs['viego:monster'][1].remove(a)

    def handle_monster_attack_collision(self,group, other):
        if group == 'viego:monster':
            if not self.is_attacking:
                self.is_attacking = True