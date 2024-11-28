from pico2d import *
import game_world
import game_framework
from background import Background
from gate import Gate
from map_ import Map
from object_locate import *
from character import Character
from floor import Floor
from land import Land
from wall import Wall
import server

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.character.handle_event(event)


def init():
    # map 추가
    server.map = Map()
    game_world.add_object(server.map, 0)

    # 캐릭터 추가
    server.character = Character()
    game_world.add_object(server.character, 3)

    # 플랫폼 추가
    game_world.add_collision_pair('character:floor', server.character, None)

    floors = [Floor(x, y) for x, y in floor_locate[Stage]]
    game_world.add_objects(floors, 1)

    for floor in floors:
        game_world.add_collision_pair('character:floor', None, floor)

    # 벽 추가
    game_world.add_collision_pair('character:wall', server.character, None)

    walls = [Wall(x, y, dir) for x, y, dir in wall_locate]
    game_world.add_objects(walls, 1)

    for wall in walls:
        game_world.add_collision_pair('character:wall', None, wall)

    # 땅 추가
    game_world.add_collision_pair('character:land', server.character, None)

    lands = [Land(x * 354) for x in range(13)]
    game_world.add_objects(lands, 1)

    for land in lands:
        game_world.add_collision_pair('character:land', None, land)

    # 배경 추가
    background = Background(Stage)
    game_world.add_object(background, 0)

    # 게이트 추가
    server.gate = Gate(Stage)
    game_world.add_object(server.gate, 1)

    game_world.add_collision_pair('character:gate', server.character, server.gate)


def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    server.character.character_land = False
    server.character.block = 1
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass