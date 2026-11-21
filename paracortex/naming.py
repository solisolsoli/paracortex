"""paracortex.naming - the project's names, and the 0.5 names that still work.

0.6.0 renamed the project from Context Layer to Paracortex. For one release the old
spellings keep working, so an existing host configuration, script or environment does
not break on upgrade (docs/RENAME.md):

- `PARACORTEX_*` environment variables are read first; the 0.5 spelling
  `CONTEXT_LAYER_*` is read when the new one is unset (`getenv`);
- variables this tool sets for a child process are set under both spellings
  (`child_env`), so a backend script written for 0.5 still finds them;
- host entries, hook commands and rule-file markers written by 0.5 are recognised
  (and replaced or removed) by `install`, `uninstall` and `rules`.

Format identifiers such as `context-layer-task-v1` are not names: they label files
already on disk and stay unchanged until their format version changes.

Standard library only; imported by the hooks, so it stays small.
"""

from __future__ import annotations

import os

NAME = "paracortex"
LEGACY_NAME = "context-layer"
ENV_PREFIX = "PARACORTEX_"
LEGACY_ENV_PREFIX = "CONTEXT_LAYER_"


def legacy_env_name(key: str) -> "str | None":
    """`CONTEXT_LAYER_X` for `PARACORTEX_X`; None for any other variable."""
    if key.startswith(ENV_PREFIX):
        return LEGACY_ENV_PREFIX + key[len(ENV_PREFIX):]
    return None


def getenv(key: str, default: "str | None" = None, environ=None) -> "str | None":
    """`os.environ[key]`, else its 0.5 spelling (`CONTEXT_LAYER_*`), else `default`.

    A variable set under the new name wins, even when it is empty, so a caller can
    clear a value the old name still sets."""
    environ = os.environ if environ is None else environ
    value = environ.get(key)
    if value is not None:
        return value
    legacy = legacy_env_name(key)
    if legacy is not None:
        value = environ.get(legacy)
        if value is not None:
            return value
    return default


def child_env(env: dict, key: str, value: str) -> dict:
    """Set `key` and its 0.5 spelling in `env` (a child process's environment)."""
    env[key] = value
    legacy = legacy_env_name(key)
    if legacy is not None:
        env[legacy] = value
    return env


def drop_env(env: dict, key: str) -> dict:
    """Remove `key` and its 0.5 spelling from `env`."""
    env.pop(key, None)
    legacy = legacy_env_name(key)
    if legacy is not None:
        env.pop(legacy, None)
    return env
