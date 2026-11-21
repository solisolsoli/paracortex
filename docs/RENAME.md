# Context Layer is now Paracortex

In 0.6.0 the project was renamed from **Context Layer** to **Paracortex**: *para*
means beside, so the name describes a second memory beside your own, kept in your
own files. Behaviour is unchanged. Every old name listed here still works in 0.6,
so upgrading breaks no existing setup. The old names will be removed in a later
release, which the changelog will announce.

## What changed

| Before (0.5) | Now (0.6) | Old name in 0.6 |
| --- | --- | --- |
| Distribution `context-layer` | `paracortex` (`pip install -e .` in a clone) | not published under either name |
| Command `context-layer` | `paracortex` | works; prints one line on stderr naming `paracortex` |
| Package `context_layer` | `paracortex` | `import context_layer` works with a `DeprecationWarning`; submodules are the same module objects |
| `python -m context_layer.cli` | `python -m paracortex.cli` | works; prints the same stderr line |
| Environment variables `CONTEXT_LAYER_*` | `PARACORTEX_*` | read when the new variable is unset; tasks set both for their child process |
| MCP server name `context-layer` | `paracortex` | an existing host entry keeps working until you reinstall |
| Tool names as the host shows them (`mcp__context-layer__search_vault`) | `mcp__paracortex__search_vault` | the tools themselves (`search_vault`, `read_source`, ...) are not renamed |
| Codex block `# >>> context-layer >>>`, table `[mcp_servers.context_layer]` | `# >>> paracortex >>>`, `[mcp_servers.paracortex]` | replaced on install, removed on uninstall |
| `.claude/context-layer.plan-default.json` | `.claude/paracortex.plan-default.json` | an existing marker stays in use |
| Rule-file markers `<!-- context-layer:records:start -->` | `<!-- paracortex:records:start -->` | a vault that has the old markers keeps them; records are appended between them |
| Obsidian plugin id `context-layer-brain`, "Context Layer Brain View" | `paracortex-brain`, "Paracortex Brain View" | see below: a new id is a new plugin for Obsidian |
| Repository `github.com/solisolsoli/context-layer` | `github.com/solisolsoli/paracortex` | GitHub redirects the old address after the rename |

## What did not change

- **Your vault.** Indexes, memory, tasks, ledgers and every other state file stay
  under `.context/` with the same names and formats. Nothing needs migrating and
  no index is rebuilt because of the rename.
- **Format identifiers.** Values such as `context-layer-task-v1`,
  `context-layer-ledger/v1` and `context-layer-claim-check/v1` name file and report
  formats, not the project. They stay as they are, so files written by 0.5 and 0.6
  read the same in both. They change only together with a format version.
- **MCP tool names and arguments**, packet fields, statuses and exit codes.

## How to migrate

1. In the environment that has 0.5, remove the old distribution first, then
   install 0.6 from an updated clone:

   ```sh
   python -m pip uninstall context-layer
   python -m pip install -e .
   ```

   The distribution has a new name, so pip does not replace the old one by
   itself. Both `paracortex` and the old `context-layer` command are installed.
   If 0.6 went in first, uninstall `context-layer` and then run
   `python -m pip install --force-reinstall -e .`: the old distribution's files
   include `context_layer/` and the `context-layer` script, which the 0.6
   compatibility shim reuses. Until then, `paracortex doctor` warns about it.
2. Re-run the host installer, preview first, then apply:

   ```sh
   paracortex install claude-code --vault /path/to/vault --project /path/to/repo --hook
   paracortex install claude-code --vault /path/to/vault --project /path/to/repo --hook --apply
   ```

   In `.mcp.json` the 0.5 `context-layer` entry is replaced by `paracortex`, and
   0.5 hooks are replaced by the new ones, in the same change and with the usual
   backup. Only entries that launch this tool are touched. For `--scope user` or
   `--scope local`, the installer cannot see the host's own file: run the
   `claude mcp remove --scope <scope> context-layer` line it prints. For Codex,
   `paracortex install codex` replaces the old marker block.
3. Update anything that names the tool by its old name: scripts, shell aliases,
   permission rules such as `mcp__context-layer__search_vault`, and environment
   variables (`CONTEXT_LAYER_SESSION` becomes `PARACORTEX_SESSION`, and so on).
4. `paracortex doctor /path/to/vault --host claude-code --project /path/to/repo` reports a
   0.5 host entry that is still in place.

If you skip step 2, nothing breaks: the old entry starts `context-layer mcp`, which
still runs, and the one stderr line appears in the host's server log.

## The Obsidian plugin

Obsidian identifies a plugin by its id, so the Paracortex Brain View installs next
to an existing Context Layer Brain View rather than over it. To move:

1. Copy `dist/main.js` (as `main.js`), `manifest.json` and `styles.css` into
   `<vault>/.obsidian/plugins/paracortex-brain/`.
2. To keep your settings and remembered layout, copy
   `.obsidian/plugins/context-layer-brain/data.json` into the new folder before
   enabling it.
3. Enable **Paracortex Brain View**, disable **Context Layer Brain View**, and
   delete the old folder. A workspace tab of the old view closes; open the view
   again from the ribbon.

Both plugins can be enabled at once without conflict, but there is no reason to.
