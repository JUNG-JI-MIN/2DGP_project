from pico2d import *
import game_framework
import village_mode
import events
image = None
running = True
def init():
    global image, running, logo_start_time
    image = load_image('background/logo.png')
    running = True
    logo_start_time = get_time()
def finish():
    global image
    del(image)
def update():
    global running, logo_start_time

def draw():
    clear_canvas()
    draw_rectangle(0, 0, 800, 600,255 ,255, 255,1, True)
    image.clip_draw(
        50, 100,  # 원본에서 잘라낼 시작 위치 (x, y)
        976, 900,  # 잘라낼 크기 (width, height)
        400, 300,  # 화면에 그릴 위치 (중앙)
        600, 600  # 화면에 그릴 크기
    )
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:  # 아무 키나 누르면
            game_framework.change_mode(village_mode)