"""Compare captured source content; annotation changes are not vendor changes."""
from .evidence import content_hash
from datetime import datetime


def _time(value):
    instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if instant.tzinfo is None:
        raise ValueError("Capture timestamps must include their timezone.")
    return instant


def snapshot(source_url, content, captured_at):
    if not source_url.startswith("https://") or not content.strip() or not captured_at:
        raise ValueError("A snapshot needs a source, nonempty captured content and capture time.")
    _time(captured_at)
    return {"source": source_url, "sha256": content_hash(content), "captured_at": captured_at}


def compare(previous, current):
    if previous["source"] != current["source"]:
        raise ValueError("Compare captures of the same source URL.")
    if _time(previous["captured_at"]) >= _time(current["captured_at"]):
        raise ValueError("The second capture must be later than the first.")
    return {"source": current["source"], "state": "content_changed" if previous["sha256"] != current["sha256"] else "unchanged", "interpretation": "Content hashes describe captured source content, not a verified product, pricing or business change."}
