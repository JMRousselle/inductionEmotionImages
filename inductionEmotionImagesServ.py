# -*- coding: utf-8 -*-

from twisted.internet import defer
import logging
from collections import OrderedDict

from le2mUtile import le2mUtileTools

import inductionEmotionImagesParametres as parametres
import inductionEmotionImagesTextes as textes
from inductionEmotionImagesPartie import PartieIEI

logger = logging.getLogger("le2m.{}".format(__name__))
    

class Serveur(object):
    def __init__(self, main_serveur):
        self._main_serveur = main_serveur
        self._main_serveur.gestionnaire_experience.ajouter_to_remote_parties(
            "inductionEmotionImages", "RemoteIEI")

        # création du menu de la partie dans le menu expérience du serveur
        actions = OrderedDict()
#        actions[u"Configurer"] = self._configurer
        actions[u"Afficher les paramètres"] = \
            lambda _: self._main_serveur.gestionnaire_graphique. \
            afficher_information2(
                le2mUtileTools.get_module_info(parametres), u"Paramètres"
            )
        actions[u"Démarrer"] = lambda _: self._demarrer()
        actions[u"Afficher les gains"] = \
            lambda _: self._main_serveur.gestionnaire_experience.\
            afficher_ecran_gains_partie("inductionEmotionImages")
        self._main_serveur.gestionnaire_graphique.ajouter_to_menu_experience(
            u"Induction émotion par des images", actions)

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Lancement de la partie. Définit tout le déroulement
        :return:
        """
        confirmation = self._main_serveur.gestionnaire_graphique.\
            afficher_question(u"Démarrer inductionEmotionImages?")
        if not confirmation:
            return
        
        # initialisation de la partie ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._main_serveur.gestionnaire_experience.initialiser_partie(
            "inductionEmotionImages", parametres
        )
        
        # formation des groupes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if parametres.TAILLE_GROUPES > 0:
            try:
                self._main_serveur.gestionnaire_groupes.former_groupes(
                    self._main_serveur.gestionnaire_joueurs.get_liste_joueurs(),
                    parametres.TAILLE_GROUPES, forcer_nouveaux=True
                )
            except ValueError as e:
                self._main_serveur.gestionnaire_graphique.afficher_erreur(
                    e.message)
                return 
    
        # creation de la partie chez chq joueur ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for j in self._main_serveur.gestionnaire_joueurs.get_liste_joueurs():
            if not j.get_partie(PartieIEI):
                yield (
                    j.ajouter_partie(PartieIEI(
                        self._main_serveur, j)
                    )
                )
        self._tous = self._main_serveur.gestionnaire_joueurs.get_liste_joueurs(
            'inductionEmotionImages')

        # On remplit la variable groupe_joueur dans la base
        for j in self._tous:
            j.IEI_groupe_joueur = j.joueur.groupe
            
        # début de la partie emotion=======================================
        # en mettant la période à 0 les écrans n'afficheront pas période ...
        yield (self._main_serveur.gestionnaire_experience.run_func(
            self._tous, "nouvelle_periode", 0)
        )

        # Affichage des images
        yield(self._main_serveur.gestionnaire_experience.run_step(
            u"Images", self._tous, "afficher_images")
        )

        # décision emotion~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        yield (self._main_serveur.gestionnaire_experience.run_step(
            u"Decision", self._tous, "afficher_ecran_decision")
        )
        
        
        # FIN DE LA PARTIE =====================================================
        self._main_serveur.gestionnaire_experience.finaliser_partie(
            "inductionEmotionImages")
