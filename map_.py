from pico2d import get_canvas_width, get_canvas_height, clamp, load_wav, get_time, load_font

import object_locate
import server

class Map:
    def __init__(self):
        self.w, self.h = 4000, 1500
        self.cw, self.ch =  get_canvas_width(), get_canvas_height()
        self.BGM_time, self.BGM_number = 0, 0

        self.font = load_font('resource/ENCR10B.TTF', 32)

        self.BGMs = {}
        self.BGMs = [load_wav("resource/BGM (%d).wav" %(i + 1)) for i in range(5)]
        for i in range(5):
            self.BGMs[i].set_volume(50)

        self.BGMs[self.BGM_number].play()

    def draw(self):
        self.font.draw(975, 750, f'Remaining Enemy : {object_locate.rifle_amount:02d}', (255, 255, 255))


    def update(self):
        self.window_left = clamp(0, int(server.character.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.character.y) - self.ch // 2, self.h - self.ch - 1)


        if get_time() - self.BGM_time > 265:
            self.BGM_number = (self.BGM_number + 1) % 5
            self.BGMs[self.BGM_number].play()

    def handle_event(self, event):
        pass