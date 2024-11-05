from pico2d import load_image

class Land:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('Platform.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)