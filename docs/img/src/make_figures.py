#!/usr/bin/env python3
"""Write the documentation figures in docs/img/ as plain SVG, in a light and a dark variant.

Run from anywhere: `python3 docs/img/src/make_figures.py`. Standard library only.

Every figure uses one visual language: rounded boxes, one accent colour, a system
font stack and real <text> elements (no scripts, no external resources, no CSS),
so GitHub can show each file through an <img> tag. A Markdown page selects the
variant with <picture> and `prefers-color-scheme`.

The values drawn here are not invented. They come from:
- overview, retrieval, integrity: a run of the quick-start commands on the
  fictional starter vault (`paracortex brain init <dir> --apply`, `index`,
  `search --prompt "which timer controller did we choose and why" --method
  synaptic`), its `.context/activation.json`, and the same vault after one
  line was appended to the decision note;
- benchmark: the table in docs/validation.md (bench/results/SUMMARY.md and the
  CI bench-reproduce job), which tests/test_doc_claims.py checks.
Regenerate them by hand from those sources when the starter vault or the
benchmark changes.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[1]

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "light": {"text": "#1f2328", "muted": "#59636e", "line": "#c8d1da", "surface": "#f6f8fa",
              "accent": "#0b6e64", "accent_soft": "#e3f3f0", "warn": "#9a5b00",
              "warn_soft": "#fff4d6", "bg": "#ffffff"},
    "dark": {"text": "#e6edf3", "muted": "#9aa4ae", "line": "#3d444d", "surface": "#161b22",
             "accent": "#4cc2b0", "accent_soft": "#10302c", "warn": "#e0a73a",
             "warn_soft": "#2f2410", "bg": "#0d1117"},
}


class Svg:
    def __init__(self, width, height, theme, title, desc):
        self.w, self.h, self.c = width, height, THEMES[theme]
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">',
            f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>',
            '<defs>'
            f'<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
            f'fill="{self.c["muted"]}"/></marker>'
            f'<marker id="arrowa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
            f'fill="{self.c["accent"]}"/></marker>'
            '</defs>',
        ]

    def color(self, name):
        return self.c.get(name, name)

    def rect(self, x, y, w, h, fill="surface", stroke="line", r=10, width=1.5, dash=None):
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
                          f'fill="{self.color(fill)}" stroke="{self.color(stroke)}" '
                          f'stroke-width="{width}"{extra}/>')

    def text(self, x, y, s, size=14, color="text", weight=400, mono=False, anchor="start",
             italic=False):
        style = ' font-style="italic"' if italic else ""
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{MONO if mono else SANS}" '
                          f'font-size="{size}" font-weight="{weight}" fill="{self.color(color)}" '
                          f'text-anchor="{anchor}"{style}>{escape(s)}</text>')

    def lines(self, x, y, rows, size=14, gap=None, **kw):
        gap = gap or round(size * 1.4)
        for i, row in enumerate(rows):
            self.text(x, y + i * gap, row, size=size, **kw)

    def arrow(self, x1, y1, x2, y2, color="muted", width=1.6, dash=None):
        marker = "arrowa" if color == "accent" else "arrow"
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                          f'stroke="{self.color(color)}" stroke-width="{width}"{extra} '
                          f'marker-end="url(#{marker})"/>')

    def path(self, d, color="line", width=1.4, dash=None):
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<path d="{d}" fill="none" stroke="{self.color(color)}" '
                          f'stroke-width="{width}"{extra}/>')

    def circle(self, cx, cy, r, fill="accent"):
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{self.color(fill)}"/>')

    def save(self, name):
        (OUT / name).write_text("\n".join(self.parts + ["</svg>"]) + "\n", encoding="utf-8",
                                newline="\n")


# ---------------------------------------------------------------------------
# 1. Overview: question -> Paracortex -> original passages -> agent
# ---------------------------------------------------------------------------

OVERVIEW_ALT = ("A question goes to Paracortex on your machine, which searches your notes, "
                "follows your links and re-checks every hash, then hands the AI agent the "
                "original passages, each with its file path, line range and SHA-256 hash.")

PASSAGES = [
    ("300-Projects/", "Example - Decision - Timer Controller.md", "lines 1-36", "5961c595",
     "search hit", "2. A battery timer with two programs."),
    ("500-Knowledge/", "Example - Watering Schedule v2.md", "lines 8-22", "7f64a289",
     "reached by a link", "19:00 for 10 minutes when the day was above 28 C."),
    ("300-Projects/", "Example - Garden Irrigation.md", "lines 1-30", "a30a9582",
     "search hit", "Status: timer chosen, pipes not yet laid."),
]


def overview(theme):
    s = Svg(920, 340, theme, "Paracortex in one picture", OVERVIEW_ALT)
    # question
    s.text(16, 58, "YOUR QUESTION", size=11, color="muted", weight=600)
    s.rect(16, 70, 178, 132, fill="bg", stroke="line")
    s.lines(32, 104, ["Which timer", "controller did we", "choose, and why?"], size=15,
            weight=500)
    s.arrow(198, 136, 232, 136)
    # paracortex
    s.text(236, 58, "ON YOUR MACHINE", size=11, color="muted", weight=600)
    s.rect(236, 70, 186, 200, fill="accent_soft", stroke="accent", width=1.8)
    s.text(254, 102, "Paracortex", size=17, weight=700, color="accent")
    steps = [("1", "search your notes"), ("2", "follow your links"), ("3", "re-check each hash")]
    for i, (n, label) in enumerate(steps):
        y = 140 + i * 38
        s.circle(266, y - 5, 11, fill="accent")
        s.text(266, y, n, size=12, weight=700, color="bg", anchor="middle")
        s.text(286, y, label, size=14)
    s.text(254, 258, "no network, no model", size=12, color="muted")
    s.arrow(426, 136, 456, 136)
    # passages
    s.text(460, 58, "ORIGINAL PASSAGES, NOT SUMMARIES", size=11, color="muted", weight=600)
    for i, (folder, name, lines, sha, why, quote) in enumerate(PASSAGES):
        y = 70 + i * 88
        s.rect(460, y, 318, 78, fill="surface", stroke="line", r=8)
        s.text(474, y + 20, folder + name if len(folder + name) <= 40 else name, size=11.5,
               mono=True, weight=600)
        s.text(474, y + 39, f"{lines}  sha256 {sha}...", size=11.5, mono=True, color="muted")
        s.text(474, y + 62, quote, size=12.5, italic=True)
    s.arrow(782, 136, 812, 136)
    # agent
    s.text(816, 58, "YOUR AGENT", size=11, color="muted", weight=600)
    s.rect(816, 70, 92, 132, fill="bg", stroke="line")
    s.text(862, 104, "AI agent", size=14, weight=700, anchor="middle")
    s.lines(862, 130, ["cites path,", "lines and", "hash"], size=12, color="muted",
            anchor="middle", gap=17)
    s.text(16, 300, "Via the command line, an MCP server or a prompt hook.", size=12.5,
           color="muted")
    s.text(16, 322, "A note that changed after indexing is withheld until you re-index.",
           size=12.5, color="muted")
    s.save(f"overview-{theme}.svg")


# ---------------------------------------------------------------------------
# 2. Pipeline: index time and query time
# ---------------------------------------------------------------------------

PIPELINE_ALT = ("Two rows. When you index: your Markdown notes are scanned (exclusions, no "
                "symlinks, UTF-8 only) into a local index with a full-text table, a link graph "
                "and the SHA-256 of every note. When you ask: the question is searched with "
                "BM25 full-text search and optionally expanded along explicit links; every "
                "source is re-hashed and compared with the index, changed notes are withheld; "
                "the evidence packet goes to the agent through the CLI, the MCP server or the "
                "prompt hook.")


def box(s, x, y, w, h, title, rows, accent=False, mono_rows=()):
    s.rect(x, y, w, h, fill="accent_soft" if accent else "surface",
           stroke="accent" if accent else "line", width=1.8 if accent else 1.5)
    s.text(x + 14, y + 26, title, size=14, weight=700, color="accent" if accent else "text")
    for i, row in enumerate(rows):
        s.text(x + 14, y + 50 + i * 19, row, size=12.5, color="muted",
               mono=i in mono_rows)


def pipeline(theme):
    s = Svg(960, 420, theme, "How Paracortex works", PIPELINE_ALT)
    W, G, X0 = 162, 30, 16
    col = [X0 + i * (W + G) for i in range(5)]
    s.text(X0, 30, "WHEN YOU INDEX  (paracortex index)", size=11.5, color="muted", weight=600)
    box(s, col[0], 44, W, 112, "Your notes", ["Markdown files or", "an Obsidian vault;",
                                               "only read here"])
    s.arrow(col[0] + W + 2, 100, col[1] - 2, 100)
    box(s, col[1], 44, W, 112, "Scan", ["exclusions checked", "before any read; no", "symlinks; UTF-8 only"])
    s.arrow(col[1] + W + 2, 100, col[2] - 2, 100)
    s.rect(col[2], 44, 2 * W + G, 112, fill="surface", stroke="line")
    s.text(col[2] + 14, 70, "Local index in .context/", size=14, weight=700)
    s.lines(col[2] + 14, 94, ["full-text table (SQLite FTS5)", "link graph of your links",
                              "SHA-256 of every note"], size=12.5, color="muted", gap=19)
    s.lines(col[3] + 14, 94, ["reused when nothing", "changed; one changed", "note is re-indexed alone"],
            size=12.5, color="muted", gap=19)
    s.text(X0, 214, "WHEN YOU ASK  (search, MCP tool or prompt hook)", size=11.5,
           color="muted", weight=600)
    box(s, col[0], 228, W, 132, "Question", ["\"which timer", "controller did we", "choose and why\""])
    s.arrow(col[0] + W + 2, 294, col[1] - 2, 294)
    box(s, col[1], 228, W, 132, "Retrieve", ["full-text search,", "BM25 ranking, top 3;", "optional: follow",
                                             "explicit links"])
    s.arrow(col[1] + W + 2, 294, col[2] - 2, 294)
    box(s, col[2], 228, W, 132, "Check", ["re-hash each source", "and compare with the", "index; a changed",
                                          "note is withheld"])
    s.arrow(col[2] + W + 2, 294, col[3] - 2, 294)
    box(s, col[3], 228, W, 132, "Evidence packet", ["original text, path,", "lines and SHA-256;",
                                                    "PARTIAL, NOT_FOUND", "or ERROR"], accent=True)
    s.arrow(col[3] + W + 2, 294, col[4] - 2, 294)
    box(s, col[4], 228, W, 132, "To your agent", ["command line (JSON)", "MCP server (9 tools)",
                                                  "prompt hook", "Obsidian Brain View"])
    # index feeds retrieve and check
    s.arrow(col[2] + 60, 158, col[1] + W / 2 + 20, 226, dash="4 4")
    s.arrow(col[2] + W / 2, 158, col[2] + W / 2, 226, dash="4 4")
    s.text(X0, 396, "Dashed: reads the index. Nothing leaves your machine unless your AI host "
           "sends the packet to its model.", size=12.5, color="muted")
    s.save(f"pipeline-{theme}.svg")


# ---------------------------------------------------------------------------
# 3. Retrieval: one real spreading-activation trace
# ---------------------------------------------------------------------------

RETRIEVAL_ALT = ("The activation trace of the quick-start question on the fictional starter "
                 "vault. Three full-text hits are the seeds (activation 1.00, 1.00 and 0.96). "
                 "One hop along explicit links reaches eight notes; Watering Schedule v2 "
                 "(activation 0.154, reached from three seeds) and Drip Irrigation Basics "
                 "(0.040) were delivered in the packet; the other six were not.")

SEEDS = [("Example - Garden Irrigation", "1.00"), ("Example - 2026-01-15", "1.00"),
         ("Example - Decision - Timer Controller", "0.96")]
HOPS = [("Example - Watering Schedule v2", "0.154", True),
        ("daily/Index", "0.069", False),
        ("Example - Drip Irrigation Basics", "0.040", True),
        ("Example - Person - Sam", "0.039", False),
        ("Example - Meeting - Garden Club 2026-01-14", "0.032", False),
        ("Example - Quick Capture", "0.031", False),
        ("300-Projects/Index", "0.026", False),
        ("100-Command-Center/Dashboard", "0.012", False)]
# (seed index, hop index): edges of the trace that reach a hop-1 note
EDGES = [(1, 0), (2, 0), (0, 0), (1, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]


def retrieval(theme):
    s = Svg(920, 470, theme, "One synaptic retrieval, traced", RETRIEVAL_ALT)
    s.text(16, 30, "SEEDS: FULL-TEXT HITS (HOP 0)", size=11.5, color="muted", weight=600)
    s.text(540, 30, "NOTES ONE EXPLICIT LINK AWAY (HOP 1)", size=11.5, color="muted", weight=600)
    seed_y = [96, 196, 296]
    hop_y = [56 + i * 44 for i in range(len(HOPS))]
    for (a, b) in EDGES:
        chosen = HOPS[b][2]
        y1, y2 = seed_y[a], hop_y[b]
        s.path(f"M 336 {y1} C 440 {y1}, 440 {y2}, 540 {y2}",
               color="accent" if chosen else "line", width=2.2 if chosen else 1.3)
    for (name, act), y in zip(SEEDS, seed_y):
        s.rect(16, y - 26, 320, 52, fill="accent_soft", stroke="accent", r=8, width=1.6)
        s.text(30, y - 4, name, size=13, weight=600)
        s.text(30, y + 15, f"activation {act}", size=11.5, color="muted", mono=True)
    for (name, act, chosen), y in zip(HOPS, hop_y):
        s.rect(540, y - 17, 364, 34, fill="accent_soft" if chosen else "surface",
               stroke="accent" if chosen else "line", r=8, width=1.6 if chosen else 1.2)
        s.text(554, y + 5, name, size=12.5, weight=600 if chosen else 400,
               color="text" if chosen else "muted")
        s.text(892, y + 5, act, size=11.5, mono=True, color="accent" if chosen else "muted",
               anchor="end")
    s.text(16, 410, "contribution(u → v) = activation(u) × 0.5 × kind weight × "
           "(1 + 2 × link relevance) / degree(u) / √degree(v)", size=13, mono=True)
    s.text(16, 440, "Highlighted: delivered after the unchanged full-text packet, within 600 "
           "extra estimated tokens.", size=12.5, color="muted")
    s.text(16, 460, "Selection uses how well each link's own line matches the question, not "
           "activation alone.", size=12.5, color="muted")
    s.save(f"retrieval-{theme}.svg")


# ---------------------------------------------------------------------------
# 4. Integrity: a changed note is withheld until the next index
# ---------------------------------------------------------------------------

INTEGRITY_ALT = ("Four steps on one note. paracortex index stores its SHA-256 5961c595. You "
                 "append a line, so the file on disk now hashes to 90d173e5. paracortex search "
                 "re-hashes the note, sees the difference and withholds it with the reason "
                 "'changed since indexing'; the other passages are still delivered. After "
                 "paracortex index runs again, the note is delivered with hash 90d173e5.")


def integrity(theme):
    s = Svg(960, 300, theme, "A changed note is withheld", INTEGRITY_ALT)
    W, G, X0 = 210, 30, 16
    col = [X0 + i * (W + G) for i in range(4)]
    s.text(X0, 28, "ONE NOTE: 300-Projects/Example - Decision - Timer Controller.md",
           size=11.5, color="muted", weight=600)
    steps = [
        ("1  paracortex index", ["index stores the note's", "SHA-256"], "5961c595...", "surface", "line"),
        ("2  you edit the note", ["one line appended;", "the file now hashes to"], "90d173e5...",
         "surface", "line"),
        ("3  paracortex search", ["90d173e5 is not 5961c595:", "withheld, \"changed since",
                                  "indexing\"; other hits", "are still delivered"], None,
         "warn_soft", "warn"),
        ("4  paracortex index", ["incremental: 1 changed,", "26 unchanged; the note is",
                                 "delivered again, with"], "90d173e5...", "accent_soft", "accent"),
    ]
    for x, (title, rows, sha, fill, stroke) in zip(col, steps):
        s.rect(x, 44, W, 176, fill=fill, stroke=stroke, width=1.7)
        s.text(x + 14, 72, title, size=14, weight=700, mono=True,
               color=stroke if stroke != "line" else "text")
        s.lines(x + 14, 100, rows, size=12.5, color="text", gap=19)
        if sha:
            s.text(x + 14, 100 + len(rows) * 19 + 6, f"sha256 {sha}", size=12.5, mono=True,
                   weight=600, color="accent" if stroke == "accent" else "text")
    for i in range(3):
        s.arrow(col[i] + W + 3, 132, col[i + 1] - 3, 132)
    s.text(X0, 252, "The hash proves which bytes were indexed and that they are still the "
           "bytes on disk.", size=12.5, color="muted")
    s.text(X0, 274, "It does not prove that the text is true, relevant or safe to follow.",
           size=12.5, color="muted")
    s.save(f"integrity-{theme}.svg")


# ---------------------------------------------------------------------------
# 5. Benchmark: the sealed offline benchmark (docs/validation.md)
# ---------------------------------------------------------------------------

BENCH_ALT = ("Sealed offline benchmark, fictional 130-note vault, 72 questions. Complete "
             "evidence on the 64 answerable questions: grep 37, FTS 33, synaptic 46, synaptic "
             "compact 37. Two-hop bridge questions (20): 0, 0, 10 and 10. Mean packet size in "
             "estimated tokens: 388, 333, 527 and 334.")

BENCH = [("grep", 37, 0, 388, False), ("FTS (default)", 33, 0, 333, False),
         ("synaptic", 46, 10, 527, True), ("synaptic --compact", 37, 10, 334, False)]


def benchmark(theme):
    s = Svg(920, 300, theme, "Sealed benchmark results", BENCH_ALT)
    s.text(16, 28, "SEALED OFFLINE BENCHMARK: FICTIONAL 130-NOTE VAULT, 72 QUESTIONS, TOP 3, "
           "6,000 CHARACTERS", size=11.5, color="muted", weight=600)
    panels = [("Complete evidence, 64 answerable questions", 64, 1, 176, 280),
              ("Two-hop bridge questions (20)", 20, 2, 560, 190)]
    for title, total, idx, x0, width in panels:
        s.text(x0, 62, title, size=13, weight=700)
        for i, row in enumerate(BENCH):
            y = 84 + i * 44
            value = row[idx]
            s.rect(x0, y, width, 26, fill="surface", stroke="line", r=5, width=1)
            if value:
                s.rect(x0, y, max(6, round(width * value / total)), 26,
                       fill="accent" if row[4] else "muted", stroke="none", r=5, width=0)
            label = f"{value} of {total}" if idx == 1 else str(value)
            s.text(x0 + width + 10, y + 18, label, size=13, mono=True, weight=600 if row[4] else 400)
    s.text(810, 62, "Mean packet", size=13, weight=700)
    for i, row in enumerate(BENCH):
        y = 84 + i * 44
        s.text(16, y + 18, row[0], size=13.5, weight=700 if row[4] else 400,
               mono=row[0].startswith("synaptic --"))
        s.text(810, y + 18, f"{row[3]} tokens", size=13, mono=True, color="muted")
    s.text(16, 272, "A question counts only when every required passage arrives verbatim from "
           "the right note. Tokens: ceil(characters / 4).", size=12.5, color="muted")
    s.text(16, 292, "One fictional vault and author-written questions: this measures evidence "
           "delivery, not answer quality.", size=12.5, color="muted")
    s.save(f"benchmark-{theme}.svg")


if __name__ == "__main__":
    for theme in THEMES:
        overview(theme)
        pipeline(theme)
        retrieval(theme)
        integrity(theme)
        benchmark(theme)
    print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
