# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""
__author__ = "Dimitri DUBOIS"

# pour i18n:
# 1)  décommenter les lignes ci-après,
# 2) entourer les expressions à traduire par _IEI()
# 3) dans le projet créer les dossiers locale/fr_FR/LC_MESSAGES
# en remplaçant fr_FR par la langue souhaitée
# 4) créer le fichier inductionEmotionImages.po: dans invite de commande, taper:
# xgettext fichierTextes.py -p locale/fr_FR/LC_MESSAGES -d inductionEmotionImages
# 5) avec poedit, éditer le fichier inductionEmotionImages.po qui a été créé

# import os
# from le2mConfig.le2mParametres import LE2M_DIRECTORY_PROGRAMMES
# try:
#     import gettext
#     localedir = os.path.join(
#         LE2M_DIRECTORY_PROGRAMMES, "inductionEmotionImages", "locale"
#     )
#     _IEI = gettext.translation("inductionEmotionImages", localedir).ugettext
# except ImportError:
#     _IEI = lambda s: s

from collections import namedtuple
from le2mUtile.le2mUtileTools import get_pluriel
import inductionEmotionImagesParametres as parametres

TITLE_MSG = namedtuple("TITLE_MSG", "titre message")


# ECRAN DECISION ===============================================================
DECISION_titre = u"Decision"
DECISION_explication = u"Explanation text"
DECISION_label = u"Decision label text"
DECISION_erreur = TITLE_MSG(
    u"Warning",
    u"Warning message"
)
DECISION_confirmation = TITLE_MSG(
    u"Confirmation",
    u"Confirmation message"
)


# ECRAN RECAPITULATIF ==========================================================
def get_recapitulatif(*args):
    txt = u"Summary text"
    return txt


# TEXTE FINAL PARTIE ===========================================================
def get_texte_final(gain_ecus, gain_euros):
    txt = u"Vous avez gagné {gain_en_ecu}, soit {gain_en_euro}.".format(
        gain_en_ecu=get_pluriel(gain_ecus, u"ecu"),
        gain_en_euro=get_pluriel(gain_euros, u"euro")
    )
    return txt