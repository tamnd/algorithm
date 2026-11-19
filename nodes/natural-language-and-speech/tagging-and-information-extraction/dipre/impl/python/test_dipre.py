# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dipre/. The authors are listed in prov/RKXK3C.jsonl.

import random

from dipre import (FORBIDDEN, Occurrence, Pattern, dipre, find_occurrences, generate_patterns, lcp, lcs,
                   match_pattern, specificity)

# The example of the page.
PAGES = [
    ("http://www.books.com/sf/list1",
     "<ul>\n<li><b>Foundation</b> by Isaac Asimov.\n<li><b>Neuromancer</b> by William Gibson.\n</ul>\n"),
    ("http://www.books.com/sf/list2",
     "<ul>\n<li><b>Hyperion</b> by Dan Simmons.\n<li><b>Dune</b> by Frank Herbert.\n"
     "<li><b>Contents</b> by chapter.\n</ul>\n"),
    ("http://www.reads.net/a/1",
     "<p>Dan Simmons: <i>Hyperion</i></p>\n<p>Ursula K. Le Guin: <i>The Dispossessed</i></p>\n<hr>\n"),
    ("http://www.reads.net/a/2",
     "<p>William Gibson: <i>Neuromancer</i></p>\n<p>Frank Herbert: <i>Dune</i></p>\n"
     "<p>Iain Banks: <i>Excession</i></p>\n<hr>\n"),
    ("http://www.blog.org/day7", "I read Dune by Frank Herbert and then Foundation by Isaac Asimov.\n"),
]
SEEDS = {("Isaac Asimov", "Foundation"), ("Frank Herbert", "Dune")}
BOOKS = {("Dan Simmons", "Hyperion"), ("William Gibson", "Neuromancer"),
         ("Ursula K. Le Guin", "The Dispossessed"), ("Iain Banks", "Excession")}
JUNK = ("chapter", "Contents")


def test_lcp_lcs_against_brute_force():
    rng = random.Random(1)
    for _ in range(300):
        strs = ["".join(rng.choice("ab") for _ in range(rng.randint(0, 5))) for _ in range(rng.randint(1, 4))]
        best = max((s[:k] for s in strs for k in range(len(s) + 1) if all(x.startswith(s[:k]) for x in strs)),
                   key=len, default="")
        assert lcp(strs) == best
        best = max((s[k:] for s in strs for k in range(len(s) + 1) if all(x.endswith(s[k:]) for x in strs)),
                   key=len, default="")
        assert lcs(strs) == best


def test_first_round_of_the_page_example():
    occs = find_occurrences(PAGES, SEEDS)
    assert len(occs) == 5
    asimov = [o for o in occs if o.author == "Isaac Asimov" and o.url.endswith("list1")][0]
    assert asimov == Occurrence("Isaac Asimov", "Foundation", False, "http://www.books.com/sf/list1",
                                "l>\n<li><b>", "</b> by ", ".\n<li><b>N")
    pats = generate_patterns(occs, 100)
    p = Pattern(False, "http://www.books.com/sf/list", "\n<li><b>", "</b> by ", ".\n<li><b>")
    assert pats == [p]
    assert specificity(p) == 28 * 8 * 8 * 9 == 16128
    # The blog group (middle " by ") has suffixes " and then " and ".\n", so its suffix is empty.
    assert match_pattern(p, PAGES) == {("Isaac Asimov", "Foundation"), ("Dan Simmons", "Hyperion"),
                                       ("Frank Herbert", "Dune")}


def test_full_run_finds_books_and_drifts():
    found, stats = dipre(PAGES, SEEDS, t=100)
    assert stats == [(5, 1, 3), (7, 2, 6), (11, 2, 7), (12, 2, 7)]
    assert found == SEEDS | BOOKS | {JUNK}


def test_higher_threshold_trades_recall_for_precision():
    found, stats = dipre(PAGES, SEEDS, t=30000)
    assert JUNK not in found
    assert found == SEEDS | {("Dan Simmons", "Hyperion")}


def occ(url, prefix, suffix):
    return Occurrence("A", "T", False, url, prefix, " by ", suffix)


def test_split_by_url_prefix():
    group = [occ("http://a.com/1", "<td>", "</td>"), occ("http://a.com/2", "<td>", "</td>"),
             occ("http://b.com/1", "<li>", "<br>"), occ("http://b.com/2", "<li>", "<br>")]
    # Whole group: urlprefix "http://", prefix ">", suffix "<": specificity 7 * 1 * 4 * 1 = 28, 28 * 4 = 112.
    assert generate_patterns(group, 111) == [Pattern(False, "http://", ">", " by ", "<")]
    a = Pattern(False, "http://a.com/", "<td>", " by ", "</td>")  # 13 * 4 * 4 * 5 = 1040, times 2
    b = Pattern(False, "http://b.com/", "<li>", " by ", "<br>")  # 13 * 4 * 4 * 4 = 832, times 2
    assert generate_patterns(group, 200) == sorted([a, b])
    assert generate_patterns(group, 2000) == [a]
    assert generate_patterns(group, 3000) == []
    assert generate_patterns(group[:1], 0) == []  # one occurrence is never enough


def field_ok(s, max_len):
    return 1 <= len(s) <= max_len and all(c not in FORBIDDEN for c in s)


def brute_match(p, pages, max_len):
    found = set()
    for url, text in pages:
        if url[:len(p.urlprefix)] != p.urlprefix:
            continue
        n = len(text)
        for a in range(n + 1):
            if text[:a][len(text[:a]) - len(p.prefix):] != p.prefix or a < len(p.prefix):
                continue
            for b in range(a, n + 1):
                if text[b:b + len(p.middle)] != p.middle:
                    continue
                c = b + len(p.middle)
                for d in range(c, n + 1):
                    if text[d:d + len(p.suffix)] == p.suffix:
                        x, y = text[a:b], text[c:d]
                        if field_ok(x, max_len) and field_ok(y, max_len):
                            found.add((x, y) if p.order else (y, x))
    return found


def rand_str(rng, alpha, lo, hi):
    return "".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi)))


def test_match_against_brute_force():
    rng = random.Random(2)
    for _ in range(300):
        pages = [("u" + rand_str(rng, "xy", 0, 2), rand_str(rng, "ab<c", 0, 14)) for _ in range(2)]
        p = Pattern(rng.random() < 0.5, rand_str(rng, "uxy", 0, 2), rand_str(rng, "ab<", 0, 2),
                    rand_str(rng, "ac", 1, 2), rand_str(rng, "b<", 0, 2))
        max_len = rng.randint(1, 5)
        assert match_pattern(p, pages, max_len) == brute_match(p, pages, max_len)


def test_patterns_match_their_own_occurrences():
    rng = random.Random(3)
    for _ in range(200):
        words = [rand_str(rng, "ab", 1, 3) for _ in range(4)]
        pages = []
        for k in range(3):
            text = "".join(rng.choice(words + ["<", "c", "cc", " "]) for _ in range(12))
            pages.append(("u/" + "xy"[k % 2] + str(k), text))
        pairs = {(rng.choice(words), rng.choice(words)) for _ in range(3)}
        occs = find_occurrences(pages, pairs, m=4, max_middle=6)
        for p in generate_patterns(occs, rng.randint(0, 50)):
            support = [o for o in occs if o.order == p.order and o.middle == p.middle
                       and o.url.startswith(p.urlprefix) and o.prefix.endswith(p.prefix)
                       and o.suffix.startswith(p.suffix)]
            assert len(support) >= 2 and specificity(p) > 0
            got = match_pattern(p, pages, max_len=40)
            for o in support:
                assert (o.author, o.title) in got


def test_loop_stops_and_only_grows():
    rng = random.Random(4)
    for _ in range(50):
        words = [rand_str(rng, "ab", 2, 3) for _ in range(5)]
        pages = [("u/" + str(k), "".join(rng.choice(words + ["<", " by ", ":"]) for _ in range(15)))
                 for k in range(3)]
        seeds = {(words[0], words[1])}
        found, stats = dipre(pages, seeds, t=5, m=3, rounds=6, max_middle=5, max_len=6)
        assert seeds <= found
        sizes = [s[2] for s in stats]
        assert sizes == sorted(sizes)
