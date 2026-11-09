# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lrat-proof/. The authors are listed in prov/XV3Z16.jsonl.

"""An LRAT checker and a DRAT-to-LRAT hint generator.

The clauses of the formula have the IDs 1..m. A proof step is
("a", id, clause, hints) for an addition or ("d", [ids]) for a deletion.
Hints are clause IDs. Positive hints must each become unit (or false) in
order under the negation of the clause. For a RAT step, a negative hint -j
names a clause D_j that contains the negated pivot; the positive hints after
it prove the resolvent with D_j. Clauses are lists of DIMACS ints.
"""

from collections import Counter

CONFLICT, OPEN, ERROR = 1, 0, -1


def _run_hints(db: dict[int, list[int]], val: dict[int, bool], hints: list[int],
               trail: list[int]) -> int:
    """Apply hint clauses in order; return CONFLICT, OPEN (no conflict yet) or ERROR."""
    for h in hints:
        d = db.get(h)
        if d is None:
            return ERROR
        free = 0
        last = 0
        for lit in d:
            v = val.get(abs(lit))
            if v is None:
                free += 1
                last = lit
            elif v == (lit > 0):
                return ERROR  # a satisfied clause is never a useful hint
        if free == 0:
            return CONFLICT
        if free > 1:
            return ERROR
        val[abs(last)] = last > 0
        trail.append(abs(last))
    return OPEN


def _split(hints: list[int]) -> tuple[list[int], list[tuple[int, list[int]]]]:
    prefix: list[int] = []
    groups: list[tuple[int, list[int]]] = []
    for h in hints:
        if h < 0:
            groups.append((-h, []))
        elif groups:
            groups[-1][1].append(h)
        else:
            prefix.append(h)
    return prefix, groups


def check_step(db: dict[int, list[int]], c: list[int], hints: list[int]) -> bool:
    """Check one addition with its hints against the active clauses db."""
    val: dict[int, bool] = {}
    for lit in c:  # @line L4
        if val.get(abs(lit)) == (lit > 0):
            return True  # a tautology
        val[abs(lit)] = lit < 0
    prefix, groups = _split(hints)
    trail: list[int] = []
    r = _run_hints(db, val, prefix, trail)  # @line L5
    if r != OPEN:
        return r == CONFLICT
    if not c:  # @line L6
        return False
    pivot = c[0]
    listed = {j for j, _ in groups}
    for j, d in db.items():  # @line L7
        if -pivot in d and j not in listed:
            return False
    for j, hs in groups:  # @line L8
        d = db.get(j)
        if d is None or -pivot not in d:
            return False
        local: list[int] = []
        tautology = False
        for lit in d:
            if lit == -pivot:
                continue
            v = val.get(abs(lit))
            if v == (lit > 0):
                tautology = True
                break
            if v is None:
                val[abs(lit)] = lit < 0
                local.append(abs(lit))
        if not tautology:
            r = _run_hints(db, val, hs, local)  # @line L9
        for v in local:
            del val[v]
        if not tautology and r != CONFLICT:
            return False
    return True


def check_lrat(formula: list[list[int]], steps: list[tuple]) -> tuple[bool, int | None]:
    """Return (True, None) for a valid refutation, (False, i) if step i fails."""
    db = {i + 1: list(c) for i, c in enumerate(formula)}
    last = len(formula)
    for i, step in enumerate(steps):  # @line L1
        if step[0] == "d":  # @line L2
            for j in step[1]:
                db.pop(j, None)
            continue
        _, cid, c, hints = step  # @line L3
        if cid <= last or not check_step(db, list(c), list(hints)):
            return False, i
        db[cid] = list(c)  # @line L10
        last = cid
        if not c:
            return True, None
    return False, None  # @line L11


def find_rup_hints(db: dict[int, list[int]], c: list[int]) -> list[int] | None:
    """Unit propagation on db and the negation of c; return the hint IDs in order, or None."""
    val: dict[int, bool] = {}
    for lit in c:
        if val.get(abs(lit)) == (lit > 0):
            return []
        val[abs(lit)] = lit < 0
    reason: dict[int, int] = {}
    order: list[int] = []
    conflict = None
    changed = True
    while changed and conflict is None:
        changed = False
        for j, d in db.items():
            free = 0
            last = 0
            sat = False
            for lit in d:
                v = val.get(abs(lit))
                if v is None:
                    free += 1
                    last = lit
                elif v == (lit > 0):
                    sat = True
                    break
            if sat or free > 1:
                continue
            if free == 0:
                conflict = j
                break
            val[abs(last)] = last > 0
            reason[abs(last)] = j
            order.append(abs(last))
            changed = True
    if conflict is None:
        return None
    used = {conflict}
    stack = [abs(lit) for lit in db[conflict]]
    while stack:
        v = stack.pop()
        j = reason.get(v)
        if j is not None and j not in used:
            used.add(j)
            stack.extend(abs(lit) for lit in db[j] if abs(lit) != v)
    return [reason[v] for v in order if reason[v] in used] + [conflict]


def drat_to_lrat(formula: list[list[int]], drat: list[tuple[str, list[int]]]) -> list[tuple]:
    """Add hints to a DRAT proof whose RAT pivots are the first literals."""
    db = {i + 1: list(c) for i, c in enumerate(formula)}
    nid = len(formula)
    out: list[tuple] = []
    for op, c in drat:
        if op == "d":
            key = Counter(c)
            j = next((j for j, d in db.items() if Counter(d) == key), None)
            if j is not None:
                del db[j]
                out.append(("d", [j]))
            continue
        hints = find_rup_hints(db, c)
        if hints is None:
            if not c:
                raise ValueError("the empty clause is not RUP")
            pivot = c[0]
            hints = []
            for j, d in list(db.items()):
                if -pivot in d:
                    res = list(dict.fromkeys(c + [a for a in d if a != -pivot]))
                    h = find_rup_hints(db, res)
                    if h is None:
                        raise ValueError(f"lemma {c} is neither RUP nor RAT")
                    hints += [-j] + h
        nid += 1
        db[nid] = list(c)
        out.append(("a", nid, list(c), hints))
        if not c:
            break
    return out


def format_lrat(steps: list[tuple]) -> str:
    lines = []
    last = 0
    for s in steps:
        if s[0] == "d":
            lines.append(f"{last} d " + " ".join(map(str, s[1] + [0])))
        else:
            _, cid, c, hints = s
            last = cid
            lines.append(" ".join(map(str, [cid] + c + [0] + hints + [0])))
    return "\n".join(lines) + "\n"


def parse_lrat(text: str) -> list[tuple]:
    steps: list[tuple] = []
    for line in text.splitlines():
        parts = line.split()
        if not parts or parts[0] == "c":
            continue
        cid = int(parts[0])
        if parts[1] == "d":
            steps.append(("d", [int(p) for p in parts[2:-1]]))
            continue
        nums = [int(p) for p in parts[1:]]
        z = nums.index(0)
        steps.append(("a", cid, nums[:z], nums[z + 1:-1]))
    return steps
