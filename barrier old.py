import pygame as pg
from pygame.sprite import Sprite, Group
from random import randint

class Barrier(Sprite):
    color = 125, 125, 125
    black = 0, 0, 0

    def __init__(self, game, rect):
        super().__init__()
        self.screen = game.screen
        self.rect = rect
        self.settings = game.settings
        self.destroyed = False
        self.scale = 1
        
    def hit(self):
        if not self.destroyed:
            if randint(0,5) == 1:
                self.destroyed = True 

    def update(self):
        if self.destroyed:
            self.kill()
        self.draw()
        
    def draw(self): 
        pg.draw.rect(self.screen, Barrier.color, self.rect, 0, 20)
        pg.draw.circle(self.screen, self.settings.bg_color, (self.rect.centerx, self.rect.bottom), self.rect.width/6)


class Barriers:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.create_barriers()
        self.aliens_lasers = game.alien_lasers
        self.ship_lasers = game.ship_lasers

    def create_barriers(self):     
        width = self.settings.screen_width / 10
        height = 2.0 * width / 4.0
        top = self.settings.screen_height - 2.1 * height
        rects = [pg.Rect(x * 2 * width + 1.5 * width, top, width, height) for x in range(4)]   # SP w  3w  5w  7w  SP
        self.barriers = [Barrier(game=self.game, rect=rects[i]) for i in range(4)]

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
        self.create_barriers()

    def update(self):
        self.check_collisions()
        for barrier in self.barriers:  
            barrier.update()
            if barrier.destroyed:
                self.barriers.remove(barrier)

    # def draw(self):
    #     for barrier in self.barriers: barrier.draw()

