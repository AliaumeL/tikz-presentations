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

# create a presentation

if __name__ == "__main__":
    tf = TitleFrame(with_name=True)

    frames = Sequential([tf], pos=0)

    preview_animation(frames)
