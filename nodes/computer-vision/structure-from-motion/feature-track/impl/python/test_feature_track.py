# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feature-track/. The authors are listed in prov/MRQ8VT.jsonl.

import random

from feature_track import DisjointSet, build_tracks, split_by_image


def components_by_search(matches):
    adj = {}
    for a, b in matches:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    seen, comps = set(), []
    for s in adj:
        if s in seen:
            continue
        stack, comp = [s], []
        seen.add(s)
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        comps.append(frozenset(comp))
    return set(comps)


def test_chain_of_matches_is_one_track():
    matches = [((0, 4), (1, 7)), ((1, 7), (2, 1)), ((2, 1), (3, 9))]
    tracks = build_tracks(matches)
    assert tracks == [([(0, 4), (1, 7), (2, 1), (3, 9)], True)]


def test_two_features_in_one_image_make_an_inconsistent_track():
    matches = [((0, 4), (1, 7)), ((1, 7), (2, 1)), ((2, 1), (0, 5)), ((3, 0), (4, 0))]
    tracks = build_tracks(matches)
    assert len(tracks) == 2
    bad = [t for t, ok in tracks if not ok]
    assert bad == [[(0, 4), (0, 5), (1, 7), (2, 1)]]
    assert split_by_image(bad[0])[0] == [4, 5]


def test_random_matches_agree_with_graph_search():
    rng = random.Random(3)
    for _ in range(20):
        n_img, n_feat = rng.randint(2, 6), rng.randint(1, 8)
        matches = []
        for _ in range(rng.randint(0, 30)):
            a, b = rng.sample(range(n_img), 2)
            matches.append(((a, rng.randrange(n_feat)), (b, rng.randrange(n_feat))))
        tracks = build_tracks(matches)
        assert {frozenset(t) for t, _ in tracks} == components_by_search(matches)
        for t, ok in tracks:
            imgs = [i for i, _ in t]
            assert ok == (len(imgs) == len(set(imgs)))


def test_match_order_does_not_matter():
    rng = random.Random(4)
    matches = [((rng.randrange(5), rng.randrange(6)), (rng.randrange(5, 9), rng.randrange(6)))
               for _ in range(25)]
    first = build_tracks(matches)
    for _ in range(5):
        rng.shuffle(matches)
        assert build_tracks(matches) == first


def test_union_by_size_keeps_trees_shallow():
    ds = DisjointSet()
    nodes = [(0, k) for k in range(1024)]
    for x in nodes:
        ds.add(x)
    for k in range(1, 1024):
        ds.union(nodes[k - 1], nodes[k])
    # union by size alone bounds the depth by log2(1024) = 10
    depth = 0
    for x in nodes:
        d = 0
        while ds.parent[x] != x:
            x = ds.parent[x]
            d += 1
        depth = max(depth, d)
    assert depth <= 10
