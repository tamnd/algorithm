# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cure/. The authors are listed in prov/C6AZ80.jsonl.

import math
import random

from cure import Cluster, cure, dist, hierarchical, label_points, make_cluster, scattered_points


def singletons(points):
    return [Cluster([p], tuple(p), [tuple(p)]) for p in points]


def partition(clusters):
    return sorted(sorted(u.points) for u in clusters)


def single_linkage(points, k):
    """Kruskal on all pairs, stopped at k components."""
    n = len(points)
    root = list(range(n))

    def find(x):
        while root[x] != x:
            x = root[x]
        return x

    comps = n
    for _, i, j in sorted((dist(points[i], points[j]), i, j) for i in range(n) for j in range(i + 1, n)):
        if comps == k:
            break
        if find(i) != find(j):
            root[find(i)] = find(j)
            comps -= 1
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(points[i])
    return sorted(sorted(g) for g in groups.values())


def centroid_linkage(points, k):
    clusters = [[p] for p in points]

    def mean(g):
        return tuple(sum(p[t] for p in g) / len(g) for t in range(len(g[0])))

    while len(clusters) > k:
        _, i, j = min((dist(mean(a), mean(b)), i, j) for i, a in enumerate(clusters)
                      for j, b in enumerate(clusters) if i < j)
        clusters[i] = clusters[i] + clusters[j]
        del clusters[j]
    return sorted(sorted(g) for g in clusters)


def random_points(rng, n):
    return [(rng.uniform(0, 10), rng.uniform(0, 10)) for _ in range(n)]


def test_alpha_zero_with_many_representatives_is_single_linkage():
    rng = random.Random(1)
    for _ in range(25):
        n = rng.randrange(2, 30)
        pts = random_points(rng, n)
        k = rng.randrange(1, n + 1)
        got = hierarchical(singletons(pts), k, c=n, alpha=0.0)
        assert partition(got) == single_linkage(pts, k)


def test_alpha_one_is_centroid_linkage():
    rng = random.Random(2)
    for _ in range(25):
        n = rng.randrange(2, 25)
        pts = random_points(rng, n)
        k = rng.randrange(1, n + 1)
        for c in (1, 4):
            got = hierarchical(singletons(pts), k, c=c, alpha=1.0)
            assert partition(got) == centroid_linkage(pts, k)


def test_representatives_are_shrunk_scattered_points():
    rng = random.Random(3)
    for _ in range(30):
        pts = random_points(rng, rng.randrange(1, 20))
        c, alpha = rng.randrange(1, 8), rng.choice([0.0, 0.2, 0.5, 1.0])
        u = make_cluster(pts, c, alpha)
        mean = tuple(sum(p[t] for p in pts) / len(pts) for t in range(2))
        assert all(abs(a - b) < 1e-12 for a, b in zip(u.mean, mean))
        assert len(u.rep) == min(c, len(pts))
        chosen = scattered_points(pts, mean, c)
        # Brute force farthest point rule.
        first = max(range(len(pts)), key=lambda j: (dist(pts[j], mean), -j))
        assert chosen[0] == pts[first]
        for i in range(1, len(chosen)):
            before = chosen[:i]
            gap = min(dist(chosen[i], q) for q in before)
            assert gap >= max(min(dist(p, q) for q in before) for p in pts if p not in before) - 1e-12
        for p, r in zip(chosen, u.rep):
            for t in range(2):
                assert abs(r[t] - (p[t] + alpha * (mean[t] - p[t]))) < 1e-12


def test_one_partition_without_sampling_is_the_plain_run():
    rng = random.Random(4)
    for _ in range(10):
        pts = random_points(rng, rng.randrange(2, 40))
        k = rng.randrange(1, 5)
        labels, clusters = cure(pts, k, c=5, alpha=0.3)
        plain = hierarchical(singletons(pts), k, 5, 0.3)
        assert partition(clusters) == partition(plain)
        assert labels == label_points(pts, plain)


def test_labels_use_the_nearest_representative():
    rng = random.Random(5)
    pts = random_points(rng, 60)
    labels, clusters = cure(pts, 3, c=4, alpha=0.5, rng=rng, sample_size=30, partitions=2)
    assert len(clusters) == 3
    for x, lab in zip(pts, labels):
        best = min(dist(x, r) for u in clusters for r in u.rep)
        assert min(dist(x, r) for r in clusters[lab].rep) == best


def test_elongated_clusters():
    # Two long parallel bars and a blob. Centroid linkage cuts the bars;
    # CURE with scattered representatives keeps them whole.
    bars = [(x * 0.5, 0.0) for x in range(30)] + [(x * 0.5, 3.0) for x in range(30)]
    pts = bars + [(7.0, 10.0 + 0.3 * t) for t in range(5)]
    labels, clusters = cure(pts, 3, c=10, alpha=0.2)
    assert len(set(labels[:30])) == 1 and len(set(labels[30:60])) == 1 and len(set(labels[60:])) == 1
    assert len({labels[0], labels[30], labels[60]}) == 3
    assert centroid_linkage(pts, 3) != partition(clusters)


def test_outliers_are_removed_from_the_sample():
    rng = random.Random(6)
    pts = [(rng.gauss(0, 0.3), rng.gauss(0, 0.3)) for _ in range(30)]
    pts += [(rng.gauss(5, 0.3), rng.gauss(0, 0.3)) for _ in range(30)]
    far = [(20.0, 20.0), (-20.0, 15.0)]
    labels, clusters = cure(pts + far, 2, c=5, alpha=0.3, outlier_at=20, outlier_size=3)
    assert len(clusters) == 2
    kept = [p for u in clusters for p in u.points]
    assert all(f not in kept for f in far)
    assert len(set(labels[:30])) == 1 and len(set(labels[30:60])) == 1 and labels[0] != labels[30]


def test_example_of_the_page():
    pts = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0), (7.0, 0.0), (2.0, 4.5)]
    bar = make_cluster(pts[:5], 2, 0.5)
    assert bar.mean == (2.0, 0.0)
    assert bar.rep == [(1.0, 0.0), (3.0, 0.0)]
    b, c = singletons(pts[5:6])[0], singletons(pts[6:])[0]
    from cure import cluster_dist
    assert cluster_dist(bar, b) == 4.0 and round(cluster_dist(bar, c), 2) == 4.61
    labels, _ = cure(pts, 2, c=2, alpha=0.5)
    assert labels == [1, 1, 1, 1, 1, 1, 0]
    labels, _ = cure(pts, 2, c=2, alpha=1.0)  # centroid linkage joins the far point above
    assert labels == [1, 1, 1, 1, 1, 0, 1]


def test_edges():
    assert cure([], 2) == ([], [])
    labels, clusters = cure([(1.0, 1.0)], 3)
    assert labels == [0] and len(clusters) == 1
    assert math.isclose(dist((0, 0), (3, 4)), 5)
