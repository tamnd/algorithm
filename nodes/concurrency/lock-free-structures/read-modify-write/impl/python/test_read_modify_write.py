# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/read-modify-write/. The authors are listed in prov/Q90K2C.jsonl.

import itertools

import pytest

from explorer import Found, explore
from read_modify_write import (
    cas_fn,
    classify,
    double,
    identity,
    inc,
    nontrivial_point,
    or_two,
    put_seven,
    set_one,
    setup_for,
)

DOMAIN = range(8)
NONTRIVIAL = [inc, set_one, put_seven, double, or_two, cas_fn(0, 1), cas_fn(3, 5)]


def agreement(values):
    def check(w):
        if max(w.steps) > 3:
            return "more than 3 steps"
        dec = {w.ret[p] for p in range(2) if w.done[p]}
        if len(dec) > 1:
            return f"disagreement {dec}"
        if not dec <= set(values):
            return "invalid"
        return None

    return check


@pytest.mark.parametrize("f", NONTRIVIAL, ids=lambda f: f.__qualname__)
def test_any_nontrivial_rmw_solves_two_process_consensus(f) -> None:
    v0 = nontrivial_point(f, DOMAIN)
    assert v0 is not None
    for values in itertools.product("ab", repeat=2):
        states, finals = explore(setup_for(f, v0, values), check=agreement(values))
        assert finals >= 1


def test_the_trivial_rmw_fails() -> None:
    assert nontrivial_point(identity, DOMAIN) is None
    with pytest.raises(Found) as e:
        explore(setup_for(identity, 0, ("a", "b")), check=agreement(("a", "b")))
    assert "disagreement" in e.value.msg


def test_classes_of_function_sets() -> None:
    # Fetch-and-add with any increments: the functions commute.
    adds = [lambda x, d=d: x + d for d in (1, 2, 3)]
    assert classify(adds, DOMAIN)["commute"]
    # Test-and-set and swap: constant functions overwrite each other.
    consts = [lambda x, c=c: c for c in (1, 7)]
    assert classify(consts, DOMAIN) == {"commute": False, "overwrite": True, "interfering": True}
    # Fetch-and-or: commutes.
    assert classify([lambda x, b=b: x | b for b in (1, 2, 4)], DOMAIN)["commute"]
    # CAS: neither, so the theorem on interfering sets does not apply.
    cas = [cas_fn(e, v) for e in range(3) for v in range(3) if e != v]
    assert classify(cas, DOMAIN)["interfering"] is False
    # Add and multiply together are neither.
    assert classify([inc, double], DOMAIN)["interfering"] is False
