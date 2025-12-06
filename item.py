import pico2d
import game_world


class Item:
    image = None

    def __init__(self, x, y,type):
        if Item.image is None:
            Item.image = pico2d.load_image(f'monster/{type}_item.png')
        self.x = x
        self.y = y
        self.width = Item.image.w
        self.height = Item.image.h

    def get_bb(self):
        return (self.x - self.width // 2, self.y - self.height // 2,
                self.x + self.width // 2, self.y + self.height // 2)
    def get_attack_bb(self):
        return (self.x - 10,
                self.y - 22,
                self.x + 20,
                self.y + 22)
    def update(self):
        pass
    # 의미 없음
    def draw(self):
        screen_x, screen_y = game_world.render(self, self.x, self.y)
        Item.image.draw(screen_x, screen_y)

    def handle_collision(self, group, other):
        if group == "viego:item":
            for a in game_world.collision_pairs['viego:item'][1]:
                if a == self:
                    game_world.collision_pairs['viego:monster'][1].remove(a)
            pass


    def handle_attack_collision(self,group, other):
        pass
    def handle_monster_attack_collision(self,group, other):
        pass