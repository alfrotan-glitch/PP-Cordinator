# -*- coding: utf-8 -*-
"""
Assembles the complete master manuscript for:
«مدیریت؛ مبانی و مهارت‌های اساسی مدیریت»
(Management: The Essentials - Afghan Dari Professional Edition)
"""
import os
from builder_management.build_meta import get_meta_text
from builder_management.build_part1_2 import get_part1_2_text
from builder_management.build_part3_4 import get_part3_4_text
from builder_management.build_part5_6 import get_part5_6_text
from builder_management.build_part7_8 import get_part7_8_text
from builder_management.build_part9_10 import get_part9_10_text
from builder_management.build_part11_12 import get_part11_12_text
from builder_management.build_part13_14 import get_part13_14_text
from builder_management.build_part15_16 import get_part15_16_text
from builder_management.build_part17 import get_part17_text
from builder_management.build_part18_cases import get_part18_text
from builder_management.build_part19_tools import get_part19_text
from builder_management.build_part20_exams import get_part20_text

def assemble_manuscript(output_path="manuscript/management_essentials.md"):
    parts = [
        get_meta_text(),
        get_part1_2_text(),
        get_part3_4_text(),
        get_part5_6_text(),
        get_part7_8_text(),
        get_part9_10_text(),
        get_part11_12_text(),
        get_part13_14_text(),
        get_part15_16_text(),
        get_part17_text(),
        get_part18_text(),
        get_part19_text(),
        get_part20_text()
    ]
    full_text = "\n\n".join(parts)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"Successfully generated: {output_path}")
    print(f"Total Words: {len(full_text.split()):,}")
    print(f"Total Characters: {len(full_text):,}")

if __name__ == "__main__":
    assemble_manuscript()
