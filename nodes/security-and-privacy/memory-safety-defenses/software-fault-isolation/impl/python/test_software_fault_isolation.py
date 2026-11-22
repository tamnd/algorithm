# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/software-fault-isolation/. The authors are listed in prov/BDGPFB.jsonl.

import random

import pytest

from software_fault_isolation import SFIError, rewrite, run, sandbox_address, verify

G, M, W = 5, 10, 16
REGS = ["a", "b", "c"]
D = "d"


def in_domain(address: int) -> bool:
    """Independent oracle: the address lies in [G * 2**M, (G + 1) * 2**M)."""
    return G * 2**M <= address < (G + 1) * 2**M


def random_module(rng: random.Random, allow_ijump: bool = True, allow_load: bool = True) -> list:
    n = rng.randint(1, 10)
    ops = ["li", "add", "store", "store", "jnz", "halt"]
    if allow_ijump:
        ops.append("ijump")
    if allow_load:
        ops.append("load")
    module = []
    for _ in range(n):
        op = rng.choice(ops)
        r1, r2, r3 = (rng.choice(REGS) for _ in range(3))
        if op == "li":
            module.append(("li", r1, rng.randrange(2**W)))
        elif op == "add":
            module.append(("add", r1, r2, r3))
        elif op == "load":
            module.append(("load", r1, r2))
        elif op == "store":
            module.append(("store", r1, r2))
        elif op == "jnz":
            module.append(("jnz", r1, rng.randint(0, n)))
        elif op == "ijump":
            module.append(("ijump", r1))
        else:
            module.append(("halt",))
    return module


def random_regs(rng: random.Random) -> dict:
    regs = {r: rng.randrange(2**W) for r in REGS}
    regs[D] = G * 2**M + rng.randrange(2**M)
    return regs


EXAMPLE = [("li", "a", 3), ("li", "b", 7), ("store", "a", "b"), ("halt",)]


def test_example_of_the_page() -> None:
    assert run(EXAMPLE, {}, G, M) == ("halt", [(3, 7)])
    masked = rewrite(EXAMPLE, D, "mask")
    assert masked == [("li", "a", 3), ("li", "b", 7), ("sandbox", D, "a"), ("store", D, "b"), ("halt",)]
    assert run(masked, {D: G * 2**M}, G, M) == ("halt", [(5123, 7)])
    checked = rewrite(EXAMPLE, D, "check")
    assert run(checked, {D: G * 2**M}, G, M) == ("fault", [])


def test_sandbox_address_values() -> None:
    assert sandbox_address(3, G, M) == 5123
    assert sandbox_address(5123, G, M) == 5123
    assert sandbox_address(2**W - 1, G, M) == G * 2**M + 2**M - 1


def test_verifier_decisions() -> None:
    assert not verify(EXAMPLE, D)
    assert verify(rewrite(EXAMPLE, D), D)
    assert not verify([("li", D, 3), ("store", D, "b")], D)
    assert not verify([("add", D, "a", "b")], D)
    assert not verify([("load", D, "a")], D)
    assert not verify([("jnz", "a", 9)], D)
    assert verify([("store", D, "b"), ("sandbox", D, "a"), ("halt",)], D)


def test_rewrite_rejects_module_using_dedicated_register() -> None:
    with pytest.raises(SFIError):
        rewrite([("li", D, 1)], D)
    with pytest.raises(ValueError):
        rewrite(EXAMPLE, D, "other")


def test_jump_past_the_sandbox_step_stays_in_domain() -> None:
    # Jump straight to the store, skipping the sandbox step: d still holds a domain address.
    module = rewrite([("li", "a", 0), ("store", "a", "b"), ("halt",)], D)
    module = [("li", "c", 4), ("ijump", "c")] + module
    assert module[4] == ("store", D, "b")
    assert verify(module, D)
    status, stores = run(module, {D: G * 2**M + 17, "b": 9}, G, M)
    assert status == "halt"
    assert stores == [(G * 2**M + 17, 9)]


def test_rewritten_modules_store_only_in_domain() -> None:
    rng = random.Random(1993)
    for _ in range(800):
        module = random_module(rng)
        for mode in ("mask", "check"):
            out = rewrite(module, D, mode)
            assert verify(out, D)
            for _ in range(3):
                _, stores = run(out, random_regs(rng), G, M)
                assert all(in_domain(a) for a, _ in stores)


def test_any_verified_module_stores_only_in_domain() -> None:
    rng = random.Random(2009)
    checked = 0
    while checked < 600:
        module = random_module(rng)
        # Turn some stores into stores through d and scatter sandbox steps at random places.
        mixed = []
        for ins in module:
            if ins[0] == "store" and rng.random() < 0.8:
                ins = ("store", D, ins[2])
            if rng.random() < 0.3:
                mixed.append(("sandbox", D, rng.choice(REGS)))
            mixed.append(ins)
        mixed = [("jnz", i[1], min(i[2], len(mixed))) if i[0] == "jnz" else i for i in mixed]
        if not verify(mixed, D):
            assert any(i[0] == "store" and i[1] != D for i in mixed)
            continue
        checked += 1
        for _ in range(3):
            _, stores = run(mixed, random_regs(rng), G, M)
            assert all(in_domain(a) for a, _ in stores)


def test_transparent_when_stores_are_already_in_domain() -> None:
    rng = random.Random(1308)
    compared = 0
    for _ in range(3000):
        module = random_module(rng, allow_ijump=False)
        regs = random_regs(rng)
        status, stores = run(module, regs, G, M, budget=100)
        if status != "halt" or not all(in_domain(a) for a, _ in stores):
            continue
        compared += 1
        for mode in ("mask", "check"):
            assert run(rewrite(module, D, mode), regs, G, M, budget=200) == (status, stores)
    assert compared >= 500


def test_mask_maps_stores_and_check_faults_without_loads() -> None:
    rng = random.Random(4242)
    for _ in range(800):
        module = random_module(rng, allow_ijump=False, allow_load=False)
        regs = random_regs(rng)
        status, stores = run(module, regs, G, M, budget=100)
        if status != "halt":
            continue
        masked = run(rewrite(module, D, "mask"), regs, G, M, budget=200)
        assert masked == ("halt", [(sandbox_address(a, G, M), v) for a, v in stores])
        checked = run(rewrite(module, D, "check"), regs, G, M, budget=200)
        bad = [k for k, (a, _) in enumerate(stores) if not in_domain(a)]
        if bad:
            assert checked == ("fault", stores[: bad[0]])
        else:
            assert checked == ("halt", stores)
