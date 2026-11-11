# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/join-semilattice/. The authors are listed in prov/QS5856.jsonl.

import random
from functools import reduce

from join_semilattice import (
    BOWTIE_BELOW,
    BOWTIE_ELEMENTS,
    absorption,
    average_merge,
    is_associative,
    is_commutative,
    is_idempotent,
    is_least_upper_bound,
    is_monotone_inflationary,
    is_partial_order,
    is_semilattice,
    join_all,
    lcm_join,
    leq,
    lex_join,
    map_join,
    max_join,
    minimal_upper_bounds,
    plus_merge,
    second_merge,
    union_join,
    vector_join,
)

RNG = random.Random(5856)


def rand_set() -> frozenset:
    return frozenset(x for x in range(5) if RNG.random() < 0.4)


def rand_vec() -> tuple[int, ...]:
    return tuple(RNG.randint(0, 3) for _ in range(3))


def test_examples_satisfy_aci_and_lub() -> None:
    samples = [
        (max_join, [RNG.randint(-5, 5) for _ in range(12)]),
        (union_join, [rand_set() for _ in range(12)]),
        (vector_join, [rand_vec() for _ in range(12)]),
        (lex_join, [(RNG.randint(0, 2), rand_set()) for _ in range(12)]),
        (lcm_join, [RNG.randint(1, 30) for _ in range(12)]),
    ]
    for join, sample in samples:
        assert is_semilattice(join, sample)
        assert is_least_upper_bound(join, sample)
        assert is_partial_order(lambda a, b, j=join: leq(j, a, b), sample)


def test_map_join() -> None:
    xs = [{k: RNG.randint(0, 3) for k in RNG.sample("abc", RNG.randint(0, 3))} for _ in range(8)]

    def norm(m: dict[str, int]) -> frozenset:
        return frozenset((k, v) for k, v in m.items() if v != 0)

    for a in xs:
        assert norm(map_join(a, a)) == norm(a)
        for b in xs:
            assert norm(map_join(a, b)) == norm(map_join(b, a))
            for c in xs:
                assert norm(map_join(map_join(a, b), c)) == norm(map_join(a, map_join(b, c)))


def test_lub_on_full_finite_domains() -> None:
    # every subset of {0, 1, 2} and every vector in {0, 1, 2}^2
    subsets = [frozenset(s for s in range(3) if m >> s & 1) for m in range(8)]
    assert is_least_upper_bound(union_join, subsets)
    vecs = [(a, b) for a in range(3) for b in range(3)]
    assert is_least_upper_bound(vector_join, vecs)


def test_absorption_for_lattices() -> None:
    sets = [rand_set() for _ in range(15)]
    assert absorption(union_join, lambda a, b: a & b, sets)
    vecs = [rand_vec() for _ in range(15)]
    vmin = lambda a, b: tuple(min(p, q) for p, q in zip(a, b))
    assert absorption(vector_join, vmin, vecs)
    ints = list(range(1, 25))
    gcd = lambda a, b: a if b == 0 else gcd(b, a % b)
    assert absorption(lcm_join, gcd, ints)


def test_non_examples() -> None:
    ints = list(range(-3, 4))
    assert is_associative(plus_merge, ints) and is_commutative(plus_merge, ints)
    assert not is_idempotent(plus_merge, ints)
    assert is_associative(second_merge, ints) and is_idempotent(second_merge, ints)
    assert not is_commutative(second_merge, ints)
    reals = [0.0, 1.0, 4.0]
    assert is_commutative(average_merge, reals) and is_idempotent(average_merge, reals)
    assert not is_associative(average_merge, reals)
    assert minimal_upper_bounds(BOWTIE_ELEMENTS, BOWTIE_BELOW, "a", "b") == ["c", "d"]


def test_join_all_ignores_order_and_repeats() -> None:
    for _ in range(500):
        items = [rand_vec() for _ in range(RNG.randint(0, 6))]
        shuffled = items + RNG.choices(items, k=RNG.randint(0, 3)) if items else []
        RNG.shuffle(shuffled)
        a = join_all(vector_join, (0, 0, 0), items)
        b = join_all(vector_join, (0, 0, 0), shuffled)
        assert a == b
        # the model: the pointwise max of the list
        model = tuple(max([v[i] for v in items] + [0]) for i in range(3))
        assert a == model


def test_increment_is_inflationary_and_monotone() -> None:
    vecs = [(a, b) for a in range(3) for b in range(3)]
    inc0 = lambda v: (v[0] + 1, v[1])
    assert is_monotone_inflationary(inc0, vector_join, vecs)
    adds = [rand_set() for _ in range(10)]
    add3 = lambda s: s | {3}
    assert is_monotone_inflationary(add3, union_join, adds)
    # removing an element is not inflationary
    rm3 = lambda s: s - {3}
    assert not is_monotone_inflationary(rm3, union_join, [frozenset({3})])


def test_worked_example() -> None:
    assert vector_join((3, 0, 1), (1, 2, 1)) == (3, 2, 1)
    assert reduce(vector_join, [(1, 0, 0), (0, 2, 0), (1, 1, 1)]) == (1, 2, 1)
    assert lex_join((1, frozenset({"a"})), (2, frozenset({"b"}))) == (2, frozenset({"b"}))
    assert lex_join((2, frozenset({"a"})), (2, frozenset({"b"}))) == (2, frozenset({"a", "b"}))
