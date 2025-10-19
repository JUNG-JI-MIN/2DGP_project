from pico2d import load_image, get_time, update_canvas
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT
from state_machine import StateMachine
import sheet_list

# 이벤트를 확인하는 함수
def space_down(event): # state_event 튜플
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_SPACE

def time_out(event):
    return event[0] == 'TIMEOUT'

def crash(event):
    return event[0] == 'CRASH'

def a_key(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == 97

def a_key_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == 97

def right_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_RIGHT

def left_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_LEFT

def right_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_RIGHT

def left_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_LEFT
class guard:
    def __init__(self, viego):
        self.viego = viego

    def enter(self,e):
        self.viego.is_guarding = True

    def exit(self,e):
        self.viego.frame = 0
        self.viego.is_guarding = False
    def do(self):
        self.viego.frame = (self.viego.frame +1) % 60
        pass

    def draw(self):
        pass
class dash:
    def __init__(self, viego):
        self.viego = viego
    def enter(self,e):
        pass
    def exit(self,e):
        pass
    def do(self):
        self.viego.frame =  (self.viego.frame +1) % 60
        self.viego.x += self.viego.dir * 3.0
        pass
    def draw(self):
        f = sheet_list.viego_dash[self.viego.frame // 10]
        if self.viego.face_dir == 1:  # right
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x, self.viego.y)
        else:  # face_dir == -1: # left
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', self.viego.x, self.viego.y,f[2], f[3])

class walk:
    def __init__(self, viego):
        self.viego = viego

    def enter(self,e):

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
        self.viego.frame=(self.viego.frame+1)%50
        self.viego.x += self.viego.dir * 1.5
        pass

    def draw(self):
        f = sheet_list.viego_walk[self.viego.frame // 10]
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
        if (self.viego.frame < 600):
            self.viego.frame += 1

    def draw(self):
        f = sheet_list.viego_sleep[self.viego.frame // 100]
        self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.viego.x, self.viego.y)


class Idle:
    def __init__(self, viego):
        self.viego = viego

    def enter(self,e):
        self.viego.dir = 0
        self.viego.wait_start_time = get_time()

    def exit(self,e):
        self.viego.frame = 0
        pass

    def do(self):
        self.viego.frame=(self.viego.frame+1)%30
        if get_time() - self.viego.wait_start_time > 2.0:
            # 2초 대기 후 자동으로 Sleep 상태로 전이
            self.viego.state_machine.handle_state_event(('TIMEOUT', None))
        pass

    def draw(self):
        f = sheet_list.viego_idle[self.viego.frame // 10]
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
        self.x, self.y = 400, 90
        self.dir = 0
        self.frame = 0
        self.face_dir = 1

        self.is_dashing = False
        self.is_guarding = False

        self.IDLE = Idle(self)
        self.WALK = walk(self)
        self.DASH = dash(self)
        self.SLEEP = Sleep(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.SLEEP: {space_down: self.IDLE, right_down: self.WALK, left_down: self.WALK},
                self.IDLE: {time_out: self.SLEEP, right_down: self.WALK, left_down: self.WALK, right_up: self.WALK, left_up: self.WALK },
                self.WALK: {right_up: self.IDLE, left_up: self.IDLE,right_down: self.IDLE, left_down: self.IDLE, a_key : self.DASH},
                self.DASH: {a_key_up: self.WALK,right_up: self.IDLE, left_up: self.IDLE,right_down: self.IDLE, left_down: self.IDLE}
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

    def draw(self):
        self.state_machine.draw()