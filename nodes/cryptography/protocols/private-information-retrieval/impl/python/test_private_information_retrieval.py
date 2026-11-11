# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/private-information-retrieval/. The authors are listed in prov/Q7ZEPD.jsonl.
# There are no official test vectors for PIR schemes. The tests retrieve every
# position of random databases, check the communication counts, check the
# worked examples, and check what a single server sees, all with local
# simulated servers.

import math
import random
from collections import Counter

from private_information_retrieval import (
    GMKey,
    balanced_two_server,
    cube_pir,
    gm_keygen,
    jacobi,
    ko_answer,
    kushilevitz_ostrovsky,
    trivial,
)


def random_db(n: int, rng: random.Random) -> list[int]:
    return [rng.getrandbits(1) for _ in range(n)]


def test_worked_example_two_servers() -> None:
    x = [1, 0, 1, 1, 0, 0, 1, 0]            # x_1 .. x_8
    s1 = {2, 5, 7}
    s2 = s1 ^ {3}
    a1 = sum(x[j - 1] for j in s1) % 2
    a2 = sum(x[j - 1] for j in s2) % 2
    assert (a1, a2, a1 ^ a2) == (1, 0, x[2])


def test_basic_two_server_scheme() -> None:
    rng = random.Random(1995)
    n = 64
    db = random_db(n, rng)
    for i in range(n):
        bit, cost, _ = cube_pir(db, i, 1, rng)
        assert bit == db[i]
        assert (cost.up, cost.down) == (2 * n, 2)


def test_one_server_sees_a_uniform_subset() -> None:
    # n = 4: the query to server 2 is S xor {i}, uniform over the 16
    # subsets whatever i is.
    rng = random.Random(2)
    db = [1, 0, 1, 1]
    for i in (0, 3):
        counts = Counter(cube_pir(db, i, 1, rng)[2][1][0] for _ in range(16_000))
        chi2 = sum((counts[v] - 1000) ** 2 / 1000 for v in range(16))
        assert chi2 < 50


def test_square_scheme_with_four_servers() -> None:
    rng = random.Random(3)
    n = 100                                 # a 10 x 10 square
    db = random_db(n, rng)
    for i in range(n):
        bit, cost, queries = cube_pir(db, i, 2, rng)
        assert bit == db[i]
        assert (cost.up, cost.down) == (4 * 2 * 10, 4)
        assert len(queries) == 4


def test_cube_scheme_with_eight_servers() -> None:
    rng = random.Random(4)
    n = 216                                 # 6 x 6 x 6
    db = random_db(n, rng)
    for i in rng.sample(range(n), 40):
        bit, cost, _ = cube_pir(db, i, 3, rng)
        assert bit == db[i]
        assert (cost.up, cost.down) == (8 * 3 * 6, 8)


def test_balanced_two_server_scheme() -> None:
    rng = random.Random(5)
    n = 1024
    db = random_db(n, rng)
    for i in rng.sample(range(n), 100):
        bit, cost = balanced_two_server(db, i, rng)
        assert bit == db[i]
        assert (cost.up, cost.down) == (64, 64)     # 4 sqrt(n) bits in total


def test_trivial_scheme() -> None:
    db = [0, 1, 1, 0, 1]
    bit, cost = trivial(db, 2)
    assert (bit, cost.up, cost.down) == (1, 0, 5)


def test_ko_worked_example() -> None:
    key = GMKey(7, 11)                       # N = 77, both primes 3 mod 4
    db = [1, 0,
          0, 1]
    ys = [71, 73]                            # 71 = 15^2, 73 = -4 mod 77
    assert key.is_qr(71) and not key.is_qr(73)
    assert jacobi(71, 77) == jacobi(73, 77) == 1
    zs = ko_answer(db, 2, 2, ys, 77)
    assert zs == [58, 10]
    assert [0 if key.is_qr(z) else 1 for z in zs] == [0, 1]      # column 2


def test_kushilevitz_ostrovsky_single_server() -> None:
    rng = random.Random(1997)
    key = gm_keygen(31, rng)
    s = t = 16
    db = random_db(s * t, rng)
    k = key.n.bit_length()
    for i in range(s * t):
        bit, cost, ys = kushilevitz_ostrovsky(db, i, s, t, key, rng)
        assert bit == db[i]
        assert (cost.up, cost.down) == (k * t, k * s)
        # The server sees t numbers with Jacobi symbol +1 whatever the column.
        assert all(jacobi(y, key.n) == 1 for y in ys)


def costs(n: int, k: int) -> dict[str, int]:
    root = math.isqrt(n)
    return {
        "trivial": n,
        "2-server basic": 2 * n + 2,
        "2-server balanced": 4 * root,
        "4-server square": 4 * 2 * root + 4,
        "KO with GM": k * 2 * root,
    }


def test_communication_comparison() -> None:
    # With a 2048-bit modulus, one level of KO costs k * 2 sqrt(n) bits,
    # which beats sending the database only when n > 4 k^2 (about 2^24).
    k = 2048
    small = costs(1 << 20, k)
    assert small["2-server balanced"] == 4096
    assert small["4-server square"] == 8196
    assert small["KO with GM"] == 4 * small["trivial"]
    big = costs(1 << 30, k)
    assert big["KO with GM"] == big["trivial"] // 8
    assert costs(4 * k * k, k)["KO with GM"] == 4 * k * k
