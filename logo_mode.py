from pico2d import *
import game_framework
import play_mode
image = None
running = True
def init():
    global image, running, logo_start_time
    image = load_image('Sprite_Sheets/main_character.png')
    running = True
    logo_start_time = get_time()
def finish():
    global image
    del(image)
def update():
    global running, logo_start_time

    if get_time() - logo_start_time >= 2.0:
        logo_start_time = get_time()
        game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    image.draw(400,300)
    update_canvas()

def handle_events():
    events = get_events()