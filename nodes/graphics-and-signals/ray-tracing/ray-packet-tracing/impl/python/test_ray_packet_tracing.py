# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ray-packet-tracing/. The authors are listed in prov/Y70MRZ.jsonl.

import random
from fractions import Fraction as Q

from ray_packet_tracing import build_bvh, trace_linear, trace_packet, trace_single


def soup(rng, n, den=4):
    tris = []
    for _ in range(n):
        c = [rng.randint(-4, 4) for _ in range(3)]
        tris.append(tuple(tuple(Q(4 * c[a] + rng.randint(-7, 7), den) for a in range(3)) for _ in range(3)))
    return tris


def count_nodes(node):
    return 1 if "prims" in node else 1 + count_nodes(node["kids"][0]) + count_nodes(node["kids"][1])


def tile(eye, x0, y0, k, step):
    rays = []
    for y in range(k):
        for x in range(k):
            tgt = (x0 + x * step, y0 + y * step, Q(0))
            rays.append((eye, tuple(tgt[a] - eye[a] for a in range(3))))
    return rays


def test_coherent_packets_match_single_rays_and_linear_scan():
    rng = random.Random(51)
    hits = 0
    for _ in range(4):
        tris = soup(rng, 24)
        root = build_bvh(tris)
        eye = (Q(rng.randint(-3, 3), 7), Q(rng.randint(-3, 3), 5), Q(-15))
        for _ in range(4):
            x0, y0 = Q(rng.randint(-9, 6), 3), Q(rng.randint(-9, 6), 3)
            rays = tile(eye, x0, y0, 3, Q(1, 3))
            got = trace_packet(root, tris, rays)
            for (o, d), g in zip(rays, got):
                assert g == trace_single(root, tris, o, d) == trace_linear(tris, o, d)
                hits += g[0] is not None
    assert hits > 40


def test_incoherent_packets_match_single_rays():
    rng = random.Random(52)
    for _ in range(4):
        tris = soup(rng, 20)
        root = build_bvh(tris)
        rays = []
        for _ in range(8):  # different origins and direction signs in one packet
            o = tuple(Q(rng.randint(-20, 20), 3) for _ in range(3))
            d = tuple(Q(rng.randint(-9, 9), 2) for _ in range(3))
            if d != (0, 0, 0):
                rays.append((o, d))
        got = trace_packet(root, tris, rays)
        for (o, d), g in zip(rays, got):
            assert g == trace_linear(tris, o, d)


def test_order_of_rays_in_packet_does_not_matter():
    rng = random.Random(53)
    tris = soup(rng, 24)
    root = build_bvh(tris)
    rays = tile((Q(0), Q(0), Q(-10)), Q(-2), Q(-2), 3, Q(1, 2))
    base = trace_packet(root, tris, rays)
    for _ in range(3):
        perm = list(range(len(rays)))
        rng.shuffle(perm)
        got = trace_packet(root, tris, [rays[i] for i in perm])
        assert [got[perm.index(i)] for i in range(len(rays))] == base


def test_ties_are_broken_by_index():
    # Two copies of one triangle: both hits have the same t; the lower index wins in every order.
    tri = ((Q(-1), Q(-1), Q(0)), (Q(1), Q(-1), Q(0)), (Q(0), Q(1), Q(0)))
    far = ((Q(-1), Q(-1), Q(1)), (Q(1), Q(-1), Q(1)), (Q(0), Q(1), Q(1)))
    tris = [far, tri, tri, far]
    root = build_bvh(tris, leaf_size=1)
    ray = ((Q(0), Q(0), Q(-1)), (Q(0), Q(0), Q(1)))
    assert trace_packet(root, tris, [ray, ray]) == [(Q(1), 1), (Q(1), 1)]


def test_t_max_limits_every_ray():
    rng = random.Random(54)
    tris = soup(rng, 20)
    root = build_bvh(tris)
    rays = tile((Q(0), Q(0), Q(-15)), Q(-3), Q(-3), 3, Q(1))
    for t_max in (Q(1, 2), Q(1), Q(3, 2)):
        got = trace_packet(root, tris, rays, t_max)
        for (o, d), g in zip(rays, got):
            assert g == trace_linear(tris, o, d, t_max)


def test_each_node_is_visited_at_most_once_per_packet():
    rng = random.Random(55)
    tris = soup(rng, 24)
    root = build_bvh(tris)
    rays = tile((Q(0), Q(0), Q(-15)), Q(-4), Q(-4), 4, Q(2, 3))
    stats, single = {}, {}
    trace_packet(root, tris, rays, stats=stats)
    for o, d in rays:
        trace_single(root, tris, o, d, stats=single)
    assert stats["nodes"] <= count_nodes(root)
    assert stats["nodes"] < single["nodes"]  # this coherent packet shares node visits


def test_float_packets_match_float_single_rays():
    rng = random.Random(56)
    tris = []
    for _ in range(150):
        c = [rng.uniform(-4, 4) for _ in range(3)]
        tris.append(tuple(tuple(c[a] + rng.uniform(-0.7, 0.7) for a in range(3)) for _ in range(3)))
    root = build_bvh(tris)
    eye = (0.3, 0.2, -12.0)
    for by in range(0, 16, 4):
        for bx in range(0, 16, 4):
            rays = []
            for y in range(by, by + 4):
                for x in range(bx, bx + 4):
                    tgt = (-4 + 8 * x / 15, -4 + 8 * y / 15, 0.0)
                    rays.append((eye, tuple(tgt[a] - eye[a] for a in range(3))))
            got = trace_packet(root, tris, rays)
            for (o, d), g in zip(rays, got):
                assert g == trace_linear(tris, o, d)
