"""Verification test suite for extractor module using real data."""

import os
from dotenv import load_dotenv

import extractor
from database import init_db

load_dotenv()


def test_video_id_parsing() -> None:
    """Test get_video_id with various YouTube URL formats."""
    print("Testing get_video_id...")
    test_cases = [
        ("https://www.youtube.com/watch?v=UZPfbG0jNec", "UZPfbG0jNec"),
        ("https://www.youtube.com/watch?v=UZPfbG0jNec&list=PLKnIA16_Rmva-wY_HBh1gTH32ocu2SoTr", "UZPfbG0jNec"),
        ("https://www.youtube.com/watch?feature=shared&v=UZPfbG0jNec&t=30", "UZPfbG0jNec"),
        ("https://youtu.be/UZPfbG0jNec", "UZPfbG0jNec"),
        ("https://youtu.be/UZPfbG0jNec?t=10", "UZPfbG0jNec"),
        ("https://www.youtube.com/shorts/UZPfbG0jNec", "UZPfbG0jNec"),
        ("https://www.youtube.com/shorts/UZPfbG0jNec?feature=share", "UZPfbG0jNec"),
        ("https://www.youtube.com/embed/UZPfbG0jNec", "UZPfbG0jNec"),
        ("https://www.youtube.com/embed/UZPfbG0jNec?start=15", "UZPfbG0jNec"),
        ("UZPfbG0jNec", "UZPfbG0jNec"),
        ("https://www.google.com", ""),
        ("", ""),
    ]

    for url, expected in test_cases:
        actual = extractor.get_video_id(url)
        assert actual == expected, f"Failed for {url}: expected {expected}, got {actual}"
    print("  -> get_video_id passed!")


def test_time_formatting_and_parsing() -> None:
    """Test format_time and parse_time conversions."""
    print("Testing format_time and parse_time...")
    assert extractor.format_time(0) == "00:00"
    assert extractor.format_time(65) == "01:05"
    assert extractor.format_time(599) == "09:59"
    assert extractor.format_time(3600) == "1:00:00"
    assert extractor.format_time(3665) == "1:01:05"

    assert extractor.parse_time("00:00") == 0
    assert extractor.parse_time("01:05") == 65
    assert extractor.parse_time("09:59") == 599
    assert extractor.parse_time("1:00:00") == 3600
    assert extractor.parse_time("1:01:05") == 3665

    # Invalid cases
    assert extractor.parse_time("invalid") is None
    assert extractor.parse_time("12:65") is None
    assert extractor.parse_time("1:65:00") is None
    assert extractor.parse_time("") is None
    print("  -> format_time and parse_time passed!")


def test_segment_planning() -> None:
    """Test plan_segments chunking and tiny tail merging."""
    print("Testing plan_segments...")
    # Tail under 60s merges into preceding segment (650s = 600s + 50s -> 1 segment of 650s)
    plan_650 = extractor.plan_segments(650, 10)
    assert len(plan_650) == 1
    assert plan_650[0]["index"] == 0
    assert plan_650[0]["start_seconds"] == 0
    assert plan_650[0]["end_seconds"] == 650

    # Tail >= 60s forms its own segment (1270s = 600s + 600s + 70s -> 3 segments)
    plan_1270 = extractor.plan_segments(1270, 10)
    assert len(plan_1270) == 3
    assert plan_1270[0]["end_seconds"] == 600
    assert plan_1270[1]["end_seconds"] == 1200
    assert plan_1270[2]["start_seconds"] == 1200
    assert plan_1270[2]["end_seconds"] == 1270

    # Video under 60s with no prior segment
    plan_45 = extractor.plan_segments(45, 10)
    assert len(plan_45) == 1
    assert plan_45[0]["end_seconds"] == 45

    # Zero duration
    assert len(extractor.plan_segments(0, 10)) == 0
    print("  -> plan_segments passed!")


def test_video_info_real() -> None:
    """Test get_video_info with a real public video."""
    print("Testing get_video_info with real YouTube video...")
    test_url = "https://www.youtube.com/watch?v=UZPfbG0jNec"
    info = extractor.get_video_info(test_url)

    assert info["video_id"] == "UZPfbG0jNec"
    assert "Linear Regression" in info["title"]
    assert info["duration_seconds"] > 1000

    # Test tuple unpacking capability
    title, duration, vid = info
    assert title == info["title"]
    assert duration == info["duration_seconds"]
    assert vid == info["video_id"]

    # Test error handling on invalid URL
    try:
        extractor.get_video_info("https://www.youtube.com/watch?v=invalid_id_999999999")
        assert False, "Expected error on invalid video"
    except RuntimeError:
        pass
    print("  -> get_video_info passed!")


def test_playlist_and_day_candidates() -> None:
    """Test list_playlist caching and find_day_candidates."""
    print("Testing list_playlist and find_day_candidates...")
    playlist_url = os.getenv("PLAYLIST_URL")
    if not playlist_url:
        playlist_url = "https://youtube.com/playlist?list=PLKnIA16_Rmva-wY_HBh1gTH32ocu2SoTr"

    items = extractor.list_playlist(playlist_url)
    assert len(items) > 0
    assert items[0]["position"] == 1
    assert len(items[0]["video_id"]) == 11
    assert len(items[0]["title"]) > 0

    # Test cache hit (should return same items quickly)
    cached_items = extractor.list_playlist(playlist_url)
    assert len(cached_items) == len(items)

    # Test candidate matching logic
    mock_items = [
        {"position": 1, "video_id": "v1", "title": "Day 51: Advanced Gradient Descent"},
        {"position": 2, "video_id": "v2", "title": "Day 5 - Simple Linear Regression"},
        {"position": 3, "video_id": "v3", "title": "Understanding Support Vector Machines"},
    ]

    # Day 5 should match item 2, NOT item 1
    matches_5 = extractor.find_day_candidates(mock_items, 5)
    assert len(matches_5) == 1
    assert matches_5[0]["position"] == 2
    assert matches_5[0]["position_guess"] is False

    # Day 51 should match item 1
    matches_51 = extractor.find_day_candidates(mock_items, 51)
    assert len(matches_51) == 1
    assert matches_51[0]["position"] == 1
    assert matches_51[0]["position_guess"] is False

    # Day 3 has no title match, falls back to position 3 with position_guess=True
    matches_3 = extractor.find_day_candidates(mock_items, 3)
    assert len(matches_3) == 1
    assert matches_3[0]["position"] == 3
    assert matches_3[0]["position_guess"] is True
    print("  -> playlist and day candidate matching passed!")


def test_github_integration() -> None:
    """Test GitHub repository folder listing, notebook discovery, and text extraction."""
    print("Testing GitHub repository integration...")
    folders = extractor.list_day_folders()
    assert len(folders) > 0
    assert "day15 - working with csv files" in folders
    assert "kmeans" in folders

    # Test suggest_folders
    suggested_15 = extractor.suggest_folders(15, folders)
    assert "day15 - working with csv files" in suggested_15

    # Day 1 should not match day15
    suggested_1 = extractor.suggest_folders(1, folders)
    assert "day15 - working with csv files" not in suggested_1

    # Test list_notebooks
    target_folder = "day15 - working with csv files"
    notebooks = extractor.list_notebooks(target_folder)
    assert len(notebooks) > 0
    assert "working-with-csv.ipynb" in notebooks

    # Test get_notebook_text
    nb_text = extractor.get_notebook_text(target_folder, "working-with-csv.ipynb", max_chars=2000)
    assert len(nb_text) > 0
    assert "## Markdown" in nb_text or "## Code" in nb_text
    assert "[Note: Official notebook content truncated at max_chars limit]" in nb_text

    # Test cache hit for notebook text
    cached_text = extractor.get_notebook_text(target_folder, "working-with-csv.ipynb", max_chars=2000)
    assert cached_text == nb_text
    print("  -> GitHub integration passed!")


def main() -> None:
    """Run all tests sequentially."""
    init_db()
    test_video_id_parsing()
    test_time_formatting_and_parsing()
    test_segment_planning()
    test_video_info_real()
    test_playlist_and_day_candidates()
    test_github_integration()
    print("\nALL EXTRACTOR TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
