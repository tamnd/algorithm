# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cegis/. The authors are listed in prov/P1YF3Y.jsonl.

import itertools
import random

from cegis import cegis, first_counterexample, page_example, round_up_spec, sketch_round_up


def correct_everywhere(c, inputs, run, spec) -> bool:
    return all(spec(x, run(c, x)) for x in inputs)


def check_result(r, candidates, inputs, run, spec) -> None:
    """Check the answer against brute force and check every round of the trace."""
    brute = [c for c in candidates if correct_everywhere(c, inputs, run, spec)]
    if r.program is None:
        assert brute == []
    else:
        assert correct_everywhere(r.program, inputs, run, spec)
        assert r.program == brute[0]  # default oracles return the first correct one
    assert r.rounds <= min(len(candidates), len(inputs)) + 1
    assert len(set(r.examples)) == len(r.examples)  # each counterexample is new
    for k, (c, x) in enumerate(r.trace):
        if c is None:
            continue
        for e in r.examples[:k]:  # candidate fits all earlier counterexamples
            assert spec(e, run(c, e))
        if x is not None:
            assert not spec(x, run(c, x))  # the counterexample refutes it
            assert r.examples[k] == x


def test_page_example() -> None:
    r = page_example()
    assert r.trace == [((0, 0), 1), ((3, 4), 5), ((3, 12), None)]
    assert r.program == (3, 12) and r.rounds == 3 and r.examples == [1, 5]
    for x in range(16):
        assert sketch_round_up((3, 12), x) == (-(-x // 4) * 4) % 16
    holes = [(a, b) for a in range(16) for b in range(16)]
    check_result(r, holes, list(range(16)), sketch_round_up, round_up_spec)


def test_unrealizable() -> None:
    r = cegis(list(range(16)), list(range(16)), lambda h, x: x & h, lambda x, y: y == (x + 1) % 16)
    assert r.program is None and r.examples == [0] and r.rounds == 2


def test_random_tables_against_brute_force() -> None:
    rng = random.Random(2006)
    for _ in range(400):
        nx, ny, nc = rng.randint(1, 5), rng.randint(1, 3), rng.randint(1, 12)
        inputs = list(range(nx))
        cands = [tuple(rng.randrange(ny) for _ in inputs) for _ in range(nc)]
        cands = list(dict.fromkeys(cands))
        rel = {(x, y) for x in inputs for y in range(ny) if rng.random() < 0.6}

        def run(c, x):
            return c[x]

        def spec(x, y, rel=rel):
            return (x, y) in rel

        init = rng.sample(inputs, rng.randint(0, nx))
        r = cegis(cands, inputs, run, spec, initial=init)
        brute = [c for c in cands if correct_everywhere(c, inputs, run, spec)]
        assert (r.program is None) == (brute == [])
        if r.program is not None:
            assert correct_everywhere(r.program, inputs, run, spec)
            assert r.program == brute[0]
        new = r.examples[len(init):]
        assert len(set(new)) == len(new) and not set(new) & set(init)


def grammar(depth: int) -> list:
    """Expressions over x, y on 3 bits, with ite on x <= y, up to the given depth."""
    leaves = [("x",), ("y",), ("c", 0), ("c", 1)]
    level = list(leaves)
    for _ in range(depth):
        new = list(level)
        for a, b in itertools.product(level, repeat=2):
            new.append(("add", a, b))
            new.append(("ite", a, b))  # if x <= y then a else b
        level = list(dict.fromkeys(new))
    return level


def ev(e, xy):
    x, y = xy
    if e[0] == "x":
        return x
    if e[0] == "y":
        return y
    if e[0] == "c":
        return e[1]
    if e[0] == "add":
        return (ev(e[1], xy) + ev(e[2], xy)) & 7
    return ev(e[1], xy) if x <= y else ev(e[2], xy)


def test_max_over_grammar() -> None:
    progs = grammar(1)
    inputs = [(x, y) for x in range(8) for y in range(8)]

    def spec(xy, out):
        return out == max(xy)

    r = cegis(progs, inputs, ev, spec)
    check_result(r, progs, inputs, ev, spec)
    assert r.program == ("ite", ("y",), ("x",))
    assert r.examples == [(0, 1), (1, 0), (0, 0), (1, 1)]
    assert r.rounds == 5  # four examples suffice, far fewer than the 64 inputs


def test_successor_and_doubling() -> None:
    progs = grammar(1)
    inputs = [(x, y) for x in range(8) for y in range(8)]
    for target in (lambda x, y: (x + 1) & 7, lambda x, y: (x + y) & 7, lambda x, y: (x * y) & 7):
        def spec(xy, out, t=target):
            return out == t(*xy)

        r = cegis(progs, inputs, ev, spec)
        check_result(r, progs, inputs, ev, spec)


def test_other_verifier_order() -> None:
    rng = random.Random(65)
    holes = [(a, b) for a in range(16) for b in range(16)]
    inputs = list(range(16))
    for _ in range(30):
        def verify(c):
            bad = [x for x in inputs if not round_up_spec(x, sketch_round_up(c, x))]
            return rng.choice(bad) if bad else None

        r = cegis(holes, inputs, sketch_round_up, round_up_spec, verify=verify)
        assert r.program == (3, 12)
        assert first_counterexample(inputs, sketch_round_up, round_up_spec, r.program) is None
        assert r.rounds <= 17


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
    print("ok")
