# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conditional-entropy/. The authors are listed in prov/70YZ8M.jsonl.

import math
import random

import pytest

from conditional_entropy import (
    conditional_entropy, entropy_x, entropy_x_given_y_equals, entropy_y, joint_entropy, mutual_information,
)


def random_table(rng: random.Random, a: int, b: int, zeros: bool = False) -> list[list[float]]:
    w = [[(0.0 if zeros and rng.random() < 0.3 else rng.random()) for _ in range(b)] for _ in range(a)]
    if sum(map(sum, w)) == 0:
        w[0][0] = 1.0
    s = sum(map(sum, w))
    return [[v / s for v in row] for row in w]


def transpose(p):
    return [list(col) for col in zip(*p)]


# p[x][y]. P(Y = 1) = 3/4 and then X = 2; P(Y = 2) = 1/4 and then X is uniform.
# The joint law of the example in Cover and Thomas, Section 2.6.
EXAMPLE = [[0.0, 1 / 8], [3 / 4, 1 / 8]]


def test_example_values() -> None:
    assert math.isclose(entropy_x(EXAMPLE), 0.5435644431995964, rel_tol=1e-12)
    assert entropy_x_given_y_equals(EXAMPLE, 0) == 0.0
    assert math.isclose(entropy_x_given_y_equals(EXAMPLE, 1), 1.0)
    assert math.isclose(conditional_entropy(EXAMPLE), 0.25)
    assert math.isclose(mutual_information(EXAMPLE), entropy_x(EXAMPLE) - 0.25)


def test_conditioning_can_raise_entropy_for_one_value() -> None:
    # H(X | Y = 2) = 1 > H(X), but the average H(X | Y) = 0.25 < H(X).
    assert entropy_x_given_y_equals(EXAMPLE, 1) > entropy_x(EXAMPLE)
    assert conditional_entropy(EXAMPLE) < entropy_x(EXAMPLE)


def test_chain_rule() -> None:
    rng = random.Random(1)
    for _ in range(300):
        p = random_table(rng, rng.randint(1, 5), rng.randint(1, 5), zeros=True)
        assert math.isclose(joint_entropy(p), entropy_y(p) + conditional_entropy(p), abs_tol=1e-9)
        q = transpose(p)
        assert math.isclose(joint_entropy(p), entropy_x(p) + conditional_entropy(q), abs_tol=1e-9)


def test_mutual_information_nonnegative_and_symmetric() -> None:
    rng = random.Random(2)
    for _ in range(300):
        p = random_table(rng, rng.randint(1, 5), rng.randint(1, 5), zeros=True)
        i = mutual_information(p)
        assert i >= -1e-12
        assert math.isclose(i, mutual_information(transpose(p)), abs_tol=1e-9)
        assert math.isclose(i, entropy_x(p) - conditional_entropy(p), abs_tol=1e-9)
        assert conditional_entropy(p) <= entropy_x(p) + 1e-12
        assert conditional_entropy(p) >= -1e-12


def test_independent_gives_zero_information() -> None:
    px, py = [0.2, 0.3, 0.5], [0.6, 0.4]
    p = [[a * b for b in py] for a in px]
    assert abs(mutual_information(p)) < 1e-12
    assert math.isclose(conditional_entropy(p), entropy_x(p))


def test_function_of_y_gives_zero() -> None:
    # X = Y mod 2, Y uniform on 4 values: H(X | Y) = 0, I = H(X) = 1.
    p = [[0.25 if y % 2 == x else 0.0 for y in range(4)] for x in range(2)]
    assert conditional_entropy(p) == 0.0
    assert math.isclose(mutual_information(p), 1.0)


def test_data_processing_inequality() -> None:
    rng = random.Random(3)
    for _ in range(200):
        a, b, c = rng.randint(2, 4), rng.randint(2, 4), rng.randint(2, 4)
        px = random_table(rng, 1, a)[0]
        ch1 = [random_table(rng, 1, b)[0] for _ in range(a)]  # P(y | x)
        ch2 = [random_table(rng, 1, c)[0] for _ in range(b)]  # P(z | y)
        pxy = [[px[x] * ch1[x][y] for y in range(b)] for x in range(a)]
        pxz = [[sum(px[x] * ch1[x][y] * ch2[y][z] for y in range(b)) for z in range(c)] for x in range(a)]
        assert mutual_information(pxz) <= mutual_information(pxy) + 1e-12


def test_bad_table() -> None:
    with pytest.raises(ValueError):
        conditional_entropy([[0.5, 0.6]])
