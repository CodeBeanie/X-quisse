from math import *
from random import *
from ClassDisplay import*
import ClassSprite
import pygame,sys,time,random,os
from pygame.locals import *
from ClassCarte import *


class mainmenu:
   
    def __init__(self,scale,fps):
        self.scale=scale
        self.textscale=(500*min(scale))/500
        #window main menu
        self.mainmenu=Fenetre((500*scale[0],500*scale[1]),fps,[],round(24*self.textscale))
        self.musique=Musique("Bossa Nova.mp3")
        #je cree un group sprite
        self.boutons=pygame.sprite.Group()
        self.mouse=pygame.sprite.Group()
        self.settingbouton=pygame.sprite.Group()
        self.creditsgrp=pygame.sprite.Group()
       
        self.mainmenu.addsprite(self.boutons,'boutons')
        self.mainmenu.addsprite(self.mouse,'mouse')
        #quelques variables
       
        self.spritescale=min(scale)
        # mouse controls
        pygame.mouse.set_visible(True)

        #les sprites
        #main buttons
        self.boutonplay=(ClassSprite.Sprite((350*scale[0],400*scale[1]),self.boutons,"buttonplay_static",0,1.5*self.spritescale,1.5*self.spritescale))
        self.boutonsettings=(ClassSprite.Sprite((91*scale[0],340*scale[1]),self.boutons,"buttonsettings_static",0,0.92*self.spritescale,0.7*self.spritescale))
        self.boutontexte=(ClassSprite.Sprite((250*scale[0],160*scale[1]),self.boutons,"logo",0,2*self.spritescale,2*self.spritescale))
        self.credits=(ClassSprite.Sprite((88*self.scale[0],390*self.scale[1]),self.boutons,"buttoncredits_static",0,0.97*self.spritescale,0.97*self.spritescale))
        self.boutonquitter=(ClassSprite.Sprite((86*self.scale[0],450*self.scale[1]),self.boutons,"buttonquitter_static",0,1*self.spritescale,1*self.spritescale))
        #setting buttons
        self.boutonretour=(ClassSprite.Sprite((250*self.scale[0],400*self.scale[1]),self.settingbouton,"buttonretour",0,1*self.spritescale,1*self.spritescale))
        self.buttoncontrol=(ClassSprite.Sprite((250*self.scale[0],100*self.scale[1]),self.settingbouton,"buttonZQSD",0,1*self.spritescale,1*self.spritescale))
        #credit menu
        self.boutonretourcredits=(ClassSprite.Sprite((250*self.scale[0],400*self.scale[1]),self.creditsgrp,"buttonretour",0,1*self.spritescale,1*self.spritescale))
        #other buttons
       
        self.mousepos=(ClassSprite.Sprite((0,0),self.mouse,"nothing",0,0.003,0.003))
       
        print(self.mainmenu.layer_list())
    def openmenu(self):
        settings=False
        credit=False
        show=False
        controls=[K_z, K_s, K_q, K_d,K_e,K_f]
        control='ZQSD'
        self.musique.start(-1,1,0.15)
        while True:
            eventinfo=self.mainmenu.events()
            self.mainmenu.updatedisplay()
            #Updating the mouse sprite to be exactly where the mouse is
            self.mousepos.rect=eventinfo[2]
           
            #detecting collisions with the buttons
            collideposplay=self.mousepos.collidemask(self.boutonplay.rect,self.boutonplay.mask,None)[0]
            collidepos=self.mousepos.collidemask(self.boutonsettings.rect,self.boutonsettings.mask,None)[0]
            collideposcredit=self.mousepos.collidemask(self.credits.rect,self.credits.mask,None)[0]
            collideposquitte=self.mousepos.collidemask(self.boutonquitter.rect,self.boutonquitter.mask,None)[0]
            #Animations for buttons
            if collideposquitte and not settings and not credit:
                self.boutonquitter.animate("","buttonquitter_active")
            if not collideposquitte and not settings and not credit:
                self.boutonquitter.animate("","buttonquitter_static")
           
            if collideposplay and not settings and not credit:
                self.boutonplay.animate("","buttonplay_active")
            if not collideposplay and not settings and not credit:
                self.boutonplay.animate("","buttonplay_static")
           
            if collidepos and not settings and not credit:
                self.boutonsettings.animate("","buttonsettings_active")
            if not collidepos and not settings and not credit:
                self.boutonsettings.animate("","buttonsettings_static")
               
            if collideposcredit and not settings and not credit:
                self.credits.animate("","buttoncredits_active")
            if not collideposcredit and not settings and not credit:
                self.credits.animate("","buttoncredits_static")
               
           
            #Button clicks
               
            if collideposplay and (eventinfo[4]) and not settings and not credit:
                print(collideposplay)
                print('killing display')
                pygame.display.quit()#WARNING: have to initialise new window for this to work,otherwise window stays open
                self.musique.stop()
               
                #loading screen?
                #execute game here
                return controls
           
           
            if collideposquitte and (eventinfo[4]) and not settings and not credit:
                print(collideposplay)
                print('killing display')#WARNING: have to initialise new window for this to work,otherwise window stays open
                return 'yes kill yourself'

               
            if collidepos and (eventinfo[4]) and not settings and not credit:
                print('killing sprites now')
                #showing and removing new and old buttons
                self.mainmenu.removesprite('boutons')
                self.mainmenu.addsprite(self.settingbouton,'settingbouton')
                settings=True
               
            if collideposcredit and (eventinfo[4]) and not settings and not credit:
                print('killing sprites now')
                #showing and removing new and old buttons
                self.mainmenu.removesprite('boutons')
                self.mainmenu.addsprite(self.creditsgrp,'credits')
                credit=True
               
            #Opening settings thing
            if settings:
                #detecting new button collisions here
                collideposretour=self.mousepos.collidemask(self.boutonretour.rect,self.boutonretour.mask,None)[0]
                collideposcontrol=self.mousepos.collidemask(self.buttoncontrol.rect,self.buttoncontrol.mask,None)[0]
                #animation
                if collideposretour and not credit:
                    self.boutonretour.animate("","buttonretour_active")
                elif not collideposretour and not credit:
                    self.boutonretour.animate("","buttonretour")
                   
                #clicking button
                if collideposcontrol and not credit and (eventinfo[4]) and control=='WASD':
                    self.buttoncontrol.animate("","buttonZQSD")
                    controls=[K_z, K_s, K_q, K_d,K_e,K_f]
                    control='ZQSD'
                elif collideposcontrol and not credit and (eventinfo[4]) and control=='ZQSD':
                    self.buttoncontrol.animate("","buttonWASD")
                    controls=[K_w, K_s, K_a, K_d,K_e,K_f]
                    control='WASD'
                   
                   
                if collideposretour and (eventinfo[4]) and not credit:
                    settings=False
                    self.mainmenu.removesprite('settingbouton')
                    self.mainmenu.addsprite(self.boutons,'boutons')
               
            #opening credits menu
            if credit:
                if not show:
                    show=self.mainmenu.text('Developpement:          Léane TERRY             Guillaume JONVEL        Ian LEGRAND                                     Art:                    Léane TERRY                                     Son/Musique:            Mathis TERRY',(50*self.textscale,50*self.textscale),10,False)
               

                                #detecting new button collisions here
                collideposretour=self.mousepos.collidemask(self.boutonretourcredits.rect,self.boutonretourcredits.mask,None)[0]
               
                if collideposretour and not settings:
                    self.boutonretourcredits.animate("","buttonretour_active")
                elif not collideposretour and not settings:
                    self.boutonretourcredits.animate("","buttonretour")
                if collideposretour and (eventinfo[4]):#going back to main screen
                    credit=False
                    show=False
                    self.mainmenu.reset_text(round(24*self.textscale))

                    self.mainmenu.removesprite('credits')
                    self.mainmenu.addsprite(self.boutons,'boutons')