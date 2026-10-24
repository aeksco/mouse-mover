"""Export a model from models/<name>.py to build/<name>.{stl,step,obj,png}.

The PNG is a shaded isometric render for a quick visual check.

Usage: uv run python scripts/export.py <name> [--view]
"""

import argparse
import importlib
import sys
from pathlib import Path

from build123d import export_obj, export_step, export_stl

from render import render_isometric

ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / "build"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="module name in models/, e.g. 'example'")
    parser.add_argument("--view", action="store_true", help="show in OCP viewer")
    args = parser.parse_args()

    sys.path.insert(0, str(ROOT))
    module = importlib.import_module(f"models.{args.name}")
    shape = module.build()

    if not shape.is_valid:
        print(f"error: {args.name}.build() produced an invalid shape", file=sys.stderr)
        return 1

    BUILD_DIR.mkdir(exist_ok=True)
    stl_path = BUILD_DIR / f"{args.name}.stl"
    step_path = BUILD_DIR / f"{args.name}.step"
    export_stl(shape, str(stl_path))
    export_step(shape, str(step_path))
    obj_path = BUILD_DIR / f"{args.name}.obj"
    export_obj(shape, str(obj_path))
    png_path = BUILD_DIR / f"{args.name}.png"
    render_isometric(shape, png_path)

    bb = shape.bounding_box()
    print(f"volume: {shape.volume:.1f} mm^3")
    print(f"bbox:   {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm")
    written = ", ".join(str(p.relative_to(ROOT)) for p in (stl_path, step_path, obj_path, png_path))
    print(f"wrote:  {written}")

    if args.view:
        from ocp_vscode import show

        show(shape)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
