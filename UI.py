from pico2d import *
import nommor

class UI:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        pass

    def draw(self):
        # HP 바 그리기
        hp_bar_width = 300
        hp_bar_height = 30
        hp_ratio = nommor.viego.HP / nommor.viego.max_HP
        hp_bar_current_width = int(hp_bar_width * hp_ratio)

        # HP 바 배경 (검은색)
        draw_rectangle(10, 570, 10 + hp_bar_width, 570 + hp_bar_height)
        # HP 바 현재 상태 (빨간색)
        draw_rectangle(10, 570, 10 + hp_bar_current_width, 570 + hp_bar_height, 255, 0, 0)

        # Stamina 바 그리기
        ste_bar_width = 300
        ste_bar_height = 30
        ste_ratio = nommor.viego.ste / nommor.viego.max_STE
        ste_bar_current_width = int(ste_bar_width * ste_ratio)

        # Stamina 바 배경 (검은색)
        draw_rectangle(10, 530, 10 + ste_bar_width, 530 + ste_bar_height)
        # Stamina 바 현재 상태 (초록색)
        draw_rectangle(10, 530, 10 + ste_bar_current_width, 530 + ste_bar_height, 0, 255, 0)

        # 레벨 표시
        self.font.draw(10, 500, f'Level: {nommor.viego.level}', (0, 0, 0))

        # 아이템 개수 표시
        self.font.draw(10, 470, f'meso: {nommor.viego.money}', (0, 0, 0))

    def get_bb(self):
        return (0, 0, 0, 0)  # UI는 충돌 박스가 없음
    def get_attack_bb(self):
        return (0, 0, 0, 0)  # UI는 공격 충돌 박스가 없음
    def handle_collision(self, group, other):
        pass
    def handle_attack_collision(self,group, other):
        pass
    def handle_monster_attack_collision(self,group, other):
        pass
