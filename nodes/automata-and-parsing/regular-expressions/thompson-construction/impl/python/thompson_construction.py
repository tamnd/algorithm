# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thompson-construction/. The authors are listed in prov/WDNKY8.jsonl.

"""Thompson's construction: a regular expression to an epsilon-NFA.

Syntax: union |, concatenation by juxtaposition, postfix star *, the
constants ε (empty string) and ∅ (empty set), and parentheses. Every other
character is a symbol. Star binds tighter than concatenation, which binds
tighter than union. Parsing and construction use explicit stacks, so deeply
nested expressions need no recursion.
"""

from dataclasses import dataclass, field

EPS = "ε"
EMPTY = "∅"
CAT = "."  # the concatenation operator in the postfix form


def to_postfix(pattern: str) -> list[tuple[str, str]]:
    """Return the expression in postfix form as (kind, value) tokens.

    kind is "sym", "eps", "empty" or "op"; ops are "|", CAT and "*".
    Raises ValueError on a malformed pattern.
    """
    prec = {"|": 1, CAT: 2}
    out: list[tuple[str, str]] = []
    ops: list[str] = []
    prev_operand = False  # True if the last item can end an operand
    for c in pattern:
        if c == " ":
            continue
        if c in "(" or c not in "|*)":
            if prev_operand:  # implicit concatenation
                while ops and ops[-1] != "(" and prec[ops[-1]] >= prec[CAT]:
                    out.append(("op", ops.pop()))
                ops.append(CAT)
            if c == "(":
                ops.append("(")
                prev_operand = False
                continue
            kind = "eps" if c == EPS else "empty" if c == EMPTY else "sym"
            out.append((kind, c))
            prev_operand = True
        elif c == "*":
            if not prev_operand:
                raise ValueError("* without an operand")
            out.append(("op", "*"))
        elif c == "|":
            if not prev_operand:
                raise ValueError("| without a left operand")
            while ops and ops[-1] != "(" and prec[ops[-1]] >= prec["|"]:
                out.append(("op", ops.pop()))
            ops.append("|")
            prev_operand = False
        else:  # ")"
            if not prev_operand:
                raise ValueError("empty operand before )")
            while ops and ops[-1] != "(":
                out.append(("op", ops.pop()))
            if not ops:
                raise ValueError("unbalanced )")
            ops.pop()
            prev_operand = True
    if not prev_operand:
        raise ValueError("missing operand at the end")
    while ops:
        op = ops.pop()
        if op == "(":
            raise ValueError("unbalanced (")
        out.append(("op", op))
    return out


@dataclass
class NFA:
    """An epsilon-NFA with states 0 .. n-1, one start and one accepting state.

    sym[q] is None or a pair (a, r) for the move q --a--> r.
    eps[q] lists the targets of the epsilon-moves of q (at most two).
    """

    start: int = 0
    accept: int = 0
    sym: list[tuple[str, int] | None] = field(default_factory=list)
    eps: list[list[int]] = field(default_factory=list)

    def new_state(self) -> int:
        self.sym.append(None)
        self.eps.append([])
        return len(self.sym) - 1

    @property
    def size(self) -> int:
        return len(self.sym)


def thompson(pattern: str) -> NFA:
    """Build the Thompson epsilon-NFA of a regular expression.

    The NFA has at most 2m states and 4m moves for an expression of size m.
    """
    nfa = NFA()
    stack: list[tuple[int, int]] = []  # fragments (start, accept)  @line L1
    for kind, v in to_postfix(pattern):  # @line L2
        if kind != "op":  # @line L3
            s, f = nfa.new_state(), nfa.new_state()  # @line L4
            if kind == "sym":
                nfa.sym[s] = (v, f)  # @line L5
            elif kind == "eps":
                nfa.eps[s].append(f)  # @line L6
            stack.append((s, f))  # @line L7
        elif v == "|":  # @line L8
            s2, f2 = stack.pop()  # @line L9
            s1, f1 = stack.pop()
            s, f = nfa.new_state(), nfa.new_state()
            nfa.eps[s] += [s1, s2]  # @line L10
            nfa.eps[f1].append(f)
            nfa.eps[f2].append(f)
            stack.append((s, f))
        elif v == CAT:  # @line L11
            s2, f2 = stack.pop()  # @line L12
            s1, f1 = stack.pop()
            nfa.eps[f1].append(s2)
            stack.append((s1, f2))
        else:  # star  @line L13
            s1, f1 = stack.pop()  # @line L14
            s, f = nfa.new_state(), nfa.new_state()
            nfa.eps[s] += [s1, f]  # @line L15
            nfa.eps[f1] += [s1, f]
            stack.append((s, f))
    nfa.start, nfa.accept = stack.pop()  # @line L16
    assert not stack
    return nfa


def accepts(nfa: NFA, word: str) -> bool:
    """Run the NFA on a word by the set-of-states simulation."""

    def close(states: set[int]) -> set[int]:
        todo = list(states)
        while todo:
            q = todo.pop()
            for r in nfa.eps[q]:
                if r not in states:
                    states.add(r)
                    todo.append(r)
        return states

    cur = close({nfa.start})
    for a in word:
        nxt = set()
        for q in cur:
            m = nfa.sym[q]
            if m is not None and m[0] == a:
                nxt.add(m[1])
        cur = close(nxt)
    return nfa.accept in cur
