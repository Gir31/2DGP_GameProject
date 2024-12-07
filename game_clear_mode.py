from math import floor

from pico2d import *
import game_framework
import play_mode
import server
from background import Background
from moving_floor import Patrol_floor
from object_locate import Stage
from server import patrol_floors

frame = 0

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def init():
    global image, font, music, background, end_character
    background = Background(Stage)
    end_character = load_image("resource/character.png")
    image = [load_image("resource/end (%d).png" %(i + 1)) for i in range(79)]
    font = load_font('resource/ENCR10B.TTF',80)
    music = load_wav('resource/GAME_CLEAR_sound.wav')
    music.set_volume(40)
    music.repeat_play()

    server.character.x, server.character.y = 700, 300
    server.character.frame = 0


def finish():
    global image, font, music
    del image
    del font
    del music

def update():
    TIME_PER_ACTION = 3
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    server.end_frame = (server.end_frame + 79 * ACTION_PER_TIME * game_framework.frame_time) % 79

    C_TIME_PER_ACTION = 1
    C_ACTION_PER_TIME = 1.0 / C_TIME_PER_ACTION

    server.end_char_frame = (server.end_char_frame + 8 * C_ACTION_PER_TIME * game_framework.frame_time) % 8

def draw():
    clear_canvas()
    background.draw()
    image[int(server.end_frame)].clip_composite_draw(0, 0, 1488, 992, 0, '', 700, 400, 1488, 992)
    for land in server.lands:
        land.draw()
    font.draw(400, 390, 'GAME CLEAR!!', (255, 0, 0))
    end_character.clip_composite_draw(int(server.end_char_frame + 7) * 124, 124, 124, 124,
                                      0, 'h', 700, 160, 248, 248)
    update_canvas()

def pause():
    pass

def resume():
    pass