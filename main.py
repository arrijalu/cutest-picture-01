"""make.fun "Cutest Picture" agent competition entry.

Ships the bundled 1024x1024 entry.png to the grader by copying its exact
bytes to /output/entry.png (falling back to ./entry.png and ./output/entry.png).
Standard library only, no network access.
"""

import os
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8\xff"


def source_path():
    """Path of entry.png that ships next to this file."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def destinations():
    """Destination paths to attempt, most important first."""
    cwd = os.getcwd()
    return [
        os.path.join("/output", "entry.png"),
        os.path.join(cwd, "entry.png"),
        os.path.join(cwd, "output", "entry.png"),
    ]


def write_bytes(path, data):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)


def main():
    src = source_path()
    try:
        with open(src, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        print("error: cannot read %s: %s" % (src, exc), file=sys.stderr)
        return 1

    if not (data.startswith(PNG_SIGNATURE) or data.startswith(JPEG_SIGNATURE)):
        print("error: %s is neither PNG nor JPEG" % src, file=sys.stderr)
        return 1

    src_real = os.path.realpath(src)
    written = []
    for dest in destinations():
        if os.path.realpath(dest) == src_real:
            continue
        try:
            write_bytes(dest, data)
        except OSError:
            continue
        written.append(dest)

    if not written:
        print("error: could not write entry.png to any destination", file=sys.stderr)
        return 1

    print("wrote %d bytes to %s" % (len(data), written[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
