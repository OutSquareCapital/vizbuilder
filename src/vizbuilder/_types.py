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


class GraphArgs(TypedDict):
    template: Templates | None
    color: str | None
    color_discrete_map: dict[str, str] | None


type ArrayLike = Sequence[Any] | pl.Series
type FrameOrDict = DataFrameCompatible | dict[str, ArrayLike] | Sequence[dict[str, Any]]
type FigureFunc[**P] = Callable[P, go.Figure]
