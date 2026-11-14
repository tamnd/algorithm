# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gemini-netlist-comparison/. The authors are listed in prov/N08Y88.jsonl.
"""Gemini style netlist comparison: iterative relabeling of devices and nets,
then individualization (a guess) when the labels stop splitting.

A netlist is a pair (devices, anchors):

  devices: a list of (type, pins), where pins is a tuple of net names.
  anchors: a dict {net name: global name} for nets that must match by name,
           for example the supply nets and the ports.

PIN_CLASSES[type] gives, for each pin position of the type, its class. Pins
of one class are interchangeable (the source and the drain of a MOS
transistor, the two ends of a resistor).

compare(a, b, pin_classes) returns ("match", device_map, net_map) or
("mismatch", report). Labels are exact sorted signatures renumbered over both
netlists at once, so two vertices get the same label only when their
signatures are equal. Gemini itself uses numeric labels that can collide; a
collision only makes a class coarser, and the final check below catches it.
"""

from collections import Counter


class _Graph:
    """The bipartite device and net graph of one netlist."""

    def __init__(self, netlist, pin_classes):
        devices, anchors = netlist
        nets = sorted({v for _, pins in devices for v in pins} | set(anchors))
        self.net_index = {v: i for i, v in enumerate(nets)}
        self.nets = nets
        self.dev_type = [t for t, _ in devices]
        self.dev_pins = []  # per device: list of (class, net index)
        self.net_pins = [[] for _ in nets]  # per net: list of (class, device index)
        for d, (t, pins) in enumerate(devices):
            classes = pin_classes[t]
            if len(classes) != len(pins):
                raise ValueError(f"device {d}: wrong number of pins for {t}")
            row = []
            for c, v in zip(classes, pins):
                j = self.net_index[v]
                row.append((c, j))
                self.net_pins[j].append((c, d))
            self.dev_pins.append(row)
        self.anchor = [anchors.get(v) for v in nets]


def _renumber(keys_a, keys_b):
    """Replace keys by small integers, the same integer for equal keys in both lists."""
    table = {k: i for i, k in enumerate(sorted(set(keys_a) | set(keys_b)))}
    return [table[k] for k in keys_a], [table[k] for k in keys_b]


def _classes(lab_a, lab_b):
    count = Counter()
    for x in lab_a:
        count[x] += 1
    for x in lab_b:
        count[x] -= 1
    return count


def _refine(ga, gb, dev, net):
    """Relabel nets from devices and devices from nets until the number of
    labels stops growing. dev and net are pairs (labels of a, labels of b).
    Returns the new labels, or a mismatch report."""
    while True:
        before = len(set(dev[0]) | set(dev[1])) + len(set(net[0]) | set(net[1]))
        keys = []
        for g, dl, nl in ((ga, dev[0], net[0]), (gb, dev[1], net[1])):
            keys.append([(nl[j], tuple(sorted((c, dl[d]) for c, d in g.net_pins[j])))  # @line L4
                         for j in range(len(g.nets))])
        net = _renumber(*keys)  # @line L6
        keys = []
        for g, dl, nl in ((ga, dev[0], net[0]), (gb, dev[1], net[1])):
            keys.append([(dl[d], tuple(sorted((c, nl[j]) for c, j in g.dev_pins[d])))  # @line L5
                         for d in range(len(g.dev_type))])
        dev = _renumber(*keys)  # @line L6
        for kind, (la, lb) in (("device", dev), ("net", net)):
            bad = [x for x, k in _classes(la, lb).items() if k != 0]
            if bad:  # @line L7
                x = bad[0]
                return None, (kind, [i for i, y in enumerate(la) if y == x],
                              [i for i, y in enumerate(lb) if y == x])
        after = len(set(dev[0]) | set(dev[1])) + len(set(net[0]) | set(net[1]))
        if after == before:  # @line L8
            return (dev, net), None


def _check(ga, gb, dmap, nmap):
    """True when the maps are an isomorphism of the netlists."""
    for d, row in enumerate(ga.dev_pins):
        e = dmap[d]
        if ga.dev_type[d] != gb.dev_type[e]:
            return False
        if Counter((c, nmap[j]) for c, j in row) != Counter(gb.dev_pins[e]):
            return False
    return all(ga.anchor[j] == gb.anchor[nmap[j]] for j in range(len(ga.nets)))


def _search(ga, gb, dev, net, backtrack, stats):
    stats["refinements"] += 1
    labels, report = _refine(ga, gb, dev, net)  # @line L3
    if labels is None:
        return None, report
    dev, net = labels
    sizes = Counter(dev[0])
    nsizes = Counter(net[0])
    if all(k == 1 for k in sizes.values()) and all(k == 1 for k in nsizes.values()):  # @line L9
        dpos = {x: i for i, x in enumerate(dev[1])}
        npos = {x: i for i, x in enumerate(net[1])}
        dmap = [dpos[x] for x in dev[0]]
        nmap = [npos[x] for x in net[0]]
        if _check(ga, gb, dmap, nmap):
            return (dmap, nmap), None
        return None, ("check", [], [])
    # the smallest class with two or more members, devices first on ties
    cand = [(k, 0, x) for x, k in sizes.items() if k > 1] + [(k, 1, x) for x, k in nsizes.items() if k > 1]  # @line L10
    _, side, x = min(cand)
    labs = dev if side == 0 else net
    i = labs[0].index(x)
    fresh = 1 + max(max(dev[0]), max(net[0]) if net[0] else 0)
    report = None
    for j in [j for j, y in enumerate(labs[1]) if y == x]:  # @line L11
        stats["guesses"] += 1
        la, lb = list(labs[0]), list(labs[1])
        la[i] = lb[j] = fresh  # @line L12
        nd, nn = ((la, lb), net) if side == 0 else (dev, (la, lb))
        result, report = _search(ga, gb, nd, nn, backtrack, stats)
        if result is not None:
            return result, None
        if not backtrack:
            break
    return None, report  # @line L13


def compare(a, b, pin_classes, backtrack=True, stats=None):
    """Compare two netlists. With backtrack=False only the first guess at each
    tie is tried, as a plain guessing comparator does; a wrong guess can then
    report a false mismatch."""
    if stats is None:
        stats = {}
    stats.setdefault("refinements", 0)
    stats.setdefault("guesses", 0)
    ga, gb = _Graph(a, pin_classes), _Graph(b, pin_classes)
    if len(ga.dev_type) != len(gb.dev_type) or len(ga.nets) != len(gb.nets):
        return ("mismatch", ("size", [], []))
    dev = _renumber(ga.dev_type, gb.dev_type)  # @line L1
    net = _renumber([(ga.anchor[j] or "", len(ga.net_pins[j])) for j in range(len(ga.nets))],
                    [(gb.anchor[j] or "", len(gb.net_pins[j])) for j in range(len(gb.nets))])
    result, report = _search(ga, gb, dev, net, backtrack, stats)  # @line L2
    if result is None:
        return ("mismatch", report)
    dmap, nmap = result
    return ("match", dmap, {ga.nets[j]: gb.nets[nmap[j]] for j in range(len(ga.nets))})
