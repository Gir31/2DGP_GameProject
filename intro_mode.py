from pico2d import *
import game_framework
import play_mode
import server


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)


def init():
    global image, font, music
    image = load_image("resource/intro.png")
    font = load_font('resource/ENCR10B.TTF',40)
    music = load_wav('resource/intro_music.wav')
    music.set_volume(40)
    music.repeat_play()


def finish():
    global image, font, music
    del image
    del font
    del music

def update():
    pass

def draw():
    clear_canvas()
    image.clip_composite_draw(0, 0, 1924, 1714, 0, '', 700, 400, 1924, 1714)
    if int(get_time()) % 2 == 1:
        font.draw(550, 100, 'PRESS SPACE', (0, 0, 0))
    update_canvas()

def pause():
    pass

def resume():
    pass