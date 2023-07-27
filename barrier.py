import pygame as pg
from pygame.sprite import Sprite, Group
from random import randint
from timer import Timer

class Barrier(Sprite):
    color = 125, 125, 125
    black = 0, 0, 0
    barrier_images0 = [pg.transform.rotozoom(pg.image.load(f'images/barrier__0{n}.png'), 0, 0.7) for n in range(2)]
    barrier_images1 = [pg.transform.rotozoom(pg.image.load(f'images/barrier__1{n}.png'), 0, 0.7) for n in range(2)]
    barrier_images2 = [pg.transform.rotozoom(pg.image.load(f'images/barrier__2{n}.png'), 0, 0.7) for n in range(2)]
    barrier_images3 = [pg.transform.rotozoom(pg.image.load(f'images/barrier__3{n}.png'), 0, 0.7) for n in range(2)]
    
    barrier_timers = {0 : Timer(image_list=barrier_images0), 
                      1 : Timer(image_list=barrier_images1), 
                      2 : Timer(image_list=barrier_images2),
                      3 : Timer(image_list=barrier_images3)} 

    def __init__(self, game, type):
        super().__init__()
        self.screen = game.screen
        self.image = pg.image.load('images/barrier.png')
        self.rect = self.image.get_rect()
        self.rect.width -= 60
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type
        self.settings = game.settings
        self.destroyed = False
        self.hp = 0
        self.scale = 1
        self.timer_normal = Barrier.barrier_timers[type]
        self.timer = self.timer_normal  
        
    def hit(self):
        if not self.destroyed:
            self.type += 1
            if self.type < 4:
                self.timer = Barrier.barrier_timers[self.type]
        if self.type > 3:
            self.destroyed = True 

    def update(self):
        if self.destroyed:
            self.kill()
        self.draw()
        
    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)


class Barriers:
    def __init__(self, game):
        self.model_barrier = Barrier(game=game, type=1)
        self.game = game
        self.barriers = Group()
        self.settings = game.settings
        self.create_barriers()
        self.aliens_lasers = game.alien_lasers
        self.ship_lasers = game.ship_lasers
        
    def create_barrier(self, type, num):
        barrier = Barrier(game=self.game, type=type)
        barrier.x = 100 + 285 * num
        barrier.rect.x = barrier.x
        barrier.rect.y = 680
        self.barriers.add(barrier) 

    def create_barriers(self):
        for num in range(4):     
            type = 0
            self.create_barrier(type, num)

    def check_collisions(self): 
        collisions = pg.sprite.groupcollide(self.barriers, self.aliens_lasers.lasers, False, True)
        if collisions:
            for barrier in collisions:
                barrier.hit()
        
        collisions = pg.sprite.groupcollide(self.barriers, self.ship_lasers.lasers, False, True)
        if collisions:
            for barrier in collisions:
                barrier.hit()
    
    def reset(self):
        self.barriers.empty()
        self.create_barriers()

    def update(self):
        self.check_collisions()
        for barrier in self.barriers:  
            barrier.update()
            if barrier.destroyed:
                self.barriers.remove(barrier)

    def draw(self): 
        for barrier in self.barriers.sprites(): 
            barrier.draw() 

