# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/privacy-preserving-record-linkage/. The authors are listed in prov/KHENH3.jsonl.
import hashlib
import hmac
import random
from fractions import Fraction as F

from privacy_preserving_record_linkage import dice, encode, link, normalize, positions, qgrams

# Made-up keys for the tests only. A real linkage draws its keys from a cryptographic source.
K1 = b"demo-key-1"
K2 = b"demo-key-2"
SYLLABLES = ["ka", "lo", "mi", "ne", "ru", "sa", "to", "vi", "ze", "po", "an", "el", "or"]


def made_up_name(rng: random.Random) -> str:
    return "".join(rng.choice(SYLLABLES) for _ in range(rng.randint(2, 4)))


def typo(rng: random.Random, s: str) -> str:
    i = rng.randrange(len(s))
    return s[:i] + rng.choice("abcdefghijklmnopqrstuvwxyz") + s[i + 1 :]


def oracle_bits(s: str, k: int, m: int, q: int = 2) -> set[int]:
    """An independent encoding: the set of bit positions, from a set of q-grams."""
    t = "_" * (q - 1) + " ".join(s.lower().split()) + "_" * (q - 1)
    grams = {t[i : i + q] for i in range(len(t) - q + 1)}
    bits = set()
    for g in grams:
        h1 = int(hmac.new(K1, g.encode(), hashlib.sha1).hexdigest(), 16)
        h2 = int(hmac.new(K2, g.encode(), hashlib.md5).hexdigest(), 16)
        bits |= {(h1 + i * h2) % m for i in range(k)}
    return bits


def oracle_dice(x: set[int], y: set[int]) -> F:
    return F(2 * len(x & y), len(x) + len(y)) if x or y else F(0)


def test_page_example() -> None:
    assert qgrams("smith") == ["_s", "sm", "mi", "it", "th", "h_"]
    assert qgrams("ab", q=3) == ["__a", "_ab", "ab_", "b__"]
    assert normalize("  Smith  Jones ") == "smith jones"
    assert positions("sm", K1, K2, 2, 30) == [12, 12]
    smith, smyth, jones = (encode(s, K1, K2, 2, 30) for s in ("smith", "smyth", "jones"))
    assert {i for i in range(30) if smith >> i & 1} == {0, 4, 5, 8, 9, 12, 15, 18, 20}
    assert {i for i in range(30) if smyth >> i & 1} == {4, 5, 7, 8, 11, 12, 15, 19, 20, 22}
    assert {i for i in range(30) if jones >> i & 1} == {4, 6, 9, 14, 16, 21, 22, 23, 26, 28}
    assert dice(smith, smyth) == F(12, 19)
    assert dice(smith, jones) == F(4, 19)
    assert dice(smyth, jones) == F(1, 5)
    assert link(["smith", "jones"], ["smyth", "Jones"], K1, K2, 2, 30, F(3, 5)) == [(0, 0, F(12, 19)), (1, 1, F(1))]
    # A longer filter with more hash functions.
    a, b = encode("smith", K1, K2, 15, 1000), encode("smyth", K1, K2, 15, 1000)
    assert dice(a, b) == F(61, 89)


def test_against_oracle() -> None:
    rng = random.Random(41)
    for _ in range(500):
        k = rng.randint(1, 6)
        m = rng.choice([16, 30, 64, 200])
        x = made_up_name(rng)
        y = typo(rng, x) if rng.random() < 0.5 else made_up_name(rng)
        fx, fy = encode(x, K1, K2, k, m), encode(y, K1, K2, k, m)
        ox, oy = oracle_bits(x, k, m), oracle_bits(y, k, m)
        assert {i for i in range(m) if fx >> i & 1} == ox
        assert fx < 1 << m
        assert dice(fx, fy) == oracle_dice(ox, oy)


def test_link_against_brute_force() -> None:
    rng = random.Random(2009)
    for _ in range(20):
        left = [made_up_name(rng) for _ in range(rng.randint(1, 8))]
        right = [typo(rng, s) if rng.random() < 0.6 else made_up_name(rng) for s in left]
        rng.shuffle(right)
        theta = F(rng.randint(3, 9), 10)
        want = []
        for i, s in enumerate(left):
            for j, t in enumerate(right):
                d = oracle_dice(oracle_bits(s, 10, 500), oracle_bits(t, 10, 500))
                if d >= theta:
                    want.append((i, j, d))
        assert link(left, right, K1, K2, 10, 500, theta) == want


def test_properties() -> None:
    rng = random.Random(7)
    for _ in range(200):
        s = made_up_name(rng)
        f = encode(s, K1, K2, 15, 500)
        # Equal identifiers after normalization give equal filters and Dice 1.
        assert encode(" " + s.upper() + " ", K1, K2, 15, 500) == f
        assert dice(f, f) == 1
        # At most k bits per q-gram.
        assert f.bit_count() <= 15 * len(qgrams(s))
        # The bits of the shared q-grams are shared bits.
        t = typo(rng, s)
        g = encode(t, K1, K2, 15, 500)
        for gram in set(qgrams(s)) & set(qgrams(t)):
            for p in positions(gram, K1, K2, 15, 500):
                assert f >> p & 1 and g >> p & 1
        assert 0 <= dice(f, g) <= 1 and dice(f, g) == dice(g, f)
    # Other keys give other filters.
    assert encode("smith", b"other-key-1", K2, 2, 30) != encode("smith", K1, K2, 2, 30)
    assert dice(0, 0) == 0


def test_bad_parameters() -> None:
    for args in ((0, 30, 2), (2, 0, 2)):
        try:
            encode("smith", K1, K2, args[0], args[1], args[2])
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    try:
        qgrams("smith", q=0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
