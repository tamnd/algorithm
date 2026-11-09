# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-objective-evolutionary-algorithm/. The authors are listed in prov/1SG8N5.jsonl.

import itertools
import random
from fractions import Fraction as Fr

from multi_objective_evolutionary_algorithm import (
    bit_flip,
    dominates,
    gsemo,
    lotz,
    moea,
    one_min_max,
    update_archive,
)


def pareto_images(images):
    s = set(images)
    return {y for y in s if not any(dominates(z, y) for z in s)}


def front_numbers(images):
    """Reference O(N^2) per front: peel the non-dominated points one front at a time."""
    rank = [0] * len(images)
    left = set(range(len(images)))
    r = 0
    while left:
        r += 1
        front = [i for i in left if not any(dominates(images[j], images[i]) for j in left)]
        for i in front:
            rank[i] = r
        left -= set(front)
    return rank


# A small bi-objective knapsack: minimize (total weight, -total value), with the
# capacity as a constraint. Repair drops items from the left until x is feasible.
WEIGHTS = (3, 5, 2, 7, 4, 6, 1, 8)
VALUES = (4, 6, 3, 9, 2, 7, 2, 10)
CAPACITY = 18


def knap_f(x):
    return (sum(w for w, b in zip(WEIGHTS, x) if b), -sum(v for v, b in zip(VALUES, x) if b))


def feasible(x):
    return sum(w for w, b in zip(WEIGHTS, x) if b) <= CAPACITY


def repair(x):
    x = list(x)
    i = 0
    while not feasible(x):
        x[i] = 0
        i += 1
    return tuple(x)


def make_parts(n):
    def init(rng):
        return [repair(tuple(rng.randint(0, 1) for _ in WEIGHTS)) for _ in range(n)]

    def fitness(pop):
        return front_numbers([y for _, y in pop])

    def select(pop, phi, rng):
        out = []
        for _ in range(len(pop)):
            i, j = rng.randrange(len(pop)), rng.randrange(len(pop))
            out.append(pop[i][0] if phi[i] <= phi[j] else pop[j][0])
        return out

    def vary(parents, rng):
        return [repair(bit_flip(x, rng)) for x in parents]

    def survive(pop, off, n, rng):
        union = pop + off
        r = front_numbers([y for _, y in union])
        order = sorted(range(len(union)), key=lambda i: (r[i], rng.random()))
        return [union[i] for i in order[:n]]

    return init, fitness, select, vary, survive


def test_update_archive() -> None:
    a = []
    assert update_archive(a, "p", (2, 2))
    assert not update_archive(a, "q", (2, 2))  # same image: one member per image
    assert not update_archive(a, "r", (3, 2))
    assert update_archive(a, "s", (1, 3))
    assert update_archive(a, "t", (1, 1))  # removes both
    assert a == [("t", (1, 1))]


def test_moea_invariants() -> None:
    for seed in range(6):
        rng = random.Random(seed)
        n = 8
        seen = []
        prev = []

        def hook(pop, archive, off):
            nonlocal prev
            seen.extend(y for _, y in off)
            assert len(pop) == n
            imgs = [y for _, y in archive]
            assert len(set(imgs)) == len(imgs)
            for a, b in itertools.permutations(imgs, 2):
                assert not dominates(a, b)
            # the archive holds exactly the non-dominated images seen so far
            assert set(imgs) == pareto_images(seen)
            # elitism: a non-dominated image found before is not lost
            for y in prev:
                if not any(dominates(z, y) for z in seen):
                    assert y in imgs
            prev = list(imgs)
            assert all(feasible(x) and knap_f(x) == y for x, y in archive)

        init, fitness, select, vary, survive = make_parts(n)
        orig_init = init

        def init_and_record(r):
            xs = orig_init(r)
            seen.extend(knap_f(x) for x in xs)
            return xs

        pop, archive = moea(init_and_record, knap_f, fitness, select, vary, survive, n, 25, rng, hook)
        assert len(pop) == n
        assert all(feasible(x) for x, _ in pop + archive)


def test_bounded_crowding_archive_can_deteriorate() -> None:
    """A bounded archive that drops the most crowded point can keep a point that an earlier point dominated."""

    def crowding_2d(pts):
        order = sorted(range(len(pts)), key=lambda i: pts[i])
        r1 = pts[order[-1]][0] - pts[order[0]][0]
        r2 = pts[order[0]][1] - pts[order[-1]][1]
        d = {order[0]: None, order[-1]: None}
        for k in range(1, len(pts) - 1):
            a, b = pts[order[k - 1]], pts[order[k + 1]]
            d[order[k]] = Fr(b[0] - a[0], r1) + Fr(a[1] - b[1], r2)
        return d

    arc = [(0, 10), (10, 0)]
    seen = list(arc)
    for y in [(4, 1), (2, 4), (4, 3)]:
        seen.append(y)
        if any(dominates(a, y) or a == y for a in arc):
            continue
        arc = [a for a in arc if not dominates(y, a)] + [y]
        if len(arc) > 3:
            d = crowding_2d(arc)
            inner = [i for i in d if d[i] is not None]
            drop = min(inner, key=lambda i: d[i])
            assert sorted(d[i] for i in inner)[0] < sorted(d[i] for i in inner)[1]
            arc.pop(drop)
    assert sorted(arc) == [(0, 10), (4, 3), (10, 0)]
    assert dominates((4, 1), (4, 3))


def test_gsemo_population_is_the_front_of_all_seen() -> None:
    for f, n, seed in [(lotz, 6, 1), (one_min_max, 6, 2), (lotz, 5, 3)]:
        rng = random.Random(seed)
        seen = []

        def hook(pop, child, y):
            seen.append(y)
            imgs = [b for _, b in pop]
            assert len(set(imgs)) == len(imgs)
            for a, b in itertools.permutations(imgs, 2):
                assert not dominates(a, b)
            assert set(imgs) <= pareto_images(seen + imgs)
            assert pareto_images(seen + imgs) == set(imgs)
            assert all(f(x) == b for x, b in pop)

        gsemo(n, f, 400, rng, hook)


def test_lotz_and_one_min_max_values() -> None:
    assert lotz((1, 1, 0, 1, 0, 0)) == (-2, -2)
    assert lotz((1, 1, 1)) == (-3, 0)
    assert lotz((0, 0, 0)) == (0, -3)
    assert one_min_max((1, 0, 1, 1)) == (3, 1)
    # the Pareto front of LOTZ for n = 5 is the n + 1 strings 1^i 0^(n-i)
    imgs = {lotz(x): x for x in itertools.product((0, 1), repeat=5)}
    front = pareto_images(list(imgs))
    assert front == {(-i, -(5 - i)) for i in range(6)}
