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

with open("./data/aliaume-cv.yaml", "r") as stream:
    try:
        CV = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

@dataclasses.dataclass
class Teachometrie:
    def draw(self, pic):

        pic.style(
            "category",
            text_width="6cm",
            rounded_corners="2mm",
            thick=True,
            draw="A5",
            inner_sep="1em",
            anchor="north",
        )

        pic.node(
            r"""
                 \begin{minipage}{6cm}
                 \vspace{0.5em}
                 \begin{tabular}{ll}
                 \textbf{Info. Théorique} & 72h \\
                 \textbf{Programmation} & 60h \\
                 \textbf{Réseaux / Système} & 48h \\
                 \end{tabular}
                 \end{minipage}""",
            at=(0, 0),
            category=True,
        )

        pic.node(
            r"""Cours TD/TP""",
            at=(0, 0.3),
            category=True,
            inner_sep="0.5em",
            align="center",
            font="\\bfseries\\scshape",
            fill="A5hint",
            text_width="4cm",
        )

    def __iter__(self):
        yield (0, Bibliometrie())


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

        conf_solo = ["CSL'21", "LICS'22", "FoSSaCS'23", "STACS'25"]

        journaux = [
            "Mathematical Structures in Computer Science",
            "Colloquium Mathematicum",
        ]

        soumissions = ["MFCS'25"]

        num_soum = len(soumissions)
        num_solo = len(conf_solo)
        num_conf = len(conf_mult) + len(conf_solo)
        num_journ = len(journaux)

        pic.style(
            "category",
            text_width="6cm",
            rounded_corners="2mm",
            thick=True,
            draw="A5",
            inner_sep="1em",
            anchor="north",
        )

        pic.node(
            r"""
                 \begin{minipage}{6cm}
                 \vspace{0.5em}
                 \begin{tabular}{ll}
                 \textbf{Conférences} & """
            + f"{num_conf} (dont {num_solo} en seul auteur)"
            + r"""\\"""
            + r"""\textbf{Journaux} & """
            + f"{num_journ}"
            + r"""\\"""
            + r"""\textbf{Soumissions} & """
            + f"{num_soum}"
            + r"""\\"""
            + r"""
                    \end{tabular}
                 \end{minipage}""",
            at=(0, 0),
            category=True,
        )

        pic.node(
            r"""Publications""",
            at=(0, 0.3),
            category=True,
            inner_sep="0.5em",
            align="center",
            font="\\bfseries\\scshape",
            fill="A5hint",
            text_width="4cm",
        )

    def __iter__(self):
        yield (0, Bibliometrie())


@dataclasses.dataclass
class QuiSuisJe:
    bib: Bibliometrie

    def draw(self, pic):
        pic.draw(
            (0, 5), node("Parcours Académique", font="\\huge\\scshape", anchor="north")
        )

        pic.style("block", rounded_corners="2mm", anchor="north", text_width="5cm")

        pic.node(
            r"""
                 \begin{minipage}{5cm}
                 \textbf{ENS Paris-Saclay} \hfill (2015 -- 2019)

                 \vspace{1em}
                 Agrégation de Mathématiques
                 \newline
                 \emph{Option Info. Classé 5e}

                 \vspace{1em}
                 Stages de L3 et M1 
                 \newline
                 \emph{Birmingham et Ljubljana}

                 \vspace{1em}
                 Stage M2 au LSV \newline
                        \bsc{Goubault-Larrecq}
                        \&
                        \bsc{Schmitz}
                 \end{minipage}
                 """,
            at=(-6, 3.5),
            block=True,
        )

        pic.node(
            r"""
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
            at=(0, 3.5),
            block=True,
        )

        pic.node(
            r"""
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
            at=(6, 3.5),
            block=True,
        )

        pic.node(
            r"""
            «~Théorèmes de préservation pour la logique au premier ordre : localité, topologie et constructions limites.~»
                 """,
            at=(0, -1.7),
            font=r"\itshape",
        )

        bibscope = pic.scope(yshift="-2.5cm", xshift="0cm")
        self.bib.draw(bibscope)

    def __iter__(self):
        yield (0, self)


@dataclasses.dataclass
class ExtraTeachingPower:
    def draw(self, pic):
        extras = [
            {"title": "Agrégation Math. Info.", "color": "D2"},
            {"title": "Développeur Fullstack", "color": "D2"},
            {"title": "Projets Personnels", "color": "D2"},
            {"title": "Encadrement (2 mois, L2)", "color": "D2"},
        ]

        logos = [
            "./images/software/docker.png",
            "./images/software/linux.png",
            "./images/software/yunohost.png",
            "./images/software/github.png",
            "./images/software/haskell.png",
            "./images/software/rust.png",
            "./images/software/nix.png",
        ]

        for i, extras in enumerate(extras):
            pic.node(
                extras["title"],
                at=(0, -i * 0.7),
                font="\\scshape",
                rounded_corners="2mm",
                draw=extras["color"],
                fill=f"{extras['color']}hint",
                anchor="north west",
                text_width="5cm",
            )

        grid = [
            (6, -1),
            (7, -1),
            (8, -1),
            (6, -2.3),
            (7, -2.3),
            (8, -2.3),
            (9, -2.3),
        ]
        for logo, pos in zip(logos, grid):
            (x, y) = pos
            pic.node(
                r"\includegraphics[width=0.5cm]{" + logo + "}",
                at=(x, y + 0.2),
                anchor="center",
                fill="white",
            )

    def __iter__(self):
        yield (0, ExtraTeachingPower())


@dataclasses.dataclass
class TeachingDuties:
    fullsize: bool = False

    def draw(self, pic):
        data = CV["teaching"]

        scope = pic.scope(xshift="-9cm", yshift="4cm")
        scope.node(
            "Enseignements Effectués",
            at=(4.5, 0.7),
            font="\\bfseries\\scshape",
        )

        tothours = sum(
            int(cours["equivTD"]) for duty in data for cours in duty["courses"]
        )

        if self.fullsize:
            scope.node(
                r"Total~: " + str(tothours) + r"h~~",
                at=(8, -6.3),
                align="right",
                anchor="east",
                font="\\bfseries\\scshape",
            )

        count = 0
        for duty in data:
            location = duty["location"]
            cstart = count
            cend = cstart + len(duty["courses"]) - 1
            locationy = -(cstart + (cend - cstart) / 2) * 0.7
            uprighty = -cstart * 0.7 + 0.3
            downlefty = -cend * 0.7 - 0.3
            scope.draw(
                (0, uprighty),
                rectangle((9, downlefty)),
                fill=f"{duty['color']}hint",
            )

            if self.fullsize:
                scope.node(
                    location + r"\newline" + duty["start"] + r" -- " + duty["end"],
                    at=(9, locationy),
                    text_width="6cm",
                    font="\\bfseries",
                    anchor="west",
                )
                scope.node(
                    r"\includegraphics[width=1cm]{./images/institutions/"
                    + duty["logo"]
                    + "}",
                    at=(15, locationy),
                    anchor="west",
                    fill="white",
                )
            for cours in duty["courses"]:
                title = cours["title"]
                hours = cours["equivTD"]
                level = cours["shortlevel"]

                y = -count * 0.7
                count += 1

                scope.node(
                    title,
                    at=(0, y),
                    anchor="west",
                    text_width="7cm",
                )
                scope.node(
                    f"{hours}h",
                    at=(7, y),
                    anchor="west",
                    text_width="1cm",
                )
                scope.node(
                    level,
                    at=(8, y),
                    anchor="west",
                    text_width="1cm",
                )

    def __iter__(self):
        yield (0, TeachingDuties())


@dataclasses.dataclass
class TeachingNeeds:
    detailed: bool = False

    def draw(self, pic):

        besoins = [
            {
                "title": "Informatique Théorique",
                "cours": [
                    "Mathématiques",
                    "Automates",
                    "Complexité",
                    "Algorithmique",
                    "Logique",
                ],
                "confidence": 3,
            },
            {
                "title": "Programmation",
                "cours": [
                    "Génie Logiciel",
                    "Impérative",
                    "Fonctionnelle",
                    "Système",
                    "Objet",
                    "Web",
                ],
                "confidence": 3,
            },
            {
                "title": "Systèmes et Réseaux",
                "cours": ["Systèmes", "BDD", "Réseaux", "Cloud"],
                "confidence": 2,
            },
            {
                "title": "Sécurité",
                "cours": ["Cryptographie", "Systèmes", "Réseaux"],
                "confidence": 0,
            },
        ]

        pic.node(
            r"Besoins",
            at=(7, 1),
            font="\\bfseries\\scshape",
            anchor="center",
        )

        pic.node(
            r"\includegraphics[width=8cm]{./images/institutions/inp-bordeaux.png}",
            at=(1, -5),
            opacity=0.1,
            anchor="south west",
            fill="white",
        )

        pic.node(
            r"Semestre 9: Méthodes Formelles",
            at=(5, -7.5),
            text_width="6cm",
            rounded_corners="2mm",
            fill="A5hint",
            align="center",
            inner_sep="0.5em",
            draw="A5",
            thick=True,
        )

        for i, besoin in enumerate(besoins):
            x = 1
            y = -i * 2 - 0.1
            pic.node(
                besoin["title"],
                at=(x, y),
                minimum_height="1.5cm",
                anchor="west",
                font="\\bfseries",
                align="center",
                thick=True,
                rounded_corners="2mm",
                draw="A5",
                text_width="4cm",
            )

            for j, cours in enumerate(besoin["cours"]):
                xp = 5.2 if j % 2 == 0 else 7.2
                yp = 1 + y - (j // 2 + 1) * 0.5
                pic.node(
                    r"\strut " + cours,
                    at=(xp, yp),
                    anchor="west",
                    font="\\itshape\\small",
                )

            if not self.detailed:
                conf = besoin["confidence"]
                if conf == 0:
                    pic.node(
                        r"\strut " + r"\xmark",
                        at=(0.2, y),
                        anchor="west",
                        font="\\bfseries\\large",
                        text="A2",
                    )
                elif conf == 2:
                    pic.node(
                        r"\strut " + r"$\bullet$",
                        at=(0.2, y),
                        anchor="west",
                        font="\\bfseries\\large",
                        text="A4",
                    )
                elif conf == 3:
                    pic.node(
                        r"\strut " + r"\cmark",
                        at=(0.2, y),
                        anchor="west",
                        font="\\bfseries\\large",
                        text="A5",
                    )

    def __iter__(self):
        yield (0, TeachingNeeds())


@dataclasses.dataclass
class Teaching:

    extras: bool = True
    fullsize: bool = False
    needs: bool = False
    fullneeds: bool = True

    def draw(self, pic):
        td = TeachingDuties(fullsize=self.fullsize)
        td.draw(pic)

        if self.extras:
            escope = pic.scope(xshift="-9cm", yshift="-2cm")

            extras = ExtraTeachingPower()
            extras.draw(escope)

        if self.needs:
            tnscope = pic.scope(xshift="0cm", yshift="3.7cm")
            needs = TeachingNeeds(detailed=self.fullneeds)
            needs.draw(tnscope)

    def __iter__(self):
        yield (0, Teaching(False, True))
        yield (1, Teaching(True, False))
        yield (1, Teaching(True, False, True))
        yield (1, Teaching(True, False, True, False))


@dataclasses.dataclass
class ThemesAndLocations:
    locations: bool = False

    def draw(self, pic):
        themes = [("Ordres", cWA), ("Automates", cAut), ("Logique", cBD)]
        for i, (theme, col) in enumerate(themes):
            angle = math.radians(i * 120)
            x = 1 * math.cos(angle)
            y = 1 * math.sin(angle)
            pic.draw(
                (x, y),
                circle(2),
                color=col,
                thick=True,
            )
            pic.node(
                theme,
                at=(3 * x, 3 * y),
                font="\\bfseries\\scshape",
                anchor="center",
                fill=f"{col}hint",
                draw=col,
                rounded_corners="2mm",
                inner_sep="0.5em",
                text_width="2cm",
                align="center",
            )

        if not self.locations:
            return

        labs = [
            {"logo": "./images/institutions/irif.pdf"},
            {"logo": "./images/institutions/lmf.pdf"},
            {"logo": "./images/institutions/university_of_warsaw.pdf"},
            {"logo": "./images/institutions/mpi-sws.png"},
            {"logo": "./images/institutions/lis-marseille.pdf"},
            {"logo": "./images/institutions/labri.pdf"},
        ]

        # split logos in two groups of equal size
        half = len(labs) // 2
        labs1 = labs[:half]
        labs2 = labs[half:]
        scope1 = pic.scope(xshift="-7cm", yshift="2.5cm")
        scope2 = pic.scope(xshift="7cm", yshift="2.5cm")
        for scope, labs in [(scope1, labs1), (scope2, labs2)]:
            for i, lab in enumerate(labs):
                x = 0
                y = -i * 2
                scope.draw(
                    (x, y),
                    node(
                        r"""
                        \includegraphics[width=2cm]{"""
                        + lab["logo"]
                        + r"""}""",
                        anchor="center",
                    ),
                    thick=True,
                )

    def __iter__(self):
        yield (0, ThemesAndLocations(True))


@dataclasses.dataclass
class NSquareWqo:
    points: List[Tuple[int, int]]
    grid_size: int = 10
    grid_step: int = 1

    def draw(self, picture):
        picture.draw(
            (0, -2),
            node(r"$(\mathbb{N} \times \mathbb{N}, \leq)$"),
        )

        pic = picture.scope(rotate="45")
        pic.style("axisStyle", thick=True, opt="->")
        pic.style("rowStyle", color="C1")
        pic.style("columnStyle", color="C1")
        pic.style(
            "selectedNode",
            fill="D3",
            draw="A2",
            circle=True,
            inner_sep="2pt",
            minimum_size="0pt",
        )

        step = self.grid_step
        n = self.grid_size

        # create a grid
        lines = [[(i, 0), (i, n)] for i in range(0, n, step)]
        columns = [[(0, j), (n, j)] for j in range(0, n, step)]

        for x, y in self.points:

            pic.draw(
                (x * step, y * step),
                lineto((x * step, self.grid_size)),
                lineto((self.grid_size, self.grid_size)),
                lineto((self.grid_size, y * step)),
                lineto((x * step, y * step)),
                draw="A2",
                fill="A2",
            )

            # pic.draw((x * step, y * step),
            #          lineto((x * step, 0)),
            #          lineto((0, 0)),
            #          lineto((0, y * step)),
            #          lineto((x * step, y * step)),
            #          draw="D3bg",
            #          fill="D3bg")

        # draw the grid
        for i, coords in enumerate(lines):
            if i == 0:
                pic.draw(line(coords), axisStyle=True)
            else:
                pic.draw(line(coords), columnStyle=True)

            if 0 < i and i < n:
                pic.draw(
                    coords[0], node(f"{i}", below="2pt", anchor="north", font="\\small")
                )

        for j, coords in enumerate(columns):
            if j == 0:
                pic.draw(line(coords), axisStyle=True)
            else:
                pic.draw(line(coords), rowStyle=True)

            if 0 < j and j < n:
                pic.draw(
                    coords[0], node(f"{j}", left="2pt", anchor="north", font="\\small")
                )

        pic.draw((0, 0), node("0", anchor="north"))
        pic.draw((n * step, 0), node("$\\mathbb{N}$", anchor="south west"))
        pic.draw((0, n * step), node("$\\mathbb{N}$", anchor="south east"))

        for x, y in self.points:
            pic.draw((x * step, y * step), node("", selectedNode=True))

    def __iter__(self):
        """List the animation frames"""
        yield (
            0,
            NSquareWqo(grid_size=self.grid_size, grid_step=self.grid_step, points=[]),
        )

        for i in range(len(self.points)):
            yield (
                1,
                NSquareWqo(
                    grid_size=self.grid_size,
                    grid_step=self.grid_step,
                    points=self.points[: i + 1],
                ),
            )


@dataclasses.dataclass
class WqoUtilite:
    def draw(self, pic):

        pic.style("txt", text_width="4cm", anchor="north west", align="left")
        pic.style("titl", txt=True, font="\\scshape\\bfseries")

        pic.node(r"Vérification", titl=True, at=(0, -3.3))
        pic.node(
            r"\textcolor{A4}{Systèmes de transition bien structurés (WSTS)}",
            txt=True,
            text_width="8cm",
            at=(0, -4),
        )

        pic.node(
            r"$(\mathbb{N}^k, \to, \leq)$ $\rightsquigarrow$ réseau de Pétri",
            txt=True,
            text_width="8cm",
            at=(0, -4.5),
        )
        pic.node(r"\includegraphics[width=2cm]{./images/science/petri_net.png}",
                 at=(3,-6),
                 )

        pic.node(r"Graphes", titl=True, at=(0, -0.3))
        pic.node(r"\bsc{Robertson} \& \bsc{Seymour}", txt=True, at=(0, -1))
        pic.node(r"Mineurs de graphes", txt=True, at=(0, -1.5))
        pic.node(r"\includegraphics[width=2cm]{./images/science/graph_minor.png}",
                 at=(2,1),
                 anchor="center")

        pic.node(r"Algèbre", titl=True, at=(5, -0.3))
        pic.node(r"\bsc{Hilbert} / \bsc{Gröbner}", txt=True, at=(5, -1))
        pic.node(r"Calcul symbolique", txt=True, at=(5, -1.5))
        pic.node(r"\includegraphics[height=2cm]{./images/science/cox_little_shea.jpg}",
                 at=(5,1),
                 anchor="center")

    def __iter__(self):
        yield (0, WqoUtilite())


@dataclasses.dataclass
class WQOWorks:
    nsquare: NSquareWqo
    utilite: WqoUtilite
    show_publis: bool = True
    show_util: bool = True

    def draw(self, pic):
        if self.show_util:
            nscope = pic.scope(yshift="-2cm", scale="0.4", xshift="-11cm")
        else:
            nscope = pic.scope(yshift="-2cm", scale="0.4")

        self.nsquare.draw(nscope)

        if self.show_util:
            uscope = pic.scope(yshift="2.7cm", xshift="0cm")
            self.utilite.draw(uscope)

        if self.show_publis:
            pic.node(
                r"""
                    \textbf{Contributions}~: 3 axes
                    \newline
                    $\rightsquigarrow$ Nouveaux beaux préordres
                    \hfill
                    [FoSSaCS'23]
                    \newline
                    $\rightsquigarrow$ Complexité des préordres
                    \hfill
                    [MSCS]
                    \newline
                    $\rightsquigarrow$ Approche topologique
                    \hfill
                    [Coll. Mat.] 
                    \newline
                    \newline
                    \textbf{Collaborations}~:
                    \newline
                    IRIF (Schmitz),
                    LMF  (Goubault-Larrecq, Vialard, Schnoebelen),
                    LIS  (Lhote),
                    MPI-SWS (Schütze),
                    \textbf{LaBRI} (Ghosh).
                     """,
                at=(0, 0),
                rounded_corners="2mm",
                text_width="8cm",
                thick=True,
                fill="white",
                draw="A5",
                inner_sep="1em",
            )

    def __iter__(self):
        for d, nsq in self.nsquare:
            yield (
                d,
                WQOWorks(
                    nsquare=nsq,
                    utilite=self.utilite,
                    show_util=False,
                    show_publis=False,
                ),
            )
        yield (
            1,
            WQOWorks(
                nsquare=self.nsquare,
                utilite=self.utilite,
                show_util=True,
                show_publis=False,
            ),
        )
        yield (
            1,
            WQOWorks(
                nsquare=self.nsquare,
                utilite=self.utilite,
                show_util=True,
                show_publis=True,
            ),
        )


@dataclasses.dataclass
class AutomateOdd:
    def draw(self, autosc):
        autosc.node(r"$q_0$", name="q0", at=(-1, 0), state=True, initial=True)

        autosc.node(r"$q_1$", name="q1", at=(1, 0), state=True, accepting=True)

        autosc.draw("(q0)", topath("(q1)", bend_right="30"), opt="->")

        autosc.draw("(q1)", topath("(q0)", bend_right="30"), opt="->")

        autosc.node("a", at=(0, -0.6))
        autosc.node("a", at=(0, 0.6))

    def __iter__(self):
        yield (0, AutomateOdd())


@dataclasses.dataclass
class MSOOddEven:
    def draw(self, formsc):
        formsc.node(
            r"""$\exists X_{\text{odd}}, Y_{\text{even}},$""",
            anchor="north west",
            font="\\small",
            at=(0, 0),
        )

        formsc.node(
            r"""$\quad \text{AllPositions} = X_{\text{odd}} \uplus Y_{\text{even}}$""",
            anchor="north west",
            font="\\small",
            at=(1, -0.5),
        )

        formsc.node(
            r"""$\land\, \forall x,y, \, (x \in X_{\text{odd}} \land x+1=y)  \implies y \in Y_{\text{even}}$""",
            anchor="north west",
            font="\\small",
            at=(1, -1),
        )

        formsc.node(
            r"""$\land\, \forall x,y, \, (x \in X_{\text{even}} \land x+1=y)  \implies y \in Y_{\text{odd}}$""",
            anchor="north west",
            font="\\small",
            at=(1, -1.5),
        )

    def __iter__(self):
        yield (0, MSOOddEven())


@dataclasses.dataclass
class AutomatesTransducteurs:

    automa: bool = True
    verif: bool = True
    publis: bool = True

    def draw(self, pic):
        pic.style("txt", text_width="3.5cm", anchor="north west", align="left")
        pic.style("titl", txt=True, font="\\scshape\\bfseries")
        pic.style(
            "cat",
            text_width="2cm",
            minimum_height="2cm",
            align="center",
            draw=True,
            rounded_corners="2mm",
            inner_sep="1em",
        )

        visionsc = pic.scope(
            xshift="-7cm",
            yshift="-1.3cm",
        )

        visionsc.node(r"Logique", cat=True, name="log", at=(0, 0))
        visionsc.node(r"Automates", cat=True, name="aut", at=(4, 0))
        visionsc.node(r"Monoïdes", name="mono", cat=True, at=(0, 3))
        visionsc.node(r"Expressions", name="expr", cat=True, at=(4, 3))

        visionsc.draw("(log)", topath("(aut)"), opt="<->")
        visionsc.draw("(log)", topath("(mono)"), opt="<->")
        visionsc.draw("(expr)", topath("(mono)"), opt="<->")
        visionsc.draw("(expr)", topath("(aut)"), opt="<->")

        visionsc.node("GNU Grep",
                      align="center",
                      rotate="20",
                      color="A4",
                      at=(2,1.5))
        visionsc.node(
            r"\textbf{Langages} $L \colon \Sigma^* \to \mathsf{Bool}$",
            txt=True,
            text_width="5cm",
            at=(0, -1.5),
        )

        if self.verif:
            verifscope = pic.scope(yshift="2.7cm", xshift="1cm")
            verifscope.node(r"Décidabilité", titl=True, at=(0, -3.3))
            verifscope.node(
                r"Équivalence~? $\mathsf{FO}$-définissabilité~? etc.",
                txt=True,
                text_width="7cm",
                at=(0, -4),
            )
            verifscope.node(r"$f = g$? $f = 0$? $\exists g \in \mathsf{FO}, f = g$? ...",
                            at=(3.5,-5.5),
                            color="A4")

            verifscope.node(r"Quantitatif", titl=True, at=(0, -0.3))
            verifscope.node(r"$f \colon \Sigma^* \to \mathbb{N}$", txt=True, at=(0, -1))
            verifscope.node(r"\emph{Automates pondérés}", txt=True, at=(0, -1.5))
            verifscope.node(r"$w \mapsto 2^{|w|} \times |w|_a$",
                            at=(1.5,0),
                            color="A4")


            verifscope.node(r"Qualitatif", titl=True, at=(5, -0.3))
            verifscope.node(r"$f \colon \Sigma^* \to \Gamma^*$", txt=True, at=(5, -1))
            verifscope.node(
                r"\emph{Fonctions (poly)régulières}", txt=True, at=(5, -1.5)
            )
            verifscope.node(r"$w \mapsto w \# w$",
                            at=(6.5,0),
                            color="A4")

        if self.automa:
            visionsc.node(
                drawing_to_node(AutomateOdd(), 2),
                at=(4, 0),
                fill="white",
                anchor="center",
            )
            visionsc.node(
                drawing_to_node(MSOOddEven(), 2),
                at=(0, 0),
                fill="white",
                anchor="center",
            )

            visionsc.node(
                r"$\mathbb{Z}/2\mathbb{Z}$",
                at=(0, 3),
                text_width="2cm",
                fill="white",
                align="center",
                anchor="center",
            )

            visionsc.node(
                r"$(aa)^*$",
                at=(4, 3),
                text_width="2cm",
                fill="white",
                align="center",
                anchor="center",
            )

        if self.publis:
            pic.node(
                r"""
                    \textbf{Contributions}~: 
                    \newline
                    $\rightsquigarrow$ Apériodicité 
                    \hfill
                    [LICS'23, STACS'25]
                    \newline
                    $\rightsquigarrow$ Model checking
                    \hfill
                    [CAV'25]
                    \newline
                    \newline
                    \textbf{Collaborations}~:
                    \newline
                    IRIF (Colcombet),
                    Varsovie  (Bojańczyk, Stefański),
                    LaBRI (Morvan).
                """,
                at=(0, 0.2),
                rounded_corners="2mm",
                thick=True,
                text_width="8cm",
                fill="white",
                draw="A5",
                inner_sep="1em",
            )

    def __iter__(self):
        yield (0, AutomatesTransducteurs(False, False, False))
        for i in range(1, 4):
            yield (1, AutomatesTransducteurs(i >= 1, i >= 2, i >= 3))


@dataclasses.dataclass
class Cycle:
    size: int
    radius: float | int

    verticesProps: List[dict] = dataclasses.field(default_factory=list)
    edgesProps: dict[Tuple[int, int], dict] = dataclasses.field(default_factory=dict)

    def draw(self, pic):
        for i in range(self.size):
            angle = 2 * math.pi * i / self.size
            x = self.radius * math.cos(angle)
            y = self.radius * math.sin(angle)
            prps = self.verticesProps[i] if i < len(self.verticesProps) else {}
            n = prps.get("name", f"v{i}")
            myProps = {
                "at": (x, y),
                "circle": True,
                "inner_sep": "2pt",
                "draw": True,
                "name": n,
            }
            pic.node("", **(prps | myProps))

        for i in range(self.size):
            pi = self.verticesProps[i] if i < len(self.verticesProps) else {}
            j = (i + 1) % self.size
            pj = self.verticesProps[j] if j < len(self.verticesProps) else {}
            ni = pi.get("name", f"v{i}")
            nj = pj.get("name", f"v{j}")
            pic.draw(f"({ni})", topath(f"({nj})"))

    def __iter__(self):
        yield (0, self)


@dataclasses.dataclass
class Path:
    length: int

    def draw(self, pic):
        start = -(self.length - 1) / 2
        for i in range(self.length):
            pic.node(
                "",
                at=(start + i, 0),
                circle=True,
                draw=True,
                inner_sep="2pt",
                name=f"v{i}",
            )

        for i in range(self.length - 1):
            pic.draw(f"(v{i})", topath(f"(v{i+1})"))

    def __iter__(self):
        yield (0, self)


@dataclasses.dataclass
class Clique:
    size: int
    radius: float | int

    def draw(self, pic):
        # place nodes in a circle
        for i in range(self.size):
            angle = 2 * math.pi * i / self.size
            x = self.radius * math.cos(angle)
            y = self.radius * math.sin(angle)
            pic.node(
                "", at=(x, y), circle=True, inner_sep="2pt", draw=True, name=f"v{i}"
            )

        # draw all edges
        for i in range(self.size):
            for j in range(i + 1, self.size):
                pic.draw(f"(v{i})", topath(f"(v{j})"))

    def __iter__(self):
        yield (0, self)


@dataclasses.dataclass
class LosTarskiExemple:
    formule: Optional[Literal["informal", "formal"]] = "formal"
    exemples: Optional[int] = None
    presForm: bool = True
    presText: bool = True

    def draw(self, pic):
        pic.node(r"Graphes", at=(-6, 3), font="\\scshape\\bfseries\\Large")

        if self.formule is not None:
            pic.node(
                r"$\varphi$ = «~contient un chemin \textbf{induit} de longueur $2$~»",
                at=(3.5, 3),
                font="\\Large",
                color="A3",
            )
        if self.formule == "formal":
            pic.node(
                r"$\exists x,y,z, E(x,y) \land E(y,z) \land \neg E(x,z)$",
                at=(3.4, 2.6),
                color="A3",
            )

        exs = [
            (Cycle(6, 1), "oui"),
            (Clique(5, 1), "non"),
            (Path(2), "non"),
            (Path(3), "oui"),
        ]

        for i, (ex, b) in enumerate(exs):
            if self.exemples is not None and i >= self.exemples:
                break
            sex = pic.scope(xshift=f"{-4 + i*3}cm", yshift="1cm")
            ex.draw(sex)
            col = "A5" if b == "oui" else "A2"
            pic.node(f"$\\models \\varphi$? {b}", at=(-4 + i * 3, -0.5), color=col)

        if self.presForm:
            pic.node(
                r"$G \subseteq_i H$",
                at=(-2, -2.5),
                color="C2",
                text_width="2cm",
                font="\\Large",
            )
            pic.node(r"$\land$", at=(-3.5, -3), font="\\Large")
            pic.node(
                r"$G \models \varphi$",
                at=(-2, -3.5),
                text_width="2cm",
                color="A5",
                font="\\Large",
            )
            pic.node(r"$\implies$", at=(0, -3), font="\\Large")
            pic.node(r"$H \models \varphi$", at=(2, -3), color="A5", font="\\Large")

        if self.presText:
            pic.node(
                r"\textcolor{A3}{$\varphi$} préservée par \textcolor{C2}{extensions}",
                font="\\itshape\\huge",
                at=(3, -4),
                rounded_corners="1mm",
                draw=True,
                thick=True,
            )

    def __iter__(self):
        yield (
            0,
            LosTarskiExemple(formule=None, exemples=0, presForm=False, presText=False),
        )
        yield (
            1,
            LosTarskiExemple(
                formule="informal", exemples=0, presForm=False, presText=False
            ),
        )
        yield (
            1,
            LosTarskiExemple(
                formule="formal", exemples=0, presForm=False, presText=False
            ),
        )
        yield (
            2,
            LosTarskiExemple(
                formule="formal", exemples=1, presForm=False, presText=False
            ),
        )
        yield (
            2,
            LosTarskiExemple(
                formule="formal", exemples=None, presForm=False, presText=False
            ),
        )
        yield (
            1,
            LosTarskiExemple(
                formule="formal", exemples=None, presForm=True, presText=False
            ),
        )
        yield (
            1,
            LosTarskiExemple(
                formule="formal", exemples=None, presForm=True, presText=True
            ),
        )


@dataclasses.dataclass
class LosTarskiThm:
    mainThrm: bool = True

    def draw(self, pic):

        if self.mainThrm:
            ltrsk = pic.scope(xshift="-5cm", yshift="3cm")

            ltrsk.draw((-4, 0.6), rectangle((4, -4)), rounded_corners="2mm")

            ltrsk.node(r"Théorème Łoś-Tarski", at=(0, 0), font=r"\Large\bfseries")

            ltrsk.node(
                r"$\varphi \in \mathsf{FO}$", at=(0, -1), font=r"\Large", color="A3"
            )

            ltrsk.node(
                r"\textcolor{A3}{$\varphi$} préservée par \textcolor{C2}{extensions}",
                at=(0, -2),
                font=r"\Large",
            )

            ltrsk.node(
                r"\textcolor{A3}{$\varphi$} équivalente à \textcolor{A4}{$\psi$ existentielle}",
                at=(0, -3),
                font=r"\Large",
            )

            ltrsk.node(r"$\implies$", rotate="90", font=r"\Large", at=(-3, -2.5))
            ltrsk.node(r"$\implies$", rotate="-90", font=r"\Large", at=(3, -2.5))
            ltrsk.node(r"Facile", rotate="90", at=(-3.5, -2.5))
            ltrsk.node(r"Difficile", rotate="-90", at=(3.5, -2.5))

    def __iter__(self):
        yield (0, LosTarskiThm(True))


@dataclasses.dataclass
class LosTarskiUtilite:
    def draw(self, pic):
        pic.style("txt", text_width="8cm", anchor="north west", align="left")
        pic.style("titl", txt=True, font="\\scshape\\bfseries")

        pic.node(r"Théorie des modèles finis", titl=True, at=(0, -3.3))
        pic.node(
            r"Statut des théorèmes dans le cas fini~?",
            txt=True,
            text_width="8cm",
            at=(0, -4),
        )
        pic.node(
            r"Décompositions structurelles", txt=True, text_width="8cm", at=(0, -4.5)
        )

        pic.node(r"Bases de données", titl=True, at=(0, -0.3))
        pic.node(
            r"Structures relationnelles $\rightsquigarrow$ bases de données",
            txt=True,
            at=(0, -1),
        )
        pic.node(
            r"Bases incomplètes $\rightsquigarrow$ \emph{préservation \textcolor{A2}{par homomorphisme}}",
            txt=True,
            at=(0, -1.5),
        )

        pic.node(r"\includegraphics[height=2cm]{./images/science/libkin_fmt.jpg}",
                 at=(5, 0.5))
        pic.node(r"\includegraphics[height=2cm]{./images/science/pom_nesetril_sparsity.jpg}",
                 at=(7, -4.5))

    def __iter__(self):
        yield (0, LosTarskiUtilite())


@dataclasses.dataclass
class ThmPreservations:
    exemple: LosTarskiExemple
    theorem: LosTarskiThm
    utilite: LosTarskiUtilite

    mode: Literal["Init", "Ex", "Th", "Ut", "Fin"] = "Fin"

    def draw(self, pic):
        match self.mode:
            case "Init":
                pass
            case "Ex":
                self.exemple.draw(pic)
            case "Th":
                ctn = drawing_to_node(self.exemple, 5)
                pic.node(ctn, at=(-5, -3), opacity=0.8)
                self.theorem.draw(pic)
            case "Ut":
                exdr = drawing_to_node(self.exemple, 5)
                ltdr = drawing_to_node(self.theorem, 5)
                pic.node(exdr, at=(-5, -3), opacity=0.6)
                pic.node(ltdr, at=(-5, 2), opacity=0.8)
                utscope = pic.scope(yshift="2.7cm")
                self.utilite.draw(utscope)
            case "Fin":
                exdr = drawing_to_node(self.exemple, 5)
                ltdr = drawing_to_node(self.theorem, 5)
                pic.node(exdr, at=(-5, -3), opacity=0.6)
                pic.node(ltdr, at=(-5, 2), opacity=0.6)
                utscope = pic.scope(yshift="2.7cm")
                self.utilite.draw(utscope)
                pic.node(
                    r"""
                    \textbf{Contributions}~: méthodes \emph{génériques}
                    \newline
                    $\rightsquigarrow$ Composition (topologie)
                    \hfill
                    [CSL'21]
                    \newline
                    $\rightsquigarrow$ Localité
                    \hfill
                    [LICS'22]
                    \newline
                    \newline
                    \textbf{Collaborations}~:
                    \newline
                    IRIF (Schmitz),
                    LMF  (Goubault-Larrecq).
                    """,
                    at=(0, 0),
                    rounded_corners="2mm",
                    text_width="8cm",
                    thick=True,
                    fill="white",
                    draw="A5",
                    inner_sep="1em",
                )

    def __iter__(self):
        yield (
            0,
            ThmPreservations(self.exemple, self.theorem, self.utilite, mode="Init"),
        )
        for d, ex in self.exemple:
            yield (d + 1, ThmPreservations(ex, self.theorem, self.utilite, mode="Ex"))

        for d, th in self.theorem:
            yield (d + 1, ThmPreservations(self.exemple, th, self.utilite, mode="Th"))

        yield (1, ThmPreservations(self.exemple, self.theorem, self.utilite, mode="Ut"))
        yield (
            1,
            ThmPreservations(self.exemple, self.theorem, self.utilite, mode="Fin"),
        )


@dataclasses.dataclass
class CheminsLosTarski:
    legend: bool = False
    explication: bool = False
    showValidity: bool = False

    def draw(self, pic):
        if self.legend:
            pic.node(r"Chemins", font=r"\scshape\bfseries\Large", at=(-5, -3.8))

        for i in range(5):
            c = Path(i + 1)
            sc = pic.scope(yshift=f"{-3 + i}cm", xshift="-5cm")
            c.draw(sc)

        for i in range(4):
            pic.node(
                r"$\subseteq_i$",
                color="C2",
                rotate="90",
                font=r"\large",
                at=(-5, -2.5 + i),
            )

        if self.legend:
            pic.node(r"\vdots", at=(-5, 2), font=r"\large")

        if self.explication:
            pic.node(
                r"\textcolor{A3}{$\varphi$} préservée par \textcolor{C2}{extensions}",
                at=(5, 1),
                font=r"\Large",
            )

            pic.node(r"$\implies$", rotate="-90", at=(5, 0), font=r"\large")

            pic.node(
                r"\textcolor{A3}{$\varphi$} $\equiv$ \textcolor{A4}{«~Au moins $x$ éléments~»}",
                at=(5, -1),
                font=r"\large",
            )
            pic.node(
                r"\textcolor{A3}{$\varphi$} $\equiv$ \textcolor{A4}{$\bot$}",
                at=(5, -3),
                font=r"\large",
            )
            pic.node(r"OU", at=(5, -2), font=r"\large")

        if self.showValidity:
            pic.node(
                r"\textcolor{A5}{OUI \cmark}",
                at=(-5, 0),
                fill="white",
                rotate="30",
                font="\\Huge",
            )

    def __iter__(self):
        yield (0, CheminsLosTarski(True, False, False))
        yield (1, CheminsLosTarski(True, True, False))
        yield (1, CheminsLosTarski(True, True, True))


@dataclasses.dataclass
class CyclesLosTarski:
    legend: bool = False
    explication: bool = False
    showValidity: bool = False

    def draw(self, pic):
        if self.legend:
            pic.node(r"Cycles", font=r"\scshape\bfseries\Large", at=(-5, -3.8))

        for i in range(3, 7):
            odd = i % 2 == 1
            iup = i if odd else i - 1
            c = Cycle(i, 0.5)
            xs = "-6cm" if odd else "-4cm"
            sc = pic.scope(yshift=f"{-5 + iup}cm", xshift=xs)
            c.draw(sc)

        if self.legend:
            pic.node(r"\vdots", at=(-5, 2), font=r"\large")

        if self.explication:
            pic.node(
                r"Toute formule est préservée par \textcolor{C2}{extensions}~!",
                at=(5, 1),
                font=r"\Large",
            )

            pic.node(r"mais...", at=(5, 0), font=r"\large")

            pic.node(
                r"Toute formule est équivalente à une formule \textcolor{A4}{existentielle}~!",
                at=(5, -1),
                font=r"\large",
            )

        if self.showValidity:
            pic.node(
                r"\textcolor{A5}{OUI \cmark}",
                at=(-5, 0),
                fill="white",
                rotate="30",
                font="\\Huge",
            )

    def __iter__(self):
        yield (0, CyclesLosTarski(True, False, False))
        yield (1, CyclesLosTarski(True, True, False))
        yield (1, CyclesLosTarski(True, True, True))


@dataclasses.dataclass
class CyclesUCheminsNotLosTarski:
    legend: bool = False
    explication: bool = False
    showValidity: bool = False

    def draw(self, pic):
        if self.legend:
            pic.node(
                r"Cycles $\cup$ Chemins", font=r"\scshape\bfseries\Large", at=(-5, -3.8)
            )
        for i in range(5):
            c = Path(i + 1)
            sc = pic.scope(yshift=f"{-3 + i}cm", xshift="-5cm")
            c.draw(sc)

        for i in range(4):
            pic.node(
                r"$\subseteq_i$",
                color="C2",
                rotate="90",
                font=r"\large",
                at=(-5, -2.5 + i),
            )

        for i in range(3, 7):
            c = Cycle(i, 0.5)
            xs = -12.5 + i * 1.5
            sc = pic.scope(yshift="3cm", xshift=f"{xs}cm")
            c.draw(sc)

        if self.legend:
            pic.node(r"$\vdots$", at=(-5, 2), font=r"\large")
            pic.node(r"$\cdots$", at=(-1.5, 3), font=r"\large")

        if self.explication:
            pic.node(
                r"«~$\forall x. \textrm{degré}(x) = 2$~» \newline est préservée par \textcolor{C2}{extensions}",
                at=(5, 2),
                text_width="6cm",
                font=r"\Large",
            )

            pic.node(r"et", at=(5, 0), font=r"\large")

            pic.node(
                r"ne peut pas être écrite comme une formule \textcolor{A4}{existentielle}~!",
                at=(5, -1),
                font=r"\large",
            )

        if self.showValidity:
            pic.node(
                r"\textcolor{A2}{NON \xmark}",
                at=(-5, 0),
                fill="white",
                rotate="30",
                font="\\Huge",
            )

    def __iter__(self):
        yield (0, CyclesUCheminsNotLosTarski(True, False, False))
        yield (1, CyclesUCheminsNotLosTarski(True, True, False))
        yield (1, CyclesUCheminsNotLosTarski(True, True, True))


@dataclasses.dataclass
class RelatLosTarski:
    def draw(self, pic):
        pic.draw((-4, 0.6), rectangle((4, -4)), rounded_corners="2mm")

        pic.node(
            r"Relativisation à une classe $\mathcal{C}$?",
            at=(0, 0),
            font=r"\Large\bfseries",
        )

        pic.node(r"$\varphi \in \mathsf{FO}$", at=(0, -1), font=r"\Large", color="A3")

        pic.node(
            r"\textcolor{A3}{$\varphi$} préservée par \textcolor{C2}{extensions} \textbf{sur $\mathcal{C}$}",
            at=(0, -2),
            font=r"\large",
        )

        pic.node(
            r"\textcolor{A3}{$\varphi$} équivalente à \textcolor{A4}{$\psi$ existentielle} \textbf{sur $\mathcal{C}$}",
            at=(0, -3),
            font=r"\large",
        )

        pic.node(r"$\implies$", rotate="90", font=r"\Large", at=(-3, -2.5))
        pic.node(r"$\implies$", rotate="-90", font=r"\Large", at=(3, -2.5))
        pic.node(r"Facile", rotate="90", at=(-3.5, -2.5))
        pic.node(r"Difficile", rotate="-90", at=(3.5, -2.5))

    def __iter__(self):
        yield (0, RelatLosTarski())


@dataclasses.dataclass
class LosTarskiFiniteClasses:
    cycles: CyclesLosTarski
    paths:  CheminsLosTarski
    puc:    CyclesUCheminsNotLosTarski


    min_relat: bool = False
    show_cls: bool = False
    show_thm: bool = False

    @staticmethod
    def default():
        return LosTarskiFiniteClasses(
                cycles=CyclesLosTarski(),
                paths =CheminsLosTarski(),
                puc   =CyclesUCheminsNotLosTarski(),
                )

    def draw(self, pic):

        pic.node(r"Exemple de question technique",
                 at=(0,5),
                 font=r"\Large\scshape")

        if self.min_relat:
            pic.node(drawing_to_node(RelatLosTarski(), 4), at=(5, 3), fill="white")
        else:
            RelatLosTarski().draw(pic)
            return

        pic.style(
            "cls",
            text_width="2cm",
            align="center",
            rounded_corners="2mm",
            thick=True,
            minimum_height="2.3cm",
            draw=True,
            inner_sep="1em",
        )

        pic.node(
            r"Cycles",
            name="cycles",
            color=("A1" if not self.show_cls else "A5"),
            cls=True,
            at=(-6, 2),
        )
        pic.node(
            r"Logique",
            opacity=(0 if not self.show_cls else 1),
            at=(-6, 3.4),
        )

        pic.node(
            r"Chemins",
            cls=True,
            color=("A1" if not self.show_cls else "A5"),
            name="paths",
            at=(-6, -2),
        )
        pic.node(
            r"Beau Préordre",
            opacity=(0 if not self.show_cls else 1),
            at=(-6, -3.4),
        )

        pic.node(
            r"Cycles et Chemins",
            name="puc",
            color=("A2" if self.show_cls else "A1"),
            cls=True,
            at=(-2, 0),
        )

        pic.node(
            r"$\mathrm{Degré}_{\leq 2}$",
            name="deg2",
            color=("A5" if self.show_cls else "A1"),
            cls=True,
            at=(2, 0),
        )

        pic.node(r"Graphes Finis", name="all", cls=True, color="A2", at=(6, 0))
        pic.node(
            r"[\bsc{Tait}'59]",
            at=(6, -1),
            text="A2",
            fill="white",
            draw="A2",
            rounded_corners="2mm",
            rotate="30",
        )

        # midway for paths and puc
        pic.node(r"$\subseteq$", at=(-4, 1), rotate="-30", font="\\Large")
        pic.node(r"$\subseteq$", at=(-4, -1), rotate="30", font="\\Large")
        pic.node(r"$\subseteq$", at=(0, 0), font="\\Large")
        pic.node(r"$\subseteq$", at=(4, 0), font="\\Large")

        PICT_WIDTH = 1.7
        if self.show_cls:
            cycd = drawing_to_node(self.cycles, PICT_WIDTH)
            pathd = drawing_to_node(self.paths, PICT_WIDTH)
            pucd = drawing_to_node(self.puc, PICT_WIDTH)
            pic.node(cycd, at=(-6, 2), fill="white")
            pic.node(pathd, at=(-6, -2), fill="white")
            pic.node(pucd, at=(-2, 0), fill="white")
            pic.node(
                r"""\textbf{Condition \underline{suffisante}}
                        \newline
                         Atserias, Dawar, Grohe (2008)~:%
                         \newline%
                         \vspace{1em}%
                         \emph{clos par $\subseteq_i$},
                         \emph{clos par $\uplus$},
                         \underline{\emph{degré borné}}""",
                at=(0, -3),
                text_width="8cm",
                font=r"\large",
            )

        if self.show_thm:
            pic.node(
                r"""\begin{minipage}{9cm}
                        \textbf{Théorème [Lopez, LICS'22]} \newline
                         Soit $\mathcal{C}$
                         \emph{close par $\subseteq_i$} et \emph{$\uplus$}.
                         Les propriétés suivantes sont \underline{équivalentes}~:
                         \begin{enumerate}
                         \item Łoś-Tarski relativise à $\mathcal{C}$
                         \item Łoś-Tarski relativise à 
                         $\mathrm{Loc}_{r,k}(\mathcal{C})$, pour tout $r,k \in \mathbb{N}$
                         \end{enumerate}
                         \end{minipage}
                      """,
                text_width="9cm",
                inner_sep="2mm",
                rounded_corners="2mm",
                draw="D4",
                thick=True,
                at=(0, 2),
                fill="D4hint",
            )



    def __iter__(self):
        yield (
            0,
            LosTarskiFiniteClasses(
                cycles=self.cycles,
                paths=self.paths,
                puc=self.puc,
            ),
        )

        yield (
            1,
            LosTarskiFiniteClasses(
                cycles=self.cycles,
                paths=self.paths,
                puc=self.puc,
                min_relat=True,
            ),
        )


        yield (
            1,
            LosTarskiFiniteClasses(
                cycles=self.cycles,
                paths=self.paths,
                puc=self.puc,
                min_relat=True,
                show_cls=True,
            ),
        )
        yield (
            1,
            LosTarskiFiniteClasses(
                cycles=self.cycles,
                paths=self.paths,
                puc=self.puc,
                min_relat=True,
                show_cls=True,
                show_thm=True,
            ),
        )


@dataclasses.dataclass
class LocalityPotatoes:
    negative: bool = False
    neighbrd: bool = True
    substruct: bool = True

    def draw(self, pic):
        xmarkopacity = 1 if self.negative and not self.substruct else 0
        structopacity = 1 if not self.substruct else 0
        neighbropacity = 1 if self.neighbrd else 0
        poscycleopacity = 1 - neighbropacity

        # draw an ellipse
        pic.draw(
            (0, 0),
            circle(x_radius="3", y_radius="1.5"),
            fill="D1hint",
            opacity=structopacity,
            thick=True,
        )

        # draw three circles inside the ellipse,
        # green
        greencycles = [(0.5, -0.5), (1.5, 0), (2.5, 0.2)]

        # barycenter of the green points
        (bx, by) = (
            sum(x for (x, _) in greencycles) / 3,
            sum(y for (_, y) in greencycles) / 3,
        )
        # ellipse around the green points
        pic.draw(
            (bx, by),
            circle(x_radius=1.4, y_radius=0.5, rotate="25"),
            fill="C5hint",
            opacity=neighbropacity,
            draw=True,
            thick=True,
        )
        for x, y in greencycles:
            pic.draw((x, y), circle(0.3), fill="C5hint", opacity=poscycleopacity)
            pic.draw((x, y), circle(0.05), fill="B5", draw=None)

        # red
        redcycles = [(0, 0), (-2, 0.5), (-1, -0.7)]
        for x, y in redcycles:
            pic.draw((x, y), circle(0.3), opacity=structopacity, fill="B2hint")
            pic.draw((x, y), circle(0.05), opacity=structopacity, fill="A2", draw=None)
            pic.node(
                r"\xmark", at=(x, y), opacity=xmarkopacity, font="\\Huge", color="A5"
            )

    def __iter__(self):
        yield (0, LocalityPotatoes(False, False, False))
        for i in range(1, 4):
            yield (i, LocalityPotatoes(i >= 1, i >= 2, i >= 3))


@dataclasses.dataclass
class LocalisationCycles:
    cycles: bool = True
    centers: bool = True
    balls: bool = True
    neighbs: bool = True
    title: bool = True

    def draw(self, pic):
        if self.title:
            pic.node(
                r"$\mathrm{Loc}_{1,1}(\mathrm{Cycles}) = \{ C_3, P_3 \}$", at=(0, -0.5)
            )

        if self.centers:
            selected = {"color": "A4", "fill": True}
        else:
            selected = {}

        if self.neighbs:
            neighb = {"color": "C4", "fill": True}
        else:
            neighb = {}

        if self.cycles:
            c3 = Cycle(
                3,
                0.5,
                verticesProps=[
                    {"name": "v0"} | selected,
                    {"name": "v1"} | neighb,
                    {"name": "v2"} | neighb,
                ],
            )

            c6 = Cycle(
                6,
                0.5,
                verticesProps=[
                    {"name": "w0"} | neighb,
                    {"name": "w1"} | selected,
                    {"name": "w2"} | neighb,
                    {"name": "w3"},
                    {"name": "w4"},
                    {"name": "w5"},
                ],
            )

            s3 = pic.scope(xshift="-1.5cm", yshift="-2cm")
            s6 = pic.scope(xshift="1.5cm", yshift="-2cm")
            c3.draw(s3)
            c6.draw(s6)

            if self.balls:
                s3.draw("(v0)", circle(0.85), thick=True)
                s6.draw("(w1)", circle(0.5), thick=True)

    def __iter__(self):
        yield (0, LocalisationCycles(True, False, False, False, False))
        for i in range(1, 5):
            yield (1, LocalisationCycles(i >= 0, i >= 1, i >= 2, i >= 3, i >= 4))


@dataclasses.dataclass
class LocalToGlobalThm:
    locCycles: LocalisationCycles
    showNewCls: bool = False

    def draw(self, pic):
        pic.node(
            r"""\begin{minipage}{9cm}
                    \textbf{Théorème [Lopez, LICS'22]} \newline
                     Soit $\mathcal{C}$
                     \emph{close par $\subseteq_i$} et \emph{$\uplus$}.
                     Les propriétés suivantes sont \underline{équivalentes}~:
                     \begin{enumerate}
                     \item Łoś-Tarski relativise à $\mathcal{C}$
                     \item Łoś-Tarski relativise à 
                     $\mathrm{Loc}_{r,k}(\mathcal{C})$, pour tout $r,k \in \mathbb{N}$
                     \end{enumerate}
                     \end{minipage}
                  """,
            text_width="9cm",
            at=(0, 2),
            fill="D4hint",
        )

        sc = pic.scope(yshift="0.5cm")
        self.locCycles.draw(sc)

        if self.showNewCls:
            pic.node(
                r"""\textbf{Nouvelles classes~:} «~\emph{localement} $X$~» \newline%
                    $\rightsquigarrow$ \emph{localement fini} $\iff$ degré borné
                     """,
                at=(0, -3.5),
                text_width="6cm",
            )

    def __iter__(self):
        yield (
            0,
            LocalToGlobalThm(
                LocalisationCycles(False, False, False, False, False), False
            ),
        )
        for d, lc in self.locCycles:
            yield (d + 1, LocalToGlobalThm(lc, False))


@dataclasses.dataclass
class LocalToGlobalMethod:
    potatoes: LocalityPotatoes
    localite: bool = True
    combi1: bool = True
    combi2: bool = True
    conclusion: bool = True

    def draw(self, pic):

        pic.node(
            r"\textbf{Ré-écriture des formules}",
            at=(0, 3.2),
            font="\\bfseries\\scshape",
            anchor="center",
        )

        if self.localite:
            pic.node(r"$\varphi$", anchor="west", at=(-4, 2.5))
            pic.node(r"$\rightsquigarrow$", anchor="west", at=(-3, 2.5))
            pic.node(
                r"""
                    $\bigvee \bigwedge \, \textcolor{A2}{(\neg)}
                    \,
                    \textcolor{C3}{\exists_r^{\geq k} x.}
                    \textcolor{A5}{\psi_{|\mathcal{N}(x, r)}}(x)$""",
                anchor="west",
                at=(-2, 2.5),
            )
            pic.node(r"Localité", at=(3, 2.5), anchor="west", text="C1", fill="white")

        if self.combi1:
            pic.node(r"$\rightsquigarrow$", anchor="west", at=(-3, 1.7))
            pic.node(
                r"""
                    $\bigvee \bigwedge \, \textcolor{A2}{~~~~~~}
                    \,
                    \textcolor{C3}{\exists_r^{\geq k} x.}
                    \textcolor{A5}{\psi_{|\mathcal{N}(x, r)}}(x)$""",
                anchor="west",
                at=(-2, 1.7),
            )
            pic.node(
                r"($\subseteq_i$)", at=(3, 1.7), text="C1", anchor="west", fill="white"
            )

        if self.combi2:
            pic.node(r"$\rightsquigarrow$", anchor="west", at=(-3, 1))
            pic.node(
                r"""
                    $\exists \vec{x}. \,
                                \textcolor{A5}{\theta_{|\mathcal{N}(\vec{x}, r)}(\vec{x})}$
                     """,
                anchor="west",
                at=(-2, 1),
            )
            pic.node(r"Voisinages", at=(3, 1), text="C1", anchor="west", fill="white")

        if self.conclusion:
            pic.node(r"$\rightsquigarrow$", anchor="west", at=(-3, 0.2))
            pic.node(
                r"""
                    $\exists \vec{x}. \,
                     \exists \vec{y}. \,
                     \gamma(\vec{x}, \vec{y})$
                     """,
                anchor="west",
                at=(-2, 0.2),
            )
            pic.node(
                r"$\mathrm{Loc}_{r,|\vec{x}|}(\mathcal{C})$",
                at=(3, 0.2),
                text="C1",
                anchor="west",
                fill="white",
            )

        scope = pic.scope(yshift="-2.5cm")
        self.potatoes.draw(scope)

    def __iter__(self):
        for (d, pot), i in zip(self.potatoes, range(4)):
            yield (d, LocalToGlobalMethod(pot, i >= 0, i >= 1, i >= 2, i >= 3))


@dataclasses.dataclass
class DevTechnique:

    filAriane: FilAriane
    methode: LocalToGlobalMethod
    theorem: LocalToGlobalThm

    mode: Literal["Init", "Thm", "Meth"] = "Meth"


    def draw(self, pic):
        arsc = pic.scope(yshift="5.15cm")
        self.filAriane.draw(arsc)

        thmscope = pic.scope(xshift="-5cm")
        metsocpe = pic.scope(xshift="5cm")

        match self.mode:
            case "Init":
                pass
            case "Thm":
                self.theorem.draw(thmscope)
            case "Meth":
                self.theorem.draw(thmscope)
                thmscope.node(
                    r"$\implies$",
                    at=(-4.2, 1.3),
                    rotate="90",
                    text="A3",
                    font="\\small",
                )
                self.methode.draw(metsocpe)

    def __iter__(self):
        yield (0, DevTechnique(self.filAriane, self.methode, self.theorem, "Init"))
        for d, th in self.theorem:
            yield (d + 1, DevTechnique(self.filAriane, self.methode, th, "Thm"))
        for d, me in self.methode:
            yield (d + 1, DevTechnique(self.filAriane, me, self.theorem, "Meth"))

        thm = LocalToGlobalThm(LocalisationCycles(), True)
        yield (1, DevTechnique(self.filAriane, self.methode, thm, "Meth"))


@dataclasses.dataclass
class Research:
    ariane: FilAriane
    automates: AutomatesTransducteurs
    wqos: WQOWorks
    logique: ThmPreservations

    @staticmethod
    def default():
        return Research(
            ariane=FilAriane(
                header="Thèmes de recherche",
                width=8,
                current=None,
                titles=["Ordres", "Automates", "Logique"],
            ),
            automates=AutomatesTransducteurs(),
            wqos=WQOWorks(
                nsquare=NSquareWqo(
                    points=[(7,3), (5,6), (0,8), (8,0)],
                    grid_size=10,
                ),
                utilite=WqoUtilite(),
            ),
            logique=ThmPreservations(
                exemple=LosTarskiExemple(),
                theorem=LosTarskiThm(),
                utilite=LosTarskiUtilite(),
            ),
        )

    def draw(self, pic):
        if self.ariane.current is None:
            ThemesAndLocations().draw(pic)
        else:
            arsc = pic.scope(yshift="5.15cm")
            self.ariane.draw(arsc)

        if self.ariane.current == 1:
            self.automates.draw(pic)
        elif self.ariane.current == 0:
            self.wqos.draw(pic)
        elif self.ariane.current == 2:
            self.logique.draw(pic)

    def __iter__(self):
        yield (0, self)

        for d, wq in self.wqos:
            ar = FilAriane(
                header=self.ariane.header,
                width=self.ariane.width,
                current=0,
                titles=self.ariane.titles,
            )
            yield (
                d + 1,
                Research(
                    ariane=ar,
                    automates=self.automates,
                    wqos=wq,
                    logique=self.logique,
                ),
            )
        for d, at in self.automates:
            ar = FilAriane(
                header=self.ariane.header,
                width=self.ariane.width,
                current=1,
                titles=self.ariane.titles,
            )
            yield (
                d + 1,
                Research(
                    ariane=ar,
                    automates=at,
                    wqos=self.wqos,
                    logique=self.logique,
                ),
            )

        for d, lo in self.logique:
            ar = FilAriane(
                header=self.ariane.header,
                width=self.ariane.width,
                current=2,
                titles=self.ariane.titles,
            )
            yield (
                d + 1,
                Research(
                    ariane=ar,
                    automates=self.automates,
                    wqos=self.wqos,
                    logique=lo,
                ),
            )


@dataclasses.dataclass
class PipelineIngestion:
    mode: Literal["Init", "Pipeline", "Interaction", "Verif"] = "Verif"

    def draw(self, pic):

        pic.node(
            r"\includegraphics[width=19cm]{./images/science/flamanville.jpg}",
            at=(0, 0),
            opacity=(0.1 if self.mode != "Init" else 1),
            anchor="center",
        )

        pic.node(
            r"Un \underline{exemple} de programme utilisant des données",
            at=(0, 4.5),
            font="\\Large\\scshape",
            anchor="center",
        )

        if self.mode != "Init":
            pic.node(
                r"Amont~: Pipeline d’Ingestion",
                font=r"\scshape\bfseries\large",
                at=(-5, 3.5),
            )

            pic.draw((0, 3.5), topath((0, -3.5)), dashed=True, thick=True, color="A1")

            pic.node(
                r"\includegraphics[width=1.5cm]{./images/cliparts/centrales-map.pdf}",
                at=(-7, 2),
                draw=True,
                thick=True,
                fill="white",
                name="centrales",
                rounded_corners="2mm",
                anchor="center",
            )

            pic.node(
                r"\includegraphics[width=1.5cm]{./images/cliparts/rss-svgrepo-com.png}",
                at=(-7, 0),
                draw=True,
                name="rss",
                thick=True,
                fill="white",
                rounded_corners="2mm",
                anchor="center",
            )

            pic.node(
                r"\includegraphics[width=1.5cm]{./images/cliparts/database-svgrepo-com.png}",
                at=(-7, -2),
                draw=True,
                name="innerdb",
                thick=True,
                fill="white",
                rounded_corners="2mm",
                anchor="center",
            )

            pic.node(
                r"\includegraphics[width=1.5cm]{./images/cliparts/database-svgrepo-com copy.png}",
                at=(0, 0),
                name="db",
                draw=True,
                thick=True,
                fill="white",
                rounded_corners="2mm",
                anchor="center",
            )

            pic.draw(
                "(centrales)", topath("(db)", _out="0", _in="180"), opt="->", thick=True
            )
            pic.draw(
                "(innerdb)", topath("(db)", _out="0", _in="180"), opt="->", thick=True
            )
            pic.draw("(rss)", topath("(db)", _out="0", _in="180"), opt="->", thick=True)

        if self.mode != "Init" and self.mode != "Pipeline":
            pic.node(
                r"Aval~: Interaction via une API",
                font=r"\scshape\bfseries\large",
                at=(5, 3.5),
            )

            pic.node(
                r"\includegraphics[width=1.5cm]{./images/cliparts/task-list-svgrepo-com.png}",
                at=(7, 2),
                draw=True,
                name="annot",
                thick=True,
                fill="white",
                rounded_corners="2mm",
                anchor="center",
            )

            pic.node(
                r"\includegraphics[width=1.5cm]{./images/cliparts/admin-with-cogwheels-svgrepo-com.png}",
                at=(7, -2),
                name="admin",
                draw=True,
                thick=True,
                fill="white",
                rounded_corners="2mm",
                anchor="center",
            )

            pic.draw(
                "(db)", topath("(annot)", _in="180", _out="0"), opt="<->", thick=True
            )
            pic.draw(
                "(db)", topath("(admin)", _in="180", _out="0"), opt="<->", thick=True
            )

        if self.mode == "Verif":
            pic.node(
                r"Vérification~: $\{ \varphi \} \, P \, \{ \psi \}$~? (Hoare)",
                at=(-5, -4),
                color="A2",
                font=r"\large",
            )

            pic.node(
                r"Vérification~: $D_0 \to^* D_\text{err}$~? (Accessibilité)",
                at=(5, -4),
                color="A2",
                font=r"\large",
            )

    def __iter__(self):
        yield (0, PipelineIngestion(mode="Init"))
        for m in ["Pipeline", "Interaction", "Verif"]:
            yield (1, PipelineIngestion(mode=m))


@dataclasses.dataclass
class PolyregPonderes:
    quant: bool = False
    exp: bool = False

    def draw(self, pic):

        pic.style(
            "guessed",
            text="C1",
        )
        pic.style(
            "decidable",
            draw="B5",
            thick=True,
            double=True,
        )
        pic.style(
            "important",
            draw="A2",
            thick=True,
        )

        if self.quant:
            pic.node(r"$\mathbb{N}\mathsf{FOPoly}$", name="nsf", at=(0, 0, 0))

            pic.node(r"$\mathbb{N}\mathsf{Poly}$", name="npo", at=(0, 3, 0))

        pic.node(r"$\mathsf{FOPoly}$", name="sf", font="\\bfseries", at=(3, 0, 0))

        pic.node(r"$\mathsf{Poly}$", name="poly", font="\\bfseries", at=(3, 3, 0))

        if self.exp:
            pic.node(r"$\mathbb{N}\mathsf{Exp}$", name="nexp", at=(0, 3, -3))
            pic.node(
                r"$\mathbb{N}\mathsf{FOExp}$",
                name="nfoexp",
                guessed=True,
                at=(0, 0, -3),
            )

            pic.node(r"$\mathsf{FOExp}$", name="foexp", guessed=True, at=(3, 0, -3))

            pic.node(r"$\mathsf{Exp}$", name="exp", guessed=True, at=(3, 3, -3))

            pic.draw("(poly)", topath("(exp)"), dashed=True, opt="->")
            pic.draw("(nfoexp)", topath("(foexp)"), dashed=True, opt="->")
            pic.draw("(nsf)", topath("(nfoexp)"), dashed=True, opt="->")
            pic.draw("(sf)", topath("(foexp)"), dashed=True, opt="->")
            pic.draw("(foexp)", topath("(exp)"), dashed=True, opt="->")
            pic.draw("(nfoexp)", topath("(nexp)"), dashed=True, opt="->")
            pic.draw("(nexp)", topath("(exp)"), dashed=True, opt="->")
            pic.draw("(npo)", topath("(nexp)"), decidable=True, opt="->")

        if self.quant:
            pic.draw("(nsf)", topath("(npo)"), dashed=True, opt="->")
            pic.draw("(npo)", topath("(poly)"), decidable=True, opt="->")
            pic.draw("(nsf)", topath("(sf)"), decidable=True, opt="->")

        pic.draw("(sf)", topath("(poly)"), important=True, opt="->")

    def __iter__(self):
        yield (0, PolyregPonderes())


@dataclasses.dataclass
class ProjetPipeline:

    showProg: bool = False
    showProb: bool = True
    showUnaire: bool = True
    showExp: bool = True
    showImplem: bool = True
    showPolycheck: bool = True

    def draw(self, pic):
        pic.style(
            "lbl", anchor="north west", text_width="8cm", align="left", font="\\large"
        )

        pic.node(
            r"\includegraphics[width=8cm]{./images/cliparts/simple-for-programs.png}",
            at=(-5, -0.8),
            opacity=(1 if self.showProg else 0.2),
            anchor="center",
        )

        pic.node(
            r"\textbf{Objet~:} programmes Python «~simples~» \strut",
            at=(-9, 4),
            lbl=True,
        )

        pic.node(
            r"\textbf{Point de départ~:} \emph{fonctions polyrégulières}\strut",
            at=(-9, 3.5),
            lbl=True,
        )

        if self.showProb:
            pic.node(
                r"Problèmes théoriques à long terme",
                at=(-9, 2.5),
                color="A2",
                anchor="north west",
                font=r"\large\bfseries\scshape",
            )

            pic.node(
                r"Décider l’équivalence de fonctions",
                at=(-9, 2),
                color="A2",
                font=r"\large",
                anchor="north west",
            )
            pic.node(
                r"Décider la $\mathsf{FO}$-définissabilité",
                at=(-9, 1.5),
                font=r"\large",
                color="A2",
                anchor="north west",
            )

        if self.showUnaire:
            pic.node(
                r"""\textbf{Dans un premier temps} \newline%
                        $\rightsquigarrow$ sorties unaires $\{a\}^* \simeq \mathbb{N}$
                        \newline%
                        $\rightsquigarrow$ entrées unaires / commutatives~?
                        \newline%
                        $\rightsquigarrow$ lien quantitatif / qualitatif~?
                     """,
                at=(-9, 0.7),
                font=r"\large",
                text_width="8cm",
                anchor="north west",
            )

        if self.showProb:
            diagram = pic.scope(xshift="3cm", yshift="-0.5cm")
            PolyregPonderes(self.showUnaire, self.showExp).draw(diagram)

        if self.showImplem:
            pic.node(
                r"""Implémentation(s)""",
                at=(-9, -1.7),
                anchor="north west",
                font="\\large\\bfseries\\scshape",
                text="A1",
            )
            pic.node(
                r"""

                     $\rightsquigarrow$ Vérification de triplets de Hoare~?
                     \newline%
                     $\rightsquigarrow$ Optimisations de programmes~?
                     """,
                at=(-9, -2.3),
                anchor="north west",
                font="\\large",
                text_width="8cm",
                text="A1",
            )

        if self.showPolycheck:
            pic.node(
                r"\includegraphics[width=7cm]{./images/cliparts/polycheck.png}",
                at=(5, -2.5),
                anchor="center",
            )
            pic.node(
                r"[\textbf{Lopez}, \bsc{Stefański}, CAV'25]",
                at=(5, -2.5),
                fill="white",
                draw="A5",
                rounded_corners="2mm",
                anchor="center",
            )

    def __iter__(self):
        yield (0, ProjetPipeline(True, False, False, False, False, False))
        for i in range(1, 6):
            yield (1, ProjetPipeline(False, i >= 1, i >= 2, i >= 3, i >= 4, i >= 5))


@dataclasses.dataclass
class ProjetSystTrans:

    showPartiPris: bool = True
    showProb: bool = True
    showWqo: bool = True
    showConj: bool = True
    showRepr: bool = True
    showFutur: bool = True
    showBDD: bool = True

    def draw(self, pic):

        pic.style(
            "lbl", anchor="north west", text_width="8cm", align="left", font="\\large"
        )

        pic.node(
            r"""\textbf{Cadre~:} 
                 classes de structures relationnelles finies $\mathcal{C}$
                 avec une relation de transtion $\to$\strut
                 """,
            at=(-9, 4),
            lbl=True,
        )
        if self.showPartiPris:
            pic.node(
                r"""\textbf{Parti pris~:}
                     $(\mathcal{C}, \to, \subseteq_i)$
                     \newline%
                     \emph{Système de transition bien structuré}
                     \strut""",
                at=(9, 4),
                lbl=True,
                anchor="north east",
            )

            diagshape = pic.scope(xshift="1.1cm", yshift="1cm", scale=1.5)

            diagshape.node(r"$\mathfrak{A}$", name="A", at=(0, 0))
            diagshape.node(r"$\mathfrak{B}$", name="B", at=(1, 0))
            diagshape.node(r"$\mathfrak{A}'$", name="Ap", at=(0, 1))
            diagshape.node(r"$\mathfrak{B}'$", name="Bp", at=(1, 1))

            diagshape.draw("(A)", topath("(B)"), opt="->")
            diagshape.draw("(Ap)", topath("(Bp)"), opt="->", dashed=True)
            diagshape.node(r"$\subseteq_i$", at=(0, 0.5), rotate="90")
            diagshape.node(r"$\subseteq_i$", at=(1, 0.5), rotate="90")

            pic.node(
                r"""Couvrabilité~:
                     \newline%
                     $D_0 \to^* D' {}_i\!\!\supseteq D_{\text{err}}$ décidable
                     """,
                at=(9, 2.7),
                anchor="north east",
                fill="white",
                draw="A5",
                rounded_corners="2mm",
                text_width="5cm",
            )

            pic.node(
                r"""(Sous hypothèses de \emph{calculabilité})""",
                at=(9, 1.8),
                anchor="north east",
                text_width="5cm",
            )

        if self.showProb:
            pic.node(
                r"Problème à long terme\strut",
                at=(-9, 2.7),
                color="A2",
                anchor="north west",
                font=r"\large\bfseries\scshape",
            )

            pic.node(
                r"""\textbf{Reconnaître} les systèmes $(\mathcal{C}, \to, \subseteq_i)$ qui sont
                     bien structurés""",
                at=(-9, 2.2),
                color="A2",
                anchor="north west",
            )

        if self.showWqo:
            pic.node(
                r"""\textbf{Dans un premier temps, ignorer $\to$} \newline%
                     $\rightsquigarrow$ $(\mathcal{C}, \subseteq_i)$
                     est un \emph{beau préordre}~?""",
                text_width="7cm",
                at=(-9, 1.5),
                anchor="north west",
            )

        if self.showConj:
            pic.node(
                r"""\textbf{Conjecture [Daligault et al., 2010]~:} 
                         \newline%
                         $(\mathcal{C}, \subseteq_i)$
                         \emph{beau préordre}
                         \newline%
                         $\implies$
                         \newline%
                         $\mathcal{C}$ a \emph{largeur de clique bornée} ($\mathsf{MSO}$)""",
                at=(-9, 0.4),
                text_width="7cm",
                fill="D4hint",
                anchor="north west",
            )

        if self.showRepr:
            pic.node(
                r"""\textbf{Différentes représentations}
                            \newline%
                            $\rightsquigarrow$ $(\Sigma^*, \leq_{\text{facteur}})$
                            représente les classes $(\mathcal{C}, \subseteq_i)$
                            \newline%
                            $\rightsquigarrow$
                            Classe de largeur de clique bornée
                         """,
                at=(-9, -1.6),
                text_width="7cm",
                anchor="north west",
            )

        if self.showFutur:
            pic.node(
                r"""\textbf{Et plus tard}~?
                            \newline%
                            $\rightsquigarrow$ \emph{homomorphismes}~?
                            \newline%
                            $\rightsquigarrow$
                            relations $\to$~?
                         """,
                at=(-9, -3.2),
                text_width="7cm",
                anchor="north west",
            )

        if self.showBDD:
            pic.node(
                r"""Une ouverture sur les bases de données""",
                at=(0.8, -1),
                anchor="north west",
                font="\\large\\bfseries\\scshape",
                text="A1",
            )

            pic.node(
                r"""Algorithmes de type \emph{Chase} \newline%
                     $D_0$ base de donnée,
                     $\Delta$ contraintes,
                     $q$ requête
                         \newline%
                     «~toute complétion de $D_0$ vérifiant $\Delta$ satisfait $q$~?»""",
                at=(0.8, -1.5),
                text_width="8cm",
                anchor="north west",
            )

            pic.node(
                r"""$(\mathcal{C}, \to_{\Delta}, \to_{\text{hom}})$ 
                     $\rightsquigarrow$
                     $D_0 \to_{\Delta}^* D_{\text{err}} \models \Delta \wedge \neg q$~?""",
                at=(0.8, -3),
                text_width="7cm",
                anchor="north west",
            )

    def __iter__(self):
        yield (0, ProjetSystTrans(False, False, False, False, False, False, False))
        for i in range(1, 8):
            yield (
                1,
                ProjetSystTrans(i >= 1, i >= 2, i >= 3, i >= 4, i >= 5, i >= 6, i >= 7),
            )


@dataclasses.dataclass
class Project:
    pipeline: PipelineIngestion
    systtrans: ProjetSystTrans
    polyreg: ProjetPipeline
    ariane: FilAriane

    @staticmethod
    def default():
        return Project(
            pipeline=PipelineIngestion(),
            systtrans=ProjetSystTrans(),
            polyreg=ProjetPipeline(),
            ariane=FilAriane(
                header="Projet de recherche",
                width=12,
                current=None,
                titles=["Systèmes de transition", "Fonctions polyrégulières"],
            ),
        )

    def draw(self, pic):
        if self.ariane.current is not None:
            arsc = pic.scope(yshift="5.15cm")
            self.ariane.draw(arsc)

        if self.ariane.current is None:
            self.pipeline.draw(pic)
        elif self.ariane.current == 0:
            self.systtrans.draw(pic)
        elif self.ariane.current == 1:
            self.polyreg.draw(pic)

    def __iter__(self):
        for d, pipeline in self.pipeline:
            yield (
                d,
                Project(
                    pipeline=pipeline,
                    systtrans=self.systtrans,
                    polyreg=self.polyreg,
                    ariane=self.ariane,
                ),
            )
        for d, systtrans in self.systtrans:
            ar = FilAriane(
                header=self.ariane.header,
                width=self.ariane.width,
                current=0,
                titles=self.ariane.titles,
            )

            yield (
                1 + d,
                Project(
                    pipeline=self.pipeline,
                    systtrans=systtrans,
                    polyreg=self.polyreg,
                    ariane=ar,
                ),
            )

        for d, polyreg in self.polyreg:
            ar = FilAriane(
                header=self.ariane.header,
                width=self.ariane.width,
                current=1,
                titles=self.ariane.titles,
            )
            yield (
                1 + d,
                Project(
                    pipeline=self.pipeline,
                    systtrans=self.systtrans,
                    polyreg=polyreg,
                    ariane=ar,
                ),
            )


@dataclasses.dataclass
class IntegrationEquipe:
    def draw(self, pic):
        labo = "LaBRI"
        labo_img = "./images/institutions/labri.pdf"
        equipe = "M2F"
        equipe_long = "Modélisation et Méthodes Formelles"
        sous_equipe = "LX"
        sous_equipe_long = "Logical foundations of computing"
        themes = [
            "Automata Theory",
            "Formal Languages",
            "Logic in computing",
            "Algebraic techniques",
            "Graphs and logics",
            "Computability theory",
        ]

        pic.node(
            r"\includegraphics[width=5cm]{" + labo_img + r"}",
            at=(0, 1),
        )

        pic.node(
            equipe,
            at=(0, -1),
            font=r"\Huge\bfseries",
        )

        pic.node(equipe_long, at=(0, -1.5), font=r"\itshape\large")

        pic.node(
            sous_equipe,
            at=(0, -3),
            font=r"\Huge\bfseries",
        )
        pic.node(sous_equipe_long, at=(0, -3.5), font=r"\itshape\large")

        grid = [
            (-2, -4.5),
            (2, -4.5),
            (-2, -5.5),
            (2, -5.5),
            (-2, -6.5),
            (2, -6.5),
        ]

        for theme, pos in zip(themes, grid):
            pic.node(
                theme,
                at=pos,
            )

    def __iter__(self):
        yield (0, self)


@dataclasses.dataclass
class IntegrationBonus:
    def draw(self, pic):
        autre_equipe = "Autre équipe: \\textbf{RATIO}"
        divers = [
            {
                "name": "Arka Ghosh",
                "picture": "arka_ghosh.jpg",
            },
            {"name": "Rémi Morvan", "picture": "remi_morvan.jpg"},
        ]

        pic.draw(
            (-5, 2), rectangle((5, -4)), fill="white", rounded_corners="2mm", thick=True
        )

        pic.node(
            autre_equipe,
            at=(0, 1.5),
            font=r"\Large",
        )

        pic.node(
            "Reasoning with data, knowledge, and constraints",
            at=(0, 0.9),
            font=r"\itshape",
        )

        pic.node(
            "Collaborations existantes (non-permanents)", at=(0, 0), font=r"\Large"
        )

        for x, d in zip([-2, 2], divers):
            pic.node(
                r"\includegraphics[width=2cm]{./images/people/" + d["picture"] + "}",
                at=(x, -1.5),
            )
            pic.node(d["name"], at=(x, -3))

    def __iter__(self):
        yield (0, self)


@dataclasses.dataclass
class Trombinoscope:

    themes: List[str]

    @staticmethod
    def default():
        return Trombinoscope(themes=["AUT", "WA", "FO", "WQO", "FAMT"])

    def draw(self, pic):
        colors = {
            "WA": "A1",
            "WQO": "A2",
            "FO": "A3",
            "FAMT": "A4",
            "AUT": "A5",
        }

        tnames = {
            "WA": "Automates Pondérés",
            "WQO": "Beaux Préordres",
            "FO": "Apériodicité",
            "FAMT": "Modèles Finis",
            "AUT": "Automates",
        }

        people = [
            {
                "name": "Sylvain\\newline Lombardy",
                "picture": "sylvain_lombardy.png",
                "themes": ["WA"],
            },
            {
                "name": "Jérôme\\newline Leroux",
                "picture": "jerome_leroux.jpg",
                "themes": ["WQO"],
            },
            {
                "name": "Joanna\\newline Fijalkow",
                "picture": "joanna_fijalkow.jpg",
                "themes": ["FAMT"],
            },
            {
                "name": "Vincent\\newline Penelle",
                "picture": "vincent_penelle.jpg",
                "themes": ["WA"],
            },
            {
                "name": "Thomas\\newline Place",
                "picture": "thomas_place.jpg",
                "themes": ["FO"],
            },
            {
                "name": "Marc\\newline Zeitoun",
                "picture": "marc_zeitoun.jpg",
                "themes": ["FO"],
            },
            {
                "name": "Igor\\newline Walukiewicz",
                "picture": "igor_walukiewicz.jpg",
                "themes": ["AUT"],
            },
            {
                "name": "Nathanaël\\newline Fijalkow",
                "picture": "nathanael_fijalkow.jpg",
                "themes": ["AUT"],
            },
            {
                "name": "Hugo\\newline Gimbert",
                "picture": "hugo_gimbert.jpg",
                "themes": ["AUT"],
            },
        ]

        # create a grid to display the people
        # we need the positions of the center
        # of each image, in a grid with 3 columns
        grid = [
            (
                i // 3,
                i % 3,
            )
            for i in range(len(people))
        ]
        gscale = lambda p: (p[0] * 2.5 - 3, p[1] * 2.5 - 3)

        for i, theme in enumerate(self.themes):
            pic.node(
                tnames[theme],
                at=(5.5, -i),
                text_width="3cm",
                align="center",
                rounded_corners="1mm",
                draw=colors[theme],
                thick=True,
                fill=colors[theme] + "hint",
                font=r"\bfseries",
            )

        for people, pos in zip(people, grid):
            pos = gscale(pos)

            upleft = (pos[0] - 1.2, pos[1] + 0.8)
            dwrigt = (pos[0] + 1.3, pos[1] - 1.7)

            if people["themes"][0] in self.themes:
                pic.draw(
                    upleft,
                    rectangle(dwrigt),
                    draw=None,
                    fill=colors[people["themes"][0]] + "hint",
                )

            pic.node(
                r"\includegraphics[width=1.5cm,height=1.5cm,keepaspectratio]{./images/people/%s}"
                % people["picture"],
                at=pos,
                anchor="center",
                inner_sep=0,
                minimum_height="1.5cm",
                minimum_width="1.5cm",
            )

            pic.node(
                people["name"],
                at=(pos[0] + 0.3, pos[1] - 1.2),
                anchor="center",
                font="\\small\\scshape",
                text_width="2cm",
            )

    def __iter__(self):
        yield (0, Trombinoscope(themes=[]))
        for i in range(len(self.themes)):
            yield (1, Trombinoscope(themes=self.themes[: i + 1]))


@dataclasses.dataclass
class Integration:
    trombi: Optional[Trombinoscope] = None
    equipe: Optional[IntegrationEquipe] = None
    bonus: Optional[IntegrationBonus] = None

    @staticmethod
    def default():
        return Integration(
            trombi=Trombinoscope.default(),
            equipe=IntegrationEquipe(),
            bonus=IntegrationBonus(),
        )

    def draw(self, pic):
        trombsc = pic.scope(xshift="-5cm", yshift="1cm")
        eqsc = pic.scope(xshift="6cm", yshift="3cm")
        bnsc = pic.scope()

        if self.trombi is not None:
            self.trombi.draw(trombsc)

        if self.equipe:
            self.equipe.draw(eqsc)

        if self.bonus:
            self.bonus.draw(bnsc)

        pic.node(
            r"Intégration",
            at=(0, 4.5),
            font="\\bfseries\\Huge\\scshape",
            anchor="center",
        )

    def __iter__(self):
        yield (0, Integration())

        for d, e in self.equipe:
            yield (d + 1, Integration(trombi=None, equipe=e))

        for d, t in self.trombi:
            yield (d + 1, Integration(trombi=t, equipe=self.equipe))

        for d, b in self.bonus:
            yield (d + 1, Integration(trombi=self.trombi, equipe=self.equipe, bonus=b))


@dataclasses.dataclass
class Conclusion:
    def draw(self, pic):
        pic.node(
            r"\includegraphics[trim={0 0 0 3.7cm},clip,width=20cm]{./images/cliparts/bordeaux.png}",
            at=(0, 0),
            inner_sep=0,
            opacity=0.1,
            anchor="center",
        )


        tscope = pic.scope(yshift="4.5cm", xshift="-5cm")
        Teachometrie().draw(tscope)

        pic.node(r"\textbf{Niveaux}: L1 / L2 / L3 / M1",
                 at=(-5,1.5),
                 text_width="6cm")
        pic.node(r"\textbf{Type}: Université / École",
                 at=(-5,1),
                 text_width="6cm")

        pic.node(r"\textbf{Césure}: Développeur Fullstack",
                 at=(-5,0),
                 text_width="6cm")
        pic.node(r"Autorité de Sûreté Nucléaire",
                 at=(-5,-0.5),
                 font=r"\itshape",
                 text_width="6cm")


        pic.node(
            r"""
                 \textbf{Agrégation~:} \newline%
                 Mathématiques option informatique.
                 Khôlleur de mathématiques
                 (MPSI, MP) de 
                 2017 à 2019.
                 """,
            at=(-5, -1.8),
            anchor="north",
            rounded_corners="2mm",
            thick=True,
            draw=True,
            inner_sep="1em",
            text_width="6cm",
        )




        bibscope = pic.scope(yshift="-1.8cm", xshift="5cm")
        Bibliometrie().draw(bibscope)
        pic.node(
            r"""

                 \vspace{1em}
                 \textbf{Co-organisation} Autobóz 2024 

                 \vspace{1em}
                 Comité de programme de \textbf{CSL'26}

                 \vspace{1em}
                 Co-encadrement de 2 stagiaires

                 \vspace{1em}
                 \textcolor{A2}{\textbf{2 Prix de Thèse}} \newline
                    \emph{Ackermann Award}
                    \& \newline  \emph{E. W. Beth Dissertation Prize}
                """,
            text_width="6cm",
            anchor="north",
            at=(5, 3),
        )

        pic.node(
            r"""
                 \textbf{Expertise~:} \newline%
                 Logique, Beaux préordres, Automates
                 """,
            at=(5, 4.5),
            anchor="north",
            rounded_corners="2mm",
            thick=True,
            draw=True,
            inner_sep="1em",
            text_width="6cm",
        )

        pic.node(
            r"Résumé",
            at=(0, 4.5),
            font="\\Large\\scshape\\bfseries",
            anchor="center",
        )

    def __iter__(self):
        yield (0, Conclusion())


# create a presentation

if __name__ == "__main__":

    tc = TableOfColors()

    tf = TitleFrame(with_name=True)
    qs = QuiSuisJe(bib=Bibliometrie())

    wqo = WQOWorks(
        nsquare=NSquareWqo(
            points=[(7, 3), (8, 2), (0, 8)],
            grid_size=10,
        ),
        utilite=WqoUtilite(),
    )

    auto = AutomatesTransducteurs()

    rs = Research.default()
    te = Teaching()
    pr = Project.default()
    pip = PipelineIngestion()
    pstr = ProjetSystTrans()
    pipl = ProjetPipeline()

    it = Integration.default()

    dv = LosTarskiFiniteClasses.default()

    co = Conclusion()

    frames_list = [
        tf,
        qs,
        rs,
        # dv,
        te,
        pr,
        it,
        co,
    ]

    frames = Sequential(frames_list, pos=0)

    # preview_animation(frames)
    with open("preview.tex", "w") as f:
        f.write(tikz_of_animation(frames))
