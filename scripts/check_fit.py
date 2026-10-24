"""Check that the XIAO enclosure parts fit: no overlaps, expected clearances.

Run after changing constants in models/xiao_enclosure.py and before printing:

    uv run python scripts/check_fit.py

Exits non-zero if any pair of parts intersects or a clearance is off.
"""

import sys
from pathlib import Path

from build123d import Align, Compound, Cylinder, Location

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from models import xiao_enclosure as E  # noqa: E402

TOL = 0.01  # mm


def main() -> int:
    bottom, top = E.enclosure_halves()
    board_at = Location((E.X_PCB0 + E.PCB_L / 2, 0, E.Z_PCB0))
    plug_at = Location((E.X_PLUG0, 0, E.Z_AXIS))
    board_parts = [p.moved(board_at) for p in E.xiao_board()]
    board = Compound(children=board_parts)
    leds = next(p for p in board_parts if p.label == "leds")
    # Column of light from the LEDs up through the roof: nothing of the top may block it,
    # and every LED package must sit inside it
    beam = Cylinder(
        E.LED_HOLE_D / 2 - TOL,
        E.OUTER_H + 1 - E.Z_PCB1,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((E.X_LED, E.Y_LED, E.Z_PCB1)))
    plug = Compound(children=[p.moved(plug_at) for p in E.usb_c_plug()])

    ok = True

    def report(name: str, value: float, expect: float, kind: str) -> None:
        nonlocal ok
        good = abs(value - expect) <= TOL if kind == "==" else value >= expect - TOL
        ok &= good
        print(f"{'ok ' if good else 'BAD'} {name:28s} {value:7.3f} mm  (want {kind} {expect:.3f})")

    print(f"enclosure {E.OUTER_L:.1f} x {E.OUTER_W:.1f} x {E.OUTER_H:.1f} mm, split at Z={E.Z_SPLIT:.2f}")
    for name, a, b in [
        ("top/bottom", top, bottom),
        ("board/bottom", board, bottom),
        ("board/top", board, top),
        ("plug/bottom", plug, bottom),
        ("plug/top", plug, top),
    ]:
        report(f"overlap {name}", (a & b).volume, 0.0, "==")
    report("gap board -> ribs", board.distance_to(top), E.PCB_FIT_Z, "==")
    report("gap board -> ledge", board.distance_to(bottom), 0.0, "==")
    # Tightest designed clearance around the plug: the bare cable in its hole,
    # or the housing in the bay, whichever is smaller
    plug_fit = min(
        (E.CABLE_HOLE_D - E.CABLE_D) / 2,
        (E.CABLE_BAY_W - E.PLUG_BODY_W) / 2,
        (E.CABLE_BAY_H - E.PLUG_BODY_H) / 2,
    )
    report("gap plug -> top", plug.distance_to(top), plug_fit, ">=")
    report("gap plug -> bottom", plug.distance_to(bottom), plug_fit, ">=")
    report("relief end -> end wall", E.X_BAY1 - E.X_RELIEF_END, E.CABLE_END_GAP, "==")
    report("lip height above split", bottom.bounding_box().max.Z - E.Z_SPLIT, E.LIP_H, "==")
    report("LED hole blocked by top", (beam & top).volume, 0.0, "==")
    report("LEDs outside hole", leds.volume - (beam & leds).volume, 0.0, "==")
    print("FIT OK" if ok else "FIT PROBLEM: see BAD lines above")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
