# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-spline-linear-independence/. The authors are listed in prov/8C8B3H.jsonl.

import random
from fractions import Fraction as F

from t_spline_linear_independence import TMesh, blend, is_analysis_suitable, null_vector, nurbs_matrix, rank

HALF = F(1, 2)


def bcs_mesh(s=(HALF, HALF, HALF, F(2, 3)), t=(HALF, HALF, HALF)):
    """The T-mesh of Buffa, Cho and Sangalli (Figure 4 of Li and coauthors) in index space.

    The drawn lines are the columns 2..9 and the rows 2..8; the columns 0, 1,
    10, 11 and the rows 0, 1, 9, 10 repeat the end knots to make open knot
    vectors. T1, T2 and T3 of the figure are the anchors (4, 5), (5, 6), (6, 6).
    """
    sv = [F(0)] * 4 + list(s) + [F(1)] * 4
    tv = [F(0)] * 4 + list(t) + [F(1)] * 4
    T = TMesh(sv, tv)
    T.add_lines([0, 1, 2, 3, 5, 8, 9, 10, 11], [0, 1, 2, 3, 5, 7, 8, 9, 10])
    T.add_v(4, 0, 5)  # the column s = 1/2 that ends at T1
    T.add_h(0, 4, 4)  # the row that ends at that column
    T.add_v(6, 6, 10)  # two columns that start on the row of T2 and T3
    T.add_v(7, 6, 10)
    T.add_h(5, 11, 6)  # the row that starts at T2
    return T


def cross_mesh(vals, insertion_edges=True):
    """A tensor mesh with one face split into four; with the two insertion edges it is analysis-suitable."""
    T = TMesh(vals, vals)
    lines = [0, 1, 2, 3, 5, 7, 9, 11, 12, 13, 14]
    T.add_lines(lines, lines)
    T.add_v(6, 5, 7)
    T.add_h(3, 9, 6) if insertion_edges else T.add_h(5, 7, 6)
    return T


def random_values(rng, interior):
    xs = sorted(rng.sample(range(1, 1000), interior))
    return [F(0)] * 4 + [F(x, 1000) for x in xs] + [F(1)] * 4


def points(rng, k):
    return [(F(rng.randint(0, 100), 100), F(rng.randint(0, 100), 100)) for _ in range(k)]


def test_buffa_cho_sangalli_mesh_is_dependent():
    T = bcs_mesh()
    anchors, cols = nurbs_matrix(T)
    assert len(anchors) == 40 and len({k for c in cols for k in c}) == 56
    assert rank(cols) == 39
    assert not is_analysis_suitable(T)
    delta = null_vector(cols)
    support = {anchors[i]: d for i, d in enumerate(delta) if d}
    T1, T2, T3 = (4, 5), (5, 6), (6, 6)
    assert set(support) == {T1, T2, T3}
    assert support[T2] == -support[T1] and support[T3] == -support[T1] / 3
    rng = random.Random(1)
    for s, t in points(rng, 30):
        assert blend(T, T1, s, t) == blend(T, T2, s, t) + blend(T, T3, s, t) / 3


def test_full_rank_is_equivalent_to_independence_on_samples():
    """Theorem 1: the rank of M equals the rank of the blending functions sampled at many points."""
    rng = random.Random(2)
    pts = points(rng, 120)
    for T in (bcs_mesh(), bcs_mesh(s=(F(2, 5), HALF, F(3, 5), F(2, 3)))):
        anchors, cols = nurbs_matrix(T)
        sampled = [{p: blend(T, A, *p) for p in pts} for A in anchors]
        assert rank(sampled) == rank(cols)


def test_same_topology_with_other_knots_is_independent():
    """Li and coauthors: the mesh is dependent only if s2 = s3 = s4 and t2 = t3 = t4."""
    assert rank(nurbs_matrix(bcs_mesh(s=(F(2, 5), HALF, F(3, 5), F(2, 3))))[1]) == 40
    assert rank(nurbs_matrix(bcs_mesh(t=(F(2, 5), HALF, F(3, 5))))[1]) == 40
    assert rank(nurbs_matrix(bcs_mesh(s=(HALF, HALF, HALF, F(3, 4))))[1]) == 39


def test_analysis_suitable_meshes_are_independent_for_random_knots():
    rng = random.Random(3)
    for _ in range(6):
        vals = random_values(rng, 7)
        T = cross_mesh(vals)
        assert is_analysis_suitable(T)
        anchors, cols = nurbs_matrix(T)
        assert len(anchors) == 56 and rank(cols) == 56


def test_analysis_suitable_is_sufficient_but_not_necessary():
    T = cross_mesh([F(0)] * 4 + [F(k, 8) for k in range(1, 8)] + [F(1)] * 4, insertion_edges=False)
    assert not is_analysis_suitable(T)
    anchors, cols = nurbs_matrix(T)
    assert rank(cols) == len(anchors)


def test_tensor_mesh_matrix_is_the_identity():
    rng = random.Random(4)
    vals = random_values(rng, 5)
    T = TMesh(vals, vals)
    T.add_lines(range(13), range(13))
    anchors, cols = nurbs_matrix(T)
    assert is_analysis_suitable(T)
    for (i, j), c in zip(anchors, cols):
        assert c == {(i - 2, j - 2): 1}
