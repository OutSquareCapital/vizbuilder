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


def plot_graphs():
    displayer = (
        pl.scan_parquet(source())
        .sort("ticker", "date")
        .pipe(vz.Displayer, group="ticker", template="plotly_dark")
    )
    displayer.plot(px.line, x="date", y="close").show()


if __name__ == "__main__":
    plot_graphs()
