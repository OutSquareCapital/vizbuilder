from enum import StrEnum
from pathlib import Path

from vizbuilder._scales import get_palettes


class Text(StrEnum):
    CONTENT = "Palettes = Literal[\n"
    END_CONTENT = "]"
    START_MARKER = "# START MARKER"
    END_MARKER = "# END MARKER"
    ERROR = "Error: Markers not found in _scales.py"
    SUCCESS = "✅ Successfully generated and updated Palettes Literal in _scales.py"


def get_path():
    return Path().joinpath("src", "vizbuilder", "_scales.py")


def generate_palettes_literal() -> None:
    literal_content: str = Text.CONTENT
    for name in get_palettes().iter_keys().sort().unwrap():
        literal_content += f'    "{name}",\n'
    literal_content += Text.END_CONTENT
    scales_file: Path = get_path()
    content: str = scales_file.read_text()
    start_index: int = content.find(Text.START_MARKER)
    end_index: int = content.find(Text.END_MARKER)

    if start_index == -1 or end_index == -1:
        raise RuntimeError(Text.ERROR)

    new_content: str = (
        content[: start_index + len(Text.START_MARKER)]
        + "\n"
        + literal_content
        + "\n"
        + content[end_index:]
    )

    scales_file.write_text(new_content)
    print(Text.SUCCESS)


if __name__ == "__main__":
    generate_palettes_literal()
