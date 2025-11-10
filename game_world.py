from pico2d import *
world = [[],[],[]]
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
def update():
    for layer in world:
        for o in layer:
            o.update()
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
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a,b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

def handle_attack_collision():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if attack_collide(a,b):
                    a.handle_attack_collision(group, b)
                    b.handle_attack_collision(group, a)

def handle_monster_attack_collision():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if monster_attack_collide(a,b):
                    a.handle_monster_attack_collision(group, b)
                    b.handle_monster_attack_collision(group, a)
