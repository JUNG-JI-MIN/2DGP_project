from pico2d import load_image, get_time, load_font, draw_rectangle
from pyvisalgo.welzl import min_circle_trivial
from sdl2 import SDL_KEYDOWN, SDL_KEYUP

import game_world
import play_mode
from events import space_down, time_out, a_key, a_key_up, s_key_down, s_key_up, right_down, left_down, right_up, \
    left_up, up_down, up_up, z_key_down
from state_machine import StateMachine
import sheet_list
import game_framework
import stage_loader

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm.
WALK_SPEED_KMPH = 10.0 # Km / Hour
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0) # Meter / Minute
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0) # Meter / Second
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER) # 초당 픽셀 이동 거리 (Pixel Per Second)
JUMP_HEIGHT_PSS = WALK_SPEED_PPS * 2 # 점프 높이 (Pixel Per Second Speed)
DASH_SPEED_PSS = WALK_SPEED_PPS * 2 # 대쉬 속도 (Pixel Per Second Speed)

GRAVITY = 1000 / 3  # 중력 가속도 cm / s^2

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3


class thunder:
    image = None
    index = 0
    def __init__(self, viego, direction, x, y, count=1,max_count=5):
        if thunder.image is None:
            thunder.image = load_image('Sprite_Sheets/thunder.png')
        self.viego = viego
        self.frame = 0
        self.dir = direction
        self.max_count = max_count
        self.x, self.y = x, y
        self.count = count
    def update(self):
        if self.frame < 14:
            self.frame = (self.frame + 16 * ACTION_PER_TIME * game_framework.frame_time)
        else:
            if self.count < self.max_count:
                print( f'{self.count=} ,{self.max_count=}')
                T = thunder(self.viego,self.dir, self.x + self.max_count * 60 * self.dir, self.y, self.count +1,self.max_count)
                game_world.add_object(T, 1)
                game_world.add_collision_pair('viego_thunder:monster', T, None)

            game_world.remove_object(self)

    def draw(self):
        f = sheet_list.viego_thunder_attack[int(self.frame)]
        screen_x, screen_y = game_world.render(self.viego, self.x, self.y)
        thunder.image.clip_draw(f[0], 1240 - f[1] - f[3], f[2], f[3], screen_x, screen_y,500,800)
        pass

    def get_bb(self):
        return (self.viego.x - 15,
                self.viego.y - 15,
                self.viego.x + 15,
                self.viego.y + 15)
    def get_attack_bb(self):
        return (self.viego.x - 20,
                self.viego.y - 20,
                self.viego.x + 20,
                self.viego.y + 20)
    def handle_collision(self, group, other):
        pass
    def handle_attack_collision(self, group, other):
        pass
    def handle_monster_attack_collision(self,group, other):
        pass


class guard:
    def __init__(self, viego):
        self.viego = viego

    def enter(self,e):
        self.viego.is_guarding = True
        T = thunder(self.viego, self.viego.face_dir, self.viego.x + self.viego.face_dir * 50, 400, 0,self.viego.int //5 )
        game_world.add_object(T, 1)
        game_world.add_collision_pair('viego_thunder:monster', T, None)
    def exit(self,e):
        self.viego.frame = 0
        self.viego.is_guarding = False
    def do(self):
        pass

    def draw(self):
        f = sheet_list.viego_guard
        screen_x, screen_y = game_world.render(self.viego, self.viego.x, self.viego.y)
        if self.viego.face_dir == 1:
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], screen_x + self.viego.face_dir *5, screen_y)
        else:
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', screen_x -25/2 + f[2]/2+ self.viego.face_dir *5,screen_y -45/2 + f[3]/2,f[2], f[3])
class jump:
    def __init__(self, viego):
        self.viego = viego

    def enter(self, e):
        if up_down(e):
            # 땅에 있을 때만 점프 가능
            if self.viego.on_ground:
                self.viego.velocity_y = self.viego.min_jump_speed
                self.viego.is_jumping = True
                self.viego.is_jump_holding = True
                self.viego.on_ground = False
            elif not self.viego.on_ground and not self.viego.double_jump_used and self.viego.can_double_jump:
                self.viego.velocity_y = self.viego.min_jump_speed
                self.viego.is_jumping = True
                self.viego.is_jump_holding = True
                self.viego.double_jump_used = True  # 더블점프 사용

        # 방향 처리
        if right_down(e):
            self.viego.dir = self.viego.face_dir = 1
        elif left_down(e):
            self.viego.dir = self.viego.face_dir = -1
        elif right_up(e):
            if self.viego.dir == 1:
                self.viego.dir = 0
        elif left_up(e):
            if self.viego.dir == -1:
                self.viego.dir = 0

        if up_up(e):
            self.viego.is_jump_holding = False

    def exit(self, e):
        if up_up(e):
            self.viego.is_jump_holding = False

    def do(self):
        # 점프 키를 누르고 있고 상승 중일 때 추가 가속
        if self.viego.is_jump_holding and self.viego.velocity_y > 0:
            self.viego.velocity_y = min(
                self.viego.velocity_y + self.viego.min_jump_speed * 2 * game_framework.frame_time,
                self.viego.max_jump_speed
            )

        # 착지 시 상태 전환
        if self.viego.on_ground:
            if self.viego.is_dashing:
                self.viego.state_machine.cur_state = self.viego.DASH
            elif self.viego.dir != 0:
                self.viego.state_machine.cur_state = self.viego.WALK
            else:
                self.viego.state_machine.handle_state_event(('TIMEOUT', None))
            return

        # 좌우 이동
        if self.viego.is_dashing:
            self.viego.x += self.viego.dir * DASH_SPEED_PSS * game_framework.frame_time
        elif self.viego.dir != 0:
            self.viego.x += self.viego.dir * WALK_SPEED_PPS * game_framework.frame_time

    def draw(self):
        f = sheet_list.viego_jump
        screen_x, screen_y = game_world.render(self.viego, self.viego.x, self.viego.y)
        if self.viego.face_dir == 1:
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], screen_x, screen_y)
        else:
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h',
                screen_x - 25/2 + f[2]/2, screen_y - 45/2 + f[3]/2, f[2], f[3])
class dash:
    def __init__(self, viego):
        self.viego = viego
    def enter(self,e):
        self.viego.is_dashing = True
        pass
    def exit(self,e):
        pass
    def do(self):
        if self.viego.ste <= 0:
            self.viego.is_dashing = False
            self.viego.state_machine.cur_state = self.viego.WALK
            self.viego.frame = 0
            return
        self.viego.frame =  (self.viego.frame + self.viego.DASH_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.viego.x += self.viego.dir * DASH_SPEED_PSS * game_framework.frame_time
        self.viego.ste -= 10 * game_framework.frame_time

    def draw(self):
        f = sheet_list.viego_dash[int(self.viego.frame)]
        screen_x, screen_y = game_world.render(self.viego, self.viego.x, self.viego.y)
        if self.viego.face_dir == 1:  # right
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], screen_x, screen_y -45/2 + f[3]/2)
        else:  # face_dir == -1: # left
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', screen_x -25/2 + f[2]/2,screen_y -45/2 + f[3]/2,f[2], f[3])
class walk:
    def __init__(self, viego):
        self.viego = viego

    def enter(self,e):
        self.viego.is_dashing = False
        if right_down(e) or left_up(e):
            self.viego.dir = self.viego.face_dir = 1
        elif left_down(e) or right_up(e):
            self.viego.dir = self.viego.face_dir = -1
        pass

    def exit(self,e):
        self.viego.frame = 0
        pass

    def do(self):
        if self.viego.is_dashing:
            self.viego.state_machine.cur_state = self.viego.DASH
            return
        self.viego.frame=(self.viego.frame + self.viego.WALK_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.viego.x += self.viego.dir * WALK_SPEED_PPS * game_framework.frame_time
        pass

    def draw(self):
        f = sheet_list.viego_walk[min(int(self.viego.frame),4)]
        screen_x, screen_y = game_world.render(self.viego, self.viego.x, self.viego.y)
        if self.viego.face_dir == 1:  # right
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], screen_x -25/2 + f[2]/2,screen_y  -45/2 + f[3]/2)
        else:  # face_dir == -1: # left
            self.viego.img.clip_composite_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h',screen_x, screen_y,f[2],f[3])
class Sleep:
    def __init__(self, viego):
        self.viego = viego

    def enter(self,e):
        self.frame = 0
        self.viego.dir = 0
        self.viego.face_dir = 0

    def exit(self,e):
        self.viego.frame = 0

    def do(self):
        self.viego.ste += 5 * game_framework.frame_time
        if self.viego.ste > self.viego.max_STE:
            self.viego.ste = self.viego.max_STE
        if (self.viego.frame < 6):
            self.viego.frame = (self.viego.frame + self.viego.SLEEP_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

    def draw(self):
        f = sheet_list.viego_sleep[int(self.viego.frame)]
        screen_x, screen_y = game_world.render(self.viego, self.viego.x, self.viego.y)
        self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], screen_x -25/2 + f[2]/2,screen_y -45/2 + f[3]/2)
class attack:
    def __init__(self, viego):
        self.viego = viego
        self.count = 0
        self.attack_timer = 0
        self.combo_time_limit = 1.0  # 콤보 타임 제한 (초)


    def enter(self,e):
        # 이전 공격에서 1.0초 이내에 다시 공격하면 콤보 증가
        self.viego.ste -= 10
        self.viego.attack_hit_done = False
        self.viego.is_attacking = True
        self.viego.frame = 0

        if get_time() - self.attack_timer < self.combo_time_limit:
            self.count = (self.count + 1) % 5  # 0~4 순환
        else:
            self.count = 0  # 시간이 지나면 첫 번째 공격으로

        self.viego.x += self.viego.face_dir  * 20

    def exit(self,e):
        self.viego.is_attacking = False
        self.attack_timer = get_time()
        pass

    def do(self):
        acombo = (6, 6, 5, 9, 7)  # 각 공격 모션의 프레임 수
        if int(self.viego.frame) < acombo[self.count]:
            self.viego.frame = (self.viego.frame + self.viego.ATTACK_FRAME_PER_ACTION * self.viego.ATTACK_SPEED * game_framework.frame_time)
        else:
            self.viego.state_machine.handle_state_event(('TIMEOUT', None))


    def draw(self):
        acombo = (6, 6, 5, 9, 7)
        index = min(int(self.viego.frame), acombo[self.count] - 1)
        # 공격 범위를 카메라 좌표로 변환
        left, bottom, right, top = self.viego.get_attack_bb()
        screen_x, screen_y = game_world.render(self.viego, self.viego.x, self.viego.y)
        offset_x = screen_x - self.viego.x
        offset_y = screen_y - self.viego.y
        draw_rectangle(
            left + offset_x,
            bottom + offset_y,
            right + offset_x,
            top + offset_y,
            0,0,255
        )
        f = sheet_list.viego_attack[self.count][index]

        if self.viego.face_dir == 1:  # right
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], screen_x -25/2 + f[2]/2,screen_y -45/2 + f[3]/2)
        else:  # face_dir == -1: # left
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', screen_x, screen_y -45/2 + f[3]/2, f[2], f[3])
class Idle:
    def __init__(self, viego):
        self.viego = viego

    def enter(self,e):
        self.viego.is_dashing = False
        self.viego.dir = 0
        self.viego.frame = 0
        self.viego.wait_start_time = get_time()

    def exit(self,e):
        self.viego.frame = 0
        pass

    def do(self):
        self.viego.frame=(self.viego.frame + self.viego.IDLE_FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        if get_time() - self.viego.wait_start_time > 2.0:
            # 2초 대기 후 자동으로 Sleep 상태로 전이
            self.viego.state_machine.handle_state_event(('TIMEOUT', None))
        pass

    def draw(self):
        f = sheet_list.viego_idle[int(self.viego.frame)]
        screen_x, screen_y = game_world.render(self.viego, self.viego.x, self.viego.y)
        if self.viego.face_dir == 1:  # right
            self.viego.img.clip_draw(f[0], 1545 - f[1] - f[3], f[2], f[3], screen_x, screen_y)
        else:  # face_dir == -1: # left
            self.viego.img.clip_composite_draw(
                f[0], 1545 - f[1] - f[3], f[2], f[3], 0, 'h', screen_x -25/2 + f[2]/2,screen_y -45/2 + f[3]/2,f[2], f[3])

    pass

class Viego:
    img = None

    def __init__(self):
        self.attack_range = ((50, 45), (50, 45), (50, 45), (50, 45), (50, 45))
        if Viego.img is None:
            Viego.img = load_image('Sprite_Sheets/main_character.png')
        # 스텟
        self.HP = 500
        self.max_HP = 500
        self.ste = 100
        self.max_STE = 100
        self.money = 0

        self.str = 10
        self.int = 10
        self.dex = 10
        self.level = 1
        self.cur_exp = 0
        self.need_to_level_up_exp = 100 # 1레벨 기준

        # 아이템
        self.ghost_item = 0
        self.yeti_item = 0
        self.wolf_item = 0
        self.forest_tree_item = 0
        self.deser_tree_item = 0
        self.snow_tree_item = 0

        # 각 프레임 별 속도 설정
        self.IDLE_FRAME_PER_ACTION  = 3
        self.SLEEP_FRAME_PER_ACTION = 7
        self.WALK_FRAME_PER_ACTION = 5
        self.DASH_FRAME_PER_ACTION = 6
        self.JUMP_FRAME_PER_ACTION = 2
        self.ATTACK_FRAME_PER_ACTION = 5
        self.ATTACK_SPEED = 0.25 * self.dex

        self.font = load_font('ENCR10B.TTF', 16)
        self.x, self.y = 400, 50
        self.dir = 0
        self.frame = 0
        self.face_dir = 1

        # 물리 관련 추가
        self.velocity_y = 0  # y축 속도
        self.gravity = -800  # 중력 가속도 (음수: 아래로)
        self.on_ground = False  # 땅에 있는지 여부

        # 점프 관련
        self.min_jump_speed = JUMP_HEIGHT_PSS * 1.5
        self.max_jump_speed = JUMP_HEIGHT_PSS * 3
        self.is_jump_holding = False
        self.double_jump_used = False

        # 상태 플러그
        self.is_dashing = False
        self.is_guarding = False
        self.is_jumping = False
        self.is_attacking = False
        self.attack_hit_done = False
        self.can_double_jump = False
        self.mujuck_frame = 0
        self.MUJUCK_TIME = 1  # 무적 지속 시간(초)

        # 상태 머신 및 상태들
        self.IDLE = Idle(self)
        self.WALK = walk(self)
        self.DASH = dash(self)
        self.SLEEP = Sleep(self)
        self.GUARD = guard(self)
        self.JUMP = jump(self)
        self.ATTACK = attack(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.SLEEP: {space_down: self.IDLE, right_down: self.WALK, left_down: self.WALK},
                self.IDLE: {time_out: self.SLEEP, right_down: self.WALK, left_down: self.WALK, right_up: self.WALK, left_up: self.WALK, s_key_down: self.GUARD, up_down : self.JUMP,z_key_down : self.ATTACK},
                self.WALK: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE, a_key: self.DASH, s_key_down: self.GUARD, up_down : self.JUMP,z_key_down : self.ATTACK},
                self.DASH: {a_key_up: self.WALK, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE, s_key_down: self.GUARD, up_down : self.JUMP,z_key_down : self.ATTACK},
                self.GUARD: {s_key_up: self.IDLE,z_key_down : self.ATTACK},
                self.JUMP: {time_out: self.IDLE,left_down : self.JUMP, right_down : self.JUMP, right_up: self.JUMP, left_up: self.JUMP,up_up : self.JUMP, up_down: self.JUMP},
                self.ATTACK: {time_out : self.IDLE,s_key_down: self.GUARD}
            }
        )
    def get_attack_bb(self):
        if self.face_dir == 1:
            return (
                self.x + (30 * self.face_dir) - self.attack_range[self.ATTACK.count][0] / 2 + 10,
                self.y - self.attack_range[self.ATTACK.count][1] / 2,
                self.x + (30 * self.face_dir) + self.attack_range[self.ATTACK.count][0] / 2 + 10,
                self.y + self.attack_range[self.ATTACK.count][1] / 2
            )
        return (
            self.x + (30 * self.face_dir) - self.attack_range[self.ATTACK.count][0] / 2,
            self.y - self.attack_range[self.ATTACK.count][1] / 2,
            self.x + (30 * self.face_dir) + self.attack_range[self.ATTACK.count][0] / 2,
            self.y + self.attack_range[self.ATTACK.count][1] / 2
        )

    def update(self):
        self.state_machine.update()  # 상태 머신 업데이트
        self.re_ste() #스테미나 회복
        self.gravity_()   #중력 처리
        self.stage_change() # 스테이지 전환 처리
        self.mujeck_running() # 무적 시간 처리
        self.exp_update() # 경험치 처리

    def exp_update(self):
        if self.cur_exp >= self.need_to_level_up_exp:
            self.level += 1
            self.cur_exp -= self.need_to_level_up_exp
            self.need_to_level_up_exp += 300
            self.max_HP += 50
            self.max_STE += 50
            self.HP = self.max_HP
            self.str += 5
            self.int += 5
            self.dex += 5
            self.ATTACK_SPEED = 0.25 * self.dex

    def re_ste(self):
        # 스태미나 회복
        if self.ste < self.max_STE:
            if self.is_attacking or self.is_dashing or self.is_guarding:
                pass
            else:
                self.ste += 5 * game_framework.frame_time
                if self.ste > self.max_STE:
                    self.ste = self.max_STE
    def gravity_(self):
        if not self.on_ground:
            self.velocity_y += self.gravity * game_framework.frame_time
            self.y += self.velocity_y * game_framework.frame_time

        # 플랫폼 충돌 처리
        self.check_platform_collision()

        if play_mode.current_theme == 'village' and self.y <= 50:
            self.y = 50
            self.velocity_y = 0
            self.on_ground = True
            self.double_jump_used = False
            self.is_jumping = False
    def stage_change(self):
        # 스테이지 전환

        if self.x >= stage_loader.get_stage_size(play_mode.current_theme, play_mode.current_stage)[0]:
            self.x = 50
            self.y = 100
            next_theme = stage_loader.get_next_theme(play_mode.current_theme)
            if play_mode.current_stage == stage_loader.get_max_stages(play_mode.current_theme):
                play_mode.change_stage(next_theme, 1)
            else:
                play_mode.change_stage(play_mode.current_theme, play_mode.current_stage + 1)
        elif self.x < 0:
            self.y = 100
            prev_theme = stage_loader.get_back_theme(play_mode.current_theme)
            if play_mode.current_stage == 1:
                # 이전 테마의 마지막 스테이지로
                prev_stage = stage_loader.get_max_stages(prev_theme)
                play_mode.change_stage(prev_theme, prev_stage)
            else:
                # 같은 테마의 이전 스테이지로
                play_mode.change_stage(play_mode.current_theme, play_mode.current_stage - 1)
            self.x = stage_loader.get_stage_size(play_mode.current_theme, play_mode.current_stage)[0] - 50

    def mujeck_running(self):
        if self.mujuck_frame > 0.0:
            self.mujuck_frame -= game_framework.frame_time
            if self.mujuck_frame <= 0.0:
                self.mujuck_frame = 0.0

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == 122:  # z 키
            if self.ste <= 10:
                return

        if event.type == SDL_KEYDOWN and event.key == 97:
            self.is_dashing = True
        elif event.type == SDL_KEYUP and event.key == 97:
            self.is_dashing = False

        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def get_foot_y(self):
        return self.y - 22

    def get_bb(self):
        # 바운딩 박스 (left, bottom, right, top)
        return (self.x - 10,
                self.y - 22,
                self.x + 20,
                self.y + 22)

    def check_platform_collision(self):
        """플랫폼 좌표 리스트를 직접 가져와 충돌 체크"""
        # stage_loader에서 현재 스테이지의 플랫폼 좌표 가져오기
        platforms = stage_loader.get_stage_platform(
            play_mode.current_theme,
            play_mode.current_stage
        )

        viego_left, viego_bottom, viego_right, viego_top = self.get_bb()
        foot_y = self.get_foot_y()

        self.on_ground = False

        for plat_x, plat_y, plat_w, plat_h in platforms:
            plat_left = plat_x - plat_w // 2
            plat_bottom = plat_y - plat_h // 2
            plat_right = plat_x + plat_w // 2
            plat_top = plat_y + plat_h // 2

            # 충돌 체크
            if (viego_right > plat_left and viego_left < plat_right and
                    viego_bottom < plat_top and viego_top > plat_bottom):

                # 위에서 떨어지는 경우만 처리
                if self.velocity_y <= 0 and (foot_y <= plat_top + 22 or foot_y >= plat_top):
                    self.y = plat_top + 10  # 발 위치 조정
                    self.velocity_y = 0
                    self.on_ground = True
                    self.double_jump_used = False
                    self.is_jumping = False
                    return

        # 어떤 플랫폼과도 충돌하지 않으면
        if self.on_ground:
            self.on_ground = False

    def handle_collision(self, group, other): # 몸통 충돌 처리


        if group == 'viego:monster':
            if self.mujuck_frame > 0.0:
                return

            if self.is_guarding:
                self.ste -= 5
                self.x -= 5 * self.face_dir
                if self.ste < 0:
                    self.ste = 0
                self.mujuck_frame = self.MUJUCK_TIME
                return

            # 무적이 아니면 데미지 적용 후 무적 시작
            self.HP -= other.int * 0.1
            if self.HP < 0:
                self.HP = 0
            self.mujuck_frame = self.MUJUCK_TIME

    def handle_attack_collision(self,group, other): # 내 공격이 상대에게 충돌처리
        if group == 'viego:monster':
            pass
    def handle_monster_attack_collision(self,group, other): # 상대 공격이 내게 충돌처리
        if group == 'viego:ghost_attack':
            if self.is_guarding and self.mujuck_frame <= 0.0:
                self.x -= 5 * self.face_dir
        if group == 'viego:yeti_attack':
            if self.is_guarding and self.mujuck_frame <= 0.0:
                self.x -= 5 * self.face_dir
        if group == 'viego:wolf_attack':
            if self.is_guarding and self.mujuck_frame <= 0.0:
                self.x -= 5 * self.face_dir

    def draw(self):
        self.state_machine.draw()

        # 바운딩 박스도 카메라 좌표로
        left, bottom, right, top = self.get_bb()
        screen_x, screen_y = game_world.render(self, self.x, self.y)
        offset_x = screen_x - self.x
        offset_y = screen_y - self.y
        draw_rectangle(left + offset_x, bottom + offset_y, right + offset_x, top + offset_y)
        self.font.draw(screen_x - 70, screen_y + 30, f'(HP : {self.HP:.2f},SP : {self.ste:.2f},CANJUMP : {self.on_ground})', (255, 255, 0))
