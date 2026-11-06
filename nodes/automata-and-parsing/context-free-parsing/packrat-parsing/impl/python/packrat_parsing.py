# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/packrat-parsing/. The authors are listed in prov/1PYY5B.jsonl.

"""Packrat parsing of parsing expression grammars, without recursion.

A grammar is a dict that maps each nonterminal name to one parsing expression.
Expressions are tuples:

    ("lit", a)          the token a
    ("any",)            any one token
    ("eps",)            the empty match
    ("ref", A)          the nonterminal A
    ("seq", e1, ..., ek)
    ("alt", e1, ..., ek)   ordered choice: the first alternative that succeeds
    ("star", e)         greedy repetition
    ("not", e)          succeeds, consuming nothing, exactly when e fails
    ("and", e)          succeeds, consuming nothing, exactly when e succeeds

Every subexpression is compiled to a number, and the result of each pair
(expression, position) is computed once and kept in a table. The evaluation uses
an explicit stack, so deep inputs do not hit the recursion limit.

A parse tree is a pair (A, children) for a nonterminal node and a plain string for
a token leaf. The children of a node are the tokens and nonterminal nodes matched
by the body of its rule, in order; predicates contribute nothing.
"""

Expr = tuple
Tree = tuple[str, list] | str

FAIL = -1
LIT, ANY, EPS, REF, SEQ, ALT, STAR, NOT, AND = range(9)
_KINDS = {"lit": LIT, "any": ANY, "eps": EPS, "ref": REF, "seq": SEQ,
          "alt": ALT, "star": STAR, "not": NOT, "and": AND}


class ParseError(Exception):
    """The input is not in the language; position is the farthest failure.

    A failure is a token test or a not-predicate that fails.
    """

    def __init__(self, position: int, message: str) -> None:
        super().__init__(f"at token {position}: {message}")
        self.position = position


class Peg:
    """A grammar compiled to arrays indexed by expression number."""

    def __init__(self, grammar: dict[str, Expr]) -> None:
        self.kind: list[int] = []
        self.arg: list = []        # the token, or the rule name for "ref"
        self.kids: list[tuple[int, ...]] = []
        self.rule: dict[str, int] = {}
        todo: list[tuple[Expr, int]] = []
        for name, body in grammar.items():
            self.rule[name] = self._new(body, todo)
        while todo:
            e, k = todo.pop()
            self.kids[k] = tuple(self._new(c, todo) for c in e[1:])
        for k, kd in enumerate(self.kind):
            if kd == REF and self.arg[k] not in self.rule:
                raise ValueError(f"no rule for {self.arg[k]}")

    def _new(self, e: Expr, todo: list) -> int:
        k = len(self.kind)
        kd = _KINDS[e[0]]
        self.kind.append(kd)
        self.arg.append(e[1] if kd in (LIT, REF) else None)
        self.kids.append(())
        if kd in (SEQ, ALT, STAR, NOT, AND):
            todo.append((e, k))
        return k


class Packrat:
    """One run of the parser on one input; memo holds every computed result."""

    def __init__(self, peg: Peg, tokens: list[str]) -> None:
        self.peg = peg
        self.tokens = tokens
        self.n = len(tokens)
        self.memo: dict[int, int] = {}      # key e * (n + 1) + i -> end or FAIL
        self.choice: dict[int, int] = {}    # key of an "alt" -> winning alternative
        self.far = 0                        # farthest position of a failed token test
        self.evaluations = 0                # pairs (e, i) computed, not looked up

    def eval(self, root: int, pos: int) -> int:
        """The end of the match of expression root at pos, or FAIL."""
        peg, toks, n, memo = self.peg, self.tokens, self.n, self.memo
        kind, arg, kids = peg.kind, peg.arg, peg.kids
        width = n + 1
        active: set[int] = set()
        stack: list[list[int]] = []         # frames [e, i, state]
        req: tuple[int, int] | None = (root, pos)
        ret = FAIL
        while True:
            if req is not None:
                e, i = req
                req = None
                key = e * width + i
                r = memo.get(key)
                if r is not None:  # @line L5
                    ret = r
                elif key in active:  # @line L6
                    raise ValueError("left recursion: the grammar is not well-formed")
                else:
                    self.evaluations += 1
                    kd = kind[e]
                    if kd == LIT or kd == ANY:  # @line L8
                        if i < n and (kd == ANY or toks[i] == arg[e]):
                            r = i + 1
                        else:
                            r = FAIL
                            self.far = max(self.far, i)
                        memo[key] = r
                        ret = r
                    elif kd == EPS:
                        memo[key] = i
                        ret = i
                    else:  # @line L7
                        active.add(key)
                        stack.append([e, i, 0])
                        req = (kids[e][0] if kd != REF else peg.rule[arg[e]], i)
                        continue
            if not stack:
                return ret
            frame = stack[-1]
            e, i, state = frame
            kd = kind[e]
            done = True
            if kd == REF:  # @line L9
                r = ret
            elif kd == SEQ:  # @line L10
                if ret == FAIL or state + 1 == len(kids[e]):
                    r = ret
                else:
                    frame[2] = state + 1
                    req = (kids[e][state + 1], ret)
                    done = False
            elif kd == ALT:  # @line L11
                if ret != FAIL:
                    self.choice[e * width + i] = state
                    r = ret
                elif state + 1 == len(kids[e]):
                    r = FAIL
                else:
                    frame[2] = state + 1
                    req = (kids[e][state + 1], i)
                    done = False
            elif kd == STAR:  # @line L12
                if state == 1:
                    r = ret
                elif ret == FAIL:
                    r = i
                elif ret == i:
                    raise ValueError("repetition of an empty match: the grammar is not well-formed")
                else:
                    frame[2] = 1
                    req = (e, ret)
                    done = False
            else:  # @line L13
                r = i if (ret == FAIL) == (kd == NOT) else FAIL
                if r == FAIL and kd == NOT:
                    self.far = max(self.far, i)
            if done:
                key = e * width + i
                memo[key] = r  # @line L14
                active.discard(key)
                stack.pop()
                ret = r

    def tree(self, name: str, pos: int) -> Tree:
        """The parse tree of the successful match of the rule name at pos.

        A node for the same rule at the same position is built once and shared,
        so the tree is returned as a graph with O(|G| (n + 1)) distinct nodes even
        when, written out, it is much larger (empty matches can nest deeply).
        """
        peg, toks, memo, width = self.peg, self.tokens, self.memo, self.n + 1
        kind, kids = peg.kind, peg.kids
        root: tuple[str, list] = (name, [])
        built: dict[int, tuple[str, list]] = {peg.rule[name] * width + pos: root}
        work: list[tuple[int, int, list]] = [(peg.rule[name], pos, root[1])]
        while work:
            e, i, out = work.pop()
            kd = kind[e]
            if kd == LIT or kd == ANY:  # @line L15
                out.append(toks[i])
            elif kd == REF:  # @line L16
                body = peg.rule[peg.arg[e]]
                node = built.get(body * width + i)
                if node is None:
                    node = (peg.arg[e], [])
                    built[body * width + i] = node
                    work.append((body, i, node[1]))
                out.append(node)
            elif kd == SEQ:  # @line L17
                parts = []
                for c in kids[e]:
                    parts.append((c, i, out))
                    i = memo[c * width + i]
                work.extend(reversed(parts))
            elif kd == ALT:
                work.append((kids[e][self.choice[e * width + i]], i, out))
            elif kd == STAR:
                c = kids[e][0]
                j = memo[c * width + i]
                if j != FAIL:
                    work.append((e, j, out))
                    work.append((c, i, out))
            # @line L18: eps, not and and add nothing
        return root


def packrat_parse(grammar: dict[str, Expr], start: str, tokens: list[str],
                  stats: dict | None = None) -> Tree:
    """Match the rule start against all of tokens and return the parse tree.

    Raises ParseError at the farthest failed token test when the rule fails or
    leaves input unread, and ValueError when the run meets left recursion or a
    repetition of an empty match.
    """
    peg = Peg(grammar)
    run = Packrat(peg, list(tokens))  # @line L1
    end = run.eval(peg.rule[start], 0)  # @line L2
    if stats is not None:
        stats["evaluations"] = run.evaluations
        stats["expressions"] = len(peg.kind)
    if end == FAIL:  # @line L3
        raise ParseError(run.far, "no match")
    if end < run.n:
        raise ParseError(max(run.far, end), "input left over")
    return run.tree(start, 0)  # @line L4


def packrat_match(grammar: dict[str, Expr], start: str, tokens: list[str]) -> int | None:
    """The end of the match of start at position 0, or None if it fails."""
    peg = Peg(grammar)
    run = Packrat(peg, list(tokens))
    end = run.eval(peg.rule[start], 0)
    return None if end == FAIL else end
