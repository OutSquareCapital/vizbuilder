# VizBuilder

A Python library for building interactive data visualizations with Plotly and Polars.
Implement a builder pattern for creating complex visualizations step-by-step.

## Installation

```bash
uv add git+https://github.com/OutSquareCapital/vizbuilder.git
```

## Developpement

### Literal Palettes

Run the following script to update the `Palettes` Literal in `_scales.py` whenever new color palettes are added or existing ones are modified.

```bash
uv run scripts/build_palettes.py
```

### Doctests

Run the following script to execute all doctests in the `vizbuilder` package.

```bash
uv run tests/doctests.py
```
