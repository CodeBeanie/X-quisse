#crée par Léane
import pygame,sys,time,random,os
import pygame,sys
from pygame.locals import *

class Musique:
    def __init__(self,fichier):
        """
        fichier: nom du fichier d'un son
        """

        pygame.mixer.init()
        pygame.mixer.set_num_channels(20)
        self.nomfichier=os.path.join("Son", fichier)
        self.son = pygame.mixer.Sound(self.nomfichier)
        pygame.mixer.music.load(self.nomfichier)

    def start(self,repetition,channel,volume=1):
        """
        repetition: nombre de répétition du son, avec -1 pour répéter indéfiniment
        channel: permet de joueur plusieurs sons en même temps
        """
        self.channel=channel
        if pygame.mixer.Channel(channel).get_sound() == None:
            print(self.nomfichier)
            pygame.mixer.Channel(channel).play(pygame.mixer.Sound(self.nomfichier),repetition)
            pygame.mixer.Channel(channel).set_volume(volume)
            return True
        else:
            return False

    def stop(self):
        pygame.mixer.Channel(self.channel).stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()