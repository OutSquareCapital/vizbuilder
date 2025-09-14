from collections.abc import Callable
from dataclasses import dataclass
from typing import Concatenate, Self

import plotly.express as px
import plotly.graph_objects as go
import polars as pl

from ._colors import palette_from_df
from ._types import (
    FigureFunc,
    GraphArgs,
    Templates,
)


@dataclass(slots=True)
class Displayer:
    df: pl.LazyFrame
    kwargs: GraphArgs

    def pipe[**P, R](
        self, func: Callable[Concatenate[Self, P], R], *args: P.args, **kwargs: P.kwargs
    ) -> R:
        """
        Pass the Displayer instance and additional arguments to a function and return the result.
        """
        return func(self, *args, **kwargs)

    @classmethod
    def from_df(
        cls,
        df: pl.LazyFrame | pl.DataFrame,
        group: str,
        x: str | None = None,
        y: str | None = None,
        base_palette: list[str] = px.colors.sequential.Turbo,
        template: Templates = "plotly_dark",
    ) -> Self:
        """
        Construct a Displayer from a Polars LazyFrame by collecting and building a color map.
        """
        return cls(
            df=df.lazy(),
            kwargs=GraphArgs(
                x=x,
                y=y,
                color=group,
                color_discrete_map=df.pipe(palette_from_df, group, base_palette),
                template=template,
            ),
        )

    def plot[**P](
        self,
        func: FigureFunc[P],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> go.Figure:
        """
        Build and return a Plotly figure using the provided function and stored data.
        """
        x_expr = self.kwargs["x"] or None
        y_expr = self.kwargs["y"] or None
        return func(
            self.df.select(
                x_expr,
                y_expr,
                pl.col(self.kwargs["color"]),
            ).collect(),
            *args,
            **{**self.kwargs, **kwargs},
        )  # type: ignore[arg-type]

    def update_color(self, key: str, value: str) -> Self:
        """
        Update a color in the discrete color map if the key exists and return self.
        """
        if key in self.kwargs["color_discrete_map"]:
            self.kwargs["color_discrete_map"][key] = value
        return self

    def set_x(self, x: str | None) -> Self:
        """
        Set the x attribute and return self.
        """
        self.kwargs["x"] = x
        return self

    def set_y(self, y: str | None) -> Self:
        """
        Set the y attribute and return self.
        """
        self.kwargs["y"] = y
        return self

    def set_template(self, template: Templates) -> Self:
        """
        Set the template for the graphs and return self.
        """
        self.kwargs["template"] = template
        return self
