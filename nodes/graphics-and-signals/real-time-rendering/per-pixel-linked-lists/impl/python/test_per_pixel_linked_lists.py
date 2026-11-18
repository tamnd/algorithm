# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/per-pixel-linked-lists/. The authors are listed in prov/XK6ZQN.jsonl.

"""Per-pixel linked lists: the build under random interleavings and the resolve."""

import random
from fractions import Fraction as F

from per_pixel_linked_lists import (
    NULL,
    build,
    insertion_sort_by_depth,
    over_composite,
    resolve,
    walk,
)

BG = (F(1, 10), F(2, 10), F(3, 10))


def random_scene(rng: random.Random, num_pixels: int, count: int):
    depths = rng.sample(range(1, 10 * count + 10), count)
    pairs = []
    for z in depths:
        q = rng.randrange(num_pixels)
        a = F(rng.randint(1, 20), 20)
        col = tuple(a * F(rng.randint(0, 10), 10) for _ in range(3))
        pairs.append((q, (col, a, F(z))))
    return pairs


def per_pixel(pairs, num_pixels, keep=None):
    lists = [[] for _ in range(num_pixels)]
    for t, (q, f) in enumerate(pairs):
        if keep is None or t in keep:
            lists[q].append(f)
    return lists


def test_exact_when_the_pool_is_large_enough() -> None:
    rng = random.Random(51)
    for _ in range(20):
        p = rng.randint(1, 6)
        pairs = random_scene(rng, p, rng.randint(0, 25))
        store, nodes = build(p, len(pairs) + rng.randint(0, 3), pairs, rng)
        assert NULL not in nodes
        assert sorted(nodes) == list(range(len(pairs)))
        expect = per_pixel(pairs, p)
        for q in range(p):
            got = sorted(store.frag[i][2] for i in walk(store, q))
            assert got == sorted(f[2] for f in expect[q])
        assert resolve(store, BG) == [over_composite(expect[q], BG) for q in range(p)]


def test_image_does_not_depend_on_the_interleaving() -> None:
    rng = random.Random(52)
    p = 4
    pairs = random_scene(rng, p, 30)
    images = set()
    lists = set()
    for seed in range(15):
        store, _ = build(p, 40, pairs, random.Random(seed))
        images.add(tuple(resolve(store, BG)))
        lists.add(tuple(tuple(walk(store, q)) for q in range(p)))
    assert len(images) == 1
    assert len(lists) > 1  # the lists themselves do depend on the timing


def test_list_is_the_reverse_of_the_exchange_order() -> None:
    rng = random.Random(53)
    for _ in range(20):
        p = rng.randint(1, 5)
        pairs = random_scene(rng, p, rng.randint(1, 20))
        store, _ = build(p, len(pairs), pairs, rng)
        for q in range(p):
            order = [i for qq, i in store.exchange_log if qq == q]
            assert walk(store, q) == order[::-1]


def test_overflow_keeps_the_first_n_counter_values() -> None:
    rng = random.Random(54)
    differs = 0
    for _ in range(20):
        p = rng.randint(1, 4)
        pairs = random_scene(rng, p, rng.randint(5, 25))
        cap = rng.randint(0, len(pairs) - 1)
        store, nodes = build(p, cap, pairs, rng)
        kept = {t for t, i in enumerate(nodes) if i != NULL}
        assert len(kept) == cap
        assert sorted(nodes[t] for t in kept) == list(range(cap))
        assert store.counter == len(pairs)
        img = resolve(store, BG)
        assert img == [over_composite(fs, BG) for fs in per_pixel(pairs, p, kept)]
        if img != [over_composite(fs, BG) for fs in per_pixel(pairs, p)]:
            differs += 1
    assert differs > 0  # dropped fragments change the image


def test_insertion_sort_is_stable_and_sorted() -> None:
    rng = random.Random(55)
    for _ in range(50):
        a = [((rng.randint(0, 3),), F(1, 2), rng.randint(0, 5)) for _ in range(rng.randint(0, 12))]
        assert insertion_sort_by_depth(a) == sorted(a, key=lambda f: f[2])


def test_worked_example() -> None:
    red = ((F(1, 2), F(0), F(0)), F(1, 2), F(1))
    blue = ((F(0), F(0), F(1, 2)), F(1, 2), F(2))
    green = ((F(0), F(1, 4), F(0)), F(1, 4), F(3))
    pairs = [(0, green), (0, red), (1, blue), (0, blue)]
    store, nodes = build(2, 3, pairs, random.Random(7))
    kept = [t for t, i in enumerate(nodes) if i != NULL]
    assert len(kept) == 3 and store.counter == 4
    black = (F(0), F(0), F(0))
    full = over_composite([red, blue, green], black)
    assert full == (F(1, 2), F(1, 16), F(1, 4))
