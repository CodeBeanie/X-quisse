from math import *
from random import *
from ClassDisplay import *
from ClassPersonnage import *
from ClassCoeur import *
import ClassSprite
import pygame, sys, time, random, os
from pygame.locals import *
from ClassCarte import *
from ClassProjectile import *
from ClassParticule import *
from ClassBlob import *
from ClassMusique import *
from mainscreen import *
from time import sleep
mainmenu1=mainmenu((1,1),60)
maininputs=mainmenu1.openmenu()
if maininputs=='yes kill yourself':
    quit()
vitrine = Fenetre((1000, 1000), 60, maininputs, 24)

###Creation des Groupes de Sprites
joueurGroup = pygame.sprite.Group()  # Groupe pour les sprites du joueur
joueurGroupArme = pygame.sprite.Group()
joueurHitboxGroup = pygame.sprite.Group()  # Groupe pour la hitbox du joueur
groupBlob = pygame.sprite.Group()
UI = pygame.sprite.Group()  # Groupe pour l'interfaces visuelle
ProjectilesGroup = pygame.sprite.Group()
ParticuleGroup = pygame.sprite.Group()
GroupPorte = pygame.sprite.Group()
GroupTransition = pygame.sprite.Group()
GroupFin = pygame.sprite.Group()

###Mets les groupes ci-dessous dans la liste d'affichage
vitrine.addsprite(joueurGroupArme, "armes")
vitrine.addsprite(joueurGroup, "joueur")
vitrine.addsprite(UI, "UI")
vitrine.addsprite(ProjectilesGroup, "Projectiles")
vitrine.addsprite(ParticuleGroup, "Particules")
vitrine.addsprite(groupBlob, "Blob")
vitrine.addsprite(GroupPorte, "GroupPorte")

###Musique


door1=Musique("Door1.mp3")
door2=Musique("Door2.mp3")
door3=Musique("Door3.mp3")
door_sound=[door1,door2,door3]
trapdoor=Musique("TrapDoor.mp3")
heal=Musique("Heal.mp3")
intro = Musique("Intro.mp3")
boucle = Musique("Loop.mp3")



listosounds=[door1,door2,door3,trapdoor,heal,intro,boucle]

###Initialisation de la carte
TailleCarte = 1.5  # La taille par default des tuiles est de 720 x 720 pixel, TailleCarte est simplement un multiplicateur (ex: TailleCarte = 2, il y aura des tuilles de 1440 x 1440 pixel)
carte = CarteDuMondeV2(-1, vitrine, TailleCarte)
carte.PlacerEnemies(2,2,0)

# carte = CarteDuMondeV2(5, vitrine, TailleCarte)
# carte.generationCarte(10, vitrine, 10)
# carte.PlacerEnemies(10,1)

###
vitrine.change_layer("GroupPorte", 15)
vitrine.change_layer("Particules", 15)
vitrine.change_layer("Blob", 15)
vitrine.change_layer("Projectiles", 15)
vitrine.change_layer("joueur", 15)
vitrine.change_layer("ennemi", 15)
vitrine.change_layer("sallesOverlay", 15)
vitrine.change_layer("UI", 15)

###Variables du jeu
GameState = 1  # 0: Menu Principale  0.5: Tutoriel 1: Jeux
PosX = -35
PosY = -35
ProgressionSoin = 0
joueur = Personnage(joueurGroup, joueurHitboxGroup, joueurGroupArme)
Coeurs = [Coeur(i, UI, joueur) for i in range(joueur.pvMax)]
ListeProjectiles = []
ListeParticule = []
ListeBlob = []
DimensionEcran = pygame.display.get_desktop_sizes()[len(pygame.display.get_desktop_sizes()) - 1]  # Prends les dimensions de l'ecran
InkFiller = ClassSprite.Sprite((120, 625), UI, "InkMeterFiling", 0, 1, 1)
InkBar = ClassSprite.Sprite((100, 500), UI, "InkMeter", 0, 1, 1)
PeutBouger = True
Text = ""
TextFini = False
TextAttente = 0
vitrine.removesprite("armes")
NIVEAU = 0


for i in carte.map:
    if i.type== "Boss":
        PorteX=i.x
        PorteY=i.y
        BossRoom = i

PorteOffsetX = 0
PorteOffsetY = 0

PorteBossFiller = ClassSprite.Sprite((720 * TailleCarte * PorteX + PosX + 440 ,720 * TailleCarte * PorteY + PosY + 440  ), GroupPorte, "BossDoorFilling", 0, 0.5 , 0.25 )
PorteBoss = ClassSprite.Sprite((720 * TailleCarte * PorteX + PosX + 440 ,720 * TailleCarte * PorteY + PosY + 440  ), GroupPorte, "BossDoor", 0, TailleCarte , TailleCarte )
TrapBoss = ClassSprite.Sprite((720 * TailleCarte * PorteX + PosX + 440 ,720 * TailleCarte * PorteY + PosY + 440  ), GroupPorte, "Trapdoor1", 0, 0.5 , 0.5 )
Transition = ClassSprite.Sprite((0,0), GroupTransition, "Transition", 0, 1 , 1 )
TransitionTimer=0
TrapTimer = 0
TrapAnimation = 1
Fin = ClassSprite.Sprite((500,500), GroupFin, "Tombe", 0, 5 , 5 )

# # # # # # # # # # # # # # # 
listosounds[5].start(0,1,0.1)

while True:
    listosounds[6].start(-1,1,0.1)
    Inputs = vitrine.events()
    vitrine.updatedisplay()
    multiplicateurFPS = 60 / (Inputs[0] + 0.1)  # afin que le lag sur des machine moins performantes n'affectent pas la vitesse deplacement et autres
    if multiplicateurFPS > 100:
        multiplicateurFPS=1

    
    if GameState == 0.5:
        
        TransitionTimer+=vitrine.clock.get_time()
        if TransitionTimer <500:
            
            print("E")
            vitrine.addsprite(GroupTransition, "Transition")
            vitrine.change_layer("Transition", 15)
            Transition.echelle(1,TransitionTimer/500)
            Transition.rect.x =0
            Transition.rect.y = 0
        elif TransitionTimer >500 and TransitionTimer<750:
            Transition.echelle(1,1)
            for i in carte.ennemies:
                i.sprite.kill()
                i.hitbox.kill()
                del(i)
            for i in carte.item:
                i.objet.kill()
                del(i)
            for i in carte.map:
                i.collision.kill()
                i.sprite.kill()
                i.overlay.kill()
                del(i)
            for i in ListeProjectiles:
                i.Objet.kill()
                del(i)
            for i in ListeParticule:
                i.sprite.kill()
                del(i)
            for i in ListeBlob:
                i.sprite.kill()
                del(i)
            PorteBossFiller.kill()
            PorteBoss.kill()
            TrapBoss.kill()
            TrapTimer = 0
            TrapAnimation = 1
            PorteOffsetX = 0
            PorteOffsetY = 0

            PosX = -35
            PosY = -35
            ProgressionSoin = 0
            ListeProjectiles = []
            ListeParticule = []
            ListeBlob = []
            

            NIVEAU +=1
            if NIVEAU == 1:
                carte = CarteDuMondeV2(5, vitrine, TailleCarte)
                carte.generationCarte(10, vitrine, 8)
                carte.PlacerEnemies(6,5,NIVEAU)
            elif NIVEAU == 2:
                carte = CarteDuMondeV2(5, vitrine, TailleCarte)
                carte.generationCarte(10, vitrine, 12)
                carte.PlacerEnemies(8,5,NIVEAU)
            elif NIVEAU == 3:
                carte = CarteDuMondeV2(5, vitrine, TailleCarte)
                carte.generationCarte(10, vitrine, 15)
                carte.PlacerEnemies(10,7,NIVEAU)
            elif NIVEAU == 4:
                carte = CarteDuMondeV2(5, vitrine, TailleCarte)
                carte.generationCarte(10, vitrine, 20)
                carte.PlacerEnemies(15,10,NIVEAU)
            elif NIVEAU == 5:
                carte = CarteDuMondeV2(5, vitrine, TailleCarte)
                carte.generationCarte(10, vitrine, 25)
                carte.PlacerEnemies(20,15,NIVEAU)
            elif NIVEAU == 6:
                carte = CarteDuMondeV2(5, vitrine, TailleCarte)
                carte.generationCarte(10, vitrine, 30)
                carte.PlacerEnemies(25,20,NIVEAU)
            elif NIVEAU == 7:
                vitrine.addsprite(GroupFin, "Fin")
                vitrine.change_layer("Fin", 15)
                GameState = 2
                TextAttente = 0
                vitrine.reset_text(50)
                TransitionTimer = 0
                
            for i in carte.map:
                if i.type== "Boss":
                    PorteX=i.x
                    PorteY=i.y
                    BossRoom = i
            PorteBossFiller = ClassSprite.Sprite((720 * TailleCarte * PorteX + PosX + 440 ,720 * TailleCarte * PorteY + PosY + 440  ), GroupPorte, "BossDoorFilling", 0, 0.5 , 0.25 )
            PorteBoss = ClassSprite.Sprite((720 * TailleCarte * PorteX + PosX + 440 ,720 * TailleCarte * PorteY + PosY + 440  ), GroupPorte, "BossDoor", 0, TailleCarte , TailleCarte )
            TrapBoss = ClassSprite.Sprite((720 * TailleCarte * PorteX + PosX + 440 ,720 * TailleCarte * PorteY + PosY + 440  ), GroupPorte, "Trapdoor1", 0, 0.5 , 0.5 )
            TransitionTimer = 750
            
        elif TransitionTimer >750:
            Transition.rect.x =0
            Transition.rect.y = 0
            print(TransitionTimer)
            GameState = 1

    elif GameState == 1:

        if TransitionTimer >750 and TransitionTimer <10000:
            TransitionTimer=10001
        elif TransitionTimer >10000 and TransitionTimer <10500:
            vitrine.addsprite(GroupTransition, "Transition")
            vitrine.change_layer("Transition", 15)
            Transition.rect.y = 1000*(TransitionTimer-10000)/500
            TransitionTimer+=vitrine.clock.get_time()
        elif TransitionTimer >10500:
            vitrine.removesprite("Transition")
            TransitionTimer = 0

            

            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # Rafraichissement des objets
        compteur = 0
        Modif=[0,""]
        for i in carte.item:
            i.objet.rect.x = 720 * TailleCarte * carte.item[compteur].salleX + PosX + carte.item[compteur].x
            i.objet.rect.y = -720 * TailleCarte * carte.item[compteur].salleY + PosY + carte.item[compteur].y
            if PeutBouger:
                i.timerDelai -= vitrine.clock.get_time()
            
            Temp = i.modife_joueur(joueur, Inputs, vitrine,[Coeurs,UI],carte)
            if Temp[1] != "":
                Modif = Temp
            types = Modif[0]


            # Supresiion des items
            if i.joueur_touche(joueur):
                if i.type <7 or i.type >10:
                    carte.item.pop(carte.item.index(i))
            compteur += 1
        compteur = 0


        if Modif[1] == "":
            if not Text == "":
                print("Door1")
                TextFini = False
                PeutBouger = False
                if vitrine.text(Text, (30, 800), 20):
                    print("Door2")
                    TextFini = True
                    TextAttente = 0
                    Text = ""

        else:
            Text, Modif[1] = Modif[1], ""

        TextAttente += vitrine.clock.get_time()
        if TextFini:
            if Inputs[1] and TextAttente > 1000:
                vitrine.reset_text(24)
                TextFini = False
                PeutBouger = True
            elif TextAttente > 5000:
                vitrine.reset_text(24)
                TextFini = False
                PeutBouger = True
        # Attaque du joueur
        if PeutBouger and joueur.typeArme != "":
            joueur.attaque(Inputs, vitrine, joueurGroupArme, ListeProjectiles,PosX,PosY,ProjectilesGroup)

        # Rafraichissement des ennemies

        if PeutBouger:
            for i in carte.ennemies:
                
                distanceX = 720*TailleCarte*i.salleX+i.x-TailleCarte*360 + PosX+150
                distanceY = -720*TailleCarte*i.salleY+i.y-TailleCarte*360 + PosY+150
                TotalDistance = sqrt(distanceX **2 + distanceY ** 2)
                if TotalDistance<800:
                
                    i.sprite.rect.x = 720 * TailleCarte * i.salleX + PosX + i.x + i.offsetX
                    i.hitbox.rect.x = 720 * TailleCarte * i.salleX + PosX + i.x + i.offsetX
                    i.sprite.rect.y = -720 * TailleCarte * i.salleY + PosY + i.y + i.offsetY
                    i.hitbox.rect.y = -720 * TailleCarte * i.salleY + PosY + i.y + i.offsetY
                    i.comportement(carte, joueur, PosX, PosY, TailleCarte, vitrine, ListeProjectiles, ProjectilesGroup,[BossRoom,carte])
                    i.degatEnemie(joueur, vitrine, carte, ListeBlob, groupBlob, TailleCarte, ListeParticule, ParticuleGroup,0)
                    i.sprite.rect.x = 720 * TailleCarte * i.salleX + PosX + i.x + i.offsetX
                    i.hitbox.rect.x = 720 * TailleCarte * i.salleX + PosX + i.x + i.offsetX
                    i.sprite.rect.y = -720 * TailleCarte * i.salleY + PosY + i.y + i.offsetY
                    i.hitbox.rect.y = -720 * TailleCarte * i.salleY + PosY + i.y + i.offsetY
                    compteur += 1
                compteur = 0

        # Rafraichissement des salles
        compteur = 0
        for i in carte.salles:
            i.rect.x = 720 * TailleCarte * carte.map[compteur].x + PosX
            i.rect.y = -720 * TailleCarte * carte.map[compteur].y + PosY
            compteur += 1
        compteur = 0
        for i in carte.hitbox:
            i.rect.x = 720 * TailleCarte * carte.map[compteur].x + PosX
            i.rect.y = -720 * TailleCarte * carte.map[compteur].y + PosY
            compteur += 1
        compteur = 0
        for i in carte.sallesOverlay:
            i.rect.x = 720 * TailleCarte * carte.map[compteur].x + PosX
            i.rect.y = -720 * TailleCarte * carte.map[compteur].y + PosY
            compteur += 1
        compteur = 0

        #Rafraichissemnt Porte de Boss


        if not carte.EnemiesKills >= carte.EnemiesCota:
            PorteBossFiller.echelle(0.1 + 2.1 * (carte.EnemiesKills / carte.EnemiesCota),0.8)
        else:
            PorteBossFiller.echelle(2.2 ,0.8)
            
        PorteAttacked=False
        PorteOffsetX +=  -PorteOffsetX *0.3
        PorteOffsetY +=  -PorteOffsetY *0.3
        

        if PorteBoss.collidemask(joueur.arme.rect,joueur.arme.mask,None)[0] and joueur.attack:
            PorteAttacked=True
            
        if PorteAttacked:
            PorteOffsetX = randint(-5,5)
            PorteOffsetY = randint(-5,5)
            
            ######### -  Door 1 2 3
            choice(listosounds[:3]).start(0,10)
            
            if carte.EnemiesKills >= carte.EnemiesCota:
                carte.EnemiesCota = 9999 # PorteOuverte / Boss apparu
                PorteBoss.kill()
                PorteBossFiller.kill()
                if NIVEAU == 2 or NIVEAU == 4 or NIVEAU == 6:
                    carte.porteBoss(1)
                else:
                    carte.porteBoss(-1)
        PorteBossFiller.rect.x = 720 * TailleCarte * PorteX + PosX + 485 + PorteOffsetX
        PorteBossFiller.rect.y = -720 * TailleCarte * PorteY + PosY + 1094 + PorteOffsetY
        PorteBoss.rect.x = 720 * TailleCarte * PorteX + PosX + 390 + PorteOffsetX
        PorteBoss.rect.y = -720 * TailleCarte * PorteY + PosY + 950 + PorteOffsetY
        
        TrapBoss.rect.x = 720 * TailleCarte * PorteX + PosX + 420
        TrapBoss.rect.y = -720 * TailleCarte * PorteY + PosY + 470
        
        BossEnVie = True
        if carte.EnemiesCota == 9999:
            BossEnVie = False
            for i in carte.ennemies:
                if i.type=="Maurice":
                    BossEnVie = True
                    
        if BossEnVie == False:
            TrapTimer += vitrine.clock.get_time()
            if TrapTimer > 200:
                TrapTimer = 0
                TrapAnimation +=1
                TrapBoss.animate(TrapAnimation,"Trapdoor",False)
                if TrapAnimation == 6:
                    TrapAnimation = 3
            if TrapBoss.collidemask(joueur.arme.rect,joueur.arme.mask,None)[0] and Inputs[3][5]:
                print("ProchainNiveau")
                 ######### - TrapDoor
                trapdoor.start(0,11)
                GameState = 0.5
                TransitionTimer=0
            

            
        # Rafraichissement des projectiles
        if PeutBouger:
            for i in ListeProjectiles:
                i.mouvement(carte, joueur, PosX, PosY, ListeProjectiles, TailleCarte,(joueur,vitrine,carte,ListeBlob,groupBlob,TailleCarte,ListeParticule,ParticuleGroup,0),vitrine,multiplicateurFPS,ProjectilesGroup)
                i.Objet.rect.x = PosX + i.x
                i.Objet.rect.y = PosY + i.y

        # Rafraichissement des Blobs

        for i in ListeBlob:
            i.rafraichissement(vitrine, joueur, ListeBlob)
            i.sprite.rect.x = PosX + i.x
            i.sprite.rect.y = PosY + i.y

        # Mouvement du joueur

        inputHorizontal = int(Inputs[3][2]) - int(Inputs[3][3])  # Gauche Droite
        inputVertical = int(Inputs[3][0]) - int(Inputs[3][1])  # Haut Bas
        if PeutBouger:

            if joueur.attack:
                if joueur.directionAttaque == "NS":
                    inputHorizontal = 0
                elif joueur.directionAttaque == "EO":
                    inputVertical = 0
                else:
                    inputVertical = 0
                    inputHorizontal = 0

            
            collision = False
            if inputHorizontal * inputVertical != 0:  # Si les inputs horizontale et verticales sont tous les deux utilisés

                PosX += round(sqrt((joueur.vitesse ** 2) / 2), 1) * inputHorizontal * (multiplicateurFPS)
                joueur.hitbox.rect.x -= round(sqrt((joueur.vitesse ** 2) / 2), 1) * inputHorizontal * (
                    multiplicateurFPS)

                for sprites in carte.hitbox:
                    if joueur.hitbox.collidemask(sprites.rect, sprites.mask, None)[0]:
                        collision = True

                if collision:
                    PosX -= round(sqrt((joueur.vitesse ** 2) / 2), 1) * inputHorizontal * (multiplicateurFPS)

                joueur.hitbox.rect.x = 430
                collision = False
                joueur.hitbox.rect.y -= round(sqrt((joueur.vitesse ** 2) / 2), 1) * inputVertical * (multiplicateurFPS)
                PosY += round(sqrt((joueur.vitesse ** 2) / 2), 1) * inputVertical * (multiplicateurFPS)

                for sprites in carte.hitbox:
                    if joueur.hitbox.collidemask(sprites.rect, sprites.mask, None)[0]:
                        collision = True

                if collision:
                    PosY -= round(sqrt((joueur.vitesse ** 2) / 2), 1) * inputVertical * (multiplicateurFPS)

            else:
                PosX += joueur.vitesse * inputHorizontal * (multiplicateurFPS)
                joueur.hitbox.rect.x -= joueur.vitesse * inputHorizontal * (multiplicateurFPS)
                PosY += joueur.vitesse * inputVertical * (multiplicateurFPS)
                joueur.hitbox.rect.y -= joueur.vitesse * inputVertical * (multiplicateurFPS)
                for sprites in carte.hitbox:
                    if joueur.hitbox.collidemask(sprites.rect, sprites.mask, None)[0]:
                        joueur.hitbox.rect.y += joueur.vitesse * inputVertical * (multiplicateurFPS)
                        joueur.hitbox.rect.x += joueur.vitesse * inputHorizontal * (multiplicateurFPS)
                        PosY -= joueur.vitesse * inputVertical * (multiplicateurFPS)
                        PosX -= joueur.vitesse * inputHorizontal * (multiplicateurFPS)
        
        #MORT
        if joueur.pv <=0:
            TextAttente += vitrine.clock.get_time()
            vitrine.addsprite(GroupTransition, "Transition")
            vitrine.change_layer("Transition", 15)
            Transition.echelle(1,1)
            Transition.rect.x =0
            Transition.rect.y = 0
            Text="Tu as échoué . . . "
            if vitrine.text(Text, (30, 800), 20):
                print("a")

                sleep(3)
                pygame.display.quit()
                quit()
            
        # Rafraichissement des Particules

        for i in ListeParticule:
            i.rafraichissement(vitrine, multiplicateurFPS)

            i.sprite.rect.x = PosX + i.x
            i.sprite.rect.y = PosY + i.y

        # Rafraichissment des coeurs
        for i in Coeurs:
            a = i.rafraichir(joueur)
            if a[0]:
                Coeurs.pop(Coeurs.index(a[1]))

        joueur.sprite.rect.x = 430
        joueur.sprite.rect.y = 430
        joueur.hitbox.rect.x = 430
        joueur.hitbox.rect.y = 430

        ##Rafraichissement du GUI

        InkFiller.echelle(0.45, (0.1 + 3.7 * (joueur.encre / joueur.encreMax)))
        InkFiller.rect.y = 620 - (345 * (joueur.encre / joueur.encreMax))

        ##Rafraichissement du joueur
        if PeutBouger:
            joueur.animationJoueur(Inputs, vitrine)
            if Inputs[3][5] and not joueur.pvMax <= joueur.pv and joueur.encre > 25:
                ProgressionSoin += vitrine.clock.get_time()
                if ProgressionSoin > 0:
                    ListeParticule.append(
                        Particule((-PosX + 500, -PosY + 500, randint(-10, 10), randint(-10, -5)), "encre",
                                  ParticuleGroup, "Particule_Ink", randint(1, 3) * 0.1))
                if ProgressionSoin > 1000:
                    ListeParticule.append(
                        Particule((-PosX + 500, -PosY + 500, randint(-10, 10), randint(-10, -5)), "encre",
                                  ParticuleGroup, "Particule_Ink", randint(1, 3) * 0.1))
                if ProgressionSoin > 2000:
                    ListeParticule.append(
                        Particule((-PosX + 500, -PosY + 500, randint(-10, 10), randint(-10, -5)), "encre",
                                  ParticuleGroup, "Particule_Ink", randint(1, 3) * 0.1))

                if ProgressionSoin > 3000:
                    ProgressionSoin = -1000
                    joueur.pv += 1
                    ######### -  HEal
                    heal.start(0,12)
                    joueur.encre -= 25
                    for i in range(50):
                        ListeParticule.append(
                            Particule((-PosX + 500, -PosY + 500, randint(-10, 10), randint(-10, -5)), "encre",
                                      ParticuleGroup, "Particule_Ink", randint(1, 3) * 0.1))

            else:
                if ProgressionSoin > 0:
                    ProgressionSoin = 0
                else:
                    ProgressionSoin += vitrine.clock.get_time()

    elif GameState == 2:
        TransitionTimer+=vitrine.clock.get_time()
        print(TransitionTimer)
        if TransitionTimer < 1250:
            vitrine.addsprite(GroupTransition, "Transition")
            vitrine.change_layer("Transition", 30)
            Transition.rect.y = 1000*((500-(TransitionTimer- 750)))/500-1000
        elif TransitionTimer < 10000 :
            print("e")
            vitrine.removesprite("Transition")
            TransitionTimer = 9999999
            
            
        
        
        TextAttente += vitrine.clock.get_time()
        Text="Félicitation... "
        
        if vitrine.text(Text, (200, 100), 20,False):
            sleep(10)
            pygame.display.quit()
            quit()
