# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-random-access-memory/. The authors are listed in prov/Q40QQ0.jsonl.

import cmath
import itertools
import math
import random

import pytest

from qsim import apply_permutation, close
from quantum_random_access_memory import QRAM, W, oracle, serial_steps


def random_state(n: int, rng: random.Random) -> dict:
    amps = {(i, b): complex(rng.gauss(0, 1), rng.gauss(0, 1)) for i in range(1 << n) for b in (0, 1)}
    s = math.sqrt(sum(abs(a) ** 2 for a in amps.values()))
    return {k: a / s for k, a in amps.items()}


def test_every_memory_and_every_basis_input_for_small_n() -> None:
    for n in (1, 2, 3):
        for bits in itertools.product((0, 1), repeat=1 << n):
            q = QRAM(n, list(bits))
            for i in range(1 << n):
                for b in (0, 1):
                    assert q.query({(i, b): 1}) == {(i, b ^ bits[i]): 1}
                    assert q._branch(i, b)[4] == i  # the bus reached cell i
            q.check_invariant()


def test_superposition_query_matches_the_oracle_and_qsim() -> None:
    rng = random.Random(5051)
    for n in (1, 2, 3, 4, 5):
        data = [rng.randrange(2) for _ in range(1 << n)]
        q = QRAM(n, data)
        psi = random_state(n, rng)
        out = q.query(psi)
        ref = oracle(data, psi)
        assert set(out) == set(ref) and all(abs(out[k] - ref[k]) < 1e-12 for k in ref)
        assert abs(sum(abs(a) ** 2 for a in out.values()) - 1) < 1e-12  # norm is kept
        # the same map on a state vector of n + 1 qubits: bus on qubit 0, address on qubits 1 .. n
        vec = [psi[(x >> 1, x & 1)] for x in range(1 << (n + 1))]
        perm = [((x >> 1) << 1) | ((x & 1) ^ data[x >> 1]) for x in range(1 << (n + 1))]
        got = [out[(x >> 1, x & 1)] for x in range(1 << (n + 1))]
        assert close(apply_permutation(vec, perm), got)


def test_query_twice_is_identity_and_phase_oracle() -> None:
    rng = random.Random(5052)
    n = 3
    data = [rng.randrange(2) for _ in range(1 << n)]
    q = QRAM(n, data)
    psi = random_state(n, rng)
    back = q.query(q.query(psi))
    assert all(abs(back[k] - psi[k]) < 1e-12 for k in psi)
    # with the bus in |->, a query gives the phase (-1)^(x_i) (phase kickback)
    r = 1 / math.sqrt(2)
    amps = [cmath.exp(0.3j * i) / math.sqrt(1 << n) for i in range(1 << n)]
    minus = {}
    for i, a in enumerate(amps):
        minus[(i, 0)] = a * r
        minus[(i, 1)] = -a * r
    out = q.query(minus)
    for i, a in enumerate(amps):
        s = (-1) ** data[i]
        assert abs(out[(i, 0)] - s * a * r) < 1e-12 and abs(out[(i, 1)] + s * a * r) < 1e-12


def test_only_n_routers_are_active_and_they_hold_the_address() -> None:
    for n in (1, 2, 3, 4, 5, 6):
        q = QRAM(n)
        configs = set()
        for i in range(1 << n):
            routers = q.router_state_after_load(i)
            active = [k for k in range(1, 1 << n) if routers[k] != W]
            assert len(active) == n  # n of the N - 1 routers, one per level
            # they are the path from the root to cell i
            node = 1
            for j in range(n):
                assert node in active and routers[node] == (i >> (n - 1 - j)) & 1
                node = 2 * node + routers[node]
            assert node - (1 << n) == i
            configs.add(routers)
        # the routers hold which-address information, so the query must reset them
        assert len(configs) == 1 << n
        q.query({(0, 0): 1})
        assert q.last_stats == {"steps": serial_steps(n), "active_routers": n}


def test_random_operations_against_a_dict_model() -> None:
    rng = random.Random(5053)
    n = 4
    q = QRAM(n)
    model = {i: 0 for i in range(1 << n)}
    for _ in range(300):
        op = rng.randrange(3)
        i = rng.randrange(1 << n)
        if op == 0:
            bit = rng.randrange(2)
            q.write(i, bit)
            model[i] = bit
        elif op == 1:
            assert q.read(i) == model[i]
        else:
            psi = random_state(n, rng) if rng.random() < 0.3 else {(i, rng.randrange(2)): 1}
            out = q.query(psi)
            for (a, b), amp in psi.items():
                assert abs(out[(a, b ^ model[a])] - amp) < 1e-12
        q.check_invariant()


def test_bad_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        QRAM(0)
    with pytest.raises(ValueError):
        QRAM(2, [0, 1, 2, 0])
    q = QRAM(2)
    with pytest.raises(ValueError):
        q.write(4, 1)
    with pytest.raises(ValueError):
        q.query({(5, 0): 1})
