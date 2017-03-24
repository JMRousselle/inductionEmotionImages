# -*- coding: utf-8 -*-

from twisted.internet import defer
import logging
import random
from datetime import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey, String

from le2mConfig.le2mParametres import MONNAIE
from le2mServ.le2mServParties import Partie
from le2mUtile.le2mUtileTools import get_monnaie

import inductionEmotionImagesParametres as parametres
import inductionEmotionImagesTextes as textes


logger = logging.getLogger("le2m.{}".format(__name__))


class PartieIEI(Partie):
    __tablename__ = "partie_inductionEmotionImages"
    __mapper_args__ = {'polymorphic_identity': 'inductionEmotionImages'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    
    IEI_traitement = Column(Integer)
    IEI_decision = Column(Integer)
    IEI_decision_temps = Column(Integer)
    IEI_gain_ecus = Column(Float)
    
    IEI_groupe_joueur = Column(Integer)
    IEI_ressenti = Column(String)
    IEI_type_emotion = Column(String)
    IEI_adjectif = Column(String)    
    
    def __init__(self, main_serveur, joueur):
        super(PartieIEI, self).__init__("inductionEmotionImages", "IEI")
        self._main_serveur = main_serveur
        self.joueur = joueur
        self._texte_recapitulatif = u""
        self._texte_final = u""
        self.IEI_gain_ecus = 0
        self.IEI_gain_euros = 0
        self._histo_vars = [
            "IEI_decision",
            "IEI_gain_ecus"
        ]
        self._histo = [
            [u"Décision", u"Gain"]
        ]

    @defer.inlineCallbacks
    def nouvelle_periode(self, periode):
        """
        Informe le remote du numéro de cette période (0)
        Vide l'historique
        :param periode: ici normalement 0 puis one-shot
        :return:
        """
        del self._histo[1:]
        yield (
            self.remote.callRemote("nouvelle_periode", periode)
        )
        logger.info(u"Période {} -> Ok".format(periode))

    @defer.inlineCallbacks
    def afficher_images(self):
        """
        Affiche la suite d images en fonction
        des emtions des groupes
        """
        self.son_groupe = self.IEI_groupe_joueur[-1]
        yield(self.remote.callRemote("afficher_images",  self.son_groupe))
        self.joueur.remove_wait_mode()

    @defer.inlineCallbacks
    def afficher_ecran_decision(self):
        """
        Affiche l'écran de décision sur le remote.
        Récupère la ou les décisions, le temps de décision et enregistre le tout
        dans la base.
        :param args:
        :param kwargs:
        :return:
        """
        debut = datetime.now()
        self.son_groupe = self.IEI_groupe_joueur[-1]
        reponse = \
            yield(
                self.remote.callRemote("afficher_ecran_decision", self.son_groupe)
        )
        if parametres.TYPE_EXPE == 0:
            self.IEI_type_emotion = \
                parametres.LISTE_TITRE_EMOTIONS[
                    int(parametres.LISTE_EMOTIONS[int(self.son_groupe)])
                ]
        else:
            self.IEI_type_emotion = \
                parametres.LISTE_TITRE_EMOTIONS[
                    int(parametres.EMOTION)
                ]
        self.IEI_ressenti = reponse["ressenti"]
        self.IEI_adjectif = reponse["adjectif"]        
        self.IEI_decision_temps = (datetime.now() - debut).seconds
        self.joueur.afficher_info("u{}".format(self.IEI_decision))
        self.joueur.remove_wait_mode()
        

    
    def calculer_gain_partie(self):
        """
        Calcul du gain de la partie
        :return:
        """
        self.IE_gain_ecus = 0
        self.IE_gain_euros = 0

