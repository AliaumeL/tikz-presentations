

from tikz import *

import math
import dataclasses
from typing import Literal, Generator, Callable, List, Union, Tuple, Optional
import random

from utils import *


@dataclasses.dataclass
class Cycle:
    size:   int
    radius: float | int
    
    verticesProps: List[dict] = dataclasses.field(default_factory=list)
    edgesProps:    dict[Tuple[int,int], dict] = dataclasses.field(default_factory=dict)

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
                     "name": n }
            pic.node("", **(prps | myProps ))

        for i in range(self.size):
            pi = self.verticesProps[i] if i < len(self.verticesProps) else {}
            j = (i+1)%self.size
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
        start = -(self.length-1)/2
        for i in range(self.length):
            pic.node("",
                     at=(start + i,0),
                     circle=True,
                     draw=True,
                     inner_sep="2pt",
                     name=f"v{i}")

        for i in range(self.length-1):
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
            pic.node("",
                     at=(x, y),
                     circle=True,
                     inner_sep="2pt",
                     draw=True,
                     name=f"v{i}")

        # draw all edges
        for i in range(self.size):
            for j in range(i+1, self.size):
                pic.draw(f"(v{i})", topath(f"(v{j})"))

    def __iter__(self):
        yield (0, self)


