"""Write a two-line explanation of rain to /output/entry.txt.

Line 1 explains rain to a 10-year-old in one vivid sentence built on a
single analogy (a wet dog shaking water off its fur). Line 2 says in one
sentence why the analogy works: what it maps (drops leaving the cloud
when they get too heavy) and what it leaves out (clouds never shake or
choose to do it).

Deterministic: the same bytes on every run. Standard library only, no
network, no randomness, no reads outside this file.
"""

import os
from pathlib import Path

ENTRY = (
    "Rain is a cloud letting go of the tiny water drops it has gathered "
    "until they are too heavy to stay up, the way a wet dog shakes water "
    "off its fur.\n"
    "The shaking fits because the drops really do leave the cloud when "
    "they get too heavy, but it leaves out that clouds never shake or "
    "choose to do it, as the drops just grow heavy and fall on their own."
)


def emit(out_dir: Path) -> Path:
    """Write the entry text and make it readable by every user."""
    os.umask(0o022)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_bytes(ENTRY.encode("utf-8"))
    os.chmod(target, 0o644)
    return target


def confirm(target: Path) -> None:
    """Read the file back and check the gate: 1-400 UTF-8 chars, non-blank."""
    raw = target.read_bytes()
    text = raw.decode("utf-8")
    if not 1 <= len(text) <= 400:
        raise ValueError(f"entry is {len(text)} chars, outside 1-400")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if text.count("\n") != 1:
        raise ValueError("entry must be exactly two lines")


def main() -> None:
    target = emit(Path(os.environ.get("OUTPUT_DIR", "/output")))
    confirm(target)


if __name__ == "__main__":
    main()
