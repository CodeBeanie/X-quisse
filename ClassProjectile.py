# créé par Léane

import pygame
import ClassSprite
from math import *
from ClassMusique import *

class Projectile:
    """
    création d'une instance Projectile:
        projectile = Projectile(type(int) , pos_x(int), pos_y(int), vitesse(int), collision(bool), degat(int), orientation(str), image(png), scale(int))
    attributs d'instance: type, pos_x, pos_y, vitesse, oritentation, collision, degat, image, scale

    attribut type = définit le mouvement du projectile
        type = 0: projectile basique, se déplace en ligne droite jusqu'à atteindre un hitbox et disparaître
        type = 1: projectile diagonal, se déplace en diagonal jusqu'à atteindre un hitbox et disparaître
        type = 2: projectile long, avance dans la direction que s'oriente le joueur avant de revenir vers lui et disparaître
        type = 3: projectile collant, se déplace en ligne droite jusqu'à atteindre un hitbox et de s'y fixer pour une période, puis disparaître
        type = 4: projectile rebondissant, se déplace en ligne droite jusqu'à atteindre un hitbox et d'y rebondir à un angle

    attribut orientation = orientation du joueur
        options: N (=nord), E (=est), S (=sud), O (=ouest)


    méthodes:
        direction: détermine la direction de la trajectoire du projectile selon orientation de la source
        mouvement: déplace le projetile selon son type

    """

    def __init__(self, Type, pos_x, pos_y, vitesse, degat, orientation, image, scale,
                 spritegroup,estMechant = False,dx=0, dy=0, collision=False):
        self.type = Type
        self.x = pos_x
        self.y = pos_y
        self.vitesse = vitesse
        self.dx = dx
        self.dy = dy
        self.collision = collision
        self.degat = degat
        self.orientation = orientation
        self.image = image
        self.Objet = ClassSprite.Sprite((1000000, 1000000), spritegroup, image,0, scale,scale)  ###unsure if this works  ###Yep that works too
        self.estMechant = estMechant
        self.timerAnimation = 0
        self.orientationAngle= 0
        
        #UNiquement pour type 7
        self.enemiesTouches = []
        
        
    def direction(self):
        if self.orientation == 'N':
            self.Objet.pivoter(-90)
            self.orientationAngle=-90
            self.dx = 1
            self.dy = 1
        elif self.orientation == 'E':
            self.Objet.pivoter(0)
            self.orientationAngle=0
            self.dx = 1
            self.dy = -1
        elif self.orientation == 'S':
            self.Objet.pivoter(90)
            self.orientationAngle=90
            self.dx = -1
            self.dy = -1
        elif self.orientation == 'O':
            self.orientationAngle=180
            self.Objet.pivoter(180)
            self.dx = -1
            self.dy = 1
        
        #Exeptions
        if self.type == 8:
            self.Objet.pivoter(self.orientationAngle+180)

        return self.dx, self.dy
    

                        
    def touche_mur(self,carte):
        for sprites in carte.hitbox:
            if self.Objet.collidemask(sprites.rect,sprites.mask,None)[0]:
                return True
                
        return False
    
    def touche_ennemi(self,carte,PacketEnemie):
        for sprites in carte.ennemies:
            
            if self.Objet.collidemask(sprites.hitbox.rect,sprites.hitbox.mask,None)[0]:
                sprites.degatEnemie(PacketEnemie[0],PacketEnemie[1],PacketEnemie[2],PacketEnemie[3],PacketEnemie[4],PacketEnemie[5],PacketEnemie[6],PacketEnemie[7],self.degat)
                return True

        return False
                
    def touche_joueur(self,joueur):
        if self.Objet.collidemask(joueur.hitbox.rect,joueur.hitbox.mask,None)[0]:
            if joueur.degatTimer <= 0:
                if joueur.armure > 0:
                    joueur.armure -=1
                else:
                    joueur.pv -=1
                    brip=Musique("Big Rip.mp3")
                    brip.start(0,15,0.5)
            return True
        else:
            return False
                
    def mouvement(self, carte,joueur,PosX,PosY,ListeProjectiles,TailleCarte,PacketEnemie,vitrine,multiplicateurFPS,ProjectileGroup):
        self.timerAnimation += vitrine.clock.get_time()
        self.direction()  #### this probably doesn't work    ###Well it works now >:)

        ###aniamtion
        
        
        
        
        
        
        
        
        
        
        
        
        ###Mouvement
        if self.type < 3:
            if self.estMechant == False:
                if self.touche_mur(carte) == True or self.touche_ennemi(carte,PacketEnemie):
                    ListeProjectiles.pop(ListeProjectiles.index(self))
                    self.Objet.kill()
                    del(self)
                    return
            else:
                if self.touche_mur(carte) == True or self.touche_joueur(joueur):

                    ListeProjectiles.pop(ListeProjectiles.index(self))
                    self.Objet.kill()
                    del(self)
                    return
                    
            if self.type == 0:							#projectile basique
                self.Objet.pivoter(self.orientationAngle+180)
                if self.image == "Projectile_Crayon":
                    self.Objet.pivoter(self.orientationAngle+90)
                
                
                
                if self.orientation == 'N' or self.orientation == 'S':
                    self.y += self.dy * self.vitesse * multiplicateurFPS
                    position = (self.x, self.y)
                    self.Objet.rect.x,self.Objet.rect.y = position
                elif self.orientation == 'E' or self.orientation == 'O':
                    self.x += self.dx * self.vitesse * multiplicateurFPS
                    position = (self.x, self.y)
                    self.Objet.rect.x,self.Objet.rect.y = position

            elif self.type == 1:						#projectile diagonal
                
                print(multiplicateurFPS)
                self.Objet.pivoter(self.orientationAngle)
                self.x += self.dx *  multiplicateurFPS * sqrt((self.vitesse**2)/2)
                self.y += self.dy *  multiplicateurFPS * sqrt((self.vitesse**2)/2)

                self.Objet.rect.x = self.x
                self.Objet.rect.y = self.y
                
                
                
        if self.type==4:									#projectile rebondissant
            if touche_mur(carte) == True:
                self.dx = -self.dx
                self.dy = -self.dy

            self.x = dx * self.vitesse * multiplicateurFPS
            self.y = dy * self.vitesse * multiplicateurFPS
            position = (self.x, self.y)
            self.Objet.rect.x,self.Objet.rect.y = position
            
            
        if self.type == 5:								#Projectile a tete chercheuse
            distanceX = self.x -TailleCarte*360 + PosX+150
            distanceY = self.y -TailleCarte*360 +PosY+150
            TotalDistance = sqrt(distanceX **2 + distanceY ** 2)
            self.dx = distanceX/TotalDistance
            self.dy = distanceY/TotalDistance
    
            self.x += -self.dx * self.vitesse * multiplicateurFPS
            self.y += -self.dy * self.vitesse * multiplicateurFPS

            self.Objet.rect.x = self.x+PosX
            self.Objet.rect.y = self.y+PosY

            if self.touche_mur(carte) or self.touche_joueur(joueur):
                ListeProjectiles.pop(ListeProjectiles.index(self))
                self.Objet.kill()
                del(self)
                return
            if self.timerAnimation > 500 :
                self.timerAnimation = 0
                self.Objet.animate("","Projectile_Oeuil1" ,False)

            elif self.timerAnimation > 250: 
                self.Objet.animate("","Projectile_Oeuil2" ,False)
            
            
            
        elif self.type == 6:								#Projectile
            if self.orientation == "":
                distanceX = self.x -TailleCarte*360 + PosX+150
                distanceY = self.y -TailleCarte*360 + PosY+150
                TotalDistance = sqrt(distanceX **2 + distanceY ** 2)
                self.dx = distanceX/TotalDistance
                self.dy = distanceY/TotalDistance
                self.orientation = "ouiouibaguette"
            
            if self.timerAnimation > 500 :
                self.timerAnimation = 0
                self.Objet.animate("","Projectile_Cubisme1" ,False)

            elif self.timerAnimation > 250: 
                self.Objet.animate("","Projectile_Cubisme2",False)
          
            
            self.x += -self.dx * self.vitesse * multiplicateurFPS
            self.y += -self.dy * self.vitesse * multiplicateurFPS

            self.Objet.rect.x = self.x+PosX
            self.Objet.rect.y = self.y+PosY

            if self.touche_mur(carte) or self.touche_joueur(joueur):
                ListeProjectiles.pop(ListeProjectiles.index(self))
                self.Objet.kill()
                del(self)
        
        elif self.type == 7:								#Slash d'encre
            
            if self.timerAnimation > 450:
                ListeProjectiles.pop(ListeProjectiles.index(self))
                self.Objet.kill()
                del(self)
                return
            elif self.timerAnimation > 300:
                self.Objet.animate(3,"Projectile_InkSlash" ,False)
                self.Objet.pivoter(self.orientationAngle)
            elif self.timerAnimation > 150:

                self.Objet.animate(2,"Projectile_InkSlash" ,False)
                self.Objet.pivoter(self.orientationAngle)
            else:
                self.Objet.animate(1,"Projectile_InkSlash" ,False)
                self.Objet.pivoter(self.orientationAngle)
                
            for sprites in carte.ennemies:
                if self.Objet.collidemask(sprites.hitbox.rect,sprites.hitbox.mask,None)[0] and sprites not in self.enemiesTouches:
                    sprites.degatEnemie(PacketEnemie[0],PacketEnemie[1],PacketEnemie[2],PacketEnemie[3],PacketEnemie[4],PacketEnemie[5],PacketEnemie[6],PacketEnemie[7],self.degat)
                    self.enemiesTouches.append(sprites)
        elif self.type == 8:								#Slash d'encre
            
            if self.touche_mur(carte) == True or self.touche_ennemi(carte,PacketEnemie):
                if self.orientation == 'N' or self.orientation == 'S':
                    self.y -= self.dy * self.vitesse * multiplicateurFPS *2
                    position = (self.x, self.y)
                    self.Objet.rect.x,self.Objet.rect.y = position
                elif self.orientation == 'E' or self.orientation == 'O':
                    self.x -= self.dx * self.vitesse * multiplicateurFPS *2
                    position = (self.x, self.y)
                    self.Objet.rect.x,self.Objet.rect.y = position
                ListeProjectiles.append(Projectile(0,self.x+40,self.y+50,7,1,"O","Particule_Ink",0.5,ProjectileGroup))
                ListeProjectiles.append(Projectile(0,self.x+40,self.y+50,7,1,"E","Particule_Ink",0.5,ProjectileGroup))
                ListeProjectiles.append(Projectile(0,self.x+40,self.y+50,7,1,"S","Particule_Ink",0.5,ProjectileGroup))
                ListeProjectiles.append(Projectile(0,self.x+40,self.y+50,7,1,"N","Particule_Ink",0.5,ProjectileGroup))
                ListeProjectiles.append(Projectile(1,self.x+40,self.y+50,7,1,"O","Particule_Ink",0.5,ProjectileGroup))
                ListeProjectiles.append(Projectile(1,self.x+40,self.y+50,7,1,"E","Particule_Ink",0.5,ProjectileGroup))
                ListeProjectiles.append(Projectile(1,self.x+40,self.y+50,7,1,"S","Particule_Ink",0.5,ProjectileGroup))
                ListeProjectiles.append(Projectile(1,self.x+40,self.y+50,7,1,"N","Particule_Ink",0.5,ProjectileGroup))                
                
                ListeProjectiles.pop(ListeProjectiles.index(self))
                self.Objet.kill()
                del(self)
                return
            
            if self.orientation == 'N' or self.orientation == 'S':
                self.y += self.dy * self.vitesse * multiplicateurFPS
                position = (self.x, self.y)
                self.Objet.rect.x,self.Objet.rect.y = position
            elif self.orientation == 'E' or self.orientation == 'O':
                self.x += self.dx * self.vitesse * multiplicateurFPS
                position = (self.x, self.y)
                self.Objet.rect.x,self.Objet.rect.y = position


                

            
