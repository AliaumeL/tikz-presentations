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
from dataclasses import dataclass, field
from typing import Literal, Generator, Callable, List, Union, Tuple, Optional


@dataclasses.dataclass
class TitleFrame:
    def draw(self, pic: Picture):
        scope = pic.scope(yshift="2cm")

        scope.node(
            "Polyregular",
            at=(0, 1),
            anchor="center",
            font="\\huge\\scshape",
            color="A2",
        )
        scope.node(
            "Model Checking",
            at=(0, 0),
            anchor="center",
            align="center",
            color="A4",
            text_width="16cm",
            font="\\huge\\scshape",
        )

        pic.draw(
            (0, -1),
            node("Aliaume Lopez and Rafał Stefański", anchor="center", font="\\Large"),
        )
        pic.draw((0, -1.5), node("University of Warsaw", anchor="center"))
        pic.draw((0, -3), node(f"Paris", anchor="center", font="\\Large"))
        pic.draw((0, -3.5), node(f"Séminaire automates, 2025-06-13", anchor="center"))
        pic.draw((6, -2), node(r"\qrcode{https://www.irif.fr/~alopez/}"))
        pic.draw((6, -3.5), node(r"\url{https://www.irif.fr/~alopez/}"))

        logos = [
            "images/institutions/university_of_warsaw.pdf",
            "images/institutions/zigmunt_zaleski_stitching.png",
        ]
        for i, logo in enumerate(logos):
            pic.draw(
                (-4.5 - 2.8 * i, -2),
                node(f"\\includegraphics[width=2cm]{{{logo}}}", anchor="center"),
            )

    def __iter__(self):
        yield (0, self)


@dataclass
class ModelChecking:
    show_hoare: bool = True
    show_regular: bool = True
    show_continuous: bool = True
    show_regular_mc: bool = True
    show_allfolks: bool = True

    def draw(self, pic: Picture):
        pic.node(
            "(Regular) Model Checking",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        pic.node(
            "Verify that a system satisfies a specification",
            at=(-9, 3.3),
            anchor="west",
            text_width="8cm",
        )

        sc = pic.scope(yshift="1cm", opacity=(1 if self.show_hoare else 0))

        sc.node(r"$\{ \varphi \}$", at=(-2, 0), color="C2", font="\\LARGE")
        sc.node(r"$P$", at=(0, 0), color="A4", font="\\LARGE")
        sc.node(r"$\{ \psi \}$", at=(2, 0), color="C2", font="\\LARGE")

        sc.node(
            r"precondition", at=(-2.5, 0), anchor="east", color="C2", font="\\Large"
        )
        sc.node(
            r"postcondition", at=(2.5, 0), anchor="west", color="C2", font="\\Large"
        )
        sc.node(r"program", at=(0, -0.7), color="A4", font="\\Large")

        sc.node(r"Hoare Triple", at=(0, -1.5), color="A1", font="\\scshape\\Large")

        pic.node(
            r"""
                 \textbf{Regular} Model Checking:
                 \begin{itemize}
                 \item \textbf{Programs}: string-to-string programs
                 \item \textbf{Specifications}: regular expressions
                 \end{itemize}
                 """,
            at=(-9, -2),
            anchor="north west",
            text_width="8cm",
            opacity=(1 if self.show_regular else 0),
        )

        pic.node(
            r"""
                \textbf{Continuous functions}:
                 \newline
                 $f^{-1}(L)$ is regular whenever $L$ is a regular language
                 """,
            at=(9, -2),
            anchor="north east",
            text_width="7cm",
            opacity=(1 if self.show_continuous else 0),
        )

        pic.node(
            r"""Regular Model Checking of Continuous Functions 
                     \newline 
                     $\varphi \implies P^{-1}(\psi)$
                 """,
            at=(0, -0.5),
            font=r"\large",
            inner_sep="5mm",
            text_width="9cm",
            align="center",
            fill="white",
            draw=True,
            opacity=(1 if self.show_regular_mc else 0),
            rounded_corners="5pt",
        )

        pic.node(
            r"\includegraphics[width=2.5cm]{images/cliparts/thats-all-folks.jpg}",
            at=(0, -2.5),
            opacity=(1 if self.show_allfolks else 0),
        )

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self,
                show_hoare=False,
                show_regular=False,
                show_continuous=False,
                show_regular_mc=False,
                show_allfolks=False,
            ),
        )
        for i in range(1, 6):
            yield (
                1,
                dataclasses.replace(
                    self,
                    show_hoare=(i >= 1),
                    show_regular=(i >= 2),
                    show_continuous=(i >= 3),
                    show_regular_mc=(i >= 4),
                    show_allfolks=(i >= 5),
                ),
            )


@dataclass
class ContinuousOrNot:
    questions: list[dict]

    @staticmethod
    def default():
        qlist = [
            {"text": r"$w \mapsto w \# w$", "answ": True},
            {"text": r"$w_1 \# w_2 \mapsto (w_1 = w_2)$", "answ": False},
            {"text": r"$w \mapsto w^{|w|}$", "answ": True},
            {"text": r"$w \mapsto \mathsf{sort}(w)$", "answ": True},
            {
                "text": r"$w_1 \# \cdots \# w_n \mapsto \mathsf{sort}(\cdots)$",
                "answ": False,
            },
            {"text": r"$w \mapsto a^{!|w|}$", "answ": True},
            {"text": r"$\exists f \text{non-computable and continuous}$", "answ": True},
        ]
        return ContinuousOrNot(questions=qlist)

    def draw(self, pic: Picture):
        pic.node(
            "Continuity Quizz",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        if len(self.questions) > 0:
            curr = self.questions[-1]
            col = "A1"
            if curr["answ"] is True:
                col = "A5"
            elif curr["answ"] is False:
                col = "A2"

            pic.node(curr["text"], at=(0, 3), font=r"\large", color=col)

        oldones = self.questions[:-1]

        positives = [q for q in oldones if q["answ"] is True]
        negatives = [q for q in oldones if q["answ"] is False]

        ypscale = lambda y: 1 - y * 0.7
        ynscale = lambda y: 1 - y * 0.7

        for y, q in enumerate(positives):
            pic.node(q["text"], at=(-1, ypscale(y)), anchor="east", color="A5")
        for y, q in enumerate(negatives):
            pic.node(q["text"], at=(1, ynscale(y)), anchor="west", color="A2")

    def __iter__(self):
        yield (0, dataclasses.replace(self, questions=[]))
        for i in range(len(self.questions)):
            old = self.questions[:i]
            cur = self.questions[i]
            curQ = {**cur, "answ": None}
            yield (1, dataclasses.replace(self, questions=old + [curQ]))
            yield (1, dataclasses.replace(self, questions=old + [cur]))


@dataclass
class TransducerModels:
    models: set[str]
    inclusion_arrows: bool = True
    show_cont: bool = True
    show_example: bool = True
    show_problem: bool = True

    @staticmethod
    def default():
        return TransducerModels(
            models={"mealy", "seq", "umealy", "uft", "tdft", "ptdft", "ariadne"},
            inclusion_arrows=True,
            show_cont=True,
            show_example=True,
            show_problem=True,
        )

    def draw(self, pic: Picture):
        pic.node(
            "A zoo of transducer models",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        classes = [
            {"name": "mealy", "text": "Mealy", "at": (-8, 0)},
            {"name": "seq", "text": "Seq.", "at": (-6, 2)},
            {"name": "umealy", "text": "UMealy", "at": (-6, -2)},
            {"name": "uft", "text": "UFT", "at": (-4, 0)},
            {"name": "tdft", "text": r"2DFT", "at": (-1, 0)},
            {
                "name": "ptdft",
                "at": (2, 0),
                "text": r"2DFT \newline + pebbles",
                "text_width": "2cm",
            },
            {
                "name": "ariadne",
                "text": r"Ariadne \newline Transducers",
                "at": (6, 0),
                "text_width": "2cm",
            },
        ]

        pic.style(
            "transducer",
            fill="D4hint",
            anchor="west",
            minimum_width="2cm",
            inner_sep="5mm",
            draw=True,
            rounded_corners="5pt",
        )

        for c in classes:
            d = {k: v for k, v in c.items() if k != "text"}
            if c.get("name", None) in self.models:
                pic.node(c["text"], transducer=True, **d)

        if self.show_cont:
            pic.node(
                r"""\textbf{Continuity}: all those automata-based models
                     compute regular languages""",
                at=(-2, 3),
                anchor="north west",
                text_width="6cm",
            )
        if self.inclusion_arrows:
            # draw inclusion arrows
            arrows = [
                ("mealy", "seq", {"_in": "180", "_out": "90"}),
                ("mealy", "umealy", {"_in": "180", "_out": "-90"}),
                ("seq", "uft", {"_out": "0", "_in": "90"}),
                ("umealy", "uft", {"_out": "0", "_in": "-90"}),
                ("uft", "tdft", {}),
                ("tdft", "ptdft", {}),
                ("ptdft", "ariadne", {}),
            ]
            for f, t, d in arrows:
                pic.draw(
                    f"({f})",
                    topath(f"({t})"),
                    thick=True,
                    color="A1",
                    draw=True,
                    opt="->",
                    **d,
                )

        if self.show_example:
            pic.node(
                r"""\textbf{Example}: 2DFT $\simeq$ SST \newline
                     $\mathsf{PSPACE}$ model checking \newline [Alur Černý, POPL'11]""",
                at=(2, -2),
                anchor="north west",
                text_width="6cm",
            )

        if self.show_problem:
            pic.node(
                r"""\textbf{Problem}: terrible to use""",
                fill="A2hint",
                draw=True,
                thick=True,
                font=r"\Large",
                rotate="10",
                inner_sep="5mm",
            )

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self,
                models=set(),
                inclusion_arrows=False,
                show_cont=False,
                show_example=False,
                show_problem=False,
            ),
        )
        for i in range(1, len(self.models) + 1):
            yield (
                1,
                dataclasses.replace(
                    self,
                    models=set(list(self.models)[:i]),
                    inclusion_arrows=False,
                    show_cont=False,
                    show_example=False,
                    show_problem=False,
                ),
            )
        for i in range(2, 6):
            yield (
                1,
                dataclasses.replace(
                    self,
                    inclusion_arrows=(i >= 2),
                    show_cont=(i >= 3),
                    show_example=(i >= 4),
                    show_problem=(i >= 5),
                ),
            )


@dataclass
class Polyreg:
    show_meme: bool = True

    def draw(self, pic: Picture):
        pic.node(
            "Polyregular Functions",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        pic.style(
            "polyreg",
            fill="D4hint",
            text_width="2.5cm",
            minimum_height="2cm",
            inner_sep="5mm",
            draw=True,
            rounded_corners="5pt",
        )

        pic.node(
            r"MSO \newline interpretations",
            polyreg=True,
            at=(-3, 2),
        )
        pic.node(
            r"Pebble \newline transducers",
            polyreg=True,
            at=(-3, -2),
        )
        pic.node(
            r"List functions",
            polyreg=True,
            at=(3, -2),
        )
        pic.node(
            r"For-programs",
            polyreg=True,
            at=(3, 2),
        )

        pic.node(
            r"\includegraphics[width=6cm]{images/cliparts/spiderman-polyreg.jpg}",
            at=(0, 0),
            anchor="center",
            opacity=(1 if self.show_meme else 0),
        )

    def __iter__(self):
        yield (0, dataclasses.replace(self, show_meme=False))
        yield (1, dataclasses.replace(self, show_meme=True))


@dataclass
class HighLevelForPrograms:
    show_rules: bool = True
    show_surprise: bool = True

    def draw(self, pic: Picture):
        pic.node(
            "Let's design",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        pic.node(
            r"\includegraphics[width=10cm]{images/cliparts/simple-for-programs.png}",
            at=(4, 0),
            anchor="center",
            fill="white",
            draw=True,
            rounded_corners="5pt",
        )

        if self.show_rules:
            pic.node(
                r"""Rules of the fight
                     \begin{description}
                     \item[lists] (2)
                     \item[loops] (6) and (7)
                     \item[variables] (6)
                     \item[equality] (4)
                     \item[tests] (1)
                     \item[shadowing] no nay never
                     \item[functions] no boolean inputs
                     \item[updates] (3) and (5)
                    \end{description}
                    """,
                at=(-9, 3),
                anchor="north west",
                text_width="8cm",
            )

        if self.show_surprise:
            pic.node(
                r"\includegraphics[width=5cm]{images/cliparts/surprise-tool.jpg}",
                at=(0, 0),
                anchor="center",
            )

    def __iter__(self):
        yield (0, dataclasses.replace(self, show_rules=False, show_surprise=False))
        yield (1, dataclasses.replace(self, show_rules=True, show_surprise=False))
        yield (1, dataclasses.replace(self, show_rules=True, show_surprise=True))


@dataclass
class LowLevelForPrograms:
    def draw(self, pic: Picture):
        pic.node(
            "Simple for programs",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        pic.node(
            r"\includegraphics[width=10cm]{images/cliparts/simple-for-program-simple.pdf}",
            at=(4, 0),
            anchor="center",
            fill="white",
            draw=True,
            rounded_corners="5pt",
        )

        pic.node(
            r"""Rules of the fight
                 \begin{description}
                 \item[functions] no no no
                 \item[lists] no!
                 \item[variables] only booleans / positions
                \end{description}
                """,
            at=(-9, 3),
            anchor="north west",
            text_width="8cm",
        )

    def __iter__(self):
        yield (0, self)


@dataclass
class SwapAsBsFOI:
    input: str = "automates"

    show_vars: bool = True
    select_dom: bool = True
    order_vars: bool = True
    show_out: bool = True

    def draw(self, pic: Picture):
        l = len(self.input)
        w = 6
        s = w / l
        m = w / 2

        # create the input letters
        # with numbers below them
        for i, c in enumerate(self.input):
            pic.node(
                c,
                at=(-m + i * s, -1),
                anchor="center",
                color="A5",
            )
            pic.node(
                str(i),
                at=(-m + i * s, -1.2),
                anchor="center",
                font="\\tiny",
                color="A5",
            )
        if self.show_vars:
            # create the numbers for the "print" formula
            pic.node(r"\texttt{printB}", at=(-m - 0.2, -2), anchor="east", color="A3")
            for i, c in enumerate(self.input):
                isInDom = c == "a"
                txt = "b" if self.show_out else str(i)
                pic.node(
                    txt,
                    name=f"print{i}",
                    at=(-m + i * s, -2),
                    anchor="center",
                    color="A3",
                    opacity=(1 if isInDom or not self.select_dom else 0.1),
                )

            # create the numbers for the "copy" formula
            pic.node(r"\texttt{copy}", at=(-m - 0.2, -3), anchor="east", color="C3")
            for i, c in enumerate(self.input):
                isInDom = c != "a"
                txt = c if self.show_out else str(i)
                pic.node(
                    txt,
                    name=f"copy{i}",
                    at=(-m + i * s, -3),
                    anchor="center",
                    color="C3",
                    opacity=(1 if isInDom or not self.select_dom else 0.1),
                )

        if self.order_vars:
            for i, c in enumerate(self.input[:-1]):
                j = i + 1
                ni = f"print{i}" if c == "a" else f"copy{i}"
                nj = f"print{j}" if self.input[j] == "a" else f"copy{j}"
                pic.draw(
                    f"({ni})",
                    topath(f"({nj})"),
                    thick=True,
                    color="A1",
                    opt="->",
                )

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self,
                show_vars=False,
                select_dom=False,
                order_vars=False,
                show_out=False,
            ),
        )

        for i in range(1, 5):
            yield (
                1,
                dataclasses.replace(
                    self,
                    show_vars=(i >= 1),
                    select_dom=(i >= 2),
                    order_vars=(i >= 3),
                    show_out=(i >= 4),
                ),
            )


@dataclass
class FirstOrderInterpretations:
    show_def: bool = True
    show_example: bool = True

    evaluated: Optional[SwapAsBsFOI] = None

    @staticmethod
    def default():
        return FirstOrderInterpretations(
            evaluated=SwapAsBsFOI(),
        )

    def draw(self, pic: Picture):
        pic.node(
            "First-Order Interpretations",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        pic.node(
            r"\includegraphics[width=6cm]{images/cliparts/fo-interp-spap-as-to-bs.pdf}",
            at=(4, 0),
            anchor="center",
            fill="white",
            draw=True,
            rounded_corners="5pt",
            opacity=(1 if self.show_example else 0),
        )

        pic.node(
            r"""Rules of the fight
                 \begin{description}
                 \item[tags] finite set $\mathsf{tags}$
                 \item[arities] $\mathsf{ar} \colon \mathsf{tags} \to \mathbb{N}$
                 \item[domain] first order formulas
                 $\varphi_{\mathsf{dom}}^{t}$
                 \item[output letters]
                 $\mathsf{out} \colon \mathsf{tags} \to A + \mathbb{N}$
                 \item[output order] first order formulas
                 $\varphi_{\leq}^{t_1, t_2}$
                \end{description}
                """,
            at=(-9, 3),
            anchor="north west",
            text_width="8cm",
            opacity=(1 if self.show_def else 0),
        )

        sc = pic.scope(xshift="-4cm", yshift="0cm")

        if self.evaluated:
            self.evaluated.draw(sc)

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self,
                show_def=False,
                show_example=False,
                evaluated=None,
            ),
        )
        for i in range(1, 3):
            yield (
                1,
                dataclasses.replace(
                    self, show_def=(i >= 1), show_example=(i >= 2), evaluated=None
                ),
            )
        if self.evaluated is not None:
            for d, e in self.evaluated:
                yield (
                    d + 1,
                    dataclasses.replace(self, evaluated=e),
                )


@dataclass
class FirstOrderLogicWithTags:
    show_pullback: bool = True
    show_defs: bool = True

    def draw(self, pic: Picture):
        pic.node(
            "First-Order Logic... with tags!",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        pic.node(
            r"""
                 $\varphi :=
                 \textcolor{C3}{\exists x : \mathsf{tag}}, \varphi \mid
                 \textcolor{A5}{\exists x : \mathsf{pos}}, \varphi \mid
                 \neg \varphi \mid
                 \varphi_1 \land \varphi_2 \mid
                 \textcolor{A5}{ x =_L \mathtt{a} } \mid
                 \textcolor{A5}{x \leq y} \mid
                 \textcolor{C3}{x = \mathfrak{t}}
                 $
                """,
            at=(-9, 3),
            anchor="north west",
            text_width="15cm",
        )

        pbs = pic.scope(xshift="-6cm", opacity=(1 if self.show_pullback else 0))
        fos = pic.scope(
            xshift="-3cm",
            yshift="3.5cm",
            font="\\small",
            color="B1",
            opacity=(1 if self.show_defs else 0),
        )

        pbs.draw((-2.7, 2), rectangle((2.7, -1)))
        pbs.node(r"$\mathsf{FO}$", name="fo", color="A5", at=(-2, 1))
        pbs.node(r"$f$ $\in$ $\mathsf{FO}$-I", name="foi", at=(0, 1.5))
        pbs.node(
            r"\textcolor{A5}{$\mathsf{FO}$}+\textcolor{C3}{T}", name="fot", at=(2, 1)
        )

        pbs.draw("(fo)", topath("(fot)"), opt="->", thick=True, color="A1")

        pbs.node(
            r"$\forall w, f(w) \models \varphi \iff w \models f(\varphi)$", at=(0, 0)
        )

        fos.node(
            r"""
                 $ f(\forall_{x} \psi)
                 := 
                   \textcolor{C3}{\forall_{t_x \in \mathsf{tags}}} \; 
                   \textcolor{A5}{\forall_{x_1, \ldots, x_{\mathsf{ar}(f)}}}
                   \left( {\mathsf{dom}}(t_x, x_1, \ldots, x_{\mathsf{ar}(f)}) \Rightarrow f(\psi)\right)$
                 """,
            anchor="west",
            at=(0, -2),
        )

        fos.node(
            r"""
                 $ \mathsf{dom}(t, x_1, \ldots, x_{\mathsf{ar}(t)}) :=
                   \bigvee_{t' \in \mathsf{tags}}
                   \left(\textcolor{C3}{t = t'}
                         \wedge \varphi_{\mathsf{dom}}^{t'}(x_1, \ldots, x_{\mathsf{ar}(t')}) \right)
                 $""",
            anchor="west",
            at=(0, -3),
        )

        fos.node(
            r"""
                 $ f(x \leq y) :=
                   \bigvee_{t_1, t_2 \in \mathsf{tags}}
                   \left( \textcolor{C3}{t_x = t_1} \wedge 
                         \textcolor{C3}{t_y = t_2} \wedge
                     \varphi_{\leq}^{t_1, t_2}(x_1, \ldots, x_{\mathsf{ar}(t_1)}, y_1, \ldots, y_{\mathsf{ar}(t_2)}) \right)
                 $""",
            anchor="west",
            at=(0, -4),
        )

        fos.node(
            r"""
                 $ f(x =_L \mathtt{a}) :=
                   \left(\bigvee_{t \in \mathsf{tags} \wedge \mathsf{out}(t) = \mathtt{a}} 
                         \textcolor{C3}{t = t_x} \right) \vee
                   \left(\bigvee_{t \in \mathsf{tags} \wedge \mathsf{out}(t) \not \in A} 
                         (\textcolor{C3}{t = t_x} \wedge
                          \textcolor{A5}{x_{\mathtt{out}(t)} =_L \mathtt{a}})\right)
                 $""",
            anchor="west",
            at=(0, -5),
        )

    def __iter__(self):
        yield (0, dataclasses.replace(self, show_pullback=False, show_defs=False))
        for i in range(1, 3):
            yield (
                1,
                dataclasses.replace(
                    self,
                    show_pullback=(i >= 1),
                    show_defs=(i >= 2),
                ),
            )


@dataclass
class DemoTime:
    def draw(self, pic: Picture):
        pic.node(
            "demo",
            at=(0, 0),
            anchor="center",
            font="\\Huge\\scshape",
            color="A2",
        )

    def __iter__(self):
        yield (0, self)


@dataclass
class Architecture:
    status: dict[str, Literal["unknown", "validated"]]

    @staticmethod
    def default():
        return Architecture(
            status={
                "prog": "unknown",
                "forprog": "unknown",
                "foi": "unknown",
                "fot": "unknown",
                "smtlib2": "unknown",
                "mona": "unknown",
                "altergo": "unknown",
            }
        )

    def draw(self, pic: Picture):
        pic.node(
            "Anatomy of a For(program checker)",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        def getprops(name: str) -> dict:
            if self.status[name] == "unknown":
                return {"unknown": True}
            else:
                return {"validated": True}

        pic.style(
            "isformat",
            fill="D4hint",
            minimum_width="2cm",
            inner_sep="5mm",
            draw=True,
            rounded_corners="5pt",
        )

        pic.style("unknown", dashed=True)
        pic.style("validated", draw="D3", dashed=None, thick=True)

        pic.node("Program", name="prog", isformat=True, at=(-8, 0), **getprops("prog"))

        pic.node(
            "For-program",
            name="forprog",
            isformat=True,
            at=(-4, 0),
            **getprops("forprog"),
        )

        pic.node("FO-Int.", name="foi", isformat=True, at=(0, 0), **getprops("foi"))

        pic.node("FO", name="fo", isformat=True, fill="C3hint", at=(2, -2))

        pic.node("FO+T", isformat=True, name="fot", at=(4, 0), **getprops("fot"))

        pic.node(
            "SMTLib2", name="smtlib2", isformat=True, at=(8, 2), **getprops("smtlib2")
        )

        pic.node("MONA", name="mona", isformat=True, at=(8, 0), **getprops("mona"))

        pic.node(
            "Alt-Ergo", name="altergo", isformat=True, at=(8, -2), **getprops("altergo")
        )

        pic.style(
            "inclarrow",
            thick=True,
            color="A1",
            draw=True,
            opt="->",
        )
        pic.draw("(prog)", topath("(forprog)"), inclarrow=True)
        pic.draw("(forprog)", topath("(foi)"), inclarrow=True)
        pic.draw("(foi)", topath("(fot)"), inclarrow=True)
        pic.draw("(fot)", topath("(mona)"), inclarrow=True)
        pic.draw("(fot)", topath("(smtlib2)"), inclarrow=True)
        pic.draw("(fot)", topath("(altergo)"), inclarrow=True)
        pic.draw("(fo)", topath("(2,0)"), inclarrow=True)

        if self.status.get("prog", "unknown") == "validated":
            pic.node(
                r"\includegraphics[width=2cm]{images/cliparts/simple-for-programs.png}",
                at=(-8, 2),
            )

        if self.status.get("forprog", "unknown") == "validated":
            pic.node(
                r"\includegraphics[width=2cm]{images/cliparts/simple-for-program-simple.pdf}",
                at=(-4, 2),
            )

        if self.status.get("foi", "unknown") == "validated":
            pic.node(
                r"\includegraphics[width=2cm]{images/cliparts/fo-interp-spap-as-to-bs.pdf}",
                at=(-0, 2),
            )

    def __iter__(self):
        yield (0, self)


@dataclass
class LowToFOI:
    show_tags: bool = True
    show_arities: bool = True
    show_out: bool = True
    show_order: bool = True
    show_domain: bool = True
    show_progformulas: bool = True

    def draw(self, pic: Picture):
        pic.node(
            "Compiling to First Order",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        pic.node(
            r"\includegraphics[width=8cm]{images/cliparts/simple-for-program-simple.pdf}",
            at=(-5, 0),
            anchor="center",
            fill="white",
            draw=True,
            rounded_corners="5pt",
        )

        if self.show_tags:
            pic.node("$t_1$", at=(-4, -0.2), font=r"\tiny")
            pic.node("$t_2$", at=(-4, -0.4), font=r"\tiny")
            pic.node("$t_3$", at=(-4, -2.1), font=r"\tiny")

        sc = pic.scope(xshift="0cm", yshift="2.5cm")

        sc.node(
            r"""\textbf{Tags}: $\mathsf{tags} = \{t_1, t_2, t_3\}$""",
            anchor="north west",
            text_width="5cm",
            at=(0, 0),
            opacity=(1 if self.show_tags else 0),
        )

        sc.node(
            r"""\textbf{Arities}: $\mathsf{ar}(t_1) = 2, \mathsf{ar}(t_2) = 1, \mathsf{ar}(t_3) = 1$""",
            anchor="north west",
            text_width="8cm",
            at=(0, -0.5),
            opacity=(1 if self.show_arities else 0),
        )
        sc.node(
            r"""\textbf{Out}: $\mathsf{out}(t_1) = j$, 
                                  $\mathsf{out}(t_2) = \texttt{space}$,
                                  $\mathsf{out}(t_3) = j$""",
            anchor="north west",
            text_width="8cm",
            at=(0, -1),
            opacity=(1 if self.show_out else 0),
        )
        sc.node(
            r"""\textbf{Order}: Lexicographic based on positions (QF)""",
            anchor="north west",
            text_width="8cm",
            at=(0, -1.5),
            opacity=(1 if self.show_order else 0),
        )

        sc.node(
            r"""\textbf{Domain}: ... difficult part!""",
            anchor="north west",
            text_width="8cm",
            at=(0, -2),
            opacity=(1 if self.show_domain else 0),
        )

        sc.node(
            r"""values of the boolean variables?""",
            anchor="north west",
            text_width="8cm",
            color="A5",
            font="\\large\\bfseries",
            at=(0, -3),
            opacity=(1 if self.show_domain else 0),
        )

        pic.node(
            r"""\textbf{Program formulas} 
                 \begin{itemize}
                 \item $\mathsf{FO}$ + input (pos,bool) / output (bool)
                 \item Can be composed easily
                 \item Can implement if-then-else
                 \item Can implement loops
                 \end{itemize}
                 One can write a program formula to 
                 compute the boolean variables
                 at a given program position.
                 """,
            at=(0, 0),
            text_width="8cm",
            fill="white",
            draw=True,
            thick=True,
            rounded_corners="5pt",
            inner_sep="5mm",
            opacity=(1 if self.show_progformulas else 0),
        )

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self,
                show_tags=False,
                show_arities=False,
                show_out=False,
                show_order=False,
                show_domain=False,
                show_progformulas=False,
            ),
        )
        for i in range(1, 7):
            yield (
                1,
                dataclasses.replace(
                    self,
                    show_tags=(i >= 1),
                    show_arities=(i >= 2),
                    show_out=(i >= 3),
                    show_order=(i >= 4),
                    show_domain=(i >= 5),
                    show_progformulas=(i >= 6),
                ),
            )


@dataclass
class FOToSolvers:
    show_mona: bool = True
    show_smtl: bool = True
    show_desc: bool = True
    show_tabl: bool = True
    show_towr: bool = True

    def draw(self, pic: Picture):
        pic.node(
            "Calling solvers for help",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        monasc = pic.scope(
            xshift="-5cm", yshift="3cm", opacity=(1 if self.show_mona else 0)
        )
        smtlib = pic.scope(
            xshift="5cm", yshift="3cm", opacity=(1 if self.show_smtl else 0)
        )

        monasc.node(
            r"MONA", at=(0, 0), anchor="center", font="\\Large\\scshape", color="A1"
        )

        monasc.node(r"\textbf{Solves}: WS1S/WS2S over words", at=(0, -1))

        monasc.draw((-3, -2), rectangle((3, -1.8)))
        monasc.draw((-3, -2), rectangle((-2, -1.8)))
        monasc.node(
            r"$\mathsf{tags}$", at=(-2.5, -2.5), anchor="center", font="\\large"
        )
        monasc.node(r"$w$", at=(0.5, -2.5), anchor="center", font="\\large")

        monasc.node(
            r"Complete but slow",
            at=(0, -4),
            font=r"\bfseries",
            color="A2",
            opacity=(1 if self.show_desc else 0),
        )

        smtlib.node(
            r"SMTLib2", at=(0, 0), anchor="center", font="\\Large\\scshape", color="A1"
        )

        smtlib.node(r"\textbf{Solves}: First order theories", at=(0, -1))

        smtlib.node(
            r"""
                    \begin{itemize}
                    \item \texttt{DT}: $\mathsf{tags}$ 
                    \item \texttt{UF}: $w \colon \mathbb{N} \to A + \bot$
                    \item \texttt{LIA}: positions 
                    \end{itemize}
                    """,
            at=(0, -2),
            text_width="5cm",
        )

        smtlib.node(
            r"Incomplete but fast",
            at=(0, -4),
            font=r"\bfseries",
            color="A2",
            opacity=(1 if self.show_desc else 0),
        )

        pic.node(
            r"\includegraphics[width=8cm]{images/cliparts/polycheck-sizes.pdf}",
            at=(0, -1),
            anchor="center",
            fill="white",
            draw=True,
            rounded_corners="5pt",
            opacity=(1 if self.show_tabl else 0),
        )

        pic.node(
            r"$\mathsf{FO}$ model checking on words is $\mathsf{TOWER}$-complete [Stockmeyer, 1974]",
            at=(0, -1),
            text_width="5cm",
            font=r"\large\bfseries",
            color="C3",
            rotate="20",
            opacity=(1 if self.show_towr else 0),
        )

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self,
                show_mona=False,
                show_smtl=False,
                show_desc=False,
                show_tabl=False,
                show_towr=False,
            ),
        )

        for i in range(1, 6):
            yield (
                1,
                dataclasses.replace(
                    self,
                    show_mona=(i >= 1),
                    show_smtl=(i >= 2),
                    show_desc=(i >= 3),
                    show_tabl=(i >= 4),
                    show_towr=(i >= 5),
                ),
            )


@dataclass
class HighToLow:
    show_gen: bool = True
    show_sam: bool = True
    show_rew: bool = True
    show_dif: bool = True

    def draw(self, pic: Picture):
        pic.node(
            "From High to Low",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        gensc = pic.scope(xshift="-9cm", yshift="3cm")

        gensc.node(
            r"""\textbf{New operator:} generator expressions.
                 \begin{itemize}
                 \item $\mathsf{gen}( s )$ 
                 \item Can be used in place of a list / boolean
                 \item Captures list variables but not boolean variables
                 \item Simulate function calls
                 \end{itemize}
                 """,
            at=(0, 0),
            anchor="north west",
            text_width="8cm",
            opacity=(1 if self.show_gen else 0),
        )

        gensc.node(
            r"""\textbf{Example code:}
                   \newline
                   \texttt{for (i,x) in enumerate(gen( expr )) ...}""",
            at=(0, -2.5),
            anchor="north west",
            text_width="8cm",
            opacity=(1 if self.show_sam else 0),
        )

        gensc.node(
            r"""\textbf{Easy rewriting steps:}
                   \begin{enumerate}
                   \item Remove literals
                   \item Remove functions
                   \item Remove boolean generators
                   \item Remove let expressions
                   \item Push boolean introductions upwards
                   \end{enumerate}""",
            at=(0, -3.7),
            anchor="north west",
            text_width="8cm",
            opacity=(1 if self.show_rew else 0),
        )

        codesc = pic.scope(
            xshift="1cm", yshift="3cm", opacity=(1 if self.show_dif else 0)
        )
        codesc.draw(
            (-0.5, 0.5),
            rectangle((8.5, -7.5)),
            opt="rounded corners=5pt",
            fill="white",
            draw=True,
            thick=True,
        )

        codesc.node(
            r"""\textbf{Print all but first}, program ``$s$''
                    \begin{verbatim}
b = False
for (i,x) in enumerate(u):
    if b:
        yield x
    else:
        b = True
                    \end{verbatim}
                    """,
            at=(0, 0),
            anchor="north west",
            text_width="8cm",
        )

        codesc.node(
            r"""What are the following
                        programs doing?""",
            font=r"\bfseries",
            color="A2",
            at=(0, -4),
            anchor="north west",
            text_width="8cm",
        )

        codesc.node(
            r"""
                    \begin{verbatim}
for (i,x) in reverse(enumerate(s)):
    yield x
                    \end{verbatim}
                    """,
            at=(0, -4.5),
            anchor="north west",
            text_width="4cm",
            color="A5",
        )

        codesc.node(
            r"""
                    \begin{verbatim}
for (i,x) in enumerate(s):
    yield x
                    \end{verbatim}
                    """,
            at=(0, -5.5),
            anchor="north west",
            text_width="4cm",
            color="A3",
        )

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self,
                show_gen=False,
                show_sam=False,
                show_rew=False,
                show_dif=False,
            ),
        )
        for i in range(1, 5):
            yield (
                1,
                dataclasses.replace(
                    self,
                    show_gen=(i >= 1),
                    show_sam=(i >= 2),
                    show_rew=(i >= 3),
                    show_dif=(i >= 4),
                ),
            )


@dataclass
class ForwardLoopElimination:
    show_idea: bool = True
    show_prob: bool = True
    show_solu: bool = True
    show_code_outer: bool = True
    show_code_inner: bool = True
    show_code_body: bool = True

    def draw(self, pic: Picture):
        pic.node(
            "Forward Loop Elimination",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        pic.node(
            r"""
                 \begin{verbatim}
for (i,x) in enumerate(s):
    for (j,y) in enumerate(s):
        if i == j:
            yield x
                 \end{verbatim}
                 """,
            at=(-9, 4),
            anchor="north west",
            text_width="8cm",
            color="A5",
        )

        pic.node(
            r"""
                 \textbf{Idea:}
                 substitute the body of the loop
                 in $s$.
                 \newline
                 $s[ \mathsf{yield} e \mapsto ... ]$.
                 """,
            at=(-9, 1.5),
            anchor="north west",
            text_width="8cm",
            opacity=(1 if self.show_idea else 0),
        )
        pic.node(
            r"""
                 \textbf{Problem:}
                 We lost the index variable $i$!
                 """,
            at=(-9, 0),
            anchor="north west",
            text_width="8cm",
            color="A2",
            font=r"\bfseries",
            opacity=(1 if self.show_prob else 0),
        )

        pic.node(
            r"""\textbf{Solution:}
                 \begin{itemize}
                 \item $i$ can only be used
                 in tests
                 \item $i$ can only be tested
                 against positions of $s$
                 \item we can replace 
                 $i = j$ by an
                 \textbf{order formula}
                 \end{itemize}
                 """,
            at=(-9, -1.5),
            color="B4",
            text_width="8cm",
            anchor="north west",
            opacity=(1 if self.show_solu else 0),
        )

        if self.show_code_outer:
            pic.draw((0.5, 3.5), rectangle((8, -3)), fill="D4hint")

        if self.show_code_inner:
            pic.draw((1.5, 1.7), rectangle((8, -1.2)), fill="B4hint")

        if self.show_code_body:
            pic.draw((2.6, 0.5), rectangle((8, -0.4)), fill="A4hint")

        pic.node(
            r"""
                 \begin{verbatim}
b1 = False
for (i1,x1) in enumerate(s):
    if b1:
        b2 = False
        for (i2,x2) in enumerate(s):
            if b2:
                if i1 = i2:
                    yield x1
            else:
                b2 = True
    else:
        b1 = True
                 \end{verbatim}""",
            at=(1, 3.5),
            anchor="north west",
            text_width="8cm",
        )

        if not self.show_code_outer:
            pic.draw((0.5, 3.5), rectangle((8, -3)), draw="white", fill="white")

        if not self.show_code_inner:
            pic.draw((1.5, 1.7), rectangle((8, -1.2)), draw="white", fill="white")

        if not self.show_code_body:
            pic.draw((2.6, 0.5), rectangle((8, -0.4)), draw="white", fill="white")

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self,
                show_idea=False,
                show_prob=False,
                show_solu=False,
                show_code_outer=False,
                show_code_inner=False,
                show_code_body=False,
            ),
        )
        for i in range(1, 7):
            yield (
                1,
                dataclasses.replace(
                    self,
                    show_idea=(i >= 1),
                    show_prob=(i >= 2),
                    show_solu=(i >= 3),
                    show_code_outer=(i >= 4),
                    show_code_inner=(i >= 5),
                    show_code_body=(i >= 6),
                ),
            )


@dataclass
class BackwardLoopElimination:
    show_prob: bool = True
    show_solu: bool = True
    show_remk: bool = True
    show_code_outer: bool = True
    show_code_inner: bool = True
    show_code_body: bool = True

    def draw(self, pic: Picture):
        pic.node(
            "Backward Loop Elimination",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        pic.node(
            r"""
                    \begin{verbatim}
for (i,x) in reverse(enumerate(s)):
    yield x
                    \end{verbatim}
                    """,
            at=(-9, 3.5),
            anchor="north west",
            text_width="4cm",
            color="A5",
        )

        pic.node(
            r"""\textbf{Problem:} reverse
                 a non reversible computation!
                 """,
            at=(-9, 2),
            color="A2",
            anchor="north west",
            font=r"\bfseries",
            text_width="8cm",
            opacity=(1 if self.show_prob else 0),
        )

        pic.node(
            r"""\textbf{Solution:} 
                 \begin{itemize}
                 \item Compute a \emph{superset}
                 of the reachable yields in the reversed order
                 \item For every yield, check that 
                 it would be reachable
                 \item If so, perform the rest of
                 the computation
                 \end{itemize}
                 """,
            at=(-9, 1),
            color="B4",
            anchor="north west",
            text_width="8cm",
            opacity=(1 if self.show_solu else 0),
        )

        pic.node(
            r"""\textbf{Remark:} this is the proof
                 that \emph{polyregular functions} are
                 closed under composition.""",
            at=(-9, -2),
            font=r"\itshape",
            color="B1",
            text_width="8cm",
            anchor="north west",
            opacity=(1 if self.show_remk else 0),
        )

        if self.show_code_outer:
            pic.draw((0.5, 2.5), rectangle((8, -1.6)), fill="D4hint")

        if self.show_code_inner:
            pic.draw((1.5, 1.6), rectangle((8, -1.4)), fill="B4hint")

        if self.show_code_body:
            pic.draw((2.5, 0.3), rectangle((8, -0.6)), fill="A4hint")

        pic.node(
            r"""
                 \begin{verbatim}
for (i1, x1) in reversed(enumerate(u)):
    for (i2, x2) in enumerate(u):
        b2 = False
        if b2:
            if i1 = i2:
                yield x1
        else:
            b2 = True
                  \end{verbatim}""",
            at=(1, 2.5),
            anchor="north west",
            text_width="8cm",
            opacity=(1 if self.show_code_outer else 0),
        )

        if not self.show_code_outer:
            pic.draw((0.5, 2.5), rectangle((8, -1.6)), draw="white", fill="white")
        if not self.show_code_inner:
            pic.draw((1.5, 1.6), rectangle((8, -1.4)), draw="white", fill="white")
        if not self.show_code_body:
            pic.draw((2.5, 0.3), rectangle((8, -0.6)), draw="white", fill="white")

    def __iter__(self):
        yield (
            0,
            dataclasses.replace(
                self,
                show_prob=False,
                show_solu=False,
                show_remk=False,
                show_code_outer=False,
                show_code_inner=False,
                show_code_body=False,
            ),
        )

        for i in range(1, 7):
            yield (
                1,
                dataclasses.replace(
                    self,
                    show_prob=(i >= 1),
                    show_solu=(i >= 2),
                    show_remk=(i >= 3),
                    show_code_outer=(i >= 4),
                    show_code_inner=(i >= 5),
                    show_code_body=(i >= 6),
                ),
            )


@dataclass
class Conclusion:
    def draw(self, pic: Picture):
        pic.node(
            "In the end...",
            at=(-9, 4),
            anchor="west",
            font="\\huge\\scshape",
            color="A2",
        )

        pic.node(
            r"\includegraphics[width=8cm]{images/cliparts/cav-polycheck-stars.pdf}",
            at=(0, 2),
            anchor="center",
            fill="white",
            draw=True,
            rounded_corners="5pt",
        )

        pic.node(
            r"""\textbf{Future work:}
                 \begin{itemize}
                 \item Comparison with other models
                 \item Better interface with solvers
                 \item Composable checks
                 \item Monadic second order logic
                 \end{itemize}""",
            at=(2, 0),
            anchor="north west",
            text_width="7cm",
        )

        pic.node(
            r"""\textbf{And more:}
                 \begin{itemize}
                 \item Haskell implementation + webapp
                 \item Nix / Docker / reproducible builds
                 \item Symbolic alphabets
                 \item Some optimisations
                 \end{itemize}""",
            at=(-9, 0),
            anchor="north west",
            text_width="8cm",
        )

        pic.node(
            r"\qrcode{https://github.com/AliaumeL/polyregular-model-checking}",
            at=(0, -2),
            anchor="center",
            font="\\large",
        )

    def __iter__(self):
        yield (0, self)


if __name__ == "__main__":
    tc = TableOfColors()
    tt = TitleFrame()

    cfg = PresConfig(
        title="Polyczek",
        author="Aliaume Lopez",
        location="IRIF",
        date="2025-06-13",
        draft=False,
    )

    architecture = Architecture.default()

    frames_list = [
        tt,
        ModelChecking(),
        ContinuousOrNot.default(),
        TransducerModels.default(),
        Polyreg(),
        HighLevelForPrograms(),
        DemoTime(),
        architecture,
        dataclasses.replace(
            architecture,
            status={
                **architecture.status,
                "prog": "validated",
            },
        ),
        LowLevelForPrograms(),
        dataclasses.replace(
            architecture,
            status={
                **architecture.status,
                "prog": "validated",
                "forprog": "validated",
            },
        ),
        FirstOrderInterpretations.default(),
        dataclasses.replace(
            architecture,
            status={
                **architecture.status,
                "prog": "validated",
                "forprog": "validated",
                "foi": "validated",
            },
        ),
        FirstOrderLogicWithTags(),
        dataclasses.replace(
            architecture,
            status={
                **architecture.status,
                "prog": "validated",
                "forprog": "validated",
                "foi": "validated",
                "fot": "validated",
            },
        ),
        FOToSolvers(),
        dataclasses.replace(
            architecture,
            status={
                "prog": "validated",
                "forprog": "validated",
                "foi": "validated",
                "fot": "validated",
                "mona": "validated",
                "smtlib2": "validated",
                "altergo": "validated",
            },
        ),
        LowToFOI(),
        SequentialAnimation(
            [
                HighToLow(),
                ForwardLoopElimination(),
                BackwardLoopElimination(),
            ],
            pos=0,
        ),
        Conclusion(),
    ]

    frames = Sequential(frames_list, pos=0)

    cfg.preview(frames)
