from pico2d import *

import logo_mode
from viego import Viego
import game_world
import game_framework

running = True

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(logo_mode)
        else:
            viego.handle_event(event)

def init():
    global running
    global world
    global viego

    viego = Viego()
    game_world.add_object(viego,1)
    pass
def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    pass

def draw():
    clear_canvas()
    game_world.draw()
    update_canvas()
    pass
