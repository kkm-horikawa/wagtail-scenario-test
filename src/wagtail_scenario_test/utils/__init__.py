"""
Utility classes for Wagtail E2E testing.

Provides factory base classes and helper functions.
"""

from wagtail_scenario_test.utils.factories import (
    WagtailSuperUserFactory,
    WagtailUserFactory,
)
from wagtail_scenario_test.utils.video import (
    convert_all_videos_to_gif,
    convert_video_to_gif,
    is_ffmpeg_available,
)

__all__ = [
    "WagtailUserFactory",
    "WagtailSuperUserFactory",
    "convert_video_to_gif",
    "convert_all_videos_to_gif",
    "is_ffmpeg_available",
]
