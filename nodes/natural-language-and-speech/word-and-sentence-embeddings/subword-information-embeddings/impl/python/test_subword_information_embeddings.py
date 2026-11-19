# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subword-information-embeddings/. The authors are listed in prov/3998JC.jsonl.

import math
import random

from subword_information_embeddings import (
    NoiseSampler,
    char_ngrams,
    embed,
    fnv1a_32,
    pair_gradient,
    pair_loss,
    subword_rows,
    train,
    word_vector,
)


def cos(u, v):
    return sum(a * b for a, b in zip(u, v)) / math.sqrt(sum(a * a for a in u) * sum(b * b for b in v))


def test_ngrams_of_where():
    assert char_ngrams("where", 3, 3) == ["<wh", "whe", "her", "ere", "re>"]
    grams = char_ngrams("where")
    assert len(grams) == 5 + 4 + 3 + 2
    assert "<where" in grams and "where>" in grams and "<where>" not in grams
    assert "her" in grams and "<her>" not in grams


def test_ngram_count_formula():
    for word in ["a", "ab", "abc", "abcdefgh", "abcdefghijk"]:
        m = len(word) + 2
        expect = sum(max(0, m - n + 1) for n in range(3, 7))
        assert len(char_ngrams(word)) == expect


def test_fnv1a_standard_vectors():
    assert fnv1a_32("", signed_bytes=False) == 0x811C9DC5
    assert fnv1a_32("a", signed_bytes=False) == 0xE40C292C
    assert fnv1a_32("foobar", signed_bytes=False) == 0xBF9CF968
    assert fnv1a_32("foobar") == 0xBF9CF968  # ASCII: no difference


def test_fnv1a_signed_byte_quirk():
    plain, quirk = fnv1a_32("é", signed_bytes=False), fnv1a_32("é")
    assert plain != quirk
    h = 2166136261
    for b in "é".encode("utf-8"):
        h = ((h ^ (b - 256 + 2 ** 32)) * 16777619) % 2 ** 32
    assert quirk == h


def test_rows_of_seen_and_unseen_words():
    vocab = {"where": 0, "here": 1}
    seen = subword_rows("where", vocab, 100)
    unseen = subword_rows("wherever", vocab, 100)
    assert seen[0] == 0 and len(seen) == 15
    assert all(2 <= r < 102 for r in seen[1:]) and all(2 <= r < 102 for r in unseen)
    assert len(unseen) == len(char_ngrams("wherever"))


def test_gradient_against_finite_differences():
    rng = random.Random(1)
    d, nrows, nwords = 4, 30, 6
    z = [[rng.uniform(-0.5, 0.5) for _ in range(d)] for _ in range(nrows)]
    v = [[rng.uniform(-0.5, 0.5) for _ in range(d)] for _ in range(nwords)]
    rows, ctx, neg = [0, 7, 7, 12, 29], 2, [1, 4, 4]
    gz, gv = pair_gradient(z, v, rows, ctx, neg)
    h = 1e-6
    for mat, grads in ((z, gz), (v, gv)):
        for r in range(len(mat)):
            for k in range(d):
                old = mat[r][k]
                mat[r][k] = old + h
                up = pair_loss(z, v, rows, ctx, neg)
                mat[r][k] = old - h
                down = pair_loss(z, v, rows, ctx, neg)
                mat[r][k] = old
                num = (up - down) / (2 * h)
                ana = grads.get(r, [0.0] * d)[k]
                assert abs(num - ana) < 1e-5


def test_noise_distribution():
    sampler = NoiseSampler([8, 4, 2, 1, 1])
    z = sum(c ** 0.75 for c in [8, 4, 2, 1, 1])
    exact = [c ** 0.75 / z for c in [8, 4, 2, 1, 1]]
    rng = random.Random(2)
    n = 20000
    freq = [0] * 5
    for _ in range(n):
        freq[sampler.draw(rng)] += 1
    assert all(abs(f / n - p) < 0.01 for f, p in zip(freq, exact))


def planted_corpus(seed=0, sentences=80, length=6):
    """Words of stem pak meet only contexts x*, words of stem zot meet only contexts y*."""
    rng = random.Random(seed)
    groups = [(["pakir", "pakor", "pakus", "pakel", "pakim"], ["xo", "xu", "xi"]),
              (["zotir", "zotor", "zotus", "zotel", "zotim"], ["yo", "yu", "yi"])]
    corpus = []
    for _ in range(sentences):
        words, ctx = groups[rng.randrange(2)]
        corpus.append([rng.choice(words) if k % 2 == 0 else rng.choice(ctx) for k in range(length)])
    return corpus, groups


def test_planted_clusters_and_unseen_word():
    corpus, groups = planted_corpus(seed=3)
    vocab, z, _ = train(corpus, d=8, epochs=4, window=2, negatives=3, lr=0.05,
                        buckets=500, minn=3, maxn=4, seed=3)
    vec = {w: embed(w, vocab, z, 500, 3, 4) for w in vocab}
    (a, _), (b, _) = groups
    inside = [cos(vec[u], vec[v]) for g in (a, b) for k, u in enumerate(g) for v in g[k + 1:]]
    across = [cos(vec[u], vec[v]) for u in a for v in b]
    assert min(inside) > max(across)
    new = embed("pakar", vocab, z, 500, 3, 4)  # never seen in training
    assert "pakar" not in vocab and any(abs(t) > 0 for t in new)
    mean_a = [sum(c) / len(a) for c in zip(*(vec[w] for w in a))]
    mean_b = [sum(c) / len(b) for c in zip(*(vec[w] for w in b))]
    assert cos(new, mean_a) > cos(new, mean_b) + 0.3


def test_vector_is_sum_of_rows():
    rng = random.Random(4)
    z = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(10)]
    rows = [2, 5, 5, 9]
    got = word_vector(z, rows)
    ref = [z[2][k] + 2 * z[5][k] + z[9][k] for k in range(3)]
    assert max(abs(x - y) for x, y in zip(got, ref)) < 1e-15
    mean = word_vector(z, rows, mean=True)
    assert max(abs(x - y / 4) for x, y in zip(mean, ref)) < 1e-15
