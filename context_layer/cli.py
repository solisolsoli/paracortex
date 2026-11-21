"""Deprecated: `python -m context_layer.cli` runs `paracortex` (docs/RENAME.md).

A host configuration written by 0.5 without the console script on PATH launches
`python -m context_layer.cli mcp ...` or `... hook ...`; this file keeps that line
working for one release. It prints one line on stderr (stdout is the protocol) and
runs the same code as `python -m paracortex.cli`.
"""

from __future__ import annotations

from paracortex import cli as _cli


def __getattr__(name: str):
    return getattr(_cli, name)


def main(argv=None) -> int:
    return _cli.legacy_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
