from pico2d import *
from nommor import viego

class UI:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)

    def draw(self, viego):
        # HP 바 그리기
        hp_bar_width = 300
        hp_bar_height = 30
        hp_ratio = viego.HP / viego.max_HP
        hp_bar_current_width = int(hp_bar_width * hp_ratio)

        # HP 바 배경 (검은색)
        draw_rectangle(10, 570, 10 + hp_bar_width, 570 + hp_bar_height)
        # HP 바 현재 상태 (빨간색)
        draw_rectangle(10, 570, 10 + hp_bar_current_width, 570 + hp_bar_height, 255, 0, 0)

        # Stamina 바 그리기
        ste_bar_width = 300
        ste_bar_height = 30
        ste_ratio = viego.STE / viego.max_STE
        ste_bar_current_width = int(ste_bar_width * ste_ratio)

        # Stamina 바 배경 (검은색)
        draw_rectangle(10, 530, 10 + ste_bar_width, 530 + ste_bar_height)
        # Stamina 바 현재 상태 (초록색)
        draw_rectangle(10, 530, 10 + ste_bar_current_width, 530 + ste_bar_height, 0, 255, 0)

        # 레벨 표시
        self.font.draw(10, 500, f'Level: {viego.level}', (255, 255, 255))

        # 아이템 개수 표시
        self.font.draw(10, 470, f'메소: {viego.money}', (255, 255, 255))
