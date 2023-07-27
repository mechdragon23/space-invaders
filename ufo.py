from ast import Or
from email.headerregistry import HeaderRegistry
from random import randint
import pygame as pg
from pygame.sprite import Sprite, Group
from laser import Lasers
from timer import Timer


class Ufo(Sprite):
    ufo_images0 = [pg.transform.rotozoom(pg.image.load(f'images/ufo__0{n}.png'), 0, 0.7) for n in range(2)]
    
    ufo_timers = {0 : Timer(image_list=ufo_images0)}  

    ufo_explosion_images = [pg.image.load(f'images/explode{n}.png') for n in range(20)]

    def __init__(self, game, type):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pg.image.load('images/ufo.png')
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x) - 100
        self.sb = game.scoreboard   
        self.dying = self.dead = False                  
        self.timer_normal = Ufo.ufo_timers[0]             
        self.timer_explosion = Timer(image_list=Ufo.ufo_explosion_images, is_loop=False)  
        self.timer = self.timer_normal 
        
    def check_edges(self): 
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right + 100                                
    
    def hit(self):
        if not self.dying:
            self.dying = True 
            self.timer = self.timer_explosion
            self.sb.score += 2000
            self.sb.prep_score()
            
    def hitnt(self):
        if not self.dying:
            self.dying = True 
            self.timer = self.timer_explosion
            
    def update(self): 
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        if not self.dying:
            self.x += 5    #ufo speed!!!!!!!!!!!!!!!!!!
        self.rect.x = self.x
        self.draw()
        
    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)


class Ufos:
    def __init__(self, game): 
        self.model_ufo = Ufo(game=game, type=1)
        self.game = game
        self.sound = game.sound
        self.sb = game.scoreboard
        self.ufos = Group()
        self.ship_lasers = game.ship_lasers.lasers    # a laser Group
        self.ufos_lasers = game.alien_lasers
        self.screen = game.screen
        self.settings = game.settings
        self.shoot_requests = 0
        self.ship = game.ship
        self.create_fleet()
          
    def reset(self):
        self.ufos.empty()
        self.create_fleet()
        
    def create_ufo(self, ufo_number, row_number):
        type = row_number // 2     
        ufo = Ufo(game=self.game, type=type)
        ufo.rect.x = -100
        ufo.rect.y = 10
        self.ufos.add(ufo)   
          
    def create_fleet(self):
         self.create_ufo(0, 0)      
            
    def check_fleet_empty(self):
        if len(self.ufos.sprites()) == 0:
            self.sound.ufo_stop()
            if randint(0,150) == 1:
                self.reset()
                self.sound.ufo_fly() 

    def check_collisions(self):  
        collisions = pg.sprite.groupcollide(self.ufos, self.ship_lasers, False, True)  
        if collisions:
            for ufo in collisions:
                ufo.hit()

    def update(self): 
        self.check_collisions()
        self.check_fleet_empty()
        for ufo in self.ufos.sprites(): 
            if ufo.check_edges():
                    ufo.hitnt()
        for ufo in self.ufos.sprites():
            if ufo.dead:      # set True once the explosion animation has completed
                ufo.remove()
            ufo.update() 
        
    def draw(self): 
        for ufo in self.ufos.sprites(): 
            ufo.draw() 
