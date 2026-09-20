# -*- coding: utf-8 -*-
"""
Builder for Part XVI - Sections 2 to 5 (Q151 to Q270)
Imports and combines all 4 sections into a unified Master Exam Domain Bank.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from builder_hm.build_sec2_cases import get_sec2_text
    from builder_hm.build_sec3_short import get_sec3_text
    from builder_hm.build_sec4_data import get_sec4_text
    from builder_hm.build_sec5_lead import get_sec5_text
except ImportError:
    from build_sec2_cases import get_sec2_text
    from build_sec3_short import get_sec3_text
    from build_sec4_data import get_sec4_text
    from build_sec5_lead import get_sec5_text

def get_domain_text():
    parts = [
        get_sec2_text(),
        get_sec3_text(),
        get_sec4_text(),
        get_sec5_text()
    ]
    return "\n\n".join(parts)

if __name__ == "__main__":
    t = get_domain_text()
    print("Part 16 Domain text (Q151 to Q270) total length:", len(t))
