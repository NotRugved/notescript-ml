"""Extractor module shim forwarding all functionality to yt_extractor."""

from yt_extractor import (
    find_day_candidates,
    format_time,
    get_notebook_text,
    get_video_id,
    get_video_info,
    list_day_folders,
    list_notebooks,
    list_playlist,
    parse_time,
    plan_segments,
    suggest_folders,
)

__all__ = [
    "find_day_candidates",
    "format_time",
    "get_notebook_text",
    "get_video_id",
    "get_video_info",
    "list_day_folders",
    "list_notebooks",
    "list_playlist",
    "parse_time",
    "plan_segments",
    "suggest_folders",
]
