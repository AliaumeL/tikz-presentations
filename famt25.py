#!/usr/bin/env python3
#
# Aliaume LOPEZ
#

from tikz import *

import tikz_presentations_aliaume as tpa

from tikz_presentations_aliaume.components.utils import *
from tikz_presentations_aliaume.components.graphs import *

import yaml

import bibtexparser

import math

import random
import dataclasses
from typing import Literal, Generator, Callable, List, Union, Tuple, Optional


@dataclasses.dataclass
class TitleFrame:
    def draw(self, pic: Picture):
        scope = pic.scope(yshift="2cm")

        scope.node(
            "Well-Quasi-Orders",
            at=(0, 1),
            anchor="center",
            font="\\huge\\scshape",
            color="D2",
        )
        scope.node(
            "and",
            at=(0, 0),
            anchor="center",
            font="\\huge\\scshape",
            color="A4",
        )

        scope.node(
            "Logic on Graphs",
            at=(0, -1),
            anchor="center",
            align="center",
            color="A3",
            text_width="16cm",
            font="\\huge\\scshape",
        )

        pic.draw((0, -1), node("Aliaume Lopez", anchor="center", font="\\Large"))
        pic.draw((0, -1.5), node("University of Warsaw", anchor="center"))
        pic.draw((0, -3), node(f"Les Houches", anchor="center", font="\\Large"))
        pic.draw((0, -3.5), node(f"FMT'25, 2025-05-29", anchor="center"))
        pic.draw((6, -2), node(r"\qrcode{https://www.irif.fr/~alopez/}"))
        pic.draw((6, -3.5), node(r"\url{https://www.irif.fr/~alopez/}"))

        logos = [
            "images/institutions/university_of_warsaw.pdf",
            "images/institutions/zigmunt_zaleski_stitching.png",
        ]
        for i, logo in enumerate(logos):
            pic.draw(
                (-4 - 3 * i, -2),
                node(f"\\includegraphics[width=2cm]{{{logo}}}", anchor="center"),
            )

    def __iter__(self):
        yield (0, self)


@dataclasses.dataclass
class BunchOfGraphs:
    rows: int = 3
    cols: int = 4
    graphs: List = dataclasses.field(default_factory=list)
    width: float = 15
    height: float = 10
    scale: float = 1

    def draw(self, pic: Picture):
        xpos = lambda x: (self.width / (self.cols - 1)) * x - (self.width / 2)
        ypos = lambda y: (self.height / (self.rows - 1)) * y - (self.height / 2)

        grid = [(xpos(i), ypos(j)) for i in range(self.cols) for j in range(self.rows)]

        for g, (i, j) in zip(self.graphs, grid):
            scg = pic.scope(
                xshift=f"{i:0.2f}cm", yshift=f"{j:0.2f}cm", scale=f"{self.scale}"
            )
            g.draw(scg)

    def __iter__(self):
        yield (0, dataclasses.replace(self, graphs=self.graphs[:1]))
        for i in range(2, len(self.graphs) + 1):
            yield (1, dataclasses.replace(self, graphs=self.graphs[:i]))


@dataclasses.dataclass
class AbstractionLabel:
    lbl: str

    def draw(self, pic):
        pic.node(
            self.lbl,
            at=(0, 0),
            draw=True,
            fill="white",
            rounded_corners="2mm",
            inner_sep="2pt",
        )

    def __iter__(self):
        yield (0, self)


@dataclasses.dataclass
class SequenceOfHG:
    bog: BunchOfGraphs
    dims: List[Tuple[int, int]]
    show_dims: bool

    def from_dims(dims: List[Tuple[int, int]], rows: int, cols: int):
        grs = [HalfGraph(topsize=x, botsize=y) for (x, y) in dims]
        bog = BunchOfGraphs(
            graphs=grs, scale=0.5, width=10, height=6, rows=rows, cols=cols
        )

        return SequenceOfHG(bog=bog, dims=dims, show_dims=True)

    def draw(self, pic: Picture):
        self.bog.draw(pic)
        if self.show_dims:
            lbls = [AbstractionLabel(f"({i},{j})") for (i, j) in self.dims]
            bog2 = dataclasses.replace(self.bog, graphs=lbls)

            bog2.draw(pic)

    def __iter__(self):
        for d, bog in self.bog:
            yield (d, dataclasses.replace(self, bog=bog, show_dims=False))
        yield (1, self)


@dataclasses.dataclass
class WqoSeq:
    points: List[str]
    pair: Tuple[int, int]
    show_sequence: bool = True
    show_pair: bool = True

    def draw(self, pic):
        pic.node(
            "Well-quasi-order (WQO)", at=(-0.5, 1), anchor="west", font=r"\bfseries"
        )

        pic.node(r"$(X, \leq)$", at=(4, 1))

        if self.show_sequence:
            for i, x in enumerate(self.points):
                pic.node(x + r"\strut", at=(i, 0), name=f"ws{i}")

        if self.show_pair:
            i, j = self.pair
            pic.draw(
                f"(ws{i})",
                topath(f"(ws{j})", _in="-90", _out="-90"),
                thick=True,
                opt="->",
                color="D2",
            )
            pic.node(r"$\leq$", at=((i + j) / 2, -1.2), font=r"\bfseries", color="D2")
            pic.node(r"$\exists$", at=((i + j) / 2, -0.4), color="D2")

    def __iter__(self):
        yield (0, dataclasses.replace(self, show_sequence=False, show_pair=False))
        for i in range(1, 3):
            yield (
                1,
                dataclasses.replace(self, show_sequence=(i >= 1), show_pair=(i >= 2)),
            )


@dataclasses.dataclass
class WQO101:
    wqo_def: WqoSeq
    show_uses: bool = True

    def draw(self, pic):
        pic.node(r"Well-Quasi-Orders 101", at=(0, 4), font=r"\Large\bfseries")

        defsc = pic.scope(xshift="-9cm", yshift="2cm")
        self.wqo_def.draw(defsc)

        imgs = [
            ("./images/science/cox_little_shea.jpg", "4", "Algebra"),
            ("./images/science/graph_minor.png", "4", "Graph Minors"),
            ("./images/science/petri_net.png", "4", "Transition Systems"),
        ]

        grid = [(6, 0), (0, 0), (-5, -2)]

        if self.show_uses:
            for (path, width, legend), pos in zip(imgs, grid):
                pic.node(
                    r"\includegraphics[width=" + width + r"cm]{" + path + r"}", at=pos
                )
                pic.node(legend, at=pos, fill="white", draw=True, thick=True)

    def __iter__(self):
        yield (0, dataclasses.replace(self, show_uses=False))
        yield (1, dataclasses.replace(self, show_uses=True))


@dataclasses.dataclass
class WhoIsWqo:
    examples: list
    answers: List[bool]
    position: Tuple[int, Literal["question", "answer"]] = (0, "question")

    def draw(self, pic):
        pic.node(
            r"Is the following class WQO for induced subgraphs",
            at=(0, 4),
            font=r"\Large\bfseries",
        )

        pic.node(r"YES", at=(-5, 3), color="B4", font=r"\large\bfseries")

        pic.node(r"NO", at=(5, 3), color="A2", font=r"\large\bfseries")

        current, mode = self.position
        bad_answ = 0
        good_answ = 0
        for j in range(current):
            if self.answers[j]:
                good_answ += 1
                xj = -5
                yj = -good_answ * 1.5 + 2
            else:
                bad_answ += 1
                xj = 5
                yj = -bad_answ * 1.5 + 2
            sc = pic.scope(xshift=f"{xj}cm", yshift=f"{yj}cm", scale=0.5)
            self.examples[j].draw(sc)

        sc = pic.scope(scale=1.1)

        if mode == "question":
            color_mode = "A1"
            bg_mode = "white"
        elif mode == "answer" and self.answers[current]:
            color_mode = "B4"
            bg_mode = "B4hint"
        else:
            color_mode = "A2"
            bg_mode = "A2hint"

        sc.draw(
            (-2, 2),
            rectangle((2, -2)),
            thick=True,
            rounded_corners="2mm",
            fill=bg_mode,
            draw=color_mode,
        )

        self.examples[current].draw(sc)

    def __iter__(self):
        yield (0, dataclasses.replace(self, position=(0, "question")))
        yield (1, dataclasses.replace(self, position=(0, "answer")))
        for i in range(1, len(self.examples)):
            yield (1, dataclasses.replace(self, position=(i, "question")))
            yield (1, dataclasses.replace(self, position=(i, "answer")))


@dataclasses.dataclass
class WqoStatus:
    show_theorems: bool = True
    show_remarks: bool = True
    show_words: bool = True
    show_instead: bool = True

    def draw(self, pic):
        pic.node(r"""What is known for WQO?""", at=(0, 4), font=r"\Large\bfseries")

        if self.show_theorems:
            pic.node(
                r"""\textbf{Theorems}  [Ding'92, folklore]
                     \begin{itemize}
                        \item 
                     Bounded tree-depth 
                     \hfill
                     $\implies$ WQO
                        \item 
                     Bounded shrub-depth 
                     \hfill
                     $\implies$ WQO 
                        \item 
                     $m$-partite cograph
                     \hfill
                     $\implies$ WQO 
                     \end{itemize}
                     """,
                at=(-5, 2),
                anchor="north",
                text_width="6cm",
                draw="A5",
                inner_sep="5pt",
                rounded_corners="2mm",
            )

        if self.show_remarks:
            pic.node(
                r"""
                     \textbf{Remark} [folklore]
                     ``Every'' order $(X,\leq)$ is represented
                     as a class of finite graphs
                     $(\mathcal{C}, \subseteq_i)$.

                     $\rightsquigarrow$ Not easy to characterise
                     WQOs inside
                     """,
                at=(5, 2),
                anchor="north",
                text_width="8cm",
                draw="A2",
                inner_sep="5pt",
                rounded_corners="2mm",
            )

        if self.show_words:
            pic.node(
                r"""For \textbf{colored paths}
                     (i.e. finite words), WQO is decidable
                     \begin{itemize}
                     \item for \emph{regular languages}
                     [Atminas, Lozin, Moshkov, '17]
                     \item for languages
                     recognized by \emph{amalgamation systems} (CFG, VASS, etc)
                     and infixes of \emph{morphic words}
                     [Lhote, L, Schütze, arxiv 2025]
                     \end{itemize}""",
                at=(0, -2),
                text_width="15cm",
                inner_sep="5pt",
                rounded_corners="2mm",
                thick=True,
                draw="C3",
            )

        if self.show_instead:
            pic.node(
                r"""\textbf{Instead:} consider \emph{hereditary classes}
                     and \emph{freely colour} them""",
                at=(0, -1),
                text_width="5cm",
                inner_sep="6mm",
                rounded_corners="2mm",
                fill="white",
                thick=True,
                draw="B4",
            )

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self,
                show_theorems=False,
                show_remarks=False,
                show_words=False,
                show_instead=False,
            ),
        )
        for i in range(1, 5):
            yield (
                1,
                dataclasses.replace(
                    self,
                    show_theorems=(i >= 1),
                    show_remarks=(i >= 2),
                    show_words=(i >= 3),
                    show_instead=(i >= 4),
                ),
            )


@dataclasses.dataclass
class LabelledWqo:
    show_finite: bool = True
    show_order: bool = True
    show_conj: bool = True
    show_meme: bool = True

    def draw(self, pic):
        pic.node(r"Labelling Graphs", at=(0, 4), font=r"\Large\bfseries")

        pic.node(
            r"$\mathsf{Label}_X(\mathcal{C})$ ``X-labelled elements of $\mathcal{C}$''",
            at=(-5, 3),
        )
        pic.node(
            r"$\mathcal{C}$ is $(X,\leq)$-WQO $\iff$ $\mathsf{Label}_X(\mathcal{C})$ is WQO",
            at=(5, 3),
        )

        sc = pic.scope(yshift="-1cm")

        sc.style(
            "wqotype",
            fill="white",
            draw=True,
            thick=True,
            rounded_corners="2mm",
            inner_sep="5pt",
            text_width="1.5cm",
            align="center",
            minimum_height="2.2cm",
        )
        sc.style(
            "conj",
            draw="D3",
            text="D3",
            dashed=True,
        )

        if self.show_finite or self.show_order:
            sc.node("WQO", name="W1", at=(-8, 0), wqotype=True, fill="C1hint")
            sc.node(
                r"$\forall X$-WQO (wqo)",
                name="WX",
                at=(8, 0),
                wqotype=True,
                fill="A2hint",
            )

        if self.show_finite:
            sc.node(
                r"$2$-WQO (antichain)",
                name="W2",
                at=(-3, 2),
                wqotype=True,
                fill="B4hint",
            )
            sc.node(
                r"$\forall k$-WQO (finite)",
                name="Wk",
                at=(3, 2),
                wqotype=True,
                fill="C4hint",
            )
            impls = ["W1", "W2", "Wk", "WX"]
            for i, j in zip(impls, impls[1:]):
                sc.draw(f"({i})", topath(f"({j})"), opt="<-", double=True, thick=True)

        if self.show_order:
            sc.node(
                r"$2$-WQO (ordered)",
                name="Wh",
                at=(-3, -2),
                wqotype=True,
                fill="B3hint",
            )
            sc.node(
                r"$\alpha$-WQO (ordinal)",
                name="Wa",
                at=(3, -2),
                wqotype=True,
                fill="C3hint",
            )
            impls = ["W1", "Wh", "Wa", "WX"]
            for i, j in zip(impls, impls[1:]):
                sc.draw(f"({i})", topath(f"({j})"), opt="<-", double=True, thick=True)

            sc.draw("(W2)", topath("(Wh)"), opt="->", double=True, thick=True)

        if self.show_conj:
            sc.draw(
                "(W2)",
                topath("(Wk)", _out="20", _in="160"),
                opt="->",
                double=True,
                thick=True,
                conj=True,
            )
            sc.node("[Pouzet'72]", conj=True, at=(0, 3.2))
            sc.node("[Pouzet]", conj=True, at=(6, 3.2))

            sc.draw(
                "(Wh)",
                topath("(Wa)", _out="-20", _in="-160"),
                opt="->",
                double=True,
                thick=True,
                conj=True,
            )

            sc.draw(
                "(Wk)",
                topath("(WX)", _out="20", _in="90"),
                opt="->",
                double=True,
                thick=True,
                conj=True,
            )
            sc.draw(
                "(Wa)",
                topath("(WX)", _out="-20", _in="-90"),
                opt="->",
                double=True,
                thick=True,
                conj=True,
            )

        if self.show_meme:
            pic.node(
                r"\includegraphics[width=3cm]{./images/cliparts/lwqo-exploding-brain.jpg}",
                at=(0, -1),
            )

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self,
                show_finite=False,
                show_order=False,
                show_conj=False,
                show_meme=False,
            ),
        )
        for i in range(1, 5):
            yield (
                1,
                dataclasses.replace(
                    self,
                    show_finite=(i >= 1),
                    show_order=(i >= 2),
                    show_conj=(i >= 3),
                    show_meme=(i >= 4),
                ),
            )


@dataclasses.dataclass
class LogicAndLabWqo:
    show_struct: bool = True
    show_decomp: bool = True
    show_wqo: bool = True
    show_bdcw: bool = True
    show_relations: bool = True

    def draw(self, pic):
        pic.node(
            r"Relationship with structural graph theory",
            at=(0, 4),
            font=r"\Large\bfseries",
        )

        sc = pic.scope(yshift="0.5cm", xshift="-5cm")

        sc.style(
            "box",
            fill="white",
            draw=True,
            thick=True,
            rounded_corners="2mm",
            inner_sep="5pt",
            text_width="2.5cm",
            align="center",
            minimum_height="1.2cm",
        )
        sc.style(
            "implication",
            thick=True,
            double=True,
            opt="->",
        )
        sc.style(
            "conj",
            draw="D3",
            text="D3",
            dashed=True,
        )

        if self.show_struct:
            sc.node("No restriction", name="allg", at=(0, 2), box=True, fill="A2hint")

            sc.node("Mon. Dependent", name="mondep", at=(0, 0), box=True, fill="B2hint")

            sc.node("Mon. Stable", name="monst", at=(0, -2), box=True, fill="C2hint")

            sc.node("Nowhere Dense", name="nd", at=(0, -4), box=True, fill="D2hint")

        if self.show_decomp:
            sc.node("bd. tree-depth", name="bdtd", at=(5, -4), box=True, fill="D4hint")

            sc.node("bd. shrub-depth", name="bdsd", at=(5, -2), box=True, fill="C4hint")

            sc.node("bd. clique-width", name="bdcw", at=(5, 0), box=True, fill="B4hint")

        if self.show_wqo:
            sc.node(
                r"$\forall X$-WQO", name="xwqo", at=(10, -2), box=True, fill="D3hint"
            )

        structImpls = ["nd", "monst", "mondep", "allg"]
        decompImpls = ["bdtd", "bdsd", "bdcw"]
        xwqoImpls = ["bdsd", "xwqo"]

        twowqoImpls = [
            ("allg", "mondep", False, {"_out": "180", "_in": "180"}),
            ("allg", "bdcw", False, {"_out": "0", "_in": "90"}),
            ("mondep", "bdcw", False, {}),
            ("monst", "bdsd", True, {}),
            ("nd", "bdtd", True, {}),
        ]

        twowqolabels = [
            ("+$2$-wqo", (2.5, 1.7), {}),
            ("[DRT'10]", (2.5, 2.3), {}),
            ("+$2$-wqo", (2.5, -0.3), {}),
            ("[et al.]", (2.5, 0.3), {}),
            ("+$2$-wqo", (2.5, -2.3), {}),
            ("[Cor. Mahlmann]", (2.5, -1.7), {}),
            ("+$2$-wqo", (2.5, -4.3), {}),
            ("[Cor. Ding]", (2.5, -3.7), {}),
            ("+$2$-wqo", (-2.3, 1), {"rotate": "90"}),
            ("[Toruńczyk]", (-2.7, 1), {"rotate": "90"}),
        ]

        if self.show_struct:
            for s, e in zip(structImpls, structImpls[1:]):
                sc.draw(f"({s})", topath(f"({e})"), implication=True)

        if self.show_decomp:
            for s, e in zip(decompImpls, decompImpls[1:]):
                sc.draw(f"({s})", topath(f"({e})"), implication=True)

        if self.show_wqo:
            for s, e in zip(xwqoImpls, xwqoImpls[1:]):
                sc.draw(f"({s})", topath(f"({e})"), implication=True)

        if self.show_relations:
            for txt, pos, props in twowqolabels:
                sc.node(txt, at=pos, font=r"\small", **props)

            for s, e, isConj, props in twowqoImpls:
                sc.draw(
                    f"({s})",
                    topath(f"({e})", **props),
                    draw="C3",
                    conj=(True if not isConj else None),
                    implication=True,
                )

        if self.show_bdcw:
            cc = pic.scope(xshift="5cm", yshift="2cm")
            Cycle(8, 1).draw(cc)

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self,
                show_struct=True,
                show_decomp=False,
                show_wqo=False,
                show_relations=False,
                show_bdcw=False,
            ),
        )
        for i in range(2, 6):
            yield (
                1,
                dataclasses.replace(
                    self,
                    show_struct=(i >= 1),
                    show_decomp=(i >= 2),
                    show_wqo=(i >= 3),
                    show_relations=(i >= 4),
                    show_bdcw=(i >= 5),
                ),
            )


@dataclasses.dataclass
class RelabelFunctions:
    construction_step: int
    show_theorem: bool = True
    show_pb: bool = True

    def draw(self, pic):
        pic.node(
            r"Relabel Functions / Clique-Width / $\mathsf{NLC}_\ell$",
            at=(0, 4),
            font=r"\Large\bfseries",
        )

        def rho(x):
            if x == "a":
                return "b"
            elif x == "b":
                return "c"
            else:
                return "c"

        edges = []
        labels = []
        positions = [(i, j) for i in range(10) for j in range(2)]

        esets = [
            {("a", "b")},
            {("a", "b"), ("a", "c")},
        ] * self.construction_step

        for i, s in enumerate(esets[: self.construction_step]):
            labels = [rho(l) for l in labels]
            for j, l in enumerate(labels):
                if ("a", l) in s:
                    edges.append((i, j))

            labels += "a"

        hg = pic.scope(xshift="3cm")

        for i, l in enumerate(labels):
            p = positions[i]
            hg.node(
                l + r"\strut",
                at=p,
                draw=True,
                fill=(l.upper() + "3hint"),
                name=f"V{i}",
                inner_sep="0pt",
                minimum_height="5pt",
                align="center",
                circle=True,
                text_width="5pt",
            )

        for i, j in edges:
            if (i - j) % 2 == 0:
                hg.draw(f"(V{i})", topath(f"(V{j})", _in="90", _out="90"))
            else:
                hg.draw(f"(V{i})", topath(f"(V{j})"))
        if self.construction_step > 1:
            hg.node(r"Connect : " + str(esets[self.construction_step]), at=(2, -1))
            hg.node(r"Relabel using $\rho$", at=(2, -1.5))

        dc = pic.scope(xshift="-5cm", yshift="3cm")

        dc.node(
            r"Finite Set: $Q = \{ a, b, c\}$",
            at=(0, 0),
        )

        dc.node(
            r"""
                 \begin{equation*}
                    \rho \colon 
                    \begin{cases}
                        a &\mapsto b \\
                        b &\mapsto c \\
                        c &\mapsto c
                    \end{cases}
                 \end{equation*}
                 """,
            at=(0, -3),
            text_width="5cm",
        )
        dc.node(
            r"Relabels : $\mathcal{F} = \{ \mathrm{id}_Q, \rho, \rho^2 \}$", at=(0, -1)
        )

        if self.show_theorem:
            pic.node(
                r"""\textbf{Theorem [DRT'10]}
                     One can decide whether $\mathsf{Relab}(\mathcal{F})$
                     is $2$-wqo. \newline
                     $2$-wqo $\iff$ 
                     $\forall X$-WQO holds on these classes.
                     """,
                at=(0, -2),
                font=r"\large",
                fill="white",
                text_width="8cm",
                inner_sep="4pt",
                draw="A5",
                text="A5",
                thick=True,
                rounded_corners="2mm",
            )

        if self.show_pb:
            pic.node(
                r"""\textbf{Problem:} this is a theorem on 
                     \emph{semigroups} not \emph{languages}.
                     """,
                at=(0, 0),
                draw="A2",
                font=r"\large",
                text_width="8cm",
                inner_sep="4pt",
                fill="white",
                rotate="20",
                thick=True,
                rounded_corners="2mm",
            )

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self, construction_step=0, show_theorem=False, show_pb=False
            ),
        )
        for i in range(1, self.construction_step + 1):
            yield (
                1,
                dataclasses.replace(
                    self, construction_step=i, show_theorem=False, show_pb=False
                ),
            )
        yield (1, dataclasses.replace(self, show_theorem=True, show_pb=False))
        yield (1, dataclasses.replace(self, show_theorem=True, show_pb=True))


@dataclasses.dataclass
class MonoidTree:
    show_lcm: bool = True
    show_mon: bool = True
    show_edg: bool = True

    def draw(self, pic):
        pic.draw(
            (-2.5, 0.5), rectangle((2.5, -0.5)), fill="D4hint", rounded_corners="2mm"
        )
        pic.node("Leaves", at=(0, -0.7))

        pic.node(r"$x$", name="X", at=(-2, 0))

        pic.node(r"$y$", name="Y", at=(2, 0))

        if self.show_lcm:
            pic.node(r"$x \land y$", name="Z", at=(0, 2))

        pic.node(r"root", name="R", at=(0, 4))

        if self.show_mon:
            pic.node(r"$m_x$", at=(-1.3, 1.3))
            pic.node(r"$m_y$", at=(1.3, 1.3))
            pic.node(r"$m_z$", at=(0.5, 3))

        if self.show_lcm:
            pic.draw("(X)", topath("(Z)"), opt="->", decorate=True, decoration="snake")

            pic.draw("(Y)", topath("(Z)"), opt="->", decorate=True, decoration="snake")

            pic.draw("(Z)", topath("(R)"), opt="->", decorate=True, decoration="snake")
        if self.show_edg:
            pic.node(
                r"$E(x,y) \iff (m_x, m_z, m_y) \in P$",
                at=(0, -1.6),
                draw=True,
                fill="D1hint",
            )

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(self, show_lcm=False, show_mon=False, show_edg=False),
        )
        for i in range(1, 4):
            yield (
                1,
                dataclasses.replace(
                    self, show_lcm=(i >= 1), show_mon=(i >= 2), show_edg=(i >= 3)
                ),
            )


@dataclasses.dataclass
class FullSetting:
    mtree: Optional[MonoidTree] = None
    bonus: bool = True
    corol: bool = True
    theor: bool = True

    def draw(self, pic):
        pic.node(
            r"Clique-width (second attempt)",
            at=(0, 4),
            font=r"\Large\bfseries",
        )

        ic = pic.scope(xshift="5cm", yshift="-2cm")
        if self.mtree:
            self.mtree.draw(ic)

        dc = pic.scope(xshift="-9cm", yshift="3cm")

        dc.node(
            r"Finite \textbf{monoid}: $M$",
            anchor="west",
            at=(0, 0),
        )

        dc.node(
            r"Accepting condition : $P \subseteq M^3$",
            anchor="west",
            at=(0, -0.7),
        )

        if self.theor:
            pic.node(
                r"""
                     \textbf{Theorem (new)}
                     Given $M,P$, one can decide if
                     $\mathsf{Relabel}(M,P)$ is $\forall k$-WQO.
                     \newline 
                     For these classes
                     \newline
                     $f(|M|)$-WQO $\iff$ $\forall k$-WQO $\iff$ $\forall X$-WQO.
                     """,
                at=(-5, 1),
                text_width="8cm",
                inner_sep="6pt",
                fill="white",
                thick=True,
                draw="D3",
                rounded_corners="2mm",
            )

        if self.corol:
            pic.node(
                r"""
                     \textbf{Corollary}
                     For classes bounded clique-width
                     \newline
                     $\forall k$-WQO $\iff$ $\forall X$-WQO.
                     """,
                at=(-5, -1),
                text_width="8cm",
                inner_sep="6pt",
                fill="white",
                thick=True,
                draw="C3",
                rounded_corners="2mm",
            )
        if self.bonus:
            pic.node(
                r"""
                     \textbf{Bonus}
                     \begin{itemize}
                     \item reduces to classes of bounded \emph{linear}
                     clique width
                     \item existential transductions of 
                     finite paths
                     \end{itemize}
                     """,
                at=(-5, -3),
                text_width="8cm",
                inner_sep="6pt",
                fill="white",
                thick=True,
                draw="D2",
                rounded_corners="2mm",
            )

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self, mtree=None, bonus=False, corol=False, theor=False
            ),
        )

        for d, t in self.mtree:
            yield (
                d + 1,
                dataclasses.replace(
                    self, mtree=t, bonus=False, corol=False, theor=False
                ),
            )

        for i in range(1, 4):
            yield (
                1,
                dataclasses.replace(
                    self, bonus=(i >= 3), corol=(i >= 2), theor=(i >= 1)
                ),
            )


@dataclasses.dataclass
class NumberedTree:
    show_emb: bool = True
    show_mon: bool = True

    def draw(self, pic):
        for i in range(1, 6):
            pic.node(
                "", name=f"N{i}", at=(0, i), draw=True, circle=True, inner_sep="2pt"
            )

        pic.node("", name=f"N0", at=(0, 0))
        pic.node("", name=f"N6", at=(0, 6))

        for i in range(6):
            ni = f"(N{i})"
            nj = f"(N{i + 1})"
            pic.draw(ni, topath(nj))

        if self.show_emb:
            for i in range(0, 16):
                if i == 0 or i == 15:
                    pic.node("", name=f"M{i}", at=(3, i * 0.4))
                else:
                    pic.node(
                        "",
                        name=f"M{i}",
                        at=(3, i * 0.4),
                        draw=True,
                        circle=True,
                        inner_sep="2pt",
                    )
            for i in range(15):
                ni = f"(M{i})"
                nj = f"(M{i + 1})"
                pic.draw(ni, topath(nj))

        pic.node("$k$", at="(N1)", xshift="-0.3cm")
        pic.node("$k$", at="(N5)", xshift="-0.3cm")
        pic.node("$k$", at="(N3)", xshift="-0.3cm")

        pic.draw(
            r"(-0.2,3.5) -- (-0.2,4.5) node[midway,xshift=3.5em]{$> k$}",
            opt="decorate,decoration={brace,amplitude=5pt,mirror,raise=4ex}",
        )
        pic.draw(
            r"(-0.2,1.5) -- (-0.2,2.5) node[midway,xshift=3.5em]{$> k$}",
            opt="decorate,decoration={brace,amplitude=5pt,mirror,raise=4ex}",
        )

        if self.show_emb:
            pic.node("$k$", at="(M1)", xshift="0.3cm")
            pic.node("$k$", at="(M7)", text="A5", xshift="0.3cm")
            pic.node("$k$", at="(M14)", text="A5", xshift="0.3cm")
            y1 = 7.5 * 0.4
            y2 = 13.5 * 0.4
            y3 = 1.5 * 0.4
            y4 = 6.5 * 0.4
            pic.draw(
                f"(3,{y1}) -- (3,{y2})" + r" node[midway,xshift=3.5em]{$\geq k$}",
                opt="decorate,decoration={brace,amplitude=5pt,mirror,raise=4ex},A5",
            )
            pic.draw(
                f"(3,{y3}) -- (3,{y4})" + r" node[midway,xshift=3.5em]{$\geq k$}",
                opt="decorate,decoration={brace,amplitude=5pt,mirror,raise=4ex},A5",
            )

        if self.show_mon:
            pic.draw((-1, 5), rectangle((-0.9, 3)), fill="B3bg")
            pic.draw((-1, 3), rectangle((-0.9, 1)), fill="B3bg")

            pic.node("$e_2$", at=(-1.3, 2), text="B3")
            pic.node("$e_1$", at=(-1.3, 4), text="B3")
            pic.node("$e_1 e_2 = e_1$", at=(0, -1), text="B3")

        if self.show_emb:
            pic.style("emb", opt="->", thick=True, draw="A5")

            pic.draw("(N1)", topath("(M1)"), emb=True)
            pic.draw("(N3)", topath("(M7)"), emb=True)
            pic.draw("(N5)", topath("(M14)"), emb=True)

    def __iter__(self):
        yield (0, dataclasses.replace(self, show_mon=False, show_emb=False))
        yield (1, dataclasses.replace(self, show_mon=True, show_emb=False))
        yield (1, dataclasses.replace(self, show_mon=False, show_emb=True))
        yield (1, dataclasses.replace(self, show_mon=True, show_emb=True))


@dataclasses.dataclass
class ProofIdea:
    numtree: Optional[NumberedTree] = None
    goals: bool = True
    tools: bool = True
    problem: bool = True

    def draw(self, pic):
        pic.node(
            r"How does one prove such statements?",
            at=(0, 4),
            font=r"\Large\bfseries",
        )

        if self.goals:
            pic.node(
                r"""
                     \textbf{Part 1:} Order tree-decompositions s.t.
                     $I \colon \mathsf{Trees} \to \mathsf{Graphs}$
                     is \emph{order preserving}
                     """,
                anchor="west",
                at=(-9, 2),
                text_width="6cm",
            )

            pic.node(
                r"``product preserving'' tree embeddings",
                anchor="west",
                at=(-9, 1.2),
                text="B1",
            )

            pic.node(
                r"""
                     \textbf{Part 2:} Order tree-decompositions using
                     a WQO.
                     """,
                anchor="west",
                at=(-9, 0),
                text_width="6cm",
            )
            pic.node(
                r"usual tree embeddings (Kruskal)",
                anchor="west",
                at=(-9, -0.8),
                text="B1",
            )

            pic.node(
                r"""
                     \textbf{Goal} do (1) and (2)
                     simultaneously.
                     """,
                anchor="west",
                at=(-9, -2),
                text_width="6cm",
            )

        if self.tools:
            pic.node(
                r"Forward Ramseyan Splits \newline [Colcombet'07]",
                anchor="east",
                text_width="5cm",
                text="A3",
                at=(9, 2),
            )
            pic.node(
                r"Gap Embedding Relation \newline [Dershowitz and Tzameret'03]",
                anchor="east",
                text="A5",
                text_width="5cm",
                at=(9, 0),
            )

            pic.node(
                r"Both label nodes with elements from $\{1,...,n\}$",
                anchor="east",
                text_width="5cm",
                at=(9, -2),
            )

        if self.numtree:
            sc = pic.scope(xshift="-1.5cm", yshift="-3cm")
            self.numtree.draw(sc)

        if self.problem:
            pic.node(
                r"""\textbf{Obstacle:} $<$ is not $\leq$
                     \newline 
                     Depends on $P$ \newline
                     (as one would expect)
                     """,
                at=(0, 0),
                inner_sep="5pt",
                rounded_corners="2mm",
                text_width="5cm",
                font=r"\Large",
                fill="A2hint",
                draw="A2",
            )

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self, numtree=None, tools=False, problem=False, goals=False
            ),
        )
        yield (
            1,
            dataclasses.replace(
                self, numtree=None, tools=False, problem=False, goals=True
            ),
        )
        yield (
            1,
            dataclasses.replace(
                self, numtree=None, tools=True, problem=False, goals=True
            ),
        )
        for d, t in self.numtree:
            yield (
                1 + d,
                dataclasses.replace(
                    self, numtree=t, problem=False, tools=True, goals=True
                ),
            )

        yield (1, dataclasses.replace(self, tools=True, problem=True, goals=True))


@dataclasses.dataclass
class FinalSlide:
    def draw(self, pic):
        pic.node(
            r"What's next?",
            at=(0, 4),
            font=r"\Large\bfseries",
        )

        codelabel = drawing_to_node(LabelledWqo(), 6)
        codelogic = drawing_to_node(LogicAndLabWqo(), 6)

        pic.node(
            codelabel, at=(-5, 2), draw=True, rounded_corners="2mm", inner_sep="5pt"
        )
        pic.node(
            codelogic, at=(-5, -2), draw=True, rounded_corners="2mm", inner_sep="5pt"
        )

        pic.node(
            r"""
                 \textbf{$2$-WQO:}
                 \begin{itemize}
                    \item $2$-WQO (antichain) $\implies$ $\forall k$-WQO
                    \item $2$-WQO (order)     $\implies$ $\forall k$-WQO
                    \item Relationship to monadically dependent classes
                    \item ``Successor-free graphs''
                 \end{itemize}
                 """,
            text="A5",
            text_width="8cm",
            at=(5, -1),
        )

        pic.node(
            r"""
                 \textbf{WQO:}
                 \begin{itemize}
                    \item Decide WQO for relabel functions
                    \item Decide WQO given excluded patterns
                 \end{itemize}
                 """,
            text_width="8cm",
            text="A4",
            at=(5, -3),
        )

        pic.node(
            r"""
                     \textbf{Theorem}
                     Given $M,P$, one can decide if
                     $\mathsf{Relabel}(M,P)$ is \textcolor{A2}{$\forall k$-WQO}.
                     \newline 
                     For these classes
                     \newline
                     \textcolor{A2}{$f(|M|)$-WQO} $\iff$ $\forall k$-WQO $\iff$ $\forall X$-WQO.
                     """,
            at=(5, 2),
            text_width="8cm",
            inner_sep="4pt",
            fill="D4hint",
            thick=True,
            draw="D4",
            rounded_corners="2mm",
        )

    def __iter__(self):
        yield (0, self)


if __name__ == "__main__":
    tc = TableOfColors()
    tt = TitleFrame()

    cfg = PresConfig(
        title="Well-Quasi-Orders and Logic on Graphs",
        author="Aliaume Lopez",
        location="Les Houches",
        date="2025-05-29",
        draft=False,
    )

    hg = HalfGraph(3, 3)

    ws = WqoSeq(
        points=[
            r"$x_0$",
            r"$x_1$",
            r"$x_2$",
            r"$\dots$",
            r"$x_i$",
            r"$\dots$",
            r"$x_j$",
            r"$\dots$",
        ],
        pair=(4, 6),
    )

    wqo101 = WQO101(ws)

    wwqo = WhoIsWqo(
        [
            Path(4),
            Cycle(6, 1),
            HalfGraph(4, 4),
            HalfGraph(
                4,
                4,
                edgesProps={
                    ((x, i + 1), (y, i)): {"draw": "red", "thick": True}
                    for x in ["top", "bot"]
                    for y in ["top", "bot"]
                    for i in range(4)
                    if x != y
                },
            ),
            Path(4, verticesProps=[{"fill": "A4"}, {}, {}, {"fill": "A4"}]),
            HalfGraph(
                4,
                4,
                edgesProps={
                    ((x, i + 1), (y, i)): {"draw": "red", "thick": True}
                    for x in ["top", "bot"]
                    for y in ["top", "bot"]
                    for i in range(4)
                    if x != y
                },
                verticesProps={
                    ("bot", 0): {"fill": "A4"},
                    ("bot", 3): {"fill": "A4"},
                },
            ),
            HalfGraph(
                4,
                4,
                verticesProps={
                    ("bot", 0): {"fill": "A4"},
                    ("bot", 3): {"fill": "A4"},
                },
            ),
        ],
        [True, False, True, True, False, False, True],
    )

    st = WqoStatus()

    hgg = SequenceOfHG.from_dims([(4, 3), (2, 5), (3, 3), (3, 7)], 2, 4)

    frames_list = [
        tt,
        wqo101,
        wwqo,
        st,
        LabelledWqo(),
        LogicAndLabWqo(),
        RelabelFunctions(8),
        FullSetting(mtree=MonoidTree()),
        ProofIdea(numtree=NumberedTree()),
        FinalSlide(),
    ]

    frames = Sequential(frames_list, pos=0)

    cfg.preview(frames)
