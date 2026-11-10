# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consensus-round-lower-bound/. The authors are listed in prov/72GMWX.jsonl.

import random
from itertools import product

from consensus_round_lower_bound import (
    build_chain,
    final_views,
    find_violation,
    floodset_rule,
    make,
    max_crashes,
    one_crash_per_round,
    witness,
)

CASES = [(3, 1), (4, 1), (4, 2), (5, 2)]


def test_chain_shape() -> None:
    for n, rounds in CASES:
        chain = build_chain(n, rounds)
        assert chain[0] == make((0,) * n, {})
        assert chain[-1] == make((1,) * n, {})
        assert max_crashes(chain) == rounds
        assert all(one_crash_per_round(e) for e in chain)
        # each crash is in rounds 1 .. R, so the crash count is at most R
        assert all(1 <= c[0] <= rounds for e in chain for _, c in e[1])


def test_neighbours_share_a_live_process_with_the_same_view() -> None:
    for n, rounds in CASES:
        chain = build_chain(n, rounds)
        for a, b in zip(chain, chain[1:]):
            assert witness(a, b, rounds) is not None, (a, b)


def test_chain_lengths() -> None:
    assert len(build_chain(3, 1)) == 22
    assert len(build_chain(4, 2)) == 261


def test_floodset_with_f_rounds_breaks() -> None:
    # R = f rounds: every execution of the chain has at most f crashes.
    for n, f in CASES:
        chain = build_chain(n, f)
        bad = find_violation(chain, f, floodset_rule)
        assert bad is not None and bad[0] == "agreement"
        assert len(bad[1][1]) <= f


def test_any_rule_with_f_rounds_breaks() -> None:
    rng = random.Random(1982)
    for n, f in [(3, 1), (4, 1), (4, 2)]:
        chain = build_chain(n, f)
        for _ in range(40):
            table: dict = {}
            bias = rng.random()

            def rule(p: int, view: object) -> int:
                key = (p, view)
                if key not in table:
                    table[key] = 1 if rng.random() < bias else 0
                return table[key]

            assert find_violation(chain, f, rule) is not None


def test_floodset_with_f_plus_1_rounds_survives_its_chain() -> None:
    # With R = f + 1 rounds the chain needs f + 1 crashes, which the model
    # does not allow, and FloodSet breaks only in such executions.
    for n, f in [(3, 1), (4, 1)]:
        rounds = f + 1
        chain = build_chain(n, rounds)
        assert max_crashes(chain) == f + 1
        for e in chain:
            dec = {floodset_rule(p, v) for p, v in final_views(e, rounds).items()}
            if len(e[1]) <= f:
                assert len(dec) <= 1


def test_floodset_rule_on_all_small_runs() -> None:
    # An independent check of the rule: with f + 1 rounds and at most f
    # crashes, FloodSet agrees on every crash plan for n = 3 and f = 1.
    n, f = 3, 1
    others = {p: [q for q in range(n) if q != p] for p in range(n)}
    for inputs in product([0, 1], repeat=n):
        plans = [{}]
        for p in range(n):
            for r in (1, 2):
                for mask in range(4):
                    s = frozenset(others[p][b] for b in range(2) if mask >> b & 1)
                    plans.append({p: (r, s)})
        for plan in plans:
            views = final_views(make(inputs, plan), f + 1)
            assert len({floodset_rule(p, v) for p, v in views.items()}) == 1
