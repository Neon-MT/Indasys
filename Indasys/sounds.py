import pygame.mixer
from audioplayer import AudioPlayer
import simpleaudio as sa
import os 
import random


pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()

class Speaker():

    def __init__(self, b):
        self.musicChannel = pygame.mixer.Channel(1)
        self.sfxChannel = pygame.mixer.Channel(2)
        self.ambientChannel = pygame.mixer.Channel(3)
        if b:
            self.menumusic = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "music" , "BeepBox-Song.ogg"))
            self.musicChannel.play(self.menumusic)
        else:
            self.s = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "music" , "s.ogg"))
            self.deletesound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "soundfx" , "delete.ogg"))
            self.a = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "music" , "hahhhh.ogg"))
            self.chaos = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "music" , "Chaotic ahh.ogg"))
            self.bbxs = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "music" , "BeepBox-Song.ogg"))
            self.dune = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "music" , "Dune.ogg"))
            self.rainsfx = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "soundfx" , "rain.ogg"))
            # self.place = sa.WaveObject.from_wave_file(os.path.join(os.path.dirname(__file__), "sounds" , "soundfx" , "place.wav"))
            self.playingsound = False
            self.frame = 0

    def update(self, biome):
        if not self.playingsound:
            self.frame += 1

        rand = self.getRand()

        if rand <= self.frame:
            self.playingsound = True
            if biome == 0:
                self.musicChannel.play(self.a)
                self.frame = 0
            if biome == 1:
                self.musicChannel.play(self.s)
                self.frame = 0
            if biome == 2:
                self.musicChannel.play(self.dune)
                self.frame = 0

        if not self.musicChannel.get_busy():
            self.playingsound = False



    def getRand(self):
        return random.randint(200,1000)

    def delSound(self):
        self.sfxChannel.play(self.deletesound)

    def rainsound(self):
        self.ambientChannel.play(self.rainsfx)

    def pauseAll(self):
        self.musicChannel.pause()
        self.sfxChannel.pause()
        self.ambientChannel.pause()

    def unpauseAll(self):
        self.musicChannel.unpause()
        self.sfxChannel.unpause()
        self.ambientChannel.unpause()

    def stopMusic(self):
        self.musicChannel.stop()