import random
from pico2d import load_image, draw_rectangle, cur_time, get_time
import game_framework
import server

state_name = ['Idle', 'Sink']

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8.0


class Sink_floor:
    images = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.origin_y = y
        self.show = True
        self.state = 'Idle'
        self.frame = random.randint(0, 7)
        self.cur_time = 0

        if Sink_floor.images == None:
            Sink_floor.images = {}
            for name in state_name:
                Sink_floor.images[name] = [load_image("resource/sink_platform/"+ name +" (%d).png" %(i + 1)) for i in range(8)]

    def draw(self):
        if self.show == True:
            sx = self.x - server.map.window_left
            sy = self.y - server.map.window_bottom

            self.images[self.state][int(self.frame)].draw(sx, sy)
            draw_rectangle(sx - 70, sy + 37, sx + 70, sy + 42)

    def update(self):
        if self.show == True:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

            if self.cur_time != 0 and get_time() - self.cur_time > 1.5:
                PIXEL_PER_METER = (10.0 / 0.2)
                FALL_SPEED_KMPH = 10
                FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
                FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
                FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)

                self.y -= FALL_SPEED_PPS * game_framework.frame_time

                if self.origin_y - self.y > 200:
                    self.show = False
                    self.cur_time = 0
                    self.state = 'Idle'
        else:
            if self.cur_time == 0:
                self.cur_time = get_time()

            if get_time() - self.cur_time > 3:
                self.cur_time = 0
                self.show = True
                self.y = self.origin_y



    def get_bb(self):
        return self.x - 70, self.y + 37, self.x + 70, self.y + 42

    def handle_collision(self, group, other):
        match group:
            case 'character:sink_floor':
                if other.landing == True:
                    if self.cur_time == 0:
                        self.cur_time = get_time()
                    self.state = 'Sink'

class Patrol_floor:
    images = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.left_point, self.right_point = x - 150, x + 150
        self.frame = random.randint(0, 7)
        self.dir = 1
        self.speed = 0

        if Patrol_floor.images == None:
            Patrol_floor.images = {}
            Patrol_floor.images = [load_image("resource/move_platform/Idle (%d).png" % (i + 1)) for i in range(8)]


    def draw(self):
        sx = self.x - server.map.window_left
        sy = self.y - server.map.window_bottom

        self.images[int(self.frame)].draw(sx, sy)
        draw_rectangle(sx - 75, sy - 18, sx + 75, sy - 13)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        PIXEL_PER_METER = (10.0 / 0.2)
        PATROL_SPEED_KMPH = 10
        PATROL_SPEED_MPM = (PATROL_SPEED_KMPH * 1000.0 / 60.0)
        PATROL_SPEED_MPS = (PATROL_SPEED_MPM / 60.0)
        PATROL_SPEED_PPS = (PATROL_SPEED_MPS * PIXEL_PER_METER)

        self.speed = self.dir * PATROL_SPEED_PPS * game_framework.frame_time

        self.x += self.speed

        if self.x < self.left_point or self.x > self.right_point:
            self.dir *= -1

    def get_bb(self):
        return self.x - 75, self.y - 18, self.x + 75, self.y - 13

    def handle_collision(self, group, other):
        pass