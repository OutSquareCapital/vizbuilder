from collections.abc import Callable
from typing import Self

import plotly.express as px
import polars as pl
from plotly.graph_objects import Figure

from ._colors import palette_from_df
from ._scales import PALETTES, Palettes
from ._types import (
    BarMode,
    DataFrameCompatible,
    DisplayMode,
    GraphKwargs,
    Points,
    Templates,
    TwoDGraphKwargs,
)


class Displayer:
    _df: pl.LazyFrame
    _log_x: bool
    _log_y: bool
    _group: str
    _template: Templates
    _color_discrete_map: dict[str, str]
    _width: int | None
    _height: int | None
    __slots__ = (
        "_df",
        "_log_x",
        "_log_y",
        "_group",
        "_template",
        "_color_discrete_map",
        "_width",
        "_height",
    )

    def __init__(
        self,
        df: pl.LazyFrame | pl.DataFrame,
        group: str,
        palette: Palettes = "Turbo",
        template: Templates = "plotly_dark",
    ) -> None:
        self._df = df.lazy()
        self._group = group
        self._template = template
        self._color_discrete_map = df.pipe(
            palette_from_df, self._group, PALETTES[palette]
        )
        self._log_x = False
        self._log_y = False
        self._width = None
        self._height = None

    @classmethod
    def from_df_like(cls, df_like: DataFrameCompatible, group: str) -> Self:
        return cls(pl.from_dataframe(df_like), group)

    @property
    def _common_kwargs(self) -> GraphKwargs:
        return GraphKwargs(
            template=self._template,
            width=self._width,
            height=self._height,
            color=self._group,
            color_discrete_map=self._color_discrete_map,
        )

    @property
    def _2d_common_kwargs(self) -> TwoDGraphKwargs:
        return TwoDGraphKwargs(
            log_x=self._log_x,
            log_y=self._log_y,
        )

    def line(self, x: str, y: str, title: str | None = None) -> Figure:
        return px.line(
            self._df.select(self._group, y, x).collect(),
            x=x,
            y=y,
            render_mode="webgl",
            title=title,
            **self._2d_common_kwargs,
            **self._common_kwargs,
        )

    def bar(
        self,
        y: str,
        agg_expr: Callable[[str], pl.Expr],
        title: str | None = None,
        barmode: BarMode = "relative",
    ) -> Figure:
        return px.bar(
            self._df.group_by(self._group).agg(agg_expr(y)).sort(y).collect(),
            y=y,
            x=self._group,
            title=title,
            barmode=barmode,
            **self._2d_common_kwargs,
            **self._common_kwargs,
        )

    def histogram(
        self,
        x: str,
        title: str | None = None,
        barmode: BarMode = "overlay",
        nbins: int | None = None,
    ) -> Figure:
        return px.histogram(
            self._df.select(self._group, x).collect(),
            x=x,
            title=title,
            barmode=barmode,
            nbins=nbins,
            opacity=0.75,
            **self._2d_common_kwargs,
            **self._common_kwargs,
        )

    def box(
        self, y: str, title: str | None = None, boxmode: DisplayMode = "group"
    ) -> Figure:
        return px.box(
            self._df.select(self._group, y).collect(),
            y=y,
            title=title,
            boxmode=boxmode,
            **self._2d_common_kwargs,
            **self._common_kwargs,
        )

    def violin(
        self,
        y: str,
        title: str | None = None,
        violinmode: DisplayMode = "group",
        points: Points = "outliers",
    ) -> Figure:
        return px.violin(
            self._df.select(self._group, y).collect(),
            y=y,
            title=title,
            violinmode=violinmode,
            points=points,
            **self._common_kwargs,
        )

    def set_group(self, group: str) -> Self:
        """
        Set the grouping column for the graphs and return self.
        """
        self._group = group
        return self

    def set_log_x(self, log_x: bool) -> Self:
        """
        Set whether the x-axis should be logarithmic and return self.
        """
        self._log_x = log_x
        return self

    def set_log_y(self, log_y: bool) -> Self:
        """
        Set whether the y-axis should be logarithmic and return self.
        """
        self._log_y = log_y
        return self

    def set_width(self, width: int) -> Self:
        """
        Set the width of the figure and return self.
        """
        self._width = width
        return self

    def set_height(self, height: int) -> Self:
        """
        Set the height of the figure and return self.
        """
        self._height = height
        return self
