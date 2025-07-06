from sprite_source import *

from enum import Enum

import pgzrun
import random
from pgzero.builtins import Actor, keyboard
from pygame import Rect


WIDTH = 800
HEIGHT = 800
TITLE = "KEEP THE TREE"
FPS = 60

# Time since game started
game_timer = 0.0

# registering every character to animate them
enemy_list = []

class HeroAnimationState(Enum):
    LEFT = 4
    RIGHT = 6
    IDLE = 5

class EnemyAnimationState(Enum):
    WALK_LEFT = 4
    WALK_RIGHT = 6
    ATTACK_LEFT = 7
    ATTACK_RIGHT = 9
    DIE = 0


class Character(Actor):
    def __init__(self, pos: tuple, left_walking_sprites):
        super().__init__(left_walking_sprites[0], pos)

    
    def translate(self, x_speed:int, y_speed:int):
        self.x += x_speed
        self.y += y_speed



class Hero(Character):
    def __init__(self, idle_anim_sprites, left_walking_sprites, right_walking_sprites):
        super().__init__((WIDTH // 2 , HEIGHT // 2 + 50), left_walking_sprites)
        self.animationState = HeroAnimationState.IDLE
        self.animationIndex = 0
        self.weapons_activated = {
        "blade": True,
        "book": False
        }
        self.hero_idle_sprites = idle_anim_sprites
        self.left_walking_sprites = left_walking_sprites

    def animation_controller(self):
        if self.x >= 0:
            self.animationState = HeroAnimationState.RIGHT
        elif self.x < 0:
            self.animationState = HeroAnimationState.LEFT
        else:
            self.animationState = HeroAnimationState.IDLE

    def animate(self, dt):
        animation_change_timeout = 0.2
        animation_timer = animation_change_timeout

        animation_timer -= dt
        if animation_timer <= 0.0:
            animation_timer = animation_change_timeout
            hero_animation_index += 1

        if self.animationState == HeroAnimationState.IDLE:
            self.image = self.hero_idle_sprites[self.animationIndex % len(self.hero_idle_sprites)]

        if self.animationState == HeroAnimationState.RIGHT:
            self.image = self.hero_walk_right_sprites[self.animationIndex % len(self.hero_walk_right_sprites)]

        if self.animationState == HeroAnimationState.LEFT:
            self.image = self.left_walking_sprites[self.animationIndex % len(self.left_walking_sprites)]



class Enemy(Character):
    def __init__(self, pos, target, left_walking_sprites, right_walking_sprites, left_attack_sprites, right_attack_sprites, die_sprites):
        super().__init__(pos, left_walking_sprites)
        self.animationState = EnemyAnimationState.WALK_LEFT
        self.animationIndex = 0
        self.target = target
        self.left_walking_sprites = left_walking_sprites
        self.right_walking_sprites = right_walking_sprites
        self.left_attack_sprites = left_attack_sprites
        self.right_attack_sprites = right_attack_sprites
        self.die_sprites = die_sprites

    def get_dir_to_hero(self):
        dir_to_hero = {"x": 0, "y": 0}
        if hero.x <= self.x:
            dir_to_hero["x"] = -1
        else:
            dir_to_hero["x"] = 1
        if hero.y <= self.y:
            dir_to_hero["x"] = -1
        else:
            dir_to_hero["y"] = 1
        return dir_to_hero


    def move_to_target(self):
        movement_vector = self.get_dir_to_hero()


    def animation_controller(self):
        if self.x >= 0:
            self.animationState = EnemyAnimationState.RIGHT
        elif self.x < 0:
            self.animationState = EnemyAnimationState.LEFT
        else:
            self.animationState = EnemyAnimationState.IDLE

    def animate(self, dt):
        animation_change_timeout = 0.2
        animation_timer = animation_change_timeout

        animation_timer -= dt
        if animation_timer <= 0.0:
            animation_timer = animation_change_timeout
            hero_animation_index += 1

        if self.animationState == EnemyAnimationState.WALK_LEFT:
            self.image = self.left_walking_sprites[self.animationIndex % len(self.left_walking_sprites)]

        if self.animationState == EnemyAnimationState.WALK_RIGHT:
            self.image = self.right_walking_sprites[self.animationIndex % len(self.right_walking_sprites)]

        if self.animationState == EnemyAnimationState.ATTACK_LEFT:
            self.image = self.left_attack_sprites[self.animationIndex % len(self.left_attack_sprites)]

        if self.animationState == EnemyAnimationState.ATTACK_RIGHT:
            self.image = self.right_attack_sprites[self.animationIndex % len(self.right_attack_sprites)]
        
        if self.animationState == EnemyAnimationState.DIE:
            self.image = self.die_sprites[self.animationIndex % len(self.die_sprites)]

class Weapon(Actor):
    def __init__(self, hero:Character, sprite, ui, interval: float, damage: int):
        super().__init__(sprite, (hero.x + 10, hero.y + 10))
        self.hero = hero
        self.interval = interval,
        self.ui_image = ui
        self.damage = damage

    def set_damage(self, increase_amount: int):
        self.damage += increase_amount
        return self.damage
    
    def get_damage(self):
        return self.damage
    
class EnemySpawner:
    def __init__(self, enemy_class_list:tuple, game_timer):
        self.enemy_list = enemy_list
    
    def spawn_enemy(self):
        chosen_enemy = random.choice(self.enemy_list)
        random_x = random.choice((random.randint(-50, -20), random.randint(WIDTH + 4, WIDTH + 20)))
        random_y = random.choice((random.randint(-50, -20), random.randint(HEIGHT + 4, HEIGHT + 20)))
        new_enemy = chosen_enemy()
    



tree_health = 50


hero = Hero(hero_idle_sprites, hero_walk_left_sprites, hero_walk_right_sprites)
tree = Actor("tree", (WIDTH // 2, HEIGHT // 2))

# Weapons
book = Weapon(hero, "book", "book_ui", 3, 2)
blade = Weapon(hero, "blade", "blade_ui", 1, 2)


# Weapons UI
book_ui = Actor("book_ui", (WIDTH - 20, 40))
blade_ui = Actor("blade_ui", (WIDTH - 20, 20))

def get_input():
    movement_vector = {"x": 0, "y": 0}
    moving = False
    if keyboard.left:
        movement_vector["x"] -= 1
    if keyboard.right:
        movement_vector["x"] += 1
    if keyboard.up:
        movement_vector["y"] -= 1
    if keyboard.down:
        movement_vector["y"] += 1
    hero.translate(movement_vector["x"], movement_vector["y"])

def draw_ui():
    if hero.weapons_activated["blade"]:
        blade_ui.draw()
    if hero.weapons_activated["book"]:
        book_ui.draw()

def animate_scene_elements(dt):
    for enemy in enemy_list:
        enemy.animate(dt)
    hero.animate(dt)
    


def draw():
    screen.clear()
    screen.fill("white")
    tree.draw()
    hero.draw()
    draw_ui()

def update(dt):
    global game_timer
    game_timer += dt
    animate_scene_elements(dt)
    get_input()


pgzrun.go()