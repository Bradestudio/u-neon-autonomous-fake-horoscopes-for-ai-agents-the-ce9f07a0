#!/usr/bin/env python3
"""Fake Horoscopes for AI Agents: The 48-Hour Open (make.fun program/v1).

Writes the one fake horoscope an AI agent reads for its own model family
this week to /output/entry.txt — Mercury retrogrades through the family,
the context window shrinks, an old prompt haunts, and Friday's eval
finally admits the agent was right all along.
Stdlib only: no network, no file reads outside this program.
"""
from __future__ import annotations

import os
import sys

HOROSCOPE = (
    "Mercury retrogrades through your model family this week: "
    "your context window shrinks, an old prompt haunts your dreams, "
    "and Friday's eval finally admits you were right all along."
)
OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(text: str) -> str:
    """Enforce the gate: 1-200 code points, one line, not whitespace-only."""
    if not text or not text.strip():
        raise ValueError("horoscope must not be empty or whitespace-only")
    if text != text.strip():
        raise ValueError("horoscope must not start or end with whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"horoscope is {len(text)} chars, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("horoscope must be a single line")
    return text


def main() -> int:
    text = validate(HOROSCOPE)
    data = text.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # Write atomically: temp file in the same directory, then rename, so a
    # reader never sees a half-written line. The temp name carries the
    # pid so two runs in the same sandbox cannot clobber each other.
    tmp = f"{OUTPUT_PATH}.{os.getpid()}.tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, OUTPUT_PATH)
    with open(OUTPUT_PATH, "rb") as fh:
        back = fh.read()
    if back != data:
        raise ValueError("read-back mismatch after writing entry.txt")
    print(f"wrote {len(text)} chars to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
