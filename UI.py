from pico2d import *
import nommor

class UI:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)
        self.item_chang = False
        self.status_chang = False
        self.armor_chang = False

    def update(self):
        pass

    def draw(self):
        # HP 바 그리기
        hp_bar_width = 300
        hp_bar_height = 30
        hp_ratio = nommor.viego.HP / nommor.viego.max_HP
        hp_bar_current_width = int(hp_bar_width * hp_ratio)

        # HP 바 배경 (검은색)
        draw_rectangle(10, 570, 10 + hp_bar_width, 570 + hp_bar_height,0, 0, 0, 255, True)
        # HP 바 현재 상태 (빨간색)
        draw_rectangle(10, 570, 10 + hp_bar_current_width, 570 + hp_bar_height, 255, 0, 0, 255, True)

        # Stamina 바 그리기
        ste_bar_width = 300
        ste_bar_height = 30
        ste_ratio = nommor.viego.ste / nommor.viego.max_STE
        ste_bar_current_width = int(ste_bar_width * ste_ratio)

        # Stamina 바 배경 (검은색)
        draw_rectangle(10, 530, 10 + ste_bar_width, 530 + ste_bar_height,0, 0, 0, 255, True)
        # Stamina 바 현재 상태 (초록색)
        draw_rectangle(10, 530, 10 + ste_bar_current_width, 530 + ste_bar_height, 0, 255, 0, 255, True)

        # 레벨 표시
        self.font.draw(10, 500, f'Level: {nommor.viego.level}', (0, 0, 0))

        # 아이템 개수 표시
        self.font.draw(10, 470, f'meso: {nommor.viego.money}', (0, 0, 0))

        # 상태창 (체력창 바로 밑)
        if self.status_chang:
            self.draw_status_window(nommor.viego)

        # 아이템창 (화면 오른쪽)
        if self.item_chang:
            self.draw_item_window(nommor.viego)

        # 장비창 (화면 중앙)
        if self.armor_chang:
            self.draw_armor_window(nommor.viego)
    def draw_status_window(self, viego):
        """상태창 - HP/Stamina 바 아래"""
        # 배경
        draw_rectangle(10, 350, 310, 490, 40, 40, 40, 1, True)
        # 테두리
        draw_rectangle(10, 350, 310, 490, 200, 200, 200)

        # 제목
        self.font.draw(15, 470, 'Status', (255, 255, 0))

        # 스탯 정보
        self.font.draw(15, 445, f'STR: {viego.str}', (255, 255, 255))
        self.font.draw(15, 420, f'INT: {viego.int}', (255, 255, 255))
        self.font.draw(15, 395, f'DEX: {viego.dex}', (255, 255, 255))
        self.font.draw(15, 370, f'Money: {viego.money}', (255, 255, 0))

    def draw_item_window(self, viego):
        """아이템창 - 화면 오른쪽"""
        # 배경 (800 - 310 = 490부터 시작)
        draw_rectangle(490, 350, 790, 590, 40, 40, 40, 1, True)
        # 테두리
        draw_rectangle(490, 350, 790, 590, 200, 200, 200)

        # 제목
        self.font.draw(495, 570, 'Items', (255, 255, 0))

        # 아이템 목록
        self.font.draw(495, 540, f'Ghost Items: {viego.ghost_item}', (150, 150, 255))
        self.font.draw(495, 510, f'Yeti Items: {viego.yeti_item}', (150, 200, 255))
        self.font.draw(495, 480, f'Wolf Items: {viego.wolf_item}', (200, 150, 255))
        self.font.draw(495, 450, f'forest Items: {viego.forest_tree_item}', (150, 150, 255))
        self.font.draw(495, 420, f'snow Items: {viego.snow_tree_item}', (150, 200, 255))
        self.font.draw(495, 390, f'desert Items: {viego.deser_tree_item}', (200, 150, 255))

        # 퀘스트 정보
        self.font.draw(660, 570, 'Quests:', (255, 200, 100))
        y_offset = 410
        for quest_id, (monster, count) in viego.quest.items():
            self.font.draw(495, y_offset, f'Quest {quest_id}: {monster} ({count})', (200, 200, 200))
            y_offset -= 25

    def draw_armor_window(self, viego):
        """장비창 - 화면 중앙"""
        # 배경 (400 - 150 = 250부터 시작)
        draw_rectangle(250, 250, 550, 550, 40, 40, 40, 1, True)
        # 테두리
        draw_rectangle(250, 250, 550, 550, 200, 200, 200)

        # 제목
        self.font.draw(255, 530, 'Equipment', (255, 255, 0))

        # 장비 슬롯 (예시)
        slot_names = ['Weapon', 'Helmet', 'Armor', 'Boots', 'Accessory']
        y_offset = 490
        for slot in slot_names:
            # 슬롯 배경
            draw_rectangle(260, y_offset - 25, 540, y_offset, 60, 60, 60, 1, True)
            draw_rectangle(260, y_offset - 25, 540, y_offset, 150, 150, 150)
            self.font.draw(270, y_offset - 15, f'{slot}: Empty', (200, 200, 200))
            y_offset -= 50

        # 닫기 안내
        self.font.draw(255, 270, 'Press E to close', (150, 150, 150))

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

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN :
            pass
        elif event.type == SDL_KEYUP:
            pass
