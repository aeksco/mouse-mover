"""Exploded assembly: bottom, mocked XIAO + plug, and top stacked apart vertically.

Shows how the board and cable sit inside the enclosure. Not for printing.
All dimensions live in models/xiao_enclosure.py.
"""

from build123d import Compound

from models.xiao_enclosure import assembly


def build() -> Compound:
    return assembly(exploded=True)
