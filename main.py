"""Write the NETHERWICK travel poster to /output/entry.png.

Stdlib-only, no network, no clock, no randomness. The poster image is
bundled beside this file as poster.png; this program copies it byte for
byte to /output/entry.png, so every run produces identical output.
"""

import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "poster.png"
OUTPUT = Path("/output/entry.png")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    if OUTPUT.stat().st_size != SOURCE.stat().st_size:
        raise RuntimeError("poster copy is incomplete")


if __name__ == "__main__":
    main()
