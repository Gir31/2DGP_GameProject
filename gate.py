import game_framework
from pico2d import *

import object_locate
import server
from object_locate import gate_locate
from state_machine import *

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Closed:
    @staticmethod
    def enter(gate, e):
        gate.frame = 0
        gate.state = 'closed'
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
        gate.Images['Closed'][int(gate.frame)].draw(gate.sx, gate.sy)

    
class Closing:
    @staticmethod
    def enter(gate, e):
        gate.frame = 0
        gate.state = 'closing'
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
        gate.Images['Closing'][int(gate.frame)].draw(gate.sx, gate.sy)
    
class Opening:
    @staticmethod
    def enter(gate, e):
        gate.frame = 0
        gate.state = 'opening'
        pass

    @staticmethod
    def exit(gate, e):
        pass

    @staticmethod
    def do(gate):
        if gate.frame < 6.5:
            gate.frame = (gate.frame + 7 * ACTION_PER_TIME * game_framework.frame_time) % 7
        pass

    @staticmethod
    def draw(gate):
        if gate.frame < 6.5:
            gate.Images['Opening'][int(gate.frame)].draw(gate.sx, gate.sy)

class Gate:
    Images = None

    def __init__(self, stage):
        self.x, self.y = gate_locate[stage]
        self.sx, self.sy = None, None
        self.state = 'closing'
        self.state_machine = StateMachine(self)
        self.state_machine.start(Closing)
        self.state_machine.set_transitions(
            {
                Closed : {clear : Opening},
                Closing : {motion_finish : Closed},
                Opening : {}
            }
        )

        if Gate.Images == None:
            Gate.Images = {}
            Gate.Images['Closed'] = [load_image("resource/gate_closed (%d).png" %i) for i in range(1, 6)]
            Gate.Images['Closing'] = [load_image("resource/gate_closing (%d).png" % i) for i in range(1, 10)]
            Gate.Images['Opening'] = [load_image("resource/gate_opening (%d).png" % i) for i in range(1, 8)]

    def update(self):
        self.state_machine.update()
        if object_locate.rifle_amount == 0:
            self.state_machine.add_event(('CLEAR', 0))

    def draw(self):
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom

        self.state_machine.draw()

    def get_bb(self):
        return self.x - 29, self.y - 160, self.x + 29, self.y + 160

    def handle_collision(self, group, other):
        pass