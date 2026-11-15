# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/activation-record/. The authors are listed in prov/4XG2M7.jsonl.

import random

from activation_record import OutOfFuel, compile_program, evaluate, run_machine

# main has a local x. f reads x. g has its own local y and calls f.
F = ("fun", "f", [], [], ("var", "x"), [])
G = ("fun", "g", [], ["y"], ("seq", ("assign", "y", ("int", 2)), ("call", "f", [])), [])
SCOPE = ("fun", "main", [], ["x"], ("seq", ("assign", "x", ("int", 1)), ("call", "g", [])), [F, G])

# fact(n) declares times(k) = k * n, which reads n from the frame of fact.
TIMES = ("fun", "times", ["k"], [], ("mul", ("var", "k"), ("var", "n")), [])
FACT = (
    "fun",
    "fact",
    ["n"],
    [],
    ("if", ("lt", ("var", "n"), ("int", 2)), ("int", 1), ("call", "times", [("call", "fact", [("sub", ("var", "n"), ("int", 1))])])),
    [TIMES],
)
FACT_MAIN = ("fun", "main", [], [], ("call", "fact", [("int", 6)]), [FACT])


def outcome(f, *args) -> object:
    try:
        return f(*args)
    except OutOfFuel:
        return "fuel"


def test_static_link_against_dynamic_link() -> None:
    assert evaluate(SCOPE) == 1
    assert run_machine(compile_program(SCOPE)) == 1
    assert run_machine(compile_program(SCOPE, "display")) == 1
    # Following the dynamic link finds y in the frame of g: dynamic scope.
    assert run_machine(compile_program(SCOPE), follow="dynamic") == 2


def test_recursion_with_a_nested_function() -> None:
    assert evaluate(FACT_MAIN) == 720
    assert run_machine(compile_program(FACT_MAIN)) == 720
    assert run_machine(compile_program(FACT_MAIN, "display")) == 720


def random_program(rng: random.Random) -> tuple:
    """A random program with functions nested up to depth 3."""
    pool = ["a", "b", "c", "d"]
    fnames = ["f", "g", "h"]

    def skeleton(name: str, depth: int) -> dict:
        names = rng.sample(pool, rng.randint(0, 3))
        cut = 0 if name == "main" else rng.randint(0, len(names))
        kids = []
        if depth < 3:
            for fn in rng.sample(fnames, rng.randint(0, 2)):
                kids.append(skeleton(fn, depth + 1))
        return {"name": name, "params": names[:cut], "locals": names[cut:], "kids": kids}

    def visible(chain: list) -> tuple[list, list]:
        # An inner declaration hides an outer one with the same name.
        vs: list = []
        fs: dict = {}
        for s in chain:
            vs += s["params"] + s["locals"]
            for k in s["kids"]:
                fs[k["name"]] = k
        return sorted(set(vs)), list(fs.values())

    def expr(chain: list, size: int) -> tuple:
        vs, fs = visible(chain)
        r = rng.random()
        if size <= 1 or r < 0.15:
            if vs and rng.random() < 0.6:
                return ("var", rng.choice(vs))
            return ("int", rng.randint(-3, 5))
        if r < 0.3 and vs:
            return ("assign", rng.choice(vs), expr(chain, size - 1))
        if r < 0.4:
            return ("seq", expr(chain, size // 2), expr(chain, size // 2))
        if r < 0.55:
            return ("if", expr(chain, size // 3), expr(chain, size // 3), expr(chain, size // 3))
        if r < 0.75 and fs:
            f = rng.choice(fs)
            return ("call", f["name"], [expr(chain, size // 3) for _ in f["params"]])
        op = rng.choice(["add", "sub", "mul", "lt"])
        return (op, expr(chain, size // 2), expr(chain, size // 2))

    def build(s: dict, chain: list) -> tuple:
        chain = chain + [s]
        body = expr(chain, rng.randint(1, 10))
        return ("fun", s["name"], s["params"], s["locals"], body, [build(k, chain) for k in s["kids"]])

    return build(skeleton("main", 0), [])


def test_random_programs_against_the_evaluator() -> None:
    rng = random.Random(1960)
    differ = 0
    done = 0
    for _ in range(1500):
        prog = random_program(rng)
        want = outcome(evaluate, prog, 50)
        assert outcome(run_machine, compile_program(prog), 50) == want
        assert outcome(run_machine, compile_program(prog, "display"), 50) == want
        done += want != "fuel"
        try:
            differ += run_machine(compile_program(prog), 50, "dynamic") != want
        except (OutOfFuel, IndexError):
            differ += 1
    assert done > 1000
    assert differ > 20
