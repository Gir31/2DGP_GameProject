from pico2d import load_image, draw_rectangle
from state_machine import *

def drawing(character, count):
    if character.face_dir == 1:
        character.image.clip_draw(int(character.frame + count) * 124, character.action * 124, 124, 124, character.x, character.y - 5)
    elif character.face_dir == -1:
        character.image.clip_composite_draw(int(character.frame + count) * 124, character.action * 124, 124, 124,
                                            0, 'h', character.x, character.y - 5, 124, 124)


class Idle:
    @staticmethod
    def enter(character, e):
        if start_event(e):
            character.face_dir = 1
        elif right_down(e) or left_up(e):
            character.face_dir = -1
        elif left_down(e) or right_up(e):
            character.face_dir = 1
        elif motion_finish(e):
            pass

        character.dir = 0
        character.action = 1
        character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        character.frame = (character.frame + 7 * ACTION_PER_TIME * game_framework.frame_time) % 7

    @staticmethod
    def draw(character):
        drawing(character, 0)

<<<<<<< HEAD
class Run:
    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e):
            character.dir, character.face_dir = 1, 1
            character.accel_time = get_time()
        elif left_down(e) or right_up(e):
            character.dir, character.face_dir = -1, -1
            character.accel_time = get_time()
        elif motion_move_finish(e):
            character.accel_time = get_time()


        character.acceleration = 0.0
        character.action = 9

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if character.acceleration <= 2:
            character.acceleration = get_time() - character.accel_time

        PIXEL_PER_METER = (10.0 / 0.2)
        RUN_SPEED_KMPH = (60.0 / 2) * character.acceleration
        RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

        character.frame = (character.frame + 8 * ACTION_PER_TIME * game_framework.frame_time) % 8
        character.x += character.dir * RUN_SPEED_PPS * game_framework.frame_time

        check_air(character)

    @staticmethod
    def draw(character):
        drawing(character, 1)

class JumpIdle:
    @staticmethod
    def enter(character, e):
        if space_down(e):
            character.action = 0
            character.frame = 0
            character.jump_time = get_time()
            character.accel_time = get_time()
            character.jump_acceleration = 0.0
        elif right_down(e) or left_up(e):
            character.face_dir = -1
        elif left_down(e) or right_up(e):
            character.face_dir = 1

        character.dir = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        TIME_PER_ACTION = 0.25
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

        if character.frame < 4:
            character.frame = (character.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5

        character.jump_acceleration = get_time() - character.accel_time

        PIXEL_PER_METER = (10.0 / 0.1)
        JUMP_SPEED_KMPH = 60.0 * (0.5 - character.jump_acceleration)
        JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
        JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
        JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

        character.y += JUMP_SPEED_PPS * game_framework.frame_time
        if get_time() - character.jump_time > 0.5:
            character.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(character):
        drawing(character, 0)

class JumpMove:
    @staticmethod
    def enter(character, e):
        if space_down(e):
            # 애니메이션과 관련된 변수
            character.action = 0
            character.frame = 0
            # 점프 높이, 속도
            character.jump_time = get_time()
            character.jump_acceleration = 0.0
            # 점프 시 이동
            character.air_acceleration = character.acceleration
        if right_down(e) or left_up(e):
            character.air_acceleration = 2.0
            character.dir, character.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            character.air_acceleration = 2.0
            character.dir, character.face_dir = -1, -1

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        TIME_PER_ACTION = 0.25
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        if character.frame < 4:
            character.frame = (character.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5

        PIXEL_PER_METER = (10.0 / 0.1)
        JUMP_SPEED_KMPH = 60.0 * (0.5 - character.jump_acceleration)
        JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
        JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
        JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

        character.y += JUMP_SPEED_PPS * game_framework.frame_time

        character.air_acceleration = get_time() - character.accel_time

        PIXEL_PER_METER = (10.0 / 0.2)
        AIR_MOVE_SPEED_KMPH = (60.0 / 2) * character.air_acceleration
        AIR_MOVE_SPEED_MPM = (AIR_MOVE_SPEED_KMPH * 1000.0 / 60.0)
        AIR_MOVE_SPEED_MPS = (AIR_MOVE_SPEED_MPM / 60.0)
        AIR_MOVE_SPEED_PPS = (AIR_MOVE_SPEED_MPS * PIXEL_PER_METER)

        character.x += character.dir * AIR_MOVE_SPEED_PPS * game_framework.frame_time
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
        TIME_PER_ACTION = 0.1
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4

        if character.frame > 3:
            if character.dir == 0:
                character.state_machine.add_event(('MOTION_FINISH', 0))
            else:
                character.state_machine.add_event(('MOTION_MOVE_FINISH', 0))

    @staticmethod
    def draw(character):
        drawing(character, 8)

class FallIdle:
    @staticmethod
    def enter(character, e):
        if motion_finish(e) or character_falling(e):
            character.action = 0
            character.frame = 0
            character.accel_time = get_time()
            character.acceleration = 0.0
        elif right_down(e) or left_up(e):
            character.face_dir = -1
        elif left_down(e) or right_up(e):
            character.face_dir = 1

        character.dir = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if character.acceleration <= 1:
            character.acceleration = get_time() - character.accel_time

        PIXEL_PER_METER = (10.0 / 0.1)
        FALL_SPEED_KMPH = (35.28 / 1) * character.acceleration
        FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
        FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
        FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)

        character.y -= FALL_SPEED_PPS * game_framework.frame_time

        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        if character.frame < 2:
            character.frame = (character.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3

    @staticmethod
    def draw(character):
        drawing(character, 5)

class FallMove:
    @staticmethod
    def enter(character, e):
        if motion_move_finish(e) or character_falling(e):
            character.action = 0
            character.frame = 0
            character.accel_time = get_time()
            character.acceleration = 0.0
        elif right_down(e) or left_up(e):
            character.dir, character.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            character.dir, character.face_dir = -1, -1

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if character.acceleration <= 1:
            character.acceleration = get_time() - character.accel_time

        PIXEL_PER_METER = (10.0 / 0.1)
        FALL_SPEED_KMPH = (35.28 / 1) * character.acceleration
        FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
        FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
        FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)

        character.y -= FALL_SPEED_PPS * game_framework.frame_time

        PIXEL_PER_METER = (10.0 / 0.2)
        AIR_MOVE_SPEED_KMPH = (60.0 / 2) * character.air_acceleration
        AIR_MOVE_SPEED_MPM = (AIR_MOVE_SPEED_KMPH * 1000.0 / 60.0)
        AIR_MOVE_SPEED_MPS = (AIR_MOVE_SPEED_MPM / 60.0)
        AIR_MOVE_SPEED_PPS = (AIR_MOVE_SPEED_MPS * PIXEL_PER_METER)

        character.x += character.dir * AIR_MOVE_SPEED_PPS * game_framework.frame_time

        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        if character.frame < 2:
            character.frame = (character.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3

    @staticmethod
    def draw(character):
        drawing(character, 5)

class LandIdle:
    @staticmethod
    def enter(character, e):
        if character_landing(e):
            character.action = 9
            character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if character.frame <= 3:
            TIME_PER_ACTION = 0.5
            ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
            character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
        else:
            print('finish')
            character.state_machine.add_event(('MOTION_FINISH', 0))

    @staticmethod
    def draw(character):
        drawing(character, 12)

class LandMove:
    @staticmethod
    def enter(character, e):
        if character_landing(e):
            character.action = 9
            character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if character.frame <= 3:
            TIME_PER_ACTION = 0.5
            ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
            character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
        else:
            print('finish')
            character.state_machine.add_event(('MOTION_MOVE_FINISH', 0))

    @staticmethod
    def draw(character):
        drawing(character, 12)

=======
>>>>>>> 4eb05157799b8a597be2de8cd47665e5ce346bb4
class Character:

    def __init__(self):
        self.x, self.y = 100, 132
        self.dir = 0
        self.face_dir = 1
        self.image = load_image("resource\character\character.png")
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
<<<<<<< HEAD
                Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down : JumpIdle},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down : JumpMove, character_falling : FallMove},
                JumpIdle : {right_down: JumpMove, left_down: JumpMove, right_up : JumpMove, left_up : JumpMove, time_out : FallFromJump},
                JumpMove : {right_down: JumpIdle, left_down: JumpIdle, right_up: JumpIdle, left_up: JumpIdle, time_out : FallFromJump},
                FallFromJump : {motion_finish : FallIdle, motion_move_finish : FallMove},
                FallIdle : {right_down: FallMove, left_down: FallMove, right_up: FallMove, left_up: FallMove, character_landing : LandIdle},
                FallMove: {right_down: FallIdle, left_down: FallIdle, right_up: FallIdle, left_up: FallIdle, character_landing: LandMove},
                LandIdle : {right_down: LandMove, left_down: LandMove, right_up: LandMove, left_up: LandMove, motion_finish : Idle},
                LandMove : {right_down: LandIdle, left_down: LandIdle, right_up: LandIdle, left_up: LandIdle, motion_move_finish : Run}
=======

>>>>>>> 4eb05157799b8a597be2de8cd47665e5ce346bb4
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y - 66, self.x + 25, self.y + 50

    def handle_collision(self, group, other):
        if 'character:floor' or 'character:land':
            pass