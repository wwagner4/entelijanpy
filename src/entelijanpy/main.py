import typer
import entelijanpy.for_tv as _ft
from pathlib import Path

app = typer.Typer()


@app.command(help="Create a slideshow")
def slides(
    in_dir: Path,
    name: str,
    resolution: _ft.Resolution = _ft.Resolution.UHD4k,
    out_dir: Path | None = None,
) -> None:
    _ft.main(name, in_dir, resolution, out_dir)


@app.command(help="Create a video slideshow")
def video(
    in_dir: Path,
    name: str,
    pause: float = 3.0,
    resolution: _ft.Resolution = _ft.Resolution.FullHD,
    out_dir: Path | None = None,
) -> None:
    _ft.video(name, in_dir, pause, resolution, out_dir)


if __name__ == "__main__":
    app()
