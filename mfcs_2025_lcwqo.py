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
            **self._extra
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
            **self._extra
        )

    def __iter__(self):
        yield (0, self)


@dataclass
class Graph:
    name: str
    vertices: list[Vertex]
    edges   : list[Edge]


    @staticmethod
    def cycle(name : str, size: int, radius: float = 1.0) -> 'Graph':
        vertices = [
            Vertex(name=f"{name}v{i}", 
                   at=(radius * math.cos(2 * math.pi * i / size),
                       radius * math.sin(2 * math.pi * i / size)))
            for i in range(size)
        ]
        edges = [Edge(source=vertices[i],
                      target=vertices[(i + 1) % size]) for i in range(size)]
        return Graph(name, vertices, edges)

    @staticmethod
    def path(name : str, length: int, spacing : float = 1.0) -> 'Graph':
        vertices = [
            Vertex(name=f"{name}v{i}", at=(i * spacing, 0)) for i in range(length)
        ]
        edges = [Edge(source=vertices[i],
                      target=vertices[i + 1]
                      ) for i in range(length - 1)]
        return Graph(name, vertices, edges)

    @staticmethod
    def clique(name : str, size: int, radius : float = 1.0) -> 'Graph':
        vertices = [
            Vertex(name=f"{name}v{i}", 
                   at=(radius * math.cos(2 * math.pi * i / size),
                       radius * math.sin(2 * math.pi * i / size)))
            for i in range(size)
        ]
        edges = [Edge(source=vertices[i],
                      target=vertices[j])
                 for i in range(size) for j in range(i + 1, size)]
        return Graph(name, vertices, edges)

    def draw(self, pic: Picture):
        for v in self.vertices:
            v.draw(pic)

        for e in self.edges:
            e.draw(pic)

    def map(self, vfunc: Callable[[Vertex], Vertex],
                  efunc: Callable[[Edge], Edge]) -> 'Graph':
        new_vertices = [vfunc(i,v) for (i,v) in enumerate(self.vertices)]
        new_edges = [efunc(i,e) for (i,e) in enumerate(self.edges)]
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

    e1 = Edge(source="v1", target="v2",
        _extra={"_in": "90", "_out": "90"})
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
class TitleFrame:
    def draw(self, pic: Picture):

        Typography(text=[
            "Labelled Well Quasi Ordered Classes",
            "of",
            "Bounded Linear Clique-Width",
        ], color="A4", at=(0,3)).draw(pic)

        Typography(text=[
            "Aliaume Lopez",
        ], level=2, color="A1", at=(0, 0)).draw(pic)

        Typography(text="University of Warsaw", 
                   level=3,
                   color="A1", at=(0, -0.5)).draw(pic)

        Typography(text=[
                   "MFCS'2025",
                   "Warsaw, Poland"
                ], 
                   level=4,
                   color="A1", at=(0, -2)).draw(pic)


        Image(path="images/institutions/university_of_warsaw.pdf",
              width=2.5,
              at=(-5, -2.5)).draw(pic)

        Image(path="images/institutions/zigmunt_zaleski_stitching.png",
              width=2.5,
              at=(5, -2.5)).draw(pic)


    def __iter__(self):
        yield (0, self)




@dataclass
class InducedGraph:
    """ Draws two graphs
        and an embedding 
        between the nodes.
    """

    def draw(self, pic):
        Typography(
            text="Graphs and Induced Subgraphs",
            level=1,
            color="Prune",
            anchor="west",
            align="left",
            at=(-9, 4)).draw(pic)



        g1 = Graph.cycle("g1", 3, radius=0.5)
        g2 = example_graph_two_triangles()

        emb = Embedding([ 
            Edge(source=g1.vertices[i], 
                 target=g2.vertices[i],
                 color="A4",
                 directed=True,
                _extra={"bend left": "30", "ultra thick": "true"})
            for i in range(3)
        ])

        s1 = pic.scope(xshift="-3cm")
        g1.draw(s1)
        Typography(text="G1", at=(0, -1.5), color="A1").draw(s1)
        s2 = pic.scope(xshift="3cm")
        Typography(text="G2", at=(0, -1.5), color="A1").draw(s2)
        g2.draw(s2)

        emb.draw(pic)
        

    def __iter__(self):
        yield (0, self)

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
    return [list(labeling) for labeling in product(range(1, labels + 1), repeat=vertices)]

@dataclass
class FreelyLabeled:
    """
        1. draws a triangle.
        2. Selects labels { 1, 2, 3 }
        3. Draws all freely labeled triangles (up to iso)
    """
    def draw(self, pic):
        Typography(
            text="Freely Labeled Graphs",
            level=1,
            color="Prune",
            anchor="west",
            align="left",
            at=(-9, 4)).draw(pic)

        g = Graph.cycle("g", 3, radius=0.5)
        g.draw(pic)

        for i, labels in enumerate(all_labels(3, 3)):
            g.map(
                vfunc=lambda k,v: dataclasses.replace(v, name=v.name+f"copy{i}", label=f"{labels[k]}"),
                efunc=lambda k,e: dataclasses.replace(e, source=e.source_name+f"copy{i}", target=e.target_name+f"copy{i}")
            ).draw(pic.scope(xshift=f"{(i // 3) * 2 - 8}cm",
                             yshift=f"{(i % 3) * -2 + 1}cm"))


    def __iter__(self):
        yield (0, self)


@dataclass
class GoodSequence:
    sequence: list[Optional[Graph]]
    increasing: Optional[tuple[int,int]] = None
    embedding : Optional[Embedding] = None

    def draw(self, pic: Picture):
        for i, g in enumerate(self.sequence):
            if g is None:
                Typography(text="∅", at=(i * 2, 0), color="A1").draw(pic)
            else:
                g.draw(pic.scope(xshift=f"{i * 2}cm", yshift=0))
                Typography(text=f"G{i+1}", at=(i * 2, -1.5), color="A1").draw(pic)

        if self.increasing is not None:
            Typography(text="Increasing Pair", at=(self.increasing[0] * 2, 1.5), color="A4").draw(pic)
            pic.draw(
                f"(G{self.increasing[0]+1})",
                topath(f"(G{self.increasing[1]+1})"),
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
    pass

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
    pass

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
    def draw(self, pic):
        Typography(
            text="Related Work",
            level=1,
            color="Prune",
            anchor="west",
            align="left",
            at=(-9, 4)).draw(pic)

        Statement(name="Conjecture [Pouzet'72]",
                  text=r"$2$-wqo $\implies$ $\forall k \in \mathbb{N}$, $k$-wqo",
                  at=(-9, 3),
                  border=True,
                  color="B4").draw(pic)

        Statement(name="Conjecture [Pouzet'72]",
                  text=r"$\forall k \in \mathbb{N}$, $k$-wqo $\implies$ $\forall X$, $X$-wqo",
                  at=(3, 3),
                  border=True,
                  color="B4").draw(pic)


        Statement(name="Theorem [Ding'92]",
                  text="Bounded tree-depth implies label-wqo",
                  at=(-9, 1.5),
                  border=True,
                  color="B5").draw(pic)

        Statement(text="the converse fails (ex: cliques)",
                  at=(-3, 1),
                  width=3,
                  border=True,
                  color="A2").draw(pic)


        Statement(name="Theorem [Daligault, Rao, Thomassé'10]",
                  at=(0, -1),
                  centered=True,
                  width=6.5,
                  text=r"For \textbf{some classes} of bounded clique-width,\newline both conjectures hold",
                  color="A5").draw(pic)

        Statement(name="Conjecture [Daligault, Rao, Thomassé'10]",
                  at=(0, -2.5),
                  width=6.5,
                  border=True,
                  centered=True,
                  text=r"$2$-wqo $\implies$ bounded clique-width",
                  color="B4").draw(pic)




    def __iter__(self):
        yield (0, self)


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
    pass

@dataclass
class Results:
    """
        1. linNLC(k,F,P) -> fix how you add edges once and for all
        2. [lem]: it suffices to check pouzet's conj for these classes
        3. [thm]: given k,F,P, one can decide whether the class is lwqo,
            and in this case ...
        4. [cor]: the second part of Pouzet holds!!
    """
    pass

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
    pass

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
    pass


if __name__ == "__main__":
    tc = TableOfColors()
    tt = TitleFrame()
    ic = InducedGraph()
    fl = FreelyLabeled()
    gs = GoodSequence(
            sequence=[ Graph.clique(f"c{i}", i + 3, radius=0.5) for i in range(1, 3) ] 
                     + [ None ]
                     + [ Graph.clique(f"p{i}", i + 2, radius=0.5) for i in range(1, 3) ]
                     + [ None ]
                     + [ Graph.clique(f"k{i}", i + 2, radius=0.5) for i in range(1, 3) ]
                     + [ None ],
            increasing=None,
            embedding=None)

    rw = RelatedWork()

    cfg = PresConfig(
        title="Polyczek",
        author="Aliaume Lopez",
        location="MFCS",
        date="2025-06-13",
        draft=True,
    )

    frames_list = [
        tc,
        #tt,
        #ic,
        #fl,
        #gs,
        rw  
    ]

    frames = Sequential(frames_list, pos=0)

    cfg.preview(frames)
