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
class Teaching:
    def draw(self, pic):
        pass

    def __iter__(self):
        yield (0, Teaching())

@dataclasses.dataclass
class ThemesAndLocations:
    def draw(self, pic):
        themes = [("Ordres", cWA), ("Automates", cAut), ("Logique", cBD)]
        for i,(theme,col) in enumerate(themes):
            angle = math.radians(i * 120)
            x = 1 * math.cos(angle)
            y = 1 * math.sin(angle)
            pic.draw(
                (x, y),
                circle(2), 
                color=col,
                thick=True,
            )
            pic.node(theme,
                at=(3*x,3*y),
                font="\\bfseries\\scshape",
                anchor="center",
                fill=f"{col}hint",
                draw=col,
                rounded_corners="2mm",
                inner_sep="0.5em",
                text_width="2cm",
                align="center",
            ) 

        labs = [
                { "logo": "./images/institutions/irif.pdf" },
                { "logo": "./images/institutions/lmf.pdf" },
                { "logo": "./images/institutions/university_of_warsaw.pdf" },
                { "logo": "./images/institutions/mpi-sws.png" },
                { "logo": "./images/institutions/lis-marseille.pdf" },
                { "logo": "./images/institutions/labri.pdf" },
        ]

        # split logos in two groups of equal size
        half = len(labs) // 2
        labs1 = labs[:half]
        labs2 = labs[half:]
        scope1 = pic.scope(xshift="-7cm", yshift="2.5cm")
        scope2 = pic.scope(xshift="7cm", yshift="2.5cm")
        for (scope,labs) in [(scope1,labs1),(scope2,labs2)]:
            for i, lab in enumerate(labs):
                x = 0
                y = -i * 2
                scope.draw(
                    (x, y),
                    node(
                        r"""
                        \includegraphics[width=2cm]{""" + lab["logo"] + r"""}""",
                        anchor="center",
                    ),
                    thick=True,
                )


    def __iter__(self):
        yield (0, ThemesAndLocations())


@dataclasses.dataclass
class NSquareWqo:
    points: List[Tuple[int, int]]
    grid_size: int = 10
    grid_step: int = 1

    def draw(self, picture):
        picture.draw(
            (0, -2), node(r"$(\mathbb{N} \times \mathbb{N}, \leq)$"),
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

        for (x,y) in self.points:

            pic.draw((x * step, y * step), 
                     lineto((x * step, self.grid_size)),
                     lineto((self.grid_size, self.grid_size)),
                     lineto((self.grid_size, y * step)),
                     lineto((x * step, y * step)),
                     draw="A2",
                     fill="A2")

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

        for (x,y) in self.points:
            pic.draw((x * step, y * step), node("", selectedNode=True))


    def __iter__(self):
        """List the animation frames"""
        yield (0, NSquareWqo(grid_size=self.grid_size, 
                             grid_step=self.grid_step, 
                             points=[]))

        for i in range(len(self.points)):
            yield (1, NSquareWqo(grid_size=self.grid_size, 
                                 grid_step=self.grid_step, 
                                 points=self.points[:i+1]))


@dataclasses.dataclass
class WqoUtilite:
    def draw(self, pic):

        pic.style("txt", text_width="4cm", anchor="north west", align="left")
        pic.style("titl", txt=True, font="\\scshape\\bfseries")

        pic.node(r"Vérification",
                 titl=True,
                 at=(0,-3.3))
        pic.node(r"\textcolor{A4}{Systèmes de transition bien structurés (WSTS)}",
                 txt=True,
                 text_width="8cm",
                 at=(0,-4))

        pic.node(r"$(\mathbb{N}^k, \to, \leq)$ $\rightsquigarrow$ réseau de Pétri",
                 txt=True,
                 text_width="8cm",
                 at=(0,-4.5))

        pic.node(r"Graphes",
                 titl=True,
                 at=(0,-0.3))
        pic.node(r"\bsc{Robertson} \& \bsc{Seymour}",
                 txt=True,
                 at=(0,-1))
        pic.node(r"Mineurs de graphes",
                 txt=True,
                 at=(0,-1.5))

        pic.node(r"Algèbre",
                 titl=True,
                 at=(5,-0.3))
        pic.node(r"\bsc{Hilbert} / \bsc{Gröbner}",
                 txt=True,
                 at=(5,-1))
        pic.node(r"Calcul symbolique",
                 txt=True,
                 at=(5,-1.5))

    def __iter__(self):
        yield (0, WqoUtilite())

@dataclasses.dataclass
class WQOWorks:
    nsquare     : NSquareWqo
    utilite     : WqoUtilite
    show_publis : bool = True
    show_util   : bool = True


    def draw(self, pic):
        if self.show_util:
            nscope = pic.scope(yshift="-2cm",scale="0.4", xshift="-11cm")
        else:
            nscope = pic.scope(yshift="-2cm",scale="0.4")

        self.nsquare.draw(nscope)

        if self.show_util:
            uscope = pic.scope(yshift="2.7cm", xshift="0cm")
            self.utilite.draw(uscope)

        if self.show_publis:
            pic.node(r"""
                     \textbf{FoSSaCS'23}~: théorème de point fixe 
                     \newline%
                     2 articles de journaux~:
                     \emph{types d’ordres} et \emph{nouveaux espaces}
                     """,
                     at=(0,0),
                     rounded_corners="2mm",
                     text_width="6cm",
                     thick=True,
                     fill="white",
                     draw="A5",
                     inner_sep="1em")

    def __iter__(self):
        for (d, nsq) in self.nsquare:
            yield (d, WQOWorks(nsquare=nsq, utilite=self.utilite, show_util=False, show_publis=False))
        yield (1, WQOWorks(nsquare=self.nsquare, utilite=self.utilite, show_util=True, show_publis=False))
        yield (1, WQOWorks(nsquare=self.nsquare, 
                           utilite=self.utilite, 
                           show_util=True, 
                           show_publis=True))

@dataclasses.dataclass
class AutomateOdd:
    def draw(self, autosc):
        autosc.node(r"$q_0$",
                    name="q0",
                    at=(-1,0),
                    state=True,
                    initial=True)

        autosc.node(r"$q_1$",
                    name="q1",
                    at=(1,0),
                    state=True,
                    accepting=True)

        autosc.draw("(q0)", 
                    topath("(q1)", bend_right="30"),
                    opt="->")
                    
        autosc.draw("(q1)", 
                    topath("(q0)", bend_right="30"),
                    opt="->")

        autosc.node("a", at=(0,-0.6))
        autosc.node("a", at=(0,0.6))

    def __iter__(self):
        yield (0, AutomateOdd())


@dataclasses.dataclass
class MSOOddEven:
    def draw(self, formsc):
        formsc.node(r"""$\exists X_{\text{odd}}, Y_{\text{even}},$""",
                    anchor="north west",
                    font="\\small",
                    at=(0,0))

        formsc.node(r"""$\quad \text{AllPositions} = X_{\text{odd}} \uplus Y_{\text{even}}$""",
                    anchor="north west",
                    font="\\small",
                    at=(1,-0.5))
                       
        formsc.node(r"""$\land\, \forall x,y, \, (x \in X_{\text{odd}} \land x+1=y)  \implies y \in Y_{\text{even}}$""",
                    anchor="north west",
                    font="\\small",
                    at=(1,-1))
                       
        formsc.node(r"""$\land\, \forall x,y, \, (x \in X_{\text{even}} \land x+1=y)  \implies y \in Y_{\text{odd}}$""",
                    anchor="north west",
                    font="\\small",
                    at=(1,-1.5))


    def __iter__(self):
        yield (0, MSOOddEven())


@dataclasses.dataclass
class AutomatesTransducteurs:

    automa:  bool = True
    verif:   bool = True
    publis:  bool = True


    def draw(self, pic):
        pic.style("txt", text_width="3.5cm", anchor="north west", align="left")
        pic.style("titl", txt=True, font="\\scshape\\bfseries")
        pic.style("cat",
                  text_width="2cm",
                  minimum_height="2cm",
                  align="center",
                  draw=True,
                  rounded_corners="2mm",
                  inner_sep="1em",
                  )

        visionsc = pic.scope(xshift="-7cm",yshift="-1.3cm",)

        visionsc.node(r"Logique",
                 cat=True,
                 name="log",
                 at=(0,0))
        visionsc.node(r"Automates",
                 cat=True,
                 name="aut",
                 at=(4,0))
        visionsc.node(r"Monoïdes",
                 name="mono",
                 cat=True,
                 at=(0,3))
        visionsc.node(r"Expressions",
                 name="expr",
                 cat=True,
                 at=(4,3))

        visionsc.draw("(log)", topath("(aut)"), opt="<->")
        visionsc.draw("(log)", topath("(mono)"), opt="<->")
        visionsc.draw("(expr)", topath("(mono)"), opt="<->")
        visionsc.draw("(expr)", topath("(aut)"), opt="<->")

        visionsc.node(r"\textbf{Langages} $L \colon \Sigma^* \to \mathsf{Bool}$",
                 txt=True,
                 text_width="5cm",
                 at=(0,-1.5))



        if self.verif:
            verifscope = pic.scope(yshift="2.7cm",xshift="1cm")
            verifscope.node(r"Décidabilité",
                     titl=True,
                     at=(0,-3.3))
            verifscope.node(r"Équivalence~? $\mathsf{FO}$-définissabilité~? etc.",
                     txt=True,
                     text_width="7cm",
                     at=(0,-4))

            verifscope.node(r"Quantitatif",
                     titl=True,
                     at=(0,-0.3))
            verifscope.node(r"$f \colon \Sigma^* \to \mathbb{N}$",
                     txt=True,
                     at=(0,-1))
            verifscope.node(r"\emph{Automates pondérés}",
                     txt=True,
                     at=(0,-1.5))

            verifscope.node(r"Qualitatif",
                     titl=True,
                     at=(5,-0.3))
            verifscope.node(r"$f \colon \Sigma^* \to \Gamma^*$",
                     txt=True,
                     at=(5,-1))
            verifscope.node(r"\emph{Fonctions (poly)régulières}",
                     txt=True,
                     at=(5,-1.5))

        if self.automa:
            visionsc.node(drawing_to_node(AutomateOdd(), 2),
                          at=(4,0),
                          fill="white",
                          anchor="center")
            visionsc.node(drawing_to_node(MSOOddEven(), 2),
                          at=(0,0),
                          fill="white",
                          anchor="center")

            visionsc.node(r"$\mathbb{Z}/2\mathbb{Z}$",
                          at=(0,3),
                          text_width="2cm",
                          fill="white",
                          align="center",
                          anchor="center")

            visionsc.node(r"$(aa)^*$",
                          at=(4,3),
                          text_width="2cm",
                          fill="white",
                          align="center",
                          anchor="center")


        if self.publis:
            pic.node(r"""
                     \textbf{LICS'23~:} fonctions $\mathbb{Z}$-polyrégulières 
                     \newline%
                     \textbf{STACS'25~:} fonctions $\mathbb{N}$-polyrégulières
                     """,
                     at=(0,0.2),
                     rounded_corners="2mm",
                     thick=True,
                     text_width="6cm",
                     fill="white",
                     draw="A5",
                     inner_sep="1em")



    def __iter__(self):
        yield (0, AutomatesTransducteurs(False, False, False))
        for i in range(1, 4):
            yield (1, AutomatesTransducteurs(i >= 1, i >= 2, i >= 3))


@dataclasses.dataclass
class Research:
    def draw(self, pic):
        ThemesAndLocations().draw(pic)
        f = FilAriane(
                 header="Thèmes de recherche",
                 width=8,
                 current=None,
                 titles=["Ordres", "Automates", "Logique"],
        )
        arsc = pic.scope(yshift="5.15cm")
        f.draw(arsc)
        pass

    def __iter__(self):
        yield (0, Research())

@dataclasses.dataclass
class PipelineIngestion:
    mode: Literal["Init", "Pipeline", "Interaction", "Verif"] = "Verif"
    def draw(self, pic):

        pic.node(r"\includegraphics[width=19cm]{./images/science/flamanville.jpg}",
                 at=(0,0),
                 opacity=(0.1 if self.mode != "Init" else 1),
                 anchor="center")

        pic.node(r"Un \underline{exemple} de programme utilisant des données",
                 at=(0,4.5),
                 font="\\Large\\scshape", anchor="center")

        if self.mode != "Init":
            pic.node(r"Amont~: Pipeline d’Ingestion",
                     font=r"\scshape\bfseries\large",
                     at=(-5,3.5))

            pic.draw((0,3.5), topath((0,-3.5)),
                     dashed=True,
                     thick=True,
                     color="A1")

            pic.node(r"\includegraphics[width=1.5cm]{./images/cliparts/centrales-map.pdf}",
                    at=(-7,2),
                    draw=True,
                    thick=True,
                    fill="white",
                    name="centrales",
                    rounded_corners="2mm",
                    anchor="center")

            pic.node(r"\includegraphics[width=1.5cm]{./images/cliparts/rss-svgrepo-com.png}",
                     at=(-7,0),
                    draw=True,
                    name="rss",
                    thick=True,
                    fill="white",
                    rounded_corners="2mm",
                    anchor="center")

            pic.node(r"\includegraphics[width=1.5cm]{./images/cliparts/database-svgrepo-com.png}",
                    at=(-7,-2),
                    draw=True,
                    name="innerdb",
                    thick=True,
                    fill="white",
                    rounded_corners="2mm",
                    anchor="center")

            pic.node(r"\includegraphics[width=1.5cm]{./images/cliparts/database-svgrepo-com copy.png}",
                    at=(0,0),
                    name="db",
                    draw=True,
                    thick=True,
                    fill="white",
                    rounded_corners="2mm",
                    anchor="center")

            pic.draw("(centrales)", topath("(db)", _out="0", _in="180"), opt="->", thick=True)
            pic.draw("(innerdb)",   topath("(db)", _out="0", _in="180"), opt="->", thick=True)
            pic.draw("(rss)",       topath("(db)", _out="0", _in="180"), opt="->", thick=True)

        if self.mode != "Init" and self.mode != "Pipeline":
            pic.node(r"Aval~: Interaction via une API",
                     font=r"\scshape\bfseries\large",
                     at=(5,3.5))

            pic.node(r"\includegraphics[width=1.5cm]{./images/cliparts/task-list-svgrepo-com.png}",
                    at=(7,2),
                    draw=True,
                    name="annot",
                    thick=True,
                    fill="white",
                    rounded_corners="2mm",
                    anchor="center")

            pic.node(r"\includegraphics[width=1.5cm]{./images/cliparts/admin-with-cogwheels-svgrepo-com.png}",
                    at=(7,-2),
                    name="admin",
                    draw=True,
                    thick=True,
                    fill="white",
                    rounded_corners="2mm",
                    anchor="center")

            pic.draw("(db)", topath("(annot)", _in="180", _out="0"), opt="<->",thick=True)
            pic.draw("(db)", topath("(admin)", _in="180", _out="0"), opt="<->",thick=True)


        if self.mode == "Verif":
            pic.node(r"Vérification~: $\{ \varphi \} \, P \, \{ \psi \}$~? (Hoare)",
                     at=(-5,-4),
                     color="A2",
                     font=r"\large")

            pic.node(r"Vérification~: $D_0 \to^* D_\text{err}$~? (Accessibilité)",
                     at=(5,-4),
                     color="A2",
                     font=r"\large")

    def __iter__(self):
        yield (0, PipelineIngestion(mode="Init"))
        for m in ["Pipeline", "Interaction", "Verif"]:
            yield (1, PipelineIngestion(mode=m))

@dataclasses.dataclass
class PolyregPonderes:
    quant: bool = False
    exp: bool = False
    def draw(self, pic):

        pic.style("guessed",
                  text="C1",
                  )
        pic.style("decidable",
                  draw="B5", thick=True,
                  double=True,
                  )
        pic.style("important",
                  draw="A2",
                  thick=True,
                  )

        if self.quant:
            pic.node(r"$\mathbb{N}\mathsf{FOPoly}$",
                     name="nsf",
                     at=(0,0,0))

            pic.node(r"$\mathbb{N}\mathsf{Poly}$",
                     name="npo",
                     at=(0,3,0))

        pic.node(r"$\mathsf{FOPoly}$",
                 name="sf",
                 font="\\bfseries",
                 at=(3,0,0))

        pic.node(r"$\mathsf{Poly}$",
                 name="poly",
                 font="\\bfseries",
                 at=(3,3,0))

        if self.exp:
            pic.node(r"$\mathbb{N}\mathsf{Exp}$",
                     name="nexp",
                     at=(0,3,-3))
            pic.node(r"$\mathbb{N}\mathsf{FOExp}$",
                     name="nfoexp",
                     guessed=True,
                     at=(0,0,-3))

            pic.node(r"$\mathsf{FOExp}$",
                     name="foexp",
                     guessed=True,
                     at=(3,0,-3))

            pic.node(r"$\mathsf{Exp}$",
                     name="exp",
                     guessed=True,
                     at=(3,3,-3))
        
            pic.draw("(poly)", topath("(exp)"), dashed=True, opt="->")
            pic.draw("(nfoexp)", topath("(foexp)"), dashed=True, opt="->")
            pic.draw("(nsf)", topath("(nfoexp)"), dashed=True, opt="->")
            pic.draw("(sf)", topath("(foexp)"), dashed=True, opt="->")
            pic.draw("(foexp)", topath("(exp)"), dashed=True, opt="->")
            pic.draw("(nfoexp)", topath("(nexp)"), dashed=True, opt="->")
            pic.draw("(nexp)", topath("(exp)"), dashed=True, opt="->")
            pic.draw("(npo)", topath("(nexp)"), 
                     decidable=True,
                     opt="->")

        if self.quant:
            pic.draw("(nsf)", topath("(npo)"), 
                     dashed=True, opt="->")
            pic.draw("(npo)", topath("(poly)"), 
                     decidable=True,
                     opt="->")
            pic.draw("(nsf)", topath("(sf)"), 
                     decidable=True,
                     opt="->")

        pic.draw("(sf)", topath("(poly)"), 
                 important=True,
                 opt="->")
        

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
        pic.style("lbl",
                  anchor="north west",
                  text_width="8cm",
                  align="left",
                  font="\\large")

        pic.node(r"\includegraphics[width=8cm]{./simple-for-programs.png}",
                 at=(-5,-0.8),
                 opacity=(1 if self.showProg else 0.2),
                 anchor="center")

        pic.node(r"\textbf{Objet~:} programmes Python «~simples~» \strut",
                 at=(-9,4),
                 lbl=True
                 )

        pic.node(r"\textbf{Point de départ~:} \emph{fonctions polyrégulières}\strut",
                 at=(-9,3.5),
                 lbl=True)

        if self.showProb:
            pic.node(r"Problèmes théoriques à long terme",
                     at=(-9, 2.5),
                     color="A2",
                     anchor="north west",
                     font=r"\large\bfseries\scshape")
            
            pic.node(r"Décider l’équivalence de fonctions",
                    at=(-9,2),
                     color="A2",
                    font=r"\large",
                    anchor="north west")
            pic.node(r"Décider la $\mathsf{FO}$-définissabilité",
                    at=(-9,1.5),
                    font=r"\large",
                     color="A2",
                    anchor="north west")

        
        if self.showUnaire:
            pic.node(r"""\textbf{Dans un premier temps} \newline%
                        $\rightsquigarrow$ sorties unaires $\{a\}^* \simeq \mathbb{N}$
                        \newline%
                        $\rightsquigarrow$ entrées unaires / commutatives~?
                        \newline%
                        $\rightsquigarrow$ lien quantitatif / qualitatif~?
                     """,
                    at=(-9,0.7),
                    font=r"\large",
                    text_width="8cm",
                    anchor="north west")

        if self.showProb:
            diagram = pic.scope(xshift="3cm", yshift="-0.5cm")
            PolyregPonderes(self.showUnaire, self.showExp).draw(diagram)


        if self.showImplem:
            pic.node(r"""Implémentation(s)""",
                     at=(-9,-1.7),
                     anchor="north west",
                     font="\\large\\bfseries\\scshape",
                     text="A1")
            pic.node(r"""

                     $\rightsquigarrow$ Vérification de triplets de Hoare~?
                     \newline%
                     $\rightsquigarrow$ Optimisations de programmes~?
                     """,
                     at=(-9,-2.3),
                     anchor="north west",
                     font="\\large",
                     text_width="8cm",
                     text="A1",
                     )

        if self.showPolycheck:
            pic.node(r"\includegraphics[width=7cm]{./polycheck.png}",
                     at=(5,-2.5),
                     anchor="center")
            pic.node(r"[\textbf{Lopez}, \bsc{Stefański}, preprint]",
                     at=(5,-2.5),
                     fill="white",
                     draw="A5",
                     rounded_corners="2mm",
                     anchor="center")



    def __iter__(self):
        yield (0, ProjetPipeline(True, False, False, False, False, False))
        for i in range(1, 6):
            yield (1, ProjetPipeline( 
                                     False,
                                      i >= 1, i >= 2, i >= 3, i >= 4, i >= 5))

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

        pic.style("lbl",
                  anchor="north west",
                  text_width="8cm",
                  align="left",
                  font="\\large")

        pic.node(r"""\textbf{Cadre~:} 
                 classes de structures relationnelles finies $\mathcal{C}$
                 avec une relation de transtion $\to$\strut
                 """,
                 at=(-9,4),
                 lbl=True
                 )
        if self.showPartiPris:
            pic.node(r"""\textbf{Parti pris~:}
                     $(\mathcal{C}, \to, \subseteq_i)$
                     \newline%
                     \emph{Système de transition bien structuré}
                     \strut""",
                     at=(9,4),
                     lbl=True,
                     anchor="north east")

            diagshape = pic.scope(xshift="1.1cm", yshift="1cm",scale=1.5)

            diagshape.node(r"$\mathfrak{A}$",
                           name="A",
                           at=(0,0))
            diagshape.node(r"$\mathfrak{B}$",
                           name="B",
                           at=(1,0))
            diagshape.node(r"$\mathfrak{A}'$",
                           name="Ap",
                           at=(0,1))
            diagshape.node(r"$\mathfrak{B}'$",
                           name="Bp",
                           at=(1,1))

            diagshape.draw("(A)", topath("(B)"), opt="->")
            diagshape.draw("(Ap)", topath("(Bp)"), opt="->", dashed=True)
            diagshape.node(r"$\subseteq_i$",
                           at=(0,0.5),
                           rotate="90")
            diagshape.node(r"$\subseteq_i$",
                           at=(1,0.5),
                           rotate="90")

            pic.node(r"""Couvrabilité~:
                     \newline%
                     $D_0 \to^* D' {}_i\!\!\supseteq D_{\text{err}}$ décidable
                     """,
                     at=(9,2.7),
                     anchor="north east",
                     fill="white",
                     draw="A5",
                     rounded_corners="2mm",
                     text_width="5cm")

            pic.node(r"""(Sous hypothèses de \emph{calculabilité})""",
                     at=(9,1.8),
                     anchor="north east",
                     text_width="5cm")

        if self.showProb:
            pic.node(r"Problème à long terme\strut",
                     at=(-9,2.7),
                     color="A2",
                     anchor="north west",
                     font=r"\large\bfseries\scshape")

            pic.node(r"""\textbf{Reconnaître} les systèmes $(\mathcal{C}, \to, \subseteq_i)$ qui sont
                     bien structurés""",
                    at=(-9,2.2),
                    color="A2",
                    anchor="north west")

        if self.showWqo:
            pic.node(r"""\textbf{Dans un premier temps, ignorer $\to$} \newline%
                     $\rightsquigarrow$ $(\mathcal{C}, \subseteq_i)$
                     est un \emph{beau préordre}~?""",
                     text_width="7cm",
                    at=(-9,1.5),
                    anchor="north west")

        if self.showConj:
            pic.node(r"""\textbf{Conjecture [Daligault et al., 2010]~:} 
                         \newline%
                         $(\mathcal{C}, \subseteq_i)$
                         \emph{beau préordre}
                         \newline%
                         $\implies$
                         \newline%
                         $\mathcal{C}$ a \emph{largeur de clique bornée} ($\mathsf{MSO}$)""",
                     at=(-9,0.4),
                     text_width="7cm",
                     fill="D4hint",
                     anchor="north west")
        
        if self.showRepr:
            pic.node(r"""\textbf{Différentes représentations}
                            \newline%
                            $\rightsquigarrow$ $(\Sigma^*, \leq_{\text{facteur}})$
                            représente les classes $(\mathcal{C}, \subseteq_i)$
                            \newline%
                            $\rightsquigarrow$
                            Classe de largeur de clique bornée
                         """,
                        at=(-9,-1.6),
                        text_width="7cm",
                        anchor="north west")

        if self.showFutur:
            pic.node(r"""\textbf{Et plus tard}~?
                            \newline%
                            $\rightsquigarrow$ \emph{homomorphismes}~?
                            \newline%
                            $\rightsquigarrow$
                            relations $\to$~?
                         """,
                        at=(-9,-3.2),
                        text_width="7cm",
                        anchor="north west")
        
        if self.showBDD:
            pic.node(r"""Une ouverture sur les bases de données""",
                     at=(0.8,-1),
                     anchor="north west",
                     font="\\large\\bfseries\\scshape",
                     text="A1")

            pic.node(r"""Algorithmes de type \emph{Chase} \newline%
                     $D_0$ base de donnée,
                     $\Delta$ contraintes,
                     $q$ requête
                         \newline%
                     «~toute complétion de $D_0$ vérifiant $\Delta$ satisfait $q$~?»""",
                     at=(0.8,-1.5),
                     text_width="8cm",
                     anchor="north west")

            pic.node(r"""$(\mathcal{C}, \to_{\Delta}, \to_{\text{hom}})$ 
                     $\rightsquigarrow$
                     $D_0 \to_{\Delta}^* D_{\text{err}} \models \Delta \wedge \neg q$~?""",
                     at=(0.8,-3),
                     text_width="7cm",
                     anchor="north west")


    def __iter__(self):
        yield (0, ProjetSystTrans(False,False,False,False,False,False,False))
        for i in range(1, 8):
            yield (1, ProjetSystTrans(i >= 1, i >= 2, i >= 3, i >= 4, i >= 5, i >= 6, i >= 7))

@dataclasses.dataclass
class Project:
    def draw(self, pic):
        pass

    def __iter__(self):
        yield (0, Project())

@dataclasses.dataclass
class Conclusion:
    def draw(self, pic):
        pass

    def __iter__(self):
        yield (0, Conclusion())



# create a presentation

if __name__ == "__main__":

    tf = TitleFrame(with_name=True)
    qs = QuiSuisJe(bib=Bibliometrie())

    wqo =  WQOWorks(
       nsquare=NSquareWqo(
            points=[(7,3), (8,2), (0,8)],
            grid_size=10,
           ),
       utilite=WqoUtilite(),
    )

    auto = AutomatesTransducteurs()

    rs = Research()
    te = Teaching()
    pr = Project()
    pip = PipelineIngestion()
    pstr = ProjetSystTrans()
    pipl = ProjetPipeline()

    co = Conclusion()

    frames_list = [
        tf,
        qs,
        wqo,
        auto,
        rs,
        te,
        pip,
        pstr,
        pipl,
        pr,
        co,
    ]   

    frames = Sequential(frames_list, pos=0)

    preview_animation(frames)
