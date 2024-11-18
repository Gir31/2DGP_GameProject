from pico2d import load_image, get_time, draw_rectangle
from sdl2.examples.draw import draw_rects

import game_framework
from state_machine import *
from floor_locate import *

TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

PIXEL_PER_METER = (10.0 / 0.2)
RUN_SPEED_KMPH = 40.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

def drawing(character, count):
    if character.face_dir == 1:
        character.image.clip_draw(int(character.frame + count) * 124, character.action * 124, 124, 124, character.x, character.y - 5)
    elif character.face_dir == -1:
        character.image.clip_composite_draw(int(character.frame + count) * 124, character.action * 124, 124, 124,
                                            0, 'h', character.x, character.y - 5, 124, 124)











def landing(character):
    # 스테이지의 바닥을 찾았다면 멈추기
    if character.y <= 112:
        character.state_machine.add_event(('LANDING', 0))
        character.y = 112
        return

    # 스테이지 내의 인공 구조물을 찾았다면 멈추기
    for x, y in floor_locate[Stage]:
        if character.x >= x - 77 and character.x <= x + 77:  # 캐릭터가 플랫폼의 x범위 내에 있는가?
            if character.y <= y + 79 and character.y > y + 69 :
                character.state_machine.add_event(('LANDING', 0))
                character.y = y + 79
                return

    character.state_machine.add_event(('FALL', 0))


class Idle:
    @staticmethod
    def enter(character, e):
        if start_event(e):
            character.face_dir = 1
        elif right_down(e) or left_up(e):
            character.face_dir = -1
        elif left_down(e) or right_up(e):
            character.face_dir = 1
        else: pass

        character.action = 1
        character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 7 * ACTION_PER_TIME * game_framework.frame_time) % 7

    @staticmethod
    def draw(character):
        drawing(character, 0)


class Run:
    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e):
            character.dir, character.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            character.dir, character.face_dir = -1, -1

        character.action = 9
    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 9 * ACTION_PER_TIME * game_framework.frame_time) % 9
        character.x += character.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(character):
        drawing(character, 0)


class Sit:
    @staticmethod
    def enter(character, e):
        character.action = 1
        character.frame = 0
        character.y -= 10

    @staticmethod
    def exit(character, e):
        character.y += 10
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 8 * ACTION_PER_TIME * game_framework.frame_time) % 8
        pass

    @staticmethod
    def draw(character):
        drawing(character, 7)


class JumpIdle:
    @staticmethod
    def enter(character, e):
        character.dir = 0
        if space_down(e):
            character.action = 0
            character.frame = 0
            character.jump_time = get_time()
        elif right_down(e) or left_up(e):
            character.face_dir = 1
        elif left_down(e) or right_up(e):
            character.face_dir = -1

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if character.frame < 4:
            character.frame = (character.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5
        character.y +=  RUN_SPEED_PPS * game_framework.frame_time
        if get_time() - character.jump_time > 0.5:
            character.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(character):
        drawing(character, 0)


class JumpMove:
    @staticmethod
    def enter(character, e):
        if space_down(e):
            character.action = 0
            character.frame = 0
            character.jump_time = get_time()
        if right_down(e) or left_up(e):
            character.dir, character.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            character.dir, character.face_dir = -1, -1

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if character.frame < 4:
            character.frame = (character.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5

        character.y += RUN_SPEED_PPS * game_framework.frame_time
        character.x += character.dir * RUN_SPEED_PPS * game_framework.frame_time
        if get_time() - character.jump_time > 0.5:
            character.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(character):
        drawing(character, 0)


class FallFromJump:
    @staticmethod
    def enter(character, e):
        character.action = 0
        character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4

        if character.frame > 3:
            character.state_machine.add_event(('MOTION_FINISH', 0))

    @staticmethod
    def draw(character):
        drawing(character, 8)


class FallIdle:
    @staticmethod
    def enter(character, e):
        if motion_finish(e):
            character.action = 0
            character.frame = 0
        elif right_down(e) or left_up(e):
            character.face_dir = 1
        elif left_down(e) or right_up(e):
            character.face_dir = -1


    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.y -= RUN_SPEED_PPS * game_framework.frame_time
        if character.frame < 2:
            character.frame = (character.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3

        landing(character)
        pass

    @staticmethod
    def draw(character):
        drawing(character, 5)


class FallMove:
    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e):
            character.dir, character.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            character.dir, character.face_dir = -1, -1

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.y -= RUN_SPEED_PPS * game_framework.frame_time
        character.x += character.dir * RUN_SPEED_PPS * game_framework.frame_time
        if character.frame < 2:
            character.frame = (character.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3

        landing(character)
        pass

    @staticmethod
    def draw(character):
        drawing(character, 5)


class Land:
    @staticmethod
    def enter(character, e):
        character.action = 9
        character.frame = 0
        character.dir = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4

        if character.frame > 3:
            character.state_machine.add_event(('MOTION_FINISH', 0))
        pass

    @staticmethod
    def draw(character):
        drawing(character, 12)


class Character:

    def __init__(self):
        self.x, self.y = 400, 112
        self.face_dir = 1
        self.jump_time = 0
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, down_down : Sit, space_down : JumpIdle},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down : JumpMove, character_landing : Idle, character_falling : FallIdle},
                Sit: {right_down: Run, left_down: Run, right_up: Run, left_up: Run},
                JumpIdle: {right_down: JumpMove, left_down: JumpMove, right_up: JumpMove, left_up: JumpMove, time_out : FallFromJump},
                JumpMove: {right_down: JumpIdle, left_down: JumpIdle, right_up: JumpIdle, left_up: JumpIdle, time_out : FallFromJump},
                FallFromJump : {motion_finish : FallIdle},
                FallIdle: {right_down: FallMove, left_down: FallMove, right_up: FallMove, left_up: FallMove, character_landing : Land},
                FallMove: {right_down: FallIdle, left_down: FallIdle, right_up: FallIdle, left_up: FallIdle, character_landing : Land},
                Land: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, motion_finish : Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y - 63, self.x + 25, self.y + 50

    def handle_collision(self, group, other):
        if 'character:land':
            self.state_machine.add_event(('LANDING', 0))
        pass


