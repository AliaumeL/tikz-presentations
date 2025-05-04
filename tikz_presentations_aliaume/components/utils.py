from tikz import *

import math
import dataclasses
from typing import Literal, Generator, Callable, List, Union, Tuple, Optional
import random


RATIO = 16 / 9
WIDTH = 20
HEIGHT = WIDTH / RATIO
TITLE = "Aliaume Lopez"
LOCATION = "Bordeaux"
DATE = "2025-05-06"

IS_DRAFT =  False # True

cAut = "A4"
cWA = "A3"
cBD = "A2"
cCom = "C3"
cGrp = "B5"


def extract_author(author):
    """extract list of last names from a bibtex author string"""
    names = author.split(" and ")
    return [name.split(",")[0] for name in names]


def animation_to_slides(anim) -> Generator[Tuple[int, Picture], None, None]:
    for depth, state in anim:
        pic = Picture()
        state.draw(pic)
        yield (depth, pic)


def tikz_of_animation(anim):
    slides = list(animation_to_slides(anim))
    packages = ["ensps-colorscheme", "amsmath", "amsfonts", "qrcode", "amssymb"]
    imports = "\n".join(f"\\usepackage{{{p}}}" for p in packages)

    depths = [0.5 / (d + 1) for d, _ in slides]

    code = "\n\n\n".join(
        [
            f"% Frame number {num}, animation depth {d} \n"
            + framing(Progress(num, depths), p).code()
            for num, (d, p) in enumerate(slides)
        ]
    )

    return r"""
\documentclass[tikz,9pt]{{standalone}}
\usepackage[maxbibnames=99,
    style=alphabetic,
    backend=biber,
    sorting=ydnt,
]{{biblatex}}
\usepackage{{hyperref}}
\hypersetup{{
    hidelinks,
    colorlinks,
    anchorcolor=A2,
    linkcolor=A4,
    citecolor=Prune,
}}
\usepackage[french]{{babel}}
\usepackage{{csquotes}}
\usepackage{{fontspec}}
\usepackage{{booktabs}}
\setmainfont{{EB Garamond}}
\usetikzlibrary{{decorations.markings}}
\usetikzlibrary{{arrows}}
\usetikzlibrary{{automata}}
\addbibresource{{papers.bib}}
\usepackage{{pifont}}% http://ctan.org/pkg/pifont
\newcommand{{\cmark}}{{\ding{{51}}}}%
\newcommand{{\xmark}}{{\ding{{55}}}}%
{imports}
\begin{{document}}
{code}
\end{{document}}
""".format(
        code=code, imports=imports
    )


def to_slide(anim):
    for state in anim:
        pic = Picture()
        state.draw(pic)
        yield pic


def preview_animation(anim):
    print("Previewing")
    with open("preview.tex", "w") as f:
        print(tikz_of_animation(anim))
        f.write(tikz_of_animation(anim))
    print("Compiling generated tex")
    os.system("xelatex preview.tex")
    print("Opening pdf viewer")
    # if osx, then open, else xdg-open
    if os.name == "posix":
        if os.uname().sysname == "Darwin":
            os.system("open preview.pdf")
        else:
            # spawn and do not wait for the process
            os.system("xdg-open preview.pdf &")
    print("DONE.")


@dataclasses.dataclass
class Progress:
    current: int
    depths: List[int]


def progress_bar(p: Progress, pic: Picture) -> Picture:
    i = p.current
    total = len(p.depths)
    totalTop = len([x for x in p.depths if x == 0.5])
    currentTop = len([x for x in p.depths[: i + 1] if x == 0.5])

    for j, depth in enumerate(p.depths):
        upleft = (-WIDTH / 2 + j * WIDTH / total, -HEIGHT / 2 + depth)
        downright = (-WIDTH / 2 + (j + 1) * WIDTH / total, -HEIGHT / 2)

        if j == i:
            pic.path(upleft, rectangle(downright), fill="D3", draw="A1")
        elif j < i:  # slides already seen
            pic.path(upleft, rectangle(downright), fill="D4", draw="A1")
        else:  # slides to come
            pic.path(upleft, rectangle(downright), fill="D1", draw="A1")

        lw = "{:.2f}".format(abs(upleft[0] - downright[0]) * 0.9)
        lh = "{:.2f}".format(abs(upleft[1] - downright[1]) * 0.9)
        pic.node(
            r"\hyperlink{page-"
            + str(j + 1)
            + "}{\\phantom{\\rule{"
            + lw
            + "cm}{"
            + lh
            + "cm}}}",
            align="left",
            at=downright,
            inner_sep="0pt",
            anchor="south east",
            color="A1",
        )

    pic.draw((-WIDTH / 2, HEIGHT / 2), rectangle((WIDTH / 2, -HEIGHT / 2)))
    pic.draw(
        (WIDTH / 2, -HEIGHT / 2 + 0.5),
        node(
            f"\\strut {currentTop}/{totalTop}",
            anchor="south east",
            align="right",
            text_width="3cm",
        ),
    )

    return pic


def framing(p: Progress, pic: Picture) -> Picture:
    i = p.current
    pic.draw((0, 0), node("\\hypertarget{page-" + str(i + 1) + "}{}"), opacity=0)

    if i > 0:
        pic.draw(
            (WIDTH / 2, HEIGHT / 2),
            node(TITLE, anchor="north east", font=r"\scshape"),
        )
        pic.draw(
            (-WIDTH / 2, HEIGHT / 2),
            node(f"{DATE} [{LOCATION}]", anchor="north west", font=r"\scshape"),
        )

    if IS_DRAFT:
        pic.draw((WIDTH / 2, -HEIGHT / 2), rectangle((-WIDTH / 2, HEIGHT / 2)))
        return pic
    else:
        return progress_bar(p, pic)


@dataclasses.dataclass
class Sequential:
    frames: list
    pos: int

    def draw(self, pic: Picture):
        self.frames[self.pos].draw(pic)

    def __iter__(self):
        for f in self.frames:
            for x in f:
                yield x


def drawing_to_node(d, size: float):
    pic = Picture()
    d.draw(pic)
    code = pic.code()
    node_ctn = f"\\resizebox{{{size:0.2f}cm}}{{!}}{{ {code} }}"
    return node_ctn


@dataclasses.dataclass
class AnimateAndThenMinimize[T]:
    anim: T
    size: float
    finished: bool
    run_args: dict
    fin_args: dict

    def draw(self, pic: Picture):
        if self.finished:
            final_pic = Picture()
            self.anim.draw(final_pic)
            code = final_pic.code()
            node_ctn = f"\\resizebox{{{self.size:0.2f}cm}}{{!}}{{ {code} }}"
            pic.node(
                node_ctn,
                **self.fin_args,
            )
        else:
            scope = pic.scope(**self.run_args)
            self.anim.draw(scope)

    def __iter__(self):
        for depth, state in self.anim:
            yield (
                depth,
                AnimateAndThenMinimize(
                    state, self.size, False, self.run_args, self.fin_args
                ),
            )
        yield (
            0,
            AnimateAndThenMinimize(
                state, self.size, True, self.run_args, self.fin_args
            ),
        )


@dataclasses.dataclass
class Bibliography:
    def draw(self, pic):
        pic.draw(
            (0, 0),
            node(
                r"""
\begin{minipage}{10cm}
\printbibliography
\end{minipage}
        """
            ),
        )

    def __iter__(self):
        yield (0, Bibliography())


@dataclasses.dataclass
class TableOfColors:
    def draw(self, pic):
        pic.draw(
            (0, 0),
            node(
                r"""
                             coucou
\begin{minipage}{10cm}
    \enspscolors
\end{minipage}
        """
            ),
        )

    def __iter__(self):
        yield (0, TableOfColors())


@dataclasses.dataclass
class TitleFrame:
    with_name: bool

    def draw(self, pic: Picture):
        scope = pic.scope(yshift="3cm")

        scope.node(
            "Concours MCF Section 27",
            at=(0, 1.5),
            anchor="center",
            font="\\Huge\\scshape",
            color="A4",
        )
        scope.node(
            "Offre 251816",
            at=(0, 0.5),
            anchor="center",
            font="\\huge\\scshape",
            color="A4",
        )

        scope.node(
            "Logique Monadique du Second Ordre et Beaux Préordres",
            at=(0, -1),
            anchor="center",
            align="center",
            color="A3",
            text_width="16cm",
            font="\\Large\\scshape",
        )
        scope.node("pour les", at=(0, -1.5), anchor="center", font="\\Large\\scshape")
        scope.node(
            "Méthodes Formelles",
            color="A5",
            at=(0, -2),
            anchor="center",
            font="\\Large\\scshape",
        )

        if self.with_name:
            pic.draw((0, -1), node("Aliaume Lopez", anchor="center", font="\\Large"))
            pic.draw((0, -1.5), node("Université de Varsovie", anchor="center"))
            pic.draw((0, -3), node(f"à {LOCATION}", anchor="center", font="\\Large"))
            pic.draw((0, -3.5), node(f"le {DATE}", anchor="center"))
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
class FilAriane:
    titles: List[str] = dataclasses.field(default_factory=list)
    current: Optional[int] = None
    width: float = 15
    header: Optional[str] = None

    def draw(self, pic):
        size = max(1, len(self.titles))

        if self.header is not None:
            pic.node(self.header, at=(0, 0.2), font="\\scshape", anchor="center")

        title_width = f"{self.width / size:0.2f}"
        pic.style(
            "titl",
            text_width=f"{title_width}cm",
            anchor="north west",
            align="center",
            font="\\large\\scshape\\bfseries",
        )

        pic.style("selected", text="A1")
        pic.style("notselected", opacity=0.3)

        for i, title in enumerate(self.titles):
            x = -self.width / 2 + i * self.width / size
            if i == self.current:
                style = "selected"
                ntitl = title  # = r"$\bullet$ " + title + r" $\bullet$"
                xx = x + float(title_width) / 2
                pic.draw(
                    (xx - 0.4, -0.6), rectangle((xx + 0.5, -0.65)), fill="A1", draw="A1"
                )
            else:
                style = "notselected"
                ntitl = title

            pic.node(ntitl, at=(x, 0), titl=True, style=style)

    def __iter__(self):
        yield (0, self)
