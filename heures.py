#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bibliothèques standards
import logging
import datetime

import tkinter as tk

from pathlib import Path

# PIPy
import sqlalchemy as sqla

# Bibliothèques maison
from polygphys.outils.config import FichierConfig
from polygphys.outils.base_de_donnees import BaseDeDonnées
from polygphys.outils.base_de_donnees.dtypes import column
from polygphys.outils.reseau import DisqueRéseau
from polygphys.outils.journal import Formats, Journal

from polygphys.outils.interface_graphique import InterfaceHandler
from polygphys.outils.interface_graphique.tableau import Formulaire
from polygphys.outils.interface_graphique.tkinter import tkHandler

class FeuilleDeTempsConfig(FichierConfig):

    def default(self) -> str:
        return (Path(__file__).parent / 'heures.cfg').open().read()

class FeuilleDeTemps(BaseDeDonnées):
    colonnes_standard = (column('index', int, primary_key=True),
                         column('payeur', str),
                         column('date', datetime.datetime),
                         column('description', str),
                         column('demandeur', str),
                         column('heures', float),
                         column('atelier', bool),
                         column('precision_dept', str),
                         column('autres', str))
    table_standard = 'heures'

    def __init__(self, adresse: str, reflect: bool = True):
        metadata = sqla.MetaData()
        super().__init__(adresse, metadata)

        if reflect:
            moteur = self.create_engine()
            self.metadata.reflect(moteur)
        else:
            sqla.Table(self.table_standard,
                       self.metadata,
                       *self.colonnes_standard)

class FormulaireDeTemps(Formulaire):

    def __init__(self, handler: InterfaceHandler, feuille: FeuilleDeTemps):
        super().__init__(handler, feuille, feuille.table_standard)


if __name__ == '__main__':
    chemin = Path('~/Documents/Polytechnique/Heures').expanduser()
    config = FeuilleDeTempsConfig(chemin / 'heures.cfg')

    adresse = config.get('bd', 'adresse')

    feuille_de_temps = FeuilleDeTemps(adresse)

    racine = tk.Tk()
    handler = tkHandler(racine)
    formulaire = FormulaireDeTemps(handler, feuille_de_temps)
    formulaire.grid(0, 0)
    racine.mainloop()
