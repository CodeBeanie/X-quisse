from math import *
from random import *
from ClassDisplay import*
import ClassSprite
import pygame,sys,time,random,os
from pygame.locals import *
from ClassProjectile import *
class Personnage:
    """
    Les Objets de la classe Personnage représente le joueur
    Paramètres:
    GroupeSprite (Objet SpriteGroup dans ClassDisplay): SpriteGroup de sprite
    GroupeHitbox (Objet SpriteGroup dans ClassDisplay): SpriteGroup de la hitbox
    GroupeArme (Objet SpriteGroup dans ClassDisplay): SpriteGroup de l'arme
    """
    def __init__(self,GroupeSprite,GroupeHitbox,GroupeArme):
        #Stats de jeu
        self.vitesse = 7
        self.encre = 25
        self.encreMax = 50
        self.armure = 1
        self.pv = 5
        self.pvMax = 5
        self.objets=[]
        self.typeArme=""
        self.VitesseAttaque = 1
        self.force = 0
        
        #Affichage et controlles
        self.GGroup = GroupeSprite
        self.GGroup2 = GroupeHitbox
        self.hitbox = ClassSprite.Sprite((500,500),self.GGroup2,"Joueur_hitbox",0,0.75,0.75)
        self.sprite = ClassSprite.Sprite((500,500),self.GGroup,"Joueur_S1",0,0.75,0.75)
        self.arme = ClassSprite.Sprite((500,500),GroupeArme,"Weapon_Cutter_O",0,0.65,0.65) 
        self.animationTimer = 0
        self.animationNumber = 1
        self.attack = False
        self.specialAttack = False
        self.attackCooldown = 0
        self.imageActuelle = "Joueur_S"
        self.directionAttaque = "NS"
        self.animationAttack=[]
        self.degatTimer=0
        

    
    def placementArme(self):
        self.arme.animate( "_O","Weapon_"+str(self.typeArme),False)

        if self.typeArme == "Cutter": 
            PlacementArme = [(460,430),(530,465),(475,515),(410,465)]
        elif self.typeArme == "Brush": 
            PlacementArme = [(460,430),(530,465),(475,515),(410,465)]            
        elif self.typeArme == "Feather": 
            PlacementArme = [(460,430),(530,465),(475,515),(410,465)]              
        elif self.typeArme == "Pencil": 
            PlacementArme = [(460,425),(535,465),(475,520),(405,465)]              
        elif self.typeArme == "Plume": 
            PlacementArme = [(460,430),(530,465),(475,515),(410,465)]          
            
        if self.imageActuelle == "Joueur_N":
            self.arme.pivoter(-90)
            self.arme.rect.x = PlacementArme[0][0]
            self.arme.rect.y = PlacementArme[0][1]
        elif self.imageActuelle == "Joueur_E":
            self.arme.pivoter(180)

            self.arme.rect.x = PlacementArme[1][0]
            self.arme.rect.y = PlacementArme[1][1]
        elif self.imageActuelle == "Joueur_S":
            self.arme.pivoter(90)

            self.arme.rect.x = PlacementArme[2][0]
            self.arme.rect.y = PlacementArme[2][1]
        elif self.imageActuelle == "Joueur_O":
            
            self.arme.pivoter(0)
            self.arme.rect.x = PlacementArme[3][0]
            self.arme.rect.y = PlacementArme[3][1]
    
    
    def creerProjectile(self,ListeProjectiles,PosX,PosY,ProjectilesGroup):
        if self.specialAttack:
            if self.typeArme == "Cutter":
                if self.imageActuelle == "Joueur_N":
                    ListeProjectiles.append(Projectile(0,-PosX+470,-PosY+430,8,1+self.force,"S","Projectile_Cutter",0.5,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_E":
                    ListeProjectiles.append(Projectile(0,-PosX+540,-PosY+475,8,1+self.force,"E","Projectile_Cutter",0.5,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_S":
                    ListeProjectiles.append(Projectile(0,-PosX+480,-PosY+530,8,1+self.force,"N","Projectile_Cutter",0.5,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_O":
                    ListeProjectiles.append(Projectile(0,-PosX+480,-PosY+475,8,1+self.force,"O","Projectile_Cutter",0.5,ProjectilesGroup))
            if self.typeArme == "Brush":
                if self.imageActuelle == "Joueur_N":
                    ListeProjectiles.append(Projectile(7,-PosX+440,-PosY+320,16,2+self.force,"N","Projectile_InkSlash1",1.25,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_E":
                    ListeProjectiles.append(Projectile(7,-PosX+550,-PosY+450,16,2+self.force,"O","Projectile_InkSlash1",1.25,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_S":
                    ListeProjectiles.append(Projectile(7,-PosX+420,-PosY+550,16,2+self.force,"S","Projectile_InkSlash1",1.25,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_O":
                    ListeProjectiles.append(Projectile(7,-PosX+310,-PosY+425,16,2+self.force,"E","Projectile_InkSlash1",1.25,ProjectilesGroup))
            if self.typeArme == "Plume":
                if self.imageActuelle == "Joueur_N":
                    ListeProjectiles.append(Projectile(8,-PosX+410,-PosY+345,6,2+self.force,"S","Projectile_Plume",1.5,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_E":
                    ListeProjectiles.append(Projectile(8,-PosX+520,-PosY+415,6,2+self.force,"E","Projectile_Plume",1.5,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_S":
                    ListeProjectiles.append(Projectile(8,-PosX+420,-PosY+520,6,2+self.force,"N","Projectile_Plume",1.5,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_O":
                    ListeProjectiles.append(Projectile(8,-PosX+310,-PosY+415,6,2+self.force,"O","Projectile_Plume",1.5,ProjectilesGroup))
            if self.typeArme == "Pencil":
                if self.imageActuelle == "Joueur_N":
                    ListeProjectiles.append(Projectile(0,-PosX+440,-PosY+355,7,1.5+self.force,"S","Projectile_Pencil2",1,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_E":
                    ListeProjectiles.append(Projectile(0,-PosX+560,-PosY+445,7,1.5+self.force,"E","Projectile_Pencil2",1,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_S":
                    ListeProjectiles.append(Projectile(0,-PosX+453,-PosY+550,7,1.5+self.force,"N","Projectile_Pencil2",1,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_O":
                    ListeProjectiles.append(Projectile(0,-PosX+340,-PosY+440,7,1.5+self.force,"O","Projectile_Pencil2",1,ProjectilesGroup))

        else:
            
            if self.typeArme == "Plume":
                if self.imageActuelle == "Joueur_N":
                    ListeProjectiles.append(Projectile(0,-PosX+440,-PosY+355,7,1+self.force,"S","Projectile_Plume",1,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_E":
                    ListeProjectiles.append(Projectile(0,-PosX+560,-PosY+445,7,1+self.force,"E","Projectile_Plume",1,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_S":
                    ListeProjectiles.append(Projectile(0,-PosX+453,-PosY+550,7,1+self.force,"N","Projectile_Plume",1,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_O":
                    ListeProjectiles.append(Projectile(0,-PosX+340,-PosY+440,7,1+self.force,"O","Projectile_Plume",1,ProjectilesGroup))

            elif self.typeArme == "Pencil":
                if self.imageActuelle == "Joueur_N":
                    ListeProjectiles.append(Projectile(0,-PosX+470,-PosY+395,7,0.5+self.force,"S","Projectile_Crayon",0.5,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_E":
                    ListeProjectiles.append(Projectile(0,-PosX+565,-PosY+475,7,0.5+self.force,"E","Projectile_Crayon",0.5,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_S":
                    ListeProjectiles.append(Projectile(0,-PosX+488,-PosY+540,7,0.5+self.force,"N","Projectile_Crayon",0.5,ProjectilesGroup))
                elif self.imageActuelle == "Joueur_O":
                    ListeProjectiles.append(Projectile(0,-PosX+380,-PosY+475,7,0.5+self.force,"O","Projectile_Crayon",0.5,ProjectilesGroup))

    def attaque(self,Inputs,vitrine,joueurGroupArme,ListeProjectiles,PosX,PosY,ProjectilesGroup):
        
        self.attackCooldown -= vitrine.clock.get_time()
        
        self.placementArme()

        if self.attack:
            if self.specialAttack:
                compteur=0
                for Frame in self.animationAttack:
                    compteur+=1
                    if self.animationNumber == compteur:
                        if Frame[1] * self.VitesseAttaque < self.animationTimer:
                            self.animationNumber +=1
                            self.animationTimer = 0
                            if Frame[2]:
                                self.creerProjectile(ListeProjectiles,PosX,PosY,ProjectilesGroup)
                            if Frame[3]==1:
                                vitrine.addsprite(joueurGroupArme,"armes")
                                if self.imageActuelle == "Joueur_S":
                                    vitrine.change_layer("armes",3)
                                else:
                                    
                                    vitrine.change_layer("armes",5)
                            elif Frame[3]==2:
                                vitrine.removesprite("armes")
                        else:
                            self.sprite.animate( Frame[0] ,self.imageActuelle + "_Attack",False)
                    elif len(self.animationAttack) <= self.animationNumber:
                        self.attack = False
                        self.sprite.animate( "",self.imageActuelle + "1",False)
                        self.animationNumber = 1
            else:
                compteur=0
                for Frame in self.animationAttack:
                    compteur+=1
                    if self.animationNumber == compteur:
                        if Frame[1] * self.VitesseAttaque < self.animationTimer:
                            self.animationNumber +=1
                            self.animationTimer = 0
                            if Frame[2]:
                                self.creerProjectile(ListeProjectiles,PosX,PosY,ProjectilesGroup)
                            if Frame[3]==1:
                                vitrine.addsprite(joueurGroupArme,"armes")
                                if self.imageActuelle == "Joueur_S":
                                    vitrine.change_layer("armes",6)
                                else:
                                    vitrine.change_layer("armes",3)
                            elif Frame[3]==2:
                                vitrine.removesprite("armes")
                        else:
                            self.sprite.animate( Frame[0] ,self.imageActuelle + "_Attack",False)
                    elif len(self.animationAttack) <= self.animationNumber:
                        self.attack = False
                        self.sprite.animate( "",self.imageActuelle + "1",False)                   
                        self.animationNumber = 1

        if self.attackCooldown <= 0 and not self.attack:
            if Inputs[3][4]:   #Touche E
                peutAttacker = False
                if self.typeArme == "Cutter" and self.encre>5:
                    peutAttacker=True
                    self.encre-=5
                elif self.typeArme == "Pencil" and self.encre>10:
                    peutAttacker=True
                    self.encre-=10
                elif self.typeArme == "Brush" and self.encre>10:
                    peutAttacker=True
                    self.encre-=10
                elif self.typeArme == "Plume" and self.encre>20:
                    peutAttacker=True
                    self.encre-=20
                       
                if peutAttacker:
                    
                    print("atatck special")
                    self.attack = True
                    self.attackCooldown = 800 * self.VitesseAttaque
                    self.sprite.animate(1,self.imageActuelle + "_Attack",False)
                    self.animationTimer = 0
                    self.animationNumber = 1
                    self.specialAttack = True
                    #Information nessaire pour le Verouillage du deplacement du joueur dans CodePrincipale
                    #Cependant le joueur ne peut pas se deplacer pendant les attaques speciales
                    self.directionAttaque = ""

                        
                    #ANIMATION
                    cutter=Musique("Cutter.mp3")
                    pencil=Musique("Pencil.mp3")
                    plume=Musique("Plume.mp3")
                    brush=Musique("Brush.mp3")
                    if self.typeArme == "Cutter":
                        ######### -  Cutter
                         cutter.start(0,8,0.7)
                         self.animationAttack=[(1,50,False,1),(2,100,True,0),(3,100,False,2),(4,50,False,0),(4,50,False,0)]        
                    elif self.typeArme == "Pencil":
                         ######### -  Pencil
                         pencil.start(0,8,0.7)
                         self.animationAttack=[(1,50,True,1),(2,200,False,0),(3,200,False,2),(4,50,False,0),(4,50,False,0)]         
                    elif self.typeArme == "Plume":
                        ######### -  Plume
                         plume.start(0,8,0.7)
                         self.animationAttack=[(1,50,False,1),(2,100,False,0),(3,100,False,0),(2,100,False,0),(3,100,False,0),(2,100,True,0),(3,100,False,2),(4,50,False,0),(4,50,False,0)]               
                    elif self.typeArme == "Brush":
                        ######### -  Brush
                         brush.start(0,8,0.7)
                         self.animationAttack=[(1,50,False,1),(2,100,True,0),(3,100,False,0),(2,100,False,0),(3,100,False,2),(4,50,False,0),(4,50,False,0)]                 
                
            elif Inputs[1]:    #Click Gauche
                print("atatck")
                self.attack = True
                
                self.sprite.animate(1,self.imageActuelle + "_Attack",False)
                self.animationTimer = 0
                self.animationNumber = 1
                self.specialAttack = False
                
                #Information nessaire pour le Verouillage du deplacement du joueur dans CodePrincipale
                if self.imageActuelle == "Joueur_E" or self.imageActuelle == "Joueur_O":
                    self.directionAttaque = "EO"
                else:
                    self.directionAttaque = "NS"
            
                #ANIMATION
                cutter=Musique("Cutter.mp3")
                pencil=Musique("Pencil.mp3")
                plume=Musique("Plume.mp3")
                brush=Musique("Brush.mp3")
                pencil2=Musique("Pencil2.mp3")
                if self.typeArme == "Cutter":
                    ######### -  Cutter
                     cutter.start(0,8,0.7)
                     self.attackCooldown = 800 * self.VitesseAttaque
                     self.animationAttack=[(1,50,False,1),(2,100,False,0),(3,100,False,2),(4,50,False,0),(4,50,False,0)]        
                elif self.typeArme == "Pencil":
                    ######### -  Pencil2
                     pencil2.start(0,8,0.7)
                     self.attackCooldown = 400 * self.VitesseAttaque
                     self.animationAttack=[(1,25,True,1),(2,50,False,0),(3,50,False,2),(4,25,False,0),(4,25,False,0)]       
                elif self.typeArme == "Plume":
                    ######### -  Plume
                     plume.start(0,8,0.7)
                     self.attackCooldown = 1000 * self.VitesseAttaque
                     self.animationAttack=[(1,50,True,1),(2,200,False,0),(3,200,False,2),(4,50,False,0),(4,50,False,0)]                 
                elif self.typeArme == "Brush":
                     self.attackCooldown = 800 * self.VitesseAttaque
                     self.animationAttack=[(1,50,True,1),(2,200,False,0),(3,200,False,2),(4,50,False,0),(4,50,False,0)]   
            
        
        
    def animationJoueur(self,Inputs,Vitrine):
        self.animationTimer += Vitrine.clock.get_time()
        self.degatTimer -= Vitrine.clock.get_time()
        if not self.attack:
            inputHorizontal = (Inputs[3][2] or Inputs[3][3]) and not (Inputs[3][2] and Inputs[3][3]) # porte xOR
            inputVertical = (Inputs[3][0] or Inputs[3][1]) and not (Inputs[3][0] and Inputs[3][1]) # Haut Bas
            imageFinal = "Joueur_"

            if inputVertical:
                if Inputs[3][1]:
                    imageFinal = imageFinal + "S"
                elif Inputs[3][0]:
                    imageFinal = imageFinal + "N"
            elif inputHorizontal:
                if Inputs[3][3]:
                    imageFinal = imageFinal + "E"
                elif Inputs[3][2]:
                    imageFinal =imageFinal + "O"
                    
            if imageFinal != "Joueur_":
                self.imageActuelle = imageFinal
                if self.animationTimer >= 150:
                    self.animationTimer = 0
                    if self.animationNumber ==4:
                        self.animationNumber = 1
                        self.sprite.animate(3,imageFinal ,False)
                    elif self.animationNumber ==3:
                        self.sprite.animate(1,imageFinal ,False)
                        self.animationNumber += 1
                    elif self.animationNumber ==2:
                        self.sprite.animate(2,imageFinal ,False)
                        self.animationNumber += 1
                    else:
                        self.animationNumber +=1
                        self.sprite.animate(1,imageFinal ,False)
            else:
                self.sprite.animate(1,self.imageActuelle,False)

            
            
        

        