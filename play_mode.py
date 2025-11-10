from pico2d import *

import logo_mode
from viego import Viego
import game_world
import game_framework
import stage_loader
import monster
running = True

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            viego.handle_event(event)

def init():
    global running
    global world
    global viego, monster
    global soop_back, grass

    soop_back = stage_loader.Background('background/soop_back.png',3)
    game_world.add_object(soop_back,0)

    monsters = [monster.Ghost() for _ in range(3)]
    game_world.add_objects(monsters,1)

    grass = stage_loader.Grass()
    game_world.add_object(grass,0)

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
