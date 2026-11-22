# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constant-time-verification/. The authors are listed in prov/B355TH.jsonl.

import random
from itertools import product as cartesian

from constant_time_verification import cache_cost, ct_verif, product, run

W = 4
T = {"T": [3, 1, 0, 2]}


def v(x):
    return ("v", x)


def c(n):
    return ("c", n)


# An independent interpreter for the oracle. It returns the final variables
# and the trace of leakage events of one run.
def oracle_run(prog, inputs, tables, w=W):
    env = dict(inputs)
    mem = {a: list(t) for a, t in tables.items()}
    events = []

    def ev(e):
        k = e[0]
        if k == "c":
            return e[1] % w
        if k == "v":
            return env.get(e[1], 0)
        if k == "ld":
            i = ev(e[2])
            events.append(("addr", e[1], i))
            return mem[e[1]][i]
        x, y = ev(e[1]), ev(e[2])
        if k == "div":
            events.append(("div", x, y))
            return 0 if y == 0 else x // y
        table = {
            "+": lambda: (x + y) % w,
            "-": lambda: (x - y) % w,
            "*": lambda: (x * y) % w,
            "&": lambda: (x & y) % w,
            "|": lambda: (x | y) % w,
            "^": lambda: (x ^ y) % w,
            "<": lambda: int(x < y),
            "==": lambda: int(x == y),
        }
        return table[k]()

    def ex(block):
        for s in block:
            if s[0] == "set":
                env[s[1]] = ev(s[2])
            elif s[0] == "st":
                i = ev(s[2])
                val = ev(s[3])
                events.append(("addr", s[1], i))
                mem[s[1]][i] = val
            elif s[0] == "if":
                b = ev(s[1]) != 0
                events.append(("br", b))
                ex(s[2] if b else s[3])
            else:
                n = ev(s[1])
                events.append(("loop", n))
                for _ in range(n):
                    ex(s[2])

    ex(prog)
    return env, events


def oracle_ct(prog, public, secret, tables, w=W):
    """Run every pair of start states with equal public inputs twice."""
    space = list(cartesian(range(w), repeat=len(secret)))
    for pv in cartesian(range(w), repeat=len(public)):
        traces = set()
        for sv in space:
            inputs = dict(zip(public, pv)) | dict(zip(secret, sv))
            traces.add(tuple(oracle_run(prog, inputs, tables, w)[1]))
        if len(traces) > 1:
            return False
    return True


def check(prog, expected, public=("p",), secret=("s",)):
    ok, pair = ct_verif(prog, public, secret, T, W)
    assert ok == expected
    assert oracle_ct(prog, public, secret, T) == expected
    if not ok:
        a, b = pair
        assert all(a[x] == b[x] for x in public)
        assert oracle_run(prog, a, T)[1] != oracle_run(prog, b, T)[1]
    else:
        assert pair is None


def masked_lookup():
    # y = T[0] & m0 | T[1] & m1 | ..., with mj = 0 - (j == s), all ones or 0.
    prog = [("set", "y", c(0))]
    for j in range(W):
        mask = ("-", c(0), ("==", c(j), v("s")))
        prog.append(("set", "y", ("|", v("y"), ("&", ("ld", "T", c(j)), mask))))
    return prog


def test_secret_index_lookup_is_not_constant_time():
    check([("set", "y", ("ld", "T", v("s")))], False)


def test_public_index_lookup_is_constant_time():
    check([("set", "y", ("ld", "T", v("p")))], True)


def test_masked_lookup_is_constant_time_and_correct():
    prog = masked_lookup()
    assert len(prog) <= 10
    check(prog, True)
    for s in range(W):
        env, _ = run(prog, {"p": 0, "s": s}, T, W)
        assert env["y"] == T["T"][s]


def test_secret_branch_is_not_constant_time():
    check([("if", v("s"), [("set", "y", c(1))], [("set", "y", c(2))])], False)


def test_branch_on_s_xor_s_is_constant_time():
    # A security type system rejects this program; the product accepts it.
    check([("if", ("^", v("s"), v("s")), [("set", "y", ("ld", "T", v("s")))], [("set", "y", c(2))])], True)


def test_division_leaks_its_operands():
    check([("set", "y", ("div", v("p"), v("s")))], False)
    check([("set", "y", ("div", v("p"), c(1)))], True)


def test_loop_count():
    check([("rep", v("s"), [("set", "y", ("+", v("y"), c(1)))])], False)
    check([("rep", v("p"), [("set", "y", ("+", v("y"), v("s")))])], True)


def test_flow_through_a_variable():
    check([("set", "x", v("s")), ("set", "y", ("ld", "T", v("x")))], False)
    check([("set", "x", ("^", v("s"), v("s"))), ("set", "y", ("ld", "T", v("x")))], True)


def test_store_to_secret_index():
    check([("st", "T", v("s"), c(0))], False)
    check([("st", "T", v("p"), v("s")), ("set", "y", ("ld", "T", v("p")))], True)
    # The stored secret later becomes an index.
    check([("st", "T", c(0), v("s")), ("set", "y", ("ld", "T", ("ld", "T", c(0))))], False)


def test_product_keeps_the_control_structure():
    prog = [
        ("if", v("p"), [("rep", v("p"), [("set", "y", c(1))])], []),
        ("set", "x", ("ld", "T", v("p"))),
    ]
    q = product(prog)

    def shape(block):
        return [(s[0], [shape(b) for b in s[2:] if isinstance(b, list)]) for s in block if s[0] in ("if", "rep")]

    assert shape(q) == shape(prog)
    assert sum(1 for s in q if s[0] == "assert") == len(prog)


def test_two_secrets():
    prog = [("set", "y", ("ld", "T", ("&", v("s"), v("k"))))]
    for s in (prog, [("set", "y", ("&", ("ld", "T", v("p")), ("^", v("s"), v("k"))))]):
        ok, _ = ct_verif(s, ("p",), ("s", "k"), T, W)
        assert ok == oracle_ct(s, ("p",), ("s", "k"), T)
    assert not ct_verif(prog, ("p",), ("s", "k"), T, W)[0]


def test_cache_cost_example():
    prog = [("set", "x", ("ld", "T", c(0))), ("set", "y", ("ld", "T", v("s")))]
    base = {"T": 0}
    costs = {cache_cost(run(prog, {"p": 0, "s": s}, T, W)[1], base, sets=4, ways=1, line=1) for s in range(W)}
    assert costs == {11, 20}
    costs = {cache_cost(run(masked_lookup(), {"p": 0, "s": s}, T, W)[1], base, sets=4, ways=1, line=1) for s in range(W)}
    assert len(costs) == 1


def test_lru_order():
    trace = [("addr", "T", 0), ("addr", "T", 2), ("addr", "T", 0), ("addr", "T", 1)]
    # One set, two ways, lines of one cell: miss, miss, hit, miss.
    assert cache_cost(trace, {"T": 0}, sets=1, ways=2, line=1) == 31
    trace = [("addr", "T", 0), ("addr", "T", 2), ("addr", "T", 1), ("addr", "T", 0)]
    # Cell 0 was evicted by cell 1 as the least recently used line.
    assert cache_cost(trace, {"T": 0}, sets=1, ways=2, line=1) == 40


def random_expr(rng, depth):
    r = rng.random()
    if depth == 0 or r < 0.3:
        return v(rng.choice("psxy")) if rng.random() < 0.7 else c(rng.randrange(W))
    if r < 0.5:
        return ("ld", "T", random_expr(rng, depth - 1))
    if r < 0.58:
        return ("div", random_expr(rng, depth - 1), random_expr(rng, depth - 1))
    op = rng.choice(["+", "-", "*", "&", "|", "^", "<", "=="])
    return (op, random_expr(rng, depth - 1), random_expr(rng, depth - 1))


def random_block(rng, size, depth):
    block = []
    for _ in range(size):
        r = rng.random()
        if depth > 0 and r < 0.2:
            block.append(("if", random_expr(rng, 1), random_block(rng, 1, depth - 1), random_block(rng, 1, depth - 1)))
        elif depth > 0 and r < 0.3:
            block.append(("rep", random_expr(rng, 1), random_block(rng, 1, depth - 1)))
        elif r < 0.4:
            block.append(("st", "T", random_expr(rng, 1), random_expr(rng, 1)))
        else:
            block.append(("set", rng.choice("xy"), random_expr(rng, 2)))
    return block


def test_random_programs_against_the_two_run_oracle():
    rng = random.Random(20160810)
    seen = {True: 0, False: 0}
    cache_checked = 0
    for _ in range(600):
        prog = random_block(rng, rng.randrange(1, 5), 1)
        ok, pair = ct_verif(prog, ("p",), ("s",), T, W)
        assert ok == oracle_ct(prog, ("p",), ("s",), T), prog
        seen[ok] += 1
        if not ok:
            a, b = pair
            assert a["p"] == b["p"]
            assert oracle_run(prog, a, T)[1] != oracle_run(prog, b, T)[1]
        elif cache_checked < 100:
            # A constant-time program has one cache cost for each public input.
            cache_checked += 1
            for p in range(W):
                costs = {cache_cost(run(prog, {"p": p, "s": s}, T, W)[1], {"T": 0}, sets=2, ways=1, line=1) for s in range(W)}
                assert len(costs) == 1
    assert seen[True] >= 100 and seen[False] >= 100
