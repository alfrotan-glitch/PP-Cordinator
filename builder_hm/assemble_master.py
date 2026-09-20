# -*- coding: utf-8 -*-
"""
Master Assembler for Book 2:
Health Management — 24-Hour Exam & Field Practice Master Guide
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_meta import get_meta_text
from build_part1_2 import get_part1_2_text
from build_part3_4 import get_part3_4_text
from build_part5_6 import get_part5_6_text
from build_part7_8 import get_part7_8_text
from build_part9_10 import get_part9_10_text
from build_part11_12 import get_part11_12_text
from build_part13_14 import get_part13_14_text
from build_part15_cases import get_part15_cases_text
from build_part16_mcqs import get_mcqs_text
from build_part16_domain import get_domain_text
from build_part16_mocks import get_mocks_text
from build_part16_interviews import get_interviews_text
from build_part17_tools import get_part17_tools_text

def assemble_manuscript():
    sections = [
        get_meta_text(),
        get_part1_2_text(),
        get_part3_4_text(),
        get_part5_6_text(),
        get_part7_8_text(),
        get_part9_10_text(),
        get_part11_12_text(),
        get_part13_14_text(),
        get_part15_cases_text(),
        get_mcqs_text(),
        get_domain_text(),
        get_mocks_text(),
        get_interviews_text(),
        get_part17_tools_text()
    ]
    
    full_manuscript = "\n\n".join(sections)
    
    out_path = "manuscript/health_management_master.md"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_manuscript)
    
    lines = full_manuscript.splitlines()
    words = full_manuscript.split()
    chars = len(full_manuscript)
    
    print(f"=== MANUSCRIPT ASSEMBLED SUCCESSFULLY ===")
    print(f"File path: {out_path}")
    print(f"Total Lines: {len(lines):,}")
    print(f"Total Words: {len(words):,}")
    print(f"Total Characters: {chars:,}")
    return out_path

if __name__ == "__main__":
    assemble_manuscript()
