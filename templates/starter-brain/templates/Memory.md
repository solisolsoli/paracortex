---
aliases: []
related: []
supersedes:
status: active
tags: [memory]
type: preference
stated: {{date}}
---
# {{title}}

One fact, preference or standing decision per note, so each can be cited,
replaced or deleted on its own. The title states it in a few words.
`type` is one of: preference, decision, fact, reference.

## Statement

> "Quote the words as they were said or written." ({{date}})

## Why

The reason given, or the incident that led to it.

## How to apply

When this applies, and what to do differently because of it.

## Index line

Add one line for this note to the memory index (a note such as
`Memory Index`), newest last: `- [[{{title}}]] - the fact in one line`.
Agents read the index first and open only the notes they need. When a newer
note replaces this one, set `status: superseded` here, name the newer note in
its `supersedes:` field, and move this note to the archive.
