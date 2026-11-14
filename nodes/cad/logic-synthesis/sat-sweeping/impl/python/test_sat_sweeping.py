# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sat-sweeping/. The authors are listed in prov/D7SVKR.jsonl.

import random
from itertools import product

from sat_sweeping import Aig, dpll, sat_sweep

# The example of the page, n = 2 (x = 1, y = 2):
#   3 = x & !y, 4 = !x & y, 5 = !3 & !4 (XNOR), 6 = x & y, 7 = !x & !y,
#   8 = !6 & !7 (XOR), 9 = !5 & 8, output 9 (XOR and XOR = XOR).
EXAMPLE_ANDS = [(2, 5), (3, 4), (7, 9), (2, 4), (3, 5), (13, 15), (11, 16)]
EXAMPLE_OUT = [18]


def tables(n, fanins, total) -> list:
    """Truth table of every node as an integer; input 1 is the high bit."""
    full = (1 << (1 << n)) - 1
    t = [0]
    for i in range(1, n + 1):
        t.append(sum(1 << m for m in range(1 << n) if (m >> (n - i)) & 1))
    for v in range(n + 1, total):
        a, b = fanins[v]
        x = t[a >> 1] ^ (full if a & 1 else 0)
        y = t[b >> 1] ^ (full if b & 1 else 0)
        t.append(x & y)
    return t


def lit_table(t, lit, n) -> int:
    full = (1 << (1 << n)) - 1
    return t[lit >> 1] ^ (full if lit & 1 else 0)


def input_tables(n, ands, outs) -> list:
    fanins = [(0, 0)] * (n + 1) + list(ands)
    t = tables(n, fanins, len(fanins))
    return [lit_table(t, o, n) for o in outs]


def random_aig(rng, n, n_and, window):
    """A random AIG with copies of its own logic, so that sweeping has work."""
    ands = []
    for i in range(n_and):
        v = n + 1 + i
        lo = max(1, v - window)
        a, b = rng.randrange(lo, v), rng.randrange(lo, v)
        ands.append((2 * a + rng.randint(0, 1), 2 * b + rng.randint(0, 1)))
    # rebuild a few nodes in another form: a & b = !( !a | !b ) = !(!(!(!a & !b)))
    for _ in range(rng.randint(0, 4)):
        v = rng.randrange(n + 1, n + 1 + len(ands))
        a, b = ands[v - n - 1]
        base = n + 1 + len(ands)
        ands.append((a ^ 1, a ^ 1))            # base     = !a  (as !a & !a)
        ands.append((b ^ 1, b ^ 1))            # base + 1 = !b
        ands.append((2 * base + 1, 2 * (base + 1) + 1))  # base + 2 = a & b
    top = n + len(ands)
    outs = [2 * top + rng.randint(0, 1)] + [2 * rng.randrange(1, top + 1) + rng.randint(0, 1)
                                            for _ in range(2)]
    return ands, outs


def test_dpll_against_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(300):
        nv = rng.randint(1, 9)
        cls = [[rng.choice([1, -1]) * rng.randint(1, nv) for _ in range(rng.randint(1, 3))]
               for _ in range(rng.randint(1, 5 * nv))]
        brute = any(all(any((x[abs(l) - 1] == 1) == (l > 0) for l in c) for c in cls)
                    for x in product((0, 1), repeat=nv))
        model = dpll(cls, nv)
        assert (model is not None) == brute
        if model is not None:
            assert all(any((model[abs(l) - 1] == 1) == (l > 0) for l in c) for c in cls)


def test_example() -> None:
    res, outs, stats = sat_sweep(2, EXAMPLE_ANDS, EXAMPLE_OUT, n_patterns=4, seed=3)
    assert len(res.fanins) - 3 == 3  # x & !y, !x & y and one XOR node
    t = tables(2, res.fanins, len(res.fanins))
    assert lit_table(t, outs[0], 2) == 0b0110
    assert stats["unsat"] >= 1


def check_reduced(res, outs, n) -> None:
    t = tables(n, res.fanins, len(res.fanins))
    full = (1 << (1 << n)) - 1
    seen = {}
    for v in range(len(res.fanins)):
        key = min(t[v], t[v] ^ full)
        assert key not in seen, (v, seen[key])  # no two nodes equal up to complement
        seen[key] = v


def test_function_kept_and_result_reduced() -> None:
    rng = random.Random(2)
    for trial in range(150):
        n = rng.randint(1, 8)
        ands, outs = random_aig(rng, n, rng.randint(1, 25), 6)
        res, res_outs, _ = sat_sweep(n, ands, outs, n_patterns=rng.choice([1, 4, 16]),
                                     seed=trial)
        t = tables(n, res.fanins, len(res.fanins))
        assert [lit_table(t, o, n) for o in res_outs] == input_tables(n, ands, outs)
        check_reduced(res, res_outs, n)
        assert len(res.fanins) - n - 1 <= len(ands)


def test_constant_node_is_found() -> None:
    # 3 = x & y, 4 = x & !y, 5 = 3 & 4 is the constant 0 but not by a local rule
    res, outs, stats = sat_sweep(2, [(2, 4), (2, 5), (6, 8)], [10], n_patterns=2, seed=0)
    assert outs == [0]
    assert len(res.fanins) == 3


def test_add_and_rules() -> None:
    g = Aig(2)
    assert g.add_and(2, 3) == 0 and g.add_and(2, 1) == 2 and g.add_and(4, 4) == 4
    a = g.add_and(2, 4)
    assert g.add_and(4, 2) == a and len(g.fanins) == 4
