from math import *
from random import *
import ClassSprite
import pygame,sys,time,random,os
from pygame.locals import *
from ClassMusique import *

class Blob:
    """
    Les Objets de la classe Blob représente les goutte d'encre ramassable par le joueur
    Paramètres:
    PosX (float) : Position X du joueur par rapport à la carte
    PosY (float) : Position Y du joueur par rapport à la carte
    spriteGroup (Objet SpriteGroup dans ClassDisplay): SpriteGroup des blobs
    """
    def __init__(self,PosX,PosY,spriteGroup):
        self.x = PosX
        self.y = PosY
        taille = randint(3,5)*0.1
        self.sprite = ClassSprite.Sprite((100000, 10000), spriteGroup, "InkBlob",0, taille,taille)
        
        
    def rafraichissement(self,vitrine,joueur,ListeBlob):
        """

        """
        blob=Musique("Blob.mp3")
        ##############################
        collision = False
        if self.sprite.collidemask(joueur.hitbox.rect,joueur.hitbox.mask,None)[0]:
            collision = True
            ListeBlob.pop(ListeBlob.index(self))
            self.sprite.kill()
            blob.start(0,13)
            del(self)
            joueur.encre +=randint(15,25)
            ######### - Blob
            if joueur.encre > joueur.encreMax:
                joueur.encre = joueur.encreMax

            
            
        
                
    
