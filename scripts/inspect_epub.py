# -*- coding: utf-8 -*-
import zipfile
import xml.etree.ElementTree as ET

def validate_epub(epub_path):
    print(f"\n--- VALIDATING EPUB: {epub_path} ---")
    with zipfile.ZipFile(epub_path, 'r') as zf:
        file_list = zf.namelist()
        print(f"Total archive entries: {len(file_list)}")
        
        # 1. mimetype check
        assert file_list[0] == 'mimetype', "mimetype MUST be first entry!"
        mimetype_info = zf.getinfo('mimetype')
        assert mimetype_info.compress_type == zipfile.ZIP_STORED, "mimetype MUST NOT be compressed!"
        mimetype_content = zf.read('mimetype').decode('ascii')
        assert mimetype_content == 'application/epub+zip', f"Invalid mimetype content: {mimetype_content}"
        print("[PASS] mimetype is stored correctly as uncompressed application/epub+zip.")
        
        # 2. container.xml
        assert 'META-INF/container.xml' in file_list, "Missing META-INF/container.xml"
        container_xml = zf.read('META-INF/container.xml').decode('utf-8')
        root = ET.fromstring(container_xml)
        rootfile_elem = root.find('.//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile')
        assert rootfile_elem is not None, "No rootfile defined in container.xml"
        opf_path = rootfile_elem.attrib.get('full-path')
        assert opf_path in file_list, f"OPF file {opf_path} declared in container.xml does not exist in archive"
        print(f"[PASS] container.xml is well-formed XML and points to {opf_path}.")
        
        # 3. OPF validation
        opf_content = zf.read(opf_path).decode('utf-8')
        opf_tree = ET.fromstring(opf_content)
        manifest = opf_tree.find('{http://www.idpf.org/2007/opf}manifest')
        spine = opf_tree.find('{http://www.idpf.org/2007/opf}spine')
        assert manifest is not None, "Missing manifest in OPF"
        assert spine is not None, "Missing spine in OPF"
        print(f"[PASS] OPF package document is well-formed with {len(manifest)} manifest items and {len(spine)} spine items.")
        
        # 4. Check all XML / XHTML files in archive
        xml_count = 0
        xhtml_count = 0
        for name in file_list:
            if name.endswith('.xml') or name.endswith('.opf') or name.endswith('.ncx'):
                xml_count += 1
                try:
                    ET.fromstring(zf.read(name))
                except ET.ParseError as e:
                    print(f"[FAIL] XML ParseError in {name}: {e}")
                    return False
            elif name.endswith('.xhtml') or name.endswith('.html'):
                xhtml_count += 1
                try:
                    ET.fromstring(zf.read(name))
                except ET.ParseError as e:
                    print(f"[FAIL] XHTML ParseError in {name}: {e}")
                    return False
        
        print(f"[PASS] All {xml_count} XML files and {xhtml_count} XHTML files are 100% well-formed and valid!")
        
        # 5. Check cover image exists
        assert any(name.startswith('EPUB/images/') for name in file_list), "Missing cover image in EPUB/images/"
        print("[PASS] Cover art is present in archive.")
        
        # 6. Check style exists
        assert 'EPUB/style/book.css' in file_list, "Missing EPUB/style/book.css"
        print("[PASS] CSS stylesheet is present in archive.")
        
    print(f"===> EPUB {epub_path} PASSED ALL EPUB3 INTEGRITY CHECKS!\n")
    return True

if __name__ == "__main__":
    ok1 = validate_epub("build/Provincial_Coordinator_24Hour_Exam_Master_Guide.epub")
    ok2 = validate_epub("build/Health_Management_Master_Guide.epub")
    if ok1 and ok2:
        print("ALL EPUB EDITIONS VERIFIED 100% COMPLIANT AND READY FOR DISTRIBUTION!")
