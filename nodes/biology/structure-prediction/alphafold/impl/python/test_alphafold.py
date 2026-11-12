# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alphafold/. The authors are listed in prov/VWHHRT.jsonl.

import math
import random
from fractions import Fraction

from alphafold import bin_centers, confidence_loss, lddt, plddt, softmax, target_bin

REF = [(0.0, 0.0, 0.0), (3.8, 0.0, 0.0), (7.6, 0.0, 0.0), (11.4, 0.0, 0.0)]


def direct_lddt(model, ref, cutoff=15.0, thresholds=(0.5, 1.0, 2.0, 4.0)):
    """lDDT straight from the definition: count (pair, threshold) tests as exact fractions."""
    n = len(ref)
    tests = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d0 = math.dist(ref[i], ref[j])
            if not d0 < cutoff:
                continue
            d = math.dist(model[i], model[j])
            for t in thresholds:
                tests[i].append(abs(d - d0) < t)
    per = [Fraction(sum(v), len(v)) if v else None for v in tests.values()]
    allv = [b for v in tests.values() for b in v]
    return (Fraction(sum(allv), len(allv)) if allv else Fraction(0)), per


def random_chain(n, rng):
    pts = [(0.0, 0.0, 0.0)]
    for _ in range(n - 1):
        while True:
            v = [rng.gauss(0, 1) for _ in range(3)]
            r = math.sqrt(sum(x * x for x in v))
            p = tuple(a + 3.8 * x / r for a, x in zip(pts[-1], v))
            if all(math.dist(p, q) > 3.0 for q in pts[:-1]):
                break
        pts.append(p)
    return pts


def rotate(points, rng):
    # A random rotation from a unit quaternion, then a random translation.
    w, x, y, z = (rng.gauss(0, 1) for _ in range(4))
    s = math.sqrt(w * w + x * x + y * y + z * z)
    w, x, y, z = w / s, x / s, y / s, z / s
    r = [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
         [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
         [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]
    t = [rng.uniform(-20, 20) for _ in range(3)]
    return [tuple(sum(r[a][b] * p[b] for b in range(3)) + t[a] for a in range(3)) for p in points]


def test_matches_the_direct_definition() -> None:
    rng = random.Random(1)
    for _ in range(60):
        n = rng.randint(2, 14)
        ref = random_chain(n, rng)
        model = [tuple(c + rng.gauss(0, rng.choice((0.2, 1.0, 3.0))) for c in p) for p in ref]
        cut = rng.choice((8.0, 15.0))
        got, per = lddt(model, ref, cut)
        want, wper = direct_lddt(model, ref, cut)
        assert abs(got - float(want)) < 1e-12
        for a, b in zip(per, wper):
            assert (a is None and b is None) or abs(a - float(b)) < 1e-12


def test_identical_structures_score_one() -> None:
    ref = random_chain(20, random.Random(2))
    score, per = lddt(ref, ref)
    assert score == 1.0 and all(v == 1.0 for v in per)


def test_superposition_free() -> None:
    rng = random.Random(3)
    ref = random_chain(25, rng)
    model = [tuple(c + rng.gauss(0, 1.0) for c in p) for p in ref]
    a = lddt(model, ref)
    b = lddt(rotate(model, rng), ref)
    assert abs(a[0] - b[0]) < 1e-12
    assert all(abs(u - v) < 1e-12 for u, v in zip(a[1], b[1]))


def test_mirror_image_is_not_detected() -> None:
    # lDDT sees only distances, so the mirror image of the reference scores 1.
    ref = random_chain(15, random.Random(4))
    mirror = [(-x, y, z) for x, y, z in ref]
    assert lddt(mirror, ref)[0] == 1.0


def test_the_reference_chooses_the_pairs() -> None:
    a = [(0.0, 0.0, 0.0), (14.0, 0.0, 0.0)]
    b = [(0.0, 0.0, 0.0), (20.0, 0.0, 0.0)]
    assert lddt(b, a)[0] == 0.0  # the pair is scored, and its distance changed by 6
    assert lddt(a, b) == (0.0, [None, None])  # no pair is within 15 in b, so nothing is scored


def test_page_example() -> None:
    model = REF[:3] + [(9.4, 3.0, 0.0)]
    score, per = lddt(model, REF)
    assert abs(score - 5 / 6) < 1e-12
    assert [round(v, 4) for v in per] == [0.8333, 0.8333, 1.0, 0.6667]


def test_plddt_page_example() -> None:
    z = [-1e9] * 50
    z[44], z[45], z[40] = math.log(0.5), math.log(0.3), math.log(0.2)
    assert abs(plddt([z])[0] - 88.0) < 1e-9


def test_plddt_matches_a_direct_sum() -> None:
    rng = random.Random(5)
    for _ in range(50):
        z = [rng.gauss(0, 3) for _ in range(50)]
        e = [math.exp(v) for v in z]
        want = 100 * sum(e[k] * (k + 0.5) / 50 for k in range(50)) / sum(e)
        assert abs(plddt([z])[0] - want) < 1e-9
        shifted = [v + 7.0 for v in z]
        assert abs(plddt([shifted])[0] - want) < 1e-9  # softmax ignores a common shift
    assert abs(plddt([[0.0] * 50])[0] - 50.0) < 1e-12  # a flat head says 50


def test_bins_and_loss() -> None:
    assert bin_centers(50)[0] == 0.01 and abs(bin_centers(50)[-1] - 0.99) < 1e-12
    assert (target_bin(0.0), target_bin(0.5), target_bin(0.999), target_bin(1.0)) == (0, 25, 49, 49)
    sharp = [[-50.0] * 50 for _ in range(2)]
    sharp[0][45] = sharp[1][10] = 50.0
    assert confidence_loss(sharp, [0.91, 0.21]) < 1e-12  # the head puts its mass on the true bins
    assert confidence_loss(sharp, [0.21, 0.91]) > 50  # and is penalized when it is wrong
    p = softmax([0.0] * 50)
    assert abs(confidence_loss([[0.0] * 50], [0.3]) + math.log(p[0])) < 1e-12
