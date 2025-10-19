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

def right_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_RIGHT

def left_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_LEFT

def right_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_RIGHT

def left_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_LEFT



class Idle:
    def __init__(self, char):
        self.char = char

    def enter(self,e):
        self.char.dir = 0
        self.char.wait_start_time = get_time()

    def exit(self,e):
        self.char.frame = 0
        pass

    def do(self):
        self.char.frame=(self.char.frame+1)%3
        if get_time() - self.char.wait_start_time > 5.0:
            # 2초 대기 후 자동으로 Sleep 상태로 전이
            self.char.state_machine.handle_state_event(('TIMEOUT', None))
        pass

    def draw(self):
        f = sheet_list.viego_idle[self.char.frame]
        self.char.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], self.char.x, self.char.y)
    pass

class Viego:
    img = None

    def __init__(self):
        if Viego.img is None:
            Viego.img = load_image('Sprite_Sheets/main_character.png')
        self.x, self.y = 400, 300
        self.dir = 0
        self.frame = 0
        self.face_dir = 1
        self.IDLE = Idle(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {time_out: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()