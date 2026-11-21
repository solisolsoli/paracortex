# Roadmap

Proposed work that is not built. Each item says why it waits. Nothing here is a
promise or a measured result; an item moves into a release only with its tests
and documentation, within [SCOPE.md](../SCOPE.md).

## Remove the 0.5 names

The `context-layer` command, the `context_layer` import shim, the
`CONTEXT_LAYER_*` environment fallback and the recognition of 0.5 host entries
and rule markers ([RENAME.md](RENAME.md)) are kept for one release. Remove them
in a later release, announced one release ahead in the changelog. Format
identifiers (`context-layer-task-v1` and the like) change only with their next
format version, and the reader must keep accepting the old value.

## Structure-aware retrieval for working records

[Working records](working-records.md) are retrieved as ordinary text today. Two
extensions would use their structure:

- **Newest directive wins, and the packet says so.** When a packet holds two
  numbered, dated entries from a directive log and the later one names the
  earlier ("replaces 3"), mark the earlier passage as replaced in the packet
  instead of presenting both as equal. Only explicit `replaces N` references
  would count; dates alone must not decide, because a later entry may cover a
  different scope.
- **Evidence status beside the passage.** When a delivered passage is a row of
  a claim ledger, or comes from a note whose frontmatter has a recognised
  `status`, report that status as a separate packet field, never by changing
  the passage bytes.

Why it waits: both change the evidence packet. Packets have golden digests
(`tests/test_incremental_index.py`), the README and validation numbers are
recomputed from them, and the sealed benchmark must not be used to tune
retrieval. Each needs an opt-in flag first, a dev set of its own, and a
packet-format version note.

## Templates and checks for working records

- `brain init --working-records` to create an empty `Memory Index`, a first
  handover and a directive log, not only the templates.
- A read-only `rules check` extension that reports a directive-log entry
  without a date, a reused entry number, or a claim-ledger row without a status.

Why it waits: the conventions should be used for a while as plain templates
before a checker fixes their exact shape.

## Documentation and release follow-ups

- `CONTRIBUTING.md` says hosted CI runs 11 required jobs, while the accepted run
  it links passed 12. Recount after the next accepted run on the renamed
  repository and record its link.
- Re-run the hosted CI on the renamed repository and replace the accepted-run
  links in `SCOPE.md` and `CONTRIBUTING.md` with that run.
- Submit the Obsidian plugin to the community list only after its id
  (`paracortex-brain`) is final; the id cannot change after submission.
