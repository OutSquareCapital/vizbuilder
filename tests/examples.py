from pathlib import Path

import plotly.express as px
import polars as pl

import vizbuilder as vz


def source():
    return (
        Path()
        .resolve()
        .parent.joinpath("db")
        .joinpath("prices")
        .with_suffix(".parquet")
    )


if __name__ == "__main__":
    df: pl.LazyFrame = pl.scan_parquet(source()).sort("ticker", "date")
    displayer = vz.Displayer.from_df(df, group="ticker", x="date", y="equity_log_adj")

    displayer.plot(px.line).show()
    displayer.set_y("close").plot(px.line).show()
