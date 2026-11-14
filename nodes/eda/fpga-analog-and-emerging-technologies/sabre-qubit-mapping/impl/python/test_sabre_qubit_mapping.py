# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sabre-qubit-mapping/. The authors are listed in prov/2MX74V.jsonl.

import cmath
import itertools
import math
import random
from collections import deque

from sabre_qubit_mapping import (
    dependence_dag,
    distances,
    sabre,
    swap_count,
    swap_search,
    to_three_cnots,
)


# ---------- devices and circuits ----------

def line(n):
    return [(i, i + 1) for i in range(n - 1)]


def star(n):
    return [(0, i) for i in range(1, n)]


def grid(r, c):
    e = []
    for i in range(r):
        for j in range(c):
            v = i * c + j
            if j + 1 < c:
                e.append((v, v + 1))
            if i + 1 < r:
                e.append((v, v + c))
    return e


def tree(rng, n):
    return [(i, rng.randrange(i)) for i in range(1, n)]


def random_circuit(rng, n, g, one_qubit=("h",)):
    out = []
    for _ in range(g):
        if n == 1 or rng.random() < 0.25:
            out.append((rng.choice(one_qubit), (rng.randrange(n),)))
        else:
            out.append(("cx", tuple(rng.sample(range(n), 2))))
    return out


# ---------- checks ----------

def check_routing(gates, edges, ops, start, final):
    """Every two-qubit operation is on an edge, every gate runs once on the
    physical qubits of its logical qubits at that time, the order respects
    the dependences, and the final layout is the one the SWAPs make."""
    edge_set = {frozenset(e) for e in edges}
    layout = list(start)
    owner = {p: a for a, p in enumerate(layout)}
    succ, npred = dependence_dag(gates)
    npred = list(npred)
    ran = []
    for op in ops:
        if op[0] == "swap":
            p, q = op[1]
            assert frozenset((p, q)) in edge_set
            a, b = owner.get(p), owner.get(q)
            owner.pop(p, None)
            owner.pop(q, None)
            if a is not None:
                layout[a] = q
                owner[q] = a
            if b is not None:
                layout[b] = p
                owner[p] = b
        else:
            _, i, phys = op
            assert npred[i] == 0  # all its predecessors have run
            assert phys == tuple(layout[a] for a in gates[i][1])
            if len(phys) == 2:
                assert frozenset(phys) in edge_set
            for j in succ[i]:
                npred[j] -= 1
            npred[i] = -1
            ran.append(i)
    assert sorted(ran) == list(range(len(gates)))
    assert layout == list(final)


def exact_swaps(n_log, gates, n_phys, edges):
    """Fewest SWAPs over every initial layout, by breadth-first search over
    (layout, set of gates run), running every ready gate for free."""
    _, dist = distances(n_phys, edges)
    succ, _ = dependence_dag(gates)
    preds = [[j for j in range(len(gates)) if i in succ[j]] for i in range(len(gates))]
    full = (1 << len(gates)) - 1

    def run_ready(lay, done):
        changed = True
        while changed:
            changed = False
            for i, (_, qs) in enumerate(gates):
                if done >> i & 1 or any(not done >> j & 1 for j in preds[i]):
                    continue
                if len(qs) == 1 or dist[lay[qs[0]]][lay[qs[1]]] == 1:
                    done |= 1 << i
                    changed = True
        return done

    seen = {}
    queue = deque()
    for lay in itertools.permutations(range(n_phys), n_log):
        s = (lay, run_ready(lay, 0))
        if s not in seen:
            seen[s] = 0
            queue.append(s)
    while queue:
        lay, done = queue.popleft()
        if done == full:
            return seen[(lay, done)]
        owner = {p: a for a, p in enumerate(lay)}
        for p, q in edges:
            if p not in owner and q not in owner:
                continue
            nl = list(lay)
            if p in owner:
                nl[owner[p]] = q
            if q in owner:
                nl[owner[q]] = p
            nl = tuple(nl)
            s = (nl, run_ready(nl, done))
            if s not in seen:
                seen[s] = seen[(lay, done)] + 1
                queue.append(s)
    raise AssertionError("no solution")


# ---------- simulation ----------

H = [[1 / math.sqrt(2), 1 / math.sqrt(2)], [1 / math.sqrt(2), -1 / math.sqrt(2)]]
T = [[1, 0], [0, cmath.exp(1j * math.pi / 4)]]
X = [[0, 1], [1, 0]]
ONE = {"h": H, "t": T, "x": X}


def apply(state, name, qs, n):
    out = list(state)
    if len(qs) == 1:
        m, (q,) = ONE[name], qs
        for s in range(1 << n):
            if not s >> q & 1:
                a0, a1 = state[s], state[s | 1 << q]
                out[s] = m[0][0] * a0 + m[0][1] * a1
                out[s | 1 << q] = m[1][0] * a0 + m[1][1] * a1
    elif name == "cx":
        c, t = qs
        for s in range(1 << n):
            if s >> c & 1:
                out[s] = state[s ^ 1 << t]
    else:  # swap
        p, q = qs
        for s in range(1 << n):
            if (s >> p & 1) != (s >> q & 1):
                out[s] = state[s ^ (1 << p) ^ (1 << q)]
    return out


def run_logical(gates, n, x):
    state = [0j] * (1 << n)
    state[x] = 1
    for name, qs in gates:
        state = apply(state, name, qs, n)
    return state


def run_physical(gates, ops, n_phys, start, x):
    """Load logical basis state x through the initial layout, other qubits 0."""
    s0 = sum(1 << start[a] for a in range(len(start)) if x >> a & 1)
    state = [0j] * (1 << n_phys)
    state[s0] = 1
    for op in ops:
        if op[0] == "gate":
            state = apply(state, gates[op[1]][0], op[2], n_phys)
        elif op[0] == "swap":
            state = apply(state, "swap", op[1], n_phys)
        else:
            state = apply(state, op[0], op[1], n_phys)
    return state


def relabel(state, n_log, n_phys, final):
    """The logical state placed on the physical qubits of the final layout."""
    out = [0j] * (1 << n_phys)
    for y, amp in enumerate(state):
        out[sum(1 << final[a] for a in range(n_log) if y >> a & 1)] = amp
    return out


# ---------- tests ----------

def test_page_example():
    gates = [("cx", (0, 1)), ("cx", (1, 2)), ("cx", (0, 2))]  # a, b, c = 0, 1, 2
    ops, start, final = sabre(3, gates, 3, line(3), seed=0)
    check_routing(gates, line(3), ops, start, final)
    assert swap_count(ops) == 1 == exact_swaps(3, gates, 3, line(3))
    # the layout of the page, a, b, c on q0, q1, q2: the two SWAPs (q0, q1)
    # and (q1, q2) tie with score 1, and the tie is broken at random
    adj, dist = distances(3, line(3))
    seen = set()
    for seed in range(10):
        ops, final = swap_search(gates, [0, 1, 2], 3, adj, dist, random.Random(seed))
        assert ops[:2] == [("gate", 0, (0, 1)), ("gate", 1, (1, 2))]
        assert ops[2][0] == "swap" and ops[3][0] == "gate" and len(ops) == 4
        seen.add((ops[2][1], tuple(final)))
    assert seen == {((0, 1), (1, 0, 2)), ((1, 2), (0, 2, 1))}


def test_lookahead_example():
    # a, b, c, d = 0, 1, 2, 3 on the line q0 - q1 - q2 - q3; CNOT(a, c), then CNOT(a, d)
    gates = [("cx", (0, 2)), ("cx", (0, 3))]
    adj, dist = distances(4, line(4))
    for weight, counts in ((0.5, {2}), (0.0, {2, 3})):
        seen = set()
        for seed in range(20):
            ops, _ = swap_search(gates, [0, 1, 2, 3], 4, adj, dist, random.Random(seed), weight=weight)
            if weight == 0.5:
                assert ops[0] == ("swap", (0, 1))  # score 1 + 0.5 * 2 = 2, against 2.5 and 4
            seen.add(swap_count(ops))
        assert seen == counts
    # the forward pass ends in the layout a, b, c, d -> q1, q0, q3, q2 or
    # q2, q0, q1, q3; started from it, the circuit needs no SWAP
    ops, start, final = sabre(4, gates, 4, line(4), seed=0)
    assert swap_count(ops) == 0 == exact_swaps(4, gates, 4, line(4))


def test_gates_on_edges_in_order():
    rng = random.Random(0)
    for _ in range(150):
        kind = rng.randrange(4)
        if kind == 0:
            n_phys, edges = 6, line(6)
        elif kind == 1:
            n_phys, edges = 9, grid(3, 3)
        elif kind == 2:
            n_phys, edges = 7, star(7)
        else:
            n_phys = rng.randint(3, 10)
            edges = tree(rng, n_phys)
        n_log = rng.randint(2, n_phys)
        gates = random_circuit(rng, n_log, rng.randint(1, 40))
        ops, start, final = sabre(n_log, gates, n_phys, edges, seed=rng.randrange(10**6), trials=2)
        check_routing(gates, edges, ops, start, final)


def test_equivalence_on_all_basis_states_with_three_cnots():
    """CNOT and X circuits map basis states to basis states, so agreement on
    every basis state is equality of the unitaries. The SWAPs are expanded
    into three CNOTs, which checks that identity too."""
    rng = random.Random(1)
    for _ in range(40):
        n_phys = rng.randint(3, 6)
        edges = rng.choice([line(n_phys), star(n_phys), tree(rng, n_phys)])
        n_log = rng.randint(2, n_phys)
        gates = random_circuit(rng, n_log, rng.randint(2, 15), one_qubit=("x",))
        ops, start, final = sabre(n_log, gates, n_phys, edges, seed=2, trials=1)
        expanded = to_three_cnots(ops)
        for x in range(1 << n_log):
            want = relabel(run_logical(gates, n_log, x), n_log, n_phys, final)
            got = run_physical(gates, expanded, n_phys, start, x)
            assert got == want


def test_equivalence_of_the_unitaries_with_h_and_t():
    rng = random.Random(2)
    for _ in range(25):
        n_phys = rng.randint(3, 5)
        edges = rng.choice([line(n_phys), star(n_phys)])
        n_log = rng.randint(2, n_phys)
        gates = random_circuit(rng, n_log, rng.randint(2, 12), one_qubit=("h", "t"))
        ops, start, final = sabre(n_log, gates, n_phys, edges, seed=3, trials=1)
        for x in range(1 << n_log):  # column x of the unitary
            want = relabel(run_logical(gates, n_log, x), n_log, n_phys, final)
            got = run_physical(gates, ops, n_phys, start, x)
            assert all(abs(u - v) < 1e-9 for u, v in zip(got, want))


def test_swap_count_against_exact_optimum():
    rng = random.Random(0)
    hits, total, worst = 0, 0, 0
    for _ in range(150):
        n_phys = rng.choice([4, 5])
        edges = rng.choice([line(n_phys), star(n_phys),
                            grid(2, 2) if n_phys == 4 else [(0, 1), (1, 2), (2, 3), (3, 4), (1, 3)]])
        n_log = rng.randint(3, n_phys)
        gates = random_circuit(rng, n_log, rng.randint(5, 8))
        opt = exact_swaps(n_log, gates, n_phys, edges)
        ops, start, final = sabre(n_log, gates, n_phys, edges, seed=1)
        check_routing(gates, edges, ops, start, final)
        c = swap_count(ops)
        assert c >= opt
        hits += c == opt
        worst = max(worst, c - opt)
        total += 1
    assert (hits, total, worst) == (147, 150, 1)


def test_release_valve_bounds_the_swaps():
    rng = random.Random(4)
    for _ in range(60):
        n_phys = rng.randint(3, 9)
        edges = tree(rng, n_phys)
        n_log = rng.randint(2, n_phys)
        gates = random_circuit(rng, n_log, rng.randint(1, 30))
        g2 = sum(1 for _, qs in gates if len(qs) == 2)
        adj, dist = distances(n_phys, edges)
        start = rng.sample(range(n_phys), n_log)
        for limit in (0, 1, 3, None):
            ops, final = swap_search(gates, start, n_phys, adj, dist, random.Random(5), limit=limit)
            check_routing(gates, edges, ops, start, final)
            lim = 10 * n_phys if limit is None else limit
            assert swap_count(ops) <= g2 * (lim + n_phys - 2)
        # limit 0 is the plain walk along shortest paths
        ops, _ = swap_search(gates, start, n_phys, adj, dist, random.Random(5), limit=0)
        assert swap_count(ops) <= g2 * (n_phys - 2)


def test_reverse_traversal_lowers_the_swap_count():
    rng = random.Random(7)
    one = three = 0
    for k in range(30):
        gates = random_circuit(rng, 9, 40)
        one += swap_count(sabre(9, gates, 9, grid(3, 3), seed=k, trials=1, traversals=1)[0])
        three += swap_count(sabre(9, gates, 9, grid(3, 3), seed=k, trials=1, traversals=3)[0])
    assert three < one
