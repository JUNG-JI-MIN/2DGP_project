from pico2d import *
from viego import Viego
import game_world

open_canvas(800,600)
running = True
img = load_image('Sprite_Sheets/main_character.png')
def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            viego.handle_event(event)

def world_reset():
    global running
    global world
    global viego

    viego = Viego()
    game_world.add_object(viego,1)
    pass
def update_world():
    game_world.update()
    pass
def render_world():
    clear_canvas()
    game_world.draw()
    update_canvas()
    pass

world_reset()
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)


close_canvas()
