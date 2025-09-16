from typing import Literal, Protocol

import plotly.graph_objects as go
import polars as pl
import pychain as pc
from plotly.express.colors import cyclical, qualitative, sequential


class Swatchable(Protocol):
    def swatches(self) -> go.Figure: ...


MODULES: dict[str, Swatchable] = {
    "sequential": sequential,
    "cyclical": cyclical,
    "qualitative": qualitative,
}
Modules = Literal["sequential", "cyclical", "qualitative"]


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


def get_palettes() -> dict[str, list[str]]:
    df: pl.DataFrame = (
        pc.Iter(MODULES.values())
        .map(
            lambda mod: pc.Dict(mod.__dict__)
            .filter_values(lambda v: isinstance(v, list))
            .unwrap()
        )
        .pipe_into(pl.LazyFrame)
        .unpivot(value_name="color", variable_name="scale")
        .drop_nulls()
        .filter(
            pl.col("color")
            .list.eval(pl.element().first().str.starts_with("#").alias("is_hex"))
            .list.first()
        )
        .sort("scale")
        .collect()
    )

    return (
        pc.Iter(df.get_column("scale").to_list())
        .zip(df.get_column("color").to_list())
        .pipe_into(dict)
    )


PALETTES: dict[str, list[str]] = get_palettes()
# START MARKER
Palettes = Literal[
    "Alphabet",
    "Alphabet_r",
    "Cividis",
    "Cividis_r",
    "D3",
    "D3_r",
    "Dark24",
    "Dark24_r",
    "Edge",
    "Edge_r",
    "G10",
    "G10_r",
    "HSV",
    "HSV_r",
    "IceFire",
    "IceFire_r",
    "Inferno",
    "Inferno_r",
    "Light24",
    "Light24_r",
    "Magma",
    "Magma_r",
    "Plasma",
    "Plasma_r",
    "Plotly",
    "Plotly3",
    "Plotly3_r",
    "Plotly_r",
    "T10",
    "T10_r",
    "Turbo",
    "Turbo_r",
    "Twilight",
    "Twilight_r",
    "Viridis",
    "Viridis_r",
    "mrybm",
    "mrybm_r",
    "mygbm",
    "mygbm_r",
]
# END MARKER
