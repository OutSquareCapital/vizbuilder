import math
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Self

import polars as pl
import pychain as pc


@dataclass(slots=True)
class RGBColor:
    r: int
    g: int
    b: int

    @classmethod
    def from_hex(cls, hex_color: str) -> Self:
        hex_color = hex_color.lstrip("#")
        result = (
            pc.Iter.from_elements(0, 2, 4)
            .map(lambda i: int(hex_color[i : i + 2], 16))
            .pipe_into(tuple)
        )
        return cls(*result)

    def to_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def join(self, other: Self, factor: float) -> Self:
        return self.__class__(
            r=self._join(self.r, other.r, factor),
            g=self._join(self.g, other.g, factor),
            b=self._join(self.b, other.b, factor),
        )

    @staticmethod
    def _join(left: int, right: int, factor: float) -> int:
        return math.floor(left + (right - left) * factor)


def palette_from_df(
    df: pl.DataFrame | pl.LazyFrame, group: str, base_palette: Iterable[str]
) -> dict[str, str]:
    data: pl.Series = (
        df.lazy().select(pl.col(group).unique().sort()).collect().get_column(group)
    )
    return generate_palette(*data, base_palette=base_palette)


def generate_palette(*data: str, base_palette: Iterable[str]) -> dict[str, str]:
    keys = pc.Iter(data)
    n_colors: int = keys.length()
    palette: pc.Iter[str] = pc.Iter(base_palette)
    segments: int = palette.length() - 1

    if segments < 1:
        result = palette.head(1).repeat(n_colors).flatten().pipe_into(list)
        return keys.zip(result).pipe_into(dict)

    total_interval: int = (n_colors - 1) if n_colors > 1 else 1

    def _calculate_color(i: int) -> str:
        pos: float = (i / total_interval) * segments if total_interval > 0 else 0.0
        index: int = math.floor(pos)
        factor: float = pos - index
        rgb_left: RGBColor = RGBColor.from_hex(palette.item(index))
        rgb_right: RGBColor = RGBColor.from_hex(palette.item(min(index + 1, segments)))
        return rgb_left.join(rgb_right, factor).to_hex()

    result: list[str] = (
        pc.Iter.from_range(0, n_colors).map(_calculate_color).pipe_into(list)
    )
    return keys.zip(result).pipe_into(dict)
