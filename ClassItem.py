# créé par Léane

import pygame
from ClassSprite import *
from ClassDisplay import *
from ClassMusique import *
import sys
from ClassCoeur import *


class Item:
    """
    création d'une instance item:
        item = Item(pos_x(int), pos_y(int), type_item(int), sprite(png), spritegroup(), scale(int))
    attributs d'instance: pos_x, pos_y, type_item, sprite

    type d'item:
        1: donne de l'armure (coeur temporaire)
        2: augmente la vitesse d'attaque
        3: augmente la vitesse de mouvement
        4: augmente la capacité d'encre
        5: augmente l'attaque
        6: ajoute un coeur permanent

    méthodes:
        joueur_touche: test si l'item est touché par le joueur
        modife_joueur: effectue les changements aux stat que l'item amène
        item_desc: affiche une description de l'item qui comprend son nom et son effet
    """

    def __init__(self, pos_x, pos_y, type_item, image, spritegroup, scale, salleX, salleY):
        self.x = pos_x
        self.y = pos_y
        self.type = type_item
        self.salleX = salleX
        self.salleY = salleY
        self.timer = 0
        self.objet = Sprite((self.x, self.y), spritegroup, image, 0, scale, scale)
        self.timerDelai = 0
        
        #Item armes
        if self.type > 6:
            self.objet.pivoter(45)

    def joueur_touche(self, joueur):
        if joueur.hitbox.collidemask(self.objet.rect, self.objet.mask, None)[0]:
            return True
        else:
            return False
        
    def modife_joueur(self, joueur, Inputs, vitrine,packetCoeur,carte):
        
        if self.joueur_touche(joueur) == True:

            if self.type <7:
                self.objet.kill()
            if self.type == 1:  # coeur temporaire
                joueur.armure += 3
                packetCoeur[0].append(Coeur(len(packetCoeur[0]), packetCoeur[1], joueur))
                packetCoeur[0].append(Coeur(len(packetCoeur[0]), packetCoeur[1], joueur))
                packetCoeur[0].append(Coeur(len(packetCoeur[0]), packetCoeur[1], joueur))
                self.objet.killsprite()
                return ([1, "brouillon de coeur: donne 1 coeur temporaire."])

            elif self.type == 2:#vitesse d'attaque
                joueur.VitesseAttaque -= 0.1
                self.objet.killsprite()
                return ([1, "gants pour tablette: augmente la vitesse d'attaque."])


            elif self.type == 3:#vitesse de mouvement
                joueur.vitesse += 1
                self.objet.killsprite()
                return ([1, "boisson énergisante: augmente la vitesse de mouvement."])

            elif self.type == 4:#capactié d'encre
                joueur.encreMax += 25
                self.objet.killsprite()
                return ([1, "cartouche d'encre: augmente la capacité d'encre."])


            elif self.type == 5:#augmente l'attaque
                joueur.force += 0.5
                self.objet.killsprite()
                return ([1, "gomme: augmente les dégâts infligés."])

            elif self.type == 6:#coeur permanent
                joueur.pvMax += 1
                packetCoeur[0].append(Coeur(len(packetCoeur[0]), packetCoeur[1], joueur))
                self.objet.killsprite()
                return ([1, "coeur vide: augement le nombre de coeurs permanents."])
            
            ######Armes
            


            
        if self.type > 6 and self.timerDelai < 0 and self.joueur_touche(joueur) == True:

            self.timerDelai = 1000
            joueurArme= joueur.typeArme
            
            
            if self.type==7: #Cutter
                joueur.typeArme = "Cutter"
            elif self.type==8: #Plume
                joueur.typeArme = "Plume"
            elif self.type==9: #Pencil
                joueur.typeArme = "Pencil"
            elif self.type==10: #Brush
                joueur.typeArme = "Brush"
            elif self.type==11:
                self.objet.killsprite()
                return ([1, "Bonjour Artiste, on dirait que tu as plongé dans   ton dessin.                                        Cependant ne perd pas espoir: il est toujours      possible de s'en sortir dans les moments difficiles.                                                  Equipe-toi dans la salle dorée et persévère."])
            elif self.type==12:
                self.objet.killsprite()
                return ([1, " > Clic gauche pour une attaque normale."])
            elif self.type==13:
                self.objet.killsprite()
                return ([1, " > Touche [E] pour une attaque spéciale qui consomme de l'encre."])
            elif self.type==14:
                self.objet.killsprite()
                return ([1, " > Tu a pris des dégâts?                            Maintenir [F] pour se soigner en utilisant de       l'encre."])
            elif self.type==15:
                self.objet.killsprite()
                return ([1, "La jauge de la porte semble indiquer la quantité d'ennemis restant à éliminer avant de pouvoir l'ouvrir."])
     
            
            if joueurArme== "Cutter":
                self.objet.animate("","Weapon_Cutter_O",False)
                self.objet.pivoter(45)
                self.type= 7
            elif joueurArme == "Plume":
                self.type= 8
                self.objet.animate("","Weapon_Plume_O",False)
                self.objet.pivoter(45)
            elif joueurArme == "Pencil":
                self.type= 9
                self.objet.animate("","Weapon_Pencil_O",False)
                self.objet.pivoter(45)
            elif joueurArme == "Brush":
                self.type= 10
                self.objet.animate("","Weapon_Brush_O",False)
                self.objet.pivoter(45)
            elif joueurArme == "":
                self.objet.killsprite()
                carte.item.pop(carte.item.index(self))
            
            if joueur.typeArme== "Cutter":
                return ([1, "cutter: arme très efficace au corps à corps."])
            elif joueur.typeArme == "Plume":
                return ([1, "plume: arme très efficace à distance."])
            elif joueur.typeArme == "Pencil":
                return ([1, "crayon: arme très rapide."])
            elif joueur.typeArme == "Brush":
                return ([1, "pinceau: arme de corps à corps."])

            else:
                return (0, "")
        else:
            return (0, "")