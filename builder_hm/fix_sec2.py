# -*- coding: utf-8 -*-
with open("builder_hm/build_sec2_cases.py", "r", encoding="utf-8") as f:
    content = f.read()

# remove old if __name__ ...
idx = content.find('if __name__ == "__main__":')
if idx != -1:
    header = content[:idx].strip()
    idx_quotes = header.rfind('"""')
    if idx_quotes != -1:
        header = header[:idx_quotes].strip()
    
    # get part_cases_2 from line containing Q161
    idx_q161 = content.find('### سؤال Q161')
    if idx_q161 != -1:
        body2 = content[idx_q161:].strip()
        full_text = header + "\n\n" + body2 + '\n"""\n    return text\n\nif __name__ == "__main__":\n    t = get_sec2_text()\n    print("Sec 2 full length:", len(t))\n'
        with open("builder_hm/build_sec2_cases.py", "w", encoding="utf-8") as f_out:
            f_out.write(full_text)
        print("Fixed sec2!")
