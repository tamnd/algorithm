# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bottom-up-enumerative-synthesis/. The authors are listed in prov/Q97T2A.jsonl.

import random

from bottom_up_enumerative_synthesis import LEAVES, evaluate, size, synthesize


def programs_of_size(s, sort="I", memo={}):
    """Brute force: every program of the given sort with exactly s nodes."""
    key = (s, sort)
    if key in memo:
        return memo[key]
    out = []
    if sort == "I":
        if s == 1:
            out = list(LEAVES)
        for s1 in range(1, s - 1):
            for p in programs_of_size(s1):
                for q in programs_of_size(s - 1 - s1):
                    for op in ("+", "-", "*"):
                        out.append((op, p, q))
        for sb in range(3, s - 1):
            for s1 in range(1, s - sb - 1):
                for b in programs_of_size(sb, "B"):
                    for p in programs_of_size(s1):
                        for q in programs_of_size(s - 1 - sb - s1):
                            out.append(("ite", b, p, q))
    else:
        for s1 in range(1, s - 1):
            for p in programs_of_size(s1):
                for q in programs_of_size(s - 1 - s1):
                    out.append(("<=", p, q))
    memo[key] = out
    return out


def brute_min_size(examples, max_size):
    for s in range(1, max_size + 1):
        for p in programs_of_size(s):
            if all(evaluate(p, i) == o for i, o in examples):
                return s
    return None


def meets(p, examples):
    return all(evaluate(p, i) == o for i, o in examples)


def test_counts():
    assert [len(programs_of_size(s)) for s in range(1, 8)] == [4, 0, 48, 0, 1152, 256, 34560]


def test_random_targets():
    rng = random.Random(11)
    pool = [p for s in range(1, 8) for p in programs_of_size(s)]
    for t in range(14):
        target = rng.choice(pool)
        examples = []
        for _ in range(rng.randint(2, 4)):
            inp = (rng.randint(-3, 3), rng.randint(-3, 3))
            examples.append((inp, evaluate(target, inp)))
        want = brute_min_size(examples, 7)
        assert want is not None and want <= size(target)
        found, built = synthesize(examples, 7)
        assert found is not None and meets(found, examples)
        assert size(found) == want
        if t % 2 == 0:
            plain, built_plain = synthesize(examples, 7, prune=False)
            assert plain is not None and meets(plain, examples)
            assert size(plain) == want
            assert built <= built_plain


def test_random_outputs():
    # Outputs not made by a program: the synthesizer and the brute force agree, also on "none".
    rng = random.Random(12)
    for _ in range(12):
        examples = [((rng.randint(-3, 3), rng.randint(-3, 3)), rng.randint(-9, 9)) for _ in range(3)]
        want = brute_min_size(examples, 6)
        found, _ = synthesize(examples, 6)
        if want is None:
            assert found is None
        else:
            assert found is not None and meets(found, examples) and size(found) == want
        plain, _ = synthesize(examples, 6, prune=False)
        assert (plain is None) == (want is None)
        if plain is not None:
            assert size(plain) == want


def test_maximum():
    examples = [((1, 2), 2), ((3, 1), 3), ((2, 2), 2), ((3, 5), 5), ((5, 3), 5)]
    found, _ = synthesize(examples, 7)
    assert size(found) == 6
    for a in range(-4, 5):
        for b in range(-4, 5):
            assert evaluate(found, (a, b)) == max(a, b)


def test_underspecified():
    found, _ = synthesize([((1, 2), 2), ((3, 1), 3)], 7)
    assert size(found) == 3
    assert evaluate(found, (2, 2)) == 4
