# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boolean-masking/. The authors are listed in prov/H7YXSN.jsonl.

import itertools
import random
from collections import Counter

from boolean_masking import (
    PRESENT_SBOX,
    gf2_linear,
    masked_sbox,
    masked_sbox_wires,
    three_share_linear_wires,
    wrong_order_wires,
)

# An invertible GF(2)-linear map on 4 bits: output bit i is the parity of v AND ROWS[i].
ROWS = (0b0011, 0b0110, 0b1100, 0b1001 ^ 0b0001)


def runs_first_order(gadget, p):
    """For each key k, the wire vectors over all 256 pairs of masks."""
    return {
        k: [gadget(p, k, mi, mo)[1] for mi in range(16) for mo in range(16)]
        for k in range(16)
    }


def leaking(runs, t):
    """The sets of at most t wires whose joint distribution depends on the key."""
    names = [n for n, _ in next(iter(runs.values()))[0]]
    # cols[key][q] lists the values of wire q over all runs for that key.
    cols = [[[w[q][1] for w in vecs] for q in range(len(names))] for vecs in runs.values()]
    out = []
    for size in range(1, t + 1):
        for probe in itertools.combinations(range(len(names)), size):
            first = Counter(zip(*(cols[0][q] for q in probe)))
            if any(Counter(zip(*(c[q] for q in probe))) != first for c in cols[1:]):
                out.append(tuple(names[q] for q in probe))
    return out


def test_worked_example() -> None:
    (y, mo), wires = masked_sbox_wires(0x3, 0xB, 0x5, 0x9)
    w = dict(wires)
    assert w["p+m_in"] == 0x6 and w["x'"] == 0xD
    assert y == 0xA and mo == 0x9
    assert y ^ mo == PRESENT_SBOX[0x3 ^ 0xB] == 0x3


def test_correct_for_all_inputs_and_masks() -> None:
    for p, k, mi, mo in itertools.product(range(16), repeat=4):
        (y, m), _ = masked_sbox_wires(p, k, mi, mo)
        assert y ^ m == PRESENT_SBOX[p ^ k]


def test_random_oracle() -> None:
    rng = random.Random(20240508)
    for _ in range(500):
        p, k = rng.randrange(16), rng.randrange(16)
        y, m = masked_sbox(rng, p, k)
        assert y ^ m == PRESENT_SBOX[p ^ k]


def test_first_order_secure() -> None:
    # Every single wire, for three public inputs, over all keys and all 256 pairs of masks.
    for p in (0x0, 0x3, 0xC):
        assert leaking(runs_first_order(masked_sbox_wires, p), 1) == []


def test_second_order_leaks() -> None:
    # All 210 pairs of the 21 wires: exactly three pairs depend on the key.
    leaks = leaking(runs_first_order(masked_sbox_wires, 0x3), 2)
    assert sorted(leaks) == sorted([("m_in", "x'"), ("p+m_in", "x'"), ("m_out", "y'")])


def test_wrong_order_leaks_with_one_probe() -> None:
    assert leaking(runs_first_order(wrong_order_wires, 0x3), 1) == [("p+k",)]


def test_linear_map_is_invertible() -> None:
    assert sorted(gf2_linear(ROWS, v) for v in range(16)) == list(range(16))


def test_three_shares_resist_two_probes() -> None:
    for p in (0x0, 0x7):
        runs = {}
        for k in range(16):
            vecs = []
            for k1, k2 in itertools.product(range(16), repeat=2):
                y, w = three_share_linear_wires(p, (k1, k2, k ^ k1 ^ k2), ROWS)
                assert y[0] ^ y[1] ^ y[2] == gf2_linear(ROWS, p ^ k)
                vecs.append(w)
            runs[k] = vecs
        assert leaking(runs, 2) == []
        assert ("k1", "k2", "k3") in leaking(runs, 3)


def test_second_order_leakage_expectation() -> None:
    hw = lambda v: bin(v).count("1")  # noqa: E731
    for x in range(16):
        assert sum(hw(x ^ m) for m in range(16)) == 32
        e = sum((hw(x ^ m) - 2) * (hw(m) - 2) for m in range(16)) / 16
        assert e == 1 - hw(x) / 2
