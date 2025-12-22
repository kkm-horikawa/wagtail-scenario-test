"""
Video and GIF recording utilities for E2E tests.

This module provides utilities for converting Playwright video recordings
to GIF format for easier sharing and documentation.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


def is_ffmpeg_available() -> bool:
    """Check if ffmpeg is available on the system."""
    return shutil.which("ffmpeg") is not None


def convert_video_to_gif(
    video_path: str | Path,
    output_path: str | Path | None = None,
    fps: int = 10,
    width: int = 800,
    delete_original: bool = False,
) -> Path | None:
    """
    Convert a video file to GIF format using ffmpeg.

    Args:
        video_path: Path to the input video file (webm, mp4, etc.)
        output_path: Path for the output GIF. Defaults to same name with .gif.
        fps: Frames per second for the GIF (lower = smaller file). Default: 10
        width: Width of the GIF in pixels (height auto-scaled). Default: 800
        delete_original: Whether to delete the original video after conversion.

    Returns:
        Path to the created GIF, or None if conversion failed.

    Example:
        >>> convert_video_to_gif("test-results/video.webm")
        PosixPath('test-results/video.gif')
    """
    if not is_ffmpeg_available():
        return None

    video_path = Path(video_path)
    if not video_path.exists():
        return None

    if output_path is None:
        output_path = video_path.with_suffix(".gif")
    else:
        output_path = Path(output_path)

    # ffmpeg command to convert video to GIF with good quality
    # Uses palette generation for better colors
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output file
        "-i",
        str(video_path),
        "-vf",
        f"fps={fps},scale={width}:-1:flags=lanczos,split[s0][s1];"
        "[s0]palettegen[p];[s1][p]paletteuse",
        "-loop",
        "0",  # Loop forever
        str(output_path),
    ]

    try:
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            timeout=120,  # 2 minute timeout
        )
    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        FileNotFoundError,
    ):
        return None

    if output_path.exists():
        if delete_original:
            video_path.unlink()
        return output_path

    return None


def convert_all_videos_to_gif(
    directory: str | Path,
    fps: int = 10,
    width: int = 800,
    delete_originals: bool = False,
) -> list[Path]:
    """
    Convert all video files in a directory to GIF format.

    Args:
        directory: Directory containing video files
        fps: Frames per second for GIFs
        width: Width of GIFs in pixels
        delete_originals: Whether to delete original videos after conversion

    Returns:
        List of paths to created GIF files
    """
    directory = Path(directory)
    if not directory.exists():
        return []

    gifs = []
    for video_file in directory.rglob("*.webm"):
        gif_path = convert_video_to_gif(
            video_file,
            fps=fps,
            width=width,
            delete_original=delete_originals,
        )
        if gif_path:
            gifs.append(gif_path)

    return gifs
