from pico2d import *

from character import Character

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            boy.handle_event(event)

def reset_world():
    global running
    global world
    global boy

    running = True
    world = []

    boy = Character()
    world.append(boy)

def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas()
reset_world()
# game loop
while running:
    update_world()
    render_world()
    handle_events()
    delay(0.01)
# finalization code
close_canvas()