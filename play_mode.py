import random

from pico2d import *

import game_clear_mode
import game_over_mode
import game_world
import game_framework
from background import Background
from gate import Gate
from map_ import Map
from moving_floor import Sink_floor, Patrol_floor
from object_locate import *
from character import Character, Die
from floor import Floor
from land import Land
from rifleman import Rifle
from wall import Wall
import server

def handle_events():
    if server.character.state_machine.cur_state == Die:
        game_framework.change_mode(game_over_mode)

    if server.character.game_clear == True:
        game_framework.change_mode(game_clear_mode)

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
    game_world.add_object(server.map, 3)

    # 캐릭터 추가
    server.character = Character()
    game_world.add_object(server.character, 3)

    # 몬스터 추가
    # 라이플
    server.rifles = [Rifle(random.randint(300, 3700), random.randint(200, 1300)) for _ in range(5)]
    game_world.add_objects(server.rifles, 3)

    for rifle in server.rifles:
        game_world.add_collision_pair('fist:rifle', None, rifle)
        game_world.add_collision_pair('rifle:land', rifle, None)
    # 플랫폼 추가
    game_world.add_collision_pair('character:floor', server.character, None)

    server.floors = [Floor(x, y) for x, y in floor_locate[Stage]]
    game_world.add_objects(server.floors, 1)

    for floor in server.floors:
        game_world.add_collision_pair('character:floor', None, floor)
        for rifle in server.rifles:
            game_world.add_collision_pair('rifle:floor', rifle, floor)
    # 움직이는 플랫폼 추가
    # 떨어지는 플랫폼
    game_world.add_collision_pair('character:sink_floor', server.character, None)

    server.sink_floors = [Sink_floor(x, y) for x, y in sink_floor_locate[Stage]]
    game_world.add_objects(server.sink_floors, 1)

    for sink_floor in server.sink_floors:
        game_world.add_collision_pair('character:sink_floor', None, sink_floor)
    # 좌우로 움직이는 플랫폼
    game_world.add_collision_pair('character:patrol_floor', server.character, None)

    server.patrol_floors = [Patrol_floor(x, y, range) for x, y, range in patrol_floor_locate[Stage]]
    game_world.add_objects(server.patrol_floors, 1)

    for patrol_floor in server.patrol_floors:
        game_world.add_collision_pair('character:patrol_floor', None, patrol_floor)
    # 벽 추가
    game_world.add_collision_pair('character:wall', server.character, None)

    walls = [Wall(29, 242 * y, 1) for y in range(7)]
    game_world.add_objects(walls, 1)

    for wall in walls:
        game_world.add_collision_pair('character:wall', None, wall)

    walls = [Wall(3971, 508 + 242 * y, -1) for y in range(5)]
    game_world.add_objects(walls, 1)

    for wall in walls:
        game_world.add_collision_pair('character:wall', None, wall)

    # 땅 추가
    game_world.add_collision_pair('character:land', server.character, None)

    server.lands = [Land(x * 354) for x in range(13)]
    game_world.add_objects(server.lands, 1)

    for land in server.lands:
        game_world.add_collision_pair('character:land', None, land)
        game_world.add_collision_pair('rifle:land', None, land)

    # 배경 추가
    background = Background(Stage)
    game_world.add_object(background, 0)

    # 게이트 추가
    server.gate = Gate(Stage)
    game_world.add_object(server.gate, 1)

    game_world.add_collision_pair('character:gate', server.character, server.gate)


def finish():
    del server.map.BGMs
    game_world.clear()
    pass

def update():
    game_world.update()
    server.character.character_land = False
    server.character.block = 1
    server.character.ex_speed = 0
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass