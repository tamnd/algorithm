# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modified-nodal-analysis/. The authors are listed in prov/CCJ8NY.jsonl.

import random
from fractions import Fraction as F

import pytest

from modified_nodal_analysis import SingularMatrixError, solve_mna, stamp_mna


def branch_currents(netlist, e, j):
    """Current of each element from its first node to its second node, from the element laws alone."""
    out = []
    k = 0
    for el in netlist:
        kind = el[0]
        if kind == "R":
            out.append((el[1], el[2], (e[el[1]] - e[el[2]]) / el[3]))
        elif kind == "G":
            out.append((el[1], el[2], el[3] * (e[el[1]] - e[el[2]])))
        elif kind == "I":
            out.append((el[1], el[2], el[3]))
        elif kind == "V":
            out.append((el[1], el[2], j[k]))
            k += 1
        elif kind == "VCCS":
            _, p, q, c, d, g = el
            out.append((p, q, g * (e[c] - e[d])))
    return out


def assert_solution(netlist, n, e, j):
    """Check KCL at every node and the law of every voltage source, exactly."""
    leaving = [0] * (n + 1)
    for p, q, cur in branch_currents(netlist, e, j):
        leaving[p] += cur
        leaving[q] -= cur
    assert all(x == 0 for x in leaving[1:]), leaving
    assert sum(leaving) == 0
    for el in netlist:
        if el[0] == "V":
            assert e[el[1]] - e[el[2]] == el[3]


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        self.parent[rx] = ry
        return True


def graph_says_nonsingular(netlist, n):
    """The theorem of the page for circuits of positive resistors and independent sources."""
    dsu = DSU(n + 1)
    for el in netlist:
        if el[0] == "V" and not dsu.union(el[1], el[2]):
            return False  # a loop of voltage sources
    for el in netlist:
        if el[0] in ("R", "G"):
            dsu.union(el[1], el[2])
    root = dsu.find(0)
    return all(dsu.find(k) == root for k in range(n + 1))  # else a cut set of current sources


def test_page_example():
    # 6 V source at node 1, 2 ohm from 1 to 2, 3 ohm from 2 to ground, 1 A into node 2.
    net = [("V", 1, 0, F(6)), ("R", 1, 2, F(2)), ("R", 2, 0, F(3)), ("I", 0, 2, F(1))]
    a, b, names = stamp_mna(net, 2)
    assert names == ["e1", "e2", "j0"]
    assert a == [[F(1, 2), F(-1, 2), 1], [F(-1, 2), F(5, 6), 0], [1, 0, 0]]
    assert b == [0, 1, 6]
    e, j = solve_mna(net, 2)
    assert e == [0, 6, F(24, 5)]
    assert j == [F(-3, 5)]
    assert_solution(net, 2, e, j)


def test_divider_and_transconductance():
    e, j = solve_mna([("V", 1, 0, F(10)), ("R", 1, 2, F(1)), ("R", 2, 0, F(4))], 2)
    assert e == [0, 10, 8] and j == [-2]
    # Input 1 V, current 2 e1 drawn from node 2 to ground, load 5 ohm: gain -10.
    net = [("V", 1, 0, F(1)), ("VCCS", 2, 0, 1, 0, F(2)), ("R", 2, 0, F(5))]
    e, j = solve_mna(net, 2)
    assert e == [0, 1, -10] and j == [0]


def test_wheatstone_bridge():
    # 1 A in at node 1, out at ground (node 0); unit resistors except 1-3 = 2 and 2-0 = 2.
    net = [("I", 0, 1, F(1)), ("R", 1, 2, F(1)), ("R", 1, 3, F(2)), ("R", 2, 3, F(1)), ("R", 2, 0, F(2)), ("R", 3, 0, F(1))]
    e, j = solve_mna(net, 3)
    assert e == [0, F(7, 5), F(4, 5), F(3, 5)]
    assert_solution(net, 3, e, j)


@pytest.mark.parametrize(
    "net, n",
    [
        ([("V", 1, 0, F(1)), ("V", 1, 0, F(2)), ("R", 1, 0, F(1))], 1),  # two sources in parallel: a loop
        ([("V", 1, 0, F(1)), ("V", 1, 2, F(1)), ("V", 2, 0, F(1))], 2),  # a loop of three sources
        ([("V", 1, 1, F(1)), ("R", 1, 0, F(1))], 1),  # a source with both ends on one node
        ([("R", 1, 0, F(1)), ("I", 1, 2, F(1))], 2),  # node 2 meets only a current source
        ([("R", 1, 2, F(1)), ("I", 0, 1, F(1))], 2),  # nodes 1 and 2 float together
        ([("R", 1, 0, F(1))], 2),  # node 2 meets nothing, as a node with only capacitors at DC
        ([("R", 1, 0, F(1)), ("R", 1, 0, F(-1)), ("I", 0, 1, F(1))], 1),  # a negative resistor cancels
    ],
)
def test_singular_cases_are_reported(net, n):
    with pytest.raises(SingularMatrixError):
        solve_mna(net, n)


def random_circuit(rng, n, with_vccs):
    net = []
    for _ in range(rng.randint(1, 3 * n + 2)):
        p, q = rng.randint(0, n), rng.randint(0, n)
        r = rng.random()
        if r < 0.55:
            if p != q:
                net.append(("R", p, q, F(rng.randint(1, 9), rng.randint(1, 4))))
        elif r < 0.75:
            net.append(("I", p, q, F(rng.randint(-5, 5))))
        elif r < 0.9 or not with_vccs:
            net.append(("V", p, q, F(rng.randint(-5, 5))))
        else:
            c, d = rng.randint(0, n), rng.randint(0, n)
            net.append(("VCCS", p, q, c, d, F(rng.randint(-3, 3), 2)))
    return net


def test_random_circuits_match_the_graph_theorem():
    rng = random.Random(20250101)
    counts = [0, 0]
    for _ in range(1500):
        n = rng.randint(1, 6)
        net = random_circuit(rng, n, with_vccs=False)
        expected = graph_says_nonsingular(net, n)
        try:
            e, j = solve_mna(net, n)
        except SingularMatrixError:
            assert not expected, net
            counts[0] += 1
            continue
        assert expected, net
        assert_solution(net, n, e, j)
        counts[1] += 1
    assert min(counts) > 200


def test_random_circuits_with_controlled_sources_satisfy_the_laws():
    rng = random.Random(7)
    solved = 0
    for _ in range(800):
        n = rng.randint(1, 5)
        net = random_circuit(rng, n, with_vccs=True)
        try:
            e, j = solve_mna(net, n)
        except SingularMatrixError:
            continue
        assert_solution(net, n, e, j)
        solved += 1
    assert solved > 100


def test_float_agrees_with_fraction():
    rng = random.Random(99)
    checked = 0
    for _ in range(400):
        n = rng.randint(1, 6)
        net = random_circuit(rng, n, with_vccs=False)
        if not graph_says_nonsingular(net, n):
            continue
        e, j = solve_mna(net, n)
        fnet = [tuple(float(x) if isinstance(x, F) else x for x in el) for el in net]
        fe, fj = solve_mna(fnet, n, tol=1e-12)
        for exact, approx in zip(e + j, fe + fj):
            assert abs(float(exact) - approx) <= 1e-9 * (1 + abs(float(exact)))
        checked += 1
    assert checked > 50
