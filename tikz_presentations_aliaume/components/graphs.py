from tikz import *

import math
import dataclasses
from typing import Literal, Generator, Callable, List, Union, Tuple, Optional
import random

from tikz_presentations_aliaume.components.utils import *


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

            eprops = self.edgesProps.get((i, j), {})

            pic.draw(f"({ni})", topath(f"({nj})"), **eprops)

    def __iter__(self):
        yield (0, self)


@dataclasses.dataclass
class Path:
    length: int

    verticesProps: List[dict] = dataclasses.field(default_factory=list)
    edgesProps: dict[Tuple[int, int], dict] = dataclasses.field(default_factory=dict)

    def draw(self, pic):
        start = -(self.length - 1) / 2
        for i in range(self.length):
            prps = self.verticesProps[i] if i < len(self.verticesProps) else {}
            n = prps.get("name", f"v{i}")
            myProps = {
                "at": (start + i, 0),
                "circle": True,
                "inner_sep": "2pt",
                "draw": True,
                "name": n,
            }
            pic.node("", **(prps | myProps))

        for i in range(self.length - 1):
            pi = self.verticesProps[i] if i < len(self.verticesProps) else {}
            j = i + 1
            pj = self.verticesProps[j] if j < len(self.verticesProps) else {}
            ni = pi.get("name", f"v{i}")
            nj = pj.get("name", f"v{j}")

            eprops = self.edgesProps.get((i, j), {})

            pic.draw(f"(v{i})", topath(f"(v{i + 1})"), **eprops)

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


HALF_GRAPH_PART = Literal["top", "bot"]
HALF_GRAPH_NODE = Tuple[HALF_GRAPH_PART, int]


@dataclasses.dataclass
class HalfGraph:
    topsize: int
    botsize: int

    verticesProps: dict[HALF_GRAPH_NODE, dict] = dataclasses.field(default_factory=dict)
    edgesProps: dict[Tuple[HALF_GRAPH_NODE, HALF_GRAPH_NODE], dict] = dataclasses.field(
        default_factory=dict
    )

    def draw(self, pic):
        topstart = -(self.topsize - 1) / 2
        botstart = -(self.botsize - 1) / 2

        # node naming convention
        nodename = lambda n: f"v{n[0]}{n[1]}"

        # topside
        for side, start, y0, rangeside in [
            ("top", topstart, 1, self.topsize),
            ("bot", botstart, -1, self.botsize),
        ]:
            for i in range(rangeside):
                xi = start + i
                yi = y0
                n = (side, i)

                props = {
                    "at": (xi, yi),
                    "circle": True,
                    "inner_sep": "2pt",
                    "draw": True,
                    "name": nodename(n),
                }
                nprops = self.verticesProps.get(n, {})
                pic.node("", **(nprops | props))

        # draw all edges
        nodes = [
            (s, i)
            for (s, r) in [("top", self.topsize), ("bot", self.botsize)]
            for i in range(r)
        ]
        for n1 in nodes:
            for n2 in nodes:
                eprops = self.edgesProps.get((n1, n2), {})
                print(eprops)
                n1prop = self.verticesProps.get(n1, {}) | {"name": nodename(n1)}
                n2prop = self.verticesProps.get(n2, {}) | {"name": nodename(n2)}

                side1, i = n1
                side2, j = n2

                name1 = n1prop["name"]
                name2 = n2prop["name"]

                # n1 top, n2 bot : i <= j
                if side1 == "top" and side2 == "bot" and j <= i:
                    pic.draw(f"({name1})", topath(f"({name2})"), **eprops)

                # n1/n2 on the same layer => i < j too
                if side1 == side2 and i < j:
                    if eprops:  # if we are asked to draw it
                        angle = "90" if side1 == "top" else "-90"
                        pic.draw(
                            f"({name1})",
                            topath(f"({name2})", _in=angle, _out=angle),
                            **eprops,
                        )

    def __iter__(self):
        yield (0, self)
