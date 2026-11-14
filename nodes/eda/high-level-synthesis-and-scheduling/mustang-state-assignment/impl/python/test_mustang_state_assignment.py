# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mustang-state-assignment/. The authors are listed in prov/R8HB82.jsonl.

import itertools
import random

from fsmlogic import encoded_cost, encoded_function, exhaustive_best, implements, minimize
from mustang_state_assignment import embedding_cost, fanin_weights, fanout_weights, greedy_embed, mustang_encode

# The machine of the page (the same one as on the KISS page).
M1 = (1, 1, ["s0", "s1", "s2", "s3"], [
    ("0", "s0", "s2", "1"), ("1", "s0", "s2", "0"),
    ("0", "s1", "s2", "0"), ("1", "s1", "s2", "1"),
    ("0", "s2", "s3", "0"), ("1", "s2", "s1", "1"),
    ("0", "s3", "s1", "1"), ("1", "s3", "s3", "0"),
])


def random_fsm(rng: random.Random, n, ni, no):
    states = [f"s{i}" for i in range(n)]
    rows = []
    for s in states:
        for x in range(1 << ni):
            rows.append((format(x, f"0{ni}b"), s, rng.choice(states), "".join(rng.choice("01") for _ in range(no))))
    return (ni, no, states, rows)


def best_embedding(states, w, k):
    """Brute force: the least weighted Hamming cost over all injective codes."""
    return min(embedding_cost(w, dict(zip(states, cs))) for cs in itertools.permutations(range(1 << k), len(states)))


def test_page_example():
    states = M1[2]
    wo = fanout_weights(M1, 2)
    assert wo == {("s0", "s1"): 9, ("s0", "s2"): 1, ("s0", "s3"): 1, ("s1", "s2"): 1, ("s1", "s3"): 1, ("s2", "s3"): 5}
    k, co = mustang_encode(M1, "fanout")
    assert co == {"s0": 0, "s1": 1, "s2": 2, "s3": 3}
    assert embedding_cost(wo, co) == best_embedding(states, wo, 2) == 20
    assert encoded_cost(M1, co, 2) == (7, 19)
    wi = fanin_weights(M1, 2)
    assert wi == {("s0", "s1"): 0, ("s0", "s2"): 0, ("s0", "s3"): 0, ("s1", "s2"): 4, ("s1", "s3"): 6, ("s2", "s3"): 4}
    k, ci = mustang_encode(M1, "fanin")
    assert ci == {"s1": 0, "s3": 1, "s2": 2, "s0": 3}
    assert embedding_cost(wi, ci) == best_embedding(states, wi, 2) == 18
    assert encoded_cost(M1, ci, 2) == (6, 14)
    assert exhaustive_best(M1, 2)[0] == (4, 8)


def test_random_machines():
    rng = random.Random(1988)
    emb_opt = {"fanout": 0, "fanin": 0}
    hits = {"fanout": 0, "fanin": 0, "both": 0}
    excess = {"fanout": 0, "fanin": 0, "both": 0}
    worst = 0
    for _ in range(100):
        fsm = random_fsm(rng, 4, 1, 1)
        states = fsm[2]
        best = exhaustive_best(fsm, 2)[0][0]
        got = {}
        for mode in ("fanout", "fanin"):
            k, codes = mustang_encode(fsm, mode)
            assert k == 2 and len(set(codes.values())) == 4
            w = fanout_weights(fsm, k) if mode == "fanout" else fanin_weights(fsm, k)
            e, b = embedding_cost(w, codes), best_embedding(states, w, k)
            assert e >= b
            emb_opt[mode] += e == b
            domains, on, dc = encoded_function(fsm, codes, k)
            exact = minimize(domains, on, dc)
            assert implements(fsm, codes, k, exact)
            got[mode] = len(exact)
        got["both"] = min(got.values())
        for key, g in got.items():
            assert g >= best
            hits[key] += g == best
            excess[key] += g - best
        worst = max(worst, got["both"] - best)
    assert (emb_opt, hits, excess, worst) == MEASURED


# 100 machines: the greedy embedding reaches the least weighted distance on
# 84 (fanout) and 87 (fanin) machines; the final logic meets the best 2-bit
# code on 33, 47 and 57 machines (fanout, fanin, better of the two), with
# 87, 68 and 47 extra cubes in total; the better of the two loses at most 2.
MEASURED = (
    {"fanout": 84, "fanin": 87},
    {"fanout": 33, "fanin": 47, "both": 57},
    {"fanout": 87, "fanin": 68, "both": 47},
    2,
)


def test_greedy_embedding_on_five_states():
    rng = random.Random(7)
    opt = 0
    for _ in range(8):
        states = [f"s{i}" for i in range(5)]
        w = {(s, t): rng.randint(0, 6) for s, t in itertools.combinations(states, 2)}
        codes = greedy_embed(states, w, 3)
        assert len(set(codes.values())) == 5
        e, b = embedding_cost(w, codes), best_embedding(states, w, 3)
        assert e >= b
        opt += e == b
    assert opt == MEASURED_FIVE


# 8 random weight sets on 5 states in 3 bits: the greedy is optimal on 6.
MEASURED_FIVE = 6
