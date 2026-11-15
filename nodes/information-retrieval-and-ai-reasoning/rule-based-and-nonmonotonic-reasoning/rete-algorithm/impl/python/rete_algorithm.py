# SPDX-License-Identifier: MIT
# The Rete match algorithm for the page https://algorithm.tamnd.com/rete-algorithm/. The authors are listed in prov/.
"""The Rete match algorithm, with alpha memories, shared join nodes and tree-based removal.

A working memory element (WME) is a tuple of constants. A condition is a
pattern: a tuple in which a term may be a variable, a string that starts with
"?". A rule is (name, conditions), with one or more positive conditions. An
instantiation of a rule is the tuple of WMEs, one for each condition in order,
that match the conditions with one consistent binding of the variables. The
conflict set is the set of pairs (rule name, tuple of WMEs).

Rete(rules) builds the network. insert(w) and delete(w) change the working
memory, which is a set, and keep the conflict set up to date.

- An alpha memory holds the WMEs that pass the tests of one condition alone:
  its constants and the equalities between its own variables. Conditions that
  differ only in the names of their variables share one alpha memory.
- A join node stands for a prefix c_1, ..., c_i of the conditions of a rule.
  Rules with the same prefix share the node. Its beta memory holds tokens: the
  partial matches of the prefix.
- A token records its parent token, its WME and its children, and each WME
  records the tokens that hold it, so a delete removes exactly the tokens that
  contain the WME, without a new match.
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
    """Rename the variables of a pattern by their first occurrence: ("p", "?x", "?x") becomes ("p", "?0", "?0")."""
    names = {}
    out = []
    for t in pattern:
        if is_var(t):
            names.setdefault(t, "?" + str(len(names)))
            out.append(names[t])
        else:
            out.append(t)
    return tuple(out)


class AlphaMemory:
    def __init__(self, pattern):
        self.pattern = pattern
        self.items = set()
        self.successors = []  # the join nodes that read this memory


class Token:
    __slots__ = ("parent", "wme", "binding", "node", "children", "wmes")

    def __init__(self, parent, wme, binding, node):
        self.parent = parent
        self.wme = wme
        self.binding = binding
        self.node = node
        self.children = []
        self.wmes = () if parent is None else parent.wmes + (wme,)


class JoinNode:
    def __init__(self, parent, alpha, condition, depth):
        self.parent = parent  # None for the first condition
        self.alpha = alpha
        self.condition = condition
        self.depth = depth
        self.tokens = []  # the beta memory
        self.children = []
        self.productions = []


class Rete:
    def __init__(self, rules):
        self.alpha = {}
        self.joins = {}
        self.root = Token(None, None, {}, None)
        self.memory = set()
        self.conflict = {}
        self.wme_tokens = {}
        self.tokens_made = 0
        self.duplicates = 0
        for name, conditions in rules:
            if not conditions:
                raise ValueError(f"rule {name} has no condition")
            node = None
            for i, c in enumerate(conditions):
                key = tuple(conditions[: i + 1])
                if key not in self.joins:
                    am = self.alpha.setdefault(canonical(c), AlphaMemory(canonical(c)))
                    nn = JoinNode(node, am, tuple(c), i)
                    am.successors.append(nn)
                    if node is not None:
                        node.children.append(nn)
                    self.joins[key] = nn
                node = self.joins[key]
            node.productions.append(name)

    def conflict_set(self):
        return set(self.conflict)

    def _make_token(self, parent, wme, binding, node):
        t = Token(parent, wme, binding, node)  # @line L8
        self.tokens_made += 1
        node.tokens.append(t)
        parent.children.append(t)
        self.wme_tokens.setdefault(wme, []).append(t)
        for name in node.productions:
            key = (name, t.wmes)
            if key in self.conflict:
                self.duplicates += 1
            self.conflict[key] = t.binding
        for child in node.children:
            self._left_activate(child, t)

    def _left_activate(self, node, token):
        for w in list(node.alpha.items):  # @line L9
            b = match(node.condition, w, token.binding)  # @line L10
            if b is not None:
                self._make_token(token, w, b, node)  # @line L11

    def _right_activate(self, node, w):
        parents = [self.root] if node.parent is None else list(node.parent.tokens)
        for t in parents:  # @line L5
            b = match(node.condition, w, t.binding)  # @line L6
            if b is not None:
                self._make_token(t, w, b, node)  # @line L7

    def insert(self, w):
        w = tuple(w)
        if w in self.memory:
            return
        self.memory.add(w)
        targets = []
        for am in self.alpha.values():  # @line L1
            if match(am.pattern, w, {}) is not None:
                am.items.add(w)  # @line L2
                targets.extend(am.successors)
        targets.sort(key=lambda n: -n.depth)  # @line L3
        for node in targets:  # @line L4
            self._right_activate(node, w)

    def _delete_token(self, t):
        while t.children:
            self._delete_token(t.children[-1])
        t.node.tokens.remove(t)
        t.parent.children.remove(t)
        self.wme_tokens[t.wme].remove(t)
        for name in t.node.productions:
            self.conflict.pop((name, t.wmes), None)

    def delete(self, w):
        w = tuple(w)
        if w not in self.memory:
            return
        self.memory.discard(w)
        for am in self.alpha.values():  # @line L12
            am.items.discard(w)
        for t in list(self.wme_tokens.get(w, [])):  # @line L13
            if t.node is not None and t in t.node.tokens:
                self._delete_token(t)  # @line L14
        self.wme_tokens.pop(w, None)

    def token_count(self):
        return sum(len(n.tokens) for n in self.joins.values())
