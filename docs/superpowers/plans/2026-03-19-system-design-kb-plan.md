# System Design Knowledge Base — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform raw source materials (5 PDFs + 9 markdown reports) into a deduplicated, concept-driven system design knowledge base with 57 canonical topic files.

**Architecture:** Phase 0 builds a Python extraction script for PDFs, Phase 1 runs 3 parallel agents for source analysis, Phase 2 runs 3 parallel agents across 2 batches for doc generation, Phase 3 finalizes with cross-link verification and quality checks.

**Tech Stack:** Python 3 + PyMuPDF >= 1.23.0, Markdown, Mermaid diagrams

**Spec:** `docs/superpowers/specs/2026-03-19-system-design-kb-design.md`

---

## File Map

### Scripts (Phase 0)
- Create: `scripts/extract_pdfs.py` — Main extraction script
- Create: `scripts/verify_docs.py` — Cross-link and quality verification script (Phase 3)

### Extracted Output (Phase 0 — generated, not hand-written)
- Generated: `source/extracted/ddia/*.md` (~12 chapter files)
- Generated: `source/extracted/alex-xu-vol2/*.md` (~13 chapter files)
- Generated: `source/extracted/acing-system-design/*.md` (~17 chapter files)
- Generated: `source/extracted/system-design-guide/*.md` (~16 chapter files)
- Generated: `source/extracted/grokking/*.md` (~15 section files)
- Generated: `source/extracted/manifest.json`

### Meta Docs (Phase 1 — agent-generated)
- Create: `docs/meta/source-inventory.md`
- Create: `docs/meta/concept-index.md`
- Create: `docs/meta/source-map.md`
- Create: `docs/glossary.md`

### Canonical Topic Files (Phase 2 — agent-generated, 57 files)
- Create: `docs/fundamentals/*.md` (6 files)
- Create: `docs/scalability/*.md` (4 files)
- Create: `docs/storage/*.md` (8 files)
- Create: `docs/caching/*.md` (3 files)
- Create: `docs/messaging/*.md` (4 files)
- Create: `docs/architecture/*.md` (3 files)
- Create: `docs/resilience/*.md` (4 files)
- Create: `docs/security/*.md` (3 files)
- Create: `docs/observability/*.md` (2 files)
- Create: `docs/api-design/*.md` (4 files)
- Create: `docs/patterns/*.md` (6 files)
- Create: `docs/case-studies/*.md` (10 files)

### Navigation (Phase 3)
- Create: `docs/index.md`

---

## Task 1: Project Setup

**Files:**
- Create: `scripts/` directory
- Create: `source/extracted/` directory structure
- Create: `docs/` directory structure

- [ ] **Step 1: Create all required directories**

```bash
mkdir -p scripts
mkdir -p source/extracted/{ddia,alex-xu-vol2,acing-system-design,system-design-guide,grokking}
mkdir -p docs/{fundamentals,scalability,storage,caching,messaging,architecture,resilience,security,observability,api-design,patterns,case-studies,meta}
```

- [ ] **Step 2: Verify PyMuPDF version**

```bash
python3 -c "import fitz; print(fitz.__version__)"
```

Expected: Version >= 1.23.0. If not installed or too old:

```bash
pip3 install --upgrade pymupdf
```

- [ ] **Step 3: Add .gitkeep files so directories are tracked**

```bash
find scripts source/extracted docs -type d -empty -exec touch {}/.gitkeep \;
```

- [ ] **Step 4: Commit project structure**

```bash
git add scripts/ source/extracted/ docs/
git commit -m "scaffold: create directory structure for knowledge base"
```

---

## Task 2: Build PDF Extraction Script — Core Framework

**Files:**
- Create: `scripts/extract_pdfs.py`

This task builds the script skeleton: PDF loading, TOC parsing, chapter boundary detection, and output writing. Subsequent tasks add heuristics.

- [ ] **Step 1: Write the extraction script core**

Create `scripts/extract_pdfs.py` with:

```python
#!/usr/bin/env python3
"""
PDF Extraction Script for System Design Knowledge Base.

Extracts structured markdown from PDF books, organized by chapter.
Requires: PyMuPDF >= 1.23.0 (pip install pymupdf)

Usage: python3 scripts/extract_pdfs.py
"""

import fitz  # PyMuPDF
import json
import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

# --- Configuration ---

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "source"
OUTPUT_DIR = SOURCE_DIR / "extracted"

BOOKS = [
    {
        "pdf": SOURCE_DIR / "system-design-books" / "Designing Data-Intensive Applications.pdf",
        "output_dir": OUTPUT_DIR / "ddia",
        "short_name": "DDIA",
        "full_name": "Designing Data-Intensive Applications (Martin Kleppmann)",
        "has_toc": True,
    },
    {
        "pdf": SOURCE_DIR / "system-design-books" / "System Design Interview – An Insider's Guide_ Volume 2.pdf",
        "output_dir": OUTPUT_DIR / "alex-xu-vol2",
        "short_name": "Alex Xu Vol 2",
        "full_name": "System Design Interview – An Insider's Guide: Volume 2 (Alex Xu)",
        "has_toc": True,
    },
    {
        "pdf": SOURCE_DIR / "system-design-books" / "Zhiyong Tan - Acing the System Design Interview (2024, Manning Publications) - libgen.li.pdf",
        "output_dir": OUTPUT_DIR / "acing-system-design",
        "short_name": "Acing SDI",
        "full_name": "Acing the System Design Interview (Zhiyong Tan, 2024)",
        "has_toc": True,
    },
    {
        "pdf": SOURCE_DIR / "system-design-books" / "System Design Guide for Software Professionals.pdf",
        "output_dir": OUTPUT_DIR / "system-design-guide",
        "short_name": "SD Guide",
        "full_name": "System Design Guide for Software Professionals",
        "has_toc": True,
    },
    {
        "pdf": SOURCE_DIR / "system-design-notes" / "System Design - Grokking.pdf",
        "output_dir": OUTPUT_DIR / "grokking",
        "short_name": "Grokking",
        "full_name": "System Design - Grokking (Notes)",
        "has_toc": False,
    },
]


@dataclass
class Chapter:
    """Represents an extracted chapter."""
    title: str
    chapter_num: int
    start_page: int  # 0-indexed
    end_page: int    # 0-indexed, exclusive
    book_name: str
    book_short: str


@dataclass
class ExtractionResult:
    """Result of extracting a single book."""
    book_short: str
    book_full: str
    chapters_extracted: int
    files_generated: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    status: str = "success"


# --- TOC Parsing ---

def get_chapters_from_toc(doc: fitz.Document, book: dict) -> list[Chapter]:
    """Extract chapter boundaries from PDF TOC bookmarks."""
    toc = doc.get_toc()
    if not toc:
        return []

    chapters = []
    chapter_num = 0

    for i, (level, title, page) in enumerate(toc):
        # Only top-level or level-2 entries that look like chapters
        if level > 2:
            continue

        # Skip front matter (preface, foreword, acknowledgments, TOC, copyright, etc.)
        skip_patterns = [
            r"(?i)^(preface|foreword|acknowledge|copyright|table of contents|contents$|"
            r"about|index$|colophon|glossary$|afterword|safari|how to contact|"
            r"references|contributors|share your|download|get in touch|conventions|"
            r"who should|what this|livebook|other online|cover illustration)"
        ]
        if any(re.match(p, title.strip()) for p in skip_patterns):
            continue

        # Detect chapter-like entries
        is_chapter = (
            re.match(r"(?i)^(chapter\s+\d|part\s+\d|\d+[\.\s])", title.strip())
            or (level == 1 and len(title.strip()) > 3)
        )

        if not is_chapter:
            continue

        chapter_num += 1
        start_page = page - 1  # TOC pages are 1-indexed

        # Find end page: next chapter's start or end of doc
        end_page = doc.page_count
        for j in range(i + 1, len(toc)):
            next_level, _, next_page = toc[j]
            if next_level <= level:
                end_page = next_page - 1
                break

        chapters.append(Chapter(
            title=title.strip(),
            chapter_num=chapter_num,
            start_page=max(0, start_page),
            end_page=min(end_page, doc.page_count),
            book_name=book["full_name"],
            book_short=book["short_name"],
        ))

    return chapters


def get_chapters_by_font_analysis(doc: fitz.Document, book: dict) -> list[Chapter]:
    """Detect chapters in PDFs without TOC using font size analysis.

    Strategy: compute median body font size, flag lines >= 1.3x median as headers.
    Also detect ALL CAPS lines of length > 10 as headers.
    """
    # Pass 1: collect all font sizes to find median body size
    font_sizes = []
    for page_num in range(doc.page_count):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if len(text) > 5:  # Skip tiny fragments
                        font_sizes.append(span["size"])

    if not font_sizes:
        return []

    font_sizes.sort()
    median_size = font_sizes[len(font_sizes) // 2]
    header_threshold = median_size * 1.3

    # Pass 2: find section headers
    chapters = []
    chapter_num = 0

    for page_num in range(doc.page_count):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                line_text = "".join(span["text"] for span in line["spans"]).strip()
                max_font = max((span["size"] for span in line["spans"]), default=0)

                is_header = False
                # Check font size
                if max_font >= header_threshold and len(line_text) > 5:
                    is_header = True
                # Check ALL CAPS
                if (line_text.isupper() and len(line_text) > 10
                        and not line_text.startswith("HTTP")):
                    is_header = True

                if is_header and len(line_text) < 200:  # Headers shouldn't be paragraphs
                    # Close previous chapter
                    if chapters:
                        chapters[-1].end_page = page_num

                    chapter_num += 1
                    chapters.append(Chapter(
                        title=line_text,
                        chapter_num=chapter_num,
                        start_page=page_num,
                        end_page=doc.page_count,
                        book_name=book["full_name"],
                        book_short=book["short_name"],
                    ))

    # Merge very short "chapters" (< 1 page) into their successor
    merged = []
    for ch in chapters:
        page_span = ch.end_page - ch.start_page
        if merged and page_span < 1:
            # Absorb into previous
            merged[-1].end_page = ch.end_page
        else:
            merged.append(ch)

    return merged


# --- Text Extraction ---

def extract_page_text(page: fitz.Page) -> str:
    """Extract clean text from a single page."""
    text = page.get_text("text")
    # Clean common PDF artifacts
    text = re.sub(r'\n{3,}', '\n\n', text)  # Collapse excessive newlines
    text = re.sub(r'(?<=[a-z])-\n(?=[a-z])', '', text)  # Rejoin hyphenated words
    return text


def extract_tables_from_page(page: fitz.Page) -> list[str]:
    """Extract tables using PyMuPDF's find_tables API."""
    tables_md = []
    try:
        tables = page.find_tables()
        for table in tables:
            data = table.extract()
            if not data or len(data) < 2:
                continue
            # Convert to markdown table
            headers = data[0]
            md = "| " + " | ".join(str(h or "").strip() for h in headers) + " |\n"
            md += "| " + " | ".join("---" for _ in headers) + " |\n"
            for row in data[1:]:
                md += "| " + " | ".join(str(c or "").strip() for c in row) + " |\n"
            tables_md.append(md)
    except Exception:
        pass  # Graceful fallback if find_tables unavailable
    return tables_md


def tag_examples(text: str) -> list[str]:
    """Identify example/scenario passages in text."""
    examples = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        is_example = (
            re.match(r'(?i)^\s*(example|case study|scenario)\s*[:.]', line)
            or re.search(r'(?i)for example,|for instance,|e\.g\.,', line)
        )
        if is_example:
            # Capture this line and the next few lines as context
            example_lines = [line.strip()]
            j = i + 1
            while j < len(lines) and j < i + 10 and lines[j].strip():
                example_lines.append(lines[j].strip())
                j += 1
            examples.append('\n'.join(example_lines))
            i = j
        else:
            i += 1
    return examples


def tag_comparisons(text: str) -> list[str]:
    """Identify comparison/tradeoff passages near section headers."""
    comparisons = []
    lines = text.split('\n')
    # Find header line indices for proximity check
    header_indices = set()
    for i, line in enumerate(lines):
        if re.match(r'^#{1,4}\s', line) or (line.isupper() and len(line.strip()) > 10):
            for j in range(max(0, i - 2), min(len(lines), i + 15)):
                header_indices.add(j)

    for i, line in enumerate(lines):
        if re.search(r'(?i)\bvs\.?\b|\bpros and cons\b|\btradeoff\b|\btrade-off\b|\bcomparison\b', line):
            # Prefer matches near headers to reduce false positives
            near_header = i in header_indices
            if near_header or re.match(r'^#{1,4}\s', lines[max(0, i-3)].strip() if i >= 3 else ''):
                start = max(0, i - 1)
                end = min(len(lines), i + 5)
                comparisons.append('\n'.join(l.strip() for l in lines[start:end] if l.strip()))
    return comparisons


# --- Chapter to Markdown ---

def chapter_to_markdown(doc: fitz.Document, chapter: Chapter) -> str:
    """Convert a chapter's pages to structured markdown."""
    # Extract full text
    full_text = ""
    all_tables = []

    for page_num in range(chapter.start_page, chapter.end_page):
        if page_num >= doc.page_count:
            break
        page = doc[page_num]
        full_text += extract_page_text(page) + "\n\n"
        all_tables.extend(extract_tables_from_page(page))

    # Tag content
    examples = tag_examples(full_text)
    comparisons = tag_comparisons(full_text)

    # Build markdown
    md = f"# {chapter.title}\n\n"
    md += f"> Source: {chapter.book_name}, Chapter {chapter.chapter_num}, "
    md += f"Pages {chapter.start_page + 1}-{chapter.end_page}\n\n"

    # Key concepts: extract from first few paragraphs
    md += "## Key Concepts\n\n"
    first_paragraphs = full_text[:2000].split('\n\n')
    for para in first_paragraphs[:5]:
        clean = para.strip()
        if clean and len(clean) > 20:
            md += f"- {clean[:200]}\n"
    md += "\n"

    # Full content
    md += "## Content\n\n"
    md += full_text.strip() + "\n\n"

    # Examples (only if found)
    if examples:
        md += "## Examples & Scenarios\n\n"
        for ex in examples[:20]:  # Cap at 20
            md += f"- {ex}\n\n"

    # Tables (only if found)
    if all_tables:
        md += "## Tables & Comparisons\n\n"
        for table in all_tables:
            md += table + "\n"

    # Comparisons as takeaways if no tables
    if comparisons and not all_tables:
        md += "## Key Takeaways\n\n"
        for comp in comparisons[:10]:
            md += f"- {comp}\n\n"

    return md


def slugify(title: str) -> str:
    """Convert a chapter title to a filename slug."""
    # Remove chapter numbering prefix
    title = re.sub(r'^(chapter\s+\d+[\.:]\s*|part\s+\d+[\.:]\s*|\d+[\.\s]+)', '', title, flags=re.IGNORECASE)
    # Convert to slug
    slug = title.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug[:60]  # Cap length


# --- Main Extraction ---

def extract_book(book: dict) -> ExtractionResult:
    """Extract all chapters from a single book."""
    result = ExtractionResult(
        book_short=book["short_name"],
        book_full=book["full_name"],
        chapters_extracted=0,
    )

    pdf_path = book["pdf"]
    if not pdf_path.exists():
        result.status = "failed"
        result.errors.append(f"PDF not found: {pdf_path}")
        return result

    try:
        doc = fitz.open(str(pdf_path))
    except Exception as e:
        result.status = "failed"
        result.errors.append(f"Failed to open PDF: {e}")
        return result

    # Get chapters
    if book["has_toc"]:
        chapters = get_chapters_from_toc(doc, book)
    else:
        chapters = get_chapters_by_font_analysis(doc, book)

    if not chapters:
        result.status = "failed"
        result.errors.append("No chapters detected")
        doc.close()
        return result

    # Create output directory
    output_dir = book["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n  Extracting {book['short_name']}: {len(chapters)} chapters detected")

    for chapter in chapters:
        try:
            md_content = chapter_to_markdown(doc, chapter)

            # Generate filename
            slug = slugify(chapter.title)
            filename = f"ch{chapter.chapter_num:02d}-{slug}.md"
            filepath = output_dir / filename

            filepath.write_text(md_content, encoding="utf-8")
            result.files_generated.append(str(filepath.relative_to(BASE_DIR)))
            result.chapters_extracted += 1

            print(f"    ✓ {filename} ({chapter.end_page - chapter.start_page} pages)")

        except Exception as e:
            result.errors.append(f"Chapter '{chapter.title}': {e}")
            print(f"    ✗ {chapter.title}: {e}")

    doc.close()

    if result.chapters_extracted == 0:
        result.status = "failed"
    elif result.errors:
        result.status = "partial"

    return result


def write_manifest(results: list[ExtractionResult]):
    """Write extraction manifest for Phase 1 validation gate."""
    manifest = {
        "extraction_complete": True,
        "books": [],
        "total_files": 0,
        "total_errors": 0,
        "books_succeeded": 0,
        "books_failed": 0,
    }

    for r in results:
        book_entry = asdict(r)
        manifest["books"].append(book_entry)
        manifest["total_files"] += len(r.files_generated)
        manifest["total_errors"] += len(r.errors)
        if r.status in ("success", "partial"):
            manifest["books_succeeded"] += 1
        else:
            manifest["books_failed"] += 1

    # Gate check
    manifest["phase1_gate"] = manifest["books_succeeded"] >= 4

    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def validate_output(manifest: dict):
    """Validate extraction output meets minimum quality bar."""
    print("\n" + "=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)

    for book in manifest["books"]:
        status_icon = "✓" if book["status"] in ("success", "partial") else "✗"
        print(f"  {status_icon} {book['book_short']}: {book['chapters_extracted']} chapters, "
              f"{len(book['files_generated'])} files")
        if book["errors"]:
            for err in book["errors"]:
                print(f"    ⚠ {err}")

    print(f"\n  Total files: {manifest['total_files']}")
    print(f"  Total errors: {manifest['total_errors']}")
    print(f"  Books succeeded: {manifest['books_succeeded']}/5")
    print(f"  Phase 1 gate: {'PASS' if manifest['phase1_gate'] else 'FAIL'}")

    # Validate each file is non-empty
    empty_files = []
    for book in manifest["books"]:
        for fpath in book["files_generated"]:
            full_path = BASE_DIR / fpath
            if full_path.exists():
                content = full_path.read_text(encoding="utf-8")
                if len(content) < 100:
                    empty_files.append(fpath)

    if empty_files:
        print(f"\n  ⚠ {len(empty_files)} files below 100 char minimum:")
        for f in empty_files:
            print(f"    - {f}")

    print("=" * 60)
    return manifest["phase1_gate"]


def main():
    print("=" * 60)
    print("PDF EXTRACTION FOR SYSTEM DESIGN KNOWLEDGE BASE")
    print("=" * 60)

    # Verify PyMuPDF version
    version = fitz.__version__.split(".")
    major, minor = int(version[0]), int(version[1])
    if major < 1 or (major == 1 and minor < 23):
        print(f"WARNING: PyMuPDF {fitz.__version__} < 1.23.0. Table extraction may not work.")
        print("Run: pip install --upgrade pymupdf")

    results = []
    for book in BOOKS:
        print(f"\nProcessing: {book['short_name']}...")
        result = extract_book(book)
        results.append(result)

    manifest = write_manifest(results)
    gate_passed = validate_output(manifest)

    if not gate_passed:
        print("\n❌ Phase 1 gate FAILED. 2+ books failed extraction.")
        print("Fix errors above and re-run, or proceed with degraded coverage.")
        sys.exit(1)
    else:
        print("\n✅ Phase 1 gate PASSED. Ready for Phase 1 agents.")
        sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the script on a single book to verify basic functionality**

```bash
python3 -c "
import fitz, sys
sys.path.insert(0, 'scripts')
from extract_pdfs import extract_book, BOOKS
result = extract_book(BOOKS[0])  # DDIA
print(f'Status: {result.status}, Chapters: {result.chapters_extracted}')
for f in result.files_generated[:3]:
    print(f'  {f}')
"
```

Expected: Multiple chapter files extracted from DDIA.

- [ ] **Step 3: Verify an extracted file looks reasonable**

Read one of the extracted DDIA chapter files. Confirm it has:
- Title and source attribution
- Key Concepts section
- Content section with actual text
- Tables if the chapter had them

- [ ] **Step 4: Commit extraction script**

```bash
git add scripts/extract_pdfs.py
git commit -m "feat: add PDF extraction script with TOC parsing and font analysis"
```

---

## Task 3: Run Full PDF Extraction

**Files:**
- Run: `scripts/extract_pdfs.py`
- Generated: `source/extracted/**/*.md`, `source/extracted/manifest.json`

- [ ] **Step 1: Run the full extraction**

```bash
python3 scripts/extract_pdfs.py
```

Expected: Summary showing 4-5 books extracted successfully. Phase 1 gate PASS.

- [ ] **Step 2: Spot-check extracted quality**

Read 2-3 files from different books to verify extraction quality:
- One DDIA chapter (deep technical content)
- One Alex Xu chapter (case study format)
- One Grokking section (notes format without TOC)

Check that content is readable and structured, tables are captured, examples are tagged.

- [ ] **Step 3: Fix any extraction issues**

If a book failed or quality is poor, adjust heuristics in the script and re-run for that book.

- [ ] **Step 4: Commit extracted content**

```bash
git add source/extracted/
git commit -m "data: extract structured markdown from all PDF source materials"
```

---

## Task 4: Phase 1 — Source Analysis (3 Parallel Agents)

**Files:**
- Create: `docs/meta/source-inventory.md` (Agent 1)
- Create: `docs/meta/concept-index.md` (Agent 2)
- Create: `docs/meta/source-map.md` + `docs/glossary.md` (Agent 3)

**Pre-condition:** `source/extracted/manifest.json` exists and shows `phase1_gate: true`

- [ ] **Step 1: Dispatch 3 agents in parallel**

Launch all 3 agents simultaneously. Each agent receives the full input scope:
- YouTube reports: `source/youtube-video-reports/1.md` through `9.md`
- Extracted PDFs: `source/extracted/**/*.md`
- Exclude: `initialize.md`, `x-prompts.txt`

**Agent 1 prompt — Source Inventory:**
```
You are building a source inventory for a system design knowledge base.

Read ALL source files:
- YouTube reports: source/youtube-video-reports/1.md through 9.md
- Extracted PDF chapters: source/extracted/**/*.md (read the manifest at source/extracted/manifest.json first for the file list)

DO NOT read initialize.md or x-prompts.txt — these are not source materials.

Create /docs/meta/source-inventory.md with this structure:

# Source Inventory

## YouTube Video Reports
For each file (1.md through 9.md):
- File name
- Short description (1-2 sentences)
- Key concepts covered (bullet list)

## PDF Books (Extracted)
For each book directory in source/extracted/:
- Book name and author
- Number of chapters extracted
- For each chapter file:
  - File name
  - Short description
  - Key concepts covered

Write the file to: docs/meta/source-inventory.md
```

**Agent 2 prompt — Concept Index:**
```
You are building a master concept index for a system design knowledge base.

Read ALL source files:
- YouTube reports: source/youtube-video-reports/1.md through 9.md
- Extracted PDF chapters: source/extracted/**/*.md

Create /docs/meta/concept-index.md — a deduplicated master list of ALL system design concepts found across all sources.

Structure:

# Concept Index

## How to Use This Index
(Brief explanation: each concept appears ONCE, mapped to its canonical file)

## Fundamentals
| Concept | Canonical File | Aliases | Related Concepts |
|---------|---------------|---------|-----------------|
| System Design Framework | fundamentals/system-design-framework.md | requirements gathering, interview framework | back-of-envelope-estimation |
(continue for all concepts in this domain...)

## Scalability
(same table format)

## Storage
(same table format)

(Continue for ALL domains: Caching, Messaging, Architecture, Resilience, Security, Observability, API Design, Patterns, Case Studies)

IMPORTANT Content Boundaries — these MUST be documented in the index:
- Fan-out (read vs write, hybrid) → owned by patterns/fan-out.md
- Saga pattern → owned by resilience/distributed-transactions.md
- 2PC → owned by resilience/distributed-transactions.md
- Event sourcing → owned by messaging/event-sourcing.md
- CQRS → owned by messaging/cqrs.md
- Caching strategies → owned by caching/caching.md (NOT redis.md)
- Redis internals → owned by caching/redis.md
- Inverted index / Elasticsearch → owned by patterns/search-and-indexing.md
- Geospatial indexing → owned by patterns/geospatial-indexing.md
- Batch/stream processing → section within messaging/event-driven-architecture.md
- WAL and CDC → section within storage/database-replication.md
- Service discovery → section within architecture/microservices.md
- Networking (DNS, TCP/UDP) → fundamentals/networking-fundamentals.md
- Scalability overview → fundamentals/scaling-overview.md (scalability/ folder has mechanisms)

The full taxonomy has 57 canonical topic files. See the folder structure in the spec.

Write the file to: docs/meta/concept-index.md
```

**Agent 3 prompt — Source Map + Glossary:**
```
You are building a source traceability map and glossary for a system design knowledge base.

Read ALL source files:
- YouTube reports: source/youtube-video-reports/1.md through 9.md
- Extracted PDF chapters: source/extracted/**/*.md

Create TWO files:

FILE 1: /docs/meta/source-map.md

# Source Traceability Map

For each canonical topic file in the knowledge base, list which source files contain relevant content.

Format:
## fundamentals/
### system-design-framework.md
- source/youtube-video-reports/2.md (requirements framework section)
- source/youtube-video-reports/6.md (Hello Interview delivery framework)
- source/extracted/acing-system-design/ch02-*.md (interview flow)
- source/extracted/system-design-guide/ch01-*.md (basics)
(etc.)

### scaling-overview.md
- source/youtube-video-reports/2.md (scaling paradigm section)
(etc.)

(Continue for ALL 57 canonical topic files across all domains)

FILE 2: /docs/glossary.md

# System Design Glossary

Alphabetical list of all key terms with concise definitions (1-2 sentences each).

Format:
## A
- **ACID**: Atomicity, Consistency, Isolation, Durability — the four properties that guarantee database transactions are processed reliably.
- **API Gateway**: A centralized entry point for microservices that handles routing, authentication, and rate limiting.
(etc. through Z)

Include 100+ terms covering all major system design vocabulary.

Write both files.
```

- [ ] **Step 2: Wait for all 3 agents to complete**

Verify each output file exists and is substantive.

- [ ] **Step 3: Review concept-index.md for completeness**

Check that:
- All 57 canonical files are listed
- Content boundaries are documented
- No concept appears in multiple canonical files
- Aliases cover common alternative names

- [ ] **Step 4: Commit Phase 1 output**

```bash
git add docs/meta/ docs/glossary.md
git commit -m "docs: add source inventory, concept index, source map, and glossary (Phase 1)"
```

---

## Task 5: Phase 2 Batch 1 — Core Topic Files (3 Parallel Agents)

**Files:**
- Agent 1 creates: 10 files in `docs/fundamentals/` + `docs/scalability/`
- Agent 2 creates: 11 files in `docs/storage/` + `docs/caching/`
- Agent 3 creates: 11 files in `docs/messaging/` + `docs/architecture/` + `docs/resilience/`

**Pre-condition:** Phase 1 complete. `docs/meta/concept-index.md` exists with content boundaries.

- [ ] **Step 0: Validate Phase 1 gate**

Verify all Phase 1 outputs exist and concept-index.md is substantive:
```bash
test -s docs/meta/source-inventory.md && echo "✓ source-inventory.md" || echo "✗ MISSING"
test -s docs/meta/concept-index.md && echo "✓ concept-index.md" || echo "✗ MISSING"
test -s docs/meta/source-map.md && echo "✓ source-map.md" || echo "✗ MISSING"
test -s docs/glossary.md && echo "✓ glossary.md" || echo "✗ MISSING"
grep -c "Canonical File" docs/meta/concept-index.md  # Should show content boundary table rows
```

All 4 files must exist and be non-empty. `concept-index.md` must contain the content boundary table. Do NOT proceed if any are missing.

- [ ] **Step 1: Dispatch 3 agents in parallel**

Each agent receives:
1. The 12-section topic template (from the spec)
2. Its specific file assignments
3. Paths to ALL source files (YouTube reports + extracted PDFs)
4. The content boundaries from concept-index.md
5. Cross-linking instructions

**Agent 1 prompt — Fundamentals + Scalability (10 files):**
```
You are a senior systems architect writing canonical documentation for a system design knowledge base.

YOUR ASSIGNED FILES (write ALL of these):
1. docs/fundamentals/system-design-framework.md — requirements, estimation, interview methodology
2. docs/fundamentals/scaling-overview.md — vertical vs horizontal, scaling philosophy
3. docs/fundamentals/availability-reliability.md — nines, fault tolerance, redundancy, blast radius
4. docs/fundamentals/cap-theorem.md — CAP, PACELC, consistency models (strong, eventual, causal)
5. docs/fundamentals/networking-fundamentals.md — DNS, TCP/UDP, OSI model, subnets, NAT, IGW
6. docs/fundamentals/back-of-envelope-estimation.md — QPS, storage, bandwidth math, latency numbers
7. docs/scalability/load-balancing.md — L4/L7, algorithms (round robin, least connections, IP hash), reverse proxy
8. docs/scalability/autoscaling.md — HPA, Kubernetes scaling, traffic patterns (predictable/unpredictable/interconnected)
9. docs/scalability/consistent-hashing.md — hash rings, virtual nodes, data redistribution
10. docs/scalability/sharding.md — strategies (range, hash, directory), shard keys, cross-shard transactions, celebrity problem

SOURCE MATERIALS (read all of these for content):
- YouTube reports: source/youtube-video-reports/1.md through 9.md
- Extracted PDFs: source/extracted/**/*.md
- Concept index (for boundaries): docs/meta/concept-index.md

TEMPLATE — Every file MUST follow this exact structure:
# <Topic Name>

## 1. Overview
Clear, authoritative explanation. NOT a textbook definition — write as a senior architect explaining to a competent engineer.

## 2. Why It Matters
Why this exists in system design. Connect to real business impact.

## 3. Core Concepts
Key components and terminology. Use bullet lists with bold terms.

## 4. How It Works
Detailed technical explanation. Include algorithms, formulas, protocols where relevant.

## 5. Architecture / Flow
MUST include at least one Mermaid diagram. Use sequenceDiagram, flowchart, or graph as appropriate.

## 6. Types / Variants
Different approaches with comparison tables where applicable.

## 7. Use Cases
Real-world scenarios — specific companies and systems, not generic examples.

## 8. Tradeoffs
Structured as a table or pros/cons list. Include quantitative data where available.

## 9. Common Pitfalls
Mistakes engineers make. Write as warnings with explanations.

## 10. Real-World Examples
Specific implementations at named companies (Netflix, Twitter, Uber, etc.).

## 11. Related Concepts
Cross-links using relative paths: [Load Balancing](../scalability/load-balancing.md)

## 12. Source Traceability
- source/youtube-video-reports/X.md
- source/extracted/book/chapter.md

CONTENT BOUNDARIES (do NOT explain these in detail — cross-link instead):
- Rate limiting details → ../resilience/rate-limiting.md
- Caching details → ../caching/caching.md
- Specific databases → ../storage/ files
- Fan-out pattern → ../patterns/fan-out.md
- WAL and CDC → ../storage/database-replication.md
- Service discovery (ZooKeeper/etcd) → ../architecture/microservices.md
- Batch/stream processing (Lambda/Kappa) → ../messaging/event-driven-architecture.md
- Geospatial indexing (geohashing, quadtrees) → ../patterns/geospatial-indexing.md
- Inverted index / Elasticsearch → ../patterns/search-and-indexing.md
- Event sourcing → ../messaging/event-sourcing.md
- CQRS → ../messaging/cqrs.md
- Saga pattern / 2PC → ../resilience/distributed-transactions.md
- Redis internals → ../caching/redis.md

QUALITY BAR:
- Each file should be 300-800 lines
- Combine explanations from multiple sources into ONE superior explanation
- Include practical engineering insights, not just theory
- Mermaid diagrams are MANDATORY in section 5
- Cross-link to at least 3-5 related files per topic

Write all 10 files now.
```

**Agent 2 prompt — Storage + Caching (11 files):**
```
You are a senior systems architect writing canonical documentation for a system design knowledge base.

YOUR ASSIGNED FILES (write ALL of these):
1. docs/storage/sql-databases.md — relational model, ACID, Postgres internals, write-ahead log basics
2. docs/storage/nosql-databases.md — document (MongoDB), KV (Redis/DynamoDB), wide-column (Cassandra), graph (Neo4j) — when to use each
3. docs/storage/object-storage.md — S3, blob architecture, flat namespaces, pre-signed URLs, multipart uploads, durability
4. docs/storage/database-indexing.md — B-trees, LSM trees, hash indexes, composite indexes, write penalty
5. docs/storage/database-replication.md — leader/follower, multi-leader, leaderless, quorum, WAL, CDC, gossip protocol
6. docs/storage/time-series-databases.md — LSM trees, delta encoding, Gorilla compression, downsampling
7. docs/storage/cassandra.md — peer-to-peer architecture, tunable consistency, write path (commitlog/memtable/sstable), compaction, bloom filters
8. docs/storage/dynamodb.md — partition/sort keys, GSI/LSI, DAX, DynamoDB Streams, ACID transactions
9. docs/caching/caching.md — strategies (cache-aside, read-through, write-through, write-back), layers (external, in-process, CDN, client), pitfalls (stampede, stale data, hot keys). NOT Redis-specific.
10. docs/caching/redis.md — Redis-specific: single-threaded model, data structures (strings, sorted sets, streams), rate limiters, leaderboards, pub/sub, geospatial, hot key solutions, persistence modes
11. docs/caching/cdn.md — edge caching, CDN architecture, invalidation, static asset delivery, pull vs push CDN

SOURCE MATERIALS (read all of these for content):
- YouTube reports: source/youtube-video-reports/1.md through 9.md
- Extracted PDFs: source/extracted/**/*.md
- Concept index (for boundaries): docs/meta/concept-index.md

TEMPLATE — Every file MUST follow this exact structure:
# <Topic Name>

## 1. Overview
Clear, authoritative explanation. NOT a textbook definition — write as a senior architect explaining to a competent engineer.

## 2. Why It Matters
Why this exists in system design. Connect to real business impact.

## 3. Core Concepts
Key components and terminology. Use bullet lists with bold terms.

## 4. How It Works
Detailed technical explanation. Include algorithms, formulas, protocols where relevant.

## 5. Architecture / Flow
MUST include at least one Mermaid diagram. Use sequenceDiagram, flowchart, or graph as appropriate.

## 6. Types / Variants
Different approaches with comparison tables where applicable.

## 7. Use Cases
Real-world scenarios — specific companies and systems, not generic examples.

## 8. Tradeoffs
Structured as a table or pros/cons list. Include quantitative data where available.

## 9. Common Pitfalls
Mistakes engineers make. Write as warnings with explanations.

## 10. Real-World Examples
Specific implementations at named companies (Netflix, Twitter, Uber, etc.).

## 11. Related Concepts
Cross-links using relative paths: [Load Balancing](../scalability/load-balancing.md)

## 12. Source Traceability
- source/youtube-video-reports/X.md
- source/extracted/book/chapter.md

CONTENT BOUNDARIES:
- caching.md owns caching strategies/patterns. redis.md owns Redis-specific internals. No overlap.
- database-replication.md owns WAL and CDC as sections within the file
- Consistent hashing details → ../scalability/consistent-hashing.md (cross-link only)
- Sharding details → ../scalability/sharding.md (cross-link only)
- Search/inverted index → ../patterns/search-and-indexing.md (cross-link only)

QUALITY BAR:
- Each file 300-800 lines
- Combine multiple source explanations into ONE superior explanation
- Mermaid diagrams MANDATORY in section 5
- Cross-link 3-5 related files per topic
- Include Cassandra write path diagram, Redis data structure examples, replication topology diagrams

Write all 11 files now.
```

**Agent 3 prompt — Messaging + Architecture + Resilience (11 files):**
```
You are a senior systems architect writing canonical documentation for a system design knowledge base.

YOUR ASSIGNED FILES (write ALL of these):
1. docs/messaging/message-queues.md — Kafka architecture (partitions, consumer groups, sequential I/O), SQS (visibility timeout, DLQ), backpressure, hot partitions, idempotency
2. docs/messaging/event-driven-architecture.md — pub/sub, choreography vs orchestration, saga pattern overview (detail in distributed-transactions), batch/stream processing (Lambda/Kappa architecture, Flink, Spark) as a section
3. docs/messaging/event-sourcing.md — append-only event logs, hydration/replay, audit trail, time travel, relationship to Kafka/Kinesis
4. docs/messaging/cqrs.md — command/query separation, materialized views, read/write model optimization, when to combine with event sourcing
5. docs/architecture/api-gateway.md — routing, authentication, rate limiting, complexity budget, 3-stage infrastructure maturity
6. docs/architecture/microservices.md — decomposition, monolith-first, tradeoffs, service discovery (ZooKeeper/etcd) as a section, API gateway relationship
7. docs/architecture/serverless.md — Lambda, vendor lock-in ecosystem, FaaS patterns, cold starts, when to use vs containers
8. docs/resilience/rate-limiting.md — algorithms (fixed window, sliding window, token bucket, leaky bucket), implementation with Redis, API gateway placement
9. docs/resilience/circuit-breaker.md — states (closed, open, half-open), exponential backoff, jitter, thundering herd prevention, retry storms
10. docs/resilience/distributed-transactions.md — two-phase commit (2PC), saga pattern (choreography vs orchestration), compensating actions, cross-shard transactions
11. docs/resilience/feature-flags.md — progressive releases, canary deployments, kill switches, audit trails, TTL/caching for flags

SOURCE MATERIALS (read all of these for content):
- YouTube reports: source/youtube-video-reports/1.md through 9.md
- Extracted PDFs: source/extracted/**/*.md
- Concept index (for boundaries): docs/meta/concept-index.md

TEMPLATE — same 12-section template (Overview through Source Traceability, Mermaid diagrams mandatory in section 5).

CONTENT BOUNDARIES:
- distributed-transactions.md owns 2PC and saga pattern canonically
- event-driven-architecture.md includes batch/stream processing as a section
- microservices.md includes service discovery as a section
- Rate limiting implementation → this file owns it; api-gateway.md cross-links
- Fan-out → ../patterns/fan-out.md (cross-link only)
- Caching → ../caching/caching.md (cross-link only)

QUALITY BAR: 300-800 lines per file, Mermaid diagrams mandatory, cross-link 3-5 related files, combine multiple sources.

Write all 11 files now.
```

- [ ] **Step 2: Wait for all 3 agents to complete**

Verify all 32 files exist:
```bash
find docs/fundamentals docs/scalability docs/storage docs/caching docs/messaging docs/architecture docs/resilience -name "*.md" | wc -l
```
Expected: 32

- [ ] **Step 3: Spot-check quality of 3-4 files**

Read one file from each agent's output. Verify:
- All 12 sections present
- Mermaid diagram in section 5
- Cross-links to related files
- Source traceability section
- Content depth (not superficial)

- [ ] **Step 4: Commit Batch 1**

```bash
git add docs/fundamentals/ docs/scalability/ docs/storage/ docs/caching/ docs/messaging/ docs/architecture/ docs/resilience/
git commit -m "docs: add 32 canonical topic files — fundamentals, scalability, storage, caching, messaging, architecture, resilience (Phase 2 Batch 1)"
```

---

## Task 6: Phase 2 Batch 2 — Remaining Topics + Case Studies (3 Parallel Agents)

**Files:**
- Agent 1 creates: 7 files in `docs/security/` + `docs/observability/` + `docs/api-design/` (partial)
- Agent 2 creates: 8 files in `docs/api-design/` (partial) + `docs/patterns/`
- Agent 3 creates: 10 files in `docs/case-studies/`

**Pre-condition:** Batch 1 complete (32 files exist for cross-linking).

- [ ] **Step 1: Dispatch 3 agents in parallel**

**Agent 1 prompt — Security + Observability + API Design partial (7 files):**
```
You are a senior systems architect writing canonical documentation for a system design knowledge base.

YOUR ASSIGNED FILES (write ALL of these):
1. docs/security/authentication-authorization.md — OAuth 2.0, JWT, RBAC, session tokens, AuthN vs AuthZ
2. docs/security/encryption.md — at rest, in transit, TLS 1.3, key management
3. docs/security/api-security.md — input validation, DDoS protection, least privilege, injection prevention
4. docs/observability/monitoring.md — Prometheus, Grafana, four golden signals, P99 latency, SLAs/SLOs/SLIs
5. docs/observability/logging.md — ELK stack, structured logging, distributed tracing, correlation IDs
6. docs/api-design/rest-api.md — resource naming, HTTP methods, idempotency, status codes, pagination, versioning
7. docs/api-design/grpc.md — Protocol Buffers, binary serialization, streaming (unary, server, client, bidirectional), 5-10x performance vs REST

SOURCE MATERIALS: source/youtube-video-reports/1.md through 9.md + source/extracted/**/*.md
CONCEPT INDEX: docs/meta/concept-index.md

TEMPLATE: 12-section format (Overview through Source Traceability). Mermaid diagrams mandatory in section 5.

CONTENT BOUNDARIES:
- Rate limiting details → ../resilience/rate-limiting.md (cross-link only)
- API Gateway → ../architecture/api-gateway.md (cross-link only)
- Networking protocols → ../fundamentals/networking-fundamentals.md (cross-link only, api-design covers application-layer design only)

QUALITY BAR: 300-800 lines per file, Mermaid diagrams, cross-link 3-5 related files, combine multiple sources.

Write all 7 files now.
```

**Agent 2 prompt — API Design partial + Patterns (8 files):**
```
You are a senior systems architect writing canonical documentation for a system design knowledge base.

YOUR ASSIGNED FILES (write ALL of these):
1. docs/api-design/graphql.md — queries, mutations, subscriptions, N+1 problem, data loaders, schema design
2. docs/api-design/real-time-protocols.md — WebSockets, SSE, long polling, WebRTC (mesh/MCU/SFU), protocol selection guide
3. docs/patterns/fan-out.md — fan-out on read vs write, hybrid approach, celebrity problem, write amplification
4. docs/patterns/probabilistic-data-structures.md — Bloom filters, Count-Min Sketch, HyperLogLog — how each works, memory vs accuracy tradeoffs, real-world uses
5. docs/patterns/recommendation-engines.md — 3-stage pipeline (candidate gen, ranking, reranking), vector search, embeddings, HNSW, exploration vs exploitation
6. docs/patterns/video-streaming.md — adaptive bitrate (HLS/DASH), chunking, transcoding, index files (M3U8), progressive download vs RTMP vs ABS
7. docs/patterns/search-and-indexing.md — inverted index, Elasticsearch, full-text search, tokenization, TF-IDF, CDC to search index
8. docs/patterns/geospatial-indexing.md — geohashing, quadtrees, R-trees (PostGIS), proximity queries, Uber/Tinder use cases

SOURCE MATERIALS: source/youtube-video-reports/1.md through 9.md + source/extracted/**/*.md
CONCEPT INDEX: docs/meta/concept-index.md

TEMPLATE: 12-section format. Mermaid diagrams mandatory in section 5.

CONTENT BOUNDARIES:
- fan-out.md is the CANONICAL file for fan-out. Case studies (twitter.md, news-feed.md) must cross-link here, not re-explain.
- search-and-indexing.md is CANONICAL for inverted index/Elasticsearch. Other files cross-link only.
- geospatial-indexing.md is CANONICAL for geohashing/quadtrees/R-trees.
- Redis details → ../caching/redis.md. Kafka details → ../messaging/message-queues.md. Cross-link only.

QUALITY BAR: 300-800 lines per file, Mermaid diagrams, cross-link 3-5 related files.

Write all 8 files now.
```

**Agent 3 prompt — Case Studies (10 files):**
```
You are a senior systems architect writing case study documentation for a system design knowledge base.

YOUR ASSIGNED FILES (write ALL of these):
1. docs/case-studies/twitter.md — hybrid fan-out, timeline service, search, celebrity problem
2. docs/case-studies/ticketmaster.md — two-phase booking, distributed locks (Redis TTL), virtual waiting room, CDN for search
3. docs/case-studies/tinder.md — geospatial matching, atomic swiping (Redis), bloom filters for repeat profiles, 36.5TB cache problem
4. docs/case-studies/upi-payments.md — NPCI closed-loop, PSP model, VPA, push/pull transactions, rollback on ACK failure
5. docs/case-studies/facebook-live-comments.md — SSE over WebSockets, partitioned Redis pub/sub, connection mapping, hash(videoID) % N
6. docs/case-studies/whatsapp.md — WebSocket connections, Redis pub/sub routing, inbox pattern, at-least-once delivery, ACK-based deletion
7. docs/case-studies/dropbox.md — chunking (5MB parts), fingerprinting, pre-signed URLs, delta sync, adaptive polling, reconciliation
8. docs/case-studies/web-crawler.md — URL frontier, politeness (robots.txt), SQS with exponential backoff, DLQ, bandwidth math, Bloom filters for dedup
9. docs/case-studies/ad-click-aggregator.md — Kappa/Lambda architecture, Flink 1-minute windows, Spark reconciliation, logarithmic counting for index updates
10. docs/case-studies/news-feed.md — hybrid fan-out (pre-computed flag), ranking, Count-Min Sketch for hot terms, celebrity vs normal user paths

SOURCE MATERIALS: source/youtube-video-reports/1.md through 9.md + source/extracted/**/*.md
CONCEPT INDEX: docs/meta/concept-index.md

CASE STUDY TEMPLATE — DIFFERENT from standard topics:
# <System Name>

## 1. Overview
What the system does and why it's architecturally interesting.

## 2. Requirements
### Functional Requirements
### Non-Functional Requirements
(Scale numbers, latency targets, availability needs)

## 3. High-Level Architecture
Mermaid diagram showing major components and data flow.

## 4. Core Design Decisions
The key architectural choices and WHY they were made. Cross-link to canonical concept files.
Example: "Uses [fan-out on write](../patterns/fan-out.md) for normal users..."

## 5. Deep Dives
### 5.1 [Specific Challenge]
Detailed explanation of how a specific problem is solved.
### 5.2 [Another Challenge]
(Continue for 2-4 deep dives per case study)

## 6. Data Model
Key tables/collections/stores and their schemas.

## 7. Scaling Considerations
How the system handles growth, traffic spikes, hot spots.

## 8. Failure Modes & Mitigations
What can go wrong and how the architecture handles it.

## 9. Key Takeaways
Bullet list of the most important lessons from this design.

## 10. Related Concepts
Cross-links to canonical concept files. EVERY architectural concept used must link to its canonical file.

## 11. Source Traceability

CRITICAL RULE: Case studies must NOT re-explain concepts that have canonical files. Instead:
- WRONG: "Fan-out on write means pushing to all followers' caches..."
- RIGHT: "Uses [fan-out on write](../patterns/fan-out.md) to pre-compute timelines for normal users"

Cross-link to the canonical file and focus on HOW the concept is applied in this specific system.

QUALITY BAR: 400-1000 lines per case study, at least 2 Mermaid diagrams (HLD + one deep dive), 5+ cross-links to canonical files.

Write all 10 files now.
```

- [ ] **Step 2: Wait for all 3 agents to complete**

Verify all 25 files exist:
```bash
find docs/security docs/observability docs/api-design docs/patterns docs/case-studies -name "*.md" | wc -l
```
Expected: 25

- [ ] **Step 3: Spot-check case study cross-linking**

Read `docs/case-studies/twitter.md`. Verify it cross-links to `../patterns/fan-out.md` rather than re-explaining fan-out. Check 1-2 other case studies for the same pattern.

- [ ] **Step 4: Commit Batch 2**

```bash
git add docs/security/ docs/observability/ docs/api-design/ docs/patterns/ docs/case-studies/
git commit -m "docs: add 25 canonical topic files — security, observability, api-design, patterns, case studies (Phase 2 Batch 2)"
```

---

## Task 7: Phase 3 — Build Index and Navigation

**Files:**
- Create: `docs/index.md`

- [ ] **Step 1: Write docs/index.md**

Create the main index with learning path, categories, and study order. This file links to all 57 topic files.

Structure:
```markdown
# System Design Knowledge Base

## Learning Path

### Stage 1: Foundations
(Links to fundamentals/ files in recommended order)

### Stage 2: Core Building Blocks
(Links to scalability/, storage/, caching/ files)

### Stage 3: Communication & Architecture
(Links to messaging/, architecture/, api-design/ files)

### Stage 4: Reliability & Operations
(Links to resilience/, security/, observability/ files)

### Stage 5: Advanced Patterns
(Links to patterns/ files)

### Stage 6: Case Studies
(Links to case-studies/ files, grouped by complexity)

## Quick Reference
- [Glossary](glossary.md)
- [Concept Index](meta/concept-index.md)
- [Source Inventory](meta/source-inventory.md)
- [Source Traceability Map](meta/source-map.md)

## All Topics by Category
(Complete categorized list with links to every file)
```

- [ ] **Step 2: Commit index**

```bash
git add docs/index.md
git commit -m "docs: add index.md with learning path and navigation"
```

---

## Task 8: Phase 3 — Verification and Quality Check

**Files:**
- Create: `scripts/verify_docs.py`

- [ ] **Step 1: Write the verification script**

Create `scripts/verify_docs.py`:

```python
#!/usr/bin/env python3
"""
Verification script for the System Design Knowledge Base.

Checks:
1. Cross-link integrity (all relative links resolve)
2. Template compliance (all 12 sections present)
3. Mermaid diagram presence
4. Deduplication audit (key terms appearing in wrong files)
5. File count validation
"""

import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"

REQUIRED_SECTIONS = [
    "## 1. Overview",
    "## 2. Why It Matters",
    "## 3. Core Concepts",
    "## 4. How It Works",
    "## 5. Architecture / Flow",
    "## 6. Types / Variants",
    "## 7. Use Cases",
    "## 8. Tradeoffs",
    "## 9. Common Pitfalls",
    "## 10. Real-World Examples",
    "## 11. Related Concepts",
    "## 12. Source Traceability",
]

# Case studies use a different template
CASE_STUDY_SECTIONS = [
    "## 1. Overview",
    "## 2. Requirements",
    "## 3. High-Level Architecture",
    "## 4. Core Design Decisions",
    "## 5. Deep Dives",
]

# Concepts and their canonical owners (for dedup audit)
CONCEPT_OWNERS = {
    "fan-out on write": "patterns/fan-out.md",
    "fan-out on read": "patterns/fan-out.md",
    "two-phase commit": "resilience/distributed-transactions.md",
    "saga pattern": "resilience/distributed-transactions.md",
    "bloom filter": "patterns/probabilistic-data-structures.md",
    "count-min sketch": "patterns/probabilistic-data-structures.md",
    "hyperloglog": "patterns/probabilistic-data-structures.md",
    "inverted index": "patterns/search-and-indexing.md",
    "geohash": "patterns/geospatial-indexing.md",
    "quadtree": "patterns/geospatial-indexing.md",
    "cache-aside": "caching/caching.md",
    "write-through": "caching/caching.md",
    "write-back": "caching/caching.md",
}

SKIP_DIRS = {"meta", "superpowers"}


def check_cross_links():
    """Verify all relative markdown links resolve to existing files."""
    issues = []
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md[^)]*)\)')

    for md_file in DOCS_DIR.rglob("*.md"):
        if any(skip in md_file.parts for skip in SKIP_DIRS):
            continue
        content = md_file.read_text(encoding="utf-8")
        for match in link_pattern.finditer(content):
            link_text, link_path = match.groups()
            # Strip anchors
            link_path = link_path.split("#")[0]
            if link_path.startswith("http"):
                continue
            resolved = (md_file.parent / link_path).resolve()
            if not resolved.exists():
                issues.append(f"  BROKEN: {md_file.relative_to(DOCS_DIR)} -> {link_path}")

    return issues


def check_template_compliance():
    """Verify all topic files follow the 12-section template."""
    issues = []

    for md_file in DOCS_DIR.rglob("*.md"):
        if any(skip in md_file.parts for skip in SKIP_DIRS):
            continue
        rel = md_file.relative_to(DOCS_DIR)

        # Skip meta files, index, glossary
        if rel.name in ("index.md", "glossary.md") or "meta" in md_file.parts:
            continue

        content = md_file.read_text(encoding="utf-8")

        # Use appropriate template
        if "case-studies" in md_file.parts:
            sections = CASE_STUDY_SECTIONS
        else:
            sections = REQUIRED_SECTIONS

        missing = [s for s in sections if s not in content]
        if missing:
            issues.append(f"  {rel}: missing {', '.join(missing)}")

    return issues


def check_mermaid_diagrams():
    """Verify Mermaid diagrams are present in topic files."""
    issues = []

    for md_file in DOCS_DIR.rglob("*.md"):
        if any(skip in md_file.parts for skip in SKIP_DIRS):
            continue
        rel = md_file.relative_to(DOCS_DIR)

        if rel.name in ("index.md", "glossary.md") or "meta" in md_file.parts:
            continue

        content = md_file.read_text(encoding="utf-8")
        if "```mermaid" not in content:
            issues.append(f"  {rel}: no Mermaid diagram found")

    return issues


def check_mermaid_syntax():
    """Validate Mermaid diagram blocks have valid syntax structure."""
    issues = []
    mermaid_pattern = re.compile(r'```mermaid\s*\n(.*?)```', re.DOTALL)
    valid_types = {"graph", "flowchart", "sequenceDiagram", "classDiagram",
                   "stateDiagram", "erDiagram", "gantt", "pie", "gitgraph",
                   "journey", "mindmap", "timeline", "sankey", "block"}

    for md_file in DOCS_DIR.rglob("*.md"):
        if any(skip in md_file.parts for skip in SKIP_DIRS):
            continue
        rel = md_file.relative_to(DOCS_DIR)
        content = md_file.read_text(encoding="utf-8")

        for match in mermaid_pattern.finditer(content):
            block = match.group(1).strip()
            if not block:
                issues.append(f"  {rel}: empty Mermaid block")
                continue
            first_line = block.split('\n')[0].strip()
            diagram_type = first_line.split()[0] if first_line else ""
            if diagram_type not in valid_types:
                issues.append(f"  {rel}: invalid Mermaid type '{diagram_type}'")
            elif '\n' not in block.strip():
                issues.append(f"  {rel}: Mermaid block has no diagram content (single line)")

    return issues


def check_deduplication():
    """Audit for concept explanations appearing outside their canonical file."""
    issues = []

    for md_file in DOCS_DIR.rglob("*.md"):
        if any(skip in md_file.parts for skip in SKIP_DIRS):
            continue
        rel = str(md_file.relative_to(DOCS_DIR))
        content = md_file.read_text(encoding="utf-8").lower()

        for concept, owner in CONCEPT_OWNERS.items():
            if owner in rel:
                continue  # This IS the canonical file
            if "case-studies/" in rel:
                # Case studies may mention concepts briefly
                count = content.count(concept)
                if count > 5:
                    issues.append(f"  {rel}: '{concept}' mentioned {count}x (owner: {owner})")
            else:
                count = content.count(concept)
                if count > 3:
                    issues.append(f"  {rel}: '{concept}' mentioned {count}x (owner: {owner})")

    return issues


def check_file_count():
    """Verify expected number of topic files exist."""
    expected = 57
    topic_files = []
    for md_file in DOCS_DIR.rglob("*.md"):
        if any(skip in md_file.parts for skip in SKIP_DIRS):
            continue
        rel = md_file.relative_to(DOCS_DIR)
        if rel.name not in ("index.md", "glossary.md") and "meta/" not in str(rel):
            topic_files.append(rel)

    return expected, len(topic_files), topic_files


def main():
    print("=" * 60)
    print("KNOWLEDGE BASE VERIFICATION")
    print("=" * 60)

    all_passed = True

    # 1. File count
    print("\n1. File Count Check")
    expected, actual, files = check_file_count()
    if actual >= expected:
        print(f"  ✓ {actual}/{expected} topic files found")
    else:
        print(f"  ✗ {actual}/{expected} topic files found")
        all_passed = False

    # 2. Cross-links
    print("\n2. Cross-Link Integrity")
    link_issues = check_cross_links()
    if not link_issues:
        print("  ✓ All cross-links resolve")
    else:
        print(f"  ✗ {len(link_issues)} broken links:")
        for issue in link_issues:
            print(issue)
        all_passed = False

    # 3. Template compliance
    print("\n3. Template Compliance")
    template_issues = check_template_compliance()
    if not template_issues:
        print("  ✓ All files follow template")
    else:
        print(f"  ✗ {len(template_issues)} template issues:")
        for issue in template_issues:
            print(issue)
        all_passed = False

    # 4. Mermaid diagrams
    print("\n4. Mermaid Diagram Presence")
    mermaid_issues = check_mermaid_diagrams()
    if not mermaid_issues:
        print("  ✓ All topic files have Mermaid diagrams")
    else:
        print(f"  ⚠ {len(mermaid_issues)} files missing diagrams:")
        for issue in mermaid_issues:
            print(issue)

    # 4b. Mermaid syntax
    print("\n4b. Mermaid Syntax Validation")
    syntax_issues = check_mermaid_syntax()
    if not syntax_issues:
        print("  ✓ All Mermaid blocks have valid syntax structure")
    else:
        print(f"  ⚠ {len(syntax_issues)} syntax issues:")
        for issue in syntax_issues:
            print(issue)

    # 5. Deduplication audit
    print("\n5. Deduplication Audit")
    dedup_issues = check_deduplication()
    if not dedup_issues:
        print("  ✓ No significant concept duplication detected")
    else:
        print(f"  ⚠ {len(dedup_issues)} potential duplications:")
        for issue in dedup_issues:
            print(issue)

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL CHECKS PASSED")
    else:
        print("❌ ISSUES FOUND — review above")
    print("=" * 60)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run verification**

```bash
python3 scripts/verify_docs.py
```

Review output. Fix any critical issues (broken links, missing sections).

- [ ] **Step 3: Fix broken cross-links**

For any broken links reported, update the source files to correct relative paths.

- [ ] **Step 4: Fix template compliance issues**

For any files missing required sections, add the missing sections with appropriate content.

- [ ] **Step 5: Commit verification script and fixes**

```bash
git add scripts/verify_docs.py
git commit -m "feat: add verification script for cross-links, templates, dedup audit"
```

If files were fixed:
```bash
git add docs/
git commit -m "fix: resolve broken cross-links and template compliance issues"
```

---

## Task 9: Final Quality Review and Cleanup

- [ ] **Step 1: Run full verification one more time**

```bash
python3 scripts/verify_docs.py
```

All checks should pass.

- [ ] **Step 2: Verify acceptance criteria**

Manually check against the spec's acceptance criteria:
- [ ] No duplicate concepts across files
- [ ] All 57 canonical files exist
- [ ] Every topic follows template
- [ ] Mermaid diagrams present and valid
- [ ] index.md exists with learning path
- [ ] All 3 meta files exist
- [ ] glossary.md exists
- [ ] Cross-links resolve
- [ ] No raw source summaries
- [ ] Content is deep, not superficial
- [ ] Each topic combines multiple sources
- [ ] Navigable on GitHub

- [ ] **Step 3: Final commit**

```bash
git add docs/ scripts/
git commit -m "complete: system design knowledge base — 57 topics, 10 case studies, full cross-linking"
```

- [ ] **Step 4: Generate completion summary**

Document:
1. What was generated (file counts, total lines)
2. Gaps found in source materials
3. Assumptions made
4. Suggested future improvements
