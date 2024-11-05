from pico2d import load_image
from state_machine import *

class Idle:
    @staticmethod
    def enter(character, e):
        if start_event(e):
            character.action = 1
            character.face_dir = 1
        elif right_down(e) or left_up(e):
            character.action = 1
            character.face_dir = -1
        elif left_down(e) or right_up(e):
            character.action = 1
            character.face_dir = 1
        elif down_down(e) or down_up(e):
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
            character.dir, character.face_dir, character.action = 1, 1, 9
        elif left_down(e) or right_up(e):
            character.dir, character.face_dir, character.action = -1, -1, 9

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

class Fall:
    @staticmethod
    def enter(character, e):
        character.action = 0
        character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 3
        pass

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.image.clip_draw(character.frame * 124, character.action * 124, 124, 124, character.x, character.y)
        elif character.face_dir == -1:
            character.image.clip_composite_draw(character.frame * 124, character.action * 124, 124, 124,
                                                0, 'h', character.x, character.y, 124, 124)


class Character:

    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, down_down : Sit, down_up : Sit},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                Sit: {right_down: Run, left_down: Run, right_up: Run, left_up: Run},
                Fall: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, down_down : Idle, down_up : Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()


