from pathlib import Path

import plotly.express as px
import polars as pl

import vizbuilder as vz


def plot_graphs():
    (
        pl.scan_parquet(
            Path().resolve().parent.joinpath("db", "prices").with_suffix(".parquet")
        )
        .sort("ticker", "date")
        .pipe(vz.Displayer, group="ticker", template="plotly_dark")
        .plot(px.line, x="date", y="close")
        .show()
    )


if __name__ == "__main__":
    plot_graphs()
