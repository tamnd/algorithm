# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/armstrongs-axioms/. The authors are listed in prov/X72AKB.jsonl.

"""Armstrong's axioms for functional dependencies, made executable.

Sets of attributes are bitmasks over n attributes, and an FD X -> Y is the
pair (X, Y) of masks.

- derivable(n, F, rules) applies reflexivity, augmentation and transitivity
  to all subsets until nothing new appears: the syntactic closure F+.
- implied(n, F) is the semantic closure: the FDs that hold in every
  two-tuple relation that satisfies F.
- derive(F, X, Y) writes a proof of X -> Y from the three rules, following
  the attribute closure of X, and check_proof verifies such a proof.
"""

from collections.abc import Iterable, Sequence

Dep = tuple[int, int]
RULES = ("reflexivity", "augmentation", "transitivity")


def derivable(n: int, fds: Iterable[Dep], rules: Sequence[str] = RULES) -> set[Dep]:
    """All FDs over n attributes that the given rules derive from fds."""
    full = 1 << n
    out = set(fds)
    if "reflexivity" in rules:
        out |= {(x, y) for x in range(full) for y in range(full) if y & ~x == 0}
    while True:
        new = set()
        if "augmentation" in rules:
            for x, y in out:
                for z in range(full):
                    new.add((x | z, y | z))
        if "transitivity" in rules:
            by_lhs: dict[int, list[int]] = {}
            for x, y in out:
                by_lhs.setdefault(x, []).append(y)
            for x, y in out:
                for z in by_lhs.get(y, ()):
                    new.add((x, z))
        if new <= out:
            return out
        out |= new


def satisfies_two_tuple(agree: int, fds: Iterable[Dep]) -> bool:
    """The two-tuple relation whose tuples agree exactly on agree satisfies each FD."""
    return all(x & ~agree or y & ~agree == 0 for x, y in fds)


def implied(n: int, fds: Sequence[Dep]) -> set[Dep]:
    """All FDs over n attributes that hold in every two-tuple model of fds."""
    full = 1 << n
    models = [s for s in range(full) if satisfies_two_tuple(s, fds)]
    return {(x, y) for x in range(full) for y in range(full) if satisfies_two_tuple_all(models, x, y)}


def satisfies_two_tuple_all(models: Iterable[int], x: int, y: int) -> bool:
    return all(x & ~s or y & ~s == 0 for s in models)


def closure(fds: Sequence[Dep], x: int) -> int:
    out = x
    changed = True
    while changed:
        changed = False
        for v, w in fds:
            if v & ~out == 0 and w & ~out:
                out |= w
                changed = True
    return out


# A proof step is (lhs, rhs, rule, premises, extra). The rule "given" cites an
# FD of F; "aug" has one premise and the augmenting set in extra; "trans" has
# two premises, given by their positions in the proof.
Step = tuple[int, int, str, tuple[int, ...], int]


def derive(fds: Sequence[Dep], x: int, y: int) -> list[Step] | None:
    """A proof of X -> Y from fds by the three axioms, or None if Y is not in X+."""
    proof: list[Step] = [(x, x, "refl", (), 0)]
    have = 0  # proof[have] is X -> C, where C is the closure so far
    c = x
    changed = True
    while changed:
        changed = False
        for v, w in fds:
            if v & ~c == 0 and w & ~c:
                proof.append((c, v, "refl", (), 0))
                proof.append((x, v, "trans", (have, len(proof) - 1), 0))
                proof.append((v, w, "given", (), 0))
                proof.append((x, w, "trans", (len(proof) - 2, len(proof) - 1), 0))
                proof.append((x | c, w | c, "aug", (len(proof) - 1,), c))
                proof.append((x, c | w, "trans", (have, len(proof) - 1), 0))
                have = len(proof) - 1
                c |= w
                changed = True
    if y & ~c:
        return None
    proof.append((c, y, "refl", (), 0))
    proof.append((x, y, "trans", (have, len(proof) - 1), 0))
    return proof


def check_proof(fds: Sequence[Dep], proof: Sequence[Step]) -> bool:
    """Check that each step is a given FD or one application of an axiom."""
    given = set(fds)
    for i, (lhs, rhs, rule, prem, extra) in enumerate(proof):
        if any(p >= i for p in prem):
            return False
        if rule == "given":
            ok = (lhs, rhs) in given
        elif rule == "refl":
            ok = rhs & ~lhs == 0
        elif rule == "aug":
            v, w = proof[prem[0]][:2]
            ok = lhs == v | extra and rhs == w | extra
        elif rule == "trans":
            (v, w), (w2, z) = proof[prem[0]][:2], proof[prem[1]][:2]
            ok = w == w2 and lhs == v and rhs == z
        else:
            ok = False
        if not ok:
            return False
    return True
