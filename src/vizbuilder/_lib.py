from typing import Self

import plotly.graph_objects as go
import polars as pl

from ._colors import palette_from_df
from ._scales import PALETTES, Palettes
from ._types import DataFrameCompatible, FigureFunc, Templates


class Displayer:
    group: str
    template: Templates
    color_discrete_map: dict[str, str]
    __slots__ = ("group", "template", "color_discrete_map")

    def __init__(
        self,
        df: pl.LazyFrame,
        group: str,
        palette: Palettes = "Plotly",
        template: Templates = "plotly",
    ) -> None:
        self.group = group
        self.template = template
        self.color_discrete_map = df.pipe(
            palette_from_df, self.group, PALETTES[palette]
        )

    @classmethod
    def from_df_like(cls, df_like: DataFrameCompatible, group: str) -> Self:
        return cls(pl.from_dataframe(df_like).lazy(), group)

    def plot[**P](
        self,
        func: FigureFunc[P],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> go.Figure:
        """
        Build and return a Plotly figure using the provided function and stored data.
        """
        return func(
            *args,
            **kwargs,
            color=self.group,  # type: ignore[arg-type]
            template=self.template,  # type: ignore[arg-type]
            color_discrete_map=self.color_discrete_map,  # type: ignore[arg-type]
        )  # type: ignore[arg-type]

    def set_group(self, group: str) -> Self:
        """
        Set the grouping column for the graphs and return self.
        """
        self.group = group
        return self
