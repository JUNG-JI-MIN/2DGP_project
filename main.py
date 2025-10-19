from pico2d import *
import sheet_list

open_canvas(800,600)
running = True
img = load_image('Sprite_Sheets/main_character.png')

def walk():
    if not sheet_list.main_character_walk:
        return  # 프레임이 없으면 종료
    for frame in sheet_list.main_character_walk:
        clear_canvas()
        # frame은 (x, y, w, h)
        img.clip_draw(frame[0], 1545 - frame[1] - frame[3], frame[2], frame[3], 400, 300)
        update_canvas()
        delay(0.1)
def desh():
    if not sheet_list.main_character_dash:
        return  # 프레임이 없으면 종료
    for frame in sheet_list.main_character_dash:
        clear_canvas()
        # frame은 (x, y, w, h)
        img.clip_draw(frame[0], 1545 - frame[1] - frame[3], frame[2], frame[3], 400, 300)
        update_canvas()
        delay(0.1)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            pass
def world_reset():
    global running
    global world

    world = []


    pass
def update_world():
    for o in world:
        o.update()
    pass
def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()
    pass

world_reset()
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.1)


close_canvas()
