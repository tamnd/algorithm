# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/string-transformation-synthesis/. The authors are listed in prov/NBNPFH.jsonl.

import random

from string_transformation_synthesis import (
    atom_cost, count_programs, eval_atom, eval_pos, positions, program_cost, run, synthesize,
)

ALPHABET = "abAB12 "
MAX_ATOMS = 4


def brute_force(examples, max_atoms=MAX_ATOMS):
    """Search all programs with at most max_atoms atoms.

    Constants are the non-empty substrings of the first output; a constant of a
    consistent program is always one of them. Atoms with the same outputs on all
    example inputs are grouped, with their number. The search extends a list of
    atoms while the outputs so far are prefixes of the wanted outputs; a list
    that is not a prefix cannot be completed. Returns (number of consistent
    programs, least cost or None, one program with that cost).
    """
    ins = [s for s, _ in examples]
    outs = [o for _, o in examples]
    max_len = max(len(s) for s in ins)
    groups = {}
    ps = positions(max_len)
    for p1 in ps:
        for p2 in ps:
            f = ("sub", p1, p2)
            vec = tuple(eval_atom(f, s) for s in ins)
            if None not in vec:
                groups.setdefault(vec, []).append(f)
    o1 = outs[0]
    pieces = {o1[i:j] for i in range(len(o1)) for j in range(i + 1, len(o1) + 1)}
    for piece in sorted(pieces):
        groups.setdefault(tuple(piece for _ in ins), []).append(("const", piece))
    items = [(vec, sorted(fs, key=atom_cost)) for vec, fs in groups.items()]
    total = 0
    best = [None, None]

    def go(prefix_lens, depth, chosen):
        nonlocal total
        if all(n == len(o) for n, o in zip(prefix_lens, outs)) and depth > 0:
            total_here = 1
            for _, fs in chosen:
                total_here *= len(fs)
            total += total_here
            prog = tuple(fs[0] for _, fs in chosen)
            if best[0] is None or program_cost(prog) < best[0]:
                best[0] = program_cost(prog)
                best[1] = prog
            return
        if depth == max_atoms:
            return
        for vec, fs in items:
            ok = True
            new = []
            for piece, n, o in zip(vec, prefix_lens, outs):
                if o[n:n + len(piece)] != piece:
                    ok = False
                    break
                new.append(n + len(piece))
            if ok:
                go(tuple(new), depth + 1, chosen + [(vec, fs)])

    go(tuple(0 for _ in outs), 0, [])
    return total, best[0], best[1]


def random_string(rng):
    return "".join(rng.choice(ALPHABET) for _ in range(rng.randint(1, 6)))


def random_program(rng, max_len):
    ps = positions(max_len)
    prog = []
    for _ in range(rng.randint(1, 3)):
        if rng.random() < 0.3:
            prog.append(("const", rng.choice(["-", ".", "x", "ab", ", "])))
        else:
            prog.append(("sub", rng.choice(ps), rng.choice(ps)))
    return tuple(prog)


def random_task(rng, k):
    while True:
        ins = [random_string(rng) for _ in range(k)]
        prog = random_program(rng, max(len(s) for s in ins))
        outs = [run(prog, s) for s in ins]
        if None not in outs:
            return list(zip(ins, outs))


def check(examples):
    total, least, witness = brute_force(examples)
    found = synthesize(examples)
    if witness is not None:
        assert all(run(witness, s) == o for s, o in examples)
        assert program_cost(witness) == least
    if found is not None:
        assert all(run(found, s) == o for s, o in examples)
    if least is not None:
        # If the search finds a program, so does the synthesizer, and no cheaper one exists.
        assert found is not None
        assert program_cost(found) <= least
        if len(found) <= MAX_ATOMS:
            assert program_cost(found) == least
    elif found is not None:
        assert len(found) > MAX_ATOMS
    assert count_programs(examples, MAX_ATOMS) == total


def test_random_tasks_match_brute_force():
    rng = random.Random(7)
    for t in range(30):
        check(random_task(rng, 1 + t % 3))


def test_random_outputs_match_brute_force():
    rng = random.Random(8)
    for t in range(30):
        k = 1 + t % 2
        examples = [(random_string(rng), random_string(rng).strip() or "a") for _ in range(k)]
        check(examples)


def test_names():
    examples = [("Ada Lo", "A. Lo"), ("Bo Ng", "B. Ng")]
    check(examples)
    prog = synthesize(examples)
    assert run(prog, "Cy Wu") == "C. Wu"
    assert sum(1 for f in prog if f[0] == "const") == 1


def test_one_example_is_ambiguous():
    prog = synthesize([("Ada Lo", "A. Lo")])
    assert run(prog, "Ada Lo") == "A. Lo"
    assert count_programs([("Ada Lo", "A. Lo")], 3) > count_programs([("Ada Lo", "A. Lo"), ("Bo Ng", "B. Ng")], 3)


def test_positions():
    s = "ab 12 c"
    assert eval_pos(("pos", "L", "S", 1), s) == 2
    assert eval_pos(("pos", "S", "D", 1), s) == 3
    assert eval_pos(("pos", "E", "L", -1), s) == 6
    assert eval_pos(("pos", "E", "L", 3), s) is None
    assert eval_pos(("cpos", -1), s) == 7
    assert eval_pos(("cpos", -8), s) == 0
    assert eval_pos(("cpos", -9), s) is None
    assert atom_cost(("const", "x")) > atom_cost(("sub", ("cpos", 4), ("cpos", 5)))


def test_unrealizable():
    assert synthesize([("ab", "zz"), ("12", "yy")]) is None
    assert brute_force([("ab", "zz"), ("12", "yy")])[0] == 0
