# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transformation-based-reversible-synthesis/. The authors are listed in prov/WZABZ7.jsonl.

import random
from collections import Counter, deque
from itertools import permutations

from transformation_based_reversible_synthesis import (
    apply_gate,
    row_gates,
    synthesis_steps,
    synthesize,
    table,
)


def all_gates(n):
    """Every multiple-control Toffoli gate on n lines."""
    gates = []
    for t in range(n):
        others = [b for b in range(n) if b != t]
        for m in range(1 << (n - 1)):
            c = 0
            for k, b in enumerate(others):
                if m >> k & 1:
                    c |= 1 << b
            gates.append((c, t))
    return gates


def optimal_sizes_3():
    """The least number of gates for every function of 3 bits, by BFS."""
    moves = [tuple(apply_gate(g, x) for x in range(8)) for g in all_gates(3)]
    start = tuple(range(8))
    dist = {start: 0}
    queue = deque([start])
    while queue:
        p = queue.popleft()
        for m in moves:
            q = tuple(m[v] for v in p)
            if q not in dist:
                dist[q] = dist[p] + 1
                queue.append(q)
    return dist


def check_gates(circuit, n):
    for controls, target in circuit:
        assert 0 <= target < n
        assert 0 <= controls < 1 << n
        assert not controls >> target & 1


def highest_zero(i, n):
    """The position of the highest 0 bit of i below bit n, or -1."""
    for t in range(n - 1, -1, -1):
        if not i >> t & 1:
            return t
    return -1


def test_paper_example_basic():
    # Maslov, Dueck and Miller, Table I: NOT(a) for row 0, then two gates for
    # row 5 and one for row 6, found from the outputs backward.
    f = [1, 0, 3, 2, 5, 7, 4, 6]
    assert synthesize(f) == [(0b110, 0), (0b101, 1), (0b110, 0), (0b000, 0)]


def test_decrement_needs_the_bidirectional_form():
    f = [7, 0, 1, 2, 3, 4, 5, 6]
    assert len(synthesize(f)) == 7
    circuit = synthesize(f, bidirectional=True)
    assert table(circuit, 3) == f
    assert len(circuit) == 3 == optimal_sizes_3()[tuple(f)]


def test_worst_case_functions():
    f3 = [7, 1, 4, 3, 0, 2, 6, 5]
    f4 = [15, 1, 12, 3, 5, 6, 8, 7, 0, 10, 13, 9, 2, 4, 14, 11]
    for f, n in [(f3, 3), (f4, 4)]:
        circuit = synthesize(f)
        assert table(circuit, n) == f
        assert len(circuit) == (n - 1) * 2 ** n + 1
    assert optimal_sizes_3()[tuple(f3)] == 6


def test_row_gates_fix_the_rows_below():
    n = 4
    for i in range(16):
        for v in range(i + 1, 16):
            gates = row_gates(v, i, n)
            assert len(gates) == bin(v ^ i).count("1") <= highest_zero(i, n) + 1
            check_gates(gates, n)
            x = v
            for g in gates:
                x = apply_gate(g, x)
            assert x == i
            for j in range(i):
                y = j
                for g in gates:
                    y = apply_gate(g, y)
                assert y == j


def test_all_permutations_of_three_bits():
    opt = optimal_sizes_3()
    assert len(opt) == 40320
    # Shende, Prasad, Markov and Hayes, Table 1, column CNT
    assert sorted(Counter(opt.values()).items()) == [
        (0, 1), (1, 12), (2, 102), (3, 625), (4, 2780),
        (5, 8921), (6, 17049), (7, 10253), (8, 577),
    ]
    basic, both = Counter(), Counter()
    hits = Counter()
    for p in permutations(range(8)):
        f = list(p)
        for bidirectional, sizes in [(False, basic), (True, both)]:
            steps = synthesis_steps(f, bidirectional)
            for i, (_, gates) in enumerate(steps):
                assert len(gates) <= highest_zero(i, 3) + 1
            circuit = synthesize(f, bidirectional)
            check_gates(circuit, 3)
            assert table(circuit, 3) == f
            assert opt[p] <= len(circuit) <= 17
            sizes[len(circuit)] += 1
            hits[bidirectional] += len(circuit) == opt[p]
    hits_basic, hits_both = hits[False], hits[True]
    # Miller, Maslov and Dueck, Table 4, column (a)
    assert [basic[k] for k in range(17, -1, -1)] == [
        1, 14, 92, 380, 1113, 2468, 4311, 6083, 7044,
        6754, 5379, 3549, 1922, 839, 286, 72, 12, 1,
    ]
    total_basic = sum(k * v for k, v in basic.items())
    total_both = sum(k * v for k, v in both.items())
    total_opt = sum(opt.values())
    assert (total_basic, total_both, total_opt) == (349632, 297272, 236497)
    assert (hits_basic, hits_both) == (3484, 10828)
    assert (max(basic), max(both)) == (17, 15)


def test_random_functions_on_more_lines():
    rng = random.Random(3)
    for n in [4, 5, 6, 7]:
        for _ in range(6 if n < 7 else 2):
            f = list(range(1 << n))
            rng.shuffle(f)
            for bidirectional in [False, True]:
                circuit = synthesize(f, bidirectional)
                check_gates(circuit, n)
                assert table(circuit, n) == f
                assert len(circuit) <= (n - 1) * 2 ** n + 1


def test_odd_permutations_need_a_gate_on_all_lines():
    # On 4 lines every gate with at most 2 controls is an even permutation,
    # so a circuit for an odd permutation must use a gate with 3 controls.
    rng = random.Random(5)
    for _ in range(30):
        f = list(range(16))
        rng.shuffle(f)
        seen = [False] * 16
        cycles = 0
        for s in range(16):
            if not seen[s]:
                cycles += 1
                x = s
                while not seen[x]:
                    seen[x] = True
                    x = f[x]
        odd = (16 - cycles) % 2 == 1
        circuit = synthesize(f, bidirectional=True)
        assert table(circuit, 4) == f
        if odd:
            assert any(bin(c).count("1") == 3 for c, _ in circuit)


def test_rejects_a_non_permutation():
    for f in [[0, 0], [0, 1, 2], [1, 2, 3, 4]]:
        try:
            synthesize(f)
        except ValueError:
            pass
        else:
            raise AssertionError("accepted %r" % (f,))
