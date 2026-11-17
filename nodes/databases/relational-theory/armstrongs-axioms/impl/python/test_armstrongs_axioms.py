# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/armstrongs-axioms/. The authors are listed in prov/X72AKB.jsonl.

import random

from armstrongs_axioms import check_proof, closure, derivable, derive, implied

A, B, C, D = 1, 2, 4, 8


def random_fds(rng: random.Random, n: int) -> list:
    full = 1 << n
    return [(rng.randrange(full), rng.randrange(1, full)) for _ in range(rng.randint(0, 4))]


def test_example() -> None:
    f = [(A, B), (B, C)]
    plus = derivable(3, f)
    assert (A, C) in plus and (A, A | B | C) in plus and (A | C, B) in plus
    assert (C, A) not in plus and (B, A) not in plus
    assert len(plus) == len(implied(3, f))


def test_sound_and_complete() -> None:
    rng = random.Random(1)
    for n in (3, 4):
        for _ in range(40 if n == 3 else 15):
            f = random_fds(rng, n)
            syntactic = derivable(n, f)
            semantic = implied(n, f)
            assert syntactic == semantic
            full = 1 << n
            assert semantic == {(x, y) for x in range(full) for y in range(full) if y & ~closure(f, x) == 0}


def test_sound_on_larger_relations() -> None:
    # Every relation that satisfies F satisfies each FD that the axioms derive.
    rng = random.Random(2)
    n = 4
    for _ in range(30):
        f = random_fds(rng, n)
        plus = derivable(n, f)
        for _ in range(30):
            rel = [[rng.randrange(2) for _ in range(n)] for _ in range(rng.randint(1, 4))]

            def holds(x: int, y: int) -> bool:
                cols = [i for i in range(n) if x >> i & 1]
                outs = [i for i in range(n) if y >> i & 1]
                return all(
                    any(t[i] != u[i] for i in cols) or all(t[i] == u[i] for i in outs) for t in rel for u in rel
                )

            if all(holds(x, y) for x, y in f):
                assert all(holds(x, y) for x, y in plus)


def test_proofs() -> None:
    rng = random.Random(3)
    n = 4
    for _ in range(40):
        f = random_fds(rng, n)
        for x in range(1 << n):
            c = closure(f, x)
            for y in range(1 << n):
                proof = derive(f, x, y)
                if y & ~c:
                    assert proof is None
                else:
                    assert proof is not None and check_proof(f, proof)
                    assert proof[-1][:2] == (x, y)


def test_check_proof_rejects_bad_steps() -> None:
    f = [(A, B)]
    assert not check_proof(f, [(B, A, "given", (), 0)])
    assert not check_proof(f, [(A, B, "refl", (), 0)])
    assert not check_proof(f, [(A, B, "given", (), 0), (A, B | C, "aug", (0,), C)])


def test_each_rule_is_needed() -> None:
    # Without reflexivity no trivial FD appears from the empty set.
    assert (A, A) not in derivable(2, [], ("augmentation", "transitivity"))
    # Without augmentation, AC -> BC does not follow from A -> B.
    assert (A | C, B | C) not in derivable(3, [(A, B)], ("reflexivity", "transitivity"))
    assert (A | C, B | C) in derivable(3, [(A, B)])
    # Without transitivity, A -> C does not follow from A -> B and B -> C.
    assert (A, C) not in derivable(3, [(A, B), (B, C)], ("reflexivity", "augmentation"))
