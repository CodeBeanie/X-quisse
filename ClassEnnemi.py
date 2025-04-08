from random import *
from ClassDisplay import *
import ClassSprite
import pygame,sys,time,random,os
from pygame.locals import *
from ClassProjectile import *
from ClassBlob import *
from ClassParticule import *
from ClassMusique import *

class Ennemi:
    """
    Les Objets de la classe Ennemi représente les Ennemi
    Paramètres:
    X (float) : position de l'ennemi par apport à la salle
    Y (float) : position de l'ennemi par apport à la salle
    SpriteGroup (Objet SpriteGroup dans ClassDisplay): SpriteGroup des Enemmis
    SpriteHitbox (Objet SpriteGroup dans ClassDisplay): SpriteGroup des Hitboxes Enemmis
    salleX (int) : position de la tuile (la tuile fait 720x720 pixel donc est multiplié par 720)
    salleY (int) : position de la tuile (la tuile fait 720x720 pixel donc est multiplié par 720)
    carte (Objet SpriteGroup dans ClassCarteDuMondeV2): carte
    Type (string) : indique quelle énemmi ("stickman","oeuil"...)
    """
    def __init__(self,X,Y,SpriteGroup,SpriteHitbox,salleX,salleY,carte,Type):

        self.salleX=salleX
        self.salleY=salleY
        self.x = X * carte.tailleCarte
        self.y = Y * carte.tailleCarte
        self.pv = 10
        self.type = Type
        self.timer = 0
        self.timerDegat = 0
        self.estEtourdie = False
        self.animationTimer = 0
        self.animationNumber = 1
        self.attackTimer=0
        self.sprite = ClassSprite.Sprite((10000,10000),SpriteGroup,"Enemy_"+self.type+"_Sprite1",0,1,1)
        self.hitbox = ClassSprite.Sprite((10000,10000),SpriteHitbox,"Enemy_"+self.type+"_Hitbox",0,1,1)
        self.vitesseX=5
        self.vitesseY=5
        self.offsetX = 0
        self.offsetY = 0
        self.randomAttack = 0
        if self.type == "Stickman":
            self.pv = 4
        elif self.type == "Cube":
            self.pv = 7
        elif self.type == "Cube2":
            self.pv = 7
        elif self.type == "Oeuil":
            self.pv = 15
        elif self.type == "Cubisme":
            self.pv = 10
        elif self.type == "Main":
            self.pv = 10
        elif self.type == "Maurice":
            self.pv = 30
        elif self.type == "Maurice":
            self.pv = 50            
        elif self.type == "Maurice":
            self.pv = 60
            
    def degatEnemie(self,joueur,Vitrine,carte,listeBlob,groupBlob,TailleCarte,ListeParticule,ParticuleGroup,DegatProjectile):
        sonOuch = Musique("Enemy dmg.mp3")
        sonMort = Musique("Enemy death.mp3")
        self.timerDegat += Vitrine.clock.get_time()
        if DegatProjectile== 0:
            if self.hitbox.collidemask(joueur.arme.rect,joueur.arme.mask,None)[0] and joueur.attack:
                if not self.estEtourdie:
                    self.estEtourdie = True
                    
                    if joueur.typeArme == "Cutter":
                        self.pv -= 2
                    elif joueur.typeArme == "Pencil":
                        self.pv -= 0.5
                    elif joueur.typeArme == "Plume":
                        self.pv -= 0
                    elif joueur.typeArme == "Brush":
                        self.pv -= 1

                    print("ochi")
                    for i in range(randint(3,6)):
                        ListeParticule.append(Particule((720*TailleCarte*self.salleX+self.x+100,-720*TailleCarte*self.salleY+self.y+100,randint(-10,10),randint(-10,-5)),"encre",ParticuleGroup,"Particule_Monstre"+str(randint(1,3)),randint(2,4)*0.2))
                    if self.pv <= 0:
                        carte.ennemies.pop(carte.ennemies.index(self))
                        self.sprite.kill()
                        self.hitbox.kill()
                        carte.EnemiesKills +=1
                        listeBlob.append(Blob(720*TailleCarte*self.salleX+self.x+50,-720*TailleCarte*self.salleY+self.y+100,groupBlob))
                        sonMort = Musique("Enemy death.mp3")
                        ######### - Small Rip 
#                         sonMort.start(1, 4)
                        smalrip=Musique("SmallRip.mp3")
                        smalrip.start(0,14,0.5)
                    else:
                        print("")
                        ######### -  Rip
                        rip=Musique("Rip.mp3")
                        rip.start(0,9,0.5)

                            
                        
                        
            elif self.estEtourdie:
                if self.timerDegat > 500:
                    self.estEtourdie = False
                    self.timerDegat=0
        else:
            if self.pv > 0:
                self.pv -= DegatProjectile
                print("ochi2")

                for i in range(randint(3,6)):
                    ListeParticule.append(Particule((720*TailleCarte*self.salleX+self.x+100,-720*TailleCarte*self.salleY+self.y+100,randint(-10,10),randint(-10,-5)),"encre",ParticuleGroup,"Particule_Monstre"+str(randint(1,3)),randint(2,4)*0.2))
                if self.pv <= 0:
                    carte.ennemies.pop(carte.ennemies.index(self))
                    self.sprite.kill()
                    self.hitbox.kill()
                    carte.EnemiesKills +=1
                    listeBlob.append(Blob(720*TailleCarte*self.salleX+self.x+100,-720*TailleCarte*self.salleY+self.y+100,groupBlob))
                    smalrip=Musique("SmallRip.mp3")
                    smalrip.start(0,14,0.5)
                    ######### -  Rip 

                    rip=Musique("Rip.mp3")
                    rip.start(0,15,0.5)
                else:
                    print("")
                    rip=Musique("Rip.mp3")
                    rip.start(0,15,0.5)
                    ######### -  Rip 
        
    def comportement(self,carte,joueur,PosX,PosY,TailleCarte,Vitrine,ListeProjectiles,ProjectilesGroup,packetEnemies): 
        self.animationTimer += Vitrine.clock.get_time()
        self.attackTimer += Vitrine.clock.get_time()
        sonJoueur = Musique("Player dmg.mp3")
        #################################
        if self.type == "Stickman":
            distanceX = 720*TailleCarte*self.salleX+self.x-TailleCarte*360 + PosX+150
            distanceY = -720*TailleCarte*self.salleY+self.y-TailleCarte*360 + PosY+150
            TotalDistance = sqrt(distanceX **2 + distanceY ** 2)
            
            if TotalDistance >20:
                vitesse = 10
                self.x -= (distanceX/TotalDistance) * vitesse
                self.hitbox.rect.x -= (distanceX/TotalDistance) * vitesse
                
                
                collision = False
                for sprites in carte.hitbox:
                    if self.hitbox.collidemask(sprites.rect,sprites.mask,None)[0]:
                        collision = True
            
                if collision:
                    self.x += (distanceX/TotalDistance) * vitesse
                    self.hitbox.rect.x += (distanceX/TotalDistance) * vitesse

                ###
                self.y -= (distanceY/TotalDistance) * vitesse
                self.hitbox.rect.y -= (distanceY/TotalDistance) * vitesse
                
                collision = False
                for sprites in carte.hitbox:
                    if self.hitbox.collidemask(sprites.rect,sprites.mask,None)[0]:
                        collision = True
            
                if collision:             
                    self.y += (distanceY/TotalDistance) * vitesse
                    self.hitbox.rect.y += (distanceY/TotalDistance) * vitesse
            
            
            
            
            
            
            if self.animationTimer > 500:
                if self.animationNumber == 1:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 2
                    self.animationTimer = 0
                elif self.animationNumber == 2:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 1
                    self.animationTimer = 0
                    

                
                
            
            if self.hitbox.collidemask(joueur.hitbox.rect,joueur.hitbox.mask,None)[0]:
                if joueur.degatTimer <= 0:
                    if joueur.armure > 0:
                        joueur.armure -=1
                    else:
                        joueur.pv -=1

                    brip=Musique("Big Rip.mp3")
                    brip.start(0,15,0.5)
                        ######### - Big rip
                    joueur.degatTimer = 3000
                        
                    
        ####################################
        elif self.type == "Oeuil":
            if self.animationTimer > 250:
                if self.animationNumber == 1:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 2
                    self.animationTimer = 0
                elif self.animationNumber == 2:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 1
                    self.animationTimer = 0
                    
                    
            if self.attackTimer> 5000:
                ListeProjectiles.append(Projectile(5,720*TailleCarte*self.salleX+self.x,-720*TailleCarte*self.salleY+self.y,4,2,"O","Projectile_Oeuil1",1,ProjectilesGroup,True))
                self.attackTimer = 0
                
                
            if self.hitbox.collidemask(joueur.hitbox.rect,joueur.hitbox.mask,None)[0]:
                if joueur.degatTimer <= 0:
                    if joueur.armure > 0:
                        joueur.armure -=1
                    else:
                        joueur.pv -=1
#                     sonJoueur.start(0,5)
                    joueur.degatTimer = 3000
        ####################################
        elif self.type == "Cube":
            if self.animationTimer > 250:
                if self.animationNumber == 1:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 2
                    self.animationTimer = 0
                elif self.animationNumber == 2:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 3
                    self.animationTimer = 0
                elif self.animationNumber == 3:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 1
                    self.animationTimer = 0
                    
                    
            random = randint(1,4)
            if random == 1:
                self.x -= 10
                self.hitbox.rect.x -= 10    
            elif random == 2:
                self.y -= 10
                self.hitbox.rect.y -= 10
            elif random == 3:
                self.x += 10
                self.hitbox.rect.x += 10    
            elif random == 4:
                self.y += 10
                self.hitbox.rect.y += 10    
            collision = False
            for sprites in carte.hitbox:
                if self.hitbox.collidemask(sprites.rect,sprites.mask,None)[0]:
                    collision = True
            if collision:
                if random == 1:
                    self.x += 10
                    self.hitbox.rect.x += 10    
                elif random == 2:
                    self.y += 10
                    self.hitbox.rect.y += 10
                elif random == 3:
                    self.x -= 10
                    self.hitbox.rect.x -= 10    
                elif random == 4:
                    self.y -= 10
                    self.hitbox.rect.y -= 10     
            if self.hitbox.collidemask(joueur.hitbox.rect,joueur.hitbox.mask,None)[0]:
                if joueur.degatTimer <= 0:
                    if joueur.armure > 0:
                        joueur.armure -=1
                    else:
                        joueur.pv -=1
#                     sonJoueur.start(1,5)
                    joueur.degatTimer = 3000        
        ####################################
        elif self.type == "Cube2":
            if self.animationTimer > 250:
                if self.animationNumber == 1:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 2
                    self.animationTimer = 0
                elif self.animationNumber == 2:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 3
                    self.animationTimer = 0
                elif self.animationNumber == 3:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 1
                    self.animationTimer = 0 
                
                
            if self.hitbox.collidemask(joueur.hitbox.rect,joueur.hitbox.mask,None)[0]:
                if joueur.degatTimer <= 0:
                    if joueur.armure > 0:
                        joueur.armure -=1
                    else:
                        joueur.pv -=1
#                     sonJoueur.start(1,5)
                    joueur.degatTimer = 3000    
        ###################################
        elif self.type == "Cubisme":
            if self.animationTimer > 250:
                if self.animationNumber == 1:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 2
                    self.animationTimer = 0
                elif self.animationNumber == 2:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 1
                    self.animationTimer = 0
            

            self.x += self.vitesseX
            self.hitbox.rect.x += self.vitesseX
            
            collision = False
            for sprites in carte.hitbox:
                if self.hitbox.collidemask(sprites.rect,sprites.mask,None)[0]:
                    collision = True
        
            if collision:             
                self.vitesseX = -self.vitesseX
                self.x += self.vitesseX
                self.hitbox.rect.x += self.vitesseX

            
            self.y += self.vitesseY
            self.hitbox.rect.y += self.vitesseY
            collision = False
            for sprites in carte.hitbox:
                if self.hitbox.collidemask(sprites.rect,sprites.mask,None)[0]:
                    collision = True


            
            if collision:
                self.vitesseY = -self.vitesseY
                self.y += self.vitesseY
                self.hitbox.rect.y += self.vitesseY
            
            if self.attackTimer> 5000:
                ListeProjectiles.append(Projectile(6,720*TailleCarte*self.salleX+self.x,-720*TailleCarte*self.salleY+self.y,8,2,"","Projectile_Cubisme1",1,ProjectilesGroup,True))
                self.attackTimer = 0
                
                
            if self.hitbox.collidemask(joueur.hitbox.rect,joueur.hitbox.mask,None)[0]:
                if joueur.degatTimer <= 0:
                    if joueur.armure > 0:
                        joueur.armure -=1
                    else:
                        joueur.pv -=1
#                     sonJoueur.start(1,5)
                    joueur.degatTimer = 3000
                    
               ###############################     
        elif self.type == "Main":
            distanceX = 720*TailleCarte*self.salleX+self.x-TailleCarte*360 + PosX+150
            distanceY = -720*TailleCarte*self.salleY+self.y-TailleCarte*360 + PosY+150
            TotalDistance = sqrt(distanceX **2 + distanceY ** 2)
            
           
            
            
            
            if self.animationTimer > 500:
                if self.animationNumber == 1:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 2
                    self.animationTimer = 0
                elif self.animationNumber == 2:
                    self.sprite.animate("","Enemy_"+self.type+"_Sprite"+str(self.animationNumber) ,False)
                    self.animationNumber = 1
                    self.animationTimer = 0
                    
            self.offsetY = -180
            self.offsetX = 40
            
            if self.attackTimer> 10000:
                self.attackTimer = 0
            elif self.attackTimer> 8500:
                self.offsetY = -10
            elif self.attackTimer> 8000:
                self.offsetY = -220
            else:
                self.offsetY = -180
                if TotalDistance >20:
                    vitesse = 20
                    self.x -= (distanceX/TotalDistance) * vitesse
                    self.hitbox.rect.x -= self.x  
                    self.y -= (distanceY/TotalDistance) * vitesse
                    self.hitbox.rect.y -= self.y   
                
                
            if self.hitbox.collidemask(joueur.hitbox.rect,joueur.hitbox.mask,None)[0]:
                if joueur.degatTimer <= 0:
                    if joueur.armure > 0:
                        joueur.armure -=1
                    else:
                        joueur.pv -=1
#                     sonJoueur.start(1,5)
                    joueur.degatTimer = 3000
                    
        ###################################
        elif self.type == "Maurice" or self.type == "Maurice1" or self.type == "Maurice2":
            if self.animationTimer > 500:
                if self.randomAttack == 0:
                    if self.animationNumber == 1:
                        self.sprite.animate("","Enemy_"+"Maurice"+"_Sprite"+str(self.animationNumber) ,False)
                        self.animationNumber = 2
                        self.animationTimer = 0
                    elif self.animationNumber == 2:
                        self.sprite.animate("","Enemy_"+"Maurice"+"_Sprite"+str(self.animationNumber) ,False)
                        self.animationNumber = 1
                        self.animationTimer = 0
                        
            if self.animationTimer > 500:

                if self.randomAttack == 1 or self.randomAttack == 2:
                    if self.animationNumber == 1:
                        self.sprite.animate(3,"Enemy_"+"Maurice"+"_Sprite" ,False)
                        self.animationNumber = 2
                        self.animationTimer = 0
                    elif self.animationNumber == 2:
                        self.sprite.animate(4,"Enemy_"+"Maurice"+"_Sprite" ,False)
                        self.animationNumber = 3
                        self.animationTimer = 0
                        ListeProjectiles.append(Projectile(6,720*TailleCarte*self.salleX+self.x,-720*TailleCarte*self.salleY+self.y,8,2,"","Projectile_Cubisme1",1,ProjectilesGroup,True))
                    elif self.animationNumber == 3:
                        self.sprite.animate(5,"Enemy_"+"Maurice"+"_Sprite",False)
                        self.animationNumber = 1
                        self.animationTimer = 0
                
            if self.animationTimer > 2400:
                if self.randomAttack == 3:
                    if self.animationNumber == 1:
                        self.sprite.animate(3,"Enemy_"+"Maurice"+"_Sprite" ,False)
                        self.animationNumber = 2
                        self.animationTimer = 0
                        
                    elif self.animationNumber == 2:
                        self.sprite.animate(4,"Enemy_"+"Maurice"+"_Sprite" ,False)
                        self.animationNumber = 3
                        self.animationTimer = 0
                        packetEnemies[0].enemiess.append(Ennemi(300,150,packetEnemies[1].ennemiesSprite,packetEnemies[1].ennemiesHitbox,packetEnemies[0].x,packetEnemies[0].y,packetEnemies[1],"Stickman"))
                        packetEnemies[1].ennemies.append(packetEnemies[0].enemiess[len(packetEnemies[0].enemiess)-1])
                    elif self.animationNumber == 3:
                        self.sprite.animate(3,"Enemy_"+"Maurice"+"_Sprite" ,False)
                        self.animationNumber = 4
                        self.animationTimer = 0

                    elif self.animationNumber == 4:
                        self.sprite.animate(4,"Enemy_"+"Maurice"+"_Sprite" ,False)
                        self.animationNumber = 1
                        self.animationTimer = 0
                        packetEnemies[0].enemiess.append(Ennemi(300,150,packetEnemies[1].ennemiesSprite,packetEnemies[1].ennemiesHitbox,packetEnemies[0].x,packetEnemies[0].y,packetEnemies[1],"Stickman"))
                        packetEnemies[1].ennemies.append(packetEnemies[0].enemiess[len(packetEnemies[0].enemiess)-1])
            
            if self.animationTimer > 1000:
                if self.randomAttack == 4 or self.randomAttack == 5:
                    if self.animationNumber == 1:
                        self.sprite.animate(3,"Enemy_"+"Maurice"+"_Sprite" ,False)
                        self.animationNumber = 2
                        self.animationTimer = 0

                        
                    elif self.animationNumber == 2:
                        self.sprite.animate(4,"Enemy_"+"Maurice"+"_Sprite" ,False)
                        self.animationNumber = 1
                        self.animationTimer = 0
                        ListeProjectiles.append(Projectile(0,720*TailleCarte*self.salleX+self.x,-720*TailleCarte*self.salleY+self.y,8,2,"N","Projectile_Cubisme1",1,ProjectilesGroup,True))
                        ListeProjectiles.append(Projectile(0,720*TailleCarte*self.salleX+self.x,-720*TailleCarte*self.salleY+self.y,8,2,"E","Projectile_Cubisme1",1,ProjectilesGroup,True))
                        ListeProjectiles.append(Projectile(0,720*TailleCarte*self.salleX+self.x,-720*TailleCarte*self.salleY+self.y,8,2,"S","Projectile_Cubisme1",1,ProjectilesGroup,True))
                        ListeProjectiles.append(Projectile(0,720*TailleCarte*self.salleX+self.x,-720*TailleCarte*self.salleY+self.y,8,2,"W","Projectile_Cubisme1",1,ProjectilesGroup,True))
                        ListeProjectiles.append(Projectile(1,720*TailleCarte*self.salleX+self.x,-720*TailleCarte*self.salleY+self.y,8,2,"N","Projectile_Cubisme1",1,ProjectilesGroup,True))
                        ListeProjectiles.append(Projectile(1,720*TailleCarte*self.salleX+self.x,-720*TailleCarte*self.salleY+self.y,8,2,"E","Projectile_Cubisme1",1,ProjectilesGroup,True))
                        ListeProjectiles.append(Projectile(1,720*TailleCarte*self.salleX+self.x,-720*TailleCarte*self.salleY+self.y,8,2,"S","Projectile_Cubisme1",1,ProjectilesGroup,True))
                        ListeProjectiles.append(Projectile(1,720*TailleCarte*self.salleX+self.x,-720*TailleCarte*self.salleY+self.y,8,2,"W","Projectile_Cubisme1",1,ProjectilesGroup,True))
                        
            
            
            if self.attackTimer> 5000:
                self.randomAttack = 0
                self.animationNumber = 1
                self.animationTimer = 0
            if self.attackTimer> 12000:
                self.attackTimer = 0
                self.randomAttack = randint(1,5)
            
            
            if self.hitbox.collidemask(joueur.hitbox.rect,joueur.hitbox.mask,None)[0]:
                if joueur.degatTimer <= 0:
                    if joueur.armure > 0:
                        joueur.armure -=1
                    else:
                        joueur.pv -=1
#                     sonJoueur.start(1,5)
                    joueur.degatTimer = 3000         

