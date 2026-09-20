# -*- coding: utf-8 -*-
"""
Part 18: Management Case Laboratory (Combines all 30 cases)
"""
from builder_management.build_part18_cases_1_10 import get_cases_1_10
from builder_management.build_part18_cases_11_20 import get_cases_11_20
from builder_management.build_part18_cases_21_30 import get_cases_21_30

def get_part18_text():
    return get_cases_1_10() + "\n" + get_cases_11_20() + "\n" + get_cases_21_30()

if __name__ == "__main__":
    t = get_part18_text()
    print("Part 18 Total Characters:", len(t))
