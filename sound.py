import pygame as pg
from laser import LaserType
import time


class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.3)
        alienlaser_sound = pg.mixer.Sound('sounds/alienlaser.wav')
        photontorpedo_sound = pg.mixer.Sound('sounds/photon_torpedo.wav')
        gameover_sound = pg.mixer.Sound('sounds/gameover.wav')
        ufo_sound = pg.mixer.Sound('sounds/ufo.wav')
        self.sounds = {'alienlaser': alienlaser_sound, 'photontorpedo': photontorpedo_sound,
                       'gameover': gameover_sound, 'ufo': ufo_sound}

    def play_bg(self):
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        pg.mixer.music.stop()

    def shoot_laser(self, type): 
        pg.mixer.Sound.play(self.sounds['alienlaser' if type == LaserType.ALIEN else 'photontorpedo'])
    
    def ufo_fly(self):
        pg.mixer.Sound.play(self.sounds['ufo'])
        
    def ufo_stop(self):
        pg.mixer.Sound.stop(self.sounds['ufo'])
        
    def gameover(self): 
        self.stop_bg() 
        pg.mixer.music.load('sounds/gameover.wav')
        self.play_bg()
        time.sleep(2.8)
