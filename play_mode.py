from pico2d import *

import logo_mode
from viego import Viego
import game_world
import game_framework
import stage_loader
import monster
import camera
running = True
current_stage = 1
current_theme = ('snow')  # 'forest', 'desert', 'castle', 'snow'
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
    global current_stage,current_theme

    # 스테이지 크기에 맞게 카메라 생성
    map_width, map_height = stage_loader.get_stage_size(current_theme, current_stage)
    cam = camera.Camera(map_width, map_height, 800, 600)
    game_world.set_camera(cam)

    back = stage_loader.Background(f'background/{current_theme}.png')
    game_world.add_object(back,0)

    platform = stage_loader.platform(f'background/{current_theme}_platform.png',current_stage)
    game_world.add_object(platform,0)

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

def change_stage(theme, stage_num):
    """스테이지 전환 함수"""
    global current_theme, current_stage, soop_back, grass, monsters

    current_theme = theme
    current_stage = stage_num

    # 1. 카메라 맵 크기 업데이트
    map_width, map_height = stage_loader.get_stage_size(theme, stage_num)
    cam.update_map_size(map_width, map_height)

    # 2. 게임 오브젝트 재로드
    game_world.clear_except_player()

    # 배경 재로드
    back = stage_loader.Background(f'background/{theme}_platform.png')
    game_world.add_object(back, 0)

    plat = stage_loader.platform(theme,stage_num)
    game_world.add_object(plat, 0)
