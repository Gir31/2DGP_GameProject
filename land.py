from pico2d import load_image

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