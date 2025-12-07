from pico2d import *
import Bossmonster
import logo_mode
import village_mode
from viego import Viego
import game_world
import game_framework
import stage_loader
import monster
import camera
import nommor
import UI
import quest_center
running = True
monsters = []
current_stage = 1
current_theme = ('village')  #'village' 'forest', 'desert', 'snow'
cam = camera.Camera(2400, 600, 800, 600)
def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.x, 600 - event.y
            # 퀘스트 창이 열려있을 때만
            if nommor.UI.quest_chang:
                # 탭 클릭 (상단: y=545~515, x=490/590/690)
                if 490 <= mouse_x <= 580 and 515 <= mouse_y <= 545:
                    nommor.UI.quest_tab = 'available'
                elif 590 <= mouse_x <= 680 and 515 <= mouse_y <= 545:
                    nommor.UI.quest_tab = 'active'
                elif 690 <= mouse_x <= 780 and 515 <= mouse_y <= 545:
                    nommor.UI.quest_tab = 'completed'

                # 퀘스트 클릭 (available 탭에서만)
                if nommor.UI.quest_tab == 'available':
                    # 퀘스트 목록 영역: x=490~790, y=500부터 60px 간격
                    if 490 <= mouse_x <= 790 and 200 <= mouse_y <= 500:
                        index = (500 - mouse_y) // 60
                        if 0 <= index < len(quest_center.player_quest['available']):
                            qid = quest_center.player_quest['available'][index]
                            quest_center.start_quest(qid)
            # 상태창 클릭
            if nommor.UI.status_chang:
                if 245 <= mouse_x <= 300:
                    if 140 <= event.y <= 165:
                        if nommor.viego.money >= 300 + nommor.viego.str * 150:
                            nommor.viego.money -= 300 + nommor.viego.str * 150
                            nommor.viego.str += 5
                    elif 166 <= event.y <= 190:
                        if nommor.viego.money >= 300 + nommor.viego.int * 150:
                            nommor.viego.money -= 300 + nommor.viego.int * 150
                            nommor.viego.int += 5
                    elif 191 <= event.y <= 215:
                        if nommor.viego.money >= 300 + nommor.viego.dex * 150:
                            nommor.viego.money -= 300 + nommor.viego.dex * 150
                            nommor.viego.dex += 5

        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            if (nommor.UI.status_chang == False and
                    nommor.UI.item_chang == False and
                    nommor.UI.armor_chang == False and
                    nommor.UI.quest_chang == False):

                game_framework.change_mode(village_mode)
                nommor.viego.HP = nommor.viego.max_HP
                nommor.viego.ste = nommor.viego.max_STE
            else:
                nommor.UI.quest_chang = False
                nommor.UI.status_chang = False
                nommor.UI.item_chang = False
                nommor.UI.armor_chang = False
                # UI 토글
        elif event.type == SDL_KEYDOWN and event.key == 105:  # i: 아이템창 (ASCII 105)
            nommor.UI.item_chang = not nommor.UI.item_chang
        elif event.type == SDL_KEYDOWN and event.key == 99:  # c: 상태창 (ASCII 99)
            nommor.UI.status_chang = not nommor.UI.status_chang
        elif event.type == SDL_KEYDOWN and event.key == 101:  # e: 장비창 (ASCII 101)
            nommor.UI.armor_chang = not nommor.UI.armor_chang
        elif event.type == SDL_KEYDOWN and event.key == 113:  # q: 퀘스트창 (ASCII 113)
            nommor.UI.quest_chang = not nommor.UI.quest_chang
        else:
            nommor.viego.handle_event(event)

def init():
    global running
    global world
    global monsters
    global soop_back, grass, cam
    global current_stage,current_theme


    # 스테이지 크기에 맞게 카메라 생성
    map_width, map_height = stage_loader.get_stage_size(current_theme, current_stage)
    cam = camera.Camera(map_width, map_height, 800, 600)
    game_world.set_camera(cam)

    back = stage_loader.Background(f'background/{current_theme}.png', current_theme)
    game_world.add_object(back,0)

    trees = [stage_loader.Tree(f'background/{current_theme}_tree.png', current_theme, current_stage, i) for i in
             range(stage_loader.get_tree_count(current_theme, current_stage))]
    game_world.add_objects(trees, 0)

    plat = stage_loader.platform(f'background/{current_theme}_platform.png',current_theme,current_stage)
    game_world.add_object(plat,0)

    if nommor.viego == None:
        nommor.viego = Viego()
    game_world.add_object(nommor.viego, 1)
    game_world.set_player(nommor.viego)  # 플레이어로 설정

    # ui 초기화
    if nommor.UI is None:
        nommor.UI = UI.UI()
    game_world.add_object(nommor.UI, 2)

    monsters = [monster.Ghost() for _ in range(10)]
    game_world.add_objects(monsters, 1)


    game_world.add_collision_pair('viego:item', nommor.viego, None)
    game_world.add_collision_pair('viego:monster', nommor.viego, None)
    game_world.add_collision_pair('viego:monster_attack', nommor.viego, None)
    game_world.add_collision_pair('viego:ground', nommor.viego, None)
    game_world.add_collision_pair('viego:tree', nommor.viego, None)

    for t in trees:
        game_world.add_collision_pair('viego:tree', None, t)

    for m in monsters:
        game_world.add_collision_pair('viego:monster', None, m)
        game_world.add_collision_pair('monster:ground', None, m)
        game_world.add_collision_pair('viego_thunder:monster', None, m)

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
    global current_theme, current_stage, soop_back, grass, monsters, viego

    current_theme = theme
    current_stage = stage_num

    # 1. 카메라 맵 크기 업데이트
    map_width, map_height = stage_loader.get_stage_size(theme, stage_num)
    cam.update_map_size(map_width, map_height)

    # 2. 게임 오브젝트 재로드
    game_world.clear()
    game_world.collision_clear()

    # 배경 재로드
    back = stage_loader.Background(f'background/{theme}.png', theme)
    game_world.add_object(back, 0)

    # 플레이어 재로드
    if nommor.viego is None:
        nommor.viego = Viego()
    game_world.add_object(nommor.viego, 1)

    # 0. ui 초기화
    if nommor.UI is None:
        nommor.UI = UI.UI()
    game_world.add_object(nommor.UI, 2)

    if theme == 'snow' and stage_num == 2:
        tree = stage_loader.Tree(f'background/gold_tree.png', current_theme, current_stage, 0)
        game_world.add_object(tree, 0)
    else:
        trees = [stage_loader.Tree(f'background/{current_theme}_tree.png', current_theme, current_stage, i) for i in
                 range(stage_loader.get_tree_count(current_theme, current_stage))]
        game_world.add_objects(trees, 0)

    # 발판 재로드
    plat = stage_loader.platform(f'background/{theme}_platform.png',theme, stage_num)
    game_world.add_object(plat, 0)

    # 몬스터 재로드
    if theme == 'desert':
        monsters = [monster.Yeti() for _ in range(10)]
        game_world.add_objects(monsters, 1)
    elif theme == 'snow':
        monsters = [Bossmonster.Wolf() for _ in range(1)]
        game_world.add_objects(monsters, 1)
    else:
        monsters = [monster.Ghost() for _ in range(10)]
        game_world.add_objects(monsters, 1)

    game_world.add_collision_pair('viego:item', nommor.viego, None)
    game_world.add_collision_pair('viego:monster', nommor.viego, None)
    game_world.add_collision_pair('viego:monster_attack', nommor.viego, None)
    game_world.add_collision_pair('viego:ground', nommor.viego, None)
    game_world.add_collision_pair('viego:tree', nommor.viego, None)

    if theme == 'snow' and stage_num == 2:
        game_world.add_collision_pair('viego:tree', None, tree)
    else:
        for t in trees:
            game_world.add_collision_pair('viego:tree', None, t)


    for m in monsters:
        game_world.add_collision_pair('viego:monster', None, m)
        game_world.add_collision_pair('monster:ground', None, m)
        game_world.add_collision_pair('viego_thunder:monster', None, m)
    pass



