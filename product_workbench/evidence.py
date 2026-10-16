"""Conservative joins and audit evidence states; no model-generated scores."""
import hashlib
import re
from urllib.parse import urlsplit

SHARED_HOSTS = {"github.com", "github.io", "readthedocs.io", "readme.io", "notion.site", "gitbook.io", "vercel.app", "netlify.app"}


def official_host(url):
    parts = urlsplit(url)
    if parts.scheme != "https" or parts.username or not parts.hostname:
        return ""
    host = parts.hostname.lower()
    for prefix in ("www.", "docs.", "developers.", "developer."):
        if host.startswith(prefix):
            host = host[len(prefix):]
            break
    if any(host == s or host.endswith("." + s) for s in SHARED_HOSTS):
        return ""
    return host


def name_key(name):
    return re.sub(r"[^a-z0-9]", "", name.casefold())


def content_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


def assess_task(steps):
    """Execution is established only by evidence of a successful actual run."""
    outcomes = []
    for step in steps:
        evidence = step.get("evidence", "").strip()
        state = step.get("state", "unknown")
        if state not in {"observed", "not_observed", "blocked", "unknown", "executed"}:
            raise ValueError("Unknown evidence state.")
        if state in {"observed", "executed"} and not evidence:
            raise ValueError("Positive findings require evidence.")
        if state == "executed" and not step.get("output_verified"):
            raise ValueError("Execution requires a verified output.")
        outcomes.append({**step, "state": state})
    required = [s for s in outcomes if s.get("required", True)]
    return {"steps": outcomes, "execution_verified": bool(required) and all(s["state"] == "executed" for s in required)}
