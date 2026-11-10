# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-u-turn-sampler/. The authors are listed in prov/1360ZZ.jsonl.

import math
import random
from typing import Callable, Sequence

Vec = list
Point = tuple[float, ...]
DELTA_MAX = 1000.0


def _leapfrog(grad, q: Vec, p: Vec, eps: float) -> tuple[Vec, Vec]:
    g = grad(q)
    p = [a + eps / 2 * b for a, b in zip(p, g)]
    q = [a + eps * b for a, b in zip(q, p)]
    g = grad(q)
    p = [a + eps / 2 * b for a, b in zip(p, g)]
    return q, p


def _no_u_turn(q_minus: Vec, p_minus: Vec, q_plus: Vec, p_plus: Vec) -> bool:
    """True while neither end moves back toward the other: (q+ - q-).p- >= 0 and (q+ - q-).p+ >= 0."""
    dq = [a - b for a, b in zip(q_plus, q_minus)]
    return sum(a * b for a, b in zip(dq, p_minus)) >= 0 and sum(a * b for a, b in zip(dq, p_plus)) >= 0


def _neg_h(log_target, q: Vec, p: Vec) -> float:
    return log_target(q) - sum(v * v for v in p) / 2


def _build_tree(log_target, grad, q, p, log_u, v, j, eps, rng):
    """Build a subtree of 2^j leapfrog steps in direction v.

    Returns (q-, p-, q+, p+, q', n', s'): the two ends, a state drawn uniformly from the
    n' states of the subtree that lie in the slice, and s' = 0 if a U-turn or a divergence
    happened inside the subtree.
    """
    if j == 0:  # @line L15
        q1, p1 = _leapfrog(grad, q, p, v * eps)  # @line L16
        nh = _neg_h(log_target, q1, p1)
        n1 = int(log_u <= nh)  # @line L17
        s1 = int(log_u < nh + DELTA_MAX)
        return q1, p1, q1, p1, q1, n1, s1  # @line L18
    qm, pm, qp, pp, q1, n1, s1 = _build_tree(log_target, grad, q, p, log_u, v, j - 1, eps, rng)  # @line L19
    if s1 == 1:  # @line L20
        if v == -1:  # @line L21
            qm, pm, _, _, q2, n2, s2 = _build_tree(log_target, grad, qm, pm, log_u, v, j - 1, eps, rng)
        else:  # @line L22
            _, _, qp, pp, q2, n2, s2 = _build_tree(log_target, grad, qp, pp, log_u, v, j - 1, eps, rng)
        if n1 + n2 > 0 and rng.random() < n2 / (n1 + n2):  # @line L23
            q1 = q2
        s1 = s2 * int(_no_u_turn(qm, pm, qp, pp))  # @line L24
        n1 = n1 + n2  # @line L25
    return qm, pm, qp, pp, q1, n1, s1  # @line L26


def no_u_turn_sampler(
    log_target: Callable[[Sequence[float]], float],
    grad_log_target: Callable[[Sequence[float]], Sequence[float]],
    x0: Sequence[float],
    eps: float,
    n_steps: int,
    rng: random.Random,
    max_depth: int = 10,
) -> tuple[list[Point], list[int]]:
    """Efficient No-U-Turn sampler (Hoffman and Gelman 2014, Algorithm 3) with a fixed step size.

    Returns (chain X_1..X_T, tree depth used at each iteration).
    One iteration uses at most 2^max_depth leapfrog steps.
    """
    if eps <= 0 or max_depth < 1:
        raise ValueError("eps must be positive and max_depth at least 1")
    q = [float(v) for v in x0]  # @line L1
    if log_target(q) == -math.inf:
        raise ValueError("x0 must be in the support of the target")
    chain: list[Point] = []
    depths: list[int] = []
    for _ in range(n_steps):  # @line L2
        p = [rng.gauss(0.0, 1.0) for _ in q]  # @line L3
        log_u = _neg_h(log_target, q, p) + math.log(1.0 - rng.random())
        qm, pm, qp, pp = q, p, q, p  # @line L4
        n, s, j, q_new = 1, 1, 0, q
        while s == 1 and j < max_depth:  # @line L5
            v = rng.choice((-1, 1))  # @line L6
            if v == -1:  # @line L7
                qm, pm, _, _, q1, n1, s1 = _build_tree(log_target, grad_log_target, qm, pm, log_u, v, j, eps, rng)
            else:  # @line L8
                _, _, qp, pp, q1, n1, s1 = _build_tree(log_target, grad_log_target, qp, pp, log_u, v, j, eps, rng)
            if s1 == 1 and rng.random() < n1 / n:  # @line L9
                q_new = q1
            n += n1  # @line L10
            s = s1 * int(_no_u_turn(qm, pm, qp, pp))  # @line L11
            j += 1  # @line L12
        q = q_new  # @line L13
        chain.append(tuple(q))
        depths.append(j)
    return chain, depths  # @line L14


def naive_tree(
    log_target: Callable[[Sequence[float]], float],
    grad_log_target: Callable[[Sequence[float]], Sequence[float]],
    q: Sequence[float],
    p: Sequence[float],
    log_u: float,
    eps: float,
    directions: Sequence[int],
    max_depth: int = 10,
) -> tuple[dict[int, tuple[Vec, Vec]], set[int], int]:
    """Build the NUTS trajectory from (q, p) with the given direction sequence, without sampling.

    Returns (states, candidates, depth): states maps an index i (0 is the start, negative is
    backward in time) to (q_i, p_i); candidates is the set C of indices that NUTS chooses from.
    It checks the same U-turn and divergence conditions as no_u_turn_sampler.
    """
    states = {0: (list(q), list(p))}
    cand = {0} if log_u <= _neg_h(log_target, q, p) else set()
    lo = hi = 0
    j = 0
    while j < max_depth:
        v = directions[j]
        size = 2**j
        new = {}
        if v == 1:
            idx = range(hi + 1, hi + 1 + size)
            prev = hi
        else:
            idx = range(lo - 1, lo - 1 - size, -1)
            prev = lo
        ok = True
        cq, cp = states[prev]
        for i in idx:
            cq, cp = _leapfrog(grad_log_target, cq, cp, v * eps)
            new[i] = (cq, cp)
            if not log_u < _neg_h(log_target, cq, cp) + DELTA_MAX:
                ok = False
        block = sorted(new)
        # every dyadic sub-block of the new half (size >= 2) must pass the U-turn test
        b = 2
        while ok and b <= size:
            for a in range(0, size, b):
                first, last = block[a], block[a + b - 1]
                if not _no_u_turn(new[first][0], new[first][1], new[last][0], new[last][1]):
                    ok = False
                    break
            b *= 2
        if not ok:
            # the new half is excluded and the run stops; the excluded states are still recorded
            states.update(new)
            return states, cand, j + 1
        states.update(new)
        cand |= {i for i in new if log_u <= _neg_h(log_target, *new[i])}
        lo, hi = min(states), max(states)
        j += 1
        if not _no_u_turn(states[lo][0], states[lo][1], states[hi][0], states[hi][1]):
            break
    return states, cand, j
