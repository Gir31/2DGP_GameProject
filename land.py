from pico2d import load_image, draw_rectangle


class Land:
    image = None

    def __init__(self, x, y):
        self.x, self.y = x, y

        if self.image == None:
            self.image = load_image('Platform.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 77, self.y - 17, self.x + 77, self.y + 17

    def handle_collision(self, group, other):
        pass