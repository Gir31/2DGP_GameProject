from pico2d import load_image, draw_rectangle

import server


class Wall:
    image = None

    def __init__(self, x, y, dir):
        self.x, self.y, self.dir = x, y, dir
        if Wall.image == None:
            Wall.image = load_image('resource/Wall.png')

    def draw(self):
        sx = self.x - server.map.window_left
        sy = self.y - server.map.window_bottom

        if self.dir == 1:
            self.image.draw(sx, sy)
        else:
            self.image.composite_draw(0, 'h', sx, sy, 59, 242)

    def update(self):
        pass

    def get_bb(self):
        return self.x - 29, self.y - 121, self.x + 29, self.y + 121

    def handle_collision(self, group, other):
        pass