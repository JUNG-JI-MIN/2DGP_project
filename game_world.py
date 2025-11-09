from pico2d import *
world = [[],[],[]]
def add_object(o, layer = 0):
    world[layer].append(o)
def add_objects(ol,layer = 0):
    world[layer] += ol
def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
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

def clear():
    for layer in world:
        layer.clear()