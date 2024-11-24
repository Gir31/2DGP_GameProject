from pico2d import load_image, draw_rectangle


class Land:
    image = None

    def __init__(self, x):
        self.x, self.y = x, 0
        if Land.image == None:
            Land.image = load_image('resource\chap1_land.png')

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 177, self.y, self.x + 177, self.y + 67

    def handle_collision(self, group, other):
        pass