from pico2d import *

import logo_mode
from viego import Viego
import game_world
import game_framework
import stage_loader
import monster
import camera
running = True
cam = camera.Camera(2400, 600, 800, 600)
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
    global viego, monsters
    global soop_back, grass, cam

    # 맵 크기에 맞게 조정
    game_world.set_camera(cam)

    soop_back = stage_loader.Background('background/soop_back.png',3)
    game_world.add_object(soop_back,0)

    grass = stage_loader.Grass()
    game_world.add_object(grass,0)

    viego = Viego()
    game_world.add_object(viego, 1)
    game_world.set_player(viego)  # 플레이어로 설정
    game_world.add_object(viego,1)

    monsters = [monster.Ghost(viego) for _ in range(3)]
    game_world.add_objects(monsters, 1)

    game_world.add_collision_pair('viego:monster', viego, None)
    for m in monsters:
        game_world.add_collision_pair('viego:monster', None, m)
    pass

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    game_world.handle_collision()
    game_world.handle_attack_collision()
    game_world.handle_monster_attack_collision()
    pass

def draw():
    clear_canvas()
    game_world.draw()
    update_canvas()
    pass

