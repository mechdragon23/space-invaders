from tkinter.tix import ButtonBox
import pygame as pg
from settings import Settings
import game_functions as gf
import random

from laser import Lasers, LaserType
from alien import Aliens
from ufo import Ufos
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from barrier import Barriers
import sys

class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.scoreboard = Scoreboard(game=self)  

        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        
        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)
        self.ufos = Ufos(game=self)
        self.settings.initialize_speed_settings()
        self.updated = False

    def reset(self):
        print('Resetting game...')
        self.barriers.reset()
        self.ship.reset()
        self.aliens.reset()
        self.ufos.reset()
        self.updated = False
        self.sound.ufo_stop()

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.ufo_stop()
        self.sound.gameover()
        self.scoreboard.reset()
        self.ufos.reset()
        pg.quit()
        main()

    def play(self):
        self.sound.play_bg()
        self.updated = False
        bgg = pg.image.load("images/bgg.png") #loads background image for game
        while True:     # at the moment, only exits in gf.check_events if Ctrl/Cmd-Q pressed
            gf.check_events(settings=self.settings, ship=self.ship)
            self.screen.blit(bgg, (0, 0))
            self.ship.update()
            self.aliens.update()
            if random.randint(0,150) == 1 or self.updated:
                if not self.updated:
                    self.sound.ufo_fly()
                self.ufos.update()
                self.updated = True              
            self.barriers.update()
            self.scoreboard.update()
            pg.display.flip()


def main():
    pg.init() 
    res = (1200,800) 
    screen = pg.display.set_mode(res)
    bg = pg.image.load("images/bg.png")        
    
    color = (255,255,255) 
    
    color_light = (63,129,220) #color of play button when hovering over it
    color_dark = (9,57,123)  #color of play button when not hovering over it
    
    width = screen.get_width()  
    height = screen.get_height()
    
    buttonwidth = 200
    buttonheight = 40  
    buttonx = width/2 - buttonwidth/2
    buttony = height/2 + 230
    
    f = open("highscores.txt", "r+")
    high_score = f.readline()
    f.close()

    smallfont = pg.font.SysFont('Corbel',40) 
    text = smallfont.render('PLAY' , True , color)
    high = smallfont.render(high_score, True, color)
    high2= smallfont.render('high score: ', True, color) 
    
    while True: 
        for ev in pg.event.get():      
            if ev.type == pg.QUIT: 
                pg.quit() 
            #checks if a mouse is clicked 
            if ev.type == pg.MOUSEBUTTONDOWN: 
                #if the mouse is clicked on the 
                # button the game is terminated 
                if buttonx <= mouse[0] <= buttonx+buttonwidth and buttony <= mouse[1] <= buttony+buttonheight: 
                    g = Game()
                    g.play() 
        # fills the screen with a color 
        screen.blit(bg, (0, 0))
        
        mouse = pg.mouse.get_pos() 
        # if mouse is hovered on a button it 
        # changes to lighter shade 
        if buttonx <= mouse[0] <= buttonx+buttonwidth and buttony <= mouse[1] <= buttony+buttonheight: 
            pg.draw.rect(screen,color_light,[buttonx,buttony,buttonwidth,buttonheight]) 
            
        else: 
            pg.draw.rect(screen,color_dark,[buttonx,buttony,buttonwidth,buttonheight]) 
        
        # superimposing the text onto our button 
        screen.blit(text , (buttonx + 60,buttony + 4))
        screen.blit(high , (buttonx + 160,buttony + 70))
        screen.blit(high2 , (buttonx - 40,buttony + 70))  
        
        # updates the frames of the game 
        pg.display.update()


if __name__ == '__main__':
    main()
