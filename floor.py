from pico2d import load_image, draw_rectangle


class Floor:
    image = None

    def __init__(self, x, y):
        self.x, self.y = x, y

        if Floor.image == None:
            Floor.image = load_image('resource\Platform.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 77, self.y + 10, self.x + 77, self.y + 17

    def handle_collision(self, group, other):
        pass