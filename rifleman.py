import math
import random

from pico2d import draw_rectangle, load_image, get_time, clamp

import game_framework
import server
from behavior_tree import *

PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 15.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

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

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

PI = math.pi

class Rifle:
    state_images = None
    arm_images = None
    body_images = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.tx, self.ty = 0, y
        self.frame = 0
        self.dir = 0
        self.aim_radian = 0
        self.waiting_time = 0
        self.resting_time = 0
        self.initial_time = 0
        self.rifle_land = True
        self.arrival_flag = False

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

        if self.frame > state_count[self.state]:
            self.frame = 0

        if self.state == 'aim' or self.state == 'ready' or self.state == 'shoot':
            width_body, height_body = rifle_body_size[self.state][int(self.frame)]

            width_arm, height_arm = rifle_arm_size[self.state][int(self.frame)]

            degree = (self.aim_radian * 180) / PI

            if degree < 90 and degree > -90:
                Rifle.body_images[self.state][int(self.frame)].composite_draw(
                    0, '', self.sx, self.sy, width_body * 2, height_body * 2)

                Rifle.arm_images[self.state][int(self.frame)].composite_draw(
                self.aim_radian, '', self.sx, self.sy + height_arm, width_arm * 2, height_arm * 2)
            else:
                Rifle.body_images[self.state][int(self.frame)].composite_draw(
                    0, 'h', self.sx, self.sy, width_body * 2, height_body * 2)

                Rifle.arm_images[self.state][int(self.frame)].composite_draw(
                    self.aim_radian, 'v', self.sx, self.sy + height_arm, width_arm * 2, height_arm * 2)
        else:
            width, height = rifle_size[self.state][int(self.frame)]
            if math.cos(self.dir) > 0:
                Rifle.state_images[self.state][int(self.frame)].composite_draw(
                    0, '', self.sx, self.sy, width*2, height*2)
                draw_rectangle(self.sx - width, self.sy - height, self.sx + width, self.sy + height)
            else:
                Rifle.state_images[self.state][int(self.frame)].composite_draw(
                    0, 'h', self.sx, self.sy, width*2, height*2)
                draw_rectangle(self.sx - width, self.sy - height, self.sx + width, self.sy + height)

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

    def set_random_location(self):
        self.arrival_flag = False
        self.tx = random.randint(300, 3700)
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
        self.dir = math.atan2(ty-self.y, tx-self.x)
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)

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
        if self.state == 'ready':
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
            self.resting_time = random.randint(3, 6)

        if get_time() - self.initial_time > self.resting_time:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def fire_start(self):
        self.state = 'shoot'
        if not self.origin_state == self.state:
            self.origin_state = self.state
            self.frame = 0
        if self.frame > 2:
            self.state = 'aim'
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
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def ready_to_shoot(self):
        self.state = 'ready'
        if not self.origin_state == self.state:
            self.origin_state = self.state
            self.frame = 0
        if self.waiting_time == 0:
            self.waiting_time = get_time()

        if get_time() - self.waiting_time > 1:
            self.waiting_time = 0
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

        c2 = Condition('사격 거리 안인가?', self.is_character_nearby, 10)

        within_shooting_range = Sequence('사격 거리 내', c2, chasing_or_stop)

        a4 = Action('추적', self.chase_character)

        outside_shooting_range = Sequence('사격 거리 밖', a4)

        within_or_outside_shooting_range = Selector('사격 거리 내 or 밖', within_shooting_range, outside_shooting_range)

        c3 = Condition('캐릭터가 감지 범위 안인가?', self.is_character_nearby, 20)

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

        root = within_or_outside_detection_range = Selector('감지 범위 내 or 밖', within_detection_range, outside_detection_range)

        self.bt = BehaviorTree(root)