# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phonetic-decision-tree-state-tying/. The authors are listed in prov/7CSFNE.jsonl.

"""Phonetic decision tree state tying (Young, Odell and Woodland 1994).

The input is the set of triphone states that share one base phone and one state
position, for example state 2 of every triphone of the phone "ae". Each state s
has a context (left phone, right phone) and the statistics of its frames: the
occupancy N_s (a frame count, or a sum of state posteriors), the mean mu_s and
the diagonal variance var_s, each a list of d numbers.

The log likelihood of the frames of a set S under one diagonal Gaussian fitted
to them by maximum likelihood is, with log the natural log,

    L(S) = -(1/2) N(S) (d log(2 pi) + sum_k log var_k(S) + d),

and it needs only the pooled statistics, not the frames. A question asks whether
the left (or the right) context phone is in a set of phones. The tree splits
leaves greedily by the question with the largest gain
L(S_yes) + L(S_no) - L(S), and stops when no split gains at least the threshold
with at least min_occ frames on each side. A merge stage then joins pairs of
leaves while the loss of likelihood stays below the threshold.
"""

import math
from typing import Dict, List, Optional, Sequence, Tuple

LOG_2PI = math.log(2 * math.pi)


class State:
    """One context-dependent state: its context and its frame statistics."""

    def __init__(self, name, left, right, occ, mean, var):
        self.name, self.left, self.right = name, left, right
        self.occ, self.mean, self.var = float(occ), list(mean), list(var)

    def __repr__(self):
        return "State(%r)" % (self.name,)


def stats_from_frames(frames: Sequence[Sequence[float]]):
    """Return (N, mean, var) of a list of frames, with the variance divided by N."""
    n = len(frames)
    d = len(frames[0])
    mean = [math.fsum(f[k] for f in frames) / n for k in range(d)]
    var = [math.fsum((f[k] - mean[k]) ** 2 for f in frames) / n for k in range(d)]
    return n, mean, var


def pool(states: Sequence[State], var_floor: float = 0.0):
    """Return the pooled (N, mean, var) of a set of states, from their statistics only.

    N = sum N_s, mean = sum N_s mu_s / N, var_k = sum N_s (var_sk + mu_sk^2) / N - mean_k^2.
    The variance is floored at var_floor.
    """
    N = math.fsum(s.occ for s in states)
    d = len(states[0].mean)
    mean = [math.fsum(s.occ * s.mean[k] for s in states) / N for k in range(d)]
    var = []
    for k in range(d):
        second = math.fsum(s.occ * (s.var[k] + s.mean[k] ** 2) for s in states) / N
        var.append(max(second - mean[k] ** 2, var_floor))
    return N, mean, var


def log_likelihood(states: Sequence[State], var_floor: float = 1e-6) -> float:
    """L(S): the log likelihood of the frames of S under one ML diagonal Gaussian."""
    if not states:
        return 0.0
    N, _, var = pool(states, var_floor)
    d = len(var)
    return -0.5 * N * (d * LOG_2PI + math.fsum(math.log(v) for v in var) + d)


def answer(question, state: State) -> bool:
    """A question is (name, side, phones) with side "L" or "R"."""
    _, side, phones = question
    return (state.left if side == "L" else state.right) in phones


def split(states, question):
    yes = [s for s in states if answer(question, s)]
    no = [s for s in states if not answer(question, s)]
    return yes, no


def best_question(states, questions, min_occ: float, var_floor: float = 1e-6):
    """Return (gain, question, yes, no) of the best allowed split, or None.

    A split is allowed if both sides have an occupancy of at least min_occ.
    Ties go to the first question in the list.
    """
    base = log_likelihood(states, var_floor)
    best = None
    for q in questions:
        yes, no = split(states, q)
        if not yes or not no:
            continue
        if sum(s.occ for s in yes) < min_occ or sum(s.occ for s in no) < min_occ:
            continue
        gain = log_likelihood(yes, var_floor) + log_likelihood(no, var_floor) - base
        if best is None or gain > best[0]:
            best = (gain, q, yes, no)
    return best


class Node:
    """A tree node. A leaf has question None and holds its states."""

    def __init__(self, states):
        self.states = states
        self.question = None
        self.yes: Optional["Node"] = None
        self.no: Optional["Node"] = None
        self.gain = 0.0


def build_tree(states, questions, threshold: float, min_occ: float, max_leaves: Optional[int] = None, var_floor: float = 1e-6):
    """Grow the tree greedily. Return (root, leaves).

    Each round splits the leaf whose best question has the largest gain.
    Without max_leaves the result does not depend on this order, because the
    decision for a leaf depends only on its own states.
    """
    root = Node(list(states))
    leaves = [root]  # @line L1
    cand = {id(root): best_question(root.states, questions, min_occ, var_floor)}  # @line L3
    while max_leaves is None or len(leaves) < max_leaves:  # @line L2
        best_leaf = None
        for leaf in leaves:  # @line L4
            c = cand[id(leaf)]
            if c is not None and (best_leaf is None or c[0] > cand[id(best_leaf)][0]):
                best_leaf = leaf
        if best_leaf is None or cand[id(best_leaf)][0] < threshold:  # @line L5
            break
        gain, q, yes, no = cand.pop(id(best_leaf))
        best_leaf.question, best_leaf.gain = q, gain  # @line L6
        best_leaf.yes, best_leaf.no = Node(yes), Node(no)
        leaves.remove(best_leaf)
        for child in (best_leaf.yes, best_leaf.no):
            leaves.append(child)
            cand[id(child)] = best_question(child.states, questions, min_occ, var_floor)
    return root, leaves  # @line L7


def merge_leaves(leaves, threshold: float, var_floor: float = 1e-6):
    """Join pairs of leaves while the smallest loss L(a) + L(b) - L(a u b) is below the threshold.

    Return a list of clusters, each a list of states. The leaves may come from
    different branches of the tree.
    """
    clusters = [list(leaf.states) if isinstance(leaf, Node) else list(leaf) for leaf in leaves]
    L = [log_likelihood(c, var_floor) for c in clusters]
    while len(clusters) > 1:  # @line L8
        best = None
        for a in range(len(clusters)):  # @line L9
            for b in range(a + 1, len(clusters)):
                loss = L[a] + L[b] - log_likelihood(clusters[a] + clusters[b], var_floor)
                if best is None or loss < best[0]:
                    best = (loss, a, b)
        if best[0] >= threshold:  # @line L10
            break
        _, a, b = best
        clusters[a] = clusters[a] + clusters[b]  # @line L11
        L[a] = log_likelihood(clusters[a], var_floor)
        del clusters[b], L[b]
    return clusters


def classify(root: Node, left: str, right: str) -> Node:
    """Return the leaf of a triphone context, seen in training or not."""
    probe = State(None, left, right, 0.0, [], [])
    node = root
    while node.question is not None:
        node = node.yes if answer(node.question, probe) else node.no
    return node


def tie(states, questions, threshold: float, min_occ: float, var_floor: float = 1e-6):
    """Build the tree, merge the leaves, and return (root, a map from state name to cluster index)."""
    root, leaves = build_tree(states, questions, threshold, min_occ, var_floor=var_floor)
    clusters = merge_leaves(leaves, threshold, var_floor)
    index = {s.name: c for c, cl in enumerate(clusters) for s in cl}
    return root, index
