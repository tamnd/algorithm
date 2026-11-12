# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/data-augmentation/. The authors are listed in prov/B4MG5J.jsonl.
"""Data augmentation: label-preserving random transforms (flip, padded crop, cutout), mixup (Zhang et al.
2018), and the orbit view of Chen, Dobriban and Lee (2020): averaging a predictor over a group that leaves
the data distribution unchanged does not increase a convex risk.
"""

import math
import random
from typing import Callable

Image = list  # a list of rows of numbers


def flip_horizontal(img: Image) -> Image:
    return [row[::-1] for row in img]


def random_flip(img: Image, rng: random.Random) -> Image:
    return flip_horizontal(img) if rng.random() < 0.5 else [row[:] for row in img]


def random_crop(img: Image, pad: int, rng: random.Random) -> Image:
    """Pad with zeros by `pad` on each side and cut a window of the original size at a random offset."""
    h, w = len(img), len(img[0])
    big = [[0] * (w + 2 * pad) for _ in range(pad)]
    big += [[0] * pad + row + [0] * pad for row in img]
    big += [[0] * (w + 2 * pad) for _ in range(pad)]
    i, j = rng.randint(0, 2 * pad), rng.randint(0, 2 * pad)
    return [row[j:j + w] for row in big[i:i + h]]


def cutout(img: Image, size: int, rng: random.Random) -> tuple[Image, tuple[int, int]]:
    """Cutout (DeVries and Taylor 2017): zero a size x size square whose center is uniform over the image.
    The square may stick out of the image; only the part inside is zeroed. Returns the image and center."""
    h, w = len(img), len(img[0])
    ci, cj = rng.randrange(h), rng.randrange(w)
    top, left = ci - size // 2, cj - size // 2
    out = [row[:] for row in img]
    for i in range(max(0, top), min(h, top + size)):
        for j in range(max(0, left), min(w, left + size)):
            out[i][j] = 0
    return out, (ci, cj)


def one_hot(k: int, classes: int) -> list[float]:
    return [1.0 if i == k else 0.0 for i in range(classes)]


def mixup_pair(x1: list, y1: list, x2: list, y2: list, lam) -> tuple[list, list]:
    """The mixup example lam (x1, y1) + (1 - lam) (x2, y2), for inputs and label vectors."""
    return ([lam * a + (1 - lam) * b for a, b in zip(x1, x2)],
            [lam * a + (1 - lam) * b for a, b in zip(y1, y2)])


def mixup_batch(xs: list, ys: list, alpha: float, rng: random.Random) -> tuple[list, list, float, list[int]]:
    """Mixup on a batch: one lam ~ Beta(alpha, alpha) and a random permutation of the batch as partners."""
    lam = rng.betavariate(alpha, alpha)
    perm = list(range(len(xs)))
    rng.shuffle(perm)
    pairs = [mixup_pair(xs[i], ys[i], xs[k], ys[k], lam) for i, k in enumerate(perm)]
    return [p[0] for p in pairs], [p[1] for p in pairs], lam, perm


def cross_entropy(target: list, probs: list) -> float:
    """H(target, probs) = -sum_k target_k log probs_k, for any target distribution."""
    return -sum(t * math.log(p) for t, p in zip(target, probs) if t != 0)


def cyclic_shifts(x: list) -> list[list]:
    """The orbit of x under the cyclic group of rotations of its coordinates."""
    return [x[k:] + x[:k] for k in range(len(x))]


def orbit_average(f: Callable[[list], object], group: Callable[[list], list[list]]) -> Callable[[list], object]:
    """f_bar(x) = mean of f(g x) over the finite group. It is invariant: f_bar(g x) = f_bar(x)."""
    def f_bar(x: list):
        orbit = group(x)
        return sum(f(z) for z in orbit) / len(orbit)
    return f_bar


def augmented_square_loss(w: list, x: list, y, group: Callable[[list], list[list]]):
    """The augmented loss mean_g (w . g x - y)^2 of one example."""
    orbit = group(x)
    return sum((sum(a * b for a, b in zip(w, z)) - y) ** 2 for z in orbit) / len(orbit)


def orbit_mean_and_covariance(x: list, group: Callable[[list], list[list]]) -> tuple[list, list]:
    """The mean and the covariance matrix of g x for g uniform on the finite group."""
    orbit = group(x)
    n, d = len(orbit), len(x)
    mean = [sum(z[i] for z in orbit) / n for i in range(d)]
    cov = [[sum((z[i] - mean[i]) * (z[j] - mean[j]) for z in orbit) / n for j in range(d)] for i in range(d)]
    return mean, cov


def augmented_stream(data: list, transforms: list[Callable], rng: random.Random, epochs: int):
    """Yield (t(x), y) for each example in each epoch, with a fresh random transform t each time."""
    for _ in range(epochs):
        for i in rng.sample(range(len(data)), len(data)):
            x, y = data[i]
            yield rng.choice(transforms)(x), y
