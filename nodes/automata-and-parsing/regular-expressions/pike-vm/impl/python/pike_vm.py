# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pike-vm/. The authors are listed in prov/VF24KJ.jsonl.

"""The Pike VM: Thompson's NFA simulation with thread priorities and submatches.

A regular expression is a tuple:
("empty",) for the empty language, ("eps",) for the empty string,
("sym", a) for one symbol, ("alt", r, s), ("cat", r, s), ("star", r),
and two extras: ("lazy", r) for the non-greedy star r*?, and ("group", r)
for a capture group. Groups are numbered 1, 2, ... in the order of their
opening parentheses; group 0 is the whole match.

The expression is compiled to a program of instructions:
("char", a), ("split", x, y) which prefers x, ("jmp", x), ("save", k),
("fail",) and ("match",). The VM runs one thread per program counter,
keeps the threads in priority order, and returns the leftmost-first match.
"""

from __future__ import annotations

from typing import Any

Regex = tuple[Any, ...]
Program = list[tuple[Any, ...]]
Spans = list[tuple[int, int] | None]


def compile_regex(regex: Regex) -> tuple[Program, int]:
    """Compile to a program; return (program, number of groups including group 0).

    The tree is walked with an explicit stack, so deep expressions need no recursion.
    """
    prog: list[list[Any]] = [["save", 0]]
    ngroups = 1
    todo: list[tuple[str, Any]] = [("emit", regex)]
    while todo:
        task, arg = todo.pop()
        if task == "emit":
            tag = arg[0]
            if tag == "sym":
                prog.append(["char", arg[1]])
            elif tag == "empty":
                prog.append(["fail"])
            elif tag == "cat":
                todo.append(("emit", arg[2]))
                todo.append(("emit", arg[1]))
            elif tag == "alt":
                split = len(prog)
                prog.append(["split", split + 1, None])
                cell = [split, None]  # the split, then the jmp that ends the left branch
                todo.append(("end_alt", cell))
                todo.append(("emit", arg[2]))
                todo.append(("mid_alt", cell))
                todo.append(("emit", arg[1]))
            elif tag in ("star", "lazy"):
                split = len(prog)
                if tag == "star":
                    prog.append(["split", split + 1, None])
                else:
                    prog.append(["split", None, split + 1])
                todo.append(("end_star", split))
                todo.append(("emit", arg[1]))
            elif tag == "group":
                k = ngroups
                ngroups += 1
                prog.append(["save", 2 * k])
                todo.append(("save", 2 * k + 1))
                todo.append(("emit", arg[1]))
            elif tag != "eps":
                raise ValueError(f"unknown node {arg!r}")
        elif task == "mid_alt":
            arg[1] = len(prog)
            prog.append(["jmp", None])
            prog[arg[0]][2] = len(prog)
        elif task == "end_alt":
            prog[arg[1]][1] = len(prog)
        elif task == "end_star":
            prog.append(["jmp", arg])
            ins = prog[arg]
            if ins[2] is None:
                ins[2] = len(prog)
            else:
                ins[1] = len(prog)
        elif task == "save":
            prog.append(["save", arg])
    prog.append(["save", 1])
    prog.append(["match"])
    return [tuple(ins) for ins in prog], ngroups


def _add_thread(
    prog: Program, threads: list[tuple[int, tuple[int, ...]]], seen: set[int], pc: int, caps: tuple[int, ...], i: int
) -> None:
    """Add the thread (pc, caps) at position i and follow jmp, split and save.

    Depth-first in priority order with an explicit stack; a program counter
    already in `seen` is skipped, so each list holds one thread per pc.
    """
    stack = [(pc, caps)]
    while stack:
        pc, caps = stack.pop()
        if pc in seen:  # @line L14
            continue
        seen.add(pc)
        ins = prog[pc]
        op = ins[0]
        if op == "jmp":  # @line L15
            stack.append((ins[1], caps))
        elif op == "split":  # @line L16
            stack.append((ins[2], caps))
            stack.append((ins[1], caps))
        elif op == "save":  # @line L17
            k = ins[1]
            stack.append((pc + 1, caps[:k] + (i,) + caps[k + 1 :]))
        elif op != "fail":  # @line L18
            threads.append((pc, caps))


def pike_vm(prog: Program, ngroups: int, text: str, full: bool = False) -> Spans | None:
    """Return the spans of the leftmost-first match of the program in `text`, or None.

    spans[k] is (start, end) for group k, or None if group k took no part.
    With full=True the match must cover the whole text.
    Cost: O(len(prog) * len(text) * ngroups) time and O(len(prog) * ngroups) space.
    """
    n = len(text)
    blank = (-1,) * (2 * ngroups)
    clist: list[tuple[int, tuple[int, ...]]] = []  # @line L1
    cseen: set[int] = set()
    matched: tuple[int, ...] | None = None
    for i in range(n + 1):  # @line L2
        if matched is None and (i == 0 or not full):  # @line L3
            _add_thread(prog, clist, cseen, 0, blank, i)
        if not clist:  # @line L4
            break
        nlist: list[tuple[int, tuple[int, ...]]] = []  # @line L5
        nseen: set[int] = set()
        for pc, caps in clist:  # @line L6
            ins = prog[pc]
            if ins[0] == "char":
                if i < n and text[i] == ins[1]:  # @line L7
                    _add_thread(prog, nlist, nseen, pc + 1, caps, i + 1)
            elif not full or i == n:  # @line L8
                matched = caps  # @line L9
                break  # @line L10
        clist, cseen = nlist, nseen  # @line L11
    if matched is None:  # @line L12
        return None
    spans: Spans = []
    for k in range(ngroups):
        s, e = matched[2 * k], matched[2 * k + 1]
        spans.append((s, e) if s >= 0 and e >= 0 else None)
    return spans  # @line L13


def search(regex: Regex, text: str) -> Spans | None:
    """The leftmost-first match of `regex` in `text`, with the spans of all groups."""
    prog, ngroups = compile_regex(regex)
    return pike_vm(prog, ngroups, text)


def fullmatch(regex: Regex, text: str) -> Spans | None:
    """The highest-priority match of `regex` that covers all of `text`, or None."""
    prog, ngroups = compile_regex(regex)
    return pike_vm(prog, ngroups, text, full=True)
