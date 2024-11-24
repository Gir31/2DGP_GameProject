from pico2d import *
import game_world
import game_framework
from background import Background
from gate import Gate
from object_locate import *
from character import Character
from floor import Floor
from land import Land
from wall import Wall

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

    game_world.add_collision_pair('character:floor', character, None)

    floors = [Floor(x, y) for x, y in floor_locate[Stage]]
    game_world.add_objects(floors, 1)

    for floor in floors:
        game_world.add_collision_pair('character:floor', None, floor)

    game_world.add_collision_pair('character:wall', character, None)

    walls = [Wall(x, y, dir) for x, y, dir in wall_locate]
    game_world.add_objects(walls, 1)

    game_world.add_collision_pair('character:land', character, None)

    lands = [Land(x * 354) for x in range(5)]
    game_world.add_objects(lands, 1)

    for land in lands:
        game_world.add_collision_pair('character:land', None, land)

    background = Background(Stage)
    game_world.add_object(background, 0)

    gate = Gate(Stage)
    game_world.add_object(gate, 1)






def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    character.character_land = False
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass