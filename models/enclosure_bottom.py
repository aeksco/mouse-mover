"""Printable bottom half of the XIAO enclosure (floor on the bed, lip up).

All dimensions live in models/xiao_enclosure.py.
"""

from build123d import Part

from models.xiao_enclosure import enclosure_halves


def build() -> Part:
    bottom, _top = enclosure_halves()
    return bottom
