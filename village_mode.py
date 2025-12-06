from pico2d import *
import game_framework
import play_mode
import game_world
import stage_loader
import camera
import nommor
import UI
import Bossmonster
import events
from viego import Viego

image = None
running = True
def init():
    global image, running
    global  back

    image = load_image('background/village.png')

    cam = camera.Camera(800, 600, 800, 600)
    game_world.set_camera(cam)

    back = stage_loader.Background('background/village.png')
    game_world.add_object(back,0)
    if nommor.viego == None:
        nommor.viego = Viego()
    nommor.viego.x = 400
    nommor.viego.y = 100
    game_world.add_object(nommor.viego, 1)
    game_world.set_player(nommor.viego)  # 플레이어로 설정

    if nommor.UI is None:
        nommor.UI = UI.UI()
    game_world.add_object(nommor.UI, 2)

    game_world.add_collision_pair('viego:portal', nommor.viego, None)
    game_world.add_collision_pair('viego:training', nommor.viego, None)

def finish():
    game_world.clear()
def update():
    game_world.update()
    game_world.handle_collision()
    if nommor.viego.x > 750:
        play_mode.current_theme = 'forest'
        play_mode.current_stage = 1
        game_framework.change_mode(play_mode)


def draw():
    clear_canvas()

    # 배경을 화면 전체에 맞춰 그리기
    back.image.clip_draw_to_origin(0, 100, 1344, 768, 0, 0, 800, 600)

    nommor.viego.draw()
    nommor.UI.draw()

    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:  # 아무 키나 누르면
            if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RETURN:
                game_framework.change_mode(play_mode)

        nommor.viego.handle_event(event)