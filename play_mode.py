from pico2d import *
import game_world
import game_framework
from floor_locate import *
from character import Character
from grass import Grass
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
    global floors

    character = Character()
    game_world.add_object(character, 3)

    game_world.add_collision_pair('character:floor', character, None)

    floors = [Land(x, y) for x, y in floor_locate[Stage]]
    game_world.add_objects(floors, 1)

    for floor in floors:
        game_world.add_collision_pair('character:floor', None, floor)

    game_world.add_collision_pair('character:land', character, None)
    grass = Grass()
    game_world.add_object(grass, 0)
    game_world.add_collision_pair('character:land', None, grass)




def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass