from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_UP


def space_down(event): # state_event 튜플
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_SPACE


def time_out(event):
    return event[0] == 'TIMEOUT'

def key_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN

def a_key(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == 97
def a_key_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == 97

def s_key_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == 115

def s_key_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == 115

def z_key_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == 122



def right_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_RIGHT

def left_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_LEFT

def up_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_UP

def up_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_UP

def right_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_RIGHT


def left_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_LEFT
