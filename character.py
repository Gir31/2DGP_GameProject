import random

from pico2d import load_image, draw_rectangle, get_time, clamp, get_canvas_width, get_canvas_height, load_font, load_wav
import game_framework
import game_over_mode
import game_world
import server
from state_machine import *


def drawing(character, count):
    if character.face_dir == 1:
        character.image.clip_draw(int(character.frame + count) * 124, character.action * 124, 124, 124, character.sx, character.sy - 5)
    elif character.face_dir == -1:
        character.image.clip_composite_draw(int(character.frame + count) * 124, character.action * 124, 124, 124,
                                            0, 'h', character.sx, character.sy - 5, 124, 124)

class Idle:
    @staticmethod
    def enter(character, e):
        if start_event(e):
            character.face_dir = 1
        elif right_down(e) or left_up(e):
            character.face_dir = -1
        elif left_down(e) or right_up(e):
            character.face_dir = 1
        elif a_down(e):
            if character.attack == False:
                character.attack = True
                character.action = 5
                character.frame = 0



        if character.jump == False and character.fall_from_jump == False and character.fall == False and character.attack == False:
            character.landing = False
            character.action = 1
            character.frame = 0

        character.dir = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

        if character.attack == False:
            if character.jump == True:
                if character.frame < 4:
                    character.frame = (character.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5
            elif character.fall_from_jump == True:
                if character.frame < 3:
                    TIME_PER_ACTION = 0.1
                    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
                    character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
                else:
                    character.fall_from_jump = False
                    character.fall = True
                    character.action = 0
                    character.frame = 0
            elif character.fall == True:
                if character.frame < 2:
                    character.frame = (character.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3
            elif character.landing == True:
                if character.frame <= 3:
                    character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
                else:
                    character.landing = False
                    character.state_machine.add_event(('AGAIN', 0))
            else:
                character.frame = (character.frame + 7 * ACTION_PER_TIME * game_framework.frame_time) % 7
        else:
            if not character.fist == None:
                character.frame = character.fist.count = (character.frame + 7 * ACTION_PER_TIME * game_framework.frame_time) % 7
                if character.frame > 6.5:
                    character.action = 1
                    character.frame = 0
                    character.attack = False
                    game_world.remove_object(character.fist)
                    character.fist = None


    @staticmethod
    def draw(character):
        if character.attack == False:
            if character.jump == True:
                drawing(character, 0)
            elif character.fall_from_jump == True:
                drawing(character, 8)
            elif character.fall == True:
                drawing(character, 5)
            elif character.landing == True:
                drawing(character, 12)
            else:
                drawing(character, 0)
        else:
            drawing(character, 4)


class Move:
    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e):
            character.dir, character.face_dir = 1, 1
            if character.attack == True:
                character.attack = False
                if not character.fist == None:
                    game_world.remove_object(character.fist)
                    character.fist = None
        elif left_down(e) or right_up(e):
            character.dir, character.face_dir = -1, -1
            if character.attack == True:
                character.attack = False
                if not character.fist == None:
                    game_world.remove_object(character.fist)
                    character.fist = None
        elif a_down(e):
            if character.attack == False:
                character.attack = True
                character.action = 5
                character.frame = 0

        if character.jump == False and character.fall_from_jump == False and character.fall == False and character.attack == False:
            character.landing = False
            character.action = 9
            character.frame = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        if character.attack == False:
            if character.jump == True:
                if character.frame < 4:
                    character.frame = (character.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5
            elif character.fall_from_jump == True:
                if character.frame < 3:
                    TIME_PER_ACTION = 0.1
                    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
                    character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
                else:
                    character.fall_from_jump = False
                    character.state_machine.add_event(('AGAIN', 0))
                    character.action = 0
                    character.frame = 0
            elif character.fall == True:
                if character.frame < 2:
                    character.frame = (character.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3
            elif character.landing == True:
                if character.frame <= 3:
                    character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
                else:
                    character.landing = False
                    character.state_machine.add_event(('AGAIN', 0))
            else:
                character.frame = (character.frame + 7 * ACTION_PER_TIME * game_framework.frame_time) % 8
                if get_time() - character.walk_time > 0.3:
                    character.walk_sound.play()
                    character.walk_time = get_time()
        else:
            if not character.fist == None:
                character.frame = character.fist.count = (character.frame + 7 * ACTION_PER_TIME * game_framework.frame_time) % 7
                if character.frame > 6.5:
                    character.action = 1
                    character.frame = 0
                    character.attack = False
                    game_world.remove_object(character.fist)
                    character.fist = None

    @staticmethod
    def draw(character):
        if character.attack == False:
            if character.jump == True:
                drawing(character, 0)
            elif character.fall_from_jump == True:
                drawing(character, 8)
            elif character.fall == True:
                drawing(character, 5)
            elif character.landing == True:
                drawing(character, 12)
            else:
                drawing(character, 1)
        else:
            drawing(character, 4)

class Die:
    @staticmethod
    def enter(character, e):
        character.frame = 0
        character.action = 7

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        TIME_PER_ACTION = 1
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

        if character.frame < 3.5 and character.action == 7:
            character.frame = (character.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
        else:
            character.action = 9
            character.frame = 0

    @staticmethod
    def draw(character):

        if character.action == 7:
            if character.face_dir == 1:
                character.image.clip_draw(int(character.frame) * 124, character.action * 124, 124, 124,
                                          character.x, character.y - 5)
            elif character.face_dir == -1:
                character.image.clip_composite_draw(int(character.frame) * 124, character.action * 124, 124,
                                                    124, 0, 'h', character.x, character.y - 5, 124, 124)
        else:
            if character.face_dir == 1:
                character.image.clip_draw(int(character.frame + 9) * 124, character.action * 124, 124, 124,
                                          character.x, character.y - 5)
            elif character.face_dir == -1:
                character.image.clip_composite_draw(int(character.frame + 9) * 124, character.action * 124, 124,
                                                    124, 0, 'h', character.x, character.y - 5, 124, 124)

class Fist:
    attack_air_sound = None
    attack_rifle_sound = None

    def __init__(self, x, y, dir):
        self.x, self.y, self.dir = x, y, dir
        self.damage = 3
        self.attack_flag = False
        self.hit_flag = False
        self.count = 0

        if not Fist.attack_air_sound:
            Fist.attack_air_sound = load_wav("resource/character/attack_air.wav")
            Fist.attack_air_sound.set_volume(50)
            Fist.attack_rifle_sound = load_wav("resource/character/attack_rifle.wav")
            Fist.attack_rifle_sound.set_volume(50)

    def draw(self):
        pass


    def update(self):
        if int(self.count) == 0 or int(self.count) == 4:
            if self.attack_flag == False:
                self.damage = 3
                self.attack_flag = True
                if self.hit_flag == True:
                    self.attack_rifle_sound.play()
                    self.hit_flag = False
                else:
                    self.attack_air_sound.play()
                    self.hit_flag = False
            else:
                self.damage = 0
        else:
            self.damage = 0
            self.attack_flag = False

    def get_bb(self):
        if self.dir == 1:
            return self.x + 15, self.y - 20, self.x + 60, self.y + 10
        elif self.dir == -1:
            return self.x - 60, self.y - 20, self.x - 15, self.y + 10

    def handle_collision(self, group, other):
        match group:
            case 'fist:rifle':
                self.hit_flag = True



class Character:

    def __init__(self):
        self.x, self.y = 100, 132
        self.sx, self.sy = get_canvas_width() / 2, get_canvas_height() / 2
        self.hp = 100
        self.damage, self.damage_time = False, 0
        self.recovery, self.recovery_time, self.recovery_amount = False, 0, 5
        self.font = load_font('resource/ENCR10B.TTF',32)
        self.ex_speed = 0
        self.dir = 0
        self.face_dir = 1
        self.block = 1
        self.character_land = True
        self.jump = False
        self.jump_time = 0
        self.fall_from_jump = False
        self.fall = False
        self.landing = False
        self.attack = False
        self.fist = None
        self.land_flag, self.walk_time = False, 0
        self.image = load_image("resource/character/character.png")
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down : Move, left_down : Move, right_up : Move, left_up : Move, again_action : Idle, a_down : Idle, character_die : Die},
                Move: {right_down : Idle, left_down : Idle, right_up : Idle, left_up : Idle, again_action : Move, a_down : Move, character_die : Die},
                Die : {}
            }
        )

        self.x = clamp(25.0, self.x, server.map.w - 25.0)
        self.y = clamp(66.0, self.y, server.map.h - 66.0)

        self.land_sound = load_wav("resource/character/land.wav")
        self.land_sound.set_volume(32)
        self.walk_sound = load_wav("resource/character/walk.wav")
        self.walk_sound.set_volume(50)
        self.jump_sound = load_wav("resource/character/jump.wav")
        self.jump_sound.set_volume(32)
        self.damaged_sound = load_wav("resource/character/damaged.wav")
        self.damaged_sound.set_volume(50)

        self.game_clear = False

    def update(self):
        self.state_machine.update()

        PIXEL_PER_METER = (10.0 / 0.2)

        FALL_SPEED_KMPH = 80
        FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
        FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
        FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)

        GRAVITY = FALL_SPEED_PPS * game_framework.frame_time * -1
        self.land_flag = True

        if self.character_land == True:
            GRAVITY = 0
            self.land_flag = False

        if self.jump == True:
            JUMP_SPEED_KMPH = 120
            JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
            JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
            JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

            GRAVITY = JUMP_SPEED_PPS * game_framework.frame_time
            if get_time() - self.jump_time > 0.2:
                self.jump = 0
                self.jump = False
                self.fall_from_jump = True
                self.action = 0
                self.frame = 0

        RUN_SPEED_KMPH = 60
        RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

        self.x += (self.dir * RUN_SPEED_PPS * game_framework.frame_time * self.block) + self.ex_speed

        self.y += GRAVITY

        self.x = clamp(25.0, self.x, server.map.w - 25.0)
        self.y = clamp(66.0, self.y, server.map.h - 66.0)

        if self.hp < 100 and self.damage == False:
            self.recovery = True
            if get_time() - self.recovery_time > 1:
                self.hp += self.recovery_amount
                self.recovery_time = get_time()
        elif self.hp == 100:
             if get_time() - self.recovery_time > 5:
                self.recovery_time = get_time()
                self.recovery = False

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                if self.character_land == True:
                    self.jump_sound.play()
                    self.jump = True
                    self.jump_time = get_time()
                    self.frame = 0
                    self.action = 0
            if event.key == SDLK_a:
                if self.fist == None:
                    self.fist = Fist(self.x, self.y, self.face_dir)
                    game_world.add_object(self.fist)
                else:
                    game_world.remove_object(self.fist)
                    self.fist = Fist(self.x, self.y, self.face_dir)
                    game_world.add_object(self.fist)
                self.land_flag = True
                game_world.add_collision_pair('fist:rifle', self.fist, None)

        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.sx, self.sy = self.x - server.map.window_left, self.y - server.map.window_bottom

        self.state_machine.draw()
        if self.damage == True:
            self.font.draw(self.sx - 100, self.sy + 75, f'{self.hp:02d}', (255, 0, 0))
            if get_time() - self.damage_time > 3:
                self.damage, self.damage_time = False, 0

        if self.recovery == True and self.damage == False:
            self.font.draw(self.sx - 100, self.sy + 75, f'{self.hp:02d}', (0, 255, 255))
            if self.hp > 100:
                self.hp = 100

    def get_bb(self):
        return self.x - 25, self.y - 66, self.x + 25, self.y + 50

    def handle_collision(self, group, other):
        match group:
            case 'character:floor':
                minX_o, minY_o, maxX_o, maxY_o = other.get_bb()
                minX_c, minY_c, maxX_c, maxY_c = self.get_bb()

                if minY_o < minY_c:
                    self.character_land = True
                    if self.fall == True:
                        self.land_sound.play()
                        self.fall = False
                        self.landing = True
                        self.action = 9
                        self.frame = 0
            case 'character:sink_floor':
                if other.show == True:
                    minX_o, minY_o, maxX_o, maxY_o = other.get_bb()
                    minX_c, minY_c, maxX_c, maxY_c = self.get_bb()

                    if minY_o < minY_c:
                        self.character_land = True
                        if self.fall == True:
                            self.land_sound.play()
                            self.fall = False
                            self.landing = True
                            self.action = 9
                            self.frame = 0
            case 'character:patrol_floor':
                minX_o, minY_o, maxX_o, maxY_o = other.get_bb()
                minX_c, minY_c, maxX_c, maxY_c = self.get_bb()

                if minY_o < minY_c:
                    self.character_land = True
                    self.ex_speed = other.speed
                    if self.fall == True:
                        self.land_sound.play()
                        self.fall = False
                        self.landing = True
                        self.action = 9
                        self.frame = 0

            case 'character:land':
                minX_o, minY_o, maxX_o, maxY_o = other.get_bb()
                minX_c, minY_c, maxX_c, maxY_c = self.get_bb()

                if minY_o < minY_c:
                    self.character_land = True
                    gap = maxY_o - minY_c
                    self.y = self.y + gap - 1
                    if self.fall == True:
                        self.land_sound.play()
                        self.fall = False
                        self.landing = True
                        self.action = 9
                        self.frame = 0
            case 'character:wall':
                PIXEL_PER_METER = (10.0 / 0.2)
                RUN_SPEED_KMPH = 60
                RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
                RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
                RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

                self.x -= self.dir * RUN_SPEED_PPS * game_framework.frame_time * self.block
                self.block = 0
            case 'character:gate':
                match other.state:
                    case 'closed':
                        PIXEL_PER_METER = (10.0 / 0.2)
                        RUN_SPEED_KMPH = 60
                        RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
                        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
                        RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

                        self.x -= self.dir * RUN_SPEED_PPS * game_framework.frame_time * self.block
                        self.block = 0
                    case 'closing':
                        PIXEL_PER_METER = (10.0 / 0.2)
                        RUN_SPEED_KMPH = 60
                        RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
                        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
                        RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

                        self.x -= self.dir * RUN_SPEED_PPS * game_framework.frame_time * self.block
                        self.block = 0
                    case 'opening':
                        self.game_clear = True
            case 'character:bullet':
                self.hp -= random.randint(8, 20)
                self.damage, self.damage_time = True, get_time()
                self.recovery_time, self.recovery = get_time(), False
                self.damaged_sound.play()
                if self.hp <= 0:
                    self.state_machine.add_event(('DIE', 0))





