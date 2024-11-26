from pico2d import load_image, draw_rectangle
import server


class Floor:
    image = None

    def __init__(self, x, y):
        self.x, self.y = x, y

        if Floor.image == None:
            Floor.image = load_image('resource\Platform.png')

    def draw(self):
        sx = self.x - server.map.window_left
        sy = self.y - server.map.window_bottom

        self.image.draw(sx, sy)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 77, self.y + 10, self.x + 77, self.y + 17

    def handle_collision(self, group, other):
        pass