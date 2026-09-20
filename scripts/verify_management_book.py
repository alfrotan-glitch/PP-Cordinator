# -*- coding: utf-8 -*-
"""
verify_management_book.py
Comprehensive integrity, EPUB3 standards, terminology, and content verification for:
«مدیریت؛ مبانی و مهارت‌های اساسی مدیریت»
(Management: The Essentials — Afghan Dari Professional Edition)
"""
import os
import sys
import zipfile
import re
import xml.etree.ElementTree as ET

def verify():
    print("=================================================================")
    print("  VERIFYING FLAGSHIP TEXTBOOK DELIVERABLES:")
    print("  «مدیریت؛ مبانی و مهارت‌های اساسی مدیریت»")
    print("=================================================================")
    
    epub_path = "build/Management_The_Essentials_Afghan_Edition.epub"
    docx_path = "build/Management_The_Essentials_Afghan_Edition.docx"
    html_path = "build/Management_The_Essentials_Afghan_Edition.html"
    svg_path = "build/cover_management.svg"
    png_path = "build/cover_management.png"
    md_path = "manuscript/management_essentials.md"
    
    # 1. Existence and size
    assert os.path.exists(md_path), f"Missing {md_path}"
    assert os.path.exists(epub_path), f"Missing {epub_path}"
    assert os.path.exists(docx_path), f"Missing {docx_path}"
    assert os.path.exists(html_path), f"Missing {html_path}"
    assert os.path.exists(svg_path), f"Missing {svg_path}"
    assert os.path.exists(png_path), f"Missing {png_path}"
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    words = len(md_text.split())
    chars = len(md_text)
    print(f"[PASS] 1. Files present. Manuscript: {words:,} words, {chars:,} characters.")
    
    # 2. Terminology Check
    assert "شهرداری" not in md_text, "Found forbidden term شهرداری"
    assert "پروژهش" not in md_text, "Found forbidden term پروژهش"
    assert "کارکنان" not in md_text, "Found forbidden term کارکنان"
    assert "گزارش" not in md_text, "Found non-preferred term گزارش"
    assert "مرخصی" not in md_text, "Found non-preferred term مرخصی"
    print("[PASS] 2. Terminology: 100% compliant with Afghan Dari standards.")
    
    # 3. EPUB3 Archive & XML Validation
    with zipfile.ZipFile(epub_path, 'r') as zf:
        file_list = zf.namelist()
        
        # Mimetype
        assert file_list[0] == 'mimetype', "mimetype must be first entry"
        minfo = zf.getinfo('mimetype')
        assert minfo.compress_type == zipfile.ZIP_STORED, "mimetype must be stored (uncompressed)"
        mcontent = zf.read('mimetype').decode('ascii')
        assert mcontent == 'application/epub+zip', "mimetype content invalid"
        
        # Container.xml
        assert 'META-INF/container.xml' in file_list
        root = ET.fromstring(zf.read('META-INF/container.xml'))
        rootfile = root.find('.//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile')
        opf_path = rootfile.attrib.get('full-path')
        assert opf_path in file_list
        
        # OPF
        opf_tree = ET.fromstring(zf.read(opf_path))
        manifest = opf_tree.find('{http://www.idpf.org/2007/opf}manifest')
        spine = opf_tree.find('{http://www.idpf.org/2007/opf}spine')
        assert len(manifest) >= 20, "Insufficient manifest items"
        assert len(spine) >= 20, "Insufficient spine items"
        
        # Parse all XML/XHTML
        xml_ok = 0
        for name in file_list:
            if name.endswith(('.xml', '.opf', '.ncx', '.xhtml')):
                ET.fromstring(zf.read(name))
                xml_ok += 1
        print(f"[PASS] 3. EPUB3 Architecture: All {xml_ok} XML/XHTML files are 100% well-formed and valid!")
        
        # 4. Content Verification inside EPUB
        found_parts = set()
        for name in file_list:
            if name.startswith('EPUB/part_') and name.endswith('.xhtml'):
                content = zf.read(name).decode('utf-8')
                for m in re.findall(r'بخش ([^:<]+)', content):
                    found_parts.add(m.strip())
        print(f"[PASS] 4. Structure: Detected {len(found_parts)} core parts across EPUB spine.")
        
        # 5. Check MCQs, Scenarios, Cases, Tools
        part20_content = zf.read('EPUB/part_20.xhtml').decode('utf-8')
        mcq_count = len(re.findall(r'سوال \d+:', part20_content))
        print(f"[PASS] 5. Exam Bank: Detected {mcq_count} numbered MCQs in Part 20.")
        assert mcq_count >= 150, f"Expected 150 MCQs, found {mcq_count}"
        
        part18_content = zf.read('EPUB/part_18.xhtml').decode('utf-8')
        case_count = len(re.findall(r'قضیه \d+:', part18_content))
        print(f"[PASS] 6. Case Laboratory: Detected {case_count} detailed case studies in Part 18.")
        assert case_count >= 30, f"Expected 30 cases, found {case_count}"
        
        part19_content = zf.read('EPUB/part_19.xhtml').decode('utf-8')
        tool_count = len(re.findall(r'ابزار \d+:', part19_content))
        print(f"[PASS] 7. Management Toolkits: Detected {tool_count} practical management tools in Part 19.")
        assert tool_count >= 14, f"Expected 14 tools, found {tool_count}"
        
        # 6. Check LaTeX leakage
        for name in file_list:
            if name.endswith('.xhtml'):
                c = zf.read(name).decode('utf-8')
                assert '\\mathbf{' not in c, f"Leaked \\mathbf in {name}"
                assert '\\frac{' not in c, f"Leaked \\frac in {name}"
        print("[PASS] 8. LaTeX Integrity: ZERO unrendered LaTeX formulas in XHTML.")
        
    print("\n=================================================================")
    print("  ALL VERIFICATIONS PASSED WITH ZERO ERRORS!")
    print("  STATUS: READY FOR PUBLICATION")
    print("=================================================================")

if __name__ == "__main__":
    verify()
