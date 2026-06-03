import json
import pytest
from src.digest import build_prompt, build_correction_prompt, parse_digest


# --- build_prompt ---

def test_build_prompt_includes_date():
    _, user = build_prompt(date="2026-06-03", email="test email")
    assert "2026-06-03" in user


def test_build_prompt_includes_email():
    _, user = build_prompt(date="Day 05", email="Assignment due Friday")
    assert "Assignment due Friday" in user


def test_build_prompt_missing_channels_show_placeholder():
    _, user = build_prompt(date="Day 05", email="", discord="", web="")
    assert user.count("Không có") == 3


def test_build_prompt_includes_discord():
    _, user = build_prompt(date="Day 05", discord="Submit lab by Monday")
    assert "Submit lab by Monday" in user


def test_build_prompt_date_used_as_anchor():
    _, user = build_prompt(date="Day 05", email="some content")
    # date appears at least twice: in header and in anchor instruction
    assert user.count("Day 05") >= 2


# --- parse_digest ---

def test_parse_digest_valid_json():
    valid = json.dumps({
        "key_concepts": ["AI", "LLM"],
        "action_items": [{"task": "Nộp bài", "deadline": "2026-06-05"}],
        "flags": []
    })
    result = parse_digest(valid)
    assert result["key_concepts"] == ["AI", "LLM"]
    assert result["action_items"][0]["task"] == "Nộp bài"
    assert result["flags"] == []
    assert "parse_error" not in result


def test_parse_digest_invalid_json_returns_fallback():
    result = parse_digest("This is not JSON at all")
    assert result["parse_error"] is True
    assert result["raw"] == "This is not JSON at all"
    assert result["key_concepts"] == []
    assert result["action_items"] == []
    assert result["flags"] == []


def test_parse_digest_strips_markdown_code_block():
    wrapped = '```json\n{"key_concepts": ["test"], "action_items": [], "flags": []}\n```'
    result = parse_digest(wrapped)
    assert result["key_concepts"] == ["test"]
    assert "parse_error" not in result


def test_parse_digest_missing_fields_default_to_empty_lists():
    result = parse_digest('{"key_concepts": ["x"]}')
    assert result["action_items"] == []
    assert result["flags"] == []


# --- build_correction_prompt ---

def test_build_correction_prompt_includes_previous_json():
    prev = '{"key_concepts": ["A"], "action_items": [], "flags": []}'
    _, user = build_correction_prompt(prev, "Deadline is June 10")
    assert "June 10" in user
    assert prev in user


def test_build_correction_prompt_includes_correction_text():
    prev = '{"key_concepts": [], "action_items": [], "flags": []}'
    _, user = build_correction_prompt(prev, "Lab submission on Friday 5pm")
    assert "Lab submission on Friday 5pm" in user
