# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/differential-file/. The authors are listed in prov/PBST4C.jsonl.

"""The differential file against a flat dict that holds the same relation."""

import math
import random

from differential_file import DifferentialFile


def initial(rng: random.Random, n: int = 150) -> dict:
    return {k: rng.randint(0, 9) for k in rng.sample(range(200), n)}


def test_random_operations_match_the_flat_relation() -> None:
    for seed in range(5):
        rng = random.Random(seed)
        flat = initial(rng)
        df = DifferentialFile(flat, m=128, k=3)
        for step in range(600):
            r = rng.random()
            key = rng.randrange(220)
            if r < 0.3:
                v = rng.randint(0, 9)
                df.put(key, v)
                flat[key] = v
            elif r < 0.4:
                df.delete(key)
                flat.pop(key, None)
            elif r < 0.42:
                generation = dict(df.main)
                df.reorganize()
                assert df.main == flat and not df.diff and df.bits == 0
                assert generation == df.archive[-2]
            else:
                assert df.lookup(key) == flat.get(key)
            if step % 50 == 0:
                assert df.scan() == sorted(flat.items())


def test_main_file_is_read_only_between_reorganizations() -> None:
    rng = random.Random(7)
    flat = initial(rng)
    df = DifferentialFile(flat)
    before = dict(df.main)
    for _ in range(100):
        df.put(rng.randrange(200), rng.randint(0, 9))
        df.delete(rng.randrange(200))
    assert df.main == before == df.archive[-1]


def test_no_false_negatives() -> None:
    rng = random.Random(3)
    df = DifferentialFile({}, m=64, k=2)
    for key in rng.sample(range(10_000), 60):
        df.put(key, 1)
    assert all(df.maybe_changed(key) for key in df.diff)


def test_false_positive_rate_near_the_formula() -> None:
    rng = random.Random(11)
    m, k, n = 1024, 4, 150
    keys = rng.sample(range(100_000), n + 2000)
    df = DifferentialFile({key: 0 for key in keys[n:]}, m=m, k=k)
    for key in keys[:n]:
        df.put(key, 1)
    for key in keys[n:]:
        assert df.lookup(key) == 0
    rate = df.false_positives / 2000
    expected = (1 - math.exp(-k * n / m)) ** k
    assert abs(rate - expected) < 0.02
    # each lookup of an unchanged key reads M once and D only on a false positive
    assert df.main_reads == 2000 and df.diff_reads == df.false_positives


def test_restore_main_after_its_loss() -> None:
    rng = random.Random(5)
    flat = initial(rng)
    df = DifferentialFile(flat)
    for _ in range(40):
        df.put(rng.randrange(200), rng.randint(0, 9))
    df.reorganize()
    for _ in range(40):
        key = rng.randrange(200)
        df.delete(key)
    expect = df.scan()
    df.main = {}  # the disk that held M fails
    df.restore_main()
    assert df.scan() == expect


def test_hand_example() -> None:
    df = DifferentialFile({1: "a", 2: "b", 3: "c"}, m=32, k=2)
    df.put(2, "B")
    df.delete(3)
    df.put(4, "d")
    assert [df.lookup(x) for x in (1, 2, 3, 4, 5)] == ["a", "B", None, "d", None]
    assert df.scan() == [(1, "a"), (2, "B"), (4, "d")]
    df.reorganize()
    assert df.main == {1: "a", 2: "B", 4: "d"}
