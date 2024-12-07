from pico2d import *
import game_framework
import server


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def init():
    global image, font, music
    image = load_image("resource/GAME_OVER.png")
    font = load_font('resource/ENCR10B.TTF',40)
    music = load_wav('resource/GAME_OVER_sound.wav')
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
    TIME_PER_ACTION = 1.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

    if server.character.frame < 3.5 and server.character.action == 7:
        server.character.frame = (server.character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
    else:
        server.character.action = 9
        server.character.frame = 0

def draw():
    clear_canvas()
    image.clip_composite_draw(0, 0, 2048, 1152, 0, '', 700, 400, 1400, 800)
    font.draw(590, 400, 'GAME OVER', (255, 255, 255))
    server.character.draw()
    update_canvas()

def pause():
    pass

def resume():
    pass