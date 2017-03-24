# -*- coding: utf -8 -*-
"""
Ce module contient les variables et les paramètres de la partie
Les variables ne doivent pas être changées
Les paramètres peuvent être changés, mais, par sécurité, demander au développeur
"""

# variables
BASELINE = 0

# paramètres
TRAITEMENT = BASELINE
TAUX_CONVERSION = 1
NOMBRE_PERIODES = 1
TAILLE_GROUPES = 4
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"

# Temps d'affichage des images en secondes
TEMPS_AFFICHAGE_IMAGES = 5


""" Codes emotions
0 = Honte
1 = Fierte
2 = Joie
3 = tristesse
4 = controle
"""
TYPE_EXPE = 0   # 0 = une emotion par groupe, 1 = meme emotion pour tous les groupes
# Liste des emotions dans le cas ou TYPE_EXPE=0 (labo pas forcement rempli)
LISTE_EMOTIONS = [0, 1, 2, 3, 4]
LISTE_TITRE_EMOTIONS = ["HONTE", "FIERTE", "JOIE", "TRISTESSE", "CONTROLE"]
# emotion a prendre pour la session si TYPE_EXPE=1
EMOTION = 4
# Adjectifs
ADJECTIFS = [u"Humilié", u"Honteux", u"Heureux", u"Réjoui", u"Fier", u"Estimé",
             u"Triste", u"Malheureux", u"Indifférent"]
