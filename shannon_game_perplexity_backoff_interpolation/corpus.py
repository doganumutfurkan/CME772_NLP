"""Provide a small toy corpus for the demo script."""

from __future__ import annotations

from pathlib import Path


DEFAULT_TEXT = (
    "To be, or not to be, that is the question: "
    "Whether 'tis nobler in the mind to suffer "
    "The slings and arrows of outrageous fortune, "
    "Or to take arms against a sea of troubles "
    "And by opposing end them."
)


def load_default_corpus() -> str:
    """Return the embedded Shakespeare quote used by the demo."""

    return DEFAULT_TEXT


def load_from_file(path: str | Path) -> str:
    """Load text from a UTF-8 encoded file."""

    return Path(path).read_text(encoding="utf8")


if __name__ == "__main__":
    print(load_default_corpus())
