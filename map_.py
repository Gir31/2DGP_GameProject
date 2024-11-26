from pico2d import get_canvas_width, get_canvas_height, clamp
import server

class Map:
    def __init__(self):
        self.w, self.h = 4000, 3500
        self.cw, self.ch =  get_canvas_width(), get_canvas_height()

    def draw(self):
        pass

    def update(self):
        self.window_left = clamp(0, int(server.character.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.character.y) - self.ch // 2, self.h - self.ch - 1)

    def handle_event(self, event):
        pass