from pico2d import *

from character import Character

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                boy.state = 1
                boy.dir_x = 1
                boy.speed += 2
            elif event.key == SDLK_LEFT:
                boy.state = 1
                boy.dir_x = 0
                boy.speed -= 2
            elif event.key == SDLK_UP:
                if boy.touch_floor() == True:
                    boy.state = 1
                    boy.dir_y = 5
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                boy.state = 3
                boy.dir_x = 1
                boy.speed -= 2
            elif event.key == SDLK_LEFT:
                boy.state = 3
                boy.dir_x = 0
                boy.speed += 2
            elif event.key == SDLK_UP:
                boy.state = 1
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
    boy.x += boy.speed
    delay(0.03)
# finalization code
close_canvas()