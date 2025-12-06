from pico2d import *
import camera
world = [[],[],[]]
camera_instance = None  # 전역 카메라 인스턴스
player = None  # 플레이어(viego) 참조
def add_object(o, layer = 0):
    world[layer].append(o)
def add_objects(ol,layer = 0):
    world[layer] += ol
def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)
def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return
    raise ValueError("Object not found")

def set_camera(cam):
    global camera_instance
    camera_instance = cam

def set_player(p):
    global player
    player = p

def update():
    if camera_instance and player:
        camera_instance.update(player.x, player.y)

    for layer in world:
        for o in layer:
            o.update()

def render(obj, screen_x, screen_y):
    """카메라 좌표로 자동 변환하여 렌더링"""
    if camera_instance:
        return camera_instance.apply(screen_x, screen_y)
    return screen_x, screen_y

def draw():
    for layer in world:
        for o in layer:
            o.draw()

def collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def attack_collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_attack_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def monster_attack_collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_attack_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def clear():
    for layer in world:
        layer.clear()


def clear_except_player():
    """플레이어를 제외한 모든 오브젝트 제거"""
    global player

    for layer in world:
        # 플레이어가 아닌 객체만 제거
        layer[:] = [obj for obj in layer if obj == player]

    # 충돌 쌍도 플레이어만 남기고 초기화
    for pairs in collision_pairs.values():
        pairs[0][:] = [obj for obj in pairs[0] if obj == player]
        pairs[1][:] = [obj for obj in pairs[1] if obj == player]

    if player:
        player.x = 100
        player.y = 100
        player.frame = 0

collision_pairs = {}
def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[],[]]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)
    return None


def handle_collision():
    for group, pairs in collision_pairs.items():
        for a in pairs[0][:]:  # 복사본
            for b in pairs[1][:]:  # 복사본
                if collide(a,b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

def handle_attack_collision():
    for group, pairs in collision_pairs.items():
        for a in pairs[0][:]:  # 복사본
            for b in pairs[1][:]:  # 복사본
                if attack_collide(a,b):
                    a.handle_attack_collision(group, b)
                    b.handle_attack_collision(group, a)

def handle_monster_attack_collision():
    for group, pairs in collision_pairs.items():
        for a in pairs[0][:]:  # 복사본
            for b in pairs[1][:]:  # 복사본
                if monster_attack_collide(a,b):
                    a.handle_monster_attack_collision(group, b)
                    b.handle_monster_attack_collision(group, a)
