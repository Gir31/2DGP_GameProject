from pico2d import load_image, get_time
from state_machine import *
from floor_locate import *

def drawing(character, count):
    if character.face_dir == 1:
        character.image.clip_draw((character.frame + count) * 124, character.action * 124, 124, 124, character.x, character.y - 5)
    elif character.face_dir == -1:
        character.image.clip_composite_draw((character.frame + count) * 124, character.action * 124, 124, 124,
                                            0, 'h', character.x, character.y - 5, 124, 124)

def landing(character):
    # 스테이지 내의 인공 구조물을 찾았다면 멈추기
    for x, y in floor_locate[Stage]:
        if character.x >= x - 77 and character.x <= x + 77:  # 캐릭터가 플랫폼의 x범위 내에 있는가?
            if character.y <= y + 79 and character.y > y + 69 :
                character.state_machine.add_event(('LANDING', 0))
                character.y = y + 79
                return

    # 스테이지의 바닥을 찾았다면 멈추기
    if character.y <= 112:
        character.state_machine.add_event(('LANDING', 0))
        character.y = 112
    else:
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
        character.frame = (character.frame + 1) % 9
        character.x += character.dir * 10
        landing(character)
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
        character.frame = (character.frame + 1) % 8
        pass

    @staticmethod
    def draw(character):
        drawing(character, 7)

class Jump:
    @staticmethod
    def enter(character, e):
        character.dir = 0
        if right_down(e):
            character.dir, character.face_dir = 1, 1
        elif left_down(e):
            character.dir, character.face_dir = -1, -1
        elif character.motion == False:
            character.action = 0
            character.frame = 0
            character.jump_time = get_time()
            character.motion = True

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if character.frame < 4:
            character.frame = (character.frame + 1) % 5
        character.y += 10
        character.x += character.dir * 7
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
        character.motion = False

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 4

        if character.frame == 3:
            character.state_machine.add_event(('MOTION_FINISH', 0))

    @staticmethod
    def draw(character):
        drawing(character, 8)

class Fall:
    @staticmethod
    def enter(character, e):
        character.dir = 0
        if right_down(e):
            character.dir, character.face_dir = 1, 1
        elif left_down(e):
            character.dir, character.face_dir = -1, -1
        elif character.motion == False:
            character.action = 0
            character.frame = 0
            character.motion = True

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.y -= 10
        character.x += character.dir * 7
        landing(character)

        if character.frame < 2:
            character.frame = (character.frame + 1) % 3
        pass

    @staticmethod
    def draw(character):
        drawing(character, 5)

class Land:
    @staticmethod
    def enter(character, e):
        character.action = 9
        character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 4

        if character.frame == 3:
            character.state_machine.add_event(('MOTION_FINISH', 0))
        pass

    @staticmethod
    def draw(character):
        drawing(character, 12)

class Character:

    def __init__(self):
        self.x, self.y = 400, 112
        self.landingY = self.y
        self.face_dir = 1
        self.jump_time = 0
        self.motion = False
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, down_down : Sit, space_down : Jump, character_landing : Idle, character_falling : Fall},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down : Jump, character_landing : Run, character_falling : Fall},
                Sit: {right_down: Run, left_down: Run, right_up: Run, left_up: Run},
                Jump: {right_down: Jump, left_down: Jump, right_up: Jump, left_up: Jump, time_out : FallFromJump},
                FallFromJump : {motion_finish : Fall},
                Fall: {right_down: Fall, left_down: Fall, right_up: Fall, left_up: Fall, character_landing : Land},
                Land: {motion_finish : Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()


