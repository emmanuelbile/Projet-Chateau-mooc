# PARTIE 1: FONCTIONS

from CONFIGS import *
import turtle 


def lire_matrice(fichier):
    """Lis les données du plan dans un fichier texte"""

    with open(fichier, 'r') as f:
        matrice = [[ int(c) for c in l.strip() if c.isnumeric()] for l in f.readlines()]
        return matrice



def creer_dictionnaire_des_objets(fichier):
    """ Lecture d'un dictionnaire de valeur """
    with open(fichier, 'r') as f:
        dico = {}
        for l in f.readlines():
            nl = l.strip()
            k, v = eval(nl)
            dico[k] = v
        return dico
    


def calculer_pas(matrice):
    """Calcule le coté d'une case du plan"""

    # nb_colonne = len(matrice[0])
    # nb_ligne = len(matrice)
    # h = ZONE_PLAN_MAXI[-1] - ZONE_PLAN_MINI[-1]
    # l = ZONE_PLAN_MAXI[0] - ZONE_PLAN_MINI[0]

    # return min(h//nb_ligne, l/nb_colonne)
    return min((ZONE_PLAN_MAXI[1] - ZONE_PLAN_MINI[1]) // len(matrice),
               (ZONE_PLAN_MAXI[0] - ZONE_PLAN_MINI[0]) // len(matrice[0]))




def coordonnees(case, pas):
    """Calcule les coordonnées d'une case du plan"""

    x = ZONE_PLAN_MINI[0] + case[1] * pas
    y = ZONE_PLAN_MAXI[1] - (case[0] + 1) * pas 
    
    return x, y
    # return ZONE_PLAN_MINI[0] + case[1] * pas, ZONE_PLAN_MAXI[1] - (case[0] + 1) * pas



def coordonnees_centre(case, pas):
    """ Calcule les coordonnées du centre d'un carré """

    return coordonnees(case, pas)[0] + pas // 2, coordonnees(case, pas)[1] + pas // 2



def tracer_carre(case, couleur, pas):
    """Tracer d'un carré à partir de son coin inferieur"""
    
    turtle.hideturtle()
    turtle.up()
    turtle.setposition(coordonnees(case, pas))
    turtle.down()
    turtle.begin_fill()
    turtle.fillcolor(couleur)
    for i in range(4):
        turtle.forward(pas)
        turtle.left(90)
    
    turtle.end_fill()
    turtle.up()



def afficher_plan(matrice):
    turtle.up()
    for i in range(len(matrice)):
        for c in range(len(matrice[0])):
            tracer_carre((i, c), COULEURS[matrice[i][c]], P)
    turtle.hideturtle()
    
    

def prochaine_position(matrice, mouvement):
    """ Determine le prochain deplacement de la tortue"""
    
    next_posi_mm = [position_depart[k] + mouvement[k] for k in range(2)] 

    # Vérifie si on sort pas de la matrice
    if 0 <= next_posi_mm[0] < len(matrice) and 0 <= next_posi_mm[1] < len(matrice[0]):

        # Si oui on récupère le type de la prochaine position.
        next_posi_type = matrice[next_posi_mm[0]][next_posi_mm[1]]

    else:
        next_posi_type = None

    return next_posi_mm, next_posi_type


def ancienne_position(mouvement):
    """ fait avancer la position de la tortue"""
    
    tracer_carre(position_depart, COULEUR_VUE, P)

    position_depart[0] += mouvement[0]  # Change notre position.
    position_depart[1] += mouvement[1]


    turtle.goto(coordonnees_centre(position_depart, P))  # Tortue va à la nouvelle position.

    turtle.dot(taille_joueur, COULEUR_PERSONNAGE)  # Replace le personnage.



def deplacer(matrice, mouvement):
    """ Fonction de deplacement du joueur dans le plan"""

    # Prochaine position et son type (VIDE, MUR, BUT, PORTE, OBJET ou None), None pour en dehors de la matrice.
    next_posi_mm, type_next_case = prochaine_position(matrice, mouvement)

    # Important de NE PAS avoir de else au niveau du if ci-dessus, car les cas où on a mur/None ne sont pas traité.
    if type_next_case in (VIDE, OBJET):

        ancienne_position(mouvement)
        # tracer_carre(position_depart, COULEUR_VUE, P)


        if type_next_case == OBJET:  # Sous-cas avec objet.

            ramasser_objet()  # Change matrice, récupère objet, l'annonce et met à jour l'inventaire
    
    elif type_next_case == BUT:

        if len(inventaire_objet) == len(dico_objets):  # Impose de collecter tous les objets pour gagner.

            annonce('case jaune', 'victoire', None)  # Victoire et annonce.
            ancienne_position(mouvement)

        else:
            annonce('case jaune', 'pas tous les objets', None)  # Pas victoire et invite à rammasser tous les objets.

    elif type_next_case == PORTE:

        if poser_question(next_posi_mm):  # Si réponse correcte.

            annonce('porte', 'correcte', None)  # Annonce ouverture porte.

            ancienne_position(mouvement)  # Déplace le personnage.

            M[position_depart[0]][position_depart[1]] = 0  # Enlève la porte de la matrice.

        else:  # Si fausse réponse.
            annonce('porte', 'faux', None)  # Annonce fausse réponse.


def deplacer_gauche():
    """ Deplace le joueur vers la gauche"""

    turtle.onkeypress(None, 'Left')  # Arrête la fenêtre Turtle d'écouter le clavier.
    deplacer(M, (0, -1))
    turtle.onkeypress(deplacer_gauche, 'Left')  # Remet la fenêtre Turtle sur écoute du clavier.


def deplacer_droite():
    """ Deplace le joueur vers la droite """

    turtle.onkeypress(None, 'Right')
    deplacer(M, (0, 1))
    turtle.onkeypress(deplacer_droite, 'Right')


def deplacer_haut():
    """ Deplace le joueur vers le haut"""

    turtle.onkeypress(None, 'Up')
    deplacer(M, (-1, 0))
    turtle.onkeypress(deplacer_haut, 'Up')


def deplacer_bas():
    """ Deplace le joueur vers le bas"""
    
    turtle.onkeypress(None, 'Down')
    deplacer(M, (1, 0))
    turtle.onkeypress(deplacer_bas, 'Down')


def effacement_annonce():
    """ mise en place d'une annonce.
    """

    x_pp, y_pp = POINT_AFFICHAGE_ANNONCES
    delta_x_pp = 900
    delta_y_pp = 20
    
    turtle.goto(x_pp - 10, y_pp + delta_y_pp)  # Haut gauche zone affichage annonces.
    # Le -10 est pour prendre de la marge pour bien tout effacer.
    turtle.color('white')
    
    turtle.begin_fill()  # on efface l'annonce précédente en l'encadrant et avec une commande de remplissage.
    turtle.goto(x_pp + delta_x_pp, y_pp + delta_y_pp)  # Haut droite zone affichage annonces.
    turtle.goto(x_pp + delta_x_pp, y_pp - delta_y_pp)  # Bas droite zone affichage annonces.
    turtle.goto(x_pp - 10, y_pp - delta_y_pp)  # Bas gauche zone affichage annonces.
    turtle.end_fill()
    
    turtle.goto(x_pp, y_pp)  # on se met en position d'écriture.


def ramasser_objet():
    """ Garde en mémoire un objet trouvé dans l'inventaire d'objets.
    """

    M[position_depart[0]][position_depart[1]] = 0  # Remplace la case objet de la matrice par une case vide.

    objet_trouve = dico_objets[(position_depart[0], position_depart[1])]  # Trouve quel objet correspond à notre position acutelle
 
    inventaire_objet.add(objet_trouve)  # Ajoute l'objet trouvé à l'inventaire.

    afficher_inventaire(objet_trouve)  # Fonctions d'affichage : inventaire et annonces
    annonce('objet', None, objet_trouve)


def afficher_inventaire(objet_trouve):
    """ Affiche l'inventaire d'objets.
    """

    turtle.goto(POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1] - 10 - 30 * len(inventaire_objet))

    turtle.color('black')
    turtle.write('* ' + objet_trouve, font=('Consolas', 10, 'italic bold'))


def poser_question(next_posi_mm):
    """ Fonction de gestion des réponses"""
    
    annonce('porte', 'fermée', None)
    

    reponse = turtle.textinput('Question pour ouvrir la porte :', dico_portes[tuple(next_posi_mm)][0])

    turtle.listen()  # Relance l'écoute du clavier après turtle.textinput

    return reponse == dico_portes[tuple(next_posi_mm)][1]


def annonce(type_annonce, sous_type_annonce, objet_trouve):

    """ Gestionnaire des annonces"""

    effacement_annonce()  # Efface l'annonce qui est en place et se met en position annonces.
    turtle.color('#000000')  # Couleur noir pour écrire.
    
    if type_annonce == 'objet':  # Si on trouve un objet.
        turtle.write('Vous avez trouvé un nouvel objet : ' + objet_trouve, font=('Consolas', 10, 'bold'))

    elif type_annonce == 'porte':  # Si on veut franchir une porte.

        if sous_type_annonce == 'fermée':  # Si la porte est fermée.
            turtle.write('Cette porte est fermée !', font=('Consolas', 10, 'bold'))

        elif sous_type_annonce == 'correcte':  # Si la réponse à la question est correcte.
            turtle.write('Bonne réponse, la porte s\'ouvre !', font=('Consolas', 10, 'bold'))

        elif sous_type_annonce == 'faux':  # Si la réponse à la question est mauvaise.
            turtle.write('Mauvaise réponse !', font=('Consolas', 10, 'bold'))

    elif type_annonce == 'case jaune':  # Si on atteint l'objectif.

        if sous_type_annonce == 'victoire':  # Si on a tous les objets on gagne.
            turtle.write('Félicitation, vous avez gagné !', font=('Consolas', 14, 'bold '))

        elif sous_type_annonce == 'pas tous les objets':  # Si non.
            turtle.write('Vous devez rassembler tous les objets pour gagner !', font=('Consolas', 10, 'bold '))





# PARTIE 2 : INTIALISATION ET CORPS DU JEU

# Paramètres initials du jeu 

M = lire_matrice(fichier_plan)      # matrice du plan
P = calculer_pas(M)                 # le pas global
position_depart = list(POSITION_DEPART)   # Posiiton de départ du joueur en liste pour être modifiable
taille_joueur = P * RATIO_PERSONNAGE  # Taille du personnage
dico_portes = creer_dictionnaire_des_objets('dico_portes.txt')  # dictionnaire contenant des questions
dico_objets = creer_dictionnaire_des_objets('dico_objets.txt')  # dictionnaire des objets
inventaire_objet = set()


# CONSTANTES des fonctions
VIDE = 0
MUR = 1
BUT = 2
PORTE = 3
OBJET = 4


# Lancement du jeu 
turtle.tracer(0)  # Vitesse "instantanée".
turtle.up()  # Pas besoin de baisser la plume pour autre chose que le traçage.
turtle.hideturtle()


# Affiche la 1e annonce.
turtle.goto(POINT_AFFICHAGE_ANNONCES)
turtle.write('Menez votre personnage à l\'objectif en jaune', font=('Consolas', 12, 'bold'))


# Début de l'affichage de l'inventaire.
turtle.goto(70, 200)
turtle.write('Votre inventaire :', font=('Consolas', 12, 'bold'))


# Dessin du plan et du personnage
afficher_plan(M)
turtle.goto(coordonnees_centre(position_depart, P))  # Place le personnage au milieu de la case de départ.
turtle.dot(taille_joueur, COULEUR_PERSONNAGE)


# Le joueur prend les commandes
turtle.listen()  # Déclenche l’écoute du clavier

turtle.onkeypress(deplacer_gauche, "Left")  # Associe à la touche Left ie flèche gauche la fonction deplacer_gauche.
turtle.onkeypress(deplacer_droite, "Right")  # Important que les fonctions appelées dans onkeypress n'aient pas de ().
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")

turtle.mainloop()  # Place le programme en position d’attente d’une action du joueur
