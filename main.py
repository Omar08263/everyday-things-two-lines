"""Write a two-line explanation of a toaster to /output/entry.txt.

Line 1 explains the toaster to a 10-year-old in one vivid sentence built
on a single analogy (a tiny elevator). Line 2 says in one sentence why
the analogy works: what it maps (bread going down and coming back up on
its own) and what it leaves out (the glowing wires and the timer).

Deterministic: the same bytes on every run. Standard library only, no
network, no randomness, no reads outside this file.
"""

import os
from pathlib import Path

ENTRY = (
    "A toaster is a tiny elevator that carries your bread down into a hot "
    "room and pops it back up when it turns golden.\n"
    "It shows the bread going down and coming back up on its own, but it "
    "leaves out the glowing wires that do the cooking and the timer that "
    "decides when it is done."
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
