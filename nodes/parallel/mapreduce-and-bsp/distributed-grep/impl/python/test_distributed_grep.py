# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-grep/. The authors are listed in prov/EX8YJV.jsonl.

import random

from distributed_grep import byte_splits, count_matches_job, distributed_grep, grep_one_machine, read_lines

TEXT = "error: disk\nok\nwarn: fan\nerror: net\nok\n"


def random_text(rng, n_lines):
    lines = ["".join(rng.choice("abcxy") for _ in range(rng.randrange(0, 9))) for _ in range(n_lines)]
    text = "\n".join(lines)
    return text + ("\n" if rng.random() < 0.5 else "")


def test_page_example():
    out, costs = distributed_grep(TEXT, "^error", 10)
    assert out == [(0, "error: disk"), (25, "error: net")]
    assert costs["map_tasks"] == 4 and costs["pairs_sent"] == 0 and costs["lines_read"] == 5
    assert [list(read_lines(TEXT, a, b)) for a, b in byte_splits(TEXT, 10)] == [
        [(0, "error: disk")], [(12, "ok"), (15, "warn: fan")], [(25, "error: net")], [(36, "ok")]]
    out1, costs1 = distributed_grep(TEXT, "^error", 10, r=1)
    assert out1 == out and costs1["pairs_sent"] == 2 and costs1["bytes_sent"] == 1 + 11 + 2 + 10


def test_every_line_read_exactly_once_and_matches_one_machine():
    rng = random.Random(10)
    for _ in range(400):
        text = random_text(rng, rng.randrange(0, 25))
        size = rng.randrange(1, 30)
        lines = [kv for a, b in byte_splits(text, size) for kv in read_lines(text, a, b)]
        assert lines == grep_one_machine(text, "")
        for regex in ("a", "^x", "y$", "ab+c", "zzz"):
            want = grep_one_machine(text, regex)
            for r in (0, 1):
                got, costs = distributed_grep(text, regex, size, r)
                assert got == want
                assert costs["pairs_sent"] == (len(want) if r == 1 else 0)
                assert costs["bytes_read"] == len(text)
            assert count_matches_job(text, regex, size)[0] == len(want)


def test_empty_and_single_line():
    assert distributed_grep("", "a", 4) == ([], {"map_tasks": 0, "lines_read": 0, "bytes_read": 0,
                                                 "pairs_sent": 0, "bytes_sent": 0, "output_pairs": 0})
    assert distributed_grep("abcabcabc", "c", 2)[0] == [(0, "abcabcabc")]
    assert distributed_grep("\n\n", "^$", 1)[0] == [(0, ""), (1, "")]
