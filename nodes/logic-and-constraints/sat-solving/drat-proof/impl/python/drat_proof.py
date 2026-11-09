# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/drat-proof/. The authors are listed in prov/9RG6K9.jsonl.

"""A small forward DRAT checker.

A proof is a list of steps ("a", clause) for an addition and ("d", clause)
for a deletion. An added clause must be RUP (reverse unit propagation) or
RAT on its first literal with respect to the current clauses. The proof
refutes F when the empty clause is added. Clauses are lists of DIMACS ints.
"""

from collections import Counter


def propagates_to_conflict(clauses: list[list[int]], assume: list[int]) -> bool:
    """True if unit propagation on clauses with the literals assume gives a conflict."""
    val: dict[int, bool] = {}
    for a in assume:
        if val.get(abs(a)) == (a < 0):
            return True
        val[abs(a)] = a > 0
    changed = True
    while changed:
        changed = False
        for c in clauses:
            free = 0
            last = 0
            for lit in c:
                v = val.get(abs(lit))
                if v is None:
                    free += 1
                    last = lit
                    if free > 1:
                        break
                elif v == (lit > 0):
                    free = -1
                    break
            if free == 0:
                return True
            if free == 1:
                val[abs(last)] = last > 0
                changed = True
    return False


def is_rup(clauses: list[list[int]], c: list[int]) -> bool:
    """C is RUP for F if unit propagation on F and the negation of C gives a conflict."""
    return propagates_to_conflict(clauses, [-a for a in c])


def is_rat(clauses: list[list[int]], c: list[int], pivot: int) -> bool:
    """C is RAT on pivot if each resolvent with a clause containing -pivot is RUP."""
    for d in clauses:
        if -pivot in d:
            resolvent = list(dict.fromkeys(c + [a for a in d if a != -pivot]))
            if not is_rup(clauses, resolvent):
                return False
    return True


def check_drat(formula: list[list[int]], proof: list[tuple[str, list[int]]]) -> tuple[bool, int | None]:
    """Check a DRAT refutation.

    Returns (True, None) if the empty clause is added and every addition is
    RUP or RAT; (False, i) if step i fails; (False, None) if the proof ends
    without the empty clause.
    """
    clauses = [list(c) for c in formula]
    for i, (op, c) in enumerate(proof):  # @line L1
        if op == "d":  # @line L2
            key = Counter(c)
            for j, d in enumerate(clauses):
                if Counter(d) == key:
                    del clauses[j]
                    break
            continue
        c = list(c)  # @line L3
        if not is_rup(clauses, c):  # @line L4
            if not c:  # @line L5
                return False, i
            if not is_rat(clauses, c, c[0]):  # @line L6
                return False, i  # @line L7
        clauses.append(c)  # @line L8
        if not c:
            return True, None
    return False, None  # @line L9


def parse_drat(text: str) -> list[tuple[str, list[int]]]:
    """Parse the text DRAT format: one clause per line, ending in 0; 'd' marks a deletion."""
    steps = []
    for line in text.splitlines():
        parts = line.split()
        if not parts or parts[0] == "c":
            continue
        op = "a"
        if parts[0] == "d":
            op, parts = "d", parts[1:]
        lits = [int(p) for p in parts]
        if not lits or lits[-1] != 0:
            raise ValueError("a DRAT line must end with 0")
        steps.append((op, lits[:-1]))
    return steps


def format_drat(proof: list[tuple[str, list[int]]]) -> str:
    out = []
    for op, c in proof:
        body = " ".join(str(a) for a in c + [0])
        out.append(("d " if op == "d" else "") + body)
    return "\n".join(out) + "\n"


def cdcl_with_proof(formula: list[list[int]], n: int, restart_every: int = 8,
                    delete: bool = False) -> tuple[dict[int, bool] | None, list[tuple[str, list[int]]]]:
    """A tiny CDCL solver that logs a DRAT proof.

    It learns first-UIP clauses, restarts every restart_every conflicts and,
    if delete is set, deletes old learned clauses at restarts (never a clause
    that is the reason of an assigned literal). Returns (model, proof); the
    model is None for an unsatisfiable formula and then the proof ends with
    the empty clause.
    """
    db: list[list[int] | None] = [list(dict.fromkeys(c)) for c in formula]
    learned: list[int] = []
    proof: list[tuple[str, list[int]]] = []
    val: dict[int, bool] = {}
    level: dict[int, int] = {}
    reason: dict[int, int | None] = {}
    trail: list[int] = []
    lim: list[int] = []

    def assign(lit: int, why: int | None) -> None:
        val[abs(lit)] = lit > 0
        level[abs(lit)] = len(lim)
        reason[abs(lit)] = why
        trail.append(lit)

    def backtrack(to: int) -> None:
        while len(lim) > to:
            start = lim.pop()
            while len(trail) > start:
                v = abs(trail.pop())
                del val[v], level[v], reason[v]

    def propagate() -> int | None:
        changed = True
        while changed:
            changed = False
            for ci, c in enumerate(db):
                if c is None:
                    continue
                free = 0
                last = 0
                sat = False
                for lit in c:
                    v = val.get(abs(lit))
                    if v is None:
                        free += 1
                        last = lit
                    elif v == (lit > 0):
                        sat = True
                        break
                if sat:
                    continue
                if free == 0:
                    return ci
                if free == 1:
                    assign(last, ci)
                    changed = True
        return None

    def analyze(confl: int) -> list[int]:
        seen: set[int] = set()
        out: list[int] = []
        counter = 0
        p = 0
        idx = len(trail) - 1
        c = confl
        while True:
            for q in db[c]:
                if q == p:
                    continue
                v = abs(q)
                if v not in seen and level[v] > 0:
                    seen.add(v)
                    if level[v] == len(lim):
                        counter += 1
                    else:
                        out.append(q)
            while abs(trail[idx]) not in seen:
                idx -= 1
            p = trail[idx]
            idx -= 1
            counter -= 1
            if counter == 0:
                return [-p] + out
            c = reason[abs(p)]

    conflicts = 0
    while True:
        confl = propagate()
        if confl is not None:
            if not lim:
                proof.append(("a", []))
                return None, proof
            conflicts += 1
            lemma = analyze(confl)
            back = max((level[abs(q)] for q in lemma[1:]), default=0)
            backtrack(back)
            db.append(lemma)
            learned.append(len(db) - 1)
            proof.append(("a", list(lemma)))
            if conflicts % restart_every == 0:
                backtrack(0)
                if propagate() is not None:
                    proof.append(("a", []))
                    return None, proof
                if delete:
                    reasons = {reason[abs(t)] for t in trail}
                    old = learned[: len(learned) // 2]
                    keep = learned[len(learned) // 2:]
                    for ci in old:
                        if ci in reasons or len(db[ci]) <= 2:
                            keep.append(ci)
                        else:
                            proof.append(("d", list(db[ci])))
                            db[ci] = None
                    learned = sorted(keep)
            continue
        free = [v for v in range(1, n + 1) if v not in val]
        if not free:
            return {v: val[v] for v in range(1, n + 1)}, proof
        lim.append(len(trail))
        assign(-free[0], None)
