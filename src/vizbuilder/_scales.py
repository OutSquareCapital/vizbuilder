import plotly.express as px
import plotly.graph_objects as go
import polars as pl
import pychain as pc


def extract_scales():
    modules = (
        px.colors.cyclical,
        px.colors.diverging,
        px.colors.qualitative,
        px.colors.sequential,
    )
    color_filter: pl.Expr = (
        pl.col("color")
        .list.eval(pl.element().first().str.starts_with("#").alias("is_hex"))
        .list.first()
    )
    scale_filter: pl.Expr = pl.col("scale").str.ends_with("r").not_()

    data = pc.Iter(modules).map(
        lambda mod: pc.Dict(mod.__dict__)
        .filter_values(lambda v: isinstance(v, list))
        .unwrap()
    )
    return (
        data.pipe_into(pl.LazyFrame)
        .unpivot(value_name="color", variable_name="scale")
        .drop_nulls()
        .filter(scale_filter)
        .with_columns(pl.col("scale").cast(pl.Categorical), color_filter.alias("type"))
        .sort("scale")
        .collect()
    )


def show_scales() -> go.Figure:
    """
    Return a Plotly figure showing the color swatches.
    """
    return px.colors.sequential.swatches().update_layout(
        title=None,
        height=550,
        width=400,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        paper_bgcolor="#181c1a",
    )
