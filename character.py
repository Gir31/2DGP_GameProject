from pico2d import load_image, draw_rectangle, get_time, clamp, get_canvas_width, get_canvas_height
import game_framework
import server
from state_machine import *


def drawing(character, count):
    if character.face_dir == 1:
        character.image.clip_draw(int(character.frame + count) * 124, character.action * 124, 124, 124, character.sx, character.sy - 5)
    elif character.face_dir == -1:
        character.image.clip_composite_draw(int(character.frame + count) * 124, character.action * 124, 124, 124,
                                            0, 'h', character.sx, character.sy - 5, 124, 124)

class Idle:
    @staticmethod
    def enter(character, e):
        if start_event(e):
            character.face_dir = 1
        elif right_down(e) or left_up(e):
            character.face_dir = -1
        elif left_down(e) or right_up(e):
            character.face_dir = 1



        if character.jump == False and character.fall_from_jump == False and character.fall == False:
            character.landing = False
            character.action = 1
            character.frame = 0

        character.dir = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

        if character.jump == True:
            if character.frame < 4:
                character.frame = (character.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5
        elif character.fall_from_jump == True:
            if character.frame < 3:
                TIME_PER_ACTION = 0.1
                ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
                character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
            else:
                character.fall_from_jump = False
                character.fall = True
                character.action = 0
                character.frame = 0
        elif character.fall == True:
            if character.frame < 2:
                character.frame = (character.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3
        elif character.landing == True:
            if character.frame <= 3:
                character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
            else:
                character.landing = False
                character.state_machine.add_event(('AGAIN', 0))
        else:
            character.frame = (character.frame + 7 * ACTION_PER_TIME * game_framework.frame_time) % 7

    @staticmethod
    def draw(character):
        if character.jump == True:
            drawing(character, 0)
        elif character.fall_from_jump == True:
            drawing(character, 8)
        elif character.fall == True:
            drawing(character, 5)
        elif character.landing == True:
            drawing(character, 12)
        else:
            drawing(character, 0)


class Move:
    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e):
            character.dir, character.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            character.dir, character.face_dir = -1, -1

        if character.jump == False and character.fall_from_jump == False and character.fall == False:
            character.landing = False
            character.action = 9
            character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        if character.jump == True:
            if character.frame < 4:
                character.frame = (character.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5
        elif character.fall_from_jump == True:
            if character.frame < 3:
                TIME_PER_ACTION = 0.1
                ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
                character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
            else:
                character.fall_from_jump = False
                character.state_machine.add_event(('AGAIN', 0))
                character.action = 0
                character.frame = 0
        elif character.fall == True:
            if character.frame < 2:
                character.frame = (character.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3
        elif character.landing == True:
            if character.frame <= 3:
                character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
            else:
                character.landing = False
                character.state_machine.add_event(('AGAIN', 0))
        else:
            character.frame = (character.frame + 7 * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(character):
        if character.jump == True:
            drawing(character, 0)
        elif character.fall_from_jump == True:
            drawing(character, 8)
        elif character.fall == True:
            drawing(character, 5)
        elif character.landing == True:
            drawing(character, 12)
        else:
            drawing(character, 1)

class Character:

    def __init__(self):
        self.x, self.y = 100, 132
        self.sx, self.sy = get_canvas_width() / 2, get_canvas_height() / 2
        self.dir = 0
        self.face_dir = 1
        self.character_land = True
        self.jump = False
        self.jump_time = 0
        self.fall_from_jump = False
        self.fall = False
        self.landing = False
        self.image = load_image("resource\character\character.png")
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down : Move, left_down : Move, right_up : Move, left_up : Move, again_action : Idle},
                Move: {right_down : Idle, left_down : Idle, right_up : Idle, left_up : Idle, again_action : Move},
            }
        )

        self.x = clamp(25.0, self.x, server.map.w - 25.0)
        self.y = clamp(66.0, self.y, server.map.h - 66.0)

    def update(self):
        self.state_machine.update()

        PIXEL_PER_METER = (10.0 / 0.2)

        FALL_SPEED_KMPH = 80
        FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
        FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
        FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)

        GRAVITY = FALL_SPEED_PPS * game_framework.frame_time * -1

        if self.character_land == True:
            GRAVITY = 0

        if self.jump == True:
            JUMP_SPEED_KMPH = 120
            JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
            JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
            JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

            GRAVITY = JUMP_SPEED_PPS * game_framework.frame_time
            if get_time() - self.jump_time > 0.2:
                self.jump = 0
                self.jump = False
                self.fall_from_jump = True
                self.action = 0
                self.frame = 0

        RUN_SPEED_KMPH = 60
        RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

        self.y += GRAVITY

        self.x = clamp(25.0, self.x, server.map.w - 25.0)
        self.y = clamp(66.0, self.y, server.map.h - 66.0)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                if self.character_land == True:
                    self.jump = True
                    self.jump_time = get_time()
                    self.frame = 0
                    self.action = 0

        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.sx, self.sy = self.x - server.map.window_left, self.y - server.map.window_bottom

        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y - 66, self.x + 25, self.y + 50

    def handle_collision(self, group, other):
        if 'character:floor' or 'character:land':
            minX_o, minY_o, maxX_o, maxY_o = other.get_bb()
            minX_c, minY_c, maxX_c, maxY_c = self.get_bb()

            if minY_o < minY_c:
                self.character_land = True
                if self.fall == True:
                    self.fall = False
                    self.landing = True
                    self.action = 9
                    self.frame = 0

