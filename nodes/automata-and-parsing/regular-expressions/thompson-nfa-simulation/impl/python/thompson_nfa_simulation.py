# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thompson-nfa-simulation/. The authors are listed in prov/X9HKD8.jsonl.

"""Thompson's NFA simulation: match a regular expression in O(mn) time.

Syntax: union |, concatenation by juxtaposition, postfix star *, the
constants ε (empty string) and ∅ (empty set), and parentheses. The pattern is
first compiled by Thompson's construction (copied here so that the module is
self-contained), then the NFA is run on the text with a set of active states.
No step uses recursion.
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
    stack: list[tuple[int, int]] = []  # fragments (start, accept)
    for kind, v in to_postfix(pattern):
        if kind != "op":
            s, f = nfa.new_state(), nfa.new_state()
            if kind == "sym":
                nfa.sym[s] = (v, f)
            elif kind == "eps":
                nfa.eps[s].append(f)
            stack.append((s, f))
        elif v == "|":
            s2, f2 = stack.pop()
            s1, f1 = stack.pop()
            s, f = nfa.new_state(), nfa.new_state()
            nfa.eps[s] += [s1, s2]
            nfa.eps[f1].append(f)
            nfa.eps[f2].append(f)
            stack.append((s, f))
        elif v == CAT:
            s2, f2 = stack.pop()
            s1, f1 = stack.pop()
            nfa.eps[f1].append(s2)
            stack.append((s1, f2))
        else:  # star
            s1, f1 = stack.pop()
            s, f = nfa.new_state(), nfa.new_state()
            nfa.eps[s] += [s1, f]
            nfa.eps[f1] += [s1, f]
            stack.append((s, f))
    nfa.start, nfa.accept = stack.pop()
    assert not stack
    return nfa


def _add(nfa: NFA, lst: list[int], mark: list[int], q: int, step: int) -> None:
    """Add q and every state that epsilon-moves reach from it to lst, once per step."""
    stack = [q]  # @line L10
    while stack:  # @line L11
        p = stack.pop()  # @line L12
        if mark[p] == step:  # @line L13
            continue
        mark[p] = step  # @line L14
        lst.append(p)
        stack.extend(reversed(nfa.eps[p]))  # @line L15


def run(nfa: NFA, text: str, search: bool = False) -> bool:
    """Run the Thompson NFA on text.

    With search=False, decide whether the whole text is in the language.
    With search=True, decide whether some substring of the text is in the
    language, by starting a new run at each position.
    Cost: O(m) per symbol, O(m n) in total, O(m) extra space.
    """
    mark = [-1] * nfa.size
    cur: list[int] = []
    _add(nfa, cur, mark, nfa.start, 0)  # @line L2
    if search and mark[nfa.accept] == 0:
        return True
    for i, a in enumerate(text, start=1):  # @line L3
        nxt: list[int] = []  # @line L4
        for q in cur:  # @line L5
            m = nfa.sym[q]
            if m is not None and m[0] == a:  # @line L6
                _add(nfa, nxt, mark, m[1], i)
        if search:
            _add(nfa, nxt, mark, nfa.start, i)
            if mark[nfa.accept] == i:
                return True
        cur = nxt  # @line L7
        if not cur:  # @line L8
            return False
    return mark[nfa.accept] == len(text)  # @line L9


def full_match(pattern: str, text: str) -> bool:
    """Decide whether text is in the language of pattern."""
    return run(thompson(pattern), text)  # @line L1


def search(pattern: str, text: str) -> bool:
    """Decide whether some substring of text is in the language of pattern."""
    return run(thompson(pattern), text, search=True)
