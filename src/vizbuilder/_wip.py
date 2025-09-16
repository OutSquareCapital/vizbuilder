from collections.abc import Sequence
from typing import Any, Literal

import plotly.graph_objs as go
from plotly._stubs_helpers import (
    ArrayLike,
    BarMode,
    BranchVals,
    ColumnData,
    DisplayMode,
    FrameOrDict,
    HistFunc,
    HistNorm,
    HoverData,
    LineShape,
    MapIdentity,
    Marginal,
    MultiColumnData,
    Orientation,
    Points,
    RenderMode,
    Templates,
    TrendlineFunc,
    TrendLineScope,
    ValNorm,
)


class Base:
    data_frame: FrameOrDict | None = None
    color: ColumnData | None = None
    color_discrete_sequence: list[str] | None = None
    color_discrete_map: MapIdentity | None = None
    title: str | None = None
    subtitle: str | None = None
    template: Templates | None = None
    width: int | None = None
    height: int | None = None
    hover_name: ColumnData | None = None
    hover_data: HoverData | None = None
    labels: dict[str, str] | None = None


class WithColorMidpoint:
    color_continuous_midpoint: int | float | None = None


class WithContinousScale:
    color_continuous_scale: list[str] | None = None
    range_color: Sequence[int | float] | None = None


class WithCustomData:
    custom_data: MultiColumnData | None = None


class Animated:
    animation_frame: ColumnData | None = None
    animation_group: ColumnData | None = None
    category_orders: dict[str, list[str]] | None = None


class XY:
    x: MultiColumnData | None = None
    y: MultiColumnData | None = None
    log_x: bool = False
    log_y: bool = False
    range_x: Sequence[int | float] | None = None
    range_y: Sequence[int | float] | None = None


class Hierarchy(Base, WithColorMidpoint, WithContinousScale, WithCustomData):
    names: ColumnData | None = None
    values: ColumnData | None = None
    parents: ColumnData | None = None
    path: ArrayLike | None = None
    ids: ColumnData | None = None
    maxdepth: int | None = None
    branchvalues: BranchVals | None = None


def treemap() -> go.Figure: ...


def icicle() -> go.Figure: ...


def sunburst() -> go.Figure: ...


class WithFacet(XY):
    facet_row: ColumnData | None = None
    facet_col: ColumnData | None = None
    facet_col_wrap: int = 0
    facet_row_spacing: float | None = None
    facet_col_spacing: float | None = None


class Histogram(Base, XY):
    pass


def histogram(
    pattern_shape: ColumnData | None = None,
    pattern_shape_sequence: list[str] | None = None,
    pattern_shape_map: MapIdentity | None = None,
    marginal: Marginal | None = None,
    opacity: float | None = None,
    orientation: Orientation | None = None,
    barmode: BarMode = "relative",
    barnorm: ValNorm | None = None,
    histnorm: HistNorm | None = None,
    histfunc: HistFunc | None = None,
    cumulative: bool = False,
    nbins: int | None = None,
    text_auto: bool | str = False,
) -> go.Figure: ...


class WithPoints(Base, XY, WithCustomData):
    points: Points | bool = "outliers"


def violin(
    orientation: Orientation | None = None,
    violinmode: Literal["group", "overlay"] = "group",
    box: bool = False,
) -> go.Figure: ...
def box(
    orientation: Orientation | None = None,
    boxmode: DisplayMode = "group",
    notched: bool = False,
) -> go.Figure: ...


class XYError(XY):
    error_x: ColumnData | None = None
    error_x_minus: ColumnData | None = None
    error_y: ColumnData | None = None
    error_y_minus: ColumnData | None = None


class XYErrorWithFacet(XYError, WithFacet):
    pass


class Bar(Base, XYErrorWithFacet, WithContinousScale, WithCustomData):
    pass


def bar(
    pattern_shape: ColumnData | None = None,
    text: ColumnData | None = None,
    base: ColumnData | None = None,
    color_continuous_scale: list[str] | None = None,
    pattern_shape_sequence: list[str] | None = None,
    pattern_shape_map: MapIdentity | None = None,
    opacity: float | None = None,
    orientation: Orientation | None = None,
    barmode: BarMode = "relative",
    text_auto: bool | str = False,
) -> go.Figure: ...


class WithSymbolMap:
    symbol_map: MapIdentity | None = None


class WithRenderMode(XYErrorWithFacet, WithSymbolMap, WithCustomData):
    render_mode: RenderMode = "auto"


def line(
    line_group: ColumnData | None = None,
    line_dash: ColumnData | None = None,
    symbol: ColumnData | None = None,
    text: ColumnData | None = None,
    orientation: Orientation | None = None,
    line_dash_sequence: list[str] | None = None,
    line_dash_map: MapIdentity | None = None,
    symbol_sequence: list[str] | None = None,
    markers: bool = False,
    line_shape: LineShape | None = None,
) -> go.Figure: ...


class Scatter(WithColorMidpoint, WithContinousScale):
    pass


class Scatter2D(Base, WithRenderMode, Scatter):
    pass


def scatter(
    symbol: ColumnData | None = None,
    size: ColumnData | None = None,
    text: ColumnData | None = None,
    orientation: Orientation | None = None,
    symbol_sequence: list[str] | None = None,
    opacity: float | None = None,
    size_max: int = 20,
    marginal_x: Marginal | None = None,
    marginal_y: Marginal | None = None,
    trendline: TrendlineFunc | None = None,
    trendline_options: dict[str, Any] | None = None,
    trendline_color_override: str | None = None,
    trendline_scope: TrendLineScope = "trace",
) -> go.Figure: ...


class Z(XYError, WithSymbolMap, WithCustomData):
    z: MultiColumnData | None = None
    log_z: bool = False
    range_z: Sequence[int | float] | None = None
    error_z: ColumnData | None = (None,)
    error_z_minus: ColumnData | None = (None,)


def line_3d(
    line_dash: ColumnData | None = None,
    text: ColumnData | None = None,
    line_group: ColumnData | None = None,
    symbol: ColumnData | None = None,
    line_dash_sequence: list[str] | None = None,
    line_dash_map: MapIdentity | None = None,
    symbol_sequence: list[str] | None = None,
    markers: bool = False,
) -> go.Figure: ...


class Scatter3D(Z, Scatter):
    pass


def scatter_3d(
    symbol: ColumnData | None = None,
    size: ColumnData | None = None,
    text: ColumnData | None = None,
    size_max: int = 20,
    symbol_sequence: list[str] | None = None,
    opacity: float | None = None,
) -> go.Figure: ...
