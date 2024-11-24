import game_framework
from pico2d import *

from object_locate import gate_locate
from state_machine import *

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Closed:
    @staticmethod
    def enter(gate, e):
        gate.frame = 0
        pass

    @staticmethod
    def exit(gate, e):
        pass

    @staticmethod
    def do(gate):
        gate.frame = (gate.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5
        pass

    @staticmethod
    def draw(gate):
        gate.Images['Closed'][int(gate.frame)].draw(gate.x, gate.y)

    
class Closing:
    @staticmethod
    def enter(gate, e):
        gate.frame = 0
        pass

    @staticmethod
    def exit(gate, e):
        pass

    @staticmethod
    def do(gate):
        if gate.frame < 8:
            gate.frame = (gate.frame + 9 * ACTION_PER_TIME * game_framework.frame_time) % 9
        else: gate.state_machine.add_event(('MOTION_FINISH', 0))

    @staticmethod
    def draw(gate):
        gate.Images['Closing'][int(gate.frame)].draw(gate.x, gate.y)
    
class Opening:
    @staticmethod
    def enter(gate, e):
        gate.frame = 0
        pass

    @staticmethod
    def exit(gate, e):
        pass

    @staticmethod
    def do(gate):
        gate.frame = (gate.frame + 7 * ACTION_PER_TIME * game_framework.frame_time) % 7
        pass

    @staticmethod
    def draw(gate):
        gate.Images['Opening'][int(gate.frame)].draw(gate.x, gate.y)

class Gate:
    Images = None

    def __init__(self, stage):
        self.x, self.y = gate_locate[stage]
        self.state_machine = StateMachine(self)
        self.state_machine.start(Closing)
        self.state_machine.set_transitions(
            {
                Closed : {},
                Closing : {motion_finish : Closed},
                Opening : {}
            }
        )

        if Gate.Images == None:
            Gate.Images = {}
            Gate.Images['Closed'] = [load_image("resource/gate/gate_closed (%d).png" %i) for i in range(1, 6)]
            Gate.Images['Closing'] = [load_image("resource/gate/gate_closing (%d).png" % i) for i in range(1, 10)]
            Gate.Images['Opening'] = [load_image("resource/gate/gate_opening (%d).png" % i) for i in range(1, 8)]

    def update(self):
        self.state_machine.update()
    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 29, self.y - 160, self.x + 29, self.y + 160

    def handle_collision(self, group, other):
        pass