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
        .pipe(vz.Displayer, group="ticker")
        .set_color_map(base_palette=px.colors.qualitative.Plotly)
        .set_template("plotly_dark")
        .set_x("date")
    )

    displayer.set_y("equity_log_adj").plot(px.line).show()
    displayer.set_y("close").plot(px.line).show()


if __name__ == "__main__":
    print(vz.extract_scales())
