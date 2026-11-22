# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shadow-stack/. The authors are listed in prov/5QQA10.jsonl.

import random

import pytest

from shadow_stack import ShadowStack, ShadowStackFault, run_trace


def test_example_of_the_page() -> None:
    trace = [
        ("call", "r1"),
        ("call", "r2"),
        ("ret",),
        ("call", "r3"),
        ("write", 0, "x"),
        ("ret",),
        ("ret",),
    ]
    assert run_trace(trace) == (["r2"], 5, "mismatch")


def test_example_without_the_write() -> None:
    trace = [("call", "r1"), ("call", "r2"), ("ret",), ("call", "r3"), ("ret",), ("ret",)]
    assert run_trace(trace) == (["r2", "r3", "r1"], None, None)


def test_longjmp_example() -> None:
    trace = [
        ("call", "r1"),
        ("setjmp", "j"),
        ("call", "r2"),
        ("call", "r3"),
        ("longjmp", "j"),
        ("ret",),
    ]
    assert run_trace(trace) == (["r1"], None, None)


def test_write_of_the_same_value_is_not_a_fault() -> None:
    trace = [("call", "r1"), ("write", 0, "r1"), ("ret",)]
    assert run_trace(trace) == (["r1"], None, None)


def test_write_to_a_deeper_frame_is_caught_later() -> None:
    trace = [("call", "r1"), ("call", "r2"), ("write", 1, "x"), ("ret",), ("ret",)]
    assert run_trace(trace) == (["r2"], 4, "mismatch")


def test_faults_of_the_operations() -> None:
    s = ShadowStack(2)
    with pytest.raises(ShadowStackFault) as e:
        s.check_return("r1")
    assert e.value.kind == "empty"
    s.push("a")
    s.push("b")
    with pytest.raises(ShadowStackFault) as e:
        s.push("c")
    assert e.value.kind == "full"
    with pytest.raises(ShadowStackFault) as e:
        s.restore(3)
    assert e.value.kind == "restore"
    with pytest.raises(ShadowStackFault) as e:
        s.check_return("a")
    assert e.value.kind == "mismatch"
    assert s.depth() == 1
    assert run_trace([("call", "a"), ("call", "b")], capacity=1) == ([], 1, "full")
    with pytest.raises(ValueError):
        ShadowStack(0)


def test_random_operations_against_a_list() -> None:
    rng = random.Random(5150)
    for _ in range(600):
        cap = rng.randint(1, 6)
        s = ShadowStack(cap)
        model: list[int] = []
        for _ in range(rng.randint(0, 30)):
            op = rng.random()
            if op < 0.4:
                a = rng.randint(0, 3)
                if len(model) == cap:
                    with pytest.raises(ShadowStackFault):
                        s.push(a)
                else:
                    s.push(a)
                    model.append(a)
            elif op < 0.8:
                r = rng.randint(0, 3)
                if not model:
                    with pytest.raises(ShadowStackFault):
                        s.check_return(r)
                else:
                    top = model.pop()
                    if top == r:
                        assert s.check_return(r) == r
                    else:
                        with pytest.raises(ShadowStackFault):
                            s.check_return(r)
            else:
                d = rng.randint(0, cap + 1)
                if d > len(model):
                    with pytest.raises(ShadowStackFault):
                        s.restore(d)
                else:
                    s.restore(d)
                    del model[d:]
            s.check_invariant()
            assert s.depth() == len(model)
            assert s.entries() == model


def random_trace(rng: random.Random, jumps: bool) -> list[tuple]:
    """A trace that satisfies the precondition of run_trace."""
    trace: list[tuple] = []
    depth = 0
    saved: dict[str, int] = {}
    for _ in range(rng.randint(0, 25)):
        op = rng.random()
        if op < 0.4 or depth == 0:
            trace.append(("call", "r" + str(rng.randint(0, 4))))
            depth += 1
        elif op < 0.75:
            trace.append(("ret",))
            depth -= 1
        elif op < 0.9:
            k = rng.randrange(depth)
            trace.append(("write", k, rng.choice(["r0", "r1", "x", "y"])))
        elif jumps:
            if saved and rng.random() < 0.5:
                name = rng.choice(sorted(saved))
                if saved[name] <= depth:
                    trace.append(("longjmp", name))
                    depth = saved[name]
            else:
                name = "j" + str(rng.randint(0, 2))
                trace.append(("setjmp", name))
                saved[name] = depth
    return trace


def observed_and_intended(trace: list[tuple]) -> list[tuple[int, str, str]]:
    """For each return: its index, the value read from the normal stack, and the
    return address of its matching call, found by a backward scan."""
    normal: list[str] = []
    out = []
    for j, ev in enumerate(trace):
        if ev[0] == "call":
            normal.append(ev[1])
        elif ev[0] == "write":
            normal[len(normal) - 1 - ev[1]] = ev[2]
        elif ev[0] == "ret":
            seen = normal.pop()
            count = 0
            for i in range(j - 1, -1, -1):
                if trace[i][0] == "ret":
                    count += 1
                elif trace[i][0] == "call":
                    if count == 0:
                        out.append((j, seen, trace[i][1]))
                        break
                    count -= 1
    return out


def test_random_traces_against_call_matching() -> None:
    rng = random.Random(1972)
    for _ in range(800):
        trace = random_trace(rng, jumps=False)
        rets = observed_and_intended(trace)
        bad = [j for (j, seen, want) in rets if seen != want]
        targets, idx, kind = run_trace(trace)
        if bad:
            assert (idx, kind) == (bad[0], "mismatch")
        else:
            assert (idx, kind) == (None, None)
        assert targets == [want for (j, seen, want) in rets if idx is None or j < idx]


def test_random_traces_with_jumps_against_a_model() -> None:
    rng = random.Random(2019)
    for _ in range(800):
        trace = random_trace(rng, jumps=True)
        pending: list[str] = []
        normal: list[str] = []
        saved: dict[str, int] = {}
        expect: tuple[list[str], int | None, str | None] = ([], None, None)
        taken: list[str] = []
        for i, ev in enumerate(trace):
            if ev[0] == "call":
                pending.append(ev[1])
                normal.append(ev[1])
            elif ev[0] == "write":
                normal[len(normal) - 1 - ev[1]] = ev[2]
            elif ev[0] == "setjmp":
                saved[ev[1]] = len(pending)
            elif ev[0] == "longjmp":
                del pending[saved[ev[1]]:]
                del normal[saved[ev[1]]:]
            else:
                want, seen = pending.pop(), normal.pop()
                if want != seen:
                    expect = (taken, i, "mismatch")
                    break
                taken.append(want)
        else:
            expect = (taken, None, None)
        assert run_trace(trace) == expect


def test_no_false_alarm_without_writes() -> None:
    rng = random.Random(7)
    for _ in range(500):
        trace = [ev for ev in random_trace(rng, jumps=True) if ev[0] != "write"]
        assert run_trace(trace)[1] is None
