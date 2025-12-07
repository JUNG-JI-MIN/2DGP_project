from pico2d import *
import random
import game_framework
import game_world
import quest_center
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
class wolf_pohyo:
    image = None
    def __init__(self,x,y):
        if wolf_pohyo.image is None:
            wolf_pohyo.image = load_image('monster/wolf_motion.png')

        self.x, self.y = x, y
        self.frame = 0
        self.int = 100

    def update(self):
        if (self.frame <2):
            self.frame = (self.frame + 5 * ACTION_PER_TIME * game_framework.frame_time)
        else:
            game_world.remove_object(self)
    def draw(self):
        screen_x, screen_y = game_world.render(self, self.x,self.y)  # 카메라 좌표로 변환
        wolf_pohyo.image.draw(screen_x, screen_y)


    def get_bb(self):
        return (
            self.x - 10,
            self.y - 10,
            self.x + 10,
            self.y + 10
        )
    def get_attack_bb(self):
        return (0,0,0,0)
    def handle_collision(self, group, other):
        pass
    def handle_attack_collision(self, group, other):
        pass

    def handle_monster_attack_collision(self,group, other):
        pass
class wolf_attack:
    def __init__(self, x,y, wolf):
        self.wolf = wolf
        self.int = wolf.int
        self.font = load_font('ENCR10B.TTF', 16)

        self.frame = 0

        self.ATTACK_FRAME_PER_ACTION = 2
        self.x = x
        self.y = y

    def update(self):
        if (self.frame <1):
            self.frame = (self.frame + self.ATTACK_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        else:
            game_world.remove_object(self)
    def draw(self):
        screen_x, screen_y = game_world.render(self, self.x, self.y)  # 카메라 좌표로 변환

        # 카메라 오프셋 계산
        offset_x = screen_x - self.x
        offset_y = screen_y - self.y

        # 바운딩 박스를 카메라 좌표로 변환
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left + offset_x, bottom + offset_y, right + offset_x, top + offset_y, 200, 200, 200)
        pass
    def get_bb(self):
        return (self.x - 200,
                self.y - 50,
                self.x + 200,
                self.y + 50)
    def get_attack_bb(self):
        return (self.x - 50,
                self.y - 20,
                self.x + 50,
                self.y + 20)
    def handle_collision(self, group, other):
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
        self.int = 100

        self.IDLE_FRAME_PER_ACTION = 1
        self.ATTACK_FRAME_PER_ACTION = 6
        self.DIE_FRAME_PER_ACTION = 10
        self.RUN_FRAME_PER_ACTION = 8

        self.attack = False
        self.idle = False
        self.walk = True
        self.die = False
        self.pohyo = False
        self.can_attack = True
        self.motion = False

        self.x = random.randint(0,2400)
        self.y = 90
        self.dir = 1
        self.frame = random.randint(1,3)
        self.face_dir = 1

        self.build_behavior_tree()

    def update(self):
        prev = self.frame
        print (self.HP)
        self.bt.run()
        if self.die:
            if (self.frame <5):
                self.frame = (self.frame + self.DIE_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            else:
                quest_center.update_quest('ghost')
                game_world.remove_object(self)
                ITEM = item.Item(self.x, self.y- 50, 'wolf')
                game_world.add_object(ITEM)
                game_world.add_collision_pair('viego:item', None, ITEM)
            if int(prev) < 1 <= int(self.frame):
                self.y -= 25
        elif self.pohyo:
            self.frame = (self.frame + self.ATTACK_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7

            if int(prev) < 6 <= int(self.frame):
                self.frame = 0
                self.motion = False
            elif int(prev) < 5 <= int(self.frame):
                p = wolf_pohyo(nommor.viego.x,nommor.viego.y)
                game_world.add_object(p)
                game_world.add_collision_pair('viego:monster', None, p)

        elif self.attack:
            self.frame = (self.frame + self.ATTACK_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5

            if int(prev) < 4 <= int(self.frame):
                self.frame = 0
                self.motion = False
            elif int(prev) < 2 <= int(self.frame):
                if nommor.viego:
                    ball = wolf_attack(self.x, self.y,self)
                    game_world.add_object(ball)
                    game_world.add_collision_pair('viego:monster', None, ball)
        elif self.walk:
            self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
            self.frame = (self.frame + self.RUN_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        else:
            self.frame = (self.frame + self.IDLE_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        pass

    def draw(self):
        screen_x, screen_y = game_world.render(self, self.x, self.y)  # 카메라 좌표로 변환
        print(self.walk)
        print(self.idle)
        if self.die == True:
            f = sheet_list.wolf_die[min(int(self.frame),4)]

        elif self.attack == True:
            f = sheet_list.wolf_attack[min(int(self.frame),4)] # 안전하게 인덱스 접근

        elif self.walk == True:
            f = sheet_list.wolf_walk[min(int(self.frame),3)] # 안전하게 인덱스 접근

        elif self.pohyo == True:
            f = sheet_list.wolf_pohyo[min(int(self.frame),4)] # 안전하게 인덱스 접근
        else:
            f = sheet_list.wolf_idle[min(int(self.frame), 2)]  # 안전하게 인덱스 접근

        self.font.draw(screen_x - 70, screen_y + 120, f'(HP : {self.HP:.2f})', (255, 255, 0))

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

        draw_rectangle(
            screen_x - 200,  # 왼쪽 (x - 200)
            screen_y - 200,  # 아래쪽 (y - 200)
            screen_x + 200,  # 오른쪽 (x + 200)
            screen_y + 200,  # 위쪽 (y + 200)
        )

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
        if group == 'viego:monster':
            if nommor.viego.is_attacking and not nommor.viego.attack_hit_done:
                self.HP -= nommor.viego.int / 10
                nommor.viego.attack_hit_done = True
                if self.HP <= 0:
                    self.die = True
                    self.frame = 0
                    game_world.remove_collision_object(self)

    def handle_monster_attack_collision(self,group, other):
            pass

    def distance_less_than(self):
        dx = abs(nommor.viego.x - self.x)
        dy = abs(nommor.viego.y - self.y)

        # X축 거리 200 이내 + Y축 차이 50 이내일 때만 공격
        if dx < 200 and dy < 200:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def player_more_than_y(self):
        if nommor.viego.y > self.y + 100:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
    def if_motion(self):
        if not self.motion:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def dead(self):
        if self.HP <= 0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def attack_player(self):
        if self.motion:
            return BehaviorTree.SUCCESS
        self.attack = True
        self.idle = False
        self.walk = False
        self.die = False
        self.pohyo = False
        self.can_attack = True
        self.motion = True
        return BehaviorTree.SUCCESS
    def hi_attack_player(self):
        if self.attack and self.motion:
            return BehaviorTree.SUCCESS
        self.attack = False
        self.idle = False
        self.walk = False
        self.die = False
        self.pohyo = True
        self.can_attack = False
        self.motion = True
        return BehaviorTree.SUCCESS
    def go_to_player(self):
        self.attack = False
        self.idle = False
        self.walk = True
        self.die = False
        self.pohyo = False
        self.motion = False
        if nommor.viego.x < self.x:
            self.dir = -1
            self.face_dir = -1
        else:
            self.dir = 1
            self.face_dir = 1
        return BehaviorTree.SUCCESS
    def dies(self):
        self.frame = 0
        self.attack = False
        self.idle = False
        self.walk = False
        self.die = True
        self.pohyo = False
        self.motion = True
        return BehaviorTree.SUCCESS
    def build_behavior_tree(self):

        a1 = Action('Attack Player', self.attack_player)
        a2 = Action('Go to Player', self.go_to_player)
        a3 = Action('Hi Attack Player', self.hi_attack_player)
        a4 = Action('Die', self.dies)

        c1 = Condition('Distance < 50', self.distance_less_than)
        c2 = Condition('Player Y > Monster Y + 100', self.player_more_than_y)
        c3 = Condition('If not in motion', self.if_motion)
        c4 = Condition('Dead', self.dead)

        hi_attack_node = Sequence('Attack Sequence', c2, a3)
        how_attack_node = Selector('뭘로 공격할거니', hi_attack_node, a1)
        attack_node = Sequence('공격 할거니?', c1, how_attack_node)

        attack_or_cahes = Selector('공격 아니면 추적',attack_node, a2)
        move_node = Sequence('지금 움직여도 됨?', c3, attack_or_cahes)

        living = Sequence('살아있니?', c4, a4)

        wolf_BH = Selector("늑대 행동 트리", living, move_node)

        root = wolf_BH

        self.bt = BehaviorTree(root)

        pass

