# -*- coding: utf-8 -*-
"""
rebuild_book1_engine.py
Generates the complete, deeply developed, narrative-rich Book 1:
Provincial Coordinator — Field Management, Operations Leadership & Exam Readiness
Organized into 24 substantial, fully developed chapters across 8 parts.
"""

import os
import sys

def generate_book1_markdown():
    print("Generating comprehensive Book 1 manuscript...")
    
    # We will assemble all 24 chapters with deep content
    # Import the modular chapters we created and combine with the full question bank and cases
    import scripts.book1_modules.part1_3 as p1_3
    import scripts.book1_modules.part4_6 as p4_6
    import scripts.book1_modules.part7_8 as p7_8
    
    text_p1_3 = p1_3.get_content().strip()
    text_p4_6 = p4_6.get_content().strip()
    text_p7_8 = p7_8.get_content().strip()
    
    # Combine into a single unified manuscript
    manuscript = f"{text_p1_3}\n\n{text_p4_6}\n\n{text_p7_8}"
    
    # Write to manuscript/master.md
    with open('manuscript/master.md', 'w', encoding='utf-8') as f:
        f.write(manuscript)
        
    print(f"Book 1 generated successfully: {len(manuscript):,} characters, {len(manuscript.split())} words.")

if __name__ == '__main__':
    sys.path.append(os.path.abspath('.'))
    generate_book1_markdown()
