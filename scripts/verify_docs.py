#!/usr/bin/env python3
"""
Verification script for the System Design Knowledge Base.

Checks:
1. Cross-link integrity (all relative links resolve)
2. Template compliance (all 12 sections present)
3. Mermaid diagram presence and syntax
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

CASE_STUDY_SECTIONS = [
    "## 1. Overview",
    "## 2. Requirements",
    "## 3. High-Level Architecture",
    "## 4. Core Design Decisions",
    "## 5. Deep Dives",
]

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

VALID_MERMAID_TYPES = {
    "graph", "flowchart", "sequenceDiagram", "classDiagram",
    "stateDiagram", "stateDiagram-v2", "erDiagram", "gantt",
    "pie", "gitgraph", "journey", "mindmap", "timeline",
    "sankey", "block",
}


def check_cross_links():
    issues = []
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md[^)]*)\)')

    for md_file in DOCS_DIR.rglob("*.md"):
        if any(skip in md_file.parts for skip in SKIP_DIRS):
            continue
        content = md_file.read_text(encoding="utf-8")
        for match in link_pattern.finditer(content):
            link_text, link_path = match.groups()
            link_path = link_path.split("#")[0]
            if link_path.startswith("http"):
                continue
            resolved = (md_file.parent / link_path).resolve()
            if not resolved.exists():
                issues.append(f"  BROKEN: {md_file.relative_to(DOCS_DIR)} -> {link_path}")

    return issues


def check_template_compliance():
    issues = []

    for md_file in DOCS_DIR.rglob("*.md"):
        if any(skip in md_file.parts for skip in SKIP_DIRS):
            continue
        rel = md_file.relative_to(DOCS_DIR)

        if rel.name in ("index.md", "glossary.md") or "meta" in md_file.parts:
            continue

        content = md_file.read_text(encoding="utf-8")

        if "case-studies" in md_file.parts:
            sections = CASE_STUDY_SECTIONS
        else:
            sections = REQUIRED_SECTIONS

        missing = [s for s in sections if s not in content]
        if missing:
            issues.append(f"  {rel}: missing {', '.join(missing)}")

    return issues


def check_mermaid_diagrams():
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
    issues = []
    mermaid_pattern = re.compile(r'```mermaid\s*\n(.*?)```', re.DOTALL)

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
            if diagram_type not in VALID_MERMAID_TYPES:
                issues.append(f"  {rel}: invalid Mermaid type '{diagram_type}'")
            elif '\n' not in block.strip():
                issues.append(f"  {rel}: Mermaid block has no content (single line)")

    return issues


def check_deduplication():
    issues = []

    for md_file in DOCS_DIR.rglob("*.md"):
        if any(skip in md_file.parts for skip in SKIP_DIRS):
            continue
        rel = str(md_file.relative_to(DOCS_DIR))
        content = md_file.read_text(encoding="utf-8").lower()

        for concept, owner in CONCEPT_OWNERS.items():
            if owner in rel:
                continue
            if "case-studies/" in rel:
                count = content.count(concept)
                if count > 5:
                    issues.append(f"  {rel}: '{concept}' mentioned {count}x (owner: {owner})")
            else:
                count = content.count(concept)
                if count > 3:
                    issues.append(f"  {rel}: '{concept}' mentioned {count}x (owner: {owner})")

    return issues


def check_file_count():
    expected = 57
    topic_files = []
    for md_file in DOCS_DIR.rglob("*.md"):
        if any(skip in md_file.parts for skip in SKIP_DIRS):
            continue
        rel = md_file.relative_to(DOCS_DIR)
        if rel.name not in ("index.md", "glossary.md") and "meta" not in md_file.parts:
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
        print(f"  PASS: {actual}/{expected} topic files found")
    else:
        print(f"  FAIL: {actual}/{expected} topic files found")
        all_passed = False

    # 2. Cross-links
    print("\n2. Cross-Link Integrity")
    link_issues = check_cross_links()
    if not link_issues:
        print("  PASS: All cross-links resolve")
    else:
        print(f"  WARN: {len(link_issues)} broken links:")
        for issue in link_issues[:20]:
            print(issue)
        if len(link_issues) > 20:
            print(f"  ... and {len(link_issues) - 20} more")

    # 3. Template compliance
    print("\n3. Template Compliance")
    template_issues = check_template_compliance()
    if not template_issues:
        print("  PASS: All files follow template")
    else:
        print(f"  WARN: {len(template_issues)} template issues:")
        for issue in template_issues:
            print(issue)

    # 4a. Mermaid presence
    print("\n4a. Mermaid Diagram Presence")
    mermaid_issues = check_mermaid_diagrams()
    if not mermaid_issues:
        print("  PASS: All topic files have Mermaid diagrams")
    else:
        print(f"  WARN: {len(mermaid_issues)} files missing diagrams:")
        for issue in mermaid_issues:
            print(issue)

    # 4b. Mermaid syntax
    print("\n4b. Mermaid Syntax Validation")
    syntax_issues = check_mermaid_syntax()
    if not syntax_issues:
        print("  PASS: All Mermaid blocks have valid syntax structure")
    else:
        print(f"  WARN: {len(syntax_issues)} syntax issues:")
        for issue in syntax_issues[:20]:
            print(issue)
        if len(syntax_issues) > 20:
            print(f"  ... and {len(syntax_issues) - 20} more")

    # 5. Deduplication audit
    print("\n5. Deduplication Audit")
    dedup_issues = check_deduplication()
    if not dedup_issues:
        print("  PASS: No significant concept duplication detected")
    else:
        print(f"  WARN: {len(dedup_issues)} potential duplications:")
        for issue in dedup_issues:
            print(issue)

    # Summary
    print("\n" + "=" * 60)
    total_lines = 0
    total_mermaid = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        if any(skip in md_file.parts for skip in SKIP_DIRS):
            continue
        content = md_file.read_text(encoding="utf-8")
        total_lines += content.count('\n')
        total_mermaid += content.count('```mermaid')

    print(f"STATS: {actual} topic files, {total_lines} total lines, {total_mermaid} Mermaid diagrams")

    if all_passed and not link_issues and not template_issues:
        print("ALL CHECKS PASSED")
    else:
        print("ISSUES FOUND — review above")
    print("=" * 60)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
