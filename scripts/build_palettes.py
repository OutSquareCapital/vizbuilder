from pathlib import Path

import pychain as pc

from vizbuilder._scales import get_palettes


def get_path():
    return Path().joinpath("src", "vizbuilder", "_scales.py")


def generate_palettes_literal() -> None:
    palette_names = pc.Dict(get_palettes()).iter_keys().sort()
    literal_content: str = "Palettes = Literal[\n"
    for name in palette_names.unwrap():
        literal_content += f'    "{name}",\n'
    literal_content += "]"
    scales_file: Path = get_path()
    content: str = scales_file.read_text()

    start_marker: str = "# START MARKER"
    end_marker: str = "# END MARKER"

    start_index: int = content.find(start_marker)
    end_index: int = content.find(end_marker)

    if start_index == -1 or end_index == -1:
        raise RuntimeError("Markers not found in _scales.py")

    new_content: str = (
        content[: start_index + len(start_marker)]
        + "\n"
        + literal_content
        + "\n"
        + content[end_index:]
    )

    scales_file.write_text(new_content)
    print("✅ Successfully generated and updated Palettes Literal in _scales.py")


if __name__ == "__main__":
    generate_palettes_literal()
