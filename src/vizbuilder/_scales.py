from types import ModuleType
from typing import Literal

import polars as pl
import pychain as pc
from plotly.express.colors import cyclical, qualitative, sequential

MODULES: set[ModuleType] = {
    sequential,
    cyclical,
    qualitative,
}


def get_palettes() -> pc.Dict[str, list[str]]:
    df: pl.DataFrame = (
        pc.Iter(MODULES)
        .map(
            lambda mod: pc.dict_of(mod)
            .filter_values(lambda v: isinstance(v, list))
            .unwrap()
        )
        .pipe_unwrap(pl.LazyFrame)
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
    return pc.dict_zip(
        keys=df.get_column("scale").to_list(), values=df.get_column("color").to_list()
    )


PALETTES: dict[str, list[str]] = get_palettes().unwrap()

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
