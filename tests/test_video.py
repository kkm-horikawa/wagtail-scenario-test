"""Tests for video conversion utilities."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from wagtail_scenario_test.utils.video import (
    convert_all_videos_to_gif,
    convert_video_to_gif,
    is_ffmpeg_available,
)


class TestIsFfmpegAvailable:
    """Tests for is_ffmpeg_available function."""

    def test_returns_true_when_ffmpeg_exists(self):
        """Test returns True when ffmpeg is found."""
        with patch("shutil.which", return_value="/usr/bin/ffmpeg"):
            assert is_ffmpeg_available() is True

    def test_returns_false_when_ffmpeg_not_found(self):
        """Test returns False when ffmpeg is not found."""
        with patch("shutil.which", return_value=None):
            assert is_ffmpeg_available() is False


class TestConvertVideoToGif:
    """Tests for convert_video_to_gif function."""

    def test_returns_none_when_ffmpeg_not_available(self, tmp_path):
        """Test returns None when ffmpeg is not available."""
        video_file = tmp_path / "video.webm"
        video_file.touch()

        with patch(
            "wagtail_scenario_test.utils.video.is_ffmpeg_available",
            return_value=False,
        ):
            result = convert_video_to_gif(video_file)
            assert result is None

    def test_returns_none_when_video_not_exists(self, tmp_path):
        """Test returns None when video file doesn't exist."""
        with patch(
            "wagtail_scenario_test.utils.video.is_ffmpeg_available",
            return_value=True,
        ):
            result = convert_video_to_gif(tmp_path / "nonexistent.webm")
            assert result is None

    def test_uses_default_output_path(self, tmp_path):
        """Test uses .gif extension when output_path is None."""
        video_file = tmp_path / "video.webm"
        video_file.touch()
        expected_gif = tmp_path / "video.gif"

        with (
            patch(
                "wagtail_scenario_test.utils.video.is_ffmpeg_available",
                return_value=True,
            ),
            patch("subprocess.run") as mock_run,
        ):
            # Create the output file to simulate successful conversion
            expected_gif.touch()

            result = convert_video_to_gif(video_file)

            assert result == expected_gif
            mock_run.assert_called_once()
            # Check that output path ends with .gif
            call_args = mock_run.call_args[0][0]
            assert call_args[-1].endswith(".gif")

    def test_uses_custom_output_path(self, tmp_path):
        """Test uses custom output path when specified."""
        video_file = tmp_path / "video.webm"
        video_file.touch()
        custom_output = tmp_path / "custom.gif"

        with (
            patch(
                "wagtail_scenario_test.utils.video.is_ffmpeg_available",
                return_value=True,
            ),
            patch("subprocess.run") as mock_run,
        ):
            custom_output.touch()
            result = convert_video_to_gif(video_file, output_path=custom_output)

            assert result == custom_output

    def test_passes_fps_and_width_to_ffmpeg(self, tmp_path):
        """Test passes fps and width parameters to ffmpeg command."""
        video_file = tmp_path / "video.webm"
        video_file.touch()
        expected_gif = tmp_path / "video.gif"

        with (
            patch(
                "wagtail_scenario_test.utils.video.is_ffmpeg_available",
                return_value=True,
            ),
            patch("subprocess.run") as mock_run,
        ):
            expected_gif.touch()
            convert_video_to_gif(video_file, fps=15, width=1024)

            call_args = mock_run.call_args[0][0]
            # Find the -vf argument
            vf_index = call_args.index("-vf")
            vf_value = call_args[vf_index + 1]
            assert "fps=15" in vf_value
            assert "scale=1024" in vf_value

    def test_deletes_original_when_requested(self, tmp_path):
        """Test deletes original video when delete_original is True."""
        video_file = tmp_path / "video.webm"
        video_file.touch()
        expected_gif = tmp_path / "video.gif"

        with (
            patch(
                "wagtail_scenario_test.utils.video.is_ffmpeg_available",
                return_value=True,
            ),
            patch("subprocess.run"),
        ):
            expected_gif.touch()
            convert_video_to_gif(video_file, delete_original=True)

            assert not video_file.exists()

    def test_keeps_original_by_default(self, tmp_path):
        """Test keeps original video by default."""
        video_file = tmp_path / "video.webm"
        video_file.touch()
        expected_gif = tmp_path / "video.gif"

        with (
            patch(
                "wagtail_scenario_test.utils.video.is_ffmpeg_available",
                return_value=True,
            ),
            patch("subprocess.run"),
        ):
            expected_gif.touch()
            convert_video_to_gif(video_file)

            assert video_file.exists()

    def test_returns_none_on_subprocess_error(self, tmp_path):
        """Test returns None when subprocess fails."""
        video_file = tmp_path / "video.webm"
        video_file.touch()

        with (
            patch(
                "wagtail_scenario_test.utils.video.is_ffmpeg_available",
                return_value=True,
            ),
            patch(
                "subprocess.run",
                side_effect=subprocess.CalledProcessError(1, "ffmpeg"),
            ),
        ):
            result = convert_video_to_gif(video_file)
            assert result is None

    def test_returns_none_on_timeout(self, tmp_path):
        """Test returns None when subprocess times out."""
        video_file = tmp_path / "video.webm"
        video_file.touch()

        with (
            patch(
                "wagtail_scenario_test.utils.video.is_ffmpeg_available",
                return_value=True,
            ),
            patch("subprocess.run", side_effect=subprocess.TimeoutExpired("ffmpeg", 120)),
        ):
            result = convert_video_to_gif(video_file)
            assert result is None

    def test_returns_none_on_file_not_found(self, tmp_path):
        """Test returns None when ffmpeg binary not found during execution."""
        video_file = tmp_path / "video.webm"
        video_file.touch()

        with (
            patch(
                "wagtail_scenario_test.utils.video.is_ffmpeg_available",
                return_value=True,
            ),
            patch("subprocess.run", side_effect=FileNotFoundError()),
        ):
            result = convert_video_to_gif(video_file)
            assert result is None

    def test_returns_none_when_output_not_created(self, tmp_path):
        """Test returns None when output file is not created."""
        video_file = tmp_path / "video.webm"
        video_file.touch()

        with (
            patch(
                "wagtail_scenario_test.utils.video.is_ffmpeg_available",
                return_value=True,
            ),
            patch("subprocess.run"),  # Don't create output file
        ):
            result = convert_video_to_gif(video_file)
            assert result is None


class TestConvertAllVideosToGif:
    """Tests for convert_all_videos_to_gif function."""

    def test_returns_empty_list_when_directory_not_exists(self, tmp_path):
        """Test returns empty list when directory doesn't exist."""
        result = convert_all_videos_to_gif(tmp_path / "nonexistent")
        assert result == []

    def test_converts_all_webm_files(self, tmp_path):
        """Test converts all webm files in directory."""
        # Create test video files
        (tmp_path / "video1.webm").touch()
        (tmp_path / "video2.webm").touch()
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "video3.webm").touch()

        with patch(
            "wagtail_scenario_test.utils.video.convert_video_to_gif"
        ) as mock_convert:
            # Make convert return a path for each call
            mock_convert.side_effect = [
                tmp_path / "video1.gif",
                tmp_path / "video2.gif",
                tmp_path / "subdir" / "video3.gif",
            ]

            result = convert_all_videos_to_gif(tmp_path)

            assert len(result) == 3
            assert mock_convert.call_count == 3

    def test_passes_options_to_convert(self, tmp_path):
        """Test passes fps, width, and delete options."""
        (tmp_path / "video.webm").touch()

        with patch(
            "wagtail_scenario_test.utils.video.convert_video_to_gif"
        ) as mock_convert:
            mock_convert.return_value = tmp_path / "video.gif"

            convert_all_videos_to_gif(
                tmp_path, fps=15, width=1024, delete_originals=True
            )

            mock_convert.assert_called_once()
            call_kwargs = mock_convert.call_args[1]
            assert call_kwargs["fps"] == 15
            assert call_kwargs["width"] == 1024
            assert call_kwargs["delete_original"] is True

    def test_skips_failed_conversions(self, tmp_path):
        """Test skips files that fail to convert."""
        (tmp_path / "video1.webm").touch()
        (tmp_path / "video2.webm").touch()

        with patch(
            "wagtail_scenario_test.utils.video.convert_video_to_gif"
        ) as mock_convert:
            # First succeeds, second fails
            mock_convert.side_effect = [tmp_path / "video1.gif", None]

            result = convert_all_videos_to_gif(tmp_path)

            assert len(result) == 1
            assert result[0] == tmp_path / "video1.gif"

    def test_handles_string_path(self, tmp_path):
        """Test handles string path input."""
        (tmp_path / "video.webm").touch()

        with patch(
            "wagtail_scenario_test.utils.video.convert_video_to_gif"
        ) as mock_convert:
            mock_convert.return_value = tmp_path / "video.gif"

            result = convert_all_videos_to_gif(str(tmp_path))

            assert len(result) == 1
