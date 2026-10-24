"""Printable top half of the XIAO enclosure, flipped so the roof is on the bed.

All dimensions live in models/xiao_enclosure.py.
"""

from build123d import Part

from models.xiao_enclosure import enclosure_halves, top_for_printing


def build() -> Part:
    _bottom, top = enclosure_halves()
    return top_for_printing(top)
