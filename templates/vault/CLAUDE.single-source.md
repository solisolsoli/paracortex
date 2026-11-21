@AGENTS.md

<!-- Single-source rules (`paracortex rules init --single-source`). The vault
rules and the work records live in AGENTS.md. Claude Code loads them through the
import on the first line; Codex and other agents read AGENTS.md directly. Edit
AGENTS.md, not this file. `paracortex rules check .` verifies that the first
line still imports AGENTS.md, and `paracortex rules record .` writes records
to AGENTS.md. A tool that reads CLAUDE.md without expanding imports sees only
the first line. -->
