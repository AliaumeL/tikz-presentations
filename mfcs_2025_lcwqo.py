#!/usr/bin/env python3
#
# Aliaume LOPEZ
#

from tikz import *

import tikz_presentations_aliaume as tpa
import tikz_presentations_aliaume.components as tpacmp

from tikz_presentations_aliaume.components.typography import *
from tikz_presentations_aliaume.components.utils import *
from tikz_presentations_aliaume.components.graphs import *

import yaml

import bibtexparser

import math

import random
import dataclasses
from dataclasses import dataclass, field
from typing import Literal, Generator, Callable, List, Union, Tuple, Optional


@dataclass
class Vertex:
    name: str
    at: Tuple[float, float] = (0, 0)
    label: Optional[str] = None
    color: str = "white"
    _extra: dict = field(default_factory=dict)

    def draw(self, pic: Picture):
        pic.node(
            self.label or "",
            at=self.at,
            circle=True,
            inner_sep="2pt",
            draw=True,
            name=self.name,
            fill=self.color,
            **self._extra,
        )

    def __iter__(self):
        yield (0, self)


@dataclass
class Edge:
    source: Union[str, Vertex]
    target: Union[str, Vertex]
    directed: bool = False
    label: Optional[str] = None
    color: str = "black"
    _extra: dict = field(default_factory=dict)

    @property
    def source_name(self) -> str:
        return self.source.name if isinstance(self.source, Vertex) else self.source

    @property
    def target_name(self) -> str:
        return self.target.name if isinstance(self.target, Vertex) else self.target

    def draw(self, pic: Picture):
        if self.directed:
            self._extra["->"] = "true"
        pic.draw(
            f"({self.source_name})",
            topath(f"({self.target_name})"),
            label=self.label or "",
            color=self.color,
            **self._extra,
        )

    def __iter__(self):
        yield (0, self)


@dataclass
class Graph:
    name: str
    vertices: list[Vertex]
    edges: list[Edge]

    @staticmethod
    def cycle(name: str, size: int, radius: float = 1.0) -> "Graph":
        vertices = [
            Vertex(
                name=f"{name}v{i}",
                at=(
                    radius * math.cos(2 * math.pi * i / size),
                    radius * math.sin(2 * math.pi * i / size),
                ),
            )
            for i in range(size)
        ]
        edges = [
            Edge(source=vertices[i], target=vertices[(i + 1) % size])
            for i in range(size)
        ]
        return Graph(name, vertices, edges)

    @staticmethod
    def path(name: str, length: int, spacing: float = 1.0) -> "Graph":
        vertices = [
            Vertex(name=f"{name}v{i}", at=(i * spacing, 0)) for i in range(length)
        ]
        edges = [
            Edge(source=vertices[i], target=vertices[i + 1]) for i in range(length - 1)
        ]
        return Graph(name, vertices, edges)

    @staticmethod
    def clique(name: str, size: int, radius: float = 1.0) -> "Graph":
        vertices = [
            Vertex(
                name=f"{name}v{i}",
                at=(
                    radius * math.cos(2 * math.pi * i / size),
                    radius * math.sin(2 * math.pi * i / size),
                ),
            )
            for i in range(size)
        ]
        edges = [
            Edge(source=vertices[i], target=vertices[j])
            for i in range(size)
            for j in range(i + 1, size)
        ]
        return Graph(name, vertices, edges)

    def draw(self, pic: Picture):
        for v in self.vertices:
            v.draw(pic)

        for e in self.edges:
            e.draw(pic)

    def map(
        self, vfunc: Callable[[int, Vertex], Vertex], efunc: Callable[[int, Edge], Edge]
    ) -> "Graph":
        new_vertices = [vfunc(i, v) for (i, v) in enumerate(self.vertices)]
        new_edges = [efunc(i, e) for (i, e) in enumerate(self.edges)]
        return Graph(self.name, new_vertices, new_edges)

    def __iter__(self):
        yield (0, self)


def example_graph_two_triangles():
    """
    a rectangle with a diagonal edge + outer diagonal edge
    """
    v1 = Vertex(name="v1", at=(-1, 0))
    v2 = Vertex(name="v2", at=(1, 0))
    v3 = Vertex(name="v3", at=(0, 0.5))
    v4 = Vertex(name="v4", at=(0, -0.5))

    e1 = Edge(source="v1", target="v2", _extra={"_in": "90", "_out": "90"})
    e2 = Edge(source="v2", target="v3")
    e3 = Edge(source="v3", target="v4")
    e4 = Edge(source="v4", target="v1")
    e5 = Edge(source="v1", target="v3")
    e6 = Edge(source="v2", target="v4")

    return Graph("ttrig", [v1, v2, v3, v4], [e1, e2, e3, e4, e5, e6])


@dataclass
class Embedding:
    embedding: list[Edge]

    def draw(self, pic: Picture):
        for e in self.embedding:
            e.draw(pic)

    def __iter__(self):
        yield (0, self)


@dataclass
class LotsOfGraphsBackGround:
    """
    Draws a background with many cycles,
    cliques and paths and half graphs 
    with clipping to the frame width and height 
    """
    graphs : list[tuple[int,int,Graph]] = field(default_factory=list)

    @staticmethod
    def from_random():
        """ Places randomly graphs to fill the background 
        """
        graphs = []
        for i in range(-10, 11, 2):
            for j in range(-5, 6, 2):
                if random.random() < 0.5:
                    g = Graph.cycle(f"cycle_{i}_{j}", random.randint(3, 8), radius=0.5)
                elif random.random() < 0.5:
                    g = Graph.clique(f"clique_{i}_{j}", random.randint(3, 8), radius=0.5)
                else:
                    g = Graph.path(f"path_{i}_{j}", random.randint(2, 4), spacing=0.5)
                graphs.append((i, j, g))
        return LotsOfGraphsBackGround(graphs=graphs)


    def draw(self, pic: Picture):
        LL = (-10, -5)
        UR = (10,   5)
        pic.path(LL, rectangle(UR), clip=True)
        for i, j, g in self.graphs:
            s = pic.scope(xshift=f"{i}cm", yshift=f"{j}cm")
            g.draw(s)
        
    def __iter__(self):
        yield (0, self)

@dataclass
class TitleFrame:
    
    pres_by : bool = False

    def draw(self, pic: Picture):
        sc = pic.scope(opacity=0.1)

        LotsOfGraphsBackGround.from_random().draw(sc)


        Typography(
            text=[
                "Labelled Well Quasi Ordered Classes",
                "of",
                "Bounded Linear Clique-Width",
            ],
            color="A4",
            at=(0, 3),
        ).draw(pic)

        Typography(
            text=[
                "Aliaume Lopez",
            ],
            level=2,
            color="A1",
            at=(0, 0),
        ).draw(pic)

        if self.pres_by: 
            Typography(
                text=["Presented by Maël Dumas"],
                level=2,
                color="A2",
                at=(0, -1.25 ),
            ).draw(pic)

        Typography(text="University of Warsaw", level=3, color="A1", at=(0, -0.5)).draw(
            pic
        )

        Typography(
            text=["MFCS'2025", "Warsaw, Poland"], level=4, color="A1", at=(0, -2)
        ).draw(pic)

        Image(
            path="images/institutions/university_of_warsaw.pdf",
            width=2.5,
            at=(-5, -2.5),
        ).draw(pic)

        Image(
            path="images/institutions/zigmunt_zaleski_stitching.png",
            width=2.5,
            at=(5, -2.5),
        ).draw(pic)

    def __iter__(self):
        yield (0, self)
        yield (1, dataclasses.replace(self, pres_by=True))


@dataclass
class InducedGraph:
    """Draws two graphs
    and an embedding
    between the nodes.
    """

    graphG: Optional[Graph] = None
    graphH: Optional[Graph] = None
    embedding: Optional[Embedding] = None

    show_embed: bool = False
    show_finlab: bool = False
    show_ordlab: bool = False

    def draw(self, pic):
        Typography(
            text="Graphs and Induced Subgraphs",
            level=1,
            color="Prune",
            anchor="west",
            align="left",
            at=(-9, 4),
        ).draw(pic)
        if not (self.graphG is None and self.graphH is None):
            Typography(
                text=r"$\triangleright$ Graphs are undirected, without self-loops",
                level=5,
                color="A1",
                anchor="west",
                align="left",
                at=(-9, 3),
            ).draw(pic)
        if self.embedding is not None:
            Typography(
                text=r"$\triangleright$ Embeddings represent subsets of \emph{vertices}",
                level=5,
                color="A1",
                anchor="west",
                align="left",
                at=(-9, 2.5),
            ).draw(pic)
        if self.show_finlab:
            Typography(
                text=r"$\triangleright$ Vertices can be labelled by a finite set",
                level=5,
                color="A1",
                anchor="west",
                align="left",
                at=(-9, 2),
            ).draw(pic)
        if self.show_ordlab:
            Typography(
                text=r"$\triangleright$ Vertices can be labelled using $(X, \leq)$",
                level=5,
                color="A1",
                anchor="west",
                align="left",
                at=(-9, 2),
            ).draw(pic)

        if self.graphG is not None:
            s1 = pic.scope(xshift="-3cm")
            self.graphG.draw(s1)
            Typography(text="$G$", level=4, at=(0, -1.5), color="A1").draw(s1)

        if self.graphH is not None:
            s2 = pic.scope(xshift="3cm")
            Typography(text="$H$", level=4, at=(0, -1.5), color="A1").draw(s2)
            self.graphH.draw(s2)

        if self.embedding is not None:
            self.embedding.draw(pic)
            Typography(
                text="$h$",
                level=4,
                at=(0, 2),
                color="C2",
            ).draw(pic)
            Typography(
                text=r"""
                      $(x,y) \in E(G)
                      \iff
                      (h(x), h(y)) \in E(H)$""",
                at=(0, -2.5),
                level=5,
                color="C2",
            ).draw(pic)

        lab = ""
        if self.show_finlab:
            lab = r"$\text{label}(x) = \text{label}(h(x))$"
        elif self.show_ordlab:
            lab = r"$\text{label}(x) \leq \text{label}(h(x))$"

        if self.show_finlab or self.show_ordlab:
            Typography(text=lab, at=(0, -3), level=5, color="B2").draw(pic)

    def __iter__(self):
        yield (0, self)

        current = self

        g1 = Graph.cycle("g1", 3, radius=0.5)
        g2 = example_graph_two_triangles()

        current = dataclasses.replace(current, graphH=g2)

        yield (1, current)

        g2col = g2.map(
            lambda i, v: v if i == 3 else dataclasses.replace(v, color="A1"),
            lambda i, e: e,
        )
        current = dataclasses.replace(current, graphH=g2col)

        yield (2, current)

        current = dataclasses.replace(current, graphG=g1)
        yield (2, current)

        def bending(source):
            if source != 2:
                return "bend left"
            else:
                return "bend right"

        emb = Embedding(
            [
                Edge(
                    source=g1.vertices[i],
                    target=g2col.vertices[i],
                    directed=True,
                    color="C2",
                    _extra={bending(i): "30", "ultra thick": "true"},
                )
                for i in range(3)
            ]
        )
        current = dataclasses.replace(current, embedding=emb)
        yield (2, current)
        current = dataclasses.replace(current, graphH=g2)
        yield (2, current)
        # give few other embeddings
        # 1 -> 4, 2 -> 3, 3 -> 1
        # 1 -> 2, 2 -> 3, 3 -> 4
        for corr in [[4, 3, 1], [2, 3, 4], [2, 1, 3]]:
            emb = Embedding(
                [
                    Edge(
                        source=g1.vertices[i],
                        target=g2.vertices[corr[i] - 1],
                        directed=True,
                        color="C2",
                        _extra={bending(i): "30", "ultra thick": "true"},
                    )
                    for i in range(3)
                ]
            )
            current = dataclasses.replace(current, embedding=emb)
            yield (3, current)

        # now add labels
        g1lbl = g1.map(
            lambda i, v: dataclasses.replace(v, color="B2") if i == 2 else v,
            lambda i, e: e,
        )
        g2lbl = g2.map(
            lambda i, v: dataclasses.replace(v, color="B2") if i == 3 else v,
            lambda i, e: e,
        )
        current = dataclasses.replace(
            current, graphG=g1lbl, graphH=g2lbl, show_finlab=True, show_ordlab=False
        )
        yield (1, current)

        emb = Embedding(
            [
                Edge(
                    source=g1lbl.vertices[i],
                    target=g2lbl.vertices[j - 1],
                    directed=True,
                    color="C2",
                    _extra={bending(i): "30", "ultra thick": "true"},
                )
                for (i, j) in zip(range(3), [1, 3, 4])
            ]
        )

        current = dataclasses.replace(current, embedding=emb)
        yield (2, current)

        # now change the labels to be ordered
        g1ord = g1lbl.map(
            lambda i, v: dataclasses.replace(v, color="white", label=f"{i}\\strut"),
            lambda i, e: e,
        )

        g2ord = g2lbl.map(
            lambda i, v: dataclasses.replace(
                v, color="white", label=f"{(i % 2) + 2}\\strut"
            ),
            lambda i, e: e,
        )

        current = dataclasses.replace(
            current, graphG=g1ord, graphH=g2ord, show_finlab=False, show_ordlab=True
        )
        yield (2, current)


@dataclass
class GraphsAndInducedGraphs:
    """
    1. creates a graph
    2. shows an induced subgraph
    3. shows the embedding
    4. adds labels to the graphs
    5. changes the embedding to work again
    6. changes labels to be numbers
    """

    pass


def all_labels(vertices: int, labels: int) -> list[list[int]]:
    """
    Generates all possible labelings of `vertices` vertices
    with `labels` distinct labels.
    """
    from itertools import product

    return [
        list(labeling) for labeling in product(range(1, labels + 1), repeat=vertices)
    ]


@dataclass
class FreelyLabeled:
    """
    1. draws a triangle.
    2. Selects labels { 1, 2, 3 }
    3. Draws all freely labeled triangles (up to iso)
    """

    graph: Optional[Graph] = None
    cols: Optional[list[str]] = None

    def draw(self, pic):
        Typography(
            text="Freely Labeled Graphs",
            level=1,
            color="Prune",
            anchor="west",
            align="left",
            at=(-9, 4),
        ).draw(pic)

        Typography(
            text=r"$\mathsf{Label}_X(\mathcal{C})$ is the collection of all possible $X$-labellings of graphs in $\mathcal{C}$",
            level=5,
            color="A1",
            anchor="west",
            align="left",
            at=(-9, 3),
        ).draw(pic)

        if self.cols is not None:
            colored_bullets = ", ".join(
                (
                    f"\\textcolor{{{c}}}{{\\textbullet}}"
                    for i, c in enumerate(self.cols, start=1)
                )
            )
            Typography(
                text=r"""$\mathcal{C} = \{ C_3 \}$ 
                          and $X = \{ """
                + colored_bullets
                + r""" \}$""",
                at=(-9, 2.5),
                level=5,
                color="A1",
                anchor="west",
                align="left",
            ).draw(pic)

        if self.graph is not None and self.cols is None:
            self.graph.draw(pic)

        if self.graph is not None and self.cols is not None:
            n = len(self.graph.vertices)
            m = len(self.cols)
            for i, labels in enumerate(all_labels(n, m)):
                self.graph.map(
                    vfunc=lambda k, v: dataclasses.replace(
                        v, name=v.name + f"copy{i}", color=f"{self.cols[labels[k] - 1]}"
                    ),
                    efunc=lambda k, e: dataclasses.replace(
                        e,
                        source=e.source_name + f"copy{i}",
                        target=e.target_name + f"copy{i}",
                    ),
                ).draw(
                    pic.scope(
                        xshift=f"{(i // 3) * 2 - 8}cm", yshift=f"{(i % 3) * -2 + 1}cm"
                    )
                )

    def __iter__(self):
        yield (0, self)
        current = self
        g = Graph.cycle("triangle", 3, radius=1.0)
        current = dataclasses.replace(current, graph=g)
        yield (1, current)
        gp = Graph.cycle("triangle", 3, radius=0.5)
        current = dataclasses.replace(current, graph=gp, cols=["B2", "D3", "A4"])
        yield (1, current)


@dataclass
class GoodSequence:
    sequence: list[Optional[tuple[str, Graph]]] = field(default_factory=list)
    increasing: Optional[tuple[int, int]] = None
    embedding: Optional[Embedding] = None

    def draw(self, pic: Picture):
        for i, g in enumerate(self.sequence):
            if g is None:
                Typography(text="∅", at=(i * 2, 0), color="A1").draw(pic)
            else:
                g.draw(pic.scope(xshift=f"{i * 2}cm", yshift=0))
                Typography(text=f"G{i + 1}", at=(i * 2, -1.5), color="A1").draw(pic)

        if self.increasing is not None:
            Typography(
                text="Increasing Pair", at=(self.increasing[0] * 2, 1.5), color="A4"
            ).draw(pic)
            pic.draw(
                f"(G{self.increasing[0] + 1})",
                topath(f"(G{self.increasing[1] + 1})"),
                color="A4",
                label="",
            )

        if self.embedding is not None:
            self.embedding.draw(pic)
            Typography(text="Embedding", at=(0, -2.5), color="A4").draw(pic)

    def __iter__(self):
        yield (0, self)


@dataclass
class WellQuasiOrders:
    """
    1. title of the slide
    2. shows the definition of a good sequence
    3. shows an example for paths
    4. shows non example with cycles
    5. defines 'labelled-wqo' as
       wqo for any set of labels
       (wqo set)
    6. show that paths are not lwqo (not even with 2 labels)
    7. show that cliques are lwqo (they are multisets)
    """

    show_sequence: bool = False
    show_wqo: bool = False
    show_non_wqo: bool = False
    show_lwqo: bool = False
    show_exs: bool = False

    def draw(self, pic: Picture):
        Typography(
            text="Well Quasi Ordered Clases of Graphs",
            level=1,
            color="Prune",
            anchor="west",
            align="left",
            at=(-9, 4),
        ).draw(pic)

        if self.show_sequence:
            Typography(
                text=r""" $\triangleright$
                A sequence of graphs $G_1, G_2, \ldots$ is a \textbf{good sequence} if
                there exists a pair $i < j$ such that $G_i$ \emph{embeds} in $G_j$.
                """,
                level=5,
                color="A1",
                anchor="west",
                align="left",
                at=(-9, 3),
            ).draw(pic)

        if self.show_wqo:
            Typography(
                text=r""" $\triangleright$
                A class is \textbf{well-quasi-ordered} (wqo) if
                every sequence is a \emph{good sequence}.
                """,
                level=5,
                color="A1",
                anchor="west",
                align="left",
                at=(-9, 2.5),
            ).draw(pic)

        if self.show_lwqo:
            Typography(
                text=r""" $\triangleright$
                A class $\mathcal{C}$ is $X$-\textbf{well-quasi-ordered} ($X$-wqo) if
                $\mathsf{Label}_X(\mathcal{C})$ is wqo.
                """,
                level=5,
                color="A1",
                anchor="west",
                align="left",
                at=(-9, 2),
            ).draw(pic)

        if self.show_sequence:
            seq = ["0", "1", "2", None, "i", None, "j", None]
            sc = pic.scope(xshift="-7cm", yshift="-0.5cm")
            for i, s in enumerate(seq):
                if s is None:
                    sc.node(r"$\cdots$", at=(i * 2, 0))
                else:
                    sc.node(r"$G_{%s}$" % s, at=(i * 2, 0), name=f"g{i}")

                    if self.show_non_wqo:
                        ci = Graph.cycle(f"g{i}graph", (i + 3), radius=0.5)
                        ci.draw(sc.scope(xshift=f"{i * 2}cm", yshift="1cm"))

                    if self.show_wqo:
                        pi = Graph.path(f"g{i}graph", (i + 1), spacing=0.5)
                        pi.draw(sc.scope(xshift=f"{i * 2}cm", yshift="1cm"))

            if self.show_wqo:
                pic.draw("(g4)", topath("(g6)"), _in="-90", _out="-90", **{"->": True})
                Typography(text="Good Sequence",
                           at=(3, 2),
                           level=1,
                           color="A5",
                           _extra={"draw": "A5", "fill": "A5hint", "rounded_corners": "2mm"}
                           ).draw(pic)

            if self.show_non_wqo:
                Typography(text="Bad Sequence",
                           at=(3, 2),
                           level=1,
                           color="A2",
                           _extra={"draw": "A2", "fill": "A2hint", "rounded_corners": "2mm"}
                           ).draw(pic)

        if self.show_exs:
            Statement(
                name="Examples",
                text=r"""Cycles (NO), Paths (YES), Colored paths (NO), Cliques (YES)""",
                at=(-9, -3),
            ).draw(pic)

    def __iter__(self):
        current = self
        yield (0, current)
        current = dataclasses.replace(current, show_sequence=True)
        yield (1, current)
        current = dataclasses.replace(current, show_non_wqo=True)
        yield (1, current)
        current = dataclasses.replace(current, show_wqo=True, show_non_wqo=False)
        yield (1, current)
        current = dataclasses.replace(current, show_lwqo=True)
        yield (1, current)
        current = dataclasses.replace(current, show_exs=True)
        yield (1, current)


@dataclass
class WhyDoWeCare:
    """
    1. title
    2. well-quasi-ordered classes
       -> fpt membership
       -> decidable properties (rewriting)
       -> appear in a lot of conjectures
    3. usually, one considers `minor` relation,
       and uses Robertson and Seymour's
       graph minor theorem, but sometimes we are
       interested in subgraphs!
    """

    show_uses: bool = False

    def draw(self, pic: Picture):
        Typography(
            text="Why care about Well-Quasi-Ordered Classes?",
            level=1,
            color="Prune",
            anchor="west",
            align="left",
            at=(-9, 4),
        ).draw(pic)

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
        yield (0, self)
        current = self
        current = dataclasses.replace(current, show_uses=True)
        yield (1, current)


@dataclass
class PropertiesInclusions:
    """
    bounded tree-depth
    bounded clique-width
    wqo
    2-wqo
    label-wqo
    wqo-wqo

    inclusions are
    tree-depth -> clique
    tree-depth -> wqo-wqo -> label-wqo -> 2-wqo -> wqo

    draw the properties as rectangles
    included in one another
    """

    show_props: list[str] = field(default_factory=list)
    show_classes: list[str] = field(default_factory=list)
    show_conj : bool = False

    def draw(self, pic: Picture):
        Typography(
            text="Inclusions of Properties",
            level=2,
            color="Prune",
            anchor="west",
            align="left",
            at=(1, 4),
        ).draw(pic)

        scope = pic.scope(yshift="-3cm", xshift="1cm")

        properties = [
            (
                "Tree-depth",
                "D2",
                (0, 0),  # lower left corner of the rectangle
                (3, 1),  # upper right corner of the rectangle
            ),
            ("Clique-width", "C2", (0, 0), (8, 2)),
            (r"$\forall X$, $X$-wqo", "A4", (0, 0), (3.5, 3)),
            (r"$\forall k$, $k$-wqo", "B4", (0, 0), (4, 4)),
            ("2-wqo", "C4", (0, 0), (4.5, 5)),
            ("Wqo", "D4", (0, 0), (5, 6)),
        ]

        properties = [p for p in properties if p[0] in self.show_props]

        if self.show_conj:
            # remove last and penultimate properties
            # increase the height of clique width
            del properties[-2]
            del properties[-2]
            properties[1] = (properties[1][0], properties[1][1], properties[1][2], (8, 4.5))
            tmp = properties[1]
            properties[1] = properties[2]
            properties[2] = tmp


        for prop, color, ll, ur in reversed(properties):
            scope.draw(
                ll,
                rectangle(ur),
                color=color,
                draw=None,
                fill=f"{color}hint",
                rounded_corners="2mm",
            )
        for prop, color, ll, ur in reversed(properties):
            scope.draw(ll, rectangle(ur), color=color, rounded_corners="2mm")
        for i, (prop, color, ll, ur) in enumerate(properties):
            mid_upper = (ll[0] + (ur[0] - ll[0]) / 2, ur[1])
            Typography(
                text=prop,
                at=mid_upper,
                level=5,
                width="2cm",
                _extra={
                    "draw": color,
                    "fill": f"{color}hint",
                    "rounded_corners": "2mm",
                },
            ).draw(scope)

        def midway_of(a, b):
            return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

        classes = [
            # name, point_pos, legend_pos
            ("Independent Sets", (1.5, 0.5), (0, -0.5)),
            ("Cliques", (1.75, 1.5), (-0.75, 1)),
            ("Paths", (4.75, 1), (2, -0.5)),
            ("Cycles", (6.5, 1), (5, -0.5)),
        ]

        classes = [c for c in classes if c[0] in self.show_classes]

        for i, (name, point_pos, legend_pos) in enumerate(classes):
            scope.node(
                "",
                at=point_pos,
                circle=True,
                inner_sep="1pt",
                draw=True,
                fill="A1",
                color="A1",
                name=f"cls{i}point",
            )
            Typography(
                text=name,
                level=6,
                at=legend_pos,
                color="A1",
                _extra={"name": f"cls{i}label"},
            ).draw(scope)
            scope.draw(
                f"(cls{i}label)",
                topath(f"(cls{i}point)"),
                **{
                    "->": "true",
                    "bend left": "20",
                    "ultra thick": "true",
                    "color": "A1",
                },
            )


@dataclass
class RelatedWork:
    """
    1. Pouzet's conjecture for hereditary classes
    2. Ding'92: bounded tree-depth => label-wqo,
    but the converse not true (cliques)
    3. DRT'10:
        [conj]: 2-wqo => bounded clique-width
        [thm] : for *some* classes of bounded clique-width,
                pouzet is true!
    """

    inclusions: Optional[PropertiesInclusions] = None
    show_pouzet: bool = False
    show_ding: bool = False
    show_drt: bool = False

    def draw(self, pic):
        Typography(
            text="Related Work",
            level=1,
            color="Prune",
            anchor="west",
            align="left",
            at=(-9, 4),
        ).draw(pic)

        if self.show_pouzet:
            Statement(
                name="Conjecture [Pouzet'72]",
                text=r"$2$-wqo $\implies$ $\forall k \in \mathbb{N}$, $k$-wqo",
                at=(-9, 3),
                border=True,
                color="B4",
            ).draw(pic)

            Statement(
                name="Conjecture [Pouzet'72]",
                text=r"$\forall k \in \mathbb{N}$, $k$-wqo $\implies$ $\forall X$, $X$-wqo",
                at=(-9, 1.5),
                border=True,
                color="B4",
            ).draw(pic)

        if self.show_ding:
            Statement(
                name="Theorem [Ding'92]",
                text=r"Bounded tree-depth implies $\forall X$, $X$-wqo",
                at=(-9, 0),
                color="A5",
            ).draw(pic)

            Statement(
                text="the converse fails (ex: cliques)",
                at=(-3, -0.5),
                width=2.5,
                border=True,
                color="A2",
            ).draw(pic)

        if self.show_drt:
            Statement(
                name="Theorem [Daligault, Rao, Thomassé'10]",
                at=(-9, -2),
                width=6.5,
                text=r"For \textbf{some classes} of bounded clique-width,\newline both conjectures hold",
                color="A5",
            ).draw(pic)

            Statement(
                name="Conjecture [Daligault, Rao, Thomassé'10]",
                at=(-9, -3.5),
                width=6.5,
                border=True,
                text=r"$2$-wqo $\implies$ bounded clique-width",
                color="B4",
            ).draw(pic)

        if self.inclusions is not None:
            self.inclusions.draw(pic)

    def __iter__(self):
        current = self
        yield (0, current)
        incls = PropertiesInclusions()
        props = ["Wqo", "2-wqo", r"$\forall k$, $k$-wqo", r"$\forall X$, $X$-wqo"]
        clss = []
        incls = dataclasses.replace(incls, show_props=props, show_classes=clss)
        current = dataclasses.replace(current, inclusions=incls)
        yield (1, current)
        current = dataclasses.replace(current, show_pouzet=True)
        yield (1, current)
        current = dataclasses.replace(current, show_ding=True)
        props.append("Tree-depth")
        clss.append("Cliques")
        clss.append("Independent Sets")
        yield (1, current)
        current = dataclasses.replace(current, show_drt=True)
        props.append("Clique-width")
        clss.append("Paths")
        clss.append("Cycles")
        yield (1, current)
        incls = dataclasses.replace(incls, show_conj=True)
        current = dataclasses.replace(current, inclusions=incls)
        yield (1, current)


@dataclass
class NLCExpr:
    def to_graph(self) -> Graph:
        """
        Converts the NLC expression to a Graph.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def draw_tree(
        self, root_pos: tuple[float, float], width: float, pic: Picture, name: str
    ):
        """Draws the NLC expression as a tree."""
        raise NotImplementedError("Subclasses must implement this method.")


@dataclass
class NLCRelabel(NLCExpr):
    graph: NLCExpr
    renaming: dict[str, str]

    def to_graph(self) -> Graph:
        """
        Converts the NLCRelabel expression to a Graph.
        It applies the renaming to the vertices of the graph produced by `from`.
        """
        base_graph = self.graph.to_graph()
        recolored = [
            dataclasses.replace(v, color=self.renaming.get(v.color, v.color))
            for v in base_graph.vertices
        ]
        return dataclasses.replace(base_graph, vertices=recolored)

    def draw_tree(
        self, root_pos: tuple[float, float], width: float, pic: Picture, name: str
    ):
        sub_pos = (root_pos[0], root_pos[1] - 1)
        self.graph.draw_tree(sub_pos, width, pic, name + "r1")
        pic.node(
            "R",
            at=root_pos,
            circle=True,
            inner_sep="2pt",
            draw=True,
            name=name,
        )
        pic.draw(
            f"({name}r1)", topath(f"({name})"), **{"->": "true", "ultra thick": "true"}
        )


@dataclass
class NLCVertex(NLCExpr):
    color: str

    def to_graph(self) -> Graph:
        """
        Converts the NLCVertex expression to a Graph.
        It creates a single vertex with the specified color.
        """
        return Graph(
            name=f"vertex_{self.color}",
            vertices=[Vertex(name=f"v_{self.color}", color=self.color)],
            edges=[],
        )

    def draw_tree(
        self, root_pos: tuple[float, float], width: float, pic: Picture, name: str
    ):
        pic.node(
            "",
            at=root_pos,
            circle=True,
            inner_sep="2pt",
            draw=True,
            name=f"{name}",
            fill=self.color,
        )


@dataclass
class NLCCombine(NLCExpr):
    left: NLCExpr
    right: NLCExpr
    edges: list[tuple[str, str]] = field(default_factory=list)

    def to_graph(self) -> Graph:
        """
        Converts the NLCCombine expression to a Graph.
        It combines the graphs produced by `left` and `right` and adds edges between them.
        """
        left_graph = self.left.to_graph()
        right_graph = self.right.to_graph()

        def rename_vertex(v: Vertex, prefix: str) -> Vertex:
            return dataclasses.replace(v, name=f"{prefix}x{v.name}")

        def rename_edge(e: Edge, prefix: str) -> Edge:
            return dataclasses.replace(
                e,
                source=f"{prefix}x{e.source_name}",
                target=f"{prefix}x{e.target_name}",
            )

        combined_vertices = [rename_vertex(v, "left_") for v in left_graph.vertices] + [
            rename_vertex(v, "right_") for v in right_graph.vertices
        ]
        combined_edges = [rename_edge(e, "left_") for e in left_graph.edges] + [
            rename_edge(e, "right_") for e in right_graph.edges
        ]

        for v1 in left_graph.vertices:
            for v2 in right_graph.vertices:
                c1 = v1.color
                c2 = v2.color
                if (c1, c2) in self.edges:
                    combined_edges.append(
                        Edge(
                            source=f"left_x{v1.name}",
                            target=f"right_x{v2.name}",
                            color="black",
                            directed=False,
                        )
                    )

        return Graph(
            name=f"combine_{left_graph.name}_{right_graph.name}",
            vertices=combined_vertices,
            edges=combined_edges,
        )

    def draw_tree(
        self, root_pos: tuple[float, float], width: float, pic: Picture, name: str
    ) -> str:
        subwidth = width / 2

        left_root = (root_pos[0] - subwidth, root_pos[1] - 1)
        right_root = (root_pos[0] + subwidth, root_pos[1] - 1)

        left_root_label = name + "cl"
        right_root_label = name + "cr"

        self.left.draw_tree(left_root, subwidth, pic, left_root_label)
        self.right.draw_tree(right_root, subwidth, pic, right_root_label)

        pic.node(
            "C",
            at=root_pos,
            circle=True,
            inner_sep="2pt",
            draw=True,
            name=name,
        )

        pic.draw(
            f"({left_root_label})",
            topath(f"({name})"),
            **{"->": "true", "bend left": "20", "ultra thick": "true"},
        )

        pic.draw(
            f"({right_root_label})",
            topath(f"({name})"),
            **{"->": "true", "bend right": "20", "ultra thick": "true"},
        )


def animate_property(obj, prop, f=lambda x: x):
    """
    essentially,
    for (d, p) in obj.prop:
        yield (d+1, dataclasses.replace(obj, **{prop: p}))
    """
    for i, value in enumerate(f(getattr(obj, prop))):
        yield (i + 1, dataclasses.replace(obj, **{prop: value}))


def set_to_true(obj, props):
    """
    iteratively sets to true the properties in `props`
    """
    current = obj
    for prop in props:
        current = dataclasses.replace(current, **{prop: True})
        yield (0, current)


@dataclass
class NLCk:
    """
    1. NLC(k,F) expressions to build graphs
    2. iteratively build a finite path using
       3 colors and one relabeling
    3. abstract notation using a tree.
    4. theorem of DRT'10: for these classes we decide
    5. [thm, courcelle]: every class of bounded clique width
    is contained in one of those
    6. Problem: maybe all containments are bad!
        + draw ellipses
    7. To simplify: consider LINEAR clique-width
    """

    path_creation: Optional[int] = None
    show_drt: bool = False
    show_cou: bool = False
    show_prb: bool = False

    def draw(self, pic: Picture):
        Typography(
            r"$\mathsf{NLC}_Q^{\mathcal{F}}$ Expressions and Bounded Clique-Width",
            level=1,
            color="Prune",
            anchor="west",
            align="left",
            at=(-9, 4),
        ).draw(pic)

        Statement(
            name="Relabel Expressions",
            text=r"""
            Select a finite set $Q$ of colors, and 
            a finite set $\mathcal{F}$ of functions from $Q$ to $Q$.
            \begin{itemize}
                \item $\mathsf{vertex}(q)$ for $q \in Q$,
                \item $\mathsf{relabel}_f(g)$ for $f \in \mathcal{F}$, $g$ an expression,
                \item $\mathsf{combine}_P(g_1, g_2)$ for $P \subseteq Q \times Q$,
                and $g_1, g_2$ expressions.
            \end{itemize}
            """,
            at=(-9, 3.5),
            width=8,
        ).draw(pic)

        # create a path.
        # start with nodes colored using C3,
        # use the relabeling C3 -> A2 -> A1
        # join using (A2, C3) always
        relabel = {"B4": "A2", "A2": "A1"}
        select = [("A2", "B4")]

        if self.path_creation is not None:
            expr = NLCVertex(color="B4")
            for i in range(self.path_creation):
                if i % 2 == 0:
                    expr = NLCRelabel(renaming=relabel, graph=expr)
                else:
                    expr = NLCCombine(
                        left=expr, right=NLCVertex(color="B4"), edges=select
                    )

            # draw the graph
            graph = expr.to_graph()
            for i, v in enumerate(graph.vertices):
                v.at = (i // 3, i % 3)
            graph.draw(pic.scope(xshift="2cm", yshift="-3cm"))

            # draw the tree
            test_scope = pic.scope(
                xshift="-7cm", yshift="-2cm", rotate="90", xscale=0.5
            )
            expr.draw_tree(root_pos=(0, 0), width=5, pic=test_scope, name="NLCkExpr")

        if self.show_drt:
            Statement(
                name="Theorem [Daligault, Rao, Thomassé'10]",
                text=r"""
                For every $Q, \mathcal{F}$, one can decide whether 
                $\mathsf{NLC}_Q^{\mathcal{F}}$ is 2-wqo. Furthermore,
                the following are equivalent:
                \begin{itemize}
                    \item $\mathsf{NLC}_Q^{\mathcal{F}}$ is 2-wqo,
                    \item $\mathsf{NLC}_Q^{\mathcal{F}}$ is $X$-wqo, $\forall X$,
                    \item $\mathsf{NLC}_Q^{\mathcal{F}}$ does not contain
                      arbitrarily large paths
                \end{itemize}
                      """,
                at=(1, 3.5),
                width=8,
                border=True,
                color="A5",
            ).draw(pic)

        if self.show_cou:
            Statement(
                name="Theorem [Courcelle]",
                text=r"""
                      A class has bounded clique-width if and only if it is contained in some
                      $\mathsf{NLC}_Q^{\mathcal{F}}$.
                      """,
                at=(1, 0),
                width=8,
                border=True,
                color="C3",
            ).draw(pic)

        if self.show_prb:
            Statement(
                name="Problem",
                text=r"""
                      Subsets could still be WQO!
                      """,
                width=8,
                border=True,
                at=(1, -2),
                color="A2",
            ).draw(pic)

    def __iter__(self):
        yield (0, self)
        current = self
        for i, next in animate_property(
            current, "path_creation", f=lambda x: range(0, 8)
        ):
            yield (2, next)
            current = next
        current = dataclasses.replace(current, show_drt=True)
        yield (1, current)
        current = dataclasses.replace(current, show_cou=True)
        yield (1, current)
        current = dataclasses.replace(current, show_prb=True)
        yield (1, current)


@dataclass
class Results:
    """
    1. linNLC(k,F,P) -> fix how you add edges once and for all
    2. [lem]: it suffices to check pouzet's conj for these classes
    3. [thm]: given k,F,P, one can decide whether the class is lwqo,
        and in this case ...
    4. [cor]: the second part of Pouzet holds!!
    """

    show_setting: bool = False
    show_linear : bool = False
    show_theorem: bool = False
    show_lemma: bool = False
    show_cor: bool = False

    def draw(self, pic: Picture):
        Typography(
            text="Results",
            level=1,
            color="Prune",
            anchor="west",
            align="left",
            at=(-9, 4),
        ).draw(pic)

        if self.show_setting:
            Statement(
                name="Setting",
                text=r"""
                      We restrict ourselves to the \textbf{linear} NLC expressions,
                      and we fix how we add edges once and for all:
                      \begin{equation*}
                      \mathsf{linNLC}_Q^{\mathcal{F},P}
                      \end{equation*}
                      """,
                width=8,
                border=True,
                color="C1",
                at=(-9, 3),
            ).draw(pic)

        if self.show_linear:
            Typography(text="linear shaped expression trees!",
                       level=4,
                       at=(-4, 3.5),
                       _extra={"name": "linNLCExpr"},
                      ).draw(pic)

            pic.draw("(linNLCExpr)", 
                     topath((-4.3, 2.5)),
                     **{"->": True, "thick": True  })



        if self.show_theorem:
            Statement(
                name="Theorem",
                text=r"""Given $Q, \mathcal{F}, P$, the following
                      properties are equivalent and \textbf{decidable}:
                      \begin{itemize}
                      \item $\mathsf{linNLC}_Q^{\mathcal{F},P}$ is $X$-wqo, for all $X$,
                      \item $\mathsf{linNLC}_Q^{\mathcal{F},P}$ is $k$-wqo, for all $k$,
                      \item $\mathsf{linNLC}_Q^{\mathcal{F},P}$ is $(|\mathcal{F}|^3 \times 2)$-wqo.
                      \end{itemize}
                      """,
                at=(1, 3),
                width=8,
                color="D2",
            ).draw(pic)

        if self.show_lemma:
            Statement(
                name="Lemma",
                text=r"""It suffices to consider $\mathsf{linNLC}_Q^{\mathcal{F},P}$
                      to talk about any class of \textbf{bounded linear clique-width}.""",
                at=(-9, -1),
                color="A5",
                width=8,
            ).draw(pic)

        if self.show_cor:
            Statement(
                name="Corollary",
                text=r"""For all classes $\mathcal{C}$ of bounded linear clique-width,
                      $\mathcal{C}$ is $X$-wqo (for all $X$)
                      if and only if 
                      it is $k$-wqo (for all $k$).
                      """,
                at=(1, -1),
                width=8,
                color="A2",
            ).draw(pic)

    def __iter__(self):
        yield (0, self)
        for i, next in set_to_true(
            self, ["show_setting", "show_linear", "show_theorem", "show_lemma", "show_cor"]
        ):
            yield (i + 1, next)


@dataclass
class ProofSketch:
    """
    1. take a sequence of graphs
    2. take a sequence of words that represend these graphs
    3. transform these words into small trees (simon)
    4. find increasing pairs of small trees (higman)
    5. conclude that you have found an increasing pair of
       graphs (lemma: works if and only if you are
       |M|^3 × 2 WQO)
    """

    show_gis: bool = False
    show_wis: bool = False
    show_tis: bool = False
    show_inc: bool = False
    show_iss: bool = False

    def draw(self, pic: Picture):
        Typography(
            text="Proof Sketch",
            level=1,
            color="Prune",
            anchor="west",
            align="left",
            at=(-9, 4),
        ).draw(pic)

        if self.show_wis:
            pic.node(r"$\exists$", color="C3", at=(-8, 0.6))

        if self.show_tis:
            pic.node(r"$\exists$", color="A5", at=(-8, 1.8))
        if self.show_gis:
            pic.node(r"$\forall$", at=(-8, -0.5))

        if self.show_gis:
            seq = ["0", "1", "2", None, "i", None, "j", None]
            sc = pic.scope(xshift="-7cm", yshift="-0.5cm")
            for i, s in enumerate(seq):
                if s is None:
                    sc.node(r"$\cdots$", at=(i * 2, 0))
                else:
                    sc.node(r"$G_{%s}$" % s, at=(i * 2, 0), name=f"g{i}")
                    scc = sc.scope(yshift="1.5cm", xshift=f"{i * 2}cm")

                    if self.show_wis:
                        sc.node(
                            r"$w_{%s}$" % s, name=f"w{i}", color="C3", at=(i * 2, 0.7)
                        )
                        scc.draw((-0.3, -0.3), rectangle((0.3, -0.4)), fill="C3")

                    if self.show_tis:
                        scc.draw(
                            (-0.3, 0),
                            topath((0.3, 0)),
                            topath((0, 0.5)),
                            topath((-0.3, 0)),
                            fill="A5",
                        )
                        sc.node(
                            r"$t_{%s}$" % s,
                            name=f"t{i}",
                            at=(i * 2, 2.4),
                            color="A5",
                        )

            if self.show_gis and self.show_iss:
                pic.draw(
                    "(g4)",
                    topath("(g6)"),
                    _in="-90",
                    _out="-90",
                    color="B5",
                    **{"->": True, "dashed": True, "ultra thick": True},
                )



            if self.show_tis and self.show_inc:
                pic.draw(
                    "(t4)",
                    topath("(t6)"),
                    _in="90",
                    _out="90",
                    color="A2",
                    **{"->": True, "ultra thick": True},
                )

        if self.show_wis:
            Statement(
                name="By definition",
                text=r"$\forall G_i, \exists w_i$",
                at=(-8, -2),
                width=4,
                color="C3",
            ).draw(pic)
        if self.show_tis:
            Statement(
                name="Theorem [Simon]",
                text=r"$\forall w_i, \exists t_i$",
                at=(-2, -2),
                width=4,
                color="A5",
            ).draw(pic)
        if self.show_inc:
            Statement(
                name="Theorem [Higman]",
                text=r"$\exists i < j, t_i \leq t_j$",
                at=(5, -2),
                width=4,
                color="A2",
            ).draw(pic)


        if self.show_gis and self.show_iss:
            Typography(
                    text="Main Result",
                    at=(3, -2),
                    level=5,
                    _extra={"draw": "B5", "fill": "B5hint", "rounded_corners": "2mm"},
                ).draw(pic)

    def __iter__(self):
        yield (0, self)
        for d, next in set_to_true(
            self, ["show_gis", "show_wis", "show_tis", "show_inc", "show_iss"]
        ):
            yield (d + 1, next)


@dataclass
class Conclusion:
    """
    1. Closer to Pouzet's conjecture + **DECIDABLE**
    2. We can go to 2-wqo by a finer analysis of the proof
    3. We can go to trees, by replacing
    all word-based theorems by their tree-based versions
    (Higman -> Kruskal, Simon -> Colcombet)
    4. Can we go beyond graphs?
    """

    def draw(self, pic: Picture):
        Typography(
            text="Conclusion(s)",
            level=1,
            color="Prune",
            anchor="west",
            align="left",
            at=(-9, 4),
        ).draw(pic)

        pic.draw(
            (-2.5, 3.5),
            rectangle((8, -4.3)),
            color="A4",
            fill="A4hint",
            rounded_corners="2mm",
        )
        pic.node(
            "Future Work",
            draw="A4",
            font=r"\scshape",
            fill="A4hint",
            rounded_corners="2mm",
            at=(2.75, 3.5),
        )

        Statement(
            name="Theorem",
            at=(-9, 3),
            color="B3",
            text=r"""Half of Pouzet's conjecture holds for
                  classes of bounded linear clique-width: $\forall k$ $\implies$ $\forall X$""",
        ).draw(pic)

        Statement(
            name="Remark",
            at=(-9, 1),
            color="C3",
            text=r"""The proof of Daligault, Rao, and Thomassé
                  follows from our analysis""",
        ).draw(pic)

        Statement(
            name="Motto",
            at=(-9, -1),
            color="A1",
            text=r"""Automata / Semigroup theory applied to well-quasi-orders and structural properties of graph classes""",
        ).draw(pic)

        Statement(
            name="Towards 2-wqo",
            at=(-2, 3),
            width=9,
            color="A4",
            text=r"""Better analysis of the proof should lead to 2-wqo""",
        ).draw(pic)

        Statement(
            name="Towards trees",
            at=(-2, 1),
            color="A4",
            width=9,
            text=r"""
                  Higman'lemma $\longrightarrow$ Kruskal's tree theorem
                  \newline
                  Simon's word factorisation $\longrightarrow$ Colcombet's tree factorization
                  """,
        ).draw(pic)

        Statement(
            name="Interpretations",
            at=(-2, -1),
            color="B4",
            width=9,
            text=r"""
                  It is conjectured that for all classes $\mathcal{C}$:
                  \newline
                  $\mathcal{C}$ is 2-wqo
                  \newline
                  $\iff$
                  \newline
                  for every existential formula $\phi(x,y)$,
                  there is a bound on the lengths of the paths
                  that $\phi(x,y)$ defines in $\mathcal{C}$.
                  """,
        ).draw(pic)

    def __iter__(self):
        yield (0, self)


if __name__ == "__main__":
    tc = TableOfColors()
    tt = TitleFrame()
    ic = InducedGraph()
    fl = FreelyLabeled()
    gs = GoodSequence()
    wo = WellQuasiOrders()
    wd = WhyDoWeCare()
    rw = RelatedWork()
    nl = NLCk()
    rs = Results()
    ps = ProofSketch()
    cc = Conclusion()

    cfg = PresConfig(
        title="Labelled Well Quasi Ordered Classes of Bounded Linear Clique-Width",
        author="Aliaume Lopez",
        location="MFCS",
        date="2025-06-13",
        draft=False,
    )

    frames_list = [tt, ic, fl, wo, wd, rw, nl, rs, ps, cc]

    tmp_list = [tc, ps]

    frames = Sequential(frames_list, pos=0)

    cfg.preview(frames)
