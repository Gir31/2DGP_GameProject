from pico2d import load_image, draw_rectangle


class Wall:
    image = None

    def __init__(self, x, y, dir):
        self.x, self.y, self.dir = x, y, dir
        if Wall.image == None:
            Wall.image = load_image('resource\Wall.png')

    def draw(self):
        if self.dir == 1:
            self.image.draw(self.x, self.y)
        else:
            self.image.composite_draw(0, 'h', self.x, self.y, 59, 242)

        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 29, self.y - 121, self.x + 29, self.y + 121

    def handle_collision(self, group, other):
        pass