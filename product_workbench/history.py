"""Compare captured source content; annotation changes are not vendor changes."""
from .evidence import content_hash


def snapshot(source_url, content, captured_at):
    if not source_url.startswith("https://") or not content.strip() or not captured_at:
        raise ValueError("A snapshot needs a source, nonempty captured content and capture time.")
    return {"source": source_url, "sha256": content_hash(content), "captured_at": captured_at}


def compare(previous, current):
    if previous["source"] != current["source"]:
        raise ValueError("Compare captures of the same source URL.")
    if previous["captured_at"] >= current["captured_at"]:
        raise ValueError("The second capture must be later than the first.")
    return {"source": current["source"], "state": "content_changed" if previous["sha256"] != current["sha256"] else "unchanged", "interpretation": "Content hashes describe captured source content, not a verified product, pricing or business change."}
