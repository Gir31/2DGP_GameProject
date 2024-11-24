import random
import game_framework
import object_locate
from pico2d import *

background_frame_count = [41]

TIME_PER_ACTION = 5.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 40.0

class Background:
    sky_images = None

    def __init__(self, stage):
        self.frame = random.randint(0, 40)
        if Background.sky_images == None:
            Background.sky_images = {}
            Background.sky_images[stage] = load_image("resource/background/chap%d/chap%d_background_sky.png"%(stage, stage))

    def update(self):
        pass

    def draw(self):
        Background.sky_images[object_locate.Stage].composite_draw(0, 'h', 700, 400, 1400, 800)