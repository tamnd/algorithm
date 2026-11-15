# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grounded-extension-algorithm/. The authors are listed in prov/XNWEB6.jsonl.

"""Linear-time computation of the grounded extension of a finite framework.

A framework is a pair (args, attacks): args is a set of hashable arguments and
attacks is a set of pairs (a, b), read "a attacks b". The method keeps, for each
argument, the number of its attackers that are not yet labelled out. An argument
whose count reaches 0 is labelled in, and each argument that it attacks is
labelled out. This is the counter method of unit propagation and of Horn-SAT
forward chaining, applied to the attack graph.
"""

from collections import deque


def grounded_labelling(args, attacks, stats=None):
    """Return the grounded labelling as a dict that maps each argument to in, out or undec.

    The in arguments form the grounded extension, the out arguments are the ones
    it attacks, and the rest are undec. Time Theta(n + m) for n arguments and m
    attacks. If stats is a dict, it receives the number of queue pops and the
    number of attack edges scanned in the main loop.
    """
    succ = {a: [] for a in args}
    count = {a: 0 for a in args}  # @line L1
    for a, b in attacks:
        if a not in succ or b not in succ:
            raise ValueError(f"attack {(a, b)!r} names an argument outside args")
        succ[a].append(b)
        count[b] += 1  # attacks is a set, so each attacker counts once
    label = {a: "undec" for a in args}  # @line L2
    queue = deque(a for a in sorted(args) if count[a] == 0)  # @line L3
    pops = scans = 0
    while queue:  # @line L4
        a = queue.popleft()  # @line L5
        pops += 1
        label[a] = "in"  # @line L6
        for b in succ[a]:  # @line L7
            scans += 1
            if label[b] == "undec":  # @line L8
                label[b] = "out"  # @line L9
                for c in succ[b]:  # @line L10
                    scans += 1
                    count[c] -= 1  # @line L11
                    if count[c] == 0:  # @line L12
                        queue.append(c)
    if stats is not None:
        stats["pops"] = pops
        stats["scans"] = scans
    return label  # @line L13


def grounded_extension_algorithm(args, attacks, stats=None):
    """Return the grounded extension of (args, attacks) as a frozenset."""
    label = grounded_labelling(args, attacks, stats)
    return frozenset(a for a, x in label.items() if x == "in")
