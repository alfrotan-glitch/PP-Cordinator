#!/usr/bin/env bash
# Full pipeline: intake -> normalize -> curated edits -> assemble -> build -> QA -> logs
set -euo pipefail
cd "$(dirname "$0")/../.."          # repository root

SRC="کتاب_Provincial_Coordinator_نسخه_ویرایش‌شده.docx"

echo "== 0-1 intake:      extract original DOCX"
python3 project/scripts/extract_docx.py "$SRC" project/manuscript/parts/00_extracted.md

echo "== 3-5 normalize:   language + Afghan terminology rules"
python3 project/scripts/normalize.py

echo "== 2-4 curated:     scientific/clinical corrections + additions"
python3 project/scripts/patch_curated.py

echo "== 5 assemble:      single-source master.md"
python3 project/scripts/assemble.py

echo "== 5 cover:         typographic cover"
python3 project/scripts/make_cover.py

echo "== 6 DOCX";  python3 project/scripts/build_docx.py
echo "== 6 PDF";   python3 project/scripts/build_pdf.py
echo "== 5 fonts"; python3 project/scripts/make_webfonts.py
echo "== 6 EPUB";  python3 project/scripts/build_epub.py

echo "== 7 QA";    python3 project/scripts/qa.py
echo "== 7 review"; python3 project/scripts/preview_epub.py
echo "== 8 logs";  python3 project/scripts/make_logs.py

echo "Done. Outputs in output/ ; reports in project/logs/"
