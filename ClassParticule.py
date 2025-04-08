from math import *
from random import *
import ClassSprite
import pygame,sys,time,random,os
from pygame.locals import *


class Particule:
    """
    Les Objets de la classe Particule représente les particules
    Paramètres:
    Pos (tuple(float,float)) : Position du joueur par rapport à la carte
    Type (string) : indique quelle particule
    spriteGroup (Objet SpriteGroup dans ClassDisplay): SpriteGroup des particules
    Image (str) : le nom de fichier de l'image
    scale (float) : taille du sprite (1 par défault)
    """
    def __init__(self,Pos,Type,spriteGroup,Image,scale):
        self.x = Pos[0]
        self.y= Pos[1]
        self.yOriginal = Pos[1] + randint(-30,20)
        self.vitesseX = Pos[2]
        self.vitesseY = Pos[3]
        self.type = "encre"
        self.tempsDeVie = 3000
        self.sprite = ClassSprite.Sprite((100000, 10000), spriteGroup, Image,0, scale,scale)
        
        
    def rafraichissement(self,vitrine,multiplicateurFPS):
        """

        """
        ##############################
        self.tempsDeVie -= vitrine.clock.get_time()
        if self.type == "encre":
            self.x += self.vitesseX
            self.y += self.vitesseY
            self.vitesseX = self.vitesseX*0.95
            self.vitesseY += 1

            if self.y > self.yOriginal:
                self.sprite.kill()
                return self

            
        
                
    