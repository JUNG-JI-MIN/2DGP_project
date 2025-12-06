from pico2d import *
import random
import game_framework
import game_world
import sheet_list
import nommor
import item
from BT import BehaviorTree, Action, Sequence, Condition, Selector

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

class wolf_attack:
    def __init__(self, x,y, wolf):
        self.wolf = wolf
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
        pass
    def get_bb(self):
        return (self.x - 15,
                self.y - 15,
                self.x + 15,
                self.y + 15)
    def get_attack_bb(self):
        return (self.x - 20,
                self.y - 20,
                self.x + 20,
                self.y + 20)
    def handle_collision(self, group, other):
        if group == 'viego:monster':
            nommor.viego.HP -= self.wolf.str
            pass
    def handle_attack_collision(self, group, other):
        pass

    def handle_monster_attack_collision(self,group, other):
        pass
class Wolf:
    img = None
    def __init__(self):
        if Wolf.img is None:
            Wolf.img = load_image('monster/Lycanthrope.png')
        self.font = load_font('ENCR10B.TTF', 16)

        self.HP = 1000
        self.str = 10

        self.IDLE_FRAME_PER_ACTION = 1
        self.ATTACK_FRAME_PER_ACTION = 6
        self.DIE_FRAME_PER_ACTION = 10
        self.RUN_FRAME_PER_ACTION = 8

        self.attack = False
        self.idle = True
        self.walk = False
        self.die = False
        self.pohyo = False
        self.can_attack = True

        self.x = random.randint(0,2400)
        self.y = 90
        self.dir = 1
        self.frame = random.randint(1,3)
        self.face_dir = 1

        self.build_behavior_tree()

    def update(self):
        prev = self.frame

        if self.die == True:
            if (self.frame <5):
                self.frame = (self.frame + self.DIE_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            else:
                game_world.remove_object(self)
                ITEM = item.Item(self.x, self.y- 50, 'wolf')
                game_world.add_object(ITEM)
                game_world.add_collision_pair('viego:item', None, ITEM)
        elif self.attack == True:
            if (self.frame <5):
                self.frame = (self.frame + self.ATTACK_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

            else:
                self.is_attacking = False
                self.face_dir = self.dir
            if int(prev) < 2 <= int(self.frame):
                if nommor.viego:
                    self.can_attack = True
                    ball = wolf_attack(self.x, self.y)
                    game_world.add_object(ball)
                    game_world.add_collision_pair('viego:monster_attack', None, ball)
        elif self.walk == True:
            self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
            self.frame = (self.frame + self.RUN_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        else:
            self.frame = (self.frame + self.IDLE_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        pass

    def draw(self):
        f = sheet_list.wolf_idle[min(int(self.frame),2)] # 안전하게 인덱스 접근
        screen_x, screen_y = game_world.render(self, self.x, self.y)  # 카메라 좌표로 변환

        if self.die == True:
            f = sheet_list.wolf_die[int(self.frame)]

        elif self.attack == True:
            f = sheet_list.wolf_attack[min(int(self.frame),4)] # 안전하게 인덱스 접근

        elif self.walk == True:
            f = sheet_list.wolf_walk[min(int(self.frame),3)] # 안전하게 인덱스 접근

        elif self.pohyo == True:
            f = sheet_list.wolf_pohyo[min(int(self.frame),4)] # 안전하게 인덱스 접근

        elif self.pohyo == True:
            f = sheet_list.wolf_pohyo[min(int(self.frame),6)] # 안전하게 인덱스 접근

        self.font.draw(screen_x - 70, screen_y + 70, f'(HP : {self.HP:.2f})', (255, 255, 0))

        if self.face_dir == -1:  # right
            Wolf.img.clip_draw(f[0], 1322 - f[1] - f[3], f[2], f[3], screen_x, screen_y)
        else:  # face_dir == -1: # left
            Wolf.img.clip_composite_draw(
                f[0], 1322 - f[1] - f[3], f[2], f[3], 0, 'h', screen_x,
                      screen_y , f[2], f[3])

        # 카메라 오프셋 계산
        offset_x = screen_x - self.x
        offset_y = screen_y - self.y

        # 바운딩 박스를 카메라 좌표로 변환
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left + offset_x, bottom + offset_y, right + offset_x, top + offset_y)

    def handle_event(self, event):
        pass

    def get_bb(self):
        # 바운딩 박스 (left, bottom, right, top)
        return (self.x - 40,
                self.y - 60,
                self.x + 40,
                self.y + 60)
    def get_attack_bb(self):
        return (self.x - 100,
                self.y - 100,
                self.x + 100,
                self.y + 100)

    def handle_collision(self, group, other):
        if group == 'viego:monster':
            pass

    def handle_attack_collision(self, group, other):
        if group == 'viego:monster_attack':
            if self.can_attack:
                self.HP -= nommor.viego.str
            pass

    def handle_monster_attack_collision(self,group, other):
            pass

    def distance_less_than(self):
        distance = (nommor.viego.x - self.x) ** 2 + (nommor.viego.y - self.y) ** 2
        return distance < 50 ** 2
        pass

    def distance_more_than(self, x1, y1, x2, y2, r):
        distance = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance > (PIXEL_PER_METER * r) ** 2
        pass

    def move_little_to(self, tx, ty):
        # frame time 을 이용해서 이동 거리 계산
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)
        pass

    def is_hp_low(self):
        return self.HP < 300

    def attack_player(self):
        self.attack = True
        self.idle = False
        self.walk = False
        self.die = False
        self.pohyo = False
        self.can_attack = True
        pass

    def go_to_player(self):
        self.attack = False
        self.idle = False
        self.walk = True
        self.die = False
        self.pohyo = False
        pass

    def runaway_from_player(self):
        self.attack = False
        self.idle = False
        self.walk = True
        self.die = False
        self.pohyo = False
        pass

    def build_behavior_tree(self):

        a1 = Action('Attack Player', self.attack_player)
        a2 = Action('Go to Player', self.go_to_player)
        a3 = Action('Runaway from Player', self.runaway_from_player)

        c1 = Condition('Distance < 50', self.distance_less_than)
        c2 = Condition('HP < 300', self.is_hp_low)

        chase_boy_if_nearby = Sequence('go to player',c1,c2)

        pass

