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

    return pc.Iter(modules).map(
        lambda mod: pc.Dict(mod.__dict__)
        .filter_values(lambda v: isinstance(v, list))
        .map_keys(lambda k: f"{mod.__name__.split('.')[-1]}.{k}")
        .unwrap()
    )


def convert_scales():
    color_filter: pl.Expr = (
        pl.col("color")
        .list.eval(pl.element().first().str.starts_with("#").alias("is_hex"))
        .list.first()
    )

    return (
        extract_scales()
        .pipe_into(pl.LazyFrame)
        .unpivot(value_name="color", variable_name="scale")
        .drop_nulls()
        .filter(color_filter)
        .select(
            pl.col("scale").str.split(".").list.first().alias("module"),
            pl.col("scale").str.split(".").list.last().alias("scale"),
            pl.col("color"),
        )
        .sort("module", "scale")
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
