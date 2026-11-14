# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-fazio-whitney-precedence-method/. The authors are listed in prov/RRPKFP.jsonl.

import itertools
import random

from assembly_boxes import AXES6, face_contact, free_by_sampling, random_boxes
from de_fazio_whitney_precedence_method import (
    answer_questions, count_sequences, evaluate, liaisons_of, sequences, show)

# ---- independent reference: every order of the parts, checked on the geometry ----


def feasible_orders(boxes, motions):
    """Orders in which each new part touches a placed part and can come in
    by one translation, checked by a sampled sweep."""
    n = len(boxes)
    cache = {}
    out = []
    for order in itertools.permutations(range(n)):
        ok = True
        for k in range(1, n):
            p = order[k]
            placed = frozenset(order[:k])
            key = (placed, p)
            if key not in cache:
                touches = any(face_contact(boxes[p], boxes[q]) is not None for q in placed)
                cache[key] = touches and any(
                    free_by_sampling([boxes[p]], [boxes[q] for q in placed], d) for d in motions)
            if not cache[key]:
                ok = False
                break
        if ok:
            out.append(order)
    return out


def image(order, liaisons):
    """The sequence of liaison states of a part order."""
    states = []
    for k in range(2, len(order) + 1):
        placed = set(order[:k])
        states.append(frozenset(i for i, (u, v) in enumerate(liaisons)
                                if u in placed and v in placed))
    return tuple(states)


def check(boxes, motions):
    liaisons = liaisons_of(boxes)
    pre, post = answer_questions(boxes, liaisons, motions)
    assert len(pre) == len(post) == len(liaisons)       # 2 questions per liaison
    n = len(boxes)
    got = sequences(n, liaisons, pre, post)
    assert len(got) == len(set(got))
    orders = feasible_orders(boxes, motions)
    assert set(got) == {image(o, liaisons) for o in orders}
    assert count_sequences(n, liaisons, pre, post) == len(got)
    return len(orders), len(got)


EXAMPLE = [
    (0, 0, 0, 4, 2, 1),   # 0 base plate
    (0, 0, 1, 1, 2, 3),   # 1 left post
    (3, 0, 1, 4, 2, 3),   # 2 right post
    (1, 0, 1, 3, 2, 2),   # 3 block
    (0, 0, 3, 4, 2, 4),   # 4 top plate
]
PLANE = ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1))

# ---- tests ----


def test_random_products_one_or_two_directions():
    rng = random.Random(21)
    for _ in range(70):
        n = rng.randint(1, 5)
        boxes = random_boxes(rng, n, size=3, max_side=3, connected=rng.random() < 0.85)
        motions = tuple(rng.sample(AXES6, rng.randint(1, 2)))
        check(boxes, motions)


def test_random_products_six_boxes():
    rng = random.Random(22)
    for _ in range(5):
        boxes = random_boxes(rng, 6, size=3, max_side=2, connected=True)
        motions = tuple(rng.sample(AXES6, rng.randint(1, 3)))
        check(boxes, motions)


def test_all_six_directions():
    rng = random.Random(23)
    for _ in range(25):
        n = rng.randint(2, 5)
        boxes = random_boxes(rng, n, size=3, max_side=3, connected=True)
        n_orders, _ = check(boxes, AXES6)
        # a box blocks another box along at most one of the six directions,
        # so with at most five others a box can always come in: every order
        # whose prefixes are connected is feasible
        connected_orders = sum(
            all(any(face_contact(boxes[o[k]], boxes[q]) for q in o[:k]) for k in range(1, n))
            for o in itertools.permutations(range(n)))
        assert n_orders == connected_orders


def test_example_frame():
    liaisons = liaisons_of(EXAMPLE)
    assert liaisons == [(0, 1), (0, 2), (0, 3), (1, 3), (1, 4), (2, 3), (2, 4)]
    pre, post = answer_questions(EXAMPLE, liaisons, PLANE)
    assert all(evaluate(p, frozenset()) for p in pre)
    n_orders, n_seq = check(EXAMPLE, PLANE)
    assert (n_orders, n_seq) == (64, 32)
    # the block cannot come in once the base, both posts and the top are placed
    closed = frozenset([0, 1, 4, 6])          # liaisons {0,1}, {0,2}, {1,4}, {2,4}
    for i in (2, 3, 5):                       # the liaisons of the block
        assert evaluate(post[i], closed)
    assert not any(evaluate(post[i], frozenset([0, 1, 2, 3, 5])) for i in range(7))
    assert "l" in show(post[2])
