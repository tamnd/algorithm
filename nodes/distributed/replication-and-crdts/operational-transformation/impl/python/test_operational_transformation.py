# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/operational-transformation/. The authors are listed in prov/C2XWTY.jsonl.

import itertools

from operational_transformation import (
    Client,
    Server,
    apply,
    dopt_puzzle,
    find_dopt_divergence,
    simulate,
    transform,
)


def all_ops(doc: str, uid: int):
    for p in range(len(doc) + 1):
        for ch in "xy":
            yield ("ins", p, ch, uid)
    for p in range(len(doc)):
        yield ("del", p)
    yield ("nop",)


def test_tp1_holds_on_all_small_cases() -> None:
    count = 0
    for length in range(4):
        for doc in map("".join, itertools.product("ab", repeat=length)):
            for a in all_ops(doc, 1):
                for b in all_ops(doc, 2):
                    left = apply(apply(doc, a), transform(b, a))
                    right = apply(apply(doc, b), transform(a, b))
                    assert left == right, (doc, a, b)
                    count += 1
    assert count > 1000


def test_page_example() -> None:
    a, b = Client(0, "ab"), Client(1, "ab")
    s = Server(2, "ab")
    ma = a.insert(0, "x")  # a: "xab"
    mb = b.delete(1)  # b: "a"
    out1 = s.receive(0, ma)  # server: "xab", relays ins(0, x) to b
    assert s.doc == "xab" and out1 == [(1, (("ins", 0, "x", 0), 0, 0))]
    out2 = s.receive(1, mb)  # del(1) becomes del(2) on the server
    assert s.doc == "xa" and out2 == [(0, (("del", 2), 0, 1))]
    a.receive(out2[0][1])
    b.receive(out1[0][1])
    assert a.doc == b.doc == s.doc == "xa"


def test_jupiter_converges() -> None:
    for seed in range(150):
        docs = simulate(seed, 2 + seed % 4, 30 + seed % 70, "abc")
        assert len(set(docs)) == 1, (seed, docs)


def test_jupiter_larger_run() -> None:
    docs = simulate(999, 5, 300)
    assert len(set(docs)) == 1


def test_dopt_puzzle_found_by_search() -> None:
    doc, o1, o2, o3, r = find_dopt_divergence()
    assert (doc, o1, o2, o3) == ("", ("ins", 0, "x", 1), ("ins", 0, "y", 2), ("ins", 1, "z", 1))
    assert r == {"site1": "xzy", "dopt_site2": "xyz", "correct_site2": "xzy"}
    assert dopt_puzzle(doc, o1, o2, o3)["correct_site2"] == r["site1"]
