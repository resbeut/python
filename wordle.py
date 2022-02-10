# ------------------------------------------------------
# -- Auteur:  stevos_teen@yahoo.fr
# -- Date: 08/02/2022
# -- Version: 1.0
# ------------------------------------------------------

import pygame
from bs4 import BeautifulSoup
import urllib3, requests, ssl
import random, sys

display_width = 415
display_height = 625
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (160, 160, 160)
DARKGREY = ( 80, 80 , 80)
GREEN = (57, 255,20)
ORANGE = (255,127,0)
RED = (255, 0, 0)
BLUE = (25,200,255)



class Grille(object):
    def __init__(self):
        self.posX=0
        self.posY=0
        for x in ( 45 , 110, 175, 240, 305 ):
            for y in ( 45 , 110, 175, 240, 305 ,370 ):
                pygame.draw.rect(win, BLACK, (x, y, 65, 65))
                pygame.draw.rect(win, WHITE, (x, y, 65, 65),2)
                
    def ecrireLettre(self,lettre):
        if self.posX < 5:
            text = fontBig.render(lettre, True, GREY)
            textLocation = ( self.posX*65 + 45 + (65-text.get_width())/2, self.posY*65 + 55 )
            win.blit(text, textLocation) 
            self.posX=self.posX+1

    def effacerLettre(self):
        if self.posX > 0:
            self.posX=self.posX-1
            pygame.draw.rect(win, BLACK, (self.posX*65+45, self.posY*65+45, 65, 65))
            pygame.draw.rect(win, WHITE, (self.posX*65+45, self.posY*65+45, 65, 65),2)

    def colorLigne(self,mot, resultat):
        cpt=0
        while cpt < 5:
            if resultat[cpt]=="2" : 
                pygame.draw.rect(win, GREEN, (cpt*65+45, self.posY*65+45, 65, 65))
            elif resultat[cpt]=="1" :
                pygame.draw.rect(win, ORANGE, (cpt*65+45, self.posY*65+45, 65, 65))
            else:
                pygame.draw.rect(win, GREY, (cpt*65+45, self.posY*65+45, 65, 65)) 
            pygame.draw.rect(win, WHITE, (cpt*65+45, self.posY*65+45, 65, 65),2)
            text = fontBig.render(mot[cpt], True, WHITE)
            textLocation = ( cpt*65 + 45 + (65-text.get_width())/2, self.posY*65 + 55 )
            win.blit(text, textLocation) 
            cpt=cpt+1

    def changeLigne(self):
        if self.posX == 5 and self.posY <5 :
            self.posX=0
            self.posY=self.posY+1

class Dictionary(object):
    def __init__(self):
        nb_mot=0
        try:
            nb_mot=len(self.liste_mots)
        except:
            self.liste_mots=[]
        if nb_mot == 0:
            ssl._create_default_https_context = ssl._create_unverified_context
            urllib3.disable_warnings()
            url="https://www.listesdemots.net/mots5lettres.htm"
            for num_page in range(2,12):
                req = requests.get(url, verify=False)
                soup = BeautifulSoup(req.text, "html.parser")
                for liste in soup.find_all('span', attrs={'class':'mot'}):
                    for mot in liste.text.split():
                        self.liste_mots.append(mot)
                url="https://www.listesdemots.net/mots5lettrespage"+str(num_page)+".htm"
        #tirage du mot à trouver
        self.motMystere=self.liste_mots[ random.randint(0, len(self.liste_mots)) ]
        #print(self.motMystere)
        
    def motExist( self, mot ):
        if mot in self.liste_mots :
            return True
        else:
            return False
    
    def verifMot( self, mot) :
        resultat=""
        num_cpt=0
        for lettre in mot:
            if lettre in self.motMystere:
                if lettre == self.motMystere[num_cpt]:
                    resultat=resultat+"2"
                else:
                    resultat=resultat+"1"
            else:
                resultat=resultat+"0"
            num_cpt+=1
        return resultat

class Letter(object):
    def __init__(self, x, y, statut, value):
        self.x = x
        self.y = y
        self.color = statut
        self.value = value
    def draw(self):
        text = font.render(self.value, True,WHITE)
        if text.get_width() < 100:
            pygame.draw.rect(win, self.color, (self.x, self.y, 40, 40))
            textLocation = ((((self.x + 20) - (text.get_width()/2)), ((self.y + 20) - (text.get_height()/2))))
        else:
            text = fontSmall.render(self.value, True, WHITE) 
            pygame.draw.rect(win, self.color, (self.x, self.y, 81, 40))
            textLocation = ((((self.x + 40) - (text.get_width()/2)), ((self.y + 20) - (text.get_height()/2))))
        win.blit(text, textLocation)    

class KeyBoard(object):
    def __init__(self,listetouche):
        self.lettersList=[]
        for obj in listetouche:
            touche= Letter(obj['x'],obj['y'], GREY, str(obj['lettre']))
            self.lettersList.append(touche)

    def touches(self):
        return self.lettersList

    def colortouches(self,mot,resultat):
        for i in range(len(resultat)):
            if resultat[i] == "2" : keycolor= GREEN
            elif resultat[i] == "1" : keycolor= ORANGE
            elif resultat[i] == "0" : keycolor= DARKGREY
            for key in self.lettersList:
                if key.value == mot[i]: 
                    key.color= keycolor
                    break
        
pygame.init()
pygame.display.set_caption('Wordle v1.0')
win = pygame.display.set_mode((display_width, display_height))

fontMicro = pygame.font.SysFont('freesansbold.ttf', 18)
fontSmall = pygame.font.SysFont('freesansbold.ttf', 22)
font = pygame.font.SysFont('freesansbold.ttf', 40)
fontBig = pygame.font.SysFont('freesansbold.ttf', 80)


ListeAZERTY = [   { 'lettre':'A', 'x':0, 'y':500},	 { 'lettre':'Z', 'x':41, 'y':500},	 { 'lettre':'E', 'x':82, 'y':500},	 { 'lettre':'R', 'x':123, 'y':500},	 { 'lettre':'T', 'x':164, 'y':500},	 { 'lettre':'Y', 'x':205, 'y':500},	 { 'lettre':'U', 'x':246, 'y':500},	 { 'lettre':'I', 'x':287, 'y':500},	 { 'lettre':'O', 'x':328, 'y':500},	 { 'lettre':'P', 'x':369, 'y':500},	 
                  { 'lettre':'Q', 'x':0, 'y':541},	 { 'lettre':'S', 'x':41, 'y':541},	 { 'lettre':'D', 'x':82, 'y':541},	 { 'lettre':'F', 'x':123, 'y':541},	 { 'lettre':'G', 'x':164, 'y':541},	 { 'lettre':'H', 'x':205, 'y':541},	 { 'lettre':'J', 'x':246, 'y':541},	 { 'lettre':'K', 'x':287, 'y':541},	 { 'lettre':'L', 'x':328, 'y':541},	 { 'lettre':'M', 'x':369, 'y':541},	 
                  { 'lettre':'W', 'x':82, 'y':582},	 { 'lettre':'X', 'x':123, 'y':582},	 { 'lettre':'C', 'x':164, 'y':582},	 { 'lettre':'V', 'x':205, 'y':582},	 { 'lettre':'B', 'x':246, 'y':582},	 { 'lettre':'N', 'x':287, 'y':582},
                  { 'lettre':'EFFACER', 'x':0, 'y':582}, { 'lettre':'ENTREE', 'x':328, 'y':582}  ]
ListeQWERTY = [   { 'lettre':'Q', 'x':0, 'y':500},	 { 'lettre':'W', 'x':41, 'y':500},	 { 'lettre':'E', 'x':82, 'y':500},	 { 'lettre':'R', 'x':123, 'y':500},	 { 'lettre':'T', 'x':164, 'y':500},	 { 'lettre':'Y', 'x':205, 'y':500},	 { 'lettre':'U', 'x':246, 'y':500},	 { 'lettre':'I', 'x':287, 'y':500},	 { 'lettre':'O', 'x':328, 'y':500},	 { 'lettre':'P', 'x':369, 'y':500},
                  { 'lettre':'A', 'x':0, 'y':541},	 { 'lettre':'S', 'x':41, 'y':541},	 { 'lettre':'D', 'x':82, 'y':541},	 { 'lettre':'F', 'x':123, 'y':541},	 { 'lettre':'G', 'x':164, 'y':541},	 { 'lettre':'H', 'x':205, 'y':541},	 { 'lettre':'J', 'x':246, 'y':541},	 { 'lettre':'K', 'x':287, 'y':541},	 { 'lettre':'L', 'x':328, 'y':541},	 { 'lettre':'Z', 'x':369, 'y':541},
                  { 'lettre':'X', 'x':82, 'y':582},	 { 'lettre':'C', 'x':123, 'y':582},	 { 'lettre':'V', 'x':164, 'y':582},	 { 'lettre':'B', 'x':205, 'y':582},	 { 'lettre':'N', 'x':246, 'y':582},	 { 'lettre':'M', 'x':287, 'y':582},
                  { 'lettre':'EFFACER', 'x':0, 'y':582}, { 'lettre':'ENTREE', 'x':328, 'y':582}  ]
ListeABCDEF = [   { 'lettre':'A', 'x':0, 'y':500},	 { 'lettre':'B', 'x':41, 'y':500},	 { 'lettre':'C', 'x':82, 'y':500},	 { 'lettre':'D', 'x':123, 'y':500},	 { 'lettre':'E', 'x':164, 'y':500},	 { 'lettre':'F', 'x':205, 'y':500},  { 'lettre':'G', 'x':246, 'y':500},	 { 'lettre':'H', 'x':287, 'y':500},	 { 'lettre':'I', 'x':328, 'y':500},	 { 'lettre':'J', 'x':369, 'y':500},	 
                  { 'lettre':'K', 'x':0, 'y':541},	 { 'lettre':'L', 'x':41, 'y':541},   { 'lettre':'M', 'x':82, 'y':541},	 { 'lettre':'N', 'x':123, 'y':541},	 { 'lettre':'O', 'x':164, 'y':541},	 { 'lettre':'P', 'x':205, 'y':541},  { 'lettre':'Q', 'x':246, 'y':541},	 { 'lettre':'R', 'x':287, 'y':541},	 { 'lettre':'S', 'x':328, 'y':541},	 { 'lettre':'T', 'x':369, 'y':541},	 
                  { 'lettre':'U', 'x':82, 'y':582},	 { 'lettre':'V', 'x':123, 'y':582},	 { 'lettre':'W', 'x':164, 'y':582},	 { 'lettre':'X', 'x':205, 'y':582},	 { 'lettre':'Y', 'x':246, 'y':582},	 { 'lettre':'Z', 'x':287, 'y':582},
                  { 'lettre':'EFFACER', 'x':0, 'y':582}, { 'lettre':'ENTREE', 'x':328, 'y':582}  ]                  



def redrawGameWindow(KeyList):
    for key in KeyList:
        key.draw()
    
    # Message en cours de jeu
    text = font.render(shownText, True, colorText)
    pygame.draw.rect(win, BLACK, (0,450, 800, 28))
    textLocation = ( 10, 450)
    win.blit(text, textLocation)  

    # Message en cours de jeu
    score="Nombre de parties jouer: "+str(nb_parties)+ "  - mots trouvés: "+str(nb_victoires)+"  réussite: "+str( round( 100*((6*nb_parties-nb_essais)/(nb_parties*6)),1) )+" %"
    text = fontMicro.render(score, True, BLUE)
    pygame.draw.rect(win, BLACK, (0,480, 800, 20))
    textLocation = ( 10, 482)
    win.blit(text, textLocation)  

    #bouton RESET
    if finPartie: 
        reset="REJOUER" 
        colorReset=RED
    else: 
        reset="RESET"
        colorReset=WHITE
    text = fontSmall.render(reset, True, colorReset)
    textLocation=(22,2)
    pygame.draw.rect(win,GREY,(0,0,99,20))
    win.blit(text, textLocation)  

    #bouton CLAVIER
    text = fontSmall.render("CLAVIER", True, WHITE)
    textLocation=(115,2)
    pygame.draw.rect(win,GREY,(100,0,99,20))
    win.blit(text, textLocation)  

    #bouton QUITTER
    text = fontSmall.render("QUITTER", True, WHITE)
    textLocation=(210,2)
    pygame.draw.rect(win,GREY,(200,0,99,20))
    win.blit(text, textLocation)  

    #bouton ABOUT
    text = fontSmall.render("A PROPOS", True, WHITE)
    textLocation=(310,2)
    pygame.draw.rect(win,GREY,(300,0,105,20))
    win.blit(text, textLocation)  


    pygame.display.update() 

run =True
shownText = ""
colorText = BLACK
dico=Dictionary()
grille=Grille()
essai=0
liste_essais=[]
saisie_mot=""
liste=ListeAZERTY
clavier=KeyBoard(liste)
nb_parties=1
nb_victoires=0
nb_essais=0
finPartie=False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONUP:
            shownText=""
            pos = pygame.mouse.get_pos()
            #print( str(pos[0]) + " / " + str(pos[1]))
            if pos[1]  <= 20:
                if pos[0] < 99:
                    colorText = BLACK
                    dico=Dictionary()
                    grille=Grille()
                    essai=0
                    liste_essais=[]
                    saisie_mot=""
                    nb_parties+=1
                    clavier=KeyBoard(ListeAZERTY)
                    finPartie=False
                if pos[0] > 100 and pos[0] < 200 :
                    keys=clavier.touches()
                    typeclavier=keys[0].value+keys[1].value+keys[2].value+keys[3].value+keys[4].value+keys[5].value # on détermine le claviuer actuel
                    if typeclavier == "AZERTY":   clavier=KeyBoard(ListeQWERTY)
                    elif typeclavier == "QWERTY": clavier=KeyBoard(ListeABCDEF)
                    else : clavier=KeyBoard(ListeAZERTY)
                if pos[0] > 200 and pos[0] < 300 :
                    print("Au revoir !")
                    pygame.quit()
                if pos[0] > 300 and pos[0] < 405 :
                   shownText = "2022.02  by  stevos_teen"
                   colorText = ORANGE
            #------------------------------------------------
            if not finPartie:
                for L in clavier.touches():
                    largeur=40
                    if len(L.value)> 1: largeur=80  # pour gérer les doubles touches ENTREE et EFFACER
                    if pos[0] > L.x and pos[0] < L.x + largeur:
                        if pos[1] > L.y and pos[1] < L.y + largeur:
                            if L.value == "EFFACER":
                                if len(saisie_mot) >0 : 
                                    saisie_mot=saisie_mot[:-1]
                                    grille.effacerLettre()
                            elif L.value == "ENTREE":
                                if len(saisie_mot) == 5 :  
                                    if dico.motExist(saisie_mot):
                                        grille.colorLigne(saisie_mot,dico.verifMot(saisie_mot))
                                        clavier.colortouches(saisie_mot,dico.verifMot(saisie_mot))
                                        if dico.verifMot(saisie_mot) == "22222":
                                            shownText = "GAGNE !"
                                            colorText = GREEN  
                                            nb_victoires+=1
                                            finPartie=True
                                        else:
                                            if grille.posY == 5:
                                                shownText = "Le mot mystère: " + dico.motMystere
                                                colorText = RED
                                                finPartie=True
                                        saisie_mot=""
                                        nb_essais+=1
                                        grille.changeLigne()
                                    else:
                                        shownText = saisie_mot+ ": absent du dico!"
                                        colorText = RED
                            else:
                                if len(saisie_mot) <5: 
                                    saisie_mot=saisie_mot+L.value
                                    grille.ecrireLettre(L.value)
    try:              
        redrawGameWindow(clavier.touches())
    except:
        pass

pygame.quit()