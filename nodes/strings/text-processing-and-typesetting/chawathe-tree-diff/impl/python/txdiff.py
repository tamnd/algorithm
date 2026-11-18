# SPDX-License-Identifier: MIT
# Shared helper of the text processing and typesetting pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Common parts of the diff and merge pages: lines, edit scripts, the LCS matcher and a unified diff printer.

An edit script turns a sequence a into a sequence b. It is a list of Op values in
order. Each Op has a kind, an index i into a, an index j into b, and the item:

- Op(KEEP, i, j, a[i]): a[i] is kept, and it is b[j];
- Op(DELETE, i, j, a[i]): a[i] is deleted; j is the number of items of b made so far;
- Op(INSERT, i, j, b[j]): b[j] is inserted; i is the number of items of a used so far.

A matching is a list of pairs (i, j), increasing in both coordinates, of items
that the script keeps. The named algorithms of the pages are not in this file.
"""

from collections.abc import Callable, Sequence
from typing import Any, NamedTuple

KEEP = "="
DELETE = "-"
INSERT = "+"


class Op(NamedTuple):
    kind: str
    i: int
    j: int
    item: Any


def split_lines(text: str) -> list[str]:
    """Split text at each "\\n" into lines without the line feed; a final line feed adds no empty line."""
    if text == "":
        return []
    lines = text.split("\n")
    if lines[-1] == "":
        lines.pop()
    return lines


def is_matching(a: Sequence[Any], b: Sequence[Any], pairs: Sequence[tuple[int, int]],
                eq: Callable[[Any, Any], bool] | None = None) -> bool:
    """Return True if pairs is strictly increasing in both coordinates and each pair is equal by eq."""
    eq = eq if eq is not None else (lambda x, y: x == y)
    pi, pj = -1, -1
    for i, j in pairs:
        if not (pi < i < len(a) and pj < j < len(b)) or not eq(a[i], b[j]):
            return False
        pi, pj = i, j
    return True


def lcs_matching(a: Sequence[Any], b: Sequence[Any],
                 eq: Callable[[Any, Any], bool] | None = None) -> list[tuple[int, int]]:
    """Return a longest matching of a and b by the O(n m) dynamic program.

    eq(x, y) decides whether x and y may be matched; the default is ==. Ties go to
    the earliest pair, so the result is fixed for given inputs.
    """
    eq = eq if eq is not None else (lambda x, y: x == y)
    n, m = len(a), len(b)
    # length[i][j] is the length of a longest matching of a[i:] and b[j:].
    length = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        row, below = length[i], length[i + 1]
        ai = a[i]
        for j in range(m - 1, -1, -1):
            if eq(ai, b[j]):
                row[j] = below[j + 1] + 1
            else:
                row[j] = below[j] if below[j] >= row[j + 1] else row[j + 1]
    pairs: list[tuple[int, int]] = []
    i = j = 0
    while i < n and j < m:
        if eq(a[i], b[j]):
            pairs.append((i, j))
            i += 1
            j += 1
        elif length[i + 1][j] >= length[i][j + 1]:
            i += 1
        else:
            j += 1
    return pairs


def matching_to_script(a: Sequence[Any], b: Sequence[Any], pairs: Sequence[tuple[int, int]]) -> list[Op]:
    """Return the edit script that keeps the pairs; in each gap the deletes come before the inserts."""
    script: list[Op] = []
    i = j = 0
    for pi, pj in list(pairs) + [(len(a), len(b))]:
        if pi < i or pj < j:
            raise ValueError("the pairs are not increasing")
        while i < pi:
            script.append(Op(DELETE, i, j, a[i]))
            i += 1
        while j < pj:
            script.append(Op(INSERT, i, j, b[j]))
            j += 1
        if pi < len(a) and pj < len(b):
            script.append(Op(KEEP, i, j, a[i]))
            i += 1
            j += 1
    return script


def script_matching(script: Sequence[Op]) -> list[tuple[int, int]]:
    """Return the pairs (i, j) that the script keeps."""
    return [(op.i, op.j) for op in script if op.kind == KEEP]


def apply_script(a: Sequence[Any], script: Sequence[Op]) -> list[Any]:
    """Apply the script to a and return the new sequence; raise ValueError if the script does not fit a."""
    out: list[Any] = []
    i = 0
    for op in script:
        if op.kind == INSERT:
            if op.i != i or op.j != len(out):
                raise ValueError(f"bad insert {op}")
            out.append(op.item)
        elif op.kind in (KEEP, DELETE):
            if op.i != i or i >= len(a) or op.item != a[i] or op.j != len(out):
                raise ValueError(f"bad {op.kind} {op}")
            if op.kind == KEEP:
                out.append(a[i])
            i += 1
        else:
            raise ValueError(f"unknown kind {op.kind!r}")
    if i != len(a):
        raise ValueError("the script does not use all of a")
    return out


def is_valid_script(a: Sequence[Any], b: Sequence[Any], script: Sequence[Op]) -> bool:
    """Return True if the script fits a and turns a into b."""
    try:
        return apply_script(a, script) == list(b)
    except ValueError:
        return False


def script_cost(script: Sequence[Op]) -> int:
    """Return the number of deletes and inserts of the script."""
    return sum(1 for op in script if op.kind != KEEP)


def _opcodes(script: Sequence[Op]) -> list[tuple[str, int, int, int, int]]:
    """Group the script into runs in the format of difflib: equal, delete, insert or replace."""
    codes: list[tuple[str, int, int, int, int]] = []
    i = j = 0
    k = 0
    while k < len(script):
        i1, j1 = i, j
        if script[k].kind == KEEP:
            while k < len(script) and script[k].kind == KEEP:
                i, j, k = i + 1, j + 1, k + 1
            codes.append(("equal", i1, i, j1, j))
        else:
            while k < len(script) and script[k].kind != KEEP:
                if script[k].kind == DELETE:
                    i += 1
                else:
                    j += 1
                k += 1
            tag = "replace" if i > i1 and j > j1 else ("delete" if i > i1 else "insert")
            codes.append((tag, i1, i, j1, j))
    return codes


def _range(start: int, stop: int) -> str:
    length = stop - start
    first = start + 1
    if length == 1:
        return f"{first}"
    if length == 0:
        first -= 1
    return f"{first},{length}"


def unified_diff(a: Sequence[str], b: Sequence[str], script: Sequence[Op], context: int = 3,
                 from_name: str = "a", to_name: str = "b") -> list[str]:
    """Return the lines of a unified diff of the script, without line feeds, in the layout of GNU diff -u.

    The hunks are grouped as difflib.unified_diff groups them, so for the same
    matching the output is the same. If the script changes nothing, the result is [].
    """
    codes = _opcodes(script)
    if not codes:
        codes = [("equal", 0, 1, 0, 1)]
    n = context
    if codes[0][0] == "equal":
        tag, i1, i2, j1, j2 = codes[0]
        codes[0] = (tag, max(i1, i2 - n), i2, max(j1, j2 - n), j2)
    if codes[-1][0] == "equal":
        tag, i1, i2, j1, j2 = codes[-1]
        codes[-1] = (tag, i1, min(i2, i1 + n), j1, min(j2, j1 + n))
    groups: list[list[tuple[str, int, int, int, int]]] = []
    group: list[tuple[str, int, int, int, int]] = []
    for tag, i1, i2, j1, j2 in codes:
        if tag == "equal" and i2 - i1 > 2 * n:
            group.append((tag, i1, min(i2, i1 + n), j1, min(j2, j1 + n)))
            groups.append(group)
            group = []
            i1, j1 = max(i1, i2 - n), max(j1, j2 - n)
        group.append((tag, i1, i2, j1, j2))
    if group and not (len(group) == 1 and group[0][0] == "equal"):
        groups.append(group)
    out: list[str] = []
    for group in groups:
        if not out:
            out += [f"--- {from_name}", f"+++ {to_name}"]
        first, last = group[0], group[-1]
        out.append(f"@@ -{_range(first[1], last[2])} +{_range(first[3], last[4])} @@")
        for tag, i1, i2, j1, j2 in group:
            if tag == "equal":
                out += [" " + line for line in a[i1:i2]]
                continue
            if tag in ("replace", "delete"):
                out += ["-" + line for line in a[i1:i2]]
            if tag in ("replace", "insert"):
                out += ["+" + line for line in b[j1:j2]]
    return out
