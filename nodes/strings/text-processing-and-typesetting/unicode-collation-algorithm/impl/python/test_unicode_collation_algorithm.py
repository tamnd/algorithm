# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-collation-algorithm/. The authors are listed in prov/7HSE2K.jsonl.
# The NFD step uses unicodedata (unidata_version 16.0.0 with Python 3.14). The tests use
# only characters that are assigned in Unicode 3.2.
import random

from unicode_collation_algorithm import (DUCET_SUBSET, MODES, apply_variable_weighting,
                                         collation_elements, compare, format_key,
                                         implicit_weights, parse_allkeys, sort_key)

# 19 consecutive lines of CollationTest_NON_IGNORABLE_SHORT.txt 16.0.0
# (Date: 2024-08-14, 00:51:39 GMT), the lines that follow "1F170 0021".
COLLATION_TEST_RUN = """\
00E1 0021
00C1 0021
00E0 0021
00C0 0021
0103 0021
0102 0021
1EAF 0021
1EAE 0021
1EB1 0021
1EB0 0021
1EB5 0021
1EB4 0021
1EB3 0021
1EB2 0021
00E2 0021
00C2 0021
1EA5 0021
1EA4 0021
1EA7 0021
"""


def _text(line):
    return "".join(chr(int(h, 16)) for h in line.split())


def test_parse_allkeys_format():
    t = parse_allkeys("0020  ; [*0209.0020.0002] # SPACE\n"
                      "00E6  ; [.2380.0020.0004][.0000.011E.0004][.23E7.0020.0004] # AE\n")
    assert t[(" ",)] == [(True, 0x0209, 0x0020, 0x0002)]
    assert t[("æ",)] == [(False, 0x2380, 0x20, 4), (False, 0, 0x11E, 4), (False, 0x23E7, 0x20, 4)]
    assert DUCET_SUBSET[("a",)] == [(False, 0x2380, 0x0020, 0x0002)]
    assert DUCET_SUBSET[("A",)] == [(False, 0x2380, 0x0020, 0x0008)]


def test_collation_test_run():
    lines = [_text(x) for x in COLLATION_TEST_RUN.splitlines()]
    keys = [sort_key(x, "non-ignorable") for x in lines]
    for k1, k2 in zip(keys, keys[1:]):
        assert k1 < k2


def test_table_2_levels():
    assert compare("role", "roles") < 0 and compare("roles", "rule") < 0  # L1
    assert compare("role", "rôle") < 0 and compare("rôle", "roles") < 0  # L2
    assert compare("role", "Role") < 0 and compare("Role", "rôle") < 0  # L3
    # L4 with U+0022 for the quotation marks: this order holds with shift-trimmed.
    assert compare("role", '"role"', "shift-trimmed") < 0
    assert compare('"role"', "Role", "shift-trimmed") < 0
    # With shifted, the quotation mark weight 033A comes before FFFF at level 4.
    assert compare('"role"', "role", "shifted") < 0
    assert compare('"role"', "Role", "shifted") < 0


def test_python_sorted_is_code_point_order():
    words = ["rôle", "Role", "role"]
    assert sorted(words) == ["Role", "role", "rôle"]
    assert sorted(words, key=sort_key) == ["role", "Role", "rôle"]


TABLE_12 = ["de luge", "de Luge", "de-luge", "de-Luge", "death", "deluge", "deLuge", "demark"]


def test_table_12_variable_weighting():
    shuffled = TABLE_12[::-1]
    assert sorted(shuffled, key=lambda s: sort_key(s, "non-ignorable")) == [
        "de luge", "de Luge", "de-luge", "de-Luge", "death", "deluge", "deLuge", "demark"]
    assert sorted(shuffled, key=lambda s: sort_key(s, "shifted")) == [
        "death", "de luge", "de-luge", "deluge", "de Luge", "de-Luge", "deLuge", "demark"]
    assert sorted(shuffled, key=lambda s: sort_key(s, "shift-trimmed")) == [
        "death", "deluge", "de luge", "de-luge", "deLuge", "de Luge", "de-Luge", "demark"]
    k = {s: sort_key(s, "blanked") for s in TABLE_12}
    assert k["de luge"] == k["de-luge"] == k["deluge"]
    assert k["de Luge"] == k["de-Luge"] == k["deLuge"]
    assert k["death"] < k["deluge"] < k["deLuge"] < k["demark"]


def test_shifted_level_4_rules():
    # Table 11: variable, ignorable after a variable, primary ignorable, non-variable.
    ces = [(True, 0x0209, 0x20, 2), (False, 0, 0x25, 2), (False, 0x2380, 0x20, 8), (False, 0, 0x25, 2),
           (False, 0, 0, 0)]
    assert apply_variable_weighting(ces, "shifted") == [
        (0, 0, 0, 0x0209), (0, 0, 0, 0), (0x2380, 0x20, 8, 0xFFFF), (0, 0x25, 2, 0xFFFF), (0, 0, 0, 0)]
    assert apply_variable_weighting(ces, "blanked") == [
        (0, 0, 0, 0), (0, 0, 0, 0), (0x2380, 0x20, 8, 0), (0, 0x25, 2, 0), (0, 0, 0, 0)]


def _compare_by_levels(a, b, mode):
    """Level-by-level comparison of the weight arrays, without building a sort key."""
    wa = apply_variable_weighting(collation_elements(a), mode)
    wb = apply_variable_weighting(collation_elements(b), mode)
    for level in range(3 if mode in ("non-ignorable", "blanked") else 4):
        la = [w[level] for w in wa if w[level]]
        lb = [w[level] for w in wb if w[level]]
        if mode == "shift-trimmed" and level == 3:
            while la and la[-1] == 0xFFFF:
                la.pop()
            while lb and lb[-1] == 0xFFFF:
                lb.pop()
        if la != lb:
            return -1 if la < lb else 1
    return 0


def test_sort_key_agrees_with_level_comparison():
    rng = random.Random(1016)
    alphabet = "aAbBeEoéèôæß -'\"_!0"
    for _ in range(250):
        a = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 5)))
        b = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 5)))
        for mode in MODES:
            assert compare(a, b, mode) == _compare_by_levels(a, b, mode)


def test_order_is_total_and_consistent():
    rng = random.Random(77)
    alphabet = "abABáÁ -"
    words = ["".join(rng.choice(alphabet) for _ in range(rng.randint(1, 4))) for _ in range(150)]
    for mode in MODES:
        ordered = sorted(words, key=lambda s: sort_key(s, mode))
        for x, y in zip(ordered, ordered[1:]):
            assert compare(x, y, mode) <= 0


def test_implicit_weights():
    assert implicit_weights("一") == [(False, 0xFB40, 0x20, 2), (False, 0xCE00, 0, 0)]
    assert implicit_weights("㐀") == [(False, 0xFB80, 0x20, 2), (False, 0xB400, 0, 0)]
    assert compare("z", "一") < 0
    assert compare("一", "丁") < 0
    assert format_key(sort_key("一")) == "FB40 CE00 | 0020 | 0002 | FFFF FFFF"


def test_expansions_and_nfd():
    assert compare("æ", "ae") > 0 and compare("æ", "af") < 0
    assert sort_key("ß")[:2] == sort_key("ss")[:2]
    assert collation_elements("İ") == DUCET_SUBSET[("İ",)]
    assert sort_key("é") == sort_key("é")


def test_role_sort_key():
    assert format_key(sort_key("role")) == (
        "2584 252C 24BC 23E7 | 0020 0020 0020 0020 | 0002 0002 0002 0002 | FFFF FFFF FFFF FFFF")


def test_contractions_made_up_for_this_test():
    # A table made up for this test, with a contraction a + U+0301.
    table = parse_allkeys("0061 ; [.0100.0020.0002]\n0301 ; [.0000.0024.0002]\n"
                          "0302 ; [.0000.0027.0002]\n0323 ; [.0000.0042.0002]\n"
                          "0061 0301 ; [.0200.0020.0002]\n")
    assert collation_elements("á", table) == [(False, 0x200, 0x20, 2)]
    # Discontiguous: U+0323 (ccc 220) does not block U+0301 (ccc 230).
    assert collation_elements("ạ́", table) == [(False, 0x200, 0x20, 2), (False, 0, 0x42, 2)]
    # Blocked: U+0302 has the same ccc 230 as U+0301.
    assert collation_elements("ấ", table) == [
        (False, 0x100, 0x20, 2), (False, 0, 0x27, 2), (False, 0, 0x24, 2)]
