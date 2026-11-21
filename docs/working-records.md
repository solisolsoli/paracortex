# Working records for long, multi-agent work

Long projects outlive any one conversation. Several agents and several sessions
work on the same thing, and each new session starts without the previous one's
context. Five kinds of plain note keep that work resumable and checkable. Each
is a template in the starter brain (`paracortex brain init` puts them in the
`Templates` folder); nothing here needs a new command.

| Record | Holds | Rule that makes it useful |
| --- | --- | --- |
| Memory note + memory index | one fact, preference or standing decision per note | one note per fact; the index has one line per note |
| Handover | where the work stands, dated, for the next session | append dated status sections; link the previous handover |
| Directive log | the owner's decisions and instructions | word for word, dated, numbered; nothing else in the note |
| Claim ledger | claims, each with an evidence status | a status changes only with a new, dated check |
| Board | the plan, before the work | written and agreed before any result is produced |

The notes you create from these templates are ordinary vault notes: `index`
indexes them and `search` returns their passages verbatim with path and
SHA-256, like any other note. The `Templates` folder itself is excluded from
search, so placeholders are never quoted as evidence.

## Memory notes and the memory index

One fact per note means each fact can be cited, replaced or deleted on its own,
and a search returns that fact rather than a long page of unrelated ones. The
frontmatter says what kind of fact it is (`type: preference`, `decision`,
`fact` or `reference`) and when it was stated. The body quotes the words, then
says why and how to apply them.

The index is one note with one line per memory, so an agent reads a short list
first and opens only what it needs. A fictional example:

```markdown
# Memory Index

- [[Water before 07:00]] - the garden is watered before 07:00 on hot days
- [[Timer batteries]] - replace the timer batteries every March
```

This is separate from `paracortex memory` ([memory.md](memory.md)), which keeps
tool-written records with source hashes under `.context/memory/`. Memory notes
are written and corrected by people; `memory` records are append-only and
written by tools. They work together: a memory record can cite a memory note
as its source.

## Handover

A handover is a dated running log. Each time the work moves, add a section
headed with the date and time from the clock: what was done and how it was
verified, where it stopped, the next steps in order, what is waiting on
someone, and the problems met. Never rewrite an earlier section; start a new
handover note for a new day or phase and link the previous one, so the chain
can be followed backwards.

The starter brain's `Last-Session` note is the short version, overwritten each
session. A handover is for work that spans many sessions or several agents.

## Directive log

The owner's decisions, word for word, with the date (and the time when the
order within a day matters), numbered in one sequence. Plans and status go
elsewhere, so the log stays a record of what was actually said, against which
any summary can be checked. Rules:

- quote exactly; label a transcription or a translation as one;
- mark a question as a question;
- never edit an entry; a later entry names the number it replaces;
- the newest entry wins for what it covers; if two entries conflict and
  neither names the other, ask.

A fictional example:

```markdown
## 2026-03-02

4. "Water the beds before seven on any day above 28 degrees." (after the
   heat wave)
5. "Should we add a third program?" (a question, not a decision)

## 2026-03-09

6. "Keep two programs; no third one this year." (replaces 5's open question)
```

## Claim ledger

One row per claim with its evidence status: SUPPORTED, USER_STATED, PARTIAL,
NOT_FOUND or CONFLICT (the labels the Decision template already uses). NOT_FOUND
means a search found nothing where it looked, not that the claim is false.
When a cited note changes, Paracortex withholds its old passage until the vault
is indexed again; that is the moment to re-check the rows that cite it.

```markdown
| # | Claim | Status | Evidence | Checked |
| --- | --- | --- | --- | --- |
| 1 | The timer has two programs | SUPPORTED | Example - Decision - Timer Controller | 2026-03-09 |
| 2 | The battery lasts a season | NOT_FOUND | searched the vault for "battery life" | 2026-03-09 |
```

## Board

A board is written before the work starts: the goal, the binding constraints
(linked to the directive log), the options and why each was chosen or
rejected, the plan with a check per step, open questions and what is out of
scope. Agents start from an agreed board, not from a one-line request.

## What Paracortex does with them today

Paracortex retrieves these notes like any others; it does not yet read their
structure. It does not compare dates between two directive entries, and it
does not attach a claim's status to the passage it returns. Supersession works
through the archive: move a replaced note there and it is excluded from search
([brain-guide.md](brain-guide.md)). Structure-aware retrieval is listed in the
[roadmap](ROADMAP.md).
