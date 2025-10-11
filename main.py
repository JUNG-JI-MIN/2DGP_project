from pico2d import *
open_canvas()
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

while running:
    handle_events()
    clear_canvas()
    img.draw(400, 300)
    update_canvas()
close_canvas()
