import math

from pico2d import draw_rectangle, load_image

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

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Rifle:
    state_images = None
    arm_images = None
    body_images = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.dir = 0

        if Rifle.state_images == None:
            Rifle.state_images = {}
            for name, number in state_name:
                Rifle.state_images[name] = [load_image("resource/Rifleman/"+ name +" (%d).png" %(i + 1)) for i in range(number)]
        if Rifle.arm_images == None:
            Rifle.arm_images = {}
            for name, number in state_arm_name:
                Rifle.state_images[name] = [load_image("resource/Rifleman/" + name + "_arm (%d).png" %(i + 1)) for i in range(number)]
        if Rifle.body_images == None:
            Rifle.body_images = {}
            for name, number in state_body_name:
                Rifle.state_images[name] = [load_image("resource/Rifleman/" + name + "_body (%d).png" %(i + 1)) for i in range(number)]

        self.state = 'spawn'
        self.build_behavior_tree()

    def update(self):
        FRAMES_PER_ACTION = state_count[self.state]
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        if self.state == 'spawn' and self.frame > 21:
            self.state = 'Idle'
            self.frame = 0

        self.bt.run()

    def handle_event(self, event):
        pass

    def draw(self):
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom

        if self.frame > state_count[self.state]:
            self.frame = 0

        if self.state == 'aim' or self.state == 'ready' or self.state == 'shoot':
            pass
        else:
            width, height = rifle_size[self.state][int(self.frame)]
            Rifle.state_images[self.state][int(self.frame)].composite_draw(0, '', self.sx, self.sy, width*2, height*2)
            draw_rectangle(self.sx - width, self.sy - height, self.sx + width, self.sy + height)

    def get_bb(self):
        return self.x - 25, self.y - 66, self.x + 25, self.y + 50

    def handle_collision(self, group, other):
        pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def is_character_nearby(self, distance):
        if self.distance_less_than(server.character.x, server.character.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def run(self):
        self.state = 'running'
        return BehaviorTree.SUCCESS

    def idle(self):
        self.state = 'Idle'
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        c1 = Condition('캐릭터가 접근 거리내에 있는가?', self.is_character_nearby, 10)
        a1 = Action('라이플 달리기', self.run)

        root = run_rifle = Sequence('달리기', c1, a1)

        a2 = Action('라이플 가만히 있기', self.idle)

        root = idle_rifle = Sequence('가만히', a2)

        root = Selector('뭐든 해봐',run_rifle, idle_rifle)

        self.bt = BehaviorTree(root)