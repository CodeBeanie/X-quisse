from math import *
from random import *
import ClassSprite
import pygame,sys,time,random,os
from pygame.locals import *


class Coeur:
    """
    Les Objets de la classe Blob représente les goutte d'encre ramassable par le joueur
    Paramètres:
    indexe (int) : Position du coeur dans la liste ListeCoeur (le zero est le plus à gauche)
    joueur (Objet Personnage dans ClassObjet SpriteGroup dans ClassDisplay) : joueur
    Groupe (Objet SpriteGroup dans ClassDisplay): SpriteGroup des Coeur
    """
    def __init__(self,indexe,Groupe,joueur):
        self.estRemplie = True
        self.estArmure = indexe+1 > joueur.pvMax
        self.indexe = indexe # Combientième coeur
        self.posX = 100 + self.indexe * 70
        self.posY = 40
        self.sprite = ClassSprite.Sprite((self.posX ,self.posY),Groupe,"Coeur",0,0.5,0.5)
        
    def rafraichir(self,joueur):
        self.estRemplie= joueur.pv >= self.indexe+1
        self.estArmure = self.indexe+1 > joueur.pvMax
        if self.estRemplie:
            self.sprite.animate("","Coeur",False)
        else:
            self.sprite.animate("","CoeurVide",False)
            
        if self.estArmure:
            if self.indexe+1> joueur.pvMax + joueur.armure:
                self.sprite.kill()
                return (True,self)
            else:
                
                self.sprite.animate("","CoeurArmure",False)
        
        return(False,None)
                
    