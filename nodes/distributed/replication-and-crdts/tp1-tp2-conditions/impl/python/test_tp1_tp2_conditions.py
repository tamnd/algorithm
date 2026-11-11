# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tp1-tp2-conditions/. The authors are listed in prov/21VA27.jsonl.

from tp1_tp2_conditions import find_tp1, find_tp2, naive, ressel, tp1_holds, tp2_holds


def test_naive_breaks_tp1() -> None:
    doc, a, b = find_tp1(naive)
    assert (doc, a, b) == ("", ("ins", 0, "x", 1), ("ins", 0, "y", 2))
    assert not tp1_holds(naive, doc, a, b)  # one site gets "yx", the other "xy"


def test_ressel_satisfies_tp1_on_small_cases() -> None:
    assert find_tp1(ressel, 4) is None


def test_ressel_breaks_tp2() -> None:
    doc, a, b, c, left, right = find_tp2(ressel, visible=True)
    assert doc == "a"
    assert (a, b, c) == (("ins", 1, "x", 1), ("del", 0), ("ins", 0, "z", 3))
    assert (left, right) == ("zx", "xz")


def test_randolph_counterexample() -> None:
    # Randolph et al. 2013, Fig. 11, positions moved from 1-based to 0-based.
    o1, o2, o3 = ("del", 0), ("ins", 1, "c", 2), ("ins", 0, "e", 3)
    assert not tp2_holds(ressel, o1, o2, o3)
    assert ressel(ressel(o3, o1), ressel(o2, o1)) == ("ins", 1, "e", 3)
    assert ressel(ressel(o3, o2), ressel(o1, o2)) == ("ins", 0, "e", 3)
