import math
import random

from pico2d import draw_rectangle, load_image, get_time, clamp, load_font, load_wav

import game_framework
import game_world
import object_locate
import server
from behavior_tree import *
from server import rifle_number

PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 30 cm
# BULLET의 속도
BULLET_SPEED_KMPH = 50.0  # Km / Hour
BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)

state_name = [('Idle', 15), ('run_start', 1), ('running', 8), ('run_stop', 6), ('spawn', 22), ('coma_roop', 8), ('coma_end', 6)]
state_arm_name = [('aim', 3), ('ready', 1), ('shoot', 3)]
state_body_name = [('aim', 3), ('ready', 1), ('shoot', 3)]

state_count = {'Idle' : 15, 'run_start' : 1, 'running' : 8,
               'run_stop' : 6, 'spawn' : 22, 'coma_roop' : 8, 'coma_end' : 6,
               'aim' : 3, 'ready' : 1, 'shoot' : 3
               }

rifle_size = {
    'Idle' : [(30, 70), (28, 68), (28, 69), (28, 69), (28, 69),
              (28, 69), (28, 69), (28, 69), (28, 69), (28, 69),
              (28, 69), (25, 67), (26, 68), (26, 68), (26, 68)],
    'run_start' : [(28, 67)],
    'running' : [(27, 65), (35, 68), (39, 68), (33, 65), (25, 65), (35, 68), (39, 69), (40, 66)],
    'run_stop' : [(39, 59), (36, 56), (36, 55), (36, 55), (34, 57), (27, 62)],
    'spawn' : [(128, 128), (100, 65), (100, 69), (100, 69), (100, 58),
               (100, 58), (100, 69), (100, 69), (100, 69), (100, 58),
               (100, 58), (100, 106), (100, 106), (35, 39), (36, 43),
               (36, 40), (36, 37), (36, 40), (36, 55), (34, 57), (27, 62), (26, 68)],
    'coma_roop' : [(36, 55), (36, 55), (36, 55), (36, 55), (36, 55), (36, 55), (36, 55), (36, 55)],
    'coma_end' : [(36, 55), (36, 55), (36, 54), (34, 57), (27, 62), (26, 68)]
}

rifle_body_size = {
    'aim' : [(26, 63), (31, 62), (29, 58)],
    'ready' : [(29, 58)],
    'shoot' : [(29, 60), (29, 60), (29, 61)]
}

rifle_arm_size = {
    'aim' : [(20, 34), (20, 33), (29, 31)],
    'ready' : [(29, 31)],
    'shoot' : [(37, 31), (45, 31), (43, 31)]
}

rifle_shoot_ex = [8, 16, 14]

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

PI = math.pi

class Bullet:
    image = None

    def __init__(self, x, y, aim_radian):
        if Bullet.image == None:
            Bullet.image = load_image("resource/Rifleman/bullet.png")
        self.x, self.y, self.aim_radian = x, y, aim_radian
        game_world.add_collision_pair('character:bullet', server.character, self)

    def draw(self):
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom

        self.image.composite_draw(self.aim_radian, '', self.sx, self.sy + 28, 36, 10)

    def update(self):
        self.x += BULLET_SPEED_PPS * math.cos(self.aim_radian) * game_framework.frame_time
        self.y += BULLET_SPEED_PPS * math.sin(self.aim_radian) * game_framework.frame_time

        if self.x < 50 or self.x > 3950:
            game_world.remove_object(self)
        elif self.y < 70 or self.y > 3450:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 18, self.y + 23, self.x + 18, self.y + 33

    def handle_collision(self, group, other):
        match group:
            case 'character:bullet':
                game_world.remove_object(self)


class Rifle:
    state_images = None
    arm_images = None
    body_images = None

    reload_sound = None
    fire_sound = None
    walk_sound = None
    destroy_sound = None
    font = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.tx, self.ty = 0, y
        self.hp = 30
        self.left_side, self.right_side = 300, 3700
        self.speed = random.randint(15, 30)
        self.frame = 0
        self.dir = 0
        self.aim_radian = 0
        self.resting_time = 0
        self.initial_time = 0
        self.coma_time = 0
        self.walk_time = 0
        self.rifle_land = True
        self.arrival_flag = False
        self.shoot_flag = True
        self.damage_flag = False
        self.coma_flag = False

        self.shooting_range = random.randint(7, 13)

        if Rifle.font == None:
            Rifle.font = load_font('resource/ENCR10B.TTF',32)

        if Rifle.state_images == None:
            Rifle.state_images = {}
            for name, number in state_name:
                Rifle.state_images[name] = [load_image("resource/Rifleman/"+ name +" (%d).png" %(i + 1)) for i in range(number)]
        if Rifle.arm_images == None:
            Rifle.arm_images = {}
            for name, number in state_arm_name:
                Rifle.arm_images[name] = [load_image("resource/Rifleman/" + name + "_arm (%d).png" %(i + 1)) for i in range(number)]
        if Rifle.body_images == None:
            Rifle.body_images = {}
            for name, number in state_body_name:
                Rifle.body_images[name] = [load_image("resource/Rifleman/" + name + "_body (%d).png" %(i + 1)) for i in range(number)]

        self.state = 'spawn'
        self.origin_state = 'spawn'
        self.build_behavior_tree()

        if not Rifle.reload_sound:
            Rifle.reload_sound = load_wav("resource/Rifleman/reload.wav")
            Rifle.reload_sound.set_volume(50)
            Rifle.fire_sound = load_wav("resource/Rifleman/fire.wav")
            Rifle.fire_sound.set_volume(50)
            Rifle.walk_sound = load_wav("resource/Rifleman/walk.wav")
            Rifle.walk_sound.set_volume(50)
            Rifle.destroy_sound = load_wav("resource/Rifleman/destroy.wav")
            Rifle.destroy_sound.set_volume(100)

    def update(self):
        PIXEL_PER_METER = (10.0 / 0.2)

        FALL_SPEED_KMPH = 80
        FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
        FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
        FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)

        GRAVITY = FALL_SPEED_PPS * game_framework.frame_time * -1

        if self.rifle_land == True:
            self.rifle_land = False
            GRAVITY = 0

        self.y += GRAVITY

        self.y = clamp(66.0, self.y, server.map.h - 66.0)

        self.ty = self.y

        if not self.origin_state == self.state:
            self.origin_state = self.state
            self.frame = 0

        FRAMES_PER_ACTION = state_count[self.state]
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        self.bt.run()


    def handle_event(self, event):
        pass

    def draw(self):
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom

        if self.state == 'aim' or self.state == 'ready' or self.state == 'shoot':
            width_body, height_body = rifle_body_size[self.state][int(self.frame)]

            width_arm, height_arm = rifle_arm_size[self.state][int(self.frame)]

            degree = (self.aim_radian * 180) / PI

            if degree < 90 and degree > -90:
                Rifle.body_images[self.state][int(self.frame)].composite_draw(
                    0, '', self.sx, self.sy, width_body * 2, height_body * 2)

                if self.state == 'shoot':
                    ex_x = rifle_shoot_ex[int(self.frame)] * math.cos(self.aim_radian)
                    ex_y = rifle_shoot_ex[int(self.frame)] * math.sin(self.aim_radian)

                    Rifle.arm_images[self.state][int(self.frame)].composite_draw(
                        self.aim_radian, '', self.sx + ex_x, self.sy + height_arm + ex_y, width_arm * 2, height_arm * 2)
                else:
                    Rifle.arm_images[self.state][int(self.frame)].composite_draw(
                        self.aim_radian, '', self.sx, self.sy + height_arm, width_arm * 2, height_arm * 2)
            else:
                Rifle.body_images[self.state][int(self.frame)].composite_draw(
                    0, 'h', self.sx, self.sy, width_body * 2, height_body * 2)

                if self.state == 'shoot':
                    ex_x = rifle_shoot_ex[int(self.frame)] * math.cos(self.aim_radian)
                    ex_y = rifle_shoot_ex[int(self.frame)] * math.sin(self.aim_radian)

                    Rifle.arm_images[self.state][int(self.frame)].composite_draw(
                        self.aim_radian, 'v', self.sx + ex_x, self.sy + height_arm + ex_y, width_arm * 2, height_arm * 2)
                else:
                    Rifle.arm_images[self.state][int(self.frame)].composite_draw(
                        self.aim_radian, 'v', self.sx, self.sy + height_arm, width_arm * 2, height_arm * 2)

            if self.state == 'shoot' and int(self.frame) == 0 and self.shoot_flag == True:
                bullet = Bullet(self.x, self.y, self.aim_radian)
                game_world.add_object(bullet)
                self.shoot_flag = False
        else:
            width, height = rifle_size[self.state][int(self.frame)]
            if math.cos(self.dir) > 0:
                Rifle.state_images[self.state][int(self.frame)].composite_draw(
                    0, '', self.sx, self.sy, width*2, height*2)
            else:
                Rifle.state_images[self.state][int(self.frame)].composite_draw(
                    0, 'h', self.sx, self.sy, width*2, height*2)

        self.font.draw(self.sx - 100, self.sy + 75, f'{self.hp:02d}', (255, 255, 0))

    def get_bb(self):
        if self.state == 'aim' or self.state == 'ready' or self.state == 'shoot':
            width_body, height_body = rifle_body_size[self.state][int(self.frame)]
            return self.x - width_body, self.y - height_body, self.x + width_body, self.y + height_body
        else:
            width, height = rifle_size[self.state][int(self.frame)]
            return self.x - width, self.y - height, self.x + width, self.y + height

    def handle_collision(self, group, other):
        match group:
            case 'rifle:land':
                minX_o, minY_o, maxX_o, maxY_o = other.get_bb()
                minX_r, minY_r, maxX_r, maxY_r = self.get_bb()

                if minY_o < minY_r:
                    self.rifle_land = True
                    gap = maxY_o - minY_r
                    self.y = self.y + gap - 1
                    self.left_side, self.right_side = 300, 3700

            case 'rifle:floor':
                minX_o, minY_o, maxX_o, maxY_o = other.get_bb()
                minX_r, minY_r, maxX_r, maxY_r = self.get_bb()

                self.rifle_land = True
                gap = maxY_o - minY_r
                self.y = self.y + gap - 1
                self.left_side, self.right_side = other.x - 77, other.x + 77

            case 'fist:rifle':
                self.damage_flag = True
                self.coma_time = get_time()
                self.hp -= other.damage
                if self.hp <= 0:
                    object_locate.rifle_amount -= 1
                    if server.rifle_number < object_locate.rifle_amount:
                        server.rifles.append(Rifle(random.randint(300, 3700), random.randint(200, 1300)))
                        game_world.add_object(server.rifles[server.rifle_number], 3)

                        game_world.add_collision_pair('fist:rifle', None, server.rifles[server.rifle_number])
                        game_world.add_collision_pair('rifle:floor', server.rifles[server.rifle_number], None)
                        game_world.add_collision_pair('rifle:land', server.rifles[server.rifle_number], None)

                        server.rifle_number += 1
                    game_world.remove_object(self)

    def set_random_location(self):
        self.arrival_flag = False
        self.tx = random.randint(self.left_side, self.right_side)
        return BehaviorTree.SUCCESS

    def set_target_location(self, x=None):
        if not x :
            raise ValueError('Location should be given')
        self.tx = x
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        # RIFLE의 움직이는 속도
        RUN_SPEED_KMPH = self.speed  # Km / Hour
        RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

        self.dir = math.atan2(ty-self.y, tx-self.x)
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)

        if get_time() - self.walk_time > 0.3:
            self.walk_sound.play()
            self.walk_time = get_time()

    def move_to(self, r=0.5):
        self.state = 'running'
        if not self.origin_state == self.state:
            self.origin_state = self.state
            self.frame = 0
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            self.arrival_flag = True
            return BehaviorTree.SUCCESS
        else:
            self.arrival_flag = False
            return BehaviorTree.RUNNING

    def is_character_nearby(self, distance):
        if self.distance_less_than(server.character.x, server.character.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_ready_to_shoot(self):
        # 현재 라이플의 상태가 ready라면 성공
        if (self.state == 'ready' and self.frame > 0.9) or (self.state == 'shoot' and self.frame < 2.9):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_running(self):
        if self.state == 'run_start' or self.state == 'running' or (self.state == 'run_stop' and self.frame < 5.9):
            return BehaviorTree.SUCCESS
        else:
            self.arrival_flag = False
            return BehaviorTree.FAIL

    def is_stopping(self):
        if not self.state == 'running':
            if self.state == 'run_start' and self.frame > 0.1:
                return BehaviorTree.FAIL
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_resting(self):
        if (self.state == 'Idle' and get_time() - self.initial_time < self.resting_time):
            return BehaviorTree.SUCCESS
        else:
            if self.arrival_flag == True:
                return BehaviorTree.SUCCESS
            return BehaviorTree.FAIL

    def is_spawn(self):
        if not self.state == 'spawn':
            return BehaviorTree.SUCCESS
        else:
            if self.frame > 21.5:
                return BehaviorTree.SUCCESS
            return BehaviorTree.FAIL

    def is_damage(self):
        if self.damage_flag == True:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def rifle_coma_end(self):
        if self.coma_flag == True:
            self.state = 'coma_end'
            if not self.origin_state == self.state:
                self.origin_state = self.state
                self.frame = 0

            if self.frame > 5.8:
                self.coma_flag = False
                return BehaviorTree.SUCCESS
            else:
                return BehaviorTree.RUNNING
        else:
            return BehaviorTree.SUCCESS


    def rifle_coma(self):
        self.state = 'coma_roop'
        if not self.origin_state == self.state:
            self.origin_state = self.state
            self.frame = 0

        if get_time() - self.coma_time > 0.1:
            self.damage_flag = False
            return BehaviorTree.SUCCESS
        else:
            self.coma_flag = True
            return BehaviorTree.RUNNING

    def spawning(self):
        self.state = 'spawn'
        if not self.origin_state == self.state:
            self.origin_state = self.state
            self.frame = 0

        if self.frame > 22.9:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def stop_running(self):
        self.state = 'run_stop'
        if not self.origin_state == self.state:
            self.origin_state = self.state
            self.frame = 0

        if self.frame > 5.9:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def running_start(self):
        self.state = 'run_start'
        if not self.origin_state == self.state:
            self.origin_state = self.state
            self.frame = 0

        if self.frame > 0.1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def resting(self):
        self.state = 'Idle'
        if not self.origin_state == self.state:
            self.origin_state = self.state
            self.frame = 0
            self.initial_time = get_time()
            self.resting_time = random.randint(2, 4)

        if get_time() - self.initial_time > self.resting_time:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def fire_start(self):
        self.state = 'shoot'
        if not self.origin_state == self.state:
            self.fire_sound.play()
            self.origin_state = self.state
            self.frame = 0

        if self.frame > 2.8:
            self.state = 'aim'
            self.shoot_flag = True
            if not self.origin_state == self.state:
                self.origin_state = self.state
                self.frame = 0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def angle_with_the_character(self):
        self.aim_radian = math.atan2(server.character.y - self.y, server.character.x - self.x)

    def take_aim(self):
        self.state = 'aim'
        if not self.origin_state == self.state:
            self.origin_state = self.state
            self.frame = 0
        self.angle_with_the_character()

        if self.frame > 2.9:
            self.reload_sound.play()
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def ready_to_shoot(self):
        self.state = 'ready'

        if not self.origin_state == self.state:
            self.origin_state = self.state
            self.frame = 0

        if self.frame > 0.9:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def chase_character(self, r = 0.5):
        self.state = 'running'
        self.move_slightly_to(server.character.x, self.y)
        if not self.origin_state == self.state:
            self.origin_state = self.state
            self.frame = 0
        if self.distance_less_than(server.character.x, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        c1 = Condition('사격 준비 완료?', self.is_ready_to_shoot)
        a1 = Action('사격 중', self.fire_start)

        shooting = Sequence('사격', c1, a1)

        a2 = Action('조준 중', self.take_aim)
        a3 = Action('사격 준비', self.ready_to_shoot)

        aiming = Sequence('조준', a2, a3)

        shooting_or_aiming = Selector('사격 or 조준', shooting, aiming)

        chasing_stop = Sequence('멈춤', shooting_or_aiming)

        c4 = Condition('추적 중인가?', self.is_running)
        a7 = Action('추적 멈추기', self.stop_running)

        chasing_stopping = Sequence('추적 중 멈추기', c4, a7)

        chasing_or_stop = Selector('추적 중 멈추는 중 or 멈춤', chasing_stopping, chasing_stop)

        c2 = Condition('사격 거리 안인가?', self.is_character_nearby, self.shooting_range)

        within_shooting_range = Sequence('사격 거리 내', c2, chasing_or_stop)

        a4 = Action('추적', self.chase_character)

        outside_shooting_range = Sequence('사격 거리 밖', a4)

        within_or_outside_shooting_range = Selector('사격 거리 내 or 밖', within_shooting_range, outside_shooting_range)

        c3 = Condition('캐릭터가 감지 범위 안인가?', self.is_character_nearby, 30)

        within_detection_range = Sequence('감지 범위 내', c3, within_or_outside_shooting_range)

        a5 = Action('새 위치 가져오기', self.set_random_location)

        c5 = Condition('캐릭터가 멈춰있는가?', self.is_stopping)
        a8 = Action('달릴 준비', self.running_start)

        ready_to_prowl = Sequence('배회 준비', c5, a8)

        a6 = Action('위치로 이동', self.move_to)

        prowling = Sequence('배회 중', a6)

        ready_or_prowling = Selector('준비 or 배회 중', ready_to_prowl, prowling)

        prowl = Sequence('배회', a5, ready_or_prowling)
        
        c7 = Condition('달리는 중인가?', self.is_running)
        a10 = Action('달리기 멈추기', self.stop_running)

        run_stopping = Sequence('달리기 멈추는 중', c7, a10)

        a9 = Action('휴식 중', self.resting)

        resting = Sequence('휴식 중', a9)

        run_stopping_or_resting = Selector('달리기 멈추기 or 휴식 중', run_stopping, resting)

        c6 = Condition('휴식 중인가?', self.is_resting)

        rest = Sequence('휴식', c6, run_stopping_or_resting)

        outside_detection_range = Selector('감지 범위 밖', rest, prowl)

        within_or_outside_detection_range = Selector('감지 범위 내 or 밖', within_detection_range, outside_detection_range)

        c9 = Condition('데미지를 받았는가?', self.is_damage)
        a11 = Action('코마 상태', self.rifle_coma)

        coma = Sequence('데미지 입음', c9, a11)

        a12 = Action('코마 종료', self.rifle_coma_end)

        normal = Sequence('정상 상태', a12, within_or_outside_detection_range)

        coma_or_normal = Selector('코마 상태 or 정상 상태', coma, normal)

        c8 = Condition('스폰 완료되었는가?', self.is_spawn)

        after_spawn = Sequence('스폰 후', c8, coma_or_normal)

        a11 = Action('스폰 중', self.spawning)

        before_spawn = Sequence('스폰 전', a11)

        root = after_or_before_spawn = Selector('스폰 전 or 후', after_spawn, before_spawn)

        self.bt = BehaviorTree(root)