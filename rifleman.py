from pico2d import draw_rectangle, load_image

state_name = ['Idle', 'run_start', 'running', 'run_stop', 'spawn', 'coma_roop', 'coma_end']
state_number = [15, 1, 8, 6, 22, 8, 6]
state_arm_name = ['aim_arm', 'ready_arm', 'shoot_arm']
state_arm_number = [3, 1, 3]
state_body_name = ['aim_body', 'shoot_body']
state_body_number = [3, 1, 3]



class Rifle:
    state_images = None
    arm_images = None
    body_images = None

    def __init__(self, x, y):

        if Rifle.state_images == None:
            Rifle.state_images = {}
            for name, number in state_name, state_number:
                Rifle.state_images = [load_image("resource/Rifleman/"+ name +" (%d).png" %i) for i in range(number)]
        if Rifle.arm_images == None:
            Rifle.arm_images = {}
            for name, number in state_arm_name, state_arm_number:
                Rifle.state_images = [load_image("resource/Rifleman/" + name + " (%d).png" % i) for i in range(number)]
        if Rifle.body_images == None:
            Rifle.body_images = {}
            for name, number in state_body_name, state_body_number:
                Rifle.state_images = [load_image("resource/Rifleman/" + name + " (%d).png" % i) for i in range(number)]

    def update(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        draw_rectangle(self.sx - 25, self.sy - 66, self.sx + 25, self.sy + 50)

    def get_bb(self):
        return self.x - 25, self.y - 66, self.x + 25, self.y + 50

    def handle_collision(self, group, other):
        pass