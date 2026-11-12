# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frustum-culling/. The authors are listed in prov/F4J7C6.jsonl.

import itertools
import random

from frustum_culling import build_bvh, classify, frustum_cull, frustum_planes

EXAMPLE = frustum_planes((0, 0, 0), -1, 1, -1, 1, 1, 10)
A = ((-1, -1, -6), (1, 1, -4))
B = ((5, -1, -4), (7, 1, -2))
C = ((3, 3, -4), (5, 5, -3))
D = ((11, -1, -13), (12, 1, -9))
E = ((-4, -1, -3), (-2, 1, -2))


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def intersects(box, planes):
    """Exact brute force: the bounded polyhedron box ∩ frustum is nonempty iff it has a vertex.

    A vertex is a point where three constraints with independent normals are tight
    and all constraints hold. Integer Cramer's rule keeps every sign exact.
    """
    lo, hi = box
    cons = list(planes)
    for k in range(3):
        u = [0, 0, 0]
        u[k] = 1
        cons.append((tuple(u), -lo[k]))
        u[k] = -1
        cons.append((tuple(u), hi[k]))
    for (n1, d1), (n2, d2), (n3, d3) in itertools.combinations(cons, 3):
        m = det3(n1, n2, n3)
        if m == 0:
            continue
        b = (-d1, -d2, -d3)
        cols = [[n1[k], n2[k], n3[k]] for k in range(3)]
        X = []
        for k in range(3):
            cc = [list(col) for col in cols]
            cc[k] = list(b)
            X.append(det3([cc[0][0], cc[1][0], cc[2][0]], [cc[0][1], cc[1][1], cc[2][1]],
                          [cc[0][2], cc[1][2], cc[2][2]]))
        s = 1 if m > 0 else -1
        if all(s * (n[0] * X[0] + n[1] * X[1] + n[2] * X[2] + d * m) >= 0 for n, d in cons):
            return True
    return False


def flat(boxes, planes):
    return [i for i, (lo, hi) in enumerate(boxes) if classify(lo, hi, planes, range(len(planes))) is not None]


def signed_permutation(rng):
    perm = list(range(3))
    rng.shuffle(perm)
    sign = [rng.choice((1, -1)) for _ in range(3)]
    return lambda v: tuple(sign[k] * v[perm[k]] for k in range(3))


def random_frustum(rng):
    left = rng.randint(-4, 1)
    right = left + rng.randint(1, 5)
    bottom = rng.randint(-4, 1)
    top = bottom + rng.randint(1, 5)
    near = rng.randint(1, 3)
    far = near + rng.randint(2, 10)
    local = frustum_planes((0, 0, 0), left, right, bottom, top, near, far)
    turn = signed_permutation(rng)
    eye = tuple(rng.randint(-3, 3) for _ in range(3))
    planes = []
    for n, d in local:
        m = turn(n)
        planes.append((m, d - (m[0] * eye[0] + m[1] * eye[1] + m[2] * eye[2])))
    return planes, (left, right, bottom, top, near, far), turn, eye


def random_boxes(rng, shape, turn, eye, count):
    left, right, bottom, top, near, far = shape
    boxes = []
    for _ in range(count):
        t = rng.randint(near, far)
        x = rng.randint(left * t // near - 3, right * t // near + 3)
        y = rng.randint(bottom * t // near - 3, top * t // near + 3)
        c = turn((x, y, -t + rng.randint(-2, 2)))
        c = tuple(c[k] + eye[k] for k in range(3))
        size = [rng.randint(0, 4) for _ in range(3)]
        lo = tuple(c[k] - rng.randint(0, size[k]) for k in range(3))
        boxes.append((lo, tuple(lo[k] + size[k] for k in range(3))))
    return boxes


def test_worked_example():
    assert classify(*A, EXAMPLE, range(6)) == []  # wholly inside
    assert classify(*B, EXAMPLE, range(6)) is None  # outside the right plane
    assert classify(*C, EXAMPLE, range(6)) == [1, 3]  # straddles right and top
    assert classify(*D, EXAMPLE, range(6)) == [1, 5]  # straddles right and far
    assert classify(*E, EXAMPLE, range(6)) == [0]  # straddles left
    boxes = [A, B, C, D, E]
    assert frustum_cull(build_bvh(boxes), boxes, EXAMPLE) == [0, 2, 3, 4]
    assert [intersects(b, EXAMPLE) for b in boxes] == [True, False, True, False, True]
    # D is kept but does not meet the frustum: the test is conservative.


def test_never_drops_a_box_that_meets_the_frustum():
    rng = random.Random(41)
    extra = 0
    for case in range(500):
        planes, shape, turn, eye = random_frustum(rng)
        boxes = random_boxes(rng, shape, turn, eye, rng.randint(1, 8))
        kept = frustum_cull(build_bvh(boxes, rng.randint(1, 3)), boxes, planes)
        assert kept == flat(boxes, planes)
        exact = [i for i, b in enumerate(boxes) if intersects(b, planes)]
        for i, (lo, hi) in enumerate(boxes):  # a check of the oracle with sample points
            for p in itertools.product(*[(2 * lo[k], lo[k] + hi[k], 2 * hi[k]) for k in range(3)]):
                if all(n[0] * p[0] + n[1] * p[1] + n[2] * p[2] + 2 * d >= 0 for n, d in planes):
                    assert i in exact
        assert set(exact) <= set(kept)
        extra += len(kept) - len(exact)
    assert extra > 0


def test_hierarchy_gives_the_flat_answer_on_large_scenes():
    rng = random.Random(42)
    for case in range(40):
        planes, shape, turn, eye = random_frustum(rng)
        boxes = random_boxes(rng, shape, turn, eye, 60)
        for leaf in (1, 2, 5):
            assert frustum_cull(build_bvh(boxes, leaf), boxes, planes) == flat(boxes, planes)


def test_corner_test_is_wrong_for_a_box_around_the_frustum():
    big = ((-20, -20, -30), (20, 20, 1))
    corners = list(itertools.product(*zip(*big)))
    assert not any(all(n[0] * c[0] + n[1] * c[1] + n[2] * c[2] + d >= 0 for n, d in EXAMPLE) for c in corners)
    assert intersects(big, EXAMPLE)
    assert frustum_cull(build_bvh([big]), [big], EXAMPLE) == [0]


def test_outward_normals_cull_everything():
    flipped = [((-n[0], -n[1], -n[2]), -d) for n, d in EXAMPLE]
    assert frustum_cull(build_bvh([A]), [A], flipped) == []
    assert intersects(A, EXAMPLE)


def test_edges():
    assert frustum_cull(build_bvh([]), [], EXAMPLE) == []
    point_on_near = ((0, 0, -1), (0, 0, -1))
    assert frustum_cull(build_bvh([point_on_near]), [point_on_near], EXAMPLE) == [0]
    just_behind = ((0, 0, 0), (1, 1, 0))
    assert frustum_cull(build_bvh([just_behind]), [just_behind], EXAMPLE) == []
    corner_touch = ((10, 10, -11), (11, 11, -10))  # touches the far corner (10, 10, -10)
    assert intersects(corner_touch, EXAMPLE)
    assert frustum_cull(build_bvh([corner_touch]), [corner_touch], EXAMPLE) == [0]
