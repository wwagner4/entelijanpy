import os
from pathlib import Path
import subprocess as sp
from datetime import datetime


def ts_():
    return datetime.now().strftime("%y%m%d-%H%M%S")


def testimages(name: str, in_dir: Path, out_dir: Path | None):
    configs = [
        (1000, 90),
        (2000, 90),
        (3000, 90),
        (4000, 90),
    ]

    assert in_dir.exists(), f"in_dir does not exist {in_dir}"
    print(f"-- testimages, indir {in_dir} exists, out_dir is {out_dir}")
    if not out_dir:
        out_dir = Path.home() / "tmp" / "testimages" / name
        out_dir.mkdir(exist_ok=True, parents=True)
    print(f"-- outdir {out_dir}")
    for file in in_dir.iterdir():
        print(f"-- {file}")
        for size, quality in configs:
            resize(file, size, quality, out_dir)


def resize(image: Path, size: int, quality: int, out_dir: Path):
    file_name = f"{image.stem}-{size}-{quality}.jpg"
    out_file = out_dir / file_name

    cmd = [
        "magick",
        f"{image}",
        "-background",
        "black",
        "-resize",
        f"{size}x",
        "-gravity",
        "center",
        "-extent",
        f"{size}x",
        "-quality",
        f"{quality}x",
        f"{out_file}",
    ]
    sp.run(cmd)

    file_size_bytes = os.path.getsize(out_file)
    file_size_mb = file_size_bytes / (1024 * 1024)
    pointsize = int(35.0 * size / 1000.0)

    cmd = [
        "magick",
        f"{out_file}",
        "-font",
        "/System/Library/Fonts/Avenir.ttc",
        "-pointsize",
        f"{pointsize}",
        "-fill",
        "white",
        "-undercolor",
        "#00000080",
        "-gravity",
        "South",
        "-annotate",
        "+0+20",
        f"size: {size}px fsize:{file_size_mb:.1f}Mb qual:{quality}%",
        f"{out_file}",
    ]
    sp.run(cmd)

    print(f"Created {out_file}")
