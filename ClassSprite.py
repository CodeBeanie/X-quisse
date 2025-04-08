import pygame,sys,time,random,os
from pygame.locals import *
from math import *
from random import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self,startingpos,spritegroupe,Image,vitesse,scaleX,scaleY):
        '''
        le class Sprite prend comme parametres:
        
        startingpos:tuple (x,y)
        le position initial du sprite
        
        spritegroupe:Objet pygame
        Il faut creer un sprite group avant de creer le sprite qui se fait en dehors de ce class
        Par exemple ceci ce fait en 2 lignes:
        exempleSpriteGroup=pygame.sprite.Group()
        exempleFenetre.addsprite(exempleSpriteGroup)
        il faut apres mettre le sprite group cree comme parametre ici,si on suit l'example,il faut mettre exempleSpriteGroup
        ATTENTION:Il faut creer un class Fenetre avant de creer le sprite
        
        Image:string
        ATTENTION:faut etre un image .png
        ATTENTION:faut avoir un directoire 'Images' avec ces images dedans
        Image est un string qui contient le nom du fichier sans le '.png'
        
        vitesse:Int
        Un variable just pour stocker le vitesse du sprite,Aussi utilise pour le debug methode:'update'
        
        scale:Int
        Un parametre pour changer la taille de l'image par multiplication
        ATTENTION:Cette sprite/image serai TOUJOURS multiplie par cette valeur,meme dans la methode:'animate'
        
        '''
        super().__init__()
        self.image = pygame.image.load(os.path.join("Images", Image+".png"))
        originale_largeur, originale_hauteur = self.image.get_size()
        echelle_largeur = int(originale_largeur * scaleX)
        echelle_hauteur = int(originale_hauteur * scaleY)
        self.image = pygame.transform.scale(self.image, (echelle_largeur, echelle_hauteur))
        self.scaleX=scaleX
        self.scaleY=scaleY
        self.rect = self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
        self.rect.center = (startingpos[0], startingpos[1])
        self.spritegroupe=spritegroupe
        spritegroupe.add(self)
        self.vitesse=vitesse
        self.clock=pygame.time.Clock()
        self.tailleOriginaleX,self.tailleOriginaleY = self.image.get_size()
        self.direction=0
        
    def killsprite(self):
        '''
        Cette methode tue/enleve le sprite de tous les groupes
        '''
        self.kill()
        
    def collidemask(self,otherpos,othermask,types):
        '''
        le methode collidemask est pour detecter le collision entre cette sprite et un autre qui contiennent un mask
        parametres:
        
        otherpos:tuple
        otherpos est un tuple qui contient (x,y) coordonnees de l'autre sprite
        
        othermask:type inconnue
        othermask est le variable self.mask de l'autre sprite
        
        types:type string ou None
        il y a 3 options:
        'bords' va renvoier True et un list qui indique quelle bord est en train de toucher l'autre sprite
        'coins' va renvoier True et un list qui indique quelle coin est en train de toucher l'autre sprite
        None va renvoier True et None
        '''
        collide=self.mask.overlap(othermask,(otherpos[0]-self.rect[0],otherpos[1]-self.rect[1]))
        if type(collide)==tuple:
            directions=[]
            if types==None:
                return True,None
            if types=='bords':
                if collide[0]<self.mask.get_size()[0]/10:
                    directions.append('left')
                if collide[0]>self.mask.get_size()[0]-self.mask.get_size()[0]/10:
                    directions.append('right')
                if collide[1]<self.mask.get_size()[1]/10:
                    directions.append('up')
                if collide[1]>self.mask.get_size()[1]-self.mask.get_size()[1]/5:
                    directions.append('down')
            elif types=='coins':
                if collide[0]<self.mask.get_size()[0]/10 and collide[1]<self.mask.get_size()[1]/10:
                    directions.append('left up')
                if collide[0]<self.mask.get_size()[0]/10 and collide[1]>self.mask.get_size()[1]-self.mask.get_size()[1]/5:
                    directions.append('left down')
                if collide[0]>self.mask.get_size()[0]-self.mask.get_size()[0]/10 and collide[1]<self.mask.get_size()[1]/10:
                    directions.append('right up')
                if collide[0]>self.mask.get_size()[0]-self.mask.get_size()[0]/10 and collide[1]>self.mask.get_size()[1]-self.mask.get_size()[1]/5:
                    directions.append('right down')
            return True,directions
        else:
            return False,None


    def update(self, movement):
        '''
        Outil de debug pour bouger le sprite
        parametre:
        movement=List
        movement est un list de 4 valeurs qui sont des booleans,le prochain ligne est la direction de chaque position
        movement=[avancer vers le haut,avancer vers le bas,avancer vers le gauche,avancer vers le droite]
        le sprite est avancee par son vitesse de pixels
        '''
        # Move the sprite based on arrow key input
        if movement[0]:
            self.rect.y -= self.vitesse
        if movement[1]:
            self.rect.y += self.vitesse
        if movement[2]:
            self.rect.x -= self.vitesse
        if movement[3]:
            self.rect.x += self.vitesse
    
    def animate(self,number,imagename,mask=False):
        '''
        Il prend 2 parametres
        ATTENTION:tout image doit etre un .png
        Le nombre d'image que tu veut changer et le nom de image
        Donc si l'image est un fichier placeholder.png
        Les animations doivent contenir un nombre apres,par example:
        placeholder1.png placeholder2.png ...
        et le parametre imagename est un string qui contient le nom du fichier sans .png ou le nombre
        si parametres est number=1 imagename='placeholder' par example
        Cette methode va chercher le fichier placeholder1.png dans le directoire "Images"
        et changer l'image du sprite
        '''
        self.image=pygame.image.load(os.path.join("Images", imagename+str(number)+".png"))
        originale_largeur, originale_hauteur = self.image.get_size()
        echelle_largeur = int(originale_largeur * self.scaleX)
        echelle_hauteur = int(originale_hauteur * self.scaleY)
        self.image = pygame.transform.scale(self.image, (echelle_largeur, echelle_hauteur))
        self.direction = 0
        if mask:
            self.mask=pygame.mask.from_surface(self.image)
        
    def echelle(self,echelleX,echelleY):
        '''
        Cette methode est pour agrandir ou reduire la taille de la sprite
        Parametre:
        echelle:Int
        Le nombre qui va multiplier la taille de la sprite(<0 pour reduire,>0 pour agrandir)
        '''
        self.scaleX=echelleX
        self.scaleY=echelleY
        echelle_largeur = int(self.tailleOriginaleX * self.scaleX)
        echelle_hauteur = int(self.tailleOriginaleY * self.scaleY)
        self.image = pygame.transform.scale(self.image, (echelle_largeur, echelle_hauteur))
        
    def pivoter(self,angle):
        '''
        Cette methode est pour pivoter le sprite
        Parametre:
        angle:Int
        De combien de degrees pivote-elle le sprite,-90 pour pivoter vers la gauche de 90 degrees et 90 pour pivoter vers la droite de 90 degrees
        '''  
        self.image=pygame.transform.rotate(self.image, angle-self.direction)
        self.direction = angle
        self.mask=pygame.mask.from_surface(self.image)
        
