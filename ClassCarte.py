from math import *
from random import *
from ClassDisplay import*
from ClassItem import*
from ClassEnnemi import*
import ClassSprite
import pygame,sys,time,random,os
from pygame.locals import *

class Salle:
    """
    Les Objets de la classe Salle représente les tuiles fromants la carte
    Paramètres:
    IDSalle (str) : le type de salle (les ouvertures et tuiles spéciales)
    X (int) : position de la tuile (la tuile fait 720x720 pixel donc est multiplié par 720)
    Y (int) : position de la tuile (la tuile fait 720x720 pixel donc est multiplié par 720)
    fenetre (fenetre de pygame) : vitrine
    GroupArrierePlan (Objet SpriteGroup dans ClassDisplay): SpriteGroup des tuiles
    CarteDuMonde (Objet SpriteGroup dans ClassCarteDuMondeV2): carte
    """
    def __init__(self,IDSalle,X,Y,fenetre,GroupArrierePlan,CarteDuMonde):
        self.type= IDSalle
        self.x = X
        self.y = Y
        self.N = None
        self.E = None
        self.S = None
        self.O = None
        self.objets = []
        self.enemiess = []
        self.carteDuMonde = CarteDuMonde #Objet CarteDuMondeV2 parent de cette objet Salle
        self.portes= [False,False,False,False] #N E S W
        self.collision= None
        self.overlay= None
        self.sprite = None
        self.typeSalle(False)
        
        
    def __str__(self):
        return ("("+str(self.x)+","+str(self.y)+" Salles attachées: ("+str(self.N)+"/"+str(self.E)+"/"+str(self.S)+"/"+str(self.O)+")"+")")
        
    def typeSalle(self,porteBoss):
        
        
        if self.type == "0":
            self.portes= [True,True,True,True]
            self.sprite=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.salles,"NESO_1",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            self.collision=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.hitbox,"NESO_1_Hitbox",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            self.overlay=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.sallesOverlay,"NESO_1_Overlay",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)

            
            
        elif self.type == "TreasureN":
            self.portes= [True,False,False,False]
            self.sprite=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.salles,"TreasureN_1",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            self.collision=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.hitbox,"TreasureN_1_Hitbox",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            self.overlay=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.sallesOverlay,"TreasureN_1_Overlay",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            
            ItemsPossibles = [(1,"Item_BrouillonCoeur"),(2,"Item_Gants"),(3,"Item_Soda"),(4,"Item_Cartouche"),(5,"Item_Gomme"),(6,"Item_Coeur"),(7,"Weapon_Cutter_O"),(8,"Weapon_Plume_O"),(9,"Weapon_Pencil_O"),(10,"Weapon_Brush_O")]
            ItemChoisi = ItemsPossibles[randint(0,len(ItemsPossibles)-1)]
            
            self.objets.append(Item(self.carteDuMonde.tailleCarte*360-90,self.carteDuMonde.tailleCarte*360-90,ItemChoisi[0],ItemChoisi[1],self.carteDuMonde.objets,1,self.x,self.y))
            self.carteDuMonde.item.append(self.objets[len(self.objets)-1])
            
            
        elif self.type == "TreasureTUTO":
            self.portes= [True,False,False,False]
            self.sprite=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.salles,"TreasureN_1",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            self.collision=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.hitbox,"TreasureN_1_Hitbox",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            self.overlay=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.sallesOverlay,"TreasureN_1_Overlay",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            
            ItemsPossibles = [(7,"Weapon_Cutter_O"),(8,"Weapon_Plume_O"),(9,"Weapon_Pencil_O"),(10,"Weapon_Brush_O")]
            ItemChoisi = ItemsPossibles[randint(0,len(ItemsPossibles)-1)]
            
            self.objets.append(Item(self.carteDuMonde.tailleCarte*360-90,self.carteDuMonde.tailleCarte*360-90,ItemChoisi[0],ItemChoisi[1],self.carteDuMonde.objets,1,self.x,self.y))
            self.carteDuMonde.item.append(self.objets[len(self.objets)-1])
            
        elif self.type == "TreasureE":
            self.portes= [True,False,False,False]
            self.sprite=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.salles,"TreasureE_1",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            self.collision=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.hitbox,"TreasureE_1_Hitbox",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            self.overlay=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.sallesOverlay,"TreasureE_1_Overlay",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            
            ItemsPossibles = [(1,"Item_BrouillonCoeur"),(2,"Item_Gants"),(3,"Item_Soda"),(4,"Item_Cartouche"),(5,"Item_Gomme"),(6,"Item_Coeur"),(7,"Weapon_Cutter_O"),(8,"Weapon_Plume_O"),(9,"Weapon_Pencil_O"),(10,"Weapon_Brush_O")]
            ItemChoisi = ItemsPossibles[randint(0,len(ItemsPossibles)-1)]
            
            self.objets.append(Item(self.carteDuMonde.tailleCarte*360-90,self.carteDuMonde.tailleCarte*360-90,ItemChoisi[0],ItemChoisi[1],self.carteDuMonde.objets,1,self.x,self.y))
            self.carteDuMonde.item.append(self.objets[len(self.objets)-1]) 
            
        elif self.type == "Boss":
            if porteBoss != 0:
                self.collision.animate("","BossS_1_Hitbox",True)
                
                if porteBoss == 1:
                    self.enemiess.append(Ennemi(300,100,self.carteDuMonde.ennemiesSprite,self.carteDuMonde.ennemiesHitbox,self.x,self.y,self.carteDuMonde,"Maurice"))
                    self.carteDuMonde.ennemies.append(self.enemiess[len(self.enemiess)-1])
                elif porteBoss == 2:
                    self.enemiess.append(Ennemi(300,300,self.carteDuMonde.ennemiesSprite,self.carteDuMonde.ennemiesHitbox,self.x,self.y,self.carteDuMonde,"Maurice"))
                    self.carteDuMonde.ennemies.append(self.enemiess[len(self.enemiess)-1])
                elif porteBoss == 3:
                    self.enemiess.append(Ennemi(300,300,self.carteDuMonde.ennemiesSprite,self.carteDuMonde.ennemiesHitbox,self.x,self.y,self.carteDuMonde,"Maurice"))
                    self.carteDuMonde.ennemies.append(self.enemiess[len(self.enemiess)-1])
                
            else:
                self.portes= [True,False,False,False]
                self.sprite=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.salles,"BossS_1",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
                self.overlay=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.sallesOverlay,"BossS_1_Overlay",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
                self.collision=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.hitbox,"BossS_1_Hitbox2",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            

        
        else:  
            PorteNord= self.carteDuMonde.AccederPortes(self.x,self.y+1)[2]
            PorteEst= self.carteDuMonde.AccederPortes(self.x+1,self.y)[3]
            PorteSud= self.carteDuMonde.AccederPortes(self.x,self.y-1)[0]
            PorteOuest= self.carteDuMonde.AccederPortes(self.x-1,self.y)[1]
            self.portes= [False,False,False,False]
              
            
            
            
            ##########
            if PorteNord or ((randint(1,2) == 1 and not (self.x,self.y+1) in self.carteDuMonde.coordoneesPrise and self.carteDuMonde.profondeur - len(self.carteDuMonde.salleAGenerer)-1 > 0)):
                string1="N"
                self.portes[0] = True
                if not PorteNord:
                    self.carteDuMonde.salleAGenerer.append((self.x,self.y+1))
            else:
                string1=""
            ##########
            if PorteEst or ((randint(1,2) == 1 and not (self.x+1,self.y) in self.carteDuMonde.coordoneesPrise and self.carteDuMonde.profondeur - len(self.carteDuMonde.salleAGenerer)-1 > 0)):
                string2="E"
                self.portes[1] = True
                if not PorteEst:
                    self.carteDuMonde.salleAGenerer.append((self.x+1,self.y))              
            else:
                string2=""
            ##########
            if PorteSud or ((randint(1,2) == 1 and not (self.x,self.y-1) in self.carteDuMonde.coordoneesPrise and self.carteDuMonde.profondeur - len(self.carteDuMonde.salleAGenerer)-1 > 0)):
                string3="S"
                self.portes[2] = True
                if not PorteSud:
                    self.carteDuMonde.salleAGenerer.append((self.x,self.y-1))
            else:
                string3=""
            ##########
            if PorteOuest or ((randint(1,2) == 1 and not (self.x-1,self.y) in self.carteDuMonde.coordoneesPrise and self.carteDuMonde.profondeur - len(self.carteDuMonde.salleAGenerer)-1 > 0)):
                string4="O"
                self.portes[3] = True
                if not PorteOuest:
                    self.carteDuMonde.salleAGenerer.append((self.x-1,self.y))
            else:
                string4=""
            
            self.type= string1+string2+string3+string4
            NOMSPRITE= string1+string2+string3+string4+"_"+"1"
            if NOMSPRITE == "_1":
                NOMSPRITE = "placeholder"
            self.overlay=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.sallesOverlay,NOMSPRITE+"_Overlay",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            self.sprite=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.salles,NOMSPRITE,0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            self.collision=ClassSprite.Sprite((720*self.carteDuMonde.tailleCarte*self.x,-720*self.carteDuMonde.tailleCarte*self.y),self.carteDuMonde.hitbox,NOMSPRITE+"_Hitbox",0,self.carteDuMonde.tailleCarte,self.carteDuMonde.tailleCarte)
            
    def placerEnnemies(self):
        Spawn =[]
        if self.type == "0":
            print("EE")
#             self.enemiess.append(Ennemi(200,360,self.carteDuMonde.ennemiesSprite,self.carteDuMonde.ennemiesHitbox,self.x,self.y,self.carteDuMonde,"Oeuil"))
#             self.carteDuMonde.ennemies.append(self.enemiess[len(self.enemiess)-1])
            Spawn=[]
        elif self.type == "N":
            Spawn=[(200,200),(200,400),(200,550),(445,435),(545,225),(545,445),(590,580),(445,580)]
        elif self.type == "E":
            Spawn=[(385,350),(435,560),(430,170)]
        elif self.type == "O":
            Spawn=[(400,350)]
        elif self.type == "NESO":
            if not (self.x == 0 and self.y == 0):
                Spawn=[(230,200),(550,200),(550,530),(230,530)]
        elif self.type == "S":
            Spawn=[(190,180),(580,180),(380,180)]
        elif self.type == "NO":
            Spawn=[(370,365),(575,190),(575,550),(205,550),(205,185)]
        elif self.type == "SO":
            Spawn=[(545,170),(340,335),(550,550),(215,550)]
        elif self.type == "NSO":
            Spawn=[(575,150),(570,550),(350,350),(185,165),(185,555)]
        elif self.type == "NEO":
            Spawn=[(540,190),(215,170),(225,550),(540,550)]
        elif self.type == "NES":
            Spawn=[(385,350)]

        return Spawn
        

        



class CarteDuMondeV2:
    """
    Les Objets de la classe CarteDuMondeV2 représente la carte 
    Paramètres:
    profondeur (int) : Inutile
    TailleCarte (int) : Multiplicateur pour la taille des tuiles
    fenetre (fenetre de pygame) : vitrine
    """
    def __init__(self,profondeur,fenetre,TailleCarte):
        
        if profondeur == -1:
            #Creation manuelle du tutoriel
            self.tailleCarte=TailleCarte
            self.coordoneesPrise = [(0,0),(1,0),(-1,0)]
            self.profondeur = profondeur
            self.salleAGenerer = []
            self.SalleTresor =1
            self.EnemiesKills = 0
            
            
            self.salles=pygame.sprite.Group()
            self.hitbox=pygame.sprite.Group()
            self.sallesOverlay=pygame.sprite.Group()
            self.objets=pygame.sprite.Group()
            self.ennemiesSprite=pygame.sprite.Group()
            self.ennemiesHitbox=pygame.sprite.Group()
            
            fenetre.addsprite(self.salles,"salles")
            fenetre.addsprite(self.sallesOverlay,"sallesOverlay")
            fenetre.addsprite(self.objets,"items")
            fenetre.addsprite(self.ennemiesSprite,"ennemi")
            
            self.map = [] #liste de tous les objets Salles
            self.item = [] #liste de tous les objets Items
            self.ennemies = [] #liste de tous les objets Ennemi
            
            #Creation des salles
            
            self.map.append(Salle("0",0,0,fenetre,self.salles,self))
            self.map.append(Salle("S",0,1,fenetre,self.salles,self))
            self.generationTresor(fenetre,True)
            self.generationBoss(fenetre)
            self.map.append(Salle("",-1,0,fenetre,self.salles,self))
            self.map.append(Salle("",1,0,fenetre,self.salles,self))
            self.item.append(Item(470,750,11,"Notes",self.objets,0.5,0,0))
            self.item.append(Item(-100,450,12,"Notes",self.objets,0.5,0,0))
            self.item.append(Item(1200,450,13,"Notes",self.objets,0.5,0,0))
            self.item.append(Item(470,-500,14,"Notes",self.objets,0.5,0,0))
            self.item.append(Item(470,-1000,15,"Notes",self.objets,0.5,0,0))
        else:
            #Generation aleatoire
            self.tailleCarte=TailleCarte
            self.coordoneesPrise = [(0,0),()] #coordonees des salles deja generes
            self.profondeur = profondeur
            self.salleAGenerer = []
            self.SalleTresor =1
            self.NombreEnemies = 0
            self.EnemiesCota=0
            
            
            self.salles=pygame.sprite.Group()
            self.hitbox=pygame.sprite.Group()
            self.sallesOverlay=pygame.sprite.Group()
            self.objets=pygame.sprite.Group()
            self.ennemiesSprite=pygame.sprite.Group()
            self.ennemiesHitbox=pygame.sprite.Group()
            
            fenetre.addsprite(self.salles,"salles")
            fenetre.addsprite(self.sallesOverlay,"sallesOverlay")
            fenetre.addsprite(self.objets,"items")
            fenetre.addsprite(self.ennemiesSprite,"ennemi")

    #         fenetre.addsprite(self.hitbox,"hitbox")
            
            self.map = [] #liste de tous les objets Salles
            self.item = [] #liste de tous les objets Items
            self.ennemies = [] #liste de tous les objets Ennemi
            
            self.map.append(Salle("0",0,0,fenetre,self.salles,self)) #creation de la salle centrale

    def generationCarte(self,iteration,fenetre,profondeur):
        self.profondeur=profondeur
        self.SalleTresor =1
        while iteration > 0 and self.profondeur > 0:
            for j in range(len(self.map)):
                i=self.map[j-1]
                
                
                ####Generation d'une salle au nord de la Salle i
                if i.portes[0] == True and self.profondeur > 0: #si la salle selectionne a une porte Nord et qu'il reste encore des salles a generer    
                    if not (i.x,i.y+1) in self.coordoneesPrise: #verifie si la salle n'existe pas deja
                        self.coordoneesPrise.append((i.x,i.y+1))
                        self.map.append(Salle("",i.x,i.y+1,fenetre,self.salles,self))
                        #reduit le compteur de salle restante a generer de 1
                        self.profondeur -=1
                        #suprime toutes les requettes de generation d'une salle au coordone
                        if (i.x,i.y+1) in self.salleAGenerer:
                            for j in self.salleAGenerer:
                                if j == (i.x,i.y+1):
                                    self.salleAGenerer.pop(self.salleAGenerer.index(j))
                                    
                ####Generation d'une salle a l'est de la Salle i     
                if i.portes[1] == True and self.profondeur > 0:
                    if not (i.x+1,i.y) in self.coordoneesPrise:
                        self.coordoneesPrise.append((i.x+1,i.y))
                        self.profondeur -=1
                        self.map.append(Salle("",i.x+1,i.y,fenetre,self.salles,self))
                        if (i.x+1,i.y) in self.salleAGenerer:
                            for j in self.salleAGenerer:
                                if j == (i.x+1,i.y):
                                    self.salleAGenerer.pop(self.salleAGenerer.index(j))

                ####Generation d'une salle au sud de la Salle i
                if i.portes[2] == True and self.profondeur > 0:
                    if not (i.x,i.y-1) in self.coordoneesPrise:
                        self.coordoneesPrise.append((i.x,i.y-1))
                        self.profondeur -=1
                        self.map.append(Salle("",i.x,i.y-1,fenetre,self.salles,self))
                        if (i.x,i.y-1) in self.salleAGenerer:
                            for j in self.salleAGenerer:
                                if j == (i.x,i.y-1):
                                    self.salleAGenerer.pop(self.salleAGenerer.index(j))
                
                ####Generation d'une salle a l'ouest de la Salle i
                if i.portes[3] == True and self.profondeur > 0:
                    if not (i.x-1,i.y) in self.coordoneesPrise:
                        self.coordoneesPrise.append((i.x-1,i.y))
                        self.profondeur -=1
                        self.map.append(Salle("",i.x-1,i.y,fenetre,self.salles,self))
                        if (i.x-1,i.y) in self.salleAGenerer:
                            for j in self.salleAGenerer:
                                if j == (i.x-1,i.y):
                                    self.salleAGenerer.pop(self.salleAGenerer.index(j))
            
            #compteur pour eviter le risque de boucle infini
            iteration = iteration-1
        self.generationTresor(fenetre)
        self.generationTresor2(fenetre)
        self.generationBoss(fenetre)

        
    def generationTresor2(self,fenetre):
        #Generation d'une salle de tresor
        tuilesLesPlusBasses=[]
        hauteurMin= self.map[0].x
        for i in self.map:
            if hauteurMin > i.x:
                hauteurMin = i.x
        for i in self.map:
            if i.x == hauteurMin and not i.type =="TreasureN":
                tuilesLesPlusBasses.append(i)
                
        tuilesSelectionne = tuilesLesPlusBasses[randint(0,len(tuilesLesPlusBasses)-1)]
        if tuilesSelectionne.portes[0]:
            string1="N"
        else:
            string1=""
        ##########
        if tuilesSelectionne.portes[1]:
            string2="E"
       
        else:
            string2=""
        ##########
            
        if tuilesSelectionne.portes[2]:
            string3="S"
       
        else:
            string3=""
        ##########

        string4="O"
            
        tuilesSelectionne.type= string1+string2+string3+string4
        NOMSPRITE= string1+string2+string3+string4+"_"+"1"
        tuilesSelectionne.sprite.animate("" ,NOMSPRITE)
        tuilesSelectionne.overlay.animate("" ,NOMSPRITE + "_Overlay")
        tuilesSelectionne.collision.animate("" ,NOMSPRITE + "_Hitbox",True)
        
        self.coordoneesPrise.append((tuilesSelectionne.x-1,tuilesSelectionne.y))
        self.map.append(Salle("TreasureE",tuilesSelectionne.x-1,tuilesSelectionne.y,fenetre,self.salles,self))
            
    def generationBoss(self,fenetre):
        #Generation d'une salle de Boss
        tuilesLesPlusBasses=[]
        hauteurMax= self.map[0].y
        for i in self.map:
            if hauteurMax < i.y:
                hauteurMax = i.y
        for i in self.map:
            if i.y == hauteurMax and not i.type == "TreasureN" and not i.type == "TreasureE":
                tuilesLesPlusBasses.append(i)
                
        tuilesSelectionne = tuilesLesPlusBasses[randint(0,len(tuilesLesPlusBasses)-1)]
        
        string1="N"

        ##########
        if tuilesSelectionne.portes[1]:
            string2="E"
       
        else:
            string2=""
        ##########
        if tuilesSelectionne.portes[2]:
            string3="S"
       
        else:
            string3=""
        ##########
        if tuilesSelectionne.portes[3]:
            string4="O"
        else:
            string4=""
            
        tuilesSelectionne.type= string1+string2+string3+string4
        NOMSPRITE= string1+string2+string3+string4+"_"+"1"
        tuilesSelectionne.sprite.animate("" ,NOMSPRITE)
        tuilesSelectionne.overlay.animate("" ,NOMSPRITE + "_Overlay")
        tuilesSelectionne.collision.animate("" ,NOMSPRITE + "_Hitbox",True)
        
        self.coordoneesPrise.append((tuilesSelectionne.x,tuilesSelectionne.y+1))
        self.map.append(Salle("Boss",tuilesSelectionne.x,tuilesSelectionne.y+1,fenetre,self.salles,self))
        
        
        
    def generationTresor(self,fenetre,tuto=False):
        #Generation d'une salle de tresor
        tuilesLesPlusBasses=[]
        hauteurMin= self.map[0].y
        for i in self.map:
            if hauteurMin > i.y:
                hauteurMin = i.y
        for i in self.map:
            if i.y == hauteurMin:
                tuilesLesPlusBasses.append(i)
                
        tuilesSelectionne = tuilesLesPlusBasses[randint(0,len(tuilesLesPlusBasses)-1)]
        if tuilesSelectionne.portes[0]:
            string1="N"
        else:
            string1=""
        ##########
        if tuilesSelectionne.portes[1]:
            string2="E"
       
        else:
            string2=""
        ##########
            
        string3="S"
        ##########
        if tuilesSelectionne.portes[3]:
            string4="O"
        else:
            string4=""
            
        tuilesSelectionne.type= string1+string2+string3+string4
        NOMSPRITE= string1+string2+string3+string4+"_"+"1"
        tuilesSelectionne.sprite.animate("" ,NOMSPRITE)
        tuilesSelectionne.overlay.animate("" ,NOMSPRITE + "_Overlay")
        tuilesSelectionne.collision.animate("" ,NOMSPRITE + "_Hitbox",True)
        
        self.coordoneesPrise.append((tuilesSelectionne.x,tuilesSelectionne.y-1))
        if tuto:
            self.map.append(Salle("TreasureTUTO",tuilesSelectionne.x,tuilesSelectionne.y-1,fenetre,self.salles,self))
        else:
            self.map.append(Salle("TreasureN",tuilesSelectionne.x,tuilesSelectionne.y-1,fenetre,self.salles,self))
        
    def porteBoss(self,estOuverte):
        #Ouverture de la porte du boss
        if estOuverte !=0:
            for i in self.map:
                if i.type == "Boss":
                    i.typeSalle(estOuverte)
        
        
    def PlacerEnemies(self,NombreEnemies,EnemiesCota,NIVEAU):
        self.NombreEnemies = NombreEnemies
        self.EnemiesCota = EnemiesCota
        self.EnemiesKills = 0
        #On fait une liste de tous les emplacement possible ou un kmonstre peut apparaitre
        PossitionnementPossible = []
        for i in self.map:
            for j in i.placerEnnemies():
                PossitionnementPossible.append([i,j])
        
        #On choisit ensuite aleatoirement
        
        for i in range(self.NombreEnemies):
            if not PossitionnementPossible == []:
                if NIVEAU == 0:
                    Monstre=choice(["Cube2"])
                if NIVEAU == 1:
                    Monstre=choice(["Stickman","Stickman","Stickman","Cube"])
                if NIVEAU == 2:
                    Monstre=choice(["Stickman","Stickman","Stickman","Stickman","Cube","Cube","Cube","Main"])
                if NIVEAU == 3:
                    Monstre=choice(["Stickman","Stickman","Stickman","Cube","Cube","Cubisme","Cubisme","Cubisme"])
                if NIVEAU == 4:
                    Monstre=choice(["Stickman","Stickman","Cube","Cubisme","Cubisme","Main","Oeuil"])
                if NIVEAU == 5:
                    Monstre=choice(["Stickman","Stickman","Cube","Cubisme","Oeuil"])
                if NIVEAU == 6:
                    Monstre=choice(["Stickman","Cube","Cubisme","Oeuil","Main"]) 
                randomInt = randint(0,len(PossitionnementPossible)-1)
                salleChoisi=PossitionnementPossible[randomInt][0]
                cooChoisi=PossitionnementPossible[randomInt][1]
                salleChoisi.enemiess.append(Ennemi(cooChoisi[0]-100,cooChoisi[1]-100,self.ennemiesSprite,self.ennemiesHitbox,salleChoisi.x,salleChoisi.y,self,Monstre))
                salleChoisi.carteDuMonde.ennemies.append(salleChoisi.enemiess[len(salleChoisi.enemiess)-1])
                PossitionnementPossible.pop(randomInt)
        
        #Stickmann 10
        #Cube 8
        #Oeuil 5
        #Cubisme 4
        #Main 2
            
            
    def AccederPortes(self,X,Y):
        for i in self.map:
            if i.x == X and i.y == Y:
                return i.portes
        return [False,False,False,False]
            
                

# carte = CarteDuMonde(20,20)
# carte.generationCarte()
# carte.debugAffichage()


