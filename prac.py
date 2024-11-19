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