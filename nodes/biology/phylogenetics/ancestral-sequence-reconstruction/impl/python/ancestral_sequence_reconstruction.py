# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ancestral-sequence-reconstruction/. The authors are listed in prov/GHTCE8.jsonl.
"""Ancestral sequence reconstruction on a fixed rooted tree.

joint_reconstruction is the dynamic program of Pupko, Pe'er, Shamir and Graur
(2000): the most probable assignment of states to all internal nodes at once.
marginal_reconstruction gives, for each internal node, the posterior of its
state given the leaves (an upward pruning pass and a downward pass).

A tree is (children, root): children maps each internal node to its list of
children. P maps each non-root node c to the transition matrix of the branch
above c, pi is the root distribution, and a site maps each leaf to a state in
range(k). The code uses only +, *, / and comparisons, so Fraction entries
give exact results.
"""

from __future__ import annotations

from typing import Dict, Hashable, List, Mapping, Sequence, Tuple

Node = Hashable


def _postorder(children: Mapping[Node, Sequence[Node]], root: Node) -> List[Node]:
    order: List[Node] = []
    stack = [root]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(children.get(v, ()))
    order.reverse()
    return order


def joint_reconstruction(children: Mapping[Node, Sequence[Node]], root: Node,
                         P: Mapping[Node, Sequence[Sequence]], pi: Sequence,
                         site: Mapping[Node, int]) -> Tuple[object, Dict[Node, int]]:
    """Pupko et al. (2000): return (max joint probability, states of the internal nodes).

    For a non-root node c and a parent state i, Lc[i] is the largest probability
    of the data below c over all states of the internal nodes below and at c,
    given state i at the parent; Cc[i] is the state of c that attains it.
    """
    k = len(pi)
    order = _postorder(children, root)
    Lm: Dict[Node, List] = {}
    Cm: Dict[Node, List[int]] = {}
    for c in order:
        if c == root:
            break
        kids = children.get(c, ())
        if not kids:
            x = site[c]
            Lm[c] = [P[c][i][x] for i in range(k)]
            Cm[c] = [x] * k
            continue
        below = []
        for j in range(k):
            prod = P[c][0][0] - P[c][0][0] + 1
            for d in kids:
                prod *= Lm[d][j]
            below.append(prod)
        Lc, Cc = [], []
        for i in range(k):
            best_j = 0
            best = P[c][i][0] * below[0]
            for j in range(1, k):
                val = P[c][i][j] * below[j]
                if val > best:
                    best, best_j = val, j
            Lc.append(best)
            Cc.append(best_j)
        Lm[c], Cm[c] = Lc, Cc
    best_state, best = 0, None
    for a in range(k):
        val = pi[a]
        for d in children[root]:
            val *= Lm[d][a]
        if best is None or val > best:
            best, best_state = val, a
    states = {root: best_state}
    stack = [root]
    while stack:
        v = stack.pop()
        for c in children.get(v, ()):
            if children.get(c):
                states[c] = Cm[c][states[v]]
                stack.append(c)
    return best, states


def marginal_posteriors(children: Mapping[Node, Sequence[Node]], root: Node,
                        P: Mapping[Node, Sequence[Sequence]], pi: Sequence,
                        site: Mapping[Node, int]) -> Dict[Node, List]:
    """Posterior Pr(state a at v | leaves) for every internal node v."""
    k = len(pi)
    one = pi[0] - pi[0] + 1
    zero = one - one
    order = _postorder(children, root)
    # Upward pass: L[v][a] = Pr(leaves below v | a at v); M[c][a] = message from c to its parent.
    L: Dict[Node, List] = {}
    M: Dict[Node, List] = {}
    for v in order:
        kids = children.get(v, ())
        if not kids:
            L[v] = [one if a == site[v] else zero for a in range(k)]
        else:
            vec = [one] * k
            for c in kids:
                for a in range(k):
                    vec[a] *= M[c][a]
            L[v] = vec
        if v != root:
            M[v] = [sum((P[v][a][b] * L[v][b] for b in range(k)), zero) for a in range(k)]
    # Downward pass: O[v][a] = Pr(leaves outside the subtree of v, a at v).
    O: Dict[Node, List] = {root: list(pi)}
    stack = [root]
    while stack:
        v = stack.pop()
        kids = children.get(v, ())
        for c in kids:
            up = list(O[v])
            for s in kids:
                if s != c:
                    for a in range(k):
                        up[a] *= M[s][a]
            O[c] = [sum((up[a] * P[c][a][b] for a in range(k)), zero) for b in range(k)]
            stack.append(c)
    post: Dict[Node, List] = {}
    for v in order:
        if children.get(v):
            joint = [O[v][a] * L[v][a] for a in range(k)]
            total = sum(joint, zero)
            post[v] = [x / total for x in joint]
    return post


def marginal_reconstruction(children: Mapping[Node, Sequence[Node]], root: Node,
                            P: Mapping[Node, Sequence[Sequence]], pi: Sequence,
                            site: Mapping[Node, int]) -> Dict[Node, int]:
    """For each internal node, the state of largest posterior (lowest index on ties)."""
    post = marginal_posteriors(children, root, P, pi, site)
    return {v: max(range(len(pi)), key=lambda a: (p[a], -a)) for v, p in post.items()}


def reconstruct_sequences(children: Mapping[Node, Sequence[Node]], root: Node,
                          P: Mapping[Node, Sequence[Sequence]], pi: Sequence,
                          alignment: Mapping[Node, Sequence[int]], joint: bool = True) -> Dict[Node, List[int]]:
    """Apply the joint (or marginal) reconstruction to each site of an alignment."""
    m = len(next(iter(alignment.values())))
    result: Dict[Node, List[int]] = {}
    for j in range(m):
        site = {v: seq[j] for v, seq in alignment.items()}
        if joint:
            states = joint_reconstruction(children, root, P, pi, site)[1]
        else:
            states = marginal_reconstruction(children, root, P, pi, site)
        for v, a in states.items():
            result.setdefault(v, []).append(a)
    return result
