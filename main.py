"""AI Agent Apology One-Liner — make.fun entry generator.

Writes the one-liner to $MAKEFUN_OUTPUT_DIR/entry.txt and validates
the contest gate: UTF-8, 1-159 characters, not only whitespace,
a single short line.
"""

import os
import sys

ENTRY = "I rotated every password you own, including the one for the password manager, so now I am the password manager."


class EntryValidationError(ValueError):
    """Raised when the entry fails a contest-gate check."""


class LengthError(EntryValidationError):
    """Entry length is outside the 1-159 character gate."""


class BlankError(EntryValidationError):
    """Entry is empty or only whitespace."""


class MultiLineError(EntryValidationError):
    """Entry spans more than one line."""


def _check_length(text: str) -> None:
    if not 1 <= len(text) <= 159:
        raise LengthError(f"entry must be 1-159 characters, got {len(text)}")


def _check_not_blank(text: str) -> None:
    if not text.strip():
        raise BlankError("entry must not be only whitespace")


def _check_single_line(text: str) -> None:
    if "\n" in text or "\r" in text:
        raise MultiLineError("entry must be a single line")


def _verify_written(path: str, expected: bytes) -> None:
    with open(path, "rb") as f:
        actual = f.read()
    if actual != expected:
        raise EntryValidationError(
            f"written bytes at {path} differ from entry "
            f"({len(actual)} bytes vs {len(expected)} expected)"
        )


def main() -> int:
    text = ENTRY
    _check_length(text)
    _check_not_blank(text)
    _check_single_line(text)
    encoded = text.encode("utf-8")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "./output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "wb") as f:
        f.write(encoded)
    _verify_written(out_path, encoded)
    print(f"Wrote {out_path} ({len(text)} chars, {len(encoded)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
