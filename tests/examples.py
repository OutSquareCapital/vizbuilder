from pathlib import Path

import polars as pl

import vizbuilder as vz

SOURCE = Path().resolve().parent.joinpath("db", "prices").with_suffix(".parquet")


def plot_graphs():
    plotter = (
        pl.scan_parquet(SOURCE)
        .sort("ticker", "date")
        .drop_nulls()
        .pipe(vz.Displayer, "ticker", "Plotly3", "plotly_dark")
    )
    plotter.line(
        x="date", y="close", title="Closing Prices of Different Tickers Over Time"
    ).show()
    plotter.bar(
        y="stdev",
        agg_expr=pl.median,
        title="Median of Standard Deviation of Closing Prices by Ticker",
    ).show()
    plotter.histogram(x="stdev", title="Stdev Distribution").show()
    plotter.box(y="stdev", title="Stdev Boxplot by Ticker", boxmode="group").show()
    plotter.violin(y="stdev", title="Stdev Violin by Ticker", violinmode="group").show()


if __name__ == "__main__":
    plot_graphs()
