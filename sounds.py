import pygame.mixer
import simpleaudio as sa
import os 
import time
import random


pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()

class Speaker():

    def __init__(self, b):
        self.musicChannel = pygame.mixer.Channel(1)
        self.sfxChannel = pygame.mixer.Channel(2)
        self.ambientChannel = pygame.mixer.Channel(3)
        self.windChannel = pygame.mixer.Channel(4)
        self.thunderChannel = pygame.mixer.Channel(5)
        if b:
            self.menumusic = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "music" , "menuTheme.ogg"))
            self.musicChannel.play(self.menumusic)
        else:
            self.s = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "music" , "s.ogg"))
            self.deletesound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "soundfx" , "delete.ogg"))
            self.a = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "music" , "a.ogg"))
            self.chaos = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "music" , "Pending.ogg"))
            self.bbxs = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "music" , "menuTheme.ogg"))
            self.dune = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "music" , "Dune.ogg"))
            self.rainsfx = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "soundfx" , "rain.ogg"))
            self.thundersfx = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "soundfx" , "thunder.mp3"))
            self.thunder2sfx = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "soundfx" , "thunder2.mp3"))
            self.thunder3sfx = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "soundfx" , "thunder3.mp3"))
            self.windsfx = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "soundfx" , "wind.mp3"))
            self.snowsfx = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds" , "soundfx" , "fallingSnow.mp3"))
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

    def rainsound(self, duration):
        self.ambientChannel.play(self.rainsfx)

    def snowSound(self, duration):
        self.ambientChannel.play(self.snowsfx, int(duration/30))

    def thunderSound(self):
        r = random.randint(1,3)
        if r == 1:
            pygame.mixer.find_channel().play(self.thundersfx)
        elif r == 2:
            pygame.mixer.find_channel().play(self.thunder2sfx)
        else:
            pygame.mixer.find_channel().play(self.thunder3sfx)

    def windSound(self, loundness):
        self.windChannel.set_volume(loundness)
        self.windChannel.play(self.windsfx)

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
    
    def stopAmbients(self):
        self.ambientChannel.fadeout(6)
        self.ambientChannel.fadeout(6)
        #self.ambientChannel.stop()