import random
import game_framework
import object_locate
from pico2d import *

background_frame_count = [41]

TIME_PER_ACTION = 5.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 40.0

class Background:
    background_images = None
    sky_images = None

    def __init__(self, stage):
        self.frame = random.randint(0, 40)

        if Background.background_images == None:
            Background.background_images = {}
            Background.background_images[stage] = [load_image("resource/background/chap%d/chap%d_background (%d).png" %(stage, stage, i)) for i in range(1, background_frame_count[stage-1])]
        if Background.sky_images == None:
            Background.sky_images = {}
            Background.sky_images[stage] = load_image("resource/background/chap%d/chap%d_background_sky.png"%(stage, stage))

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self):
        Background.sky_images[object_locate.Stage].composite_draw(0, 'h', 700, 400, 1400, 800)
        Background.background_images[object_locate.Stage][int(self.frame)].draw(700, 400)