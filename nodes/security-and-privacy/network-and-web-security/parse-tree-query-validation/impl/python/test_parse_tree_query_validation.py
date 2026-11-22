# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parse-tree-query-validation/. The authors are listed in prov/VTPNC3.jsonl.

import random
import re

import pytest

from parse_tree_query_validation import (
    QueryError,
    TemplateError,
    fill,
    leaves,
    lex,
    parse,
    shape,
    string_value,
    validate,
)

# Templates written by the programmer. A hole is quoted when its part ends in a quote.
TEMPLATES = [
    ["SELECT a FROM t WHERE name = '", "'"],
    ["SELECT a, b FROM t WHERE id = ", ""],
    ["SELECT * FROM t WHERE (name = '", "' OR id > ", ") AND NOT b < '", "'"],
    ["SELECT a FROM t WHERE id = ", " AND name <> '", "'"],
    ["SELECT a FROM t WHERE (id = ", ")"],
    ["select a from t where ", " = b"],
]

# The independent oracle: an input is confined to its literal exactly when it
# matches the language of the inside of a string (quoted hole), or of one
# literal with blanks around it (unquoted hole).
QUOTED_OK = re.compile(r"(?:[^']|'')*")
UNQUOTED_OK = re.compile(r"[ \t\n]*(?:[0-9]+|'(?:[^']|'')*')[ \t\n]*")

# Benign characters only: letters that cannot form a keyword, digits, blanks,
# quotes, a backslash, an ampersand and angle brackets.
ALPHABET = "ab12 '\\&<>"


def quoted(parts: list, i: int) -> bool:
    return parts[i].endswith("'")


def oracle(parts: list, inputs: list) -> bool:
    return all(
        (QUOTED_OK if quoted(parts, i) else UNQUOTED_OK).fullmatch(x) is not None for i, x in enumerate(inputs)
    )


def placeholder_literals(parts: list, inputs: list, tree: tuple) -> list:
    """The literal token of the accepted tree that holds each input."""
    q, origin = fill(parts, inputs)
    out = []
    for i in range(len(inputs)):
        open_quote = ("s", sum(map(len, parts[: i + 1])) - 1)  # the static quote before a quoted hole
        for t in leaves(tree):
            if quoted(parts, i):
                inside = origin[t.start] == open_quote
            else:
                inside = any(origin[p] == ("h", i) for p in range(t.start, t.end))
            if inside:
                out.append(t)
                break
    return out


def test_page_example() -> None:
    parts = ["SELECT a FROM t WHERE name = '", "' AND id = ", ""]
    tree = validate(parts, ["O''Brien", "42"])
    assert tree is not None
    toks = leaves(tree)
    assert [t.text for t in toks] == ["SELECT", "a", "FROM", "t", "WHERE", "name", "=", "'O''Brien'", "AND", "id", "=", "42"]
    assert string_value(toks[7]) == "O'Brien"
    assert validate(parts, ["O'Brien", "42"]) is None  # the quote was not doubled: the string ends early
    assert validate(parts, ["O''Brien", "4 2"]) is None  # two tokens where one literal was planned
    assert validate(parts, ["O''Brien", "id"]) is None  # an identifier is not a literal
    assert validate(parts, ["O''Brien", " 42 "]) is not None
    assert validate(parts, ["O''Brien", "'42'"]) is not None  # a string literal is a literal too


def test_lexer_and_parser() -> None:
    assert [t.kind for t in lex("a<=b <> 'x''y' 12")] == ["ident", "op", "ident", "op", "str", "num"]
    with pytest.raises(QueryError):  # outside a string a backslash is no token
        lex("a \\ b")
    with pytest.raises(QueryError):
        lex("'abc")
    with pytest.raises(QueryError):
        parse("SELECT a FROM t WHERE a = 1 b")
    with pytest.raises(QueryError):
        parse("SELECT a FROM t WHERE a = 1 = 2")
    tree = parse("SELECT a FROM t WHERE NOT (a = 1 OR b = 'x') AND c > 2")
    assert shape(tree)[5][2][0] == "and"  # AND binds tighter than OR, and NOT tighter than AND
    assert len(leaves(tree)) == 19


@pytest.mark.parametrize(
    "parts",
    [
        ["SELECT ", " FROM t"],  # a placeholder where a column name goes
        ["SELECT a FROM t WHERE ab", " = 1"],  # the placeholder joins an identifier
        ["SELECT a FROM t WHERE name = '", ""],  # the string does not end
        ["SELECT a FROM t WHERE a = ", " ", ""],  # two numbers in a row
    ],
)
def test_bad_templates(parts: list) -> None:
    with pytest.raises(TemplateError):
        validate(parts, ["x"] * (len(parts) - 1))


def test_backslash_is_ordinary() -> None:
    parts = ["SELECT a FROM t WHERE name = '", "'"]
    tree = validate(parts, ["a\\b"])
    assert tree is not None and string_value(leaves(tree)[7]) == "a\\b"
    assert validate(parts, ["a\\'"]) is None  # in this dialect a backslash does not protect a quote


def test_random_inputs_against_oracle() -> None:
    rng = random.Random(20050311)
    accepted = rejected = 0
    for _ in range(3000):
        parts = rng.choice(TEMPLATES)
        inputs = []
        for i in range(len(parts) - 1):
            r = rng.random()
            if r < 0.3:
                x = rng.choice(["O''Brien", "42", " 7 ", "''", "", "'ab'", "a''b''", "x&y", "<b>"])
            else:
                x = "".join(rng.choice(ALPHABET) for _ in range(rng.randrange(7)))
            inputs.append(x)
        tree = validate(parts, inputs)
        assert (tree is not None) == oracle(parts, inputs), (parts, inputs)
        if tree is None:
            rejected += 1
            continue
        accepted += 1
        # The accepted tree has the planned shape, and each input is the
        # content of one literal: no character of an input became code.
        q0, _ = fill(parts, ["1"] * len(inputs))
        assert shape(tree) == shape(parse(q0))
        lits = placeholder_literals(parts, inputs, tree)
        assert len(lits) == len(inputs)
        for i, (x, t) in enumerate(zip(inputs, lits)):
            if quoted(parts, i):
                assert t.kind == "str" and string_value(t) == x.replace("''", "'")
            else:
                assert t.kind in ("num", "str") and t.text == x.strip(" \t\n")
    assert accepted > 500 and rejected > 500


def test_parse_only_is_not_enough() -> None:
    """A check that the query parses accepts inputs that move token boundaries."""
    parts = ["SELECT a FROM t WHERE id <", ""]
    # The input "=2" joins the static "<" into the operator "<=": the query
    # parses, but the input is no longer inside a literal.
    q, _ = fill(parts, ["=2"])
    parse(q)
    assert validate(parts, ["=2"]) is None
    assert validate(parts, ["2"]) is not None
