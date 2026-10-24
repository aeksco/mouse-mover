# CLAUDE.md

This is a **build123d starter project** for parametric, 3D-printable parts. The
scaffolding (uv, Makefile, exporter) is done. Your job is usually just to
write or edit a model in `models/`. Don't re-create the scaffolding.

## Quick start

```sh
make setup              # once: uv sync (Python 3.12 venv in .venv)
make                    # export build/example.{stl,step,obj,png}
make MODEL=<name>       # export models/<name>.py
make list               # list models
make clean              # delete build/
make view MODEL=<name>  # push to OCP viewer (optional; needs viewer running)
```

Outputs land in `build/` (gitignored): `<name>.stl` for slicers, `<name>.step`
for CAD, `<name>.obj` for mesh tools, `<name>.png` an isometric render. Look at
the PNG to check the shape visually.

## Layout

```
models/<name>.py     one file per part; must define build() -> Part
scripts/export.py    generic exporter; imports models.<name>, calls build(), writes STL+STEP+OBJ+PNG
scripts/render.py    shaded isometric PNG render (numpy z-buffer, headless); colours parts by `.color`
scripts/check_fit.py overlap + clearance check for the XIAO enclosure parts (run before printing)
Makefile             thin wrapper around the exporter
pyproject.toml       deps managed by uv (build123d, numpy, pillow; ocp-vscode as dev dep)
```

## This project: XIAO USB-C enclosure

`models/xiao_enclosure.py` holds every dimension and all the geometry for a
two-part (glued) enclosure around a Seeed XIAO with a USB-C cable plugged in.
The other `models/*.py` files are thin wrappers that import from it:
`enclosure_bottom` and `enclosure_top` are the printable halves (top is
pre-flipped), `xiao_board` is the mock board, `enclosure_exploded` is the
exploded assembly, and `xiao_enclosure` itself builds the closed assembly.
Edit constants only in `xiao_enclosure.py`, then `make MODEL=<name>` and
`uv run python scripts/check_fit.py`.

## Making a new part

1. Copy `models/example.py` to `models/<name>.py` (or edit it in place for a one-off).
2. Keep **all dimensions as named constants at the top, in mm**. No magic numbers in geometry code.
3. Keep `build()` pure: no I/O, no `show()`, return the shape (`part.part` for `BuildPart`).
4. Run `make MODEL=<name>`. The exporter fails if the shape is invalid and prints
   volume and bounding box. Check those against what you intended.
5. To rename the project, edit `name` in `pyproject.toml`.

## build123d notes and gotchas

- Use the builder API (`with BuildPart() as p:`) and return `p.part`.
- Z is up. Use `Align.MIN` on Z to sit a box on the XY plane.
- `Mode.SUBTRACT` cuts holes; give cutters extra length so they pass fully through.
- Fillet/chamfer **early**, on simple geometry, before unioning more features.
  Filleting edges at junctions of merged solids often raises
  `Failed creating a fillet`; use a smaller radius, `max_fillet()`, or restructure.
- Docs: https://build123d.readthedocs.io
- Verify output programmatically (volume, `bounding_box()`, `is_valid`) rather than assuming.

## 3D-printing defaults to design for (FDM)

- Min wall ~1.2 mm; holes print slightly small, so add ~0.2 mm clearance for fits.
- Avoid overhangs > 45° or orient the part to avoid them; prefer a flat face on the bed.
- Export units are mm.

## Dependencies

Add with `uv add <pkg>`; never use bare `pip`. Python is pinned to 3.12 in
`.python-version` because the OCP (OpenCascade) wheels lag newer Pythons.
