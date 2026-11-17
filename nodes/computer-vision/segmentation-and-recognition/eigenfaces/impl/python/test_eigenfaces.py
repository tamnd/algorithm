# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eigenfaces/. The authors are listed in prov/22X5JB.jsonl.

import math
import random

from eigenfaces import (
    covariance_eigen,
    distance_from_face_space,
    project,
    recognize,
    reconstruct,
    train,
)

EXAMPLE = [[8, 3, 3, 6], [6, 3, 3, 8], [3, 9, 5, 3], [3, 5, 9, 3]]
EXAMPLE_LABELS = ["a", "a", "b", "b"]


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def random_set(rng, m, p):
    return [[rng.uniform(0, 255) for _ in range(p)] for _ in range(m)]


def test_example():
    model = train(EXAMPLE, EXAMPLE_LABELS, 3)
    assert model["mean"] == [5.0, 5.0, 5.0, 5.0]
    assert [round(x, 9) for x in model["values"]] == [64.0, 16.0, 4.0]
    assert [round(x, 9) for x in model["faces"][0]] == [0.5, -0.5, -0.5, 0.5]
    model = train(EXAMPLE, EXAMPLE_LABELS, 1)
    assert {k: round(v[0], 9) for k, v in model["centers"].items()} == {"a": 4.0, "b": -4.0}
    label, dist = recognize(model, [7, 4, 3, 6])
    assert label == "a" and abs(dist - 1.0) < 1e-9
    assert abs(distance_from_face_space(model, [7, 4, 3, 6]) - 1.0) < 1e-9
    label, dist = recognize(model, [5, 9, 9, 5])
    assert label == "b" and abs(dist) < 1e-9
    label, dist = recognize(model, [5, 9, 9, 5], theta_face=2.0)
    assert label == "not a face" and abs(dist - 4.0) < 1e-9


def test_small_matrix_gives_the_covariance_eigenvectors():
    rng = random.Random(3)
    images = random_set(rng, 5, 12)
    model = train(images, list(range(5)), 4)
    big_w, big_v = covariance_eigen(images)
    for lam, u, w, v in zip(model["values"], model["faces"], big_w, big_v):
        assert abs(lam - w) < 1e-7 * big_w[0]
        assert abs(abs(dot(u, v)) - 1.0) < 1e-8
    assert all(abs(w) < 1e-7 * big_w[0] for w in big_w[4:])


def test_eigenfaces_are_orthonormal():
    rng = random.Random(5)
    model = train(random_set(rng, 8, 30), list(range(8)), 7)
    faces = model["faces"]
    assert len(faces) == 7
    for i, u in enumerate(faces):
        for j, v in enumerate(faces):
            assert abs(dot(u, v) - (1.0 if i == j else 0.0)) < 1e-9


def test_rank_is_at_most_m_minus_one_and_training_set_is_rebuilt():
    rng = random.Random(6)
    images = random_set(rng, 6, 20)
    model = train(images, list(range(6)), 10)
    assert len(model["faces"]) == 5
    for img in images:
        rec = reconstruct(model, project(model, img))
        assert max(abs(a - b) for a, b in zip(rec, img)) < 1e-8


def test_residual_equals_discarded_eigenvalues():
    rng = random.Random(8)
    images = random_set(rng, 7, 16)
    full = train(images, list(range(7)), 6)
    for k in range(1, 6):
        model = train(images, list(range(7)), k)
        resid = sum(distance_from_face_space(model, img) ** 2 for img in images)
        assert abs(resid - sum(full["values"][k:])) < 1e-6 * full["values"][0]


def test_pca_beats_random_subspaces():
    rng = random.Random(10)
    images = random_set(rng, 6, 10)
    model = train(images, list(range(6)), 2)
    best = sum(distance_from_face_space(model, img) ** 2 for img in images)
    for _ in range(50):
        basis = []
        for _ in range(2):
            x = [rng.gauss(0, 1) for _ in range(10)]
            for b in basis:
                c = dot(x, b)
                x = [xi - c * bi for xi, bi in zip(x, b)]
            n = math.sqrt(dot(x, x))
            basis.append([xi / n for xi in x])
        other = dict(model, faces=basis)
        assert sum(distance_from_face_space(other, img) ** 2 for img in images) >= best - 1e-9


def test_recognizes_noisy_faces():
    rng = random.Random(12)
    p = 64
    people = [[rng.uniform(40, 220) for _ in range(p)] for _ in range(4)]
    images, labels = [], []
    for who, proto in enumerate(people):
        for _ in range(3):
            images.append([x + rng.gauss(0, 8) for x in proto])
            labels.append(who)
    model = train(images, labels, 6)
    correct = 0
    for who, proto in enumerate(people):
        for _ in range(5):
            label, _ = recognize(model, [x + rng.gauss(0, 8) for x in proto])
            correct += label == who
    assert correct == 20
    noise = [rng.uniform(0, 255) for _ in range(p)]
    face = [x + rng.gauss(0, 8) for x in people[0]]
    assert distance_from_face_space(model, noise) > 2 * distance_from_face_space(model, face)
