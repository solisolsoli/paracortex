---
aliases: []
related: []
supersedes:
status: open
tags: [claims]
---
# {{title}}

One row per claim, each with its evidence status, so a reader can see at a
glance what is established and what is not. The statuses are the ones the
Decision template uses:

- SUPPORTED: a source you opened says it; name the note or URL.
- USER_STATED: the person said it; quote it with the date.
- PARTIAL: a source supports part of it; say which part.
- NOT_FOUND: the search you ran found nothing; name where you looked. This is
  not proof that the claim is false.
- CONFLICT: sources disagree; name both, and do not pick one silently.

| # | Claim | Status | Evidence | Checked |
| --- | --- | --- | --- | --- |
| 1 |  |  |  | {{date}} |

A status changes only with a new check: update the row and its date. When a
cited note changes, Paracortex withholds it until the vault is indexed again;
re-check the rows that cite it.
