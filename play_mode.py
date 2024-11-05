from pico2d import *
import game_world
import game_framework
from character import Character
from land import Land


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            character.handle_event(event)


def init():
    global character

    character = Character()
    game_world.add_object(character, 3)

    land = Land(400, 100)
    game_world.add_object(land, 1)

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass