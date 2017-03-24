# -*- coding: utf-8 -*-
"""
Ce module contient les boites de dialogue du programme.
"""

from PyQt4 import QtGui, QtCore
import logging
import random
import os

from le2mClient.le2mClientGui.le2mClientGuiDialogs import GuiHistorique
import le2mClient.le2mClientTextes as textes_main

import inductionEmotionImagesParametres as parametres
import inductionEmotionImagesTextes as textes
from inductionEmotionImagesGuiSrc import inductionEmotionImagesGuiSrcDecision
from inductionEmotionImagesGuiSrc import afficheImagesGuiScr

logger = logging.getLogger("le2m.{}".format(__name__))


class GuiAfficheImages(QtGui.QDialog):
    def __init__(self, defered, automatique, ecran_attente, son_groupe):
        super(GuiAfficheImages, self).__init__(ecran_attente)

        # variables
        self._defered = defered
        self._automatique = automatique

        # création gui
        self.ui = afficheImagesGuiScr.Ui_Dialog()
        self.ui.setupUi(self)
        
        getParentFolder = lambda fh: os.path.abspath(os.path.join(os.path.normpath(fh),os.path.pardir))
        chemin_courant = getParentFolder(os.getcwd())
        chemin_dossier_groupes_images = u"{}{}le2mProgrammes-v2.0{}inductionEmotionImages{}inductionEmotionImagesGuiSrc{}images".format(chemin_courant,  os.sep,  os.sep,  os.sep, os.sep)

        if int(son_groupe) == 0:
            self.chemin_images = chemin_dossier_groupes_images + os.sep + "honte"
        elif int(son_groupe) == 1:
            self.chemin_images = chemin_dossier_groupes_images + os.sep + "fierte"
        elif int(son_groupe) == 2:
            self.chemin_images = chemin_dossier_groupes_images + os.sep + "joie"
        elif int(son_groupe) == 3:
            self.chemin_images = chemin_dossier_groupes_images + os.sep + "tristesse"
        elif int(son_groupe) == 4:
            self.chemin_images = chemin_dossier_groupes_images + os.sep + 'controle'
        print "self.chemin_images = ",  self.chemin_images    
        liste_extension = (".jpg",  ".jpeg",  ".gif",  ".png",  ".JPG",  ".JPEG",  ".GIF",  ".PNG")
        self.liste_des_images =[f for f in os.listdir(self.chemin_images) if os.path.splitext(f)[1] in liste_extension]
        
        # On trie les images
        self.liste_images = sorted(self.liste_des_images)
        logger.debug(u"Liste images: %s" % (self.liste_images, ))      
        self.compteur = 0
        image = QtGui.QPixmap("%s%s%s" % (self.chemin_images,  os.sep,  self.liste_images[self.compteur]))
        self.ui.label_affiche_images.setPixmap(image)
        try:
            self.timer.start(parametres.TEMPS_AFFICHAGE_IMAGES)
        except AttributeError:
            self.timer = QtCore.QTimer()
            self.connect(self.timer,  QtCore.SIGNAL('timeout()'),  self._next)
            self.timer.start(parametres.TEMPS_AFFICHAGE_IMAGES * 1000)   
#        self.deferred = defer.Deferred()      
        self.showFullScreen()
#        return self.deferred.callback(1)
    
    def _next(self):
        self.compteur += 1
        if self.compteur < len(self.liste_images):
            image = QtGui.QPixmap("%s%s%s" % (self.chemin_images,  os.sep,  self.liste_images[self.compteur]))
            self.ui.label_affiche_images.setPixmap(image) 
            self.timer.start(parametres.TEMPS_AFFICHAGE_IMAGES * 1000)
        else:
            self._stop()
            
    def _stop(self):
        self.hide()
        try:
            self.timer.stop()
        except AttributeError:
            pass 
        self._defered.callback(1)        

class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, ecran_attente, son_groupe):
        super(GuiDecision, self).__init__(ecran_attente)

        # variables
        self._defered = defered
        self._automatique = automatique

        # création gui
        self.ui = inductionEmotionImagesGuiSrcDecision.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.label_periode.setVisible(False)
        self.ui.pushButton_historique.setVisible(False)

        self.ui.label_periode.setVisible(False)
        self.ui.pushButton_historique.setVisible(False)

        # Affichage des adjectifs dans les radio_button apres tri aleatoire
        self.alea_adj = random.sample(
            parametres.ADJECTIFS, len(parametres.ADJECTIFS)
        )
        self.ui.radioButton_adj1.setText(self.alea_adj[0])
        self.ui.radioButton_adj2.setText(self.alea_adj[1])
        self.ui.radioButton_adj3.setText(self.alea_adj[2])
        self.ui.radioButton_adj4.setText(self.alea_adj[3])
        self.ui.radioButton_adj5.setText(self.alea_adj[4])
        self.ui.radioButton_adj6.setText(self.alea_adj[5])
        self.ui.radioButton_adj7.setText(self.alea_adj[6])
        self.ui.radioButton_adj8.setText(self.alea_adj[7])
        self.ui.radioButton_adj9.setText(self.alea_adj[8])

        # bouton box
        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Cancel).setVisible(False)

        # titre et taille
        self.setWindowTitle("Décision")
        self.setFixedSize(1024, 800)

        # automatique
        if self._automatique:
            self.randrep = random.randint(1, 9)
            reponseCochee = getattr(
                self.ui, 'radioButton_adj' + str(self.randrep)
            )
            reponseCochee.setChecked(True)            
            if parametres.TYPE_EXPE == 0:
                self.ui.textEdit_ressenti.setPlainText(
                    u"texte généré automatiquement de test automatique pour "
                    u"l'émotion {}".format(
                        parametres.LISTE_TITRE_EMOTIONS[
                            int(parametres.LISTE_EMOTIONS[int(son_groupe)])
                        ])
                )
            else:
                self.ui.textEdit_ressenti.setPlainText(
                    u"texte généré automatiquement de test automatique pour "
                    u"l'émotion {}".format(
                        parametres.LISTE_TITRE_EMOTIONS[
                            int(parametres.EMOTION)])
                )
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(self._accept)
            self._timer_automatique.start(7000)
                
    def reject(self):
        pass
    
    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        reponse = {}
        self._decision = unicode(
            self.ui.textEdit_ressenti.toPlainText().toUtf8(), "utf-8")
            
        self.la_decision = 0 
        for i in range(1, 10):
            te = getattr(self.ui,  'radioButton_adj' + str(i))
            if te.isChecked():
                self.la_decision = i
        if self.la_decision == 0:
            QtGui.QMessageBox.warning(self, "ATTENTION" , u"Vous devez choisir un adjectif",  QtGui.QMessageBox.Ok)
            return        

        self._adjectif = ''
        for i in range(1, 10):
            te = getattr(self.ui, 'radioButton_adj' + str(i))
            if te.isChecked():
                self._adjectif = self.alea_adj[i - 1]            
        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, u"Confirmation",
                u"Vous confirmez votre décision?", 
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes
            )
            if confirmation != QtGui.QMessageBox.Yes: 
                return
                
        reponse["ressenti"] = self._decision
        reponse["adjectif"] = self._adjectif
        logger.info(u"Renvoi de {}".format(reponse))
        self._defered.callback(reponse)
        self.accept()
