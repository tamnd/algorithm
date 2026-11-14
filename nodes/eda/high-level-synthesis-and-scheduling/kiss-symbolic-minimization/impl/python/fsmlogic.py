# SPDX-License-Identifier: MIT
# Shared helper of the hs3 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small exact two-level logic for finite state machines.

This module holds no state encoder. It gives the encoders and their tests:

- an exact multiple-valued, multiple-output two-level minimizer for tiny
  functions (all cubes, then an exact set cover by branch and bound);
- the symbolic function of a machine (present state as one multiple-valued
  input, next state as one output per state) and the encoded function of a
  machine under given codes;
- a check that a cover implements the machine;
- an exhaustive search for the best codes of a given length.

A machine is (ni, no, states, rows). A row is (inp, ps, ns, out): inp is a
string over 0, 1 and - of length ni, ps and ns are state names, and out is
a string over 0, 1 and - of length no. Rows of one present state must not
overlap in the input. Input and state pairs that no row covers are don't
cares.
"""

import itertools

# ---------------------------------------------------------------- minimizer


def _minterms(domains):
    return list(itertools.product(*[range(d) for d in domains]))


def _literals(cube, domains):
    return sum(1 for m, d in zip(cube, domains) if m != (1 << d) - 1)


def minimize(domains, on, dc):
    """Exact minimum cover; return a list of (cube, outputs).

    domains[i] is the number of values of variable i (2 for a binary one).
    on[j] and dc[j] are sets of points (tuples) for output j. The cover has
    the least number of cubes, and among those the least number of input
    literals. A cube is a tuple of nonempty value masks.
    """
    nout = len(on)
    points = _minterms(domains)
    npts = len(points)
    index = {p: i for i, p in enumerate(points)}
    # value masks: the points where variable i takes value v, as bit sets
    vmask = [[0] * d for d in domains]
    for p, i in index.items():
        for var, v in enumerate(p):
            vmask[var][v] |= 1 << i
    on_m = [sum(1 << index[p] for p in on[j]) for j in range(nout)]
    ok_m = [on_m[j] | sum(1 << index[p] for p in dc[j]) for j in range(nout)]
    sub = [[sum(vmask[var][v] for v in range(d) if m >> v & 1) for m in range(1 << d)] for var, d in enumerate(domains)]
    full = (1 << npts) - 1
    cands = []
    for cube in itertools.product(*[range(1, 1 << d) for d in domains]):
        pm = full
        for var, m in enumerate(cube):
            pm &= sub[var][m]
        outs = [j for j in range(nout) if pm & ~ok_m[j] == 0]
        cover = 0
        for j in outs:
            cover |= (pm & on_m[j]) << (j * npts)
        if cover:
            cands.append((cube, frozenset(outs), cover, _literals(cube, domains)))
    # Keep only terms that no other term dominates. A cube is dropped at
    # once if adding one value to one variable covers at least as much,
    # since that never adds a literal; the rest are compared in pairs.
    by_cube = {c[0]: c[2] for c in cands}
    pruned = []
    for c in cands:
        cube, cov = c[0], c[2]
        grown = False
        for var, m in enumerate(cube):
            for v in range(domains[var]):
                if not m >> v & 1:
                    bigger = cube[:var] + (m | 1 << v,) + cube[var + 1:]
                    if cov & ~by_cube.get(bigger, 0) == 0:
                        grown = True
                        break
            if grown:
                break
        if not grown:
            pruned.append(c)
    cands = pruned
    cands.sort(key=lambda c: (-bin(c[2]).count("1"), c[3]))
    terms = []
    for c in cands:
        if not any(c[2] & ~t[2] == 0 and t[3] <= c[3] for t in terms):
            terms.append(c)
    need = 0
    for j in range(nout):
        need |= on_m[j] << (j * npts)
    by_elem = {}
    for i, t in enumerate(terms):
        m = t[2]
        while m:
            low = m & -m
            by_elem.setdefault(low, []).append(i)
            m ^= low
    order = sorted(by_elem, key=lambda e: len(by_elem[e]))
    tmask = {e: sum(1 << i for i in by_elem[e]) for e in by_elem}
    best = [None, (len(terms) + 1, 0)]

    def lower_bound(left):
        lb = 0
        used = 0
        for e in order:
            if left & e and not used & tmask[e]:
                lb += 1
                used |= tmask[e]
        return lb

    def search(left, chosen, nlit):
        if not left:
            if (len(chosen), nlit) < best[1]:
                best[0], best[1] = list(chosen), (len(chosen), nlit)
            return
        if (len(chosen) + lower_bound(left), nlit) >= best[1]:
            return
        e = next(e for e in order if left & e)
        for i in sorted(by_elem[e], key=lambda i: (-bin(terms[i][2] & left).count("1"), terms[i][3])):
            chosen.append(i)
            search(left & ~terms[i][2], chosen, nlit + terms[i][3])
            chosen.pop()

    search(need, [], 0)
    return [(terms[i][0], terms[i][1]) for i in best[0]]


def cost(cover, domains):
    """(number of cubes, number of input literals) of a cover."""
    return len(cover), sum(_literals(c, domains) for c, _ in cover)


# ---------------------------------------------------------------- machines


def _bits_match(cube, bits):
    return all(c == "-" or int(c) == b for c, b in zip(cube, bits))


def _lookup(fsm, bits, s):
    ni, no, states, rows = fsm
    for inp, ps, ns, out in rows:
        if ps == s and _bits_match(inp, bits):
            return ns, out
    return None


def symbolic_function(fsm):
    """Domains, on and dc of the symbolic function.

    Variables: the ni inputs, then the present state with len(states)
    values. Outputs: one per next state (one-hot), then the no outputs.
    """
    ni, no, states, rows = fsm
    n = len(states)
    domains = [2] * ni + [n]
    on = [set() for _ in range(n + no)]
    dc = [set() for _ in range(n + no)]
    for p in _minterms(domains):
        hit = _lookup(fsm, p[:ni], states[p[ni]])
        for j in range(n + no):
            if hit is None:
                dc[j].add(p)
            elif j < n:
                if states[j] == hit[0]:
                    on[j].add(p)
            else:
                c = hit[1][j - n]
                if c == "1":
                    on[j].add(p)
                elif c == "-":
                    dc[j].add(p)
    return domains, on, dc


def encoded_function(fsm, codes, k):
    """Domains, on and dc of the machine under codes (state -> int of k bits).

    Variables: the ni inputs, then the k state bits, most significant
    first. Outputs: the k next state bits, then the no outputs. Codes that
    no state uses are don't cares.
    """
    ni, no, states, rows = fsm
    by_code = {codes[s]: s for s in states}
    domains = [2] * (ni + k)
    on = [set() for _ in range(k + no)]
    dc = [set() for _ in range(k + no)]
    for p in _minterms(domains):
        code = int("".join(map(str, p[ni:])), 2) if k else 0
        s = by_code.get(code)
        hit = None if s is None else _lookup(fsm, p[:ni], s)
        for j in range(k + no):
            if hit is None:
                dc[j].add(p)
            elif j < k:
                if codes[hit[0]] >> (k - 1 - j) & 1:
                    on[j].add(p)
            else:
                c = hit[1][j - k]
                if c == "1":
                    on[j].add(p)
                elif c == "-":
                    dc[j].add(p)
    return domains, on, dc


def encoded_cost(fsm, codes, k):
    domains, on, dc = encoded_function(fsm, codes, k)
    return cost(minimize(domains, on, dc), domains)


def implements(fsm, codes, k, cover):
    """Does the two-level cover give the right next state and outputs?

    It checks every input and state pair that some row specifies.
    """
    ni, no, states, rows = fsm
    for s in states:
        for bits in itertools.product((0, 1), repeat=ni):
            hit = _lookup(fsm, bits, s)
            if hit is None:
                continue
            p = tuple(bits) + tuple(codes[s] >> (k - 1 - b) & 1 for b in range(k))
            val = [0] * (k + no)
            for cube, outs in cover:
                if all(m >> v & 1 for m, v in zip(cube, p)):
                    for j in outs:
                        val[j] = 1
            if val[:k] != [codes[hit[0]] >> (k - 1 - b) & 1 for b in range(k)]:
                return False
            for j, c in enumerate(hit[1]):
                if c != "-" and val[k + j] != int(c):
                    return False
    return True


_CODES = {}


def all_codes(n, k):
    """Every injective code of n states in k bits, one per class of bit permutations.

    Permuting the bits of all codes permutes the state variables and the
    next state outputs, so the cost does not change. Complementing a bit
    can change it, so those classes stay apart.
    """
    if (n, k) not in _CODES:
        seen = set()
        keep = []
        perms = list(itertools.permutations(range(k)))
        for codes in itertools.permutations(range(1 << k), n):
            key = min(tuple(sum((c >> perm[b] & 1) << b for b in range(k)) for c in codes) for perm in perms)
            if key not in seen:
                seen.add(key)
                keep.append(codes)
        _CODES[(n, k)] = keep
    return list(_CODES[(n, k)])


def exhaustive_best(fsm, k):
    """Return (best cost, list of cost of every class) over all codes of length k."""
    ni, no, states, rows = fsm
    costs = []
    for codes in all_codes(len(states), k):
        costs.append(encoded_cost(fsm, dict(zip(states, codes)), k))
    return min(costs), costs
