# Usage: make [MODEL=example] <target>
MODEL ?= example
RUN   := uv run python

.PHONY: all stl step obj png setup view clean list help

all: build/$(MODEL).stl build/$(MODEL).step build/$(MODEL).obj build/$(MODEL).png ## Export STL + STEP + OBJ + isometric PNG for MODEL (default: example)

stl: build/$(MODEL).stl ## Export STL only
step: build/$(MODEL).step ## Export STEP only
obj: build/$(MODEL).obj ## Export OBJ only
png: build/$(MODEL).png ## Export isometric render only

# All outputs come from one run; rebuild when any model (they share code) or the exporter changes.
build/$(MODEL).stl build/$(MODEL).step build/$(MODEL).obj build/$(MODEL).png: models/$(MODEL).py $(wildcard models/*.py) scripts/export.py scripts/render.py
	$(RUN) scripts/export.py $(MODEL)

setup: ## Install dependencies into .venv
	uv sync

view: ## Export and show in the OCP viewer (needs `python -m ocp_vscode` or the VS Code extension)
	$(RUN) scripts/export.py $(MODEL) --view

list: ## List available models
	@ls models/*.py | grep -v __init__ | xargs -n1 basename | sed 's/\.py$$//'

clean: ## Remove build outputs
	rm -rf build

help: ## Show targets
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/'
