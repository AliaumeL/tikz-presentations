#!/usr/bin/env python3
#
# Aliaume LOPEZ
#
# Creating slides using tikz and python
# 
# Candidature MCF Bordeaux 2025
#

from tikz import *

import tikz_presentations_aliaume as tpa

from tikz_presentations_aliaume.components.utils import *

import yaml

import bibtexparser

import math

import random
import dataclasses
from typing import Literal, Generator, Callable, List, Union, Tuple, Optional




@dataclasses.dataclass
class Bibliometrie:
    def draw(self, pic):

        conf_mult = [
                "CSL'17",
                "QPL'17",
                "CSL'18",
                "LICS'23",
                "CAV'25",
        ]

        conf_solo = [ "CSL'21", "LICS'22", "FoSSaCS'23", "STACS'25"]

        journaux = [
                "Mathematical Structures in Computer Science",
                "Colloquium Mathematicum",
                ]

        soumissions = [ "MFCS'25" ]

        num_soum  = len(soumissions)
        num_solo  = len(conf_solo)
        num_conf  = len(conf_mult) + len(conf_solo)
        num_journ = len(journaux)

        pic.style("category", 
                  text_width="6cm",
                  rounded_corners="2mm",
                  thick=True,
                  draw="A5",
                  inner_sep="1em",
                  anchor="north")

        pic.node(r"""
                 \begin{minipage}{6cm}
                 \begin{tabular}{ll}
                 \textbf{Conférences} & """ + f"{num_conf} (dont {num_solo} en seul auteur)" + r"""\\""" + 
                 r"""\textbf{Journaux} & """ + f"{num_journ}" + r"""\\""" +
                 r"""\textbf{Soumissions} & """ + f"{num_soum}" + r"""\\""" +
                 r"""
                    \end{tabular}
                 \end{minipage}""",
                 at=(0,0),
                 category=True)




    def __iter__(self):
        yield (0, Bibliometrie())


@dataclasses.dataclass
class QuiSuisJe:
    bib : Bibliometrie

    def draw(self, pic):
        pic.draw((0,5), node("Parcours Académique", 
                               font="\\huge\\scshape", anchor="north"))

        pic.style("block",
                  rounded_corners="2mm",
                  anchor="north",
                  text_width="5cm")

        pic.node(r"""
                 \begin{minipage}{5cm}
                 \textbf{ENS Paris-Saclay} \hfill (2015 -- 2019)

                 \vspace{1em}
                 Agrégation de Mathématiques

                 \vspace{1em}
                 Stages de L3 et M1 
                 à Birmingham et Ljubljana

                 \vspace{1em}
                 Stage M2 au LSV \newline
                        \bsc{Goubault-Larrecq}
                        \&
                        \bsc{Schmitz}
                 \end{minipage}
                 """,
            at=(-6,3.5), 
            block=True)

        pic.node(r"""
                 \begin{minipage}{5cm}
                 \textbf{LMF \& IRIF} \hfill (2019 -- 2023)

                 \vspace{1em}
                 Thèse sous la direction de \newline
                        \bsc{Goubault-Larrecq}
                        \&
                        \bsc{Schmitz}

                 \vspace{1em}
                 \textcolor{A2}{\textbf{2 Prix de Thèse}} \newline
                    \emph{Ackermann Award}
                    \& \newline  \emph{E. W. Beth Dissertation Prize}

                 \vspace{1em}
                 \textcolor{A5}{\textbf{Césure}} (1 an)
                    \newline
                    \emph{Autorité de Sûreté Nucléaire}
                 \end{minipage}
                 """,
            at=(0,3.5), 
            block=True)

        pic.node(r"""
                 \begin{minipage}{5cm}
                 \textbf{Varsovie} \hfill (2023 -- 2025)

                 \vspace{1em}
                 Postdoctorat \newline
                        \bsc{Mikołaj Bojańczyk}

                 \vspace{1em}
                 \textbf{Co-organisation} Autobóz 2024 

                 \vspace{1em}
                 Membre du comité de programme de \textbf{CSL'26}

                 \vspace{1em}
                 Co-encadrement de 2 stagiaires
                 \end{minipage}
                 """,
            at=(6,3.5), 
            block=True)

        pic.node(r"""
            «~Théorèmes de préservation pour la logique au premier ordre : localité, topologie et constructions limites.~»
                 """,
                 at=(0,-1.7),
                 font=r"\itshape",
                 )
        bibscope = pic.scope(yshift="-2.5cm", xshift="0cm")
        self.bib.draw(bibscope)



    def __iter__(self):
        yield (0, self)

# create a presentation

if __name__ == "__main__":
    tf = TitleFrame(with_name=True)
    qs = QuiSuisJe(bib=Bibliometrie())

    frames = Sequential([tf,qs], pos=0)

    preview_animation(frames)
