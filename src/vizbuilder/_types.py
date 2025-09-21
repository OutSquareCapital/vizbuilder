from collections.abc import Callable, Sequence
from typing import Any, Literal, Protocol, TypedDict, get_args

import plotly.graph_objects as go
import polars as pl


class DataFrameCompatible(Protocol):
    # More details at https://data-apis.org/dataframe-protocol/latest/index.html
    def __dataframe__(self, nan_as_null: bool = ..., allow_copy: bool = ...) -> Any: ...


Templates = Literal[
    "ggplot2",
    "seaborn",
    "simple_white",
    "plotly",
    "plotly_white",
    "plotly_dark",
    "presentation",
    "xgridoff",
    "ygridoff",
    "gridon",
    "none",
]

TemplatesValues: tuple[str, ...] = get_args(Templates)

DisplayMode = Literal["group", "overlay"]
BarMode = Literal["relative", "group", "overlay"]
Points = Literal["all", "outliers", "suspectedoutliers"]

type ArrayLike = Sequence[Any] | pl.Series
type FrameOrDict = DataFrameCompatible | dict[str, ArrayLike] | Sequence[dict[str, Any]]
type FigureFunc[**P] = Callable[P, go.Figure]


class GraphKwargs(TypedDict):
    template: Templates
    width: int | None
    height: int | None
    color: str
    color_discrete_map: dict[str, str]


class TwoDGraphKwargs(TypedDict):
    log_x: bool
    log_y: bool
