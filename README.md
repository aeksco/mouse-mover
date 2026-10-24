<div align="center">

<img src="docs/example.png" alt="Isometric render of the example bracket" width="360">

# build123d starter

**Parametric, 3D-printable parts in Python.**

Write a model with [build123d](https://build123d.readthedocs.io), run `make`, get STL, STEP and OBJ files plus an isometric PNG preview.

![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white)
![build123d](https://img.shields.io/badge/CAD-build123d-4A7BB7)
![uv](https://img.shields.io/badge/deps-uv-DE5FE9)
![Outputs](https://img.shields.io/badge/outputs-STL%20%C2%B7%20STEP%20%C2%B7%20OBJ%20%C2%B7%20PNG-555)

</div>

---

Requires [uv](https://docs.astral.sh/uv/) and make.

```sh
make setup              # install deps into .venv (run once)
make                    # export build/example.{stl,step,obj,png}
make MODEL=mypart       # export models/mypart.py
make stl MODEL=mypart   # export only if build/mypart.stl is stale
make step MODEL=mypart  # export only if build/mypart.step is stale
make obj MODEL=mypart   # export only if build/mypart.obj is stale
make png MODEL=mypart   # export only if build/mypart.png is stale
make view MODEL=mypart  # export and show in the OCP viewer (needs it running)
make list               # list available models
make clean              # delete build/
make help               # show all targets
```

One exporter run writes all four files, so `stl`, `step`, `obj` and `png` each
rebuild everything when the model is out of date.

Add a part by copying `models/example.py`; each model defines `build()`.
See `CLAUDE.md` for conventions (written for AI agents, useful for humans too).

To reuse as a template: copy this folder, delete `.git`, `build/` and `.venv/`, rename the project in `pyproject.toml`, and replace `models/example.py`.

---

<p align="center">Built with ❤️ by <a href="https://x.com/aeksco">aeksco</a></p>
