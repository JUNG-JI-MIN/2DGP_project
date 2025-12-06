from pico2d import *
import random
import game_framework
import game_world
import sheet_list
import item
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

animation_names = ['Idle']
class fireball:
    img = None

    def __init__(self, x,y):
        if fireball.img is None:
            fireball.img = load_image('monster/dark_ghost.png')
        self.font = load_font('ENCR10B.TTF', 16)

        self.frame = 0

        self.ATTACK_FRAME_PER_ACTION = 2
        self.x = x
        self.y = y

    def update(self):
        if (self.frame <2):
            self.frame = (self.frame + self.ATTACK_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        else:
            game_world.remove_object(self)
    def draw(self):
        f = sheet_list.dark_ghost_attack[1][min(int(self.frame),0)]
        screen_x, screen_y = game_world.render(self, self.x, self.y)  # 카메라 좌표로 변환

        fireball.img.clip_draw(f[0], 949 - f[1] - f[3], f[2], f[3], screen_x, screen_y)
class Ghost:
    img = None
    def __init__(self, viego=None):
        if Ghost.img is None:
            Ghost.img = load_image('monster/dark_ghost.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.viego = viego

        self.HP = 1
        self.die = False
        self.is_attacking = False
        self.idle = False
        self.walk = True
        self.int = 10

        self.IDLE_FRAME_PER_ACTION = 1
        self.ATTACK_FRAME_PER_ACTION = 6
        self.DIE_FRAME_PER_ACTION = 10
        self.RUN_FRAME_PER_ACTION = 8

        self.x = random.randint(0,2400)
        self.mx = self.x - 500
        self.Mx = self.x + 500
        self.y = 90
        self.dir = 1
        self.frame = random.randint(1,3)
        self.face_dir = 1


    def update(self):
        prev = self.frame
        if self.die == True:
            if (self.frame <8):
                self.frame = (self.frame + self.DIE_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            else:
                game_world.remove_object(self)
                ITEM = item.Item(self.x, self.y - 50, 'ghost')
                game_world.add_object(ITEM)
                game_world.add_collision_pair('viego:item', None, ITEM)
        elif self.is_attacking:
            if (self.frame <5):
                self.frame = (self.frame + self.ATTACK_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

            else:
                self.is_attacking = False
                self.face_dir = self.dir
            if int(prev) < 2 <= int(self.frame):
                if self.viego:
                    ball = fireball(self.viego.x, self.viego.y)
                    game_world.add_object(ball)
        elif self.walk == True:
            self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
            self.frame = (self.frame + self.RUN_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
            if self.x >= self.Mx:
                self.dir *= -1
                self.face_dir *= -1
            elif self.x <= self.mx:
                self.dir *= -1
                self.face_dir *= -1

        else:
            self.frame = (self.frame + self.IDLE_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

    def draw(self):
        f = sheet_list.dark_ghost_idle[min(int(self.frame),5)] # 안전하게 인덱스 접근
        screen_x, screen_y = game_world.render(self, self.x, self.y) # 카메라 좌표로 변환

        if self.die == True:
            f = sheet_list.dark_ghost_die[int(self.frame)]
        elif self.is_attacking == True:
            f = sheet_list.dark_ghost_attack[0][min(int(self.frame),4)] # 안전하게 인덱스 접근
        elif self.walk == True:
            f = sheet_list.dark_ghost_walk[min(int(self.frame),5)] # 안전하게 인덱스 접근

        self.font.draw(screen_x - 70, screen_y + 70, f'(HP : {self.HP:.2f})', (255, 255, 0))

        if self.face_dir == -1:  # right
            Ghost.img.clip_draw(f[0], 949 - f[1] - f[3], f[2], f[3], screen_x, screen_y)
        else:  # face_dir == -1: # left
            Ghost.img.clip_composite_draw(
                f[0], 949 - f[1] - f[3], f[2], f[3], 0, 'h', screen_x,
                      screen_y , f[2], f[3])

        # 카메라 오프셋 계산
        offset_x = screen_x - self.x
        offset_y = screen_y - self.y

        # 바운딩 박스를 카메라 좌표로 변환
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left + offset_x, bottom + offset_y, right + offset_x, top + offset_y)

        # 공격 범위를 카메라 좌표로 변환
        left, bottom, right, top = self.get_attack_bb()
        draw_rectangle(left + offset_x, bottom + offset_y, right + offset_x, top + offset_y, 0, 0, 255)

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
            if self.viego.is_attacking and not self.viego.attack_hit_done :
                self.HP -= self.viego.int / 10
                self.viego.attack_hit_done = True
                if self.HP <= 0:
                    self.die = True
                    self.frame = 0

                    for a in game_world.collision_pairs['viego:monster'][1]:
                        if a == self:
                            game_world.collision_pairs['viego:monster'][1].remove(a)


    def handle_monster_attack_collision(self,group, other):
        if group == 'viego:monster':
            if not self.is_attacking:
                if (self.viego.x > self.x):
                    self.face_dir = 1
                else:
                    self.face_dir = -1
                self.frame = 0
                self.is_attacking = True

class Yeti:
    img = None

    def __init__(self, viego=None):
        if Yeti.img is None:
            Yeti.img = load_image('monster/Yeti.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.viego = viego

        self.HP = 100
        self.die = False
        self.is_attacking = False
        self.idle = False
        self.walk = True
        self.int = 10

        self.IDLE_FRAME_PER_ACTION = 1 # 3
        self.ATTACK_FRAME_PER_ACTION = 6 # 6
        self.DIE_FRAME_PER_ACTION = 10 # 4
        self.RUN_FRAME_PER_ACTION = 8 # 4

        self.x = random.randint(0, 2400)
        self.mx = self.x - 500
        self.Mx = self.x + 500
        self.y = 90
        self.dir = 1
        self.frame = random.randint(1, 3)
        self.face_dir = 1

    def update(self):
        prev = self.frame
        if self.die == True:
            if (self.frame < 4):
                self.frame = (self.frame + self.DIE_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            else:
                game_world.remove_object(self)
                ITEM = item.Item(self.x, self.y, 'ghost')
                game_world.add_object(ITEM)
                game_world.add_collision_pair('viego:item', None, ITEM)
        elif self.is_attacking:
            if (self.frame < 6):
                self.frame = (self.frame + self.ATTACK_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

            else:
                self.is_attacking = False
                self.face_dir = self.dir
        elif self.walk == True:
            self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
            self.frame = (self.frame + self.RUN_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
            if self.x >= self.Mx:
                self.dir *= -1
                self.face_dir *= -1
            elif self.x <= self.mx:
                self.dir *= -1
                self.face_dir *= -1

        else:
            self.frame = (self.frame + self.IDLE_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

    def draw(self):
        f = sheet_list.yeti_idle[min(int(self.frame), 0)]  # 안전하게 인덱스 접근
        screen_x, screen_y = game_world.render(self, self.x, self.y)  # 카메라 좌표로 변환

        if self.die == True:
            f = sheet_list.yeti_die[int(self.frame)]
        elif self.is_attacking == True:
            f = sheet_list.yeti_attack[min(int(self.frame), 3)]  # 안전하게 인덱스 접근
        elif self.walk == True:
            f = sheet_list.yeti_walk[min(int(self.frame), 3)]  # 안전하게 인덱스 접근

        self.font.draw(screen_x - 70, screen_y + 70, f'(HP : {self.HP:.2f})', (255, 255, 0))

        if self.face_dir == -1:  # right
            Yeti.img.clip_draw(f[0], 1116 - f[1] - f[3], f[2], f[3], screen_x, screen_y)
        else:  # face_dir == -1: # left
            Yeti.img.clip_composite_draw(
                f[0], 1116 - f[1] - f[3], f[2], f[3], 0, 'h', screen_x,
                screen_y, f[2], f[3])

        # 카메라 오프셋 계산
        offset_x = screen_x - self.x
        offset_y = screen_y - self.y

        # 바운딩 박스를 카메라 좌표로 변환
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left + offset_x, bottom + offset_y, right + offset_x, top + offset_y)

        # 공격 범위를 카메라 좌표로 변환
        left, bottom, right, top = self.get_attack_bb()
        draw_rectangle(left + offset_x, bottom + offset_y, right + offset_x, top + offset_y, 0, 0, 255)

    def handle_event(self, event):
        pass

    def get_bb(self):
        # 바운딩 박스 (left, bottom, right, top)
        return (self.x - 30,
                self.y - 45,
                self.x + 30,
                self.y + 45)

    def get_attack_bb(self):
        return (self.x - 70,
                self.y - 30,
                self.x + 70,
                self.y + 30)

    def handle_collision(self, group, other):
        if group == 'viego:monster':
            pass

    def handle_attack_collision(self, group, other):
        if group == 'viego:monster':
            if self.viego.is_attacking and not self.viego.attack_hit_done:
                self.HP -= self.viego.int / 10
                self.viego.attack_hit_done = True
                if self.HP <= 0:
                    self.die = True
                    self.frame = 0

                    for a in game_world.collision_pairs['viego:monster'][1]:
                        if a == self:
                            game_world.collision_pairs['viego:monster'][1].remove(a)


    def handle_monster_attack_collision(self, group, other):
        if group == 'viego:monster':
            if not self.is_attacking:
                if (self.viego.x > self.x):
                    self.face_dir = 1
                else:
                    self.face_dir = -1
                self.frame = 0
                self.is_attacking = True