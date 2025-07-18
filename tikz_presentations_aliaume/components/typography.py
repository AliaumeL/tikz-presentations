from tikz import *

import dataclasses
from dataclasses import dataclass, field
from typing import List, Union, Optional, Literal


@dataclass
class Image:
    path: str
    width: float = 5
    height: float = 5
    at: tuple[float, float] = (0, 0)
    border: bool = False

    def draw(self, pic: Picture):
        if self.border:
            pic.draw(
                (self.at[0], self.at[1]),
                node(
                    f"\\includegraphics[width={self.width}cm,height={self.height}cm,keepaspectratio]{{{self.path}}}",
                    anchor="center",
                    draw=True,
                    rounded_corners="0.2cm",
                    fill="white",
                ),
            )
        else:
            pic.draw(
                (self.at[0], self.at[1]),
                node(
                    f"\\includegraphics[width={self.width}cm,height={self.height}cm,keepaspectratio]{{{self.path}}}",
                    anchor="center",
                ),
            )


@dataclass
class Typography:
    text: Union[str, list[str]] = field(default_factory=list)
    level: int = 0
    color: str = "A1"
    anchor: Literal["center", "north", "south", "east", "west"] = "center"
    align: Literal["center", "left", "right"] = "center"
    width: Optional[float] = None
    height: Optional[float] = None
    at: tuple[float, float] = (0, 0)
    _extra: dict[str, str] = field(default_factory=dict)

    @property
    def font_property(self):
        match self.level:
            case 0:
                return r"\huge\scshape"
            case 1:
                return r"\Large\bfseries"
            case 2:
                return r"\large"
            case 3:
                return r"\scshape"
            case 4:
                return r"\bfseries"
            case _:
                return r"\normalsize"

    def draw(self, pic: Picture):
        if isinstance(self.text, str):
            text_list = [self.text]
        else:
            text_list = self.text

        font = self.font_property

        line_space = 0.7 if self.level < 3 else 0.4

        grid = [
            (self.at[0], self.at[1] - i * line_space) for i in range(len(text_list))
        ]

        for (x, y), text in zip(grid, text_list):
            pic.node(
                text,
                anchor=self.anchor,
                align=self.align,
                color=self.color,
                font=font,
                text_width=self.width,
                height=self.height,
                at=(x, y),
                **self._extra,
            )


@dataclass
class Statement:
    text: str
    width: float = 6
    name: Optional[str] = None
    at: tuple[float, float] = (0, 0)
    color: str = "A1"
    border: bool = False
    centered: bool = False

    def draw(self, pic: Picture):
        text = (
            r"\textbf{" + self.name + r".}\newline " + self.text
            if self.name
            else self.text
        )
        pic.node(
            text,
            at=self.at,
            name=self.name,
            anchor=("center" if self.centered else "north west"),
            align="left",
            thick=True,
            text_width=f"{self.width}cm",
            inner_sep="5pt",
            color=self.color,
            draw=(True if self.border else None),
            fill=(self.color + "hint" if self.border else "white"),
            rounded_corners="0.2cm",
        )

    def __iter__(self):
        yield (0, self)


@dataclass
class GridLayout:
    cols: int = 1
    rows: int = 1
    width: float = 5
    height: float = 5
    at: tuple[float, float] = (0, 0)

    @property
    def cell_width(self):
        return self.width / self.cols

    @property
    def cell_height(self):
        return self.height / self.rows

    def cell_rectangle(self, col: int, row: int):
        x = self.at[0] + col * self.cell_width
        y = self.at[1] - row * self.cell_height
        return (x, y, self.cell_width, self.cell_height)
