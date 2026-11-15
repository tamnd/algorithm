# SPDX-License-Identifier: MIT
# The TREAT match algorithm for the page https://algorithm.tamnd.com/treat-algorithm/. The authors are listed in prov/.
"""The TREAT match algorithm: alpha memories and the conflict set, with no beta memories.

A working memory element (WME) is a tuple of constants. A condition is a
pattern: a tuple in which a term may be a variable, a string that starts with
"?". A rule is (name, conditions), with one or more positive conditions. An
instantiation is the tuple of WMEs, one for each condition in order, that match
the conditions with one consistent binding. The conflict set is the set of
pairs (rule name, tuple of WMEs).

Treat(rules) keeps one alpha memory for each condition pattern, shared by the
conditions that differ only in the names of their variables, and the conflict
set. insert(w) joins w, as the element of each condition that it matches, with
the alpha memories of the other conditions. delete(w) removes from the conflict
set the instantiations that hold w. No partial match is stored between changes.
"""


def is_var(term):
    return isinstance(term, str) and term.startswith("?")


def match(pattern, wme, binding):
    """Extend binding so that pattern equals wme, or return None."""
    if len(pattern) != len(wme):
        return None
    out = dict(binding)
    for p, f in zip(pattern, wme):
        if is_var(p):
            if p in out:
                if out[p] != f:
                    return None
            else:
                out[p] = f
        elif p != f:
            return None
    return out


def canonical(pattern):
    """Rename the variables of a pattern by their first occurrence."""
    names = {}
    out = []
    for t in pattern:
        if is_var(t):
            names.setdefault(t, "?" + str(len(names)))
            out.append(names[t])
        else:
            out.append(t)
    return tuple(out)


class Treat:
    def __init__(self, rules):
        self.alpha = {}
        self.rules = []
        self.memory = set()
        self.conflict = {}
        self.partial_matches = 0  # the number of consistent partial bindings that joins have built
        self.duplicates = 0
        for name, conditions in rules:
            if not conditions:
                raise ValueError(f"rule {name} has no condition")
            keys = [canonical(c) for c in conditions]
            for k in keys:
                self.alpha.setdefault(k, set())
            self.rules.append((name, [tuple(c) for c in conditions], keys))

    def conflict_set(self):
        return set(self.conflict)

    def _seeded_join(self, conditions, keys, i, w):
        """Every instantiation whose element at position i is w and whose elements before i are not w."""
        order = [j for j in range(len(conditions)) if j != i]
        chosen = [None] * len(conditions)
        chosen[i] = w

        def go(k, b):
            if k == len(order):
                yield tuple(chosen), b
                return
            j = order[k]
            for v in list(self.alpha[keys[j]]):
                if j < i and v == w:
                    continue
                b2 = match(conditions[j], v, b)
                if b2 is not None:
                    self.partial_matches += 1
                    chosen[j] = v
                    yield from go(k + 1, b2)

        b0 = match(conditions[i], w, {})
        if b0 is not None:
            self.partial_matches += 1
            yield from go(0, b0)

    def insert(self, w):
        w = tuple(w)
        if w in self.memory:
            return
        self.memory.add(w)
        hit = set()
        for key, items in self.alpha.items():  # @line L1
            if match(key, w, {}) is not None:
                items.add(w)  # @line L2
                hit.add(key)
        for name, conditions, keys in self.rules:  # @line L3
            for i, key in enumerate(keys):
                if key not in hit:  # @line L4
                    continue
                for wmes, binding in self._seeded_join(conditions, keys, i, w):  # @line L5
                    inst = (name, wmes)
                    if inst in self.conflict:
                        self.duplicates += 1
                    self.conflict[inst] = binding  # @line L6

    def delete(self, w):
        w = tuple(w)
        if w not in self.memory:
            return
        self.memory.discard(w)
        for items in self.alpha.values():  # @line L7
            items.discard(w)
        for inst in [x for x in self.conflict if w in x[1]]:  # @line L8
            del self.conflict[inst]  # @line L9
