from pico2d import *
import quest_center
import nommor

class UI:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)
        self.item_chang = False
        self.status_chang = False
        self.armor_chang = False
        self.quest_chang = False
        self.quest_tab = 'available'

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
        self.font.draw(10, 480, f'exp: {nommor.viego.cur_exp} / {nommor.viego.max_HP}', (0, 0, 0))

        # 상태창 (체력창 바로 밑)
        if self.status_chang:
            self.draw_status_window()

        # 아이템창 (화면 오른쪽)
        if self.item_chang:
            self.draw_item_window()

        # 장비창 (화면 중앙)
        if self.armor_chang:
            self.draw_armor_window()
        # 퀘스트창 (화면 왼쪽 아래)
        if self.quest_chang:
            self.draw_quest_window()

    def draw_status_window(self):
        """상태창 - HP/Stamina 바 아래"""
        # 배경
        draw_rectangle(10, 350, 310, 490, 40, 40, 40, 1, True)
        # 테두리
        draw_rectangle(10, 350, 310, 490, 200, 200, 200)

        # 제목
        self.font.draw(15, 470, 'Status', (255, 255, 0))

        # 스탯 정보
        self.font.draw(15, 445, f'STR: {nommor.viego.str}', (255, 255, 255))
        self.font.draw(250,445, f'{300 + nommor.viego.str*150}', (255, 255, 255))

        self.font.draw(15, 420, f'INT: {nommor.viego.int}', (255, 255, 255))
        self.font.draw(250, 420, f'{300 + nommor.viego.int * 150}', (255, 255, 255))

        self.font.draw(15, 395, f'DEX: {nommor.viego.dex}', (255, 255, 255))
        self.font.draw(250, 395, f'{300 + nommor.viego.dex * 150}', (255, 255, 255))

        self.font.draw(15, 370, f'Money: {nommor.viego.money}', (255, 255, 0))

    def draw_item_window(self):
        """아이템창 - 화면 오른쪽"""
        # 배경 (800 - 310 = 490부터 시작)
        draw_rectangle(490, 350, 790, 590, 40, 40, 40, 1, True)
        # 테두리
        draw_rectangle(490, 350, 790, 590, 200, 200, 200)

        # 제목
        self.font.draw(495, 570, 'Items', (255, 255, 0))

        # 아이템 목록
        self.font.draw(495, 540, f'Ghost Items: {nommor.viego.ghost_item}', (150, 150, 255))
        self.font.draw(495, 510, f'Yeti Items: {nommor.viego.yeti_item}', (150, 200, 255))
        self.font.draw(495, 480, f'Wolf Items: {nommor.viego.wolf_item}', (200, 150, 255))
        self.font.draw(495, 450, f'forest Items: {nommor.viego.forest_tree_item}', (150, 150, 255))
        self.font.draw(495, 420, f'snow Items: {nommor.viego.snow_tree_item}', (150, 200, 255))
        self.font.draw(495, 390, f'desert Items: {nommor.viego.desert_tree_item}', (200, 150, 255))
        self.font.draw(495, 360, f'gold Items: {nommor.viego.gold_tree_item}', (200, 150, 255))

    def draw_armor_window(self):
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
            level = getattr(nommor.viego, f"{slot}_level", 0)
            # 슬롯 배경
            draw_rectangle(260, y_offset - 25, 540, y_offset, 60, 60, 60, 1, True)
            draw_rectangle(260, y_offset - 25, 540, y_offset, 150, 150, 150)
            label = f"{slot}: 0" if level == 0 else f"{slot}: Lv{level}"
            self.font.draw(270, y_offset - 15, label, (200, 200, 200))
            y_offset -= 50

    def draw_quest_window(self):
        # 배경 (화면 오른쪽: 490~790, 중간 높이: 50~550)
        draw_rectangle(490, 50, 790, 550, 40, 40, 40, 1, True)
        # 테두리
        draw_rectangle(490, 50, 790, 550, 200, 200, 200)

        # 탭 버튼 (상단에 배치)
        self.draw_tab_button(490, 545, 'available', self.quest_tab == 'available')
        self.draw_tab_button(590, 545, 'active', self.quest_tab == 'active')
        self.draw_tab_button(690, 545, 'completed', self.quest_tab == 'completed')

        # 퀘스트 목록 (탭 아래)
        if self.quest_tab == 'available':
            self.draw_available_quests()
        elif self.quest_tab == 'active':
            self.draw_active_quests()
        elif self.quest_tab == 'completed':
            self.draw_completed_quests()

    def draw_available_quests(self):
        """받을 수 있는 퀘스트"""
        y = 500  # 탭 아래부터 시작
        for qid in quest_center.player_quest['available']:
            quest = quest_center.quest_list[qid]
            self.font.draw(500, y, quest['name'], (200, 200, 200))
            self.font.draw(500, y - 20, quest['description'], (150, 150, 150))
            y -= 60

    def draw_active_quests(self):
        """진행 중인 퀘스트 (진행도 바 표시)"""
        y = 500
        for qid, current in quest_center.player_quest['active'].items():
            quest = quest_center.quest_list[qid]
            required = quest['objective']['count']

            # 퀘스트 이름
            self.font.draw(500, y, quest['name'], (255, 200, 100))

            # 진행도: 3/5
            progress = f"{current}/{required}"
            self.font.draw(500, y - 20, progress, (255, 255, 255))

            # 진행도 바 (250px 기준)
            bar_width = int(250 * (current / required))
            draw_rectangle(500, y - 35, 500 + bar_width, y - 30, 0, 255, 0, 1, True)  # 채워진 부분
            draw_rectangle(500, y - 35, 750, y - 30, 200, 200, 200)  # 외곽선

            y -= 70

    def draw_completed_quests(self):
        """완료한 퀘스트"""
        y = 500
        for qid in quest_center.player_quest['completed']:
            quest = quest_center.quest_list[qid]
            self.font.draw(500, y, f"✓ {quest['name']}", (0, 255, 0))
            y -= 40

    def draw_tab_button(self, x, y, label, selected):
        """탭 버튼 (선택 시 하이라이트)"""
        # 배경색 (선택 시 밝게)
        bg_color = (80, 80, 80) if selected else (40, 40, 40)
        draw_rectangle(x, y - 30, x + 90, y, bg_color[0], bg_color[1], bg_color[2], 1, True)

        # 테두리
        color = (255, 255, 0) if selected else (150, 150, 150)
        draw_rectangle(x, y - 30, x + 90, y, color[0], color[1], color[2])

        # 텍스트
        self.font.draw(x + 10, y - 20, label, color)

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
