# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/card-marking/. The authors are listed in prov/45B69W.jsonl.

import random
from typing import Optional

from card_marking import CLEAN, DIRTY, CardHeap


class Checked(CardHeap):
    """Checks, at the start of each minor collection, that every old-to-young
    pointer lies on a dirty card."""

    checks = 0

    def minor_collect(self) -> None:
        for a, i in self.old_to_young():
            assert self.covered(a, i), "an old-to-young pointer is on a clean card"
        Checked.checks += 1
        super().minor_collect()


class Oracle:
    def __init__(self) -> None:
        self.fields: dict[int, list[Optional[int]]] = {}
        self.roots: list[Optional[int]] = []

    def reachable(self) -> set[int]:
        seen: set[int] = set()
        stack = [r for r in self.roots if r is not None]
        while stack:
            o = stack.pop()
            if o not in seen:
                seen.add(o)
                stack.extend(t for t in self.fields[o] if t is not None)
        return seen


def check(h: CardHeap, m: Oracle) -> None:
    oid = lambda p: None if p is None else h.oid(p)
    assert [oid(r) for r in h.roots] == m.roots
    by_oid = {h.oid(p): p for p in list(h.young) + h.old_objects()}
    for o in m.reachable():
        assert o in by_oid, "a reachable object was freed"
        assert [oid(t) for t in h.fields_of(by_oid[o])] == m.fields[o]
    for p in by_oid.values():
        for t in h.fields_of(p):
            assert t is None or t >= 0 or t in h.young, "dangling young pointer"


def run(seed: int, mode: str) -> CardHeap:
    rng = random.Random(seed)
    h = Checked(rng.randint(1, 4), rng.randint(2, 8), rng.randint(1, 3), mode)
    m = Oracle()
    for _ in range(300):
        live = [k for k, r in enumerate(m.roots) if r is not None]
        op = rng.random()
        if op < 0.3 or not live:
            nf = rng.randint(0, 6)
            k = h.alloc(nf)
            m.fields[h.oid(h.roots[k])] = [None] * nf
            m.roots.append(h.oid(h.roots[k]))
        elif op < 0.75:
            s = rng.choice(live)
            nf = len(m.fields[m.roots[s]])
            if nf:
                i, r = rng.randrange(nf), rng.choice(live + [None])
                h.write(s, i, r)
                m.fields[m.roots[s]][i] = None if r is None else m.roots[r]
        elif op < 0.9:
            s = rng.choice(live)
            nf = len(m.fields[m.roots[s]])
            if nf:
                i, d = rng.randrange(nf), rng.randrange(len(m.roots))
                h.load(s, i, d)
                m.roots[d] = m.fields[m.roots[s]][i]
        else:
            d = rng.choice(live)
            h.drop(d)
            m.roots[d] = None
        check(h, m)
    h.minor_collect()
    check(h, m)
    return h


def test_dirty_cards_cover_old_to_young_slot_mode() -> None:
    before = Checked.checks
    for seed in range(30):
        run(seed, "slot")
    assert Checked.checks - before > 200


def test_dirty_cards_cover_old_to_young_object_mode() -> None:
    for seed in range(30):
        run(1000 + seed, "object")


def test_unconditional_dirtying() -> None:
    h = CardHeap(card_shift=2, nursery_size=100)
    k = h.alloc(2)
    h.minor_collect()
    a = h.roots[k]
    assert a == 0 and h.cards[0] == CLEAN
    h.write(k, 1, None)  # a store of nil dirties the card too
    assert h.cards[0] == DIRTY
    h.minor_collect()
    assert h.cards[0] == CLEAN  # no young pointer on it, so it is cleaned


def test_page_example() -> None:
    h = CardHeap(card_shift=2, nursery_size=100, tenure_age=1)
    ka, kb, kc = h.alloc(3), h.alloc(5), h.alloc(1)
    h.minor_collect()
    assert [h.roots[ka], h.roots[kb], h.roots[kc]] == [0, 4, 10]
    assert h.first == [0, 4, 4]
    kx = h.alloc(0)
    h.write(kb, 4, kx)  # slot word 9, card 2
    h.write(ka, 0, None)  # slot word 1, card 0
    assert list(h.cards) == [DIRTY, CLEAN, DIRTY]
    h.drop(kx)
    h.minor_collect()
    assert h.cards_scanned == 2
    assert h.mem[9] == 12 and h.oid(12) == 3  # x was promoted to address 12
    assert list(h.cards) == [CLEAN] * 4


def test_survivor_keeps_card_dirty() -> None:
    h = CardHeap(card_shift=3, nursery_size=100, tenure_age=2)
    k = h.alloc(1)
    h.minor_collect()
    h.minor_collect()  # k is promoted at age 2
    assert h.roots[k] == 0
    y = h.alloc(0)
    h.write(k, 0, y)
    h.drop(y)
    h.minor_collect()  # y survives with age 1 and stays young
    assert h.is_young(h.mem[1]) and h.cards[0] == DIRTY
    h.minor_collect()  # y is promoted now
    assert not h.is_young(h.mem[1]) and h.cards[0] == CLEAN


def test_promoted_object_pointing_to_survivor_dirties_its_card() -> None:
    h = Checked(card_shift=2, nursery_size=100, tenure_age=2)
    p = h.alloc(1)
    h.minor_collect()  # p has age 1
    c = h.alloc(0)
    h.write(p, 0, c)
    h.drop(c)
    h.minor_collect()  # p is promoted, c survives young
    assert h.covered(h.roots[p], 0)
    h.minor_collect()
    assert h.oid(h.mem[h.roots[p] + 1]) == 1
