# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parse-tree-query-validation/. The authors are listed in prov/VTPNC3.jsonl.

"""Parse-tree validation of queries built from a template and inputs.

A query template is a list of static parts p0, p1, ..., pk written by the
programmer. The query is p0 x1 p1 x2 ... xk pk, where x1, ..., xk are inputs.
validate parses the query twice: once with each input replaced by the
placeholder "1", which gives the intended tree, and once with the real
inputs. It accepts only when the two concrete parse trees have the same
shape and every token starts and ends at the same place, so that each input
stays inside the one literal that holds its placeholder. This is the method
of Buehrer, Weide and Sivilotti (2005), on a toy subset of SQL:

  query   := SELECT cols FROM ident [WHERE cond]
  cols    := '*' | ident (',' ident)*
  cond    := term (OR term)*
  term    := factor (AND factor)*
  factor  := NOT factor | '(' cond ')' | operand cmp operand
  operand := ident | number | string
  cmp     := '=' | '<>' | '<' | '<=' | '>' | '>='

Strings are in single quotes, with '' for a quote inside. A backslash is an
ordinary character. Keywords are not case sensitive.
"""

from typing import NamedTuple, Union

PLACEHOLDER = "1"
KEYWORDS = frozenset({"SELECT", "FROM", "WHERE", "AND", "OR", "NOT"})
OPERATORS = ("<=", ">=", "<>", "=", "<", ">", ",", "(", ")", "*")
COMPARISONS = frozenset({"=", "<>", "<", "<=", ">", ">="})
SPACE = frozenset(" \t\n")
LITERALS = frozenset({"num", "str"})


class QueryError(ValueError):
    """The text is not a query of the toy language."""


class TemplateError(ValueError):
    """The template itself is bad: with placeholders it does not parse, or a
    placeholder is not inside one literal."""


class Token(NamedTuple):
    kind: str  # "kw", "ident", "num", "str" or "op"
    text: str
    start: int
    end: int


Tree = tuple  # (label, child, child, ...) with Token leaves


def lex(q: str) -> list[Token]:
    """Split q into tokens, longest match first. Cost: O(len(q))."""
    toks: list[Token] = []
    i, n = 0, len(q)
    while i < n:
        ch = q[i]
        if ch in SPACE:
            i += 1
        elif ch.isascii() and (ch.isalpha() or ch == "_"):
            j = i + 1
            while j < n and q[j].isascii() and (q[j].isalnum() or q[j] == "_"):
                j += 1
            word = q[i:j]
            if word.upper() in KEYWORDS:
                toks.append(Token("kw", word.upper(), i, j))
            else:
                toks.append(Token("ident", word, i, j))
            i = j
        elif ch.isascii() and ch.isdigit():
            j = i + 1
            while j < n and q[j].isascii() and q[j].isdigit():
                j += 1
            toks.append(Token("num", q[i:j], i, j))
            i = j
        elif ch == "'":
            j = i + 1
            while True:
                if j >= n:
                    raise QueryError("a string literal does not end")
                if q[j] == "'":
                    if j + 1 < n and q[j + 1] == "'":
                        j += 2
                        continue
                    break
                j += 1
            toks.append(Token("str", q[i : j + 1], i, j + 1))
            i = j + 1
        else:
            for op in OPERATORS:
                if q.startswith(op, i):
                    toks.append(Token("op", op, i, i + len(op)))
                    i += len(op)
                    break
            else:
                raise QueryError(f"no token starts with {ch!r}")
    return toks


class _Parser:
    """Recursive descent over a token list. The grammar is LL(1)."""

    def __init__(self, toks: list[Token]) -> None:
        self.toks = toks
        self.k = 0

    def _peek(self, kind: str, text: Union[str, None] = None) -> bool:
        if self.k >= len(self.toks):
            return False
        t = self.toks[self.k]
        return t.kind == kind and (text is None or t.text == text)

    def _take(self, kind: str, text: Union[str, None] = None) -> Token:
        if not self._peek(kind, text):
            raise QueryError(f"expected {text or kind} at token {self.k}")
        self.k += 1
        return self.toks[self.k - 1]

    def query(self) -> Tree:
        children: list = [self._take("kw", "SELECT"), self._cols(), self._take("kw", "FROM"), self._take("ident")]
        if self._peek("kw", "WHERE"):
            children.append(("where", self._take("kw", "WHERE"), self._cond()))
        if self.k != len(self.toks):
            raise QueryError(f"text after the end of the query at token {self.k}")
        return ("query", *children)

    def _cols(self) -> Tree:
        if self._peek("op", "*"):
            return ("cols", self._take("op", "*"))
        items: list = [self._take("ident")]
        while self._peek("op", ","):
            items += [self._take("op", ","), self._take("ident")]
        return ("cols", *items)

    def _cond(self) -> Tree:
        node = self._term()
        while self._peek("kw", "OR"):
            node = ("or", node, self._take("kw", "OR"), self._term())
        return node

    def _term(self) -> Tree:
        node = self._factor()
        while self._peek("kw", "AND"):
            node = ("and", node, self._take("kw", "AND"), self._factor())
        return node

    def _factor(self) -> Tree:
        if self._peek("kw", "NOT"):
            return ("not", self._take("kw", "NOT"), self._factor())
        if self._peek("op", "("):
            return ("paren", self._take("op", "("), self._cond(), self._take("op", ")"))
        left = self._operand()
        if self.k >= len(self.toks) or self.toks[self.k].text not in COMPARISONS:
            raise QueryError(f"expected a comparison at token {self.k}")
        op = self._take("op")
        return ("cmp", left, op, self._operand())

    def _operand(self) -> Token:
        for kind in ("ident", "num", "str"):
            if self._peek(kind):
                return self._take(kind)
        raise QueryError(f"expected an operand at token {self.k}")


def parse(q: str) -> Tree:
    """The concrete parse tree of q; raises QueryError. Cost: O(len(q))."""
    return _Parser(lex(q)).query()


def leaves(tree: Tree) -> list[Token]:
    """The tokens of a parse tree, left to right."""
    out: list[Token] = []
    stack: list = [tree]
    while stack:
        node = stack.pop()
        if isinstance(node, Token):
            out.append(node)
        else:
            stack.extend(reversed(node[1:]))
    return out


def shape(tree: Union[Tree, Token]) -> tuple:
    """The tree with the text of each literal erased, and its kind too."""
    if isinstance(tree, Token):
        return ("lit",) if tree.kind in LITERALS else (tree.kind, tree.text)
    return (tree[0],) + tuple(shape(child) for child in tree[1:])


def fill(parts: list[str], inputs: list[str]) -> tuple[str, list[tuple[str, int]]]:
    """The text p0 x1 p1 ... xk pk and the origin of each character:
    ("s", j) for the j-th static character, ("h", i) for a character of input i."""
    if len(parts) != len(inputs) + 1:
        raise ValueError("a template with k holes has k + 1 parts")
    text: list[str] = []
    origin: list[tuple[str, int]] = []
    j = 0
    for i, part in enumerate(parts):
        text.append(part)
        origin.extend(("s", j + d) for d in range(len(part)))
        j += len(part)
        if i < len(inputs):
            text.append(inputs[i])
            origin.extend(("h", i) for _ in inputs[i])
    return "".join(text), origin


def validate(parts: list[str], inputs: list[str]) -> Union[Tree, None]:
    """VALIDATE of the page. Returns the parse tree of the query when the
    inputs keep the intended structure, None when it rejects the query, and
    raises TemplateError when the template itself is bad.

    Precondition: parts are static text from the programmer, inputs are any
    strings. Cost: O(n) time and space for a query of n characters.
    """
    q, origin = fill(parts, inputs)  # @line L1
    q0, origin0 = fill(parts, [PLACEHOLDER] * len(inputs))  # @line L2
    try:
        a = parse(q0)  # @line L3
    except QueryError as e:
        raise TemplateError(f"the template does not parse: {e}") from None  # @line L4
    la = leaves(a)
    touching = [0] * len(inputs)  # the number of tokens that meet each placeholder
    for t in la:
        for i in {origin0[p][1] for p in range(t.start, t.end) if origin0[p][0] == "h"}:
            touching[i] += 1
            if t.kind not in LITERALS:
                touching[i] = 2
    if any(c != 1 for c in touching):
        raise TemplateError("a placeholder is not inside one literal")  # @line L4
    try:
        b = parse(q)  # @line L5
    except QueryError:
        return None  # @line L6
    if shape(a) != shape(b):  # @line L7
        return None
    for ta, tb in zip(la, leaves(b)):  # @line L8
        if origin[tb.start] != origin0[ta.start] or origin[tb.end - 1] != origin0[ta.end - 1]:  # @line L9
            return None
    return b  # @line L10


def string_value(tok: Token) -> str:
    """The value of a string literal token."""
    return tok.text[1:-1].replace("''", "'")
