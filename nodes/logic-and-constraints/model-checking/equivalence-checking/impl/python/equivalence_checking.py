# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/equivalence-checking/. The authors are listed in prov/N16FPV.jsonl.

"""Behavioural equivalence checking on finite labelled transition systems.

A system has the states 0 .. n-1, a list trans of (s, a, t) triples, and an
optional list labels with one state label each (default: all equal). The
module gives a fast and a naive version of each check, so that the tests
can compare them:

  bisimilarity           partition refinement (Kanellakis and Smolka)  / greatest fixed point
  similarity             removal sets (Henzinger, Henzinger, Kopke)    / greatest fixed point
  trace equivalence      subset construction on pairs                  / bounded trace sets
  stuttering equivalence block splitting (Groote and Vaandrager)       / greatest fixed point
"""

from collections import defaultdict
from typing import Dict, List, Optional, Sequence, Set, Tuple

Trans = Sequence[Tuple[int, str, int]]


def _post(n: int, trans: Trans) -> Dict[str, List[Set[int]]]:
    post: Dict[str, List[Set[int]]] = {}
    for s, a, t in trans:
        post.setdefault(a, [set() for _ in range(n)])[s].add(t)
    return post


def _labels(n: int, labels: Optional[Sequence]) -> List:
    return list(labels) if labels is not None else [0] * n


# Bisimilarity

def bisim_partition(n: int, trans: Trans, labels=None) -> List[int]:
    """Block number of each state in the coarsest stable partition.

    Start from the label partition. In each round, give each state a
    signature: its block and, for each action a, the set of blocks that its
    a-successors lie in. States with equal signatures stay together. When a
    round makes no new block, the partition is stable. There are at most n
    rounds of O(n + m) hashed work each, so the time is O(n (n + m)), the
    bound of the Kanellakis and Smolka method.
    """
    lab = _labels(n, labels)
    post = _post(n, trans)
    ids = {l: i for i, l in enumerate(dict.fromkeys(lab))}
    block = [ids[l] for l in lab]
    while True:
        # Signature: own block, and for each action the set of blocks reached.
        sig = [(block[s],) + tuple(frozenset(block[t] for t in post[a][s]) for a in sorted(post)) for s in range(n)]
        ids = {}
        new = [ids.setdefault(x, len(ids)) for x in sig]
        if len(ids) == len(set(block)):
            return new
        block = new


def bisim_naive(n: int, trans: Trans, labels=None) -> Set[Tuple[int, int]]:
    """The greatest bisimulation, by deleting bad pairs from all label-equal pairs."""
    lab = _labels(n, labels)
    post = _post(n, trans)
    rel = {(s, t) for s in range(n) for t in range(n) if lab[s] == lab[t]}

    def ok(s, t):
        for a in post:
            for s2 in post[a][s]:
                if not any((s2, t2) in rel for t2 in post[a][t]):
                    return False
        return True

    changed = True
    while changed:
        bad = {(s, t) for s, t in rel if not ok(s, t) or not ok(t, s)}
        changed = bool(bad)
        rel -= bad
    return rel


# Similarity

def simulators(n: int, trans: Trans, labels=None) -> List[Set[int]]:
    """sim[v] = the set of states u that simulate v (v is below u).

    Each removal of w from sim[u] puts the b-predecessors of w that lose their
    last b-successor in sim[u] into remove[b][u]. Every pair leaves sim at
    most once.
    """
    lab = _labels(n, labels)
    post = _post(n, trans)
    pre: Dict[str, List[Set[int]]] = {a: [set() for _ in range(n)] for a in post}
    for s, a, t in trans:
        pre[a][t].add(s)
    acts = sorted(post)
    sim = [{u for u in range(n) if lab[u] == lab[v] and all(post[a][u] or not post[a][v] for a in acts)} for v in range(n)]
    remove = {a: [set(range(n)) - {w for x in sim[v] for w in pre[a][x]} for v in range(n)] for a in acts}
    work = [(a, v) for a in acts for v in range(n) if remove[a][v]]
    while work:
        a, v = work.pop()
        rem, remove[a][v] = remove[a][v], set()
        for u in pre[a][v]:
            for w in rem:
                if w in sim[u]:
                    sim[u].discard(w)
                    for b in acts:
                        for x in pre[b][w]:
                            if x not in remove[b][u] and not (post[b][x] & sim[u]):
                                if not remove[b][u]:
                                    work.append((b, u))
                                remove[b][u].add(x)
    return sim


def simulation_naive(n: int, trans: Trans, labels=None) -> Set[Tuple[int, int]]:
    """Pairs (v, u) with u simulating v, by the greatest fixed point."""
    lab = _labels(n, labels)
    post = _post(n, trans)
    rel = {(v, u) for v in range(n) for u in range(n) if lab[v] == lab[u]}
    changed = True
    while changed:
        bad = {(v, u) for v, u in rel if any(not any((v2, u2) in rel for u2 in post[a][u]) for a in post for v2 in post[a][v])}
        changed = bool(bad)
        rel -= bad
    return rel


# Trace equivalence

def trace_equivalent(n: int, trans: Trans, s: int, t: int) -> Optional[Tuple[str, ...]]:
    """None if s and t have the same traces, else a shortest trace of one but not the other.

    Search the pairs (X, Y) of state sets that the subset construction
    reaches from ({s}, {t}). There are at most 4^n pairs: trace inclusion is
    PSPACE-complete, so an exponential worst case is expected.
    """
    post = _post(n, trans)
    start = (frozenset([s]), frozenset([t]))
    parent = {start: None}
    queue = [start]
    for x, y in queue:
        if bool(x) != bool(y):
            word = []
            node = (x, y)
            while parent[node] is not None:
                node, a = parent[node]
                word.append(a)
            return tuple(word[::-1])
        if not x:
            continue
        for a in sorted(post):
            nxt = (frozenset(v for u in x for v in post[a][u]), frozenset(v for u in y for v in post[a][u]))
            if nxt not in parent:
                parent[nxt] = ((x, y), a)
                queue.append(nxt)
    return None


def traces(n: int, trans: Trans, s: int, k: int) -> Set[Tuple[str, ...]]:
    """All traces of s of length at most k, by direct enumeration."""
    post = _post(n, trans)
    out = {()}
    layer = {((), s)}
    for _ in range(k):
        layer = {(w + (a,), t) for w, u in layer for a in post for t in post[a][u]}
        out |= {w for w, _ in layer}
    return out


# Stuttering equivalence (divergence-blind, on Kripke structures)

def stutter_partition(n: int, succ: Sequence[Sequence[int]], labels: Sequence) -> List[int]:
    """Block number of each state for divergence-blind stuttering equivalence.

    A block B is split by a block C (C not B) into the states that can reach
    a state with a successor in C by a path that stays in B, and the rest.
    At most n - 1 splits happen. Groote and Vaandrager organize the search
    so that each split costs O(m), for O(n m) in total. This short version
    tries every pair of blocks in each round, so it is slower, but it gives
    the same partition.
    """
    pred = [[] for _ in range(n)]
    for s in range(n):
        for t in succ[s]:
            pred[t].append(s)
    ids = {l: i for i, l in enumerate(dict.fromkeys(labels))}
    block = [ids[l] for l in labels]
    nblocks = len(ids)
    changed = True
    while changed:
        changed = False
        for c in range(nblocks):
            for b in range(nblocks):
                if b == c:
                    continue
                pos = {s for s in range(n) if block[s] == b and any(block[t] == c for t in succ[s])}
                stack = list(pos)
                while stack:
                    t = stack.pop()
                    for s in pred[t]:
                        if block[s] == b and s not in pos:
                            pos.add(s)
                            stack.append(s)
                size = sum(1 for s in range(n) if block[s] == b)
                if pos and len(pos) < size:
                    for s in pos:
                        block[s] = nblocks
                    nblocks += 1
                    changed = True
    return block


def stutter_naive(n: int, succ: Sequence[Sequence[int]], labels: Sequence) -> Set[Tuple[int, int]]:
    """The greatest divergence-blind stuttering bisimulation, by deleting bad pairs."""
    rel = {(s, t) for s in range(n) for t in range(n) if labels[s] == labels[t]}

    def ok(s, t):
        for s2 in succ[s]:
            if (s2, t) in rel:
                continue
            # Walk from t through states related to s, then take one step to a match of s2.
            seen, stack, found = {t}, [t], False
            while stack and not found:
                u = stack.pop()
                for v in succ[u]:
                    if (s2, v) in rel:
                        found = True
                        break
                    if (s, v) in rel and v not in seen:
                        seen.add(v)
                        stack.append(v)
            if not found:
                return False
        return True

    changed = True
    while changed:
        bad = {(s, t) for s, t in rel if not ok(s, t) or not ok(t, s)}
        changed = bool(bad)
        rel -= bad
    return rel


def same_blocks(block: Sequence[int]) -> Set[Tuple[int, int]]:
    groups = defaultdict(list)
    for s, b in enumerate(block):
        groups[b].append(s)
    return {(s, t) for g in groups.values() for s in g for t in g}
