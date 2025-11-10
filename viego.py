from pico2d import load_image, get_time, load_font, draw_rectangle
from pyvisalgo.welzl import min_circle_trivial
from sdl2 import SDL_KEYDOWN, SDL_KEYUP
from events import space_down, time_out, a_key, a_key_up, s_key_down, s_key_up, right_down, left_down, right_up, \
    left_up, up_down, up_up, z_key_down
from state_machine import StateMachine
import sheet_list
import game_framework

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm.
WALK_SPEED_KMPH = 20.0 # Km / Hour
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0) # Meter / Minute
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0) # Meter / Second
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER) # 초당 픽셀 이동 거리 (Pixel Per Second)
JUMP_HEIGHT_PSS = WALK_SPEED_PPS # 점프 높이 (Pixel Per Second Speed)
DASH_SPEED_PSS = WALK_SPEED_PPS * 2 # 대쉬 속도 (Pixel Per Second Speed)

GRAVITY = 1000 / 3  # 중력 가속도 cm / s^2

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

class guard:
    def __init__(self, viego):
        self.viego = viego

    def enter(self,e):
        self.viego.is_guarding = True

    def exit(self,e):
        self.viego.frame = 0
        self.viego.is_guarding = False
    def do(self):
        pass

    def draw(self):
        f = sheet_list.viego_guard
        if self.viego.face_dir == 1:
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x + self.viego.face_dir *5, self.viego.y)
        else:
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', self.viego.x -25/2 + f[2]/2+ self.viego.face_dir *5,self.viego.y -45/2 + f[3]/2,f[2], f[3])
class jump:

    def __init__(self, viego):
        self.viego = viego
        self.velocity = JUMP_HEIGHT_PSS
        self.is_holding = False
        self.min_jump_speed = JUMP_HEIGHT_PSS * 0.7  # 최소 점프 속도
        self.max_jump_speed = JUMP_HEIGHT_PSS * 3  # 최대 점프 속도

    def enter(self, e):
        if up_up(e):
            self.is_holding = False
            return
        if up_down(e):
            self.velocity = self.min_jump_speed
            self.viego.is_jumping = True
            self.is_holding = True

        # 방향 설정 개선
        if right_down(e):
            self.viego.dir = self.viego.face_dir = 1
        elif left_down(e):
            self.viego.dir = self.viego.face_dir = -1
        elif right_up(e):
            # 오른쪽 키를 뗐을 때만 멈춤 (왼쪽 키가 안 눌려있으면)
            if self.viego.dir == 1:  # 오른쪽으로 가고 있었다면
                self.viego.dir = 0
        elif left_up(e):
            # 왼쪽 키를 뗐을 때만 멈춤 (오른쪽 키가 안 눌려있으면)
            if self.viego.dir == -1:  # 왼쪽으로 가고 있었다면
                self.viego.dir = 0

    def exit(self, e):
        if up_up(e):
            self.viego.is_jumping = False
            self.is_holding = False

    def do(self):
        # 1. 점프 키를 누르고 있고 상승 중일 때만 속도 증가
        if self.is_holding and self.velocity > 0:
            self.velocity = min(
                self.velocity + self.min_jump_speed * 2 * game_framework.frame_time,
                self.max_jump_speed
            )

        # 2. 중력은 항상 적용 (속도 감소)
        self.velocity -= GRAVITY * game_framework.frame_time

        # 3. y 좌표 업데이트
        self.viego.y += self.velocity * game_framework.frame_time

        # 4. 착지 감지
        if self.viego.y < 50:
            self.viego.y = 50
            self.viego.is_jumping = False
            if self.viego.is_dashing:
                self.viego.state_machine.cur_state = self.viego.DASH
            elif self.viego.dir != 0:
                self.viego.state_machine.cur_state = self.viego.WALK
            else:
                self.viego.state_machine.handle_state_event(('TIMEOUT', None))
            return

        # 5. 좌우 이동
        if self.viego.is_dashing:
            self.viego.x += self.viego.dir * DASH_SPEED_PSS * game_framework.frame_time
        elif self.viego.dir != 0:
            self.viego.x += self.viego.dir * WALK_SPEED_PPS * game_framework.frame_time

    def draw(self):
        f = sheet_list.viego_jump
        if self.viego.face_dir == 1:  # right
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x,self.viego.y)
        else:
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', self.viego.x -25/2 + f[2]/2,self.viego.y -45/2 + f[3]/2, f[2], f[3])
class dash:
    def __init__(self, viego):
        self.viego = viego
    def enter(self,e):
        self.viego.is_dashing = True
        pass
    def exit(self,e):
        pass
    def do(self):
        self.viego.frame =  (self.viego.frame + self.viego.DASH_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.viego.x += self.viego.dir * DASH_SPEED_PSS * game_framework.frame_time
        pass
    def draw(self):
        f = sheet_list.viego_dash[int(self.viego.frame)]
        if self.viego.face_dir == 1:  # right
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x,self.viego.y -45/2 + f[3]/2)
        else:  # face_dir == -1: # left
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', self.viego.x -25/2 + f[2]/2,self.viego.y -45/2 + f[3]/2,f[2], f[3])
class walk:
    def __init__(self, viego):
        self.viego = viego

    def enter(self,e):
        self.viego.is_dashing = False
        if right_down(e) or left_up(e):
            self.viego.dir = self.viego.face_dir = 1
        elif left_down(e) or right_up(e):
            self.viego.dir = self.viego.face_dir = -1
        pass

    def exit(self,e):
        self.viego.frame = 0
        pass

    def do(self):
        if self.viego.is_dashing:
            self.viego.state_machine.cur_state = self.viego.DASH
            return
        self.viego.frame=(self.viego.frame + self.viego.WALK_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.viego.x += self.viego.dir * WALK_SPEED_PPS * game_framework.frame_time
        pass

    def draw(self):
        f = sheet_list.viego_walk[int(self.viego.frame)]
        if self.viego.face_dir == 1:  # right
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x -25/2 + f[2]/2,self.viego.y -45/2 + f[3]/2)
        else:  # face_dir == -1: # left
            self.viego.img.clip_composite_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h',self.viego.x,self.viego.y,f[2],f[3])
class Sleep:
    def __init__(self, viego):
        self.viego = viego

    def enter(self,e):
        self.viego.dir = 0
        self.viego.face_dir = 0

    def exit(self,e):
        self.viego.frame = 0

    def do(self):
        if (self.viego.frame < 6):
            self.viego.frame = (self.viego.frame + self.viego.SLEEP_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

    def draw(self):
        f = sheet_list.viego_sleep[int(self.viego.frame)]
        self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x -25/2 + f[2]/2,self.viego.y -45/2 + f[3]/2)
class attack:
    def __init__(self, viego):
        self.viego = viego
        self.count = 0
        self.attack_timer = 0
        self.combo_time_limit = 1.0  # 콤보 타임 제한 (초)


    def enter(self,e):
        # 이전 공격에서 1.0초 이내에 다시 공격하면 콤보 증가
        self.viego.is_attacking = True
        self.viego.frame = 0

        if get_time() - self.attack_timer < self.combo_time_limit:
            self.count = (self.count + 1) % 5  # 0~4 순환
        else:
            self.count = 0  # 시간이 지나면 첫 번째 공격으로

        self.viego.x += self.viego.face_dir * WALK_SPEED_PPS * game_framework.frame_time * 50

    def exit(self,e):
        self.viego.is_attacking = False
        self.attack_timer = get_time()
        pass

    def do(self):
        acombo = (6, 6, 5, 9, 7)  # 각 공격 모션의 프레임 수
        if int(self.viego.frame) < acombo[self.count]:
            self.viego.frame = (self.viego.frame + self.viego.ATTACK_FRAME_PER_ACTION * self.viego.ATTACK_SPEED * game_framework.frame_time)
        else:
            self.viego.state_machine.handle_state_event(('TIMEOUT', None))


    def draw(self):
        acombo = (6, 6, 5, 9, 7)
        index = min(int(self.viego.frame), acombo[self.count] - 1)
        draw_rectangle(*self.viego.get_attack_bb(),0,0,255)
        f = sheet_list.viego_attack[self.count][index]
        if self.viego.face_dir == 1:  # right
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x -25/2 + f[2]/2,self.viego.y -45/2 + f[3]/2)
        else:  # face_dir == -1: # left
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', self.viego.x,self.viego.y -45/2 + f[3]/2, f[2], f[3])


class Idle:
    def __init__(self, viego):
        self.viego = viego

    def enter(self,e):
        self.viego.is_dashing = False
        self.viego.dir = 0
        self.viego.frame = 0
        self.viego.wait_start_time = get_time()

    def exit(self,e):
        self.viego.frame = 0
        pass

    def do(self):
        self.viego.frame=(self.viego.frame + self.viego.IDLE_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        if get_time() - self.viego.wait_start_time > 2.0:
            # 2초 대기 후 자동으로 Sleep 상태로 전이
            self.viego.state_machine.handle_state_event(('TIMEOUT', None))
        pass

    def draw(self):
        f = sheet_list.viego_idle[int(self.viego.frame)]
        if self.viego.face_dir == 1:  # right
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x, self.viego.y)
        else:  # face_dir == -1: # left
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', self.viego.x -25/2 + f[2]/2,self.viego.y -45/2 + f[3]/2,f[2], f[3])

    pass

class Viego:
    img = None

    def __init__(self):
        self.attack_range = ((50, 45), (50, 45), (50, 45), (50, 45), (50, 45))
        if Viego.img is None:
            Viego.img = load_image('Sprite_Sheets/main_character.png')

        self.HP = 5
        self.ste = 100

        self.str = 10
        self.int = 10
        self.dex = 10

        self.IDLE_FRAME_PER_ACTION  = 3
        self.SLEEP_FRAME_PER_ACTION = 7
        self.WALK_FRAME_PER_ACTION = 5
        self.DASH_FRAME_PER_ACTION = 6
        self.JUMP_FRAME_PER_ACTION = 2
        self.ATTACK_FRAME_PER_ACTION = 5
        self.ATTACK_SPEED = 0.25 * self.dex

        self.font = load_font('ENCR10B.TTF', 16)
        self.x, self.y = 400, 50
        self.dir = 0
        self.frame = 0
        self.face_dir = 1

        self.is_dashing = False
        self.is_guarding = False
        self.is_jumping = False
        self.is_attacking = False
        self.mujuck_frame = 0
        self.MUJUCK_TIME = 0.5  # 무적 지속 시간(초)

        self.IDLE = Idle(self)
        self.WALK = walk(self)
        self.DASH = dash(self)
        self.SLEEP = Sleep(self)
        self.GUARD = guard(self)
        self.JUMP = jump(self)
        self.ATTACK = attack(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.SLEEP: {space_down: self.IDLE, right_down: self.WALK, left_down: self.WALK},
                self.IDLE: {time_out: self.SLEEP, right_down: self.WALK, left_down: self.WALK, right_up: self.WALK, left_up: self.WALK, s_key_down: self.GUARD, up_down : self.JUMP,z_key_down : self.ATTACK},
                self.WALK: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE, a_key: self.DASH, s_key_down: self.GUARD, up_down : self.JUMP,z_key_down : self.ATTACK},
                self.DASH: {a_key_up: self.WALK, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE, s_key_down: self.GUARD, up_down : self.JUMP,z_key_down : self.ATTACK},
                self.GUARD: {s_key_up: self.IDLE,z_key_down : self.ATTACK},
                self.JUMP: {time_out: self.IDLE,left_down : self.JUMP, right_down : self.JUMP, right_up: self.JUMP, left_up: self.JUMP,up_up : self.JUMP},
                self.ATTACK: {time_out : self.IDLE,s_key_down: self.GUARD}
            }
        )
    def get_attack_bb(self):
        if self.face_dir == 1:
            return (
                self.x + (30 * self.face_dir) - self.attack_range[self.ATTACK.count][0] / 2 + 10,
                self.y - self.attack_range[self.ATTACK.count][1] / 2,
                self.x + (30 * self.face_dir) + self.attack_range[self.ATTACK.count][0] / 2 + 10,
                self.y + self.attack_range[self.ATTACK.count][1] / 2
            )
        return (
            self.x + (30 * self.face_dir) - self.attack_range[self.ATTACK.count][0] / 2,
            self.y - self.attack_range[self.ATTACK.count][1] / 2,
            self.x + (30 * self.face_dir) + self.attack_range[self.ATTACK.count][0] / 2,
            self.y + self.attack_range[self.ATTACK.count][1] / 2
        )

    def update(self):
        self.state_machine.update()
        if self.mujuck_frame > 0.0:
            self.mujuck_frame -= game_framework.frame_time
            if self.mujuck_frame <= 0.0:
                self.mujuck_frame = 0.0

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == 97:
            self.is_dashing = True
        elif event.type == SDL_KEYUP and event.key == 97:
            self.is_dashing = False

        self.state_machine.handle_state_event(('INPUT', event))
        pass
    def get_foot_y(self):
        return self.y - 22
    def get_bb(self):
        # 바운딩 박스 (left, bottom, right, top)
        return (self.x - 10,
                self.y - 22,
                self.x + 20,
                self.y + 22)

    def handle_collision(self, group, other):
        if group == 'viego:monster':
            if self.mujuck_frame > 0.0:
                return

            if self.is_guarding:
                self.ste -= 5
                if self.ste < 0:
                    self.ste = 0
                self.mujuck_frame = self.MUJUCK_TIME
                return

            # 무적이 아니면 데미지 적용 후 무적 시작
            self.HP -= other.int * 0.1
            if self.HP < 0:
                self.HP = 0
            self.mujuck_frame = self.MUJUCK_TIME

    def handle_attack_collision(self,group, other):
        if group == 'viego:monster':
            pass
    def handle_monster_attack_collision(self,group, other):
        if group == 'viego:monster':
            pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x-70, self.y+30, f'(HP : {self.HP:.2f},SP : {self.ste:.2f})' , (255, 255, 0))