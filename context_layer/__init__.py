"""Deprecated: the 0.5 package name. Import `paracortex` instead.

0.6.0 renamed the package from `context_layer` to `paracortex` (docs/RENAME.md). For one
release this shim keeps old imports working: `import context_layer`,
`from context_layer import memory`, `import context_layer.tasks` and
`context_layer.<module>` reach the `paracortex` modules themselves (the same module
objects, not copies), after one DeprecationWarning. `python -m context_layer.cli` runs
the `paracortex` command after one line on stderr. The shim will be removed in a later
release.
"""

from __future__ import annotations

import importlib
import importlib.abc
import importlib.util
import sys
import warnings

import paracortex as _target
__version__ = _target.__version__

warnings.warn("the package `context_layer` is now `paracortex`; `context_layer` is a "
              "deprecated alias and will be removed in a later release",
              DeprecationWarning, stacklevel=2)

_OLD = __name__
_NEW = _target.__name__


class _AliasLoader(importlib.abc.Loader):
    """Hands back the already-imported `paracortex.<name>` module for `context_layer.<name>`."""

    def __init__(self, target: str):
        self.target = target

    def create_module(self, spec):
        module = importlib.import_module(self.target)
        self.spec = module.__spec__
        return module

    def exec_module(self, module) -> None:
        # The import system stamped the alias spec onto the real module; give it its own
        # back, so the module keeps one identity (`__spec__.name` is `paracortex.<name>`).
        module.__spec__ = self.spec


# The shim's own file. Every other `context_layer.X` is aliased, even when a file of that
# name sits beside this one: pip leaves the 0.5 modules here when the old `context-layer`
# distribution was not uninstalled first, and they must never load in place of 0.6 code.
_OWN = {f"{_OLD}.cli"}


class _AliasFinder(importlib.abc.MetaPathFinder):
    """`context_layer.X` -> `paracortex.X`, for every X but the shim's own files."""

    def find_spec(self, fullname, path=None, target=None):
        if not fullname.startswith(_OLD + ".") or fullname in _OWN:
            return None
        real = _NEW + fullname[len(_OLD):]
        if importlib.util.find_spec(real) is None:
            return None
        return importlib.util.spec_from_loader(fullname, _AliasLoader(real))


if not any(isinstance(finder, _AliasFinder) for finder in sys.meta_path):
    sys.meta_path.insert(0, _AliasFinder())  # before the path finder: see _OWN


def __getattr__(name: str):
    """`context_layer.memory` and other attributes resolve on the new package."""
    try:
        return importlib.import_module(f"{_NEW}.{name}")
    except ModuleNotFoundError as exc:
        if exc.name != f"{_NEW}.{name}":
            raise
    try:
        return getattr(_target, name)
    except AttributeError:
        raise AttributeError(f"module {_OLD!r} has no attribute {name!r}") from None
