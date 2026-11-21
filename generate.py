"""Build-time script that produced poster.png from the source illustration.

Build-time only (requires Pillow); it is NOT run by the entry program.
main.py is stdlib-only and copies the bundled poster.png.

Steps, as run for this entry:
1. The source illustration (1280x1920, kept local-only in assets/) was
   generated once as a vintage travel poster for the imaginary place
   NETHERWICK, with the single tagline WHERE THE WATERFALLS FALL UP.
2. It was resized to fit within 1024x1024 (682x1024, Lanczos).
3. It was palette-quantized to 256 colours (median cut) and saved as an
   optimised PNG, bringing it under the 1,048,576-byte limit while
   keeping the title and tagline crisp and readable.

Usage: python3 generate.py [source.png] [poster.png]
"""

import hashlib
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover - build-time dependency
    raise SystemExit("generate.py needs Pillow (pip install Pillow)")


def build(source: Path, output: Path) -> None:
    image = Image.open(source).convert("RGB")
    width, height = image.size
    scale = min(1024 / width, 1024 / height)
    resized = image.resize((int(width * scale), int(height * scale)), Image.LANCZOS)
    quantized = resized.quantize(colors=256, method=Image.MEDIANCUT)
    quantized.save(output, "PNG", optimize=True)
    data = output.read_bytes()
    print(f"{output}: {quantized.size[0]}x{quantized.size[1]}, "
          f"{len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "assets" / "source-poster-1280x1920.png"
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else here / "poster.png"
    build(src, dst)
