# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reiter-hs-tree/. The authors are listed in prov/PCV2A8.jsonl.
"""Reiter's hitting set tree with the correction of Greiner, Smith and Wilkerson (1989).

hs_dag(next_label) is the HS-DAG of Greiner, Smith and Wilkerson. The caller
gives next_label(h): it returns a set that is disjoint from h and contains a
member of the conflict collection, or None when h hits every member. The
labels need not be minimal, but all of them must be subsets of one finite
set, so that the search stops. The result is the list of all minimal hitting
sets, sorted by size and then by their sorted elements. Elements must be
sortable, for example ints or strings.

minimal_hitting_sets(collection) runs hs_dag with the labels taken from an
explicit list of sets. diagnoses(components, consistent) runs it with the
conflicts computed on demand, as in Reiter's theory of diagnosis.

reiter_pruned_tree(collection) follows the pruning rules of Reiter (1987)
without the correction. It can lose minimal hitting sets, and it is here so
that the error can be shown.
"""

from collections import deque
from typing import Callable, Hashable, Iterable, List, Optional

Label = Optional[Iterable[Hashable]]

LABELED, CHECKED, CLOSED = "labeled", "checked", "closed"


class _Node:
    __slots__ = ("label", "status", "children")

    def __init__(self):
        self.label = None
        self.status = None
        self.children = {}


def _sort_key(s):
    return (len(s), sorted(s))


def hs_dag(next_label: Callable[[frozenset], Label]) -> List[frozenset]:
    """All minimal hitting sets, found with the pruned HS-DAG of Greiner, Smith and Wilkerson.

    Precondition: next_label meets the contract in the module comment. Cost:
    with k nodes, u elements and m labels, O(k (k + m) u) time outside the
    oracle, at most k oracle calls, and O(k u) space.
    """
    root = frozenset()
    nodes, labels = {root: _Node()}, []  # @line L1
    level = [root]  # @line L2
    while level:  # @line L3
        following = []  # @line L4
        for h in level:  # @line L5
            node = nodes.get(h)
            if node is None or node.status is not None:
                continue  # removed by a pruning step, or already processed
            if any(m < h and nodes[m].status == CHECKED for m in nodes):  # @line L6
                node.status = CLOSED
                continue
            label = next((s for s in labels if not (s & h)), None)  # @line L7
            if label is None:  # @line L8
                found = next_label(h)  # @line L9
                if found is None:  # @line L10
                    node.status = CHECKED
                    continue
                label = frozenset(found)
                if label & h:
                    raise ValueError("next_label returned a set that meets h")
                _prune(nodes, root, labels, label)  # @line L11
                labels.append(label)
                if h not in nodes:  # @line L12
                    continue
            node.label, node.status = label, LABELED  # @line L13
            for sigma in sorted(label):  # @line L14
                child = h | {sigma}  # @line L15
                if child not in nodes:  # @line L16
                    nodes[child] = _Node()  # @line L17
                    following.append(child)  # @line L18
                node.children[sigma] = child  # @line L19
        level = following  # @line L20
    return sorted((h for h, n in nodes.items() if n.status == CHECKED), key=_sort_key)  # @line L21


def _prune(nodes, root, labels, new):
    """Relabel each node whose label is a proper superset of new, and drop the nodes that are no longer reachable."""
    changed = False
    for node in nodes.values():  # @line L22
        if node.label is not None and new < node.label:
            for alpha in node.label - new:
                node.children.pop(alpha, None)
            node.label = new
            changed = True
    labels[:] = [s for s in labels if not new < s]
    if not changed:
        return
    seen = {root}  # @line L23
    stack = [root]
    while stack:
        for child in nodes[stack.pop()].children.values():
            if child not in seen:
                seen.add(child)
                stack.append(child)
    for h in [h for h in nodes if h not in seen]:
        del nodes[h]


def collection_labels(collection: Iterable[Iterable[Hashable]]) -> Callable[[frozenset], Optional[frozenset]]:
    """next_label for an explicit list of sets: the first member that is disjoint from h."""
    sets = [frozenset(s) for s in collection]

    def next_label(h):
        return next((s for s in sets if not (s & h)), None)

    return next_label


def minimal_hitting_sets(collection: Iterable[Iterable[Hashable]]) -> List[frozenset]:
    """All minimal hitting sets of a finite list of finite sets."""
    return hs_dag(collection_labels(collection))


def diagnoses(components: Iterable[Hashable], consistent: Callable[[frozenset], bool]) -> List[frozenset]:
    """All minimal diagnoses.

    consistent(ok) tells whether SD, OBS and the statements "c is not abnormal"
    for c in ok are consistent together. A subset of a consistent set must be
    consistent. Each conflict is found from the components outside h and then
    made minimal by deleting components one at a time.
    """
    comps = frozenset(components)

    def next_label(h):
        rest = comps - h
        if consistent(rest):
            return None
        conflict = set(rest)
        for c in sorted(rest):
            if not consistent(frozenset(conflict - {c})):
                conflict.discard(c)
        return frozenset(conflict)

    return hs_dag(next_label)


def reiter_pruned_tree(collection: Iterable[Iterable[Hashable]]) -> List[frozenset]:
    """Reiter's pruned HS-tree without the correction. It can lose minimal hitting sets."""
    sets = [frozenset(s) for s in collection]
    hs, label, status, children, alive = [frozenset()], [None], [None], [{}], [True]

    def kill(i):
        stack = [i]
        while stack:
            j = stack.pop()
            alive[j] = False
            stack.extend(children[j].values())

    def cut(i, keep):
        for alpha in label[i] - keep:
            if alpha in children[i]:
                kill(children[i].pop(alpha))

    queue = deque([0])
    while queue:
        i = queue.popleft()
        if not alive[i]:
            continue
        h = hs[i]
        others = [j for j in range(len(hs)) if j != i and alive[j]]
        if any(status[j] == CHECKED and hs[j] <= h for j in others):
            status[i] = CLOSED
            continue
        if any(j < i and hs[j] == h for j in others):
            status[i] = CLOSED
            continue
        s = next((label[j] for j in others if label[j] is not None and not (label[j] & h)), None)
        if s is None:
            s = next((t for t in sets if not (t & h)), None)
        if s is None:
            status[i] = CHECKED
            continue
        label[i], status[i] = s, LABELED
        for sigma in sorted(s):
            hs.append(h | {sigma})
            label.append(None)
            status.append(None)
            children.append({})
            alive.append(True)
            children[i][sigma] = len(hs) - 1
            queue.append(len(hs) - 1)
        for j in range(len(hs)):
            if j != i and alive[j] and label[j] is not None:
                if s < label[j]:
                    cut(j, s)
                elif label[j] < s and alive[i]:
                    cut(i, label[j])
    return sorted((hs[i] for i in range(len(hs)) if alive[i] and status[i] == CHECKED), key=_sort_key)
