from typing import Self

import plotly.graph_objects as go
import polars as pl

from ._colors import palette_from_df
from ._scales import PALETTES, Palettes
from ._types import DataFrameCompatible, FigureFunc, Templates


class Displayer:
    df: pl.LazyFrame
    group: str
    template: Templates
    palette: list[str]
    color_discrete_map: dict[str, str]

    def __init__(
        self,
        df: pl.LazyFrame,
        group: str,
        palette: Palettes = "Plotly",
        template: Templates = "plotly",
    ) -> None:
        self.df = df
        self.group = group
        self.template = template
        self.palette = PALETTES[palette]
        self.color_discrete_map = self.df.pipe(
            palette_from_df, self.group, self.palette
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
            self.df.collect(),
            *args,
            **kwargs,
            color=self.group,  # type: ignore[arg-type]
            template=self.template,  # type: ignore[arg-type]
            color_discrete_map=self.color_discrete_map,  # type: ignore[arg-type]
        )  # type: ignore[arg-type]

    def set_palette(self, palette: Palettes) -> Self:
        """
        Set the color map using a predefined Plotly color scale and return self.
        """
        self.palette = PALETTES[palette]
        return self._update()

    def set_group(self, group: str) -> Self:
        """
        Set the grouping column for the graphs and return self.
        """
        self.group = group
        return self._update()

    def _update(self) -> Self:
        self.color_discrete_map = self.df.pipe(
            palette_from_df, self.group, self.palette
        )
        return self
