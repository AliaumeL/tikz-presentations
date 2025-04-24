from tikz import *

import math
import dataclasses
from typing import Literal, Generator, Callable, List, Union, Tuple, Optional
import random
import bibtexparser


from graphs import *
from utils import *


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

        pic.node(
            r"\includegraphics[width=2cm]{./petri_net.png}",
            at=(3, -6),
        )

        pic.node(r"Graphes", titl=True, at=(0, -0.3))
        pic.node(r"\bsc{Robertson} \& \bsc{Seymour}", txt=True, at=(0, -1))
        pic.node(r"Mineurs de graphes", txt=True, at=(0, -1.5))

        pic.node(
            r"\includegraphics[width=2cm]{./graph_minor.png}",
            at=(2, 1),
            anchor="center",
        )

        pic.node(r"Algèbre", titl=True, at=(5, -0.3))
        pic.node(r"\bsc{Hilbert} / \bsc{Gröbner}", txt=True, at=(5, -1))
        pic.node(r"Calcul symbolique", txt=True, at=(5, -1.5))

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
                     \textbf{Objectif~:}
                     \newline
                     construire de \textcolor{A2}{nouveaux}
                     beaux préordres.
                     """,
                at=(0, 0),
                rounded_corners="2mm",
                text_width="7cm",
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
class HigmanSubword:
    small_word: str
    big_word: str
    embedding: List[int]
    show_big_word: bool
    show_embedding: bool
    show_orders: bool
    show_thm: bool = False

    def draw(self, pic: Picture):
        small_size = len(self.small_word)
        big_size = len(self.big_word)
        coef = 1 if self.show_orders else 0.3
        pic.draw((0, 4.5), node(r"L’ordre sous-mot de Higman", font="\\huge\\scshape"))

        sc = pic.scope(yshift="-2cm")

        for i, a in enumerate(self.small_word):
            posx = (i - small_size / 2) * coef
            sc.node(
                r"\strut\ " + a + r"\strut\ ",
                at=(posx, 0),
                name=f"A{i}",
                minimum_size="1.5em",
                align="left",
                inner_sep="0pt",
                draw=True if self.show_orders else None,
                circle=True if self.show_orders else None,
                anchor="base",
            )

        if not self.show_orders:
            sc.draw(
                "(A0.north west)",
                rectangle(f"(A{small_size - 1}.south east)"),
                draw="C5",
            )

        if self.show_big_word:
            for j, b in enumerate(self.big_word):
                posx = (j - big_size / 2) * coef
                sc.node(
                    r"\strut\ " + b + r"\strut\ ",
                    at=(posx, 2),
                    minimum_size="1.5em",
                    draw=True if self.show_orders else None,
                    circle=True if self.show_orders else None,
                    inner_sep="0pt",
                    align="left",
                    name=f"B{j}",
                    anchor="base",
                )

            if not self.show_orders:
                sc.draw("(B0.north west)", rectangle(f"(B{big_size - 1}.south east)"))

        if self.show_orders:
            for x, word, angle in [
                ("A", self.small_word, "-90"),
                ("B", self.big_word, "90"),
            ]:
                for i in range(len(word)):
                    for j in range(i):
                        sc.draw(
                            f"({x}{i})",
                            topath(f"({x}{j})", _in=angle, out=angle),
                            opacity=1 / (i - j + 1),
                            postaction=r"{decorate,decoration={markings,mark=at position 0.5 with {\arrow{>}}}}",
                            opt="->",
                        )

        if self.show_big_word and self.show_embedding:
            for i, j in enumerate(self.embedding):
                sc.draw(f"(A{i})", topath(f"(B{j})"), opt="->")

            sc.draw((0, -2), node(r"$\sigma = \{ (\leq, 2) \}$", font="\\large"))

        if self.show_thm:
            pic.node(
                r"""
                     \textbf{Théorème (Higman)~:}
                     Si $(X, \leq)$ est WQO,
                     alors $(X^*, \leq^*)$ est WQO.
                     """,
                at=(0, 0),
                rounded_corners="2mm",
                text_width="7cm",
                thick=True,
                fill="white",
                draw="A5",
                inner_sep="1em",
            )

    def __iter__(self):
        yield (
            0,
            HigmanSubword(
                self.small_word,
                self.big_word,
                self.embedding,
                False,
                False,
                False,
                False,
            ),
        )
        yield (
            1,
            HigmanSubword(
                self.small_word,
                self.big_word,
                self.embedding,
                True,
                False,
                False,
                False,
            ),
        )
        yield (
            1,
            HigmanSubword(
                self.small_word, self.big_word, self.embedding, True, True, False, False
            ),
        )
        yield (
            1,
            HigmanSubword(
                self.small_word, self.big_word, self.embedding, True, True, True, False
            ),
        )
        yield (
            1,
            HigmanSubword(
                self.small_word, self.big_word, self.embedding, True, True, True, True
            ),
        )


@dataclasses.dataclass
class StateOfTheArt:
    frame: int
    show_conj: bool = True

    def draw(self, pic: Picture):

        with open("papers.bib") as bibtex_file:
            bib = bibtexparser.load(bibtex_file)

        entries = [
            {
                "title": entry["title"],
                "author": extract_author(entry["author"]),
                "year": entry["year"],
            }
            for entry in bib.entries
            if entry.get("graphs", None) is not None
        ]
        entries.sort(key=lambda x: -int(x["year"]))

        num = len(entries)
        entries_right = entries[: num // 2]
        entries_left = entries[num // 2 :]
        entries_right.reverse()

        for e, x, align, anchor, prefix in [
            (entries_left, -10, "right", "west", "L"),
            (entries_right, 9.5, "left", "east", "R"),
        ]:
            for i, entry in enumerate(e):
                authors = ", ".join(entry["author"])
                pic.node(
                    authors,
                    at=(x, -i + 2),
                    anchor=anchor,
                    name=f"A{prefix}{i}",
                    align=align,
                    font="\\small",
                    text_width="5cm",
                )
                pic.node(
                    entry["title"],
                    at=(x, -i + 1.5),
                    anchor=anchor,
                    opacity=0.6,
                    inner_sep="0pt",
                    name=f"T{prefix}{i}",
                    font="\\itshape\\tiny",
                    align=align,
                    text_width="5cm",
                )

        timeline_y = -4
        timeline_x = -4
        first_year = 1990
        last_year = 2025
        scale = 8 / (last_year - first_year)

        pic.draw(
            (timeline_x, timeline_y),
            lineto((timeline_x + 8, timeline_y)),
            thick=True,
            opt="->",
        )

        for i in range(first_year, last_year + 1, 5):
            pic.draw(
                (timeline_x + scale * (i - first_year), timeline_y - 0.1),
                lineto((timeline_x + scale * (i - first_year), timeline_y + 0.1)),
            )
            pic.node(
                str(i),
                at=(timeline_x + scale * (i - first_year), timeline_y - 0.3),
                anchor="center",
            )

        for e, anchor, prefix, _in, _out in [
            (entries_left, "east", "L", "90", "0"),
            (entries_right, "west", "R", "90", "180"),
        ]:
            for i, entry in enumerate(e):
                year = int(entry["year"])

                x = timeline_x + scale * (year - first_year)
                pic.coordinate(f"D{prefix}{i}", at=(x, timeline_y))
                pic.draw(
                    f"(A{prefix}{i}.{anchor})",
                    topath(f"(D{prefix}{i})", _in=_in, out=_out),
                    opt="->",
                )

        if self.show_conj:
            pic.node(
                r"""
                     \textbf{Conjecture (Daligault, Rao, Thomassé)~:}
                     \newline
                     Si $(\mathcal{C}, \subseteq_i)$ est $2$-WQO,
                     alors 
                     \newline
                     $\mathcal{C}$
                     a \textbf{largeur de clique bornée}.
                     """,
                at=(0, 0),
                rounded_corners="2mm",
                text_width="7cm",
                thick=True,
                fill="white",
                draw="A5",
                inner_sep="1em",
            )

    def __iter__(self):
        yield (0, StateOfTheArt(0, False))
        yield (1, StateOfTheArt(1, True))


@dataclasses.dataclass
class FinitePaths:
    frame: int

    def draw(self, pic: Picture):
        frame = self.frame

        pic = pic.scope(xshift="-3cm", yshift="-2cm")

        if frame >= 1:
            # draw a path of length 4
            # draw a path of length 7 above it
            # draw some embeddings
            for i in range(4):
                color = "A4" if frame >= 3 and (i == 0 or i == 3) else "A1"
                pic.node(
                    f"",
                    draw=color,
                    fill=f"{color}hint",
                    name=f"A{i}",
                    at=(i, 0),
                    minimum_size="1.5em",
                    circle=True,
                    inner_sep="0pt",
                )

            for i in range(3):
                pic.draw(f"(A{i})", topath(f"(A{i+1})"))

            for j in range(7):
                color = "A4" if frame >= 3 and (j == 0 or j == 6) else "A1"
                pic.node(
                    f"",
                    draw=color,
                    fill=f"{color}hint",
                    name=f"B{j}",
                    at=(j, 2),
                    minimum_size="1.5em",
                    circle=True,
                    inner_sep="0pt",
                )
            for i in range(6):
                pic.draw(f"(B{i})", topath(f"(B{i+1})"))

        if frame == 2 or frame == 3:
            for i in range(4):
                pic.draw(
                    f"(A{i})", topath(f"(B{i+1})"), opt="->", thick=True, color="C3"
                )

        if frame >= 4:
            pic.draw(f"(A0)", topath(f"(B0)"), opt="->", thick=True, color="C3")
            pic.draw(f"(A3)", topath(f"(B6)"), opt="->", thick=True, color="C3")

            pic.node(
                r"\includegraphics[width=4cm]{path.jpg}", at=(-4, -1), anchor="center"
            )

    def __iter__(self):
        yield (0, FinitePaths(0))
        for i in range(4):
            yield (1, FinitePaths(i + 1))


@dataclasses.dataclass
class GraphWqo:
    show_table: bool = True

    def draw(self, pic):
        pic.node(
            "Graphes WQO",
            at=(0, 4.5),
            font="\\Huge\\scshape",
        )

        pscope = pic.scope(yshift="0cm", xshift="0cm")
        pscope.node("Chemins", font="\\scshape\\bfseries", at=(-5, -3.8))
        pscope.node(
            r"$\simeq (\mathbb{N}, \leq)$",
            at=(-5, 2.2),
        )
        pscope.draw(
            (-8, 2),
            rectangle((-2, -3.5)),
            draw="A4",
            thick=True,
        )

        for i in range(5):
            c = Path(i + 1)
            sc = pscope.scope(yshift=f"{-3 + i}cm", xshift="-5cm")
            c.draw(sc)

        for i in range(4):
            pscope.node(
                r"$\subseteq_i$",
                color="C2",
                rotate="90",
                font=r"\large",
                at=(-5, -2.5 + i),
            )

        cscope = pic.scope(yshift="0cm", xshift="10cm")
        cscope.node("Cycles", at=(-5, -3.8), font="\\scshape\\bfseries")
        cscope.node(
            r"$\simeq (\mathbb{N}, =)$",
            at=(-5, 2.2),
        )
        cscope.draw(
            (-8, 2),
            rectangle((-2, -3.5)),
            draw="A4",
            thick=True,
        )

        for i in range(3, 7):
            odd = i % 2 == 1
            iup = i if odd else i - 1
            c = Cycle(i, 0.5)
            xs = "-6cm" if odd else "-4cm"
            sc = cscope.scope(yshift=f"{-5 + iup}cm", xshift=xs)
            c.draw(sc)

        if self.show_table:
            pic.node(
                r"""
                     \begin{tabular}{rcl}
                     \toprule
                     \textbf{Classe} & \textbf{Couleurs} & \textbf{WQO} \\
                     \midrule
                     Chemins & non & \textcolor{A5}{oui} \\
                     Cycles  & non & \textcolor{A2}{non} \\
                     Cliques & non & \textcolor{A5}{oui} \\
                     Cliques & oui & \textcolor{A5}{oui} \\
                     Chemins & oui & \textbf{\textcolor{A2}{non}} \\
                     \bottomrule
                     \end{tabular}
                     """,
                at=(0, 0),
                rounded_corners="2mm",
                text_width="7cm",
                align="center",
                thick=True,
                fill="white",
                draw="A5",
                inner_sep="1em",
            )

    def __iter__(self):
        yield (0, GraphWqo(False))
        yield (1, GraphWqo(True))


@dataclasses.dataclass
class PouzetConjectures:
    frame: int

    def draw(self, pic):
        frame = self.frame

        pic.style("classNode", font="\\large")

        if frame <= 1:
            pic.draw((-7.5, 1.5), rectangle((-4.5, -2)), draw="A4", fill="A4hint")
            pic.draw((4.5, 1.5), rectangle((7.5, -2)), draw="A2", fill="A2hint")

        pic.draw((-6, 0), node(r"$\mathcal{C}$", name="C", classNode=True))
        pic.draw((-6, 0.6), node(r"Est-ce que"))
        pic.draw((-6, -1.6), node(r"est WQO?", color="Prune"))
        pic.draw((6, 0), node(r"$\mathcal{C}$", name="Cinf", classNode=True))
        pic.draw((6, 0.6), node(r"Est-ce que"))
        pic.draw(
            "(Cinf.south)",
            node(
                "+ couleurs WQO",
                anchor="north",
                text_width="2cm",
                align="center",
                color="A4",
            ),
        )
        pic.draw((6, -1.6), node(r"est WQO?", color="Prune"))

        pic.draw((6, 3), node(r"Constructeur"))
        pic.draw((-6, 3), node(r"Graphes"))

        if frame == 1:
            pic.draw((-3.5, 1.5), rectangle((-0.5, -2)), draw="C3", fill="C3hint")
            pic.draw((0.5, 1.5), rectangle((3.5, -2)), draw="C5", fill="C5hint")

        if frame >= 1:
            pic.draw((-2, 3), node(r"?"))
            pic.draw((2, 3), node(r"Théorie des Modèles"))

            pic.draw((-2, 0), node(r"$\mathcal{C}$", name="C2", classNode=True))
            pic.draw((2, 0), node(r"$\mathcal{C}$", name="Cfin", classNode=True))

            pic.draw(
                "(C2.south)",
                node(
                    "+ 2 couleurs",
                    anchor="north",
                    text_width="3cm",
                    align="center",
                    color="A4",
                ),
            )
            pic.draw(
                "(Cfin.south)",
                node(
                    "+ couleurs finies",
                    anchor="north",
                    text_width="2cm",
                    align="center",
                    color="A4",
                ),
            )

            for x in [-2, 2]:
                pic.draw((x, 0.6), node(r"Est-ce que"))
                pic.draw((x, -1.6), node(r"est WQO?", color="Prune"))

        if frame >= 2:
            pic.draw("(C)", topath("(C2)", bend_left="30"), double=True, opt="<-")
            pic.draw("(C2)", topath("(Cfin)", bend_left="30"), double=True, opt="<-")
            pic.draw("(Cfin)", topath("(Cinf)", bend_left="30"), double=True, opt="<-")

        if frame >= 3:
            pic.draw((0, 1.6), node("Conjecture 1", align="center", text_width="2cm"))
            pic.draw(
                (-1, 1),
                lineto((1, 1)),
                double=True,
                opt="->",
                dashed=True,
                thick=True,
                color="B2",
            )
            pic.draw((4, 1.6), node("Conjecture 2", align="center", text_width="2cm"))
            pic.draw(
                (3, 1),
                lineto((5, 1)),
                double=True,
                opt="->",
                dashed=True,
                thick=True,
                color="B2",
            )

        if frame >= 4:
            pic.draw(
                (-9.5, -1.5),
                node(
                    r"\includegraphics[width=2cm]{pouzet.jpg}",
                    anchor="north west",
                    text_width="2cm",
                    align="center",
                    rounded_corners="5pt",
                ),
            )
            pic.draw(
                (-7, -3),
                node(
                    r"\textbf{Conjecture de Pouzet (1)}: $2 = \omega$",
                    anchor="west",
                    align="left",
                    text_width="15cm",
                ),
            )
            pic.draw(
                (-7, -3.5),
                node(
                    r"\textbf{Conjecture de Pouzet (2)}: $\omega = \mathsf{WQO}$",
                    anchor="west",
                    align="left",
                    text_width="15cm",
                ),
            )
            pic.draw(
                (-7, -4),
                node(
                    r"\textbf{Conjecture de Schmitz}: les chemins sont la seule obstruction",
                    anchor="west",
                    align="left",
                    text_width="15cm",
                ),
            )

    def __iter__(self):
        yield (0, PouzetConjectures(0))
        for i in range(4):
            yield (1, PouzetConjectures(i + 1))


if __name__ == "__main__":
    preview_animation(
        Sequential(
            frames=[
                WQOWorks(
                    nsquare=NSquareWqo(
                        points=[(7, 3), (5, 6), (0, 8), (8, 0)],
                        grid_size=10,
                    ),
                    utilite=WqoUtilite(),
                ),
                HigmanSubword("psl", "paris-saclay", [0, 4, 9], True, True, True),
                GraphWqo(),
                FinitePaths(0),
                PouzetConjectures(0),
                StateOfTheArt(0),
            ],
            pos=0,
        )
    )
