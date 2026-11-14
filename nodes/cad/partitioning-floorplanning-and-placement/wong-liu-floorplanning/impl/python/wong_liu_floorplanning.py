# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wong-liu-floorplanning/. The authors are listed in prov/0Y56MN.jsonl.

"""Wong and Liu's floorplanning by annealing over normalized Polish expressions.

Tokens are block ids (ints) and the operators "V" (first part to the left of
the second) and "H" (first part below the second). The cost of a word is
area + lam * HPWL, where the area is the least area over the allowed shapes of
the blocks (computed with Stockmeyer's merge of shape fronts) and HPWL is the
half-perimeter wire length of the nets over the centres of the blocks.
"""

import math
import random
from fractions import Fraction
from typing import Callable, Optional


def is_op(t) -> bool:
    """Return True for the operators "H" and "V"."""
    return t == "H" or t == "V"


def is_normalized(e: list) -> bool:
    """Return True if e is a normalized Polish expression."""
    c = 0
    for k, t in enumerate(e):
        if is_op(t):
            c -= 1
            if c < 1 or e[k - 1] == t:
                return False
        else:
            c += 1
    ops = [t for t in e if not is_op(t)]
    return c == 1 and len(set(ops)) == len(ops)


# ----------------------------------------------------------------- the moves


def move_m1(e: list, rng: random.Random) -> list:
    """M1: swap two operands that are next to each other in the operand order."""
    pos = [k for k, t in enumerate(e) if not is_op(t)]
    if len(pos) < 2:
        return list(e)
    a = rng.randrange(len(pos) - 1)
    f = list(e)
    i, j = pos[a], pos[a + 1]
    f[i], f[j] = f[j], f[i]
    return f


def chains(e: list) -> list[tuple[int, int]]:
    """Return the maximal runs of operators as half-open index ranges."""
    out = []
    k = 0
    while k < len(e):
        if is_op(e[k]):
            s = k
            while k < len(e) and is_op(e[k]):
                k += 1
            out.append((s, k))
        else:
            k += 1
    return out


def move_m2(e: list, rng: random.Random) -> list:
    """M2: complement one chain of operators (H becomes V and V becomes H)."""
    cs = chains(e)
    if not cs:
        return list(e)
    s, t = cs[rng.randrange(len(cs))]
    f = list(e)
    for k in range(s, t):
        f[k] = "V" if f[k] == "H" else "H"
    return f


def m3_ok(e: list, i: int, prefix_ops: list[int]) -> bool:
    """Tell whether swapping e[i] and e[i + 1] (an operand and an operator) keeps e normalized.

    prefix_ops[k] is the number of operators in e[0 .. k - 1]. The test takes
    O(1) time.
    """
    a, b = e[i], e[i + 1]
    if is_op(a) == is_op(b):
        return False
    if not is_op(a):
        # The operand moves right, the operator b moves to position i. The
        # prefix e[0 .. i] then has prefix_ops[i] + 1 operators and i - prefix_ops[i]
        # operands; balloting needs more operands than operators.
        if 2 * (prefix_ops[i] + 1) >= i + 1:
            return False
        return i == 0 or e[i - 1] != b
    # The operator a moves right, to position i + 1; its new right neighbour is e[i + 2].
    return i + 2 >= len(e) or e[i + 2] != a


def move_m3(e: list, rng: random.Random, tries: int = 50) -> list:
    """M3: swap a neighbouring operand and operator if the word stays normalized."""
    if len(e) < 3:
        return list(e)
    prefix = [0]
    for t in e:
        prefix.append(prefix[-1] + (1 if is_op(t) else 0))
    for _ in range(tries):
        i = rng.randrange(len(e) - 1)
        if m3_ok(e, i, prefix):
            f = list(e)
            f[i], f[i + 1] = f[i + 1], f[i]
            return f
    return list(e)


# ------------------------------------------------------------------ the cost


def _front(shapes: list[tuple[int, int]]) -> list:
    out: list = []
    for k in sorted(range(len(shapes)), key=lambda q: shapes[q]):
        w, h = shapes[k]
        if not out or h < out[-1][1]:
            out.append((w, h, k))
    return out


def _merge(a: list, b: list, vertical: bool) -> list:
    if not vertical:  # exchange the coordinates and use the vertical merge
        ta = [(h, w, k) for (w, h, k) in reversed(a)]
        tb = [(h, w, k) for (w, h, k) in reversed(b)]
        res = _merge(ta, tb, True)
        na, nb = len(a), len(b)
        return [(w, h, (na - 1 - i, nb - 1 - j)) for (h, w, (i, j)) in reversed(res)]
    i = j = 0
    out = []
    while True:
        out.append((a[i][0] + b[j][0], max(a[i][1], b[j][1]), (i, j)))
        if a[i][1] > b[j][1]:
            if i == len(a) - 1:
                return out
            i += 1
        elif b[j][1] > a[i][1]:
            if j == len(b) - 1:
                return out
            j += 1
        else:
            if i == len(a) - 1 or j == len(b) - 1:
                return out
            i, j = i + 1, j + 1


def realize(e: list, shapes: dict) -> tuple[int, dict]:
    """Return the least area of e over the allowed shapes and a placement that reaches it.

    The placement maps each block to (x, y, w, h).
    """
    st: list = []
    for t in e:
        if is_op(t):
            b, a = st.pop(), st.pop()
            st.append([t, _merge(a[1], b[1], t == "V"), a, b])
        else:
            st.append([t, _front(shapes[t])])
    root = st[0]
    fr = root[1]
    best = min(range(len(fr)), key=lambda k: (fr[k][0] * fr[k][1], fr[k][0]))
    place: dict = {}
    todo = [(root, best, 0, 0)]
    while todo:
        node, k, x, y = todo.pop()
        w, h, back = node[1][k]
        if len(node) == 2:
            place[node[0]] = (x, y, w, h)
            continue
        i, j = back
        a, b = node[2], node[3]
        todo.append((a, i, x, y))
        if node[0] == "V":
            todo.append((b, j, x + a[1][i][0], y))
        else:
            todo.append((b, j, x, y + a[1][i][1]))
    return fr[best][0] * fr[best][1], place


def cost(e: list, shapes: dict, nets: list, lam: Fraction) -> Fraction:
    """Return area + lam * HPWL over the block centres, as an exact fraction."""
    area, place = realize(e, shapes)
    if not nets or lam == 0:
        return Fraction(area)
    wl2 = 0  # twice the HPWL, so that the centres are integers
    for net in nets:
        xs = [2 * place[b][0] + place[b][2] for b in net]
        ys = [2 * place[b][1] + place[b][3] for b in net]
        wl2 += max(xs) - min(xs) + max(ys) - min(ys)
    return Fraction(area) + lam * Fraction(wl2, 2)


# ------------------------------------------------------------- the annealing


def wong_liu_floorplan(
    shapes: dict[int, list[tuple[int, int]]],
    rng: random.Random,
    nets: Optional[list[list[int]]] = None,
    lam: Fraction = Fraction(0),
    r: float = 0.85,
    k: int = 10,
    p0: float = 0.9,
    eps: float = 1e-3,
    max_temps: int = 200,
    on_state: Optional[Callable[[list], None]] = None,
) -> tuple[list, Fraction]:
    """Anneal over normalized Polish expressions and return (best word, its cost).

    r is the cooling ratio, N = k n is the number of uphill moves per
    temperature, p0 is the probability to accept an average uphill move at the
    start. on_state, if given, is called with each word the search moves to.
    """
    nets = nets or []
    blocks = sorted(shapes)
    n = len(blocks)
    e = [blocks[0]]  # @line L1
    for b in blocks[1:]:
        e += [b, "V"]
    cur = cost(e, shapes, nets, lam)
    best, best_cost = list(e), cur
    if n == 1:
        return best, best_cost
    moves = (move_m1, move_m2, move_m3)
    ups = []  # @line L2
    for _ in range(4 * n):
        d = cost(rng.choice(moves)(e, rng), shapes, nets, lam) - cur
        if d > 0:
            ups.append(d)
    t = float(sum(ups) / len(ups)) / -math.log(p0) if ups else 1.0
    big_n = k * n
    for _ in range(max_temps):  # @line L3
        tries = uphill = rejects = 0  # @line L4
        while True:  # @line L5
            f = rng.choice(moves)(e, rng)  # @line L6
            tries += 1  # @line L7
            fc = cost(f, shapes, nets, lam)
            d = fc - cur
            if d <= 0 or rng.random() < math.exp(-float(d) / t):  # @line L8
                if d > 0:  # @line L9
                    uphill += 1
                e, cur = f, fc  # @line L10
                if on_state is not None:
                    on_state(e)
                if cur < best_cost:
                    best, best_cost = list(e), cur
            else:  # @line L11
                rejects += 1
            if uphill > big_n or tries > 2 * big_n:  # @line L12
                break
        t *= r  # @line L13
        if rejects / tries > 0.95 or t < eps:  # @line L14
            break
    return best, best_cost  # @line L15
