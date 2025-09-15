from typing import Literal, Protocol

import plotly.graph_objects as go
from plotly.express.colors import cyclical, qualitative, sequential


class Swatchable(Protocol):
    def swatches(self) -> go.Figure: ...


Modules = Literal["sequential", "cyclical", "qualitative"]

MODULES: dict[str, Swatchable] = {
    "sequential": sequential,
    "cyclical": cyclical,
    "qualitative": qualitative,
}

PALETTES: dict[str, list[str]] = {
    "Cividis": sequential.Cividis,
    "Cividis_r": sequential.Cividis_r,
    "Inferno": sequential.Inferno,
    "Inferno_r": sequential.Inferno_r,
    "Magma": sequential.Magma,
    "Magma_r": sequential.Magma_r,
    "Plasma": sequential.Plasma,
    "Plasma_r": sequential.Plasma_r,
    "Plotly3": sequential.Plotly3,
    "Plotly3_r": sequential.Plotly3_r,
    "Turbo": sequential.Turbo,
    "Turbo_r": sequential.Turbo_r,
    "Viridis": sequential.Viridis,
    "Viridis_r": sequential.Viridis_r,
    "Edge": cyclical.Edge,
    "Edge_r": cyclical.Edge_r,
    "HSV": cyclical.HSV,
    "HSV_r": cyclical.HSV_r,
    "IceFire": cyclical.IceFire,
    "IceFire_r": cyclical.IceFire_r,
    "Twilight": cyclical.Twilight,
    "Twilight_r": cyclical.Twilight_r,
    "mrybm": cyclical.mrybm,
    "mrybm_r": cyclical.mrybm_r,
    "mygbm": cyclical.mygbm,
    "mygbm_r": cyclical.mygbm_r,
    "Alphabet": qualitative.Alphabet,
    "Alphabet_r": qualitative.Alphabet_r,
    "D3": qualitative.D3,
    "D3_r": qualitative.D3_r,
    "Dark24": qualitative.Dark24,
    "Dark24_r": qualitative.Dark24_r,
    "G10": qualitative.G10,
    "G10_r": qualitative.G10_r,
    "Light24": qualitative.Light24,
    "Light24_r": qualitative.Light24_r,
    "Plotly": qualitative.Plotly,
    "Plotly_r": qualitative.Plotly_r,
    "T10": qualitative.T10,
    "T10_r": qualitative.T10_r,
}
Palettes = Literal[
    "Cividis",
    "Cividis_r",
    "Inferno",
    "Inferno_r",
    "Magma",
    "Magma_r",
    "Plasma",
    "Plasma_r",
    "Plotly3",
    "Plotly3_r",
    "Turbo",
    "Turbo_r",
    "Viridis",
    "Viridis_r",
    "Edge",
    "Edge_r",
    "HSV",
    "HSV_r",
    "IceFire",
    "IceFire_r",
    "Twilight",
    "Twilight_r",
    "mrybm",
    "mrybm_r",
    "mygbm",
    "mygbm_r",
    "Alphabet",
    "Alphabet_r",
    "D3",
    "D3_r",
    "Dark24",
    "Dark24_r",
    "G10",
    "G10_r",
    "Light24",
    "Light24_r",
    "Plotly",
    "Plotly_r",
    "T10",
    "T10_r",
]


def get_palette(palette: Palettes) -> list[str]:
    return PALETTES[palette]


def show_scales(module: Modules) -> go.Figure:
    """
    Return a Plotly figure showing the color swatches.
    """
    return (
        MODULES[module]
        .swatches()
        .update_layout(
            title=None,
            height=550,
            width=400,
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
            paper_bgcolor="#181c1a",
        )
    )
