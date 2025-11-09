from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP
from events import space_down, time_out, a_key, a_key_up, s_key_down, s_key_up, right_down, left_down, right_up, \
    left_up, up_down
from state_machine import StateMachine
import sheet_list
import game_framework

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm.
WALK_SPEED_KMPH = 20.0 # Km / Hour
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0) # Meter / Minute
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0) # Meter / Second
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER) # 초당 픽셀 이동 거리 (Pixel Per Second)
JUMP_HEIGHT_PSS = WALK_SPEED_PPS * 1.5 # 점프 높이 (Pixel Per Second Speed)
DASH_SPEED_PSS = WALK_SPEED_PPS * 2 # 대쉬 속도 (Pixel Per Second Speed)

GRAVITY = 1000 / 3 # 중력 가속도 cm / s^2

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
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x, self.viego.y)
        else:
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', self.viego.x, self.viego.y,f[2], f[3])
class jump:

    def __init__(self, viego):
        self.viego = viego
        self.velocity = JUMP_HEIGHT_PSS
    def enter(self, e):
        self.viego.is_jumping = True
        pass
    def exit(self, e):
        self.viego.is_jumping = False
        self.viego.y = 90
        pass
    def do(self):
        if self.viego.is_dashing:
            self.viego.x += self.viego.dir * DASH_SPEED_PSS * game_framework.frame_time
        elif self.viego.dir != 0:
            self.viego.x += self.viego.dir * WALK_SPEED_PPS * game_framework.frame_time

        self.velocity -= GRAVITY * game_framework.frame_time
        self.viego.y += self.velocity * game_framework.frame_time

    def draw(self):
        f = sheet_list.viego_jump
        if self.viego.face_dir == 1:  # right
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x, self.viego.y)
        else:
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', self.viego.x, self.viego.y, f[2], f[3])

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
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x, self.viego.y)
        else:  # face_dir == -1: # left
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', self.viego.x, self.viego.y,f[2], f[3])

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
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x, self.viego.y)
        else:  # face_dir == -1: # left
            self.viego.img.clip_composite_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h',self.viego.x, self.viego.y,f[2],f[3])
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
        self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x, self.viego.y)


class Idle:
    def __init__(self, viego):
        self.viego = viego

    def enter(self,e):
        self.viego.is_dashing = False
        self.viego.dir = 0
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
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', self.viego.x, self.viego.y,f[2], f[3])

    pass

class Viego:
    img = None

    def __init__(self):
        if Viego.img is None:
            Viego.img = load_image('Sprite_Sheets/main_character.png')

        self.IDLE_FRAME_PER_ACTION  = 3
        self.SLEEP_FRAME_PER_ACTION = 7
        self.WALK_FRAME_PER_ACTION = 5
        self.DASH_FRAME_PER_ACTION = 6
        self.JUMP_FRAME_PER_ACTION = 2

        self.font = load_font('ENCR10B.TTF', 16)
        self.x, self.y = 400, 90
        self.dir = 0
        self.frame = 0
        self.face_dir = 1

        self.is_dashing = False
        self.is_guarding = False
        self.is_jumping = False

        self.IDLE = Idle(self)
        self.WALK = walk(self)
        self.DASH = dash(self)
        self.SLEEP = Sleep(self)
        self.GUARD = guard(self)
        self.JUMP = jump(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.SLEEP: {space_down: self.IDLE, right_down: self.WALK, left_down: self.WALK},
                self.IDLE: {time_out: self.SLEEP, right_down: self.WALK, left_down: self.WALK, right_up: self.WALK, left_up: self.WALK, s_key_down: self.GUARD, up_down : self.JUMP},
                self.WALK: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE, a_key: self.DASH, s_key_down: self.GUARD, up_down : self.JUMP},
                self.DASH: {a_key_up: self.WALK, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE, s_key_down: self.GUARD, up_down : self.JUMP},
                self.GUARD: {s_key_up: self.IDLE},
                self.JUMP: {}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == 97:
            self.is_dashing = True
        elif event.type == SDL_KEYUP and event.key == 97:
            self.is_dashing = False

        self.state_machine.handle_state_event(('INPUT', event))
        pass
    def get_bb(self):
        # 바운딩 박스 (left, bottom, right, top)
        return (self.x - 10,
                self.y - 22,
                self.x + 10,
                self.y + 10)

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x-20, self.y+30, f'(Time: {get_time():.2f})' , (255, 255, 0))