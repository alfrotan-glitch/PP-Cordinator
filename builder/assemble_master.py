# -*- coding: utf-8 -*-
"""
Assembles all parts into manuscript/master.md
"""
import os
from build_meta import get_front_matter
from build_part1 import get_part1_text
from build_part2_3 import get_part2_3_text
from build_part4_5 import get_part4_5_text
from build_part6_7 import get_part6_7_text
from build_part8_9 import get_part8_9_text
from build_part10_11 import get_part10_11_text
from build_part12 import get_part12_text
from build_part13_core import get_part13_core_text
from build_part13_exams import get_part13_exams_text
from build_part14_15 import get_part14_15_text
from build_part16_17 import get_part16_17_text
from build_part18_19 import get_part18_19_text
from build_appendices import get_appendices_text

def assemble():
    os.makedirs("manuscript", exist_ok=True)
    parts = [
        get_front_matter(),
        get_part1_text(),
        get_part2_3_text(),
        get_part4_5_text(),
        get_part6_7_text(),
        get_part8_9_text(),
        get_part10_11_text(),
        get_part12_text(),
        get_part13_core_text(),
        get_part13_exams_text(),
        get_part14_15_text(),
        get_part16_17_text(),
        get_part18_19_text(),
        get_appendices_text()
    ]
    
    full_text = "\n\n".join(parts)
    output_path = "manuscript/master.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"Master manuscript generated at {output_path}")
    print(f"Total characters: {len(full_text):,}")
    print(f"Total words (est): {len(full_text.split()):,}")
    print(f"Total lines: {len(full_text.splitlines()):,}")

if __name__ == "__main__":
    assemble()
