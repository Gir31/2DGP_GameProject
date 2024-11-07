from pico2d import load_image, get_time
from state_machine import *
from floor_locate import *

class Idle:
    @staticmethod
    def enter(character, e):
        if start_event(e):
            character.face_dir = 1
        elif right_down(e) or left_up(e):
            character.face_dir = -1
        elif left_down(e) or right_up(e):
            character.face_dir = 1

        character.action = 1
        character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 7

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.image.clip_draw(character.frame * 124, character.action * 124, 124, 124, character.x, character.y)
        elif character.face_dir == -1:
            character.image.clip_composite_draw(character.frame * 124, character.action * 124, 124, 124,
                                                0, 'h', character.x, character.y, 124, 124)

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
        character.frame = (character.frame + 1) % 9
        character.x += character.dir * 10
        pass

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.image.clip_draw(character.frame * 124, character.action * 124, 124, 124, character.x, character.y)
        elif character.face_dir == -1:
            character.image.clip_composite_draw(character.frame * 124, character.action * 124, 124, 124,
                                                0, 'h', character.x, character.y, 124, 124)

class Sit:
    @staticmethod
    def enter(character, e):
        character.action = 1
        character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 8
        pass

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.image.clip_draw((character.frame + 7) * 124, character.action * 124, 124, 124, character.x, character.y)
        elif character.face_dir == -1:
            character.image.clip_composite_draw((character.frame + 7) * 124, character.action * 124, 124, 124,
                                                0, 'h', character.x, character.y, 124, 124)

class Jump:
    @staticmethod
    def enter(character, e):
        character.action = 0
        character.frame = 0
        character.jump_time = get_time()

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 6
        character.y += 5
        if get_time() - character.jump_time > 2:
            character.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.image.clip_draw(character.frame * 124, character.action * 124, 124, 124, character.x, character.y)
        elif character.face_dir == -1:
            character.image.clip_composite_draw(character.frame * 124, character.action * 124, 124, 124,
                                                0, 'h', character.x, character.y, 124, 124)

class Fall:
    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e):
            character.face_dir = 1
        elif left_down(e) or right_up(e):
            character.face_dir = -1

        character.action = 0
        character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.y -= 5
        
        # 스테이지의 바닥 또는 디딜곳을 찾았다면 떨어지는 것 멈추기
        if character.y < 90:
            character.state_machine.add_event(('LANDING', 0))
        else:
            for x, y in floor_locate[Stage]:
                if character.y < y:
                    character.state_machine.add_event(('LANDING', 0))
                    break


        if character.frame < 2:
            character.frame = (character.frame + 1) % 3
        pass

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.image.clip_draw((character.frame + 5) * 124, character.action * 124, 124, 124, character.x, character.y)
        elif character.face_dir == -1:
            character.image.clip_composite_draw((character.frame + 5) * 124, character.action * 124, 124, 124,
                                                0, 'h', character.x, character.y, 124, 124)


class Character:

    def __init__(self):
        self.x, self.y = 400, 90
        self.landingY = self.y
        self.face_dir = 1
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, down_down : Sit, space_down : Jump},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down : Jump},
                Sit: {right_down: Run, left_down: Run, right_up: Run, left_up: Run},
                Jump: {time_out : Fall},
                Fall: {right_down: Fall, left_down: Fall, right_up: Fall, left_up: Fall, character_landing : Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()


