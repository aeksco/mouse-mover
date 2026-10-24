"""Mocked-up Seeed Studio XIAO: PCB, castellated pads, USB-C receptacle, shield, buttons.

Approximate, for checking fit inside the enclosure. Not for printing.
All dimensions live in models/xiao_enclosure.py.
"""

from build123d import Compound

from models.xiao_enclosure import xiao_board


def build() -> Compound:
    return Compound(children=xiao_board(), label="xiao_board")
