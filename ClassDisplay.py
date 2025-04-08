import pygame,sys,time,random,os
from pygame.locals import *
from math import *
from random import *
import ClassSprite


class Fenetre:
    
    def __init__(self,taille_ecran,fps,touches,fontsize):
        '''
        le class Fenetre prend comme parametres:
        
        taille_ecran:tuple (x,y)
        le taille du fenetre en pixels
        
        fps:Int
        le fps qu'un veut limiter
        
        touches:list
        Il faut aller sur le documentation officiel pygame et trouver le nom des touches
        '''
        pygame.display.init()
        pygame.mixer.init()
        self.fenetre=pygame.display.set_mode((taille_ecran[0],taille_ecran[1]))
        self.X=taille_ecran[0]
        self.Y=taille_ecran[1]
        self.clock=pygame.time.Clock()
        self.fps=fps
        self.touches_appuyes=[]
        self.touches=touches
        for key in touches:
            self.touches_appuyes.append(False)
        self.position_clique=False
        self.spritegroups={}
        pygame.font.init()
        self.font_size=fontsize
        self.font = pygame.font.Font('PressStart2P-vaV7.ttf', self.font_size)
        self.textes=[]
        self.timer=0
        self.counter=0
        self.linecounter=0
        self.index=0
        self.textbox=None
        
    def tuerfenetre(self):
        '''
        Tue l'ecran
        '''
        pygame.display.quit()
        
    def addsprite(self,spritegroop,nom):
        '''
        Il faut creer un sprite group avant de l'ajouter au affichage qui se fait en dehors de ce class
        Par exemple ceci ce fait en 1 ligne:
        exempleSpriteGroup=pygame.sprite.Group()
        exempleFenetre.addsprite(exempleSpriteGroup,examplenom)
        cette methode est pour ajouter les groups de sprite dans un liste pour qu'ils sont affiches dans l'ecran
        '''
        self.spritegroups.update({nom:spritegroop})
        
        
    def removesprite(self,nom):
        '''
        Il faut deja  avoir un sprite group ajoute au affichange avant de l'enlever
        exempleSpriteGroup=pygame.sprite.Group()
        exempleFenetre.addsprite(exempleSpriteGroup,examplenom)
         cette methode est pour enlever les groups de sprite dans un liste pour qu'ils ne sont pas affiches dans l'ecran
        '''
        self.spritegroups.pop(nom)
    
    def events(self):
        '''
        Cette methode retourne les evenements qui se passent dans l'ecran
        n'a aucun parametre
        retourne un tuple qui contient:
        (le fps courant(Int),le clique de souris(boolean)(meme si il est tenu)(moins precis),Un list de booleans qui est dans la meme indexes de self.touches(True si touche appuye False sinon,Clique d'un souris(boolean)(plus precis mais n'affiche pas si le souris est tenu))
        '''
        click=False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                for key in self.touches:
                    if event.key == key:
                        self.touches_appuyes[self.touches.index(key)]=True
                        
            if event.type == pygame.KEYUP:
                for key in self.touches:
                    if event.key == key:
                        self.touches_appuyes[self.touches.index(key)]=False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.position_clique=True
            if event.type == pygame.MOUSEBUTTONUP:
                self.position_clique=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click=True
                
        position_souris=pygame.mouse.get_pos()
        return(self.clock.get_fps(),self.position_clique,position_souris,self.touches_appuyes,click)
    
    
    def updatedisplay(self):
        '''
        Affiche le contenu qui est dans le fenetre
        retourne rien
        '''
        textbox=self.textbox
        self.fenetre.fill((100,100,100))
        for spritegroop in self.spritegroups.values():
            spritegroop.draw(self.fenetre)
        if self.textbox!=None:
            pygame.draw.rect(self.fenetre,(200,200,200),textbox)
        for text in self.textes:
            self.fenetre.blit(text[0], text[1])
        pygame.display.update()
        self.clock.tick(self.fps)
        
    def layer_list(self):
        '''
        un methode qui indique l'ordre auquelle les groupes de sprite sont affiches
        renvoie:
        Le liste des noms des groupes de sprites en ordre(le premier est au fond et le dernier est en avant)
        Un liste debug pour afficher avec l'explication quelle group de sprite est en quelle 'Layer'
        '''
        printing='Layer '
        list_layers,list_layers2,compteur=[],[],len(self.spritegroups)
        for spritegroop in self.spritegroups:
            list_layers.append((printing+str(compteur)+':'+spritegroop))
            list_layers2.append(spritegroop)
            compteur-=1
        return list_layers2,list_layers
    
    def change_layer(self,nom,index):
        '''
        Un methode pour changer un group de sprites a un different 'Layer'
        Parametres:
        nom:String
        Le nom que tu as donne au groupe de sprites
        
        index:int
        L'endroit ou tu veut inserer ce groupe de sprites (0,1,2,...)
        Le dernier s'affiche en avant et le premier s'affiche au fond
        
        renvoie rien
        '''
        sprite_group = self.spritegroups.pop(nom)
        items = list(self.spritegroups.items())
        items.insert(index, (nom, sprite_group))
        self.spritegroups = dict(items)
        
    def addspriteat(self,spritegroop,nom,index):
        '''
        meme methode que addsprite() mais avec un index
        renvoie rien
        '''
        items = list(self.spritegroups.items())
        items.insert(index, (nom, spritegroop))
        self.spritegroups = dict(items)
        
        
    def create(self,shape,coordin,color,size):
        '''draws shapes and objects
            
            shape:
            'rect'
            'circle'
            'polygon'
            'line'
            
            size:
            (longueur,largeur) for 'rect'
            rayon(int) for 'circle'
            lineThickness(if width == 0, (default) fill the polygon,if width > 0, used for line thickness,if width < 0, nothing will be drawn)(int) for 'polygon'
            lineThickness(if width >= 1, used for line thickness (default is 1),if width < 1, nothing will be drawn)(int) for 'line'
            
            coordin:
            if shape='rect' or shape='circle':
                coordin=(X(int),Y(int))
            if shape='polygon':
                coordin=[(x,y),(x,y),(x,y)]
            if shape='line':
                coordin=[(x,y),(x,y)] (coordin[0]=start_pos,coordin[1]=end_pos)

            Sortie: rien
        '''
        if shape=='rect':
            pygame.draw.rect(self.fenetre,color,pygame.Rect(coordin[0], coordin[1], size[0], size[1]))
        if shape=='circle':
            pygame.draw.circle(self.fenetre,color,(coordin[0],coordin[1]),size)
        if shape=='polygon':
            pygame.draw.polygon(self.fenetre,color,coordin,size)
        if shape=='line':
            pygame.draw.line(self.fenetre,color,coordin[0],coordin[1],size)
            
    def text(self,text,position,time,box=True):
        letters=[]
        for letter in text:
            letters.append(self.font.render(letter,True,(0,0,0))) #getting font for each letter
            
        show=False
        self.timer+=self.clock.get_time()
        if self.timer>time:
            show=True
            self.timer=0
            textRect=letters[self.index].get_rect()
            
            if position[0]+(self.font_size-5)*self.counter+5>=self.X:
                self.linecounter+=1
                self.counter=0
                
            if position[0]+(self.font_size-5)*self.counter<self.X:
                textRect.center=(position[0]+(self.font_size-5)*self.counter,position[1]+(self.font_size-0)*self.linecounter)
                self.counter+=1
                

        if show:
            self.textes.append((letters[self.index],textRect))
            print(self.index,(textRect),textRect.center,(self.linecounter,self.counter))
            self.index+=1
            if box:
                pygame.draw.rect(self.fenetre,(0,0,0),Rect(-2000, position[1]-20, 10000, 10000))
                self.textbox=Rect(-2000, position[1]-20, 10000, 10000)
                
            if self.index>=len(text):
                return True
            
    def reset_text(self,fontsize):
        self.font_size=fontsize
        self.font = pygame.font.Font('PressStart2P-vaV7.ttf', self.font_size)
        self.timer=0
        self.counter=0
        self.linecounter=0
        self.index=0
        self.textbox=None
        self.textes=[]
        
    def remove_text(self):
        self.textes=[]
        self.counter=0
        self.linecounter=0
        self.timer=0
        self.index=0
        

            
            
            
    
        

