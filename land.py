from pico2d import load_image, draw_rectangle

import server


class Land:
    image = None

    def __init__(self, x):
        self.x, self.y = x, 0
        if Land.image == None:
            Land.image = load_image('resource/chap1_land.png')

    def draw(self):
        sx = self.x - server.map.window_left
        sy = self.y - server.map.window_bottom

        self.image.draw(sx, sy)

    def update(self):
        pass

    def get_bb(self):
        return self.x - 177, self.y, self.x + 177, self.y + 67

    def handle_collision(self, group, other):
        pass