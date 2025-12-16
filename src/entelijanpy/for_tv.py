import os
from pathlib import Path
import subprocess as sp
import tempfile
import uuid
import shutil
from datetime import datetime
from enum import Enum


class Resolution(Enum):
    HD = "HD"
    FullHD = "Full-HD"
    FullHD_P = "Full-HD-P"
    UHD4k = "4k-UHD"
    UHD8k = "8k-UHD"

    def width(self) -> int:
        match self:
            case Resolution.HD:
                return 1280
            case Resolution.FullHD:
                return 1920
            case Resolution.FullHD_P:
                return 1080
            case Resolution.UHD4k:
                return 3840
            case Resolution.UHD8k:
                return 7680

    def height(self) -> int:
        match self:
            case Resolution.HD:
                return 720
            case Resolution.FullHD:
                return 1080
            case Resolution.FullHD_P:
                return 1920
            case Resolution.UHD4k:
                return 2160
            case Resolution.UHD8k:
                return 4320


def ts_():
    return datetime.now().strftime("%y%m%d-%H%M%S")


def is_image(file: Path) -> bool:
    valid = [
        ".jpg",
        ".jpeg",
        ".png",
    ]
    return file.is_file() and file.suffix.lower() in valid


def create_base_images(
    in_dir: Path, name: str, ts: str, resolution: Resolution, cnt_format: str
) -> Path:
    work_dir = Path(tempfile.gettempdir()) / str(uuid.uuid4())[0:6]
    work_dir.mkdir(exist_ok=True, parents=True)
    cnt = 0
    in_files_sorted = sorted(
        [f for f in in_dir.iterdir() if is_image(f)], key=lambda f: f.name
    )
    max_cnt = len(in_files_sorted)
    for file in in_files_sorted:
        out_file = work_dir / f"{name}-{ts}-{cnt:{cnt_format}}.jpg"
        cmd = [
            "convert",
            f"{file}",
            "-background",
            "black",
            "-resize",
            f"{resolution.width()}x{resolution.height()}",
            "-gravity",
            "center",
            "-extent",
            f"{resolution.width()}x{resolution.height()}",
            f"{out_file}",
        ]
        rc = sp.run(cmd)
        print(
            f"Resized {rc.returncode} {cnt + 1}/{max_cnt} {file} -> {out_file.name} {resolution.value}"
        )
        cnt += 1
    return work_dir


def main(name: str, in_dir: Path, resolution: Resolution, out_dir: Path | None):
    assert in_dir.exists()
    ts = ts_()
    work_dir = create_base_images(in_dir, name, ts, resolution, "04d")
    cnt = len(list(work_dir.iterdir()))
    if cnt <= 0:
        print("WARNING: Found no images to be processed")
        return
    print(f"Resized/renamed {cnt} files to {work_dir}")
    if out_dir is None:
        out_dir = Path.home() / "tmp" / "entelijanpy"
    o_dir = out_dir / f"{name}-{ts}"
    shutil.copytree(work_dir, o_dir)
    print(f"Copied {cnt} files to {o_dir}")


def video(
    name: str, in_dir: Path, pause: float, resolution: Resolution, out_dir: Path | None
) -> None:
    assert in_dir.exists()
    ts = ts_()
    cnt_format = "04d"
    work_dir = create_base_images(in_dir, name, ts, resolution, cnt_format)
    cnt = len(list(work_dir.iterdir()))
    if cnt <= 0:
        print("WARNING: Found no images to be processed")
        return
    print(f"Resized/renamed {cnt} files to {work_dir}")
    if out_dir is None:
        out_dir = Path.home() / "tmp" / "entelijanpy"
    out_dir.mkdir(parents=True, exist_ok=True)
    image_prefix = f"{name}-{ts}-"
    image_suffix = ".jpg"
    out_file = out_dir / f"{name}-{ts}.mp4"
    cmd = [
        "ffmpeg",
        "-framerate",
        f"1/{pause:.3f}",
        "-y",
        "-i",
        f"{work_dir}{os.sep}{image_prefix}%{cnt_format}{image_suffix}",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        f"{out_file}",
    ]
    print(f"Executing :\n{' '.join(cmd)}")
    rc = sp.run(cmd)
    print(f"Created video {out_file.name} {rc.returncode} {resolution.value}")
