# -*- coding: utf-8 -*-

from twisted.internet import defer
from twisted.spread import pb
import logging
import random

from le2mClient.le2mClientGui.le2mClientGuiDialogs import GuiRecapitulatif

import inductionEmotionImagesParametres as parametres
from inductionEmotionImagesGui import GuiDecision
from inductionEmotionImagesGui import GuiAfficheImages

logger = logging.getLogger("le2m.{}".format(__name__))


class RemoteIEI(pb.Referenceable):
    """
    Class remote, celle qui est contactée par le client (sur le serveur)
    """
    def __init__(self, main_client):
        self._main_client = main_client
        self._main_client.ajouter_remote('inductionEmotionImages', self)
        self._periode_courante = 0
        self._historique = []

    def remote_nouvelle_periode(self, periode):
        """
        Appelé au début de chaque période.
        L'historique est "vidé" s'il s'agit de la première période de la partie
        Si c'est un jeu one-shot appeler cette méthode en mettant 0
        :param periode: le numéro de la période courante
        :return:
        """
        logger.info(u"Période {}".format(periode))
        self._periode_courante = periode
        if self._periode_courante == 1:
            del self._historique[:]

    def remote_afficher_images(self, son_groupe):
        """
        Affiche la suite d images
        """
        logger.info(u"Affichage des images")
        if self._main_client.simulation:
            return
        else:
            defered = defer.Deferred()
            ecran_decision = GuiAfficheImages(
                defered,
                self._main_client.automatique,
                self._main_client.gestionnaire_graphique.ecran_attente,
                son_groupe)
            ecran_decision.show()
            return defered            
        
    def remote_afficher_ecran_decision(self, son_groupe):
        """
        Affiche l'écran de décision
        :return: deferred
        """
        logger.info(u"Affichage de l'écran de décision")
        if self._main_client.simulation:
            reponse = {}
            self.alea_adj = random.sample(
                parametres.ADJECTIFS, len(parametres.ADJECTIFS)
            )
            self.randrep = random.randint(1, 9)
            reponse["adjectif"] = self.alea_adj[self.randrep - 1]  
            if parametres.TYPE_EXPE == 0:
                reponse["ressenti"] = \
                    u"texte généré automatiquement de test simulation code " \
                    u"émotion à {} donc le {}".format(
                        son_groupe,
                        parametres.LISTE_TITRE_EMOTIONS[
                            int(parametres.LISTE_EMOTIONS[int(son_groupe)])
                        ]
                    )
            else:
                reponse["ressenti"] = \
                    u"texte généré automatiquement de test simulation code " \
                    u"émotion à {} donc le {}".format(
                        son_groupe,
                        parametres.LISTE_TITRE_EMOTIONS[int(parametres.EMOTION)]
                    )
            logger.info(u"Renvoi: {}".format(reponse))
            return reponse
        else: 
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered,
                self._main_client.automatique,
                self._main_client.gestionnaire_graphique.ecran_attente,
                son_groupe)
            ecran_decision.show()
            return defered

    def remote_afficher_ecran_recapitulatif(self, texte_recap, historique):
        """
        Affiche l'écran récapitulatif
        :param texte_recap: le texte affiché
        :param historique: l'historique de la partie
        :return: deferred
        """
        self._historique = historique
        if self._main_client.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = GuiRecapitulatif(
                defered,
                self._main_client.automatique,
                self._main_client.gestionnaire_graphique.ecran_attente,
                self._periode_courante, self._historique, texte_recap)
            ecran_recap.show()
            return defered
