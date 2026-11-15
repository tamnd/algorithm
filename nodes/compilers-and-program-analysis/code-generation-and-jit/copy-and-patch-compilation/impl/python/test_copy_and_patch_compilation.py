# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/copy-and-patch-compilation/. The authors are listed in prov/KRGC64.jsonl.

import random

import pytest

import toyir
from copy_and_patch_compilation import (
    STENCILS,
    compile_program,
    disassemble,
    example,
    run,
)

ARGS = [(0, 0), (1, 2), (3, -1), (5, 7), (-4, 2), (9, 0), (2, 3)]


def add_phis(rng, prog):
    """Put phis for the variables x0, x1, ... at the top of some blocks. The
    entry of random_program defines every x, so every operand is defined."""
    xs = sorted({ins[1] for ins in prog.blocks[prog.entry].instrs if ins[1].startswith("x")} | set(prog.params))
    pr = toyir.preds(prog)
    for label, b in prog.blocks.items():
        if label == prog.entry or not pr[label] or rng.random() < 0.4:
            continue
        dests = rng.sample(xs, min(len(xs), rng.randint(1, 3)))
        new = []
        for x in dests:
            args = {p: (rng.randint(-3, 9) if rng.random() < 0.25 else rng.choice(xs)) for p in pr[label]}
            new.append(("phi", x, args))
        b.instrs[0:0] = new
    return prog


def check_layout(prog, c):
    """The stencils tile the code, each copied unchanged except at its holes,
    and each hole holds the value that was patched into it."""
    pc = 0
    for at, st, values in c.placements:
        assert at == pc
        holes = dict(st.holes)
        for i, w in enumerate(st.code):
            if i in holes:
                assert c.code[at + i] == values[holes[i]]
            else:
                assert c.code[at + i] == w
        assert set(values) == set(holes.values())
        pc += len(st)
    assert pc == len(c.code)


def same(prog, args, fuel=10000):
    expect = toyir.run(prog, args, fuel)
    got = run(prog, args, fuel)
    assert got == expect, (toyir.show(prog), args, fuel, got, expect)
    return expect


def test_example():
    prog, c = example()
    assert len(c.code) == 68
    assert c.names == ["n", "s", "i", "c"]
    assert [st.name for _, st, _ in c.placements] == [
        "const", "const", "jump_next", "op<_vv", "br_v", "op+_vv", "op+_vi", "jump", "ret_v",
    ]
    assert c.placements[4][2] == {"a": 3, "t": 35, "f": 62}
    assert c.placements[7][2] == {"t": 15}
    lines = disassemble(c)
    assert lines[7:9] == [" 15  TICK", " 16  LDS 0 2"]
    assert lines[14] == " 31  BR 0 35 62"
    assert c.run([4]) == ("ret", 6)
    assert c.run([100]) == ("ret", 4950)
    for n in range(-2, 12):
        same(prog, [n])
    check_layout(prog, c)


def test_library():
    # 1 const, 2 each of copy, br, ret and phi, 4 times 14 operators, and
    # jump, jump-next, move and goto.
    assert len(STENCILS) == 1 + 8 + 56 + 4
    st = STENCILS[("op", "+", "v", "i")]
    assert st.code == (1, 2, 0, 0, 3, 1, 0, 5, 0, 4, 0, 0)
    assert st.holes == ((3, "a"), (6, "b"), (10, "x"))


@pytest.mark.parametrize("acyclic", [True, False])
def test_random_programs(acyclic):
    rng = random.Random(1 if acyclic else 2)
    for _ in range(250):
        prog = toyir.random_program(rng, rng.randint(2, 6), rng.randint(1, 8), acyclic)
        c = compile_program(prog)
        check_layout(prog, c)
        for a in ARGS:
            assert c.run(list(a)) == toyir.run(prog, list(a))


def test_random_programs_with_phis():
    rng = random.Random(3)
    nphis = 0
    for _ in range(250):
        prog = toyir.random_program(rng, rng.randint(2, 6), rng.randint(2, 8), rng.random() < 0.5)
        add_phis(rng, prog)
        nphis += sum(ins[0] == "phi" for b in prog.blocks.values() for ins in b.instrs)
        c = compile_program(prog)
        check_layout(prog, c)
        for a in ARGS:
            same(prog, list(a))
    assert nphis > 300


def test_every_fuel_value():
    # The compiled code runs out of fuel at exactly the same point.
    rng = random.Random(4)
    for _ in range(40):
        prog = toyir.random_program(rng, 4, rng.randint(2, 7), False)
        add_phis(rng, prog)
        a = [rng.randint(0, 5), rng.randint(-3, 5)]
        need = 0
        while toyir.run(prog, a, need) == ("fuel",):
            need += 1
        for f in range(0, need + 2):
            same(prog, a, f)


def test_traps():
    prog = toyir.parse("# params: a, b\nB0:\n  q = a / b\n  r = a % b\n  s = q << r\n  ret s\n")
    for a, b in [(7, 2), (-7, 2), (7, -2), (-7, -2), (5, 0), (1, 70), (-1, 64)]:
        same(prog, [a, b])
    assert run(prog, [7, 0]) == ("trap",)
    assert run(prog, [7, 2]) == ("ret", 6)
    # -7 / 2 is -3 and -7 % 2 is -1, and a shift by -1 traps.
    assert run(prog, [-7, 2]) == ("trap",)


def test_parallel_phis():
    # The two phis swap a and b on each round, so they must read before they write.
    text = """
    # params: a, b, n
    B0:
      i = 0
      jump B1
    B1:
      x = phi [B0: a, B2: y]
      y = phi [B0: b, B2: x]
      c = i < n
      br c B2 B3
    B2:
      i = i + 1
      jump B1
    B3:
      r = x * 10
      r = r + y
      ret r
    """
    prog = toyir.parse(text)
    for n in range(5):
        same(prog, [1, 2, n])
    assert run(prog, [1, 2, 3]) == ("ret", 21)
    assert run(prog, [1, 2, 4]) == ("ret", 12)


def test_jump_to_next_block_is_left_out():
    prog = toyir.parse("# params: a\nB0:\n  x = a + 1\n  jump B1\nB1:\n  ret x\n")
    c = compile_program(prog)
    assert [st.name for _, st, _ in c.placements] == ["op+_vi", "jump_next", "ret_v"]
    assert run(prog, [4]) == ("ret", 5)
    prog = toyir.parse("# params: a\nB0:\n  x = a + 1\n  jump B2\nB1:\n  ret 0\nB2:\n  ret x\n")
    c = compile_program(prog)
    assert [st.name for _, st, _ in c.placements] == ["op+_vi", "jump", "ret_i", "ret_v"]
    assert run(prog, [4]) == ("ret", 5)


def test_rejects():
    with pytest.raises(ValueError):
        compile_program(toyir.parse("# params: p\nB0:\n  x = *p\n  ret x\n"))
    with pytest.raises(ValueError):
        compile_program(toyir.parse("# params: a\nB0:\n  x = phi [B0: a]\n  ret x\n"))
    with pytest.raises(ValueError):
        run(toyir.parse("# params: a\nB0:\n  ret a\n"), [1, 2])
    with pytest.raises(toyir.UndefinedName):
        run(toyir.parse("# params: a\nB0:\n  ret z\n"), [1])
