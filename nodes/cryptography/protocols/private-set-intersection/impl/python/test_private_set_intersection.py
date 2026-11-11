# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/private-set-intersection/. The authors are listed in prov/P1QYT2.jsonl.
# There are no official test vectors for PSI protocols. The tests compare the
# output with the plain intersection on random sets, check the worked example,
# check what each party receives, and run the dictionary attack on the naive
# hashing protocol, all on local simulated parties.

import random
from collections import Counter

from private_set_intersection import (
    SMALL_GROUP,
    TOY_GROUP,
    bin_of,
    cuckoo_insert,
    dh_psi,
    hash_to_group,
    naive_hash_psi_leak,
    oprf_psi,
)


def random_sets(rng: random.Random, n: int, m: int, common: int) -> tuple[list[str], list[str]]:
    pool = ["item-%d" % rng.getrandbits(40) for _ in range(n + m)]
    shared = pool[:common]
    return shared + pool[common:n], shared + pool[n:n + m - common]


def test_worked_example() -> None:
    g = SMALL_GROUP
    h = {x: hash_to_group(x, g) for x in ("alice", "bob", "carol", "dave")}
    assert h == {"alice": 1013, "bob": 803, "carol": 49, "dave": 953}
    a, b = 7, 11
    assert [pow(h[x], a, g.p) for x in ("alice", "bob", "carol")] == [289, 516, 816]
    assert [pow(pow(h[x], a, g.p), b, g.p) for x in ("alice", "bob", "carol")] == [411, 23, 424]
    assert [pow(h[y], b, g.p) for y in ("bob", "dave")] == [149, 500]
    assert [pow(pow(h[y], b, g.p), a, g.p) for y in ("bob", "dave")] == [23, 861]


def test_dh_psi_is_correct() -> None:
    rng = random.Random(1999)
    for _ in range(20):
        n, m = rng.randrange(1, 60), rng.randrange(1, 60)
        xs, ys = random_sets(rng, n, m, rng.randrange(0, min(n, m) + 1))
        run = dh_psi(xs, ys, TOY_GROUP, rng)
        assert run.intersection == set(xs) & set(ys)
        assert run.elements_sent == 2 * len(xs) + len(ys)
        assert all(TOY_GROUP.contains(v) for v in run.to_server + run.to_client_ys)


def test_server_messages_do_not_depend_on_items_outside_the_intersection() -> None:
    # Two server sets with the same size and the same intersection with xs.
    # In the small group, over many runs, the value H(y)^b that the client
    # gets for the item outside xs is uniform on the subgroup for both sets,
    # so it says nothing about which item it is.
    g = SMALL_GROUP
    rng = random.Random(7)
    xs = ["a", "b", "c"]
    for other in ("zeta", "omega"):
        counts: Counter[int] = Counter()
        runs = 8000
        for _ in range(runs):
            run = dh_psi(xs, ["b", other], g, rng)
            assert run.intersection == {"b"}
            assert len(set(run.to_client_xs)) == 3
            match = pow(hash_to_group("b", g), run.server_key, g.p)
            outside = [v for v in run.to_client_ys if v != match]
            assert len(outside) == 1
            counts[outside[0] % 8] += 1
        # the subgroup of 509 squares spread over 8 classes
        expected = Counter(pow(h, 2, g.p) % 8 for h in range(1, g.p))
        total = sum(expected.values())
        chi2 = sum((counts[c] - runs * expected[c] / total) ** 2 / (runs * expected[c] / total)
                   for c in range(8))
        assert chi2 < 30


def test_naive_hashing_leaks_the_whole_server_set() -> None:
    # A domain small enough to list, like 4-digit PINs or phone numbers.
    domain = ["%04d" % i for i in range(10_000)]
    rng = random.Random(3)
    ys = rng.sample(domain, 50)
    assert naive_hash_psi_leak(ys, domain) == set(ys)


def test_dh_values_cannot_be_matched_offline() -> None:
    # The client knows a, but H(y)^b for y outside xs matches no value the
    # client can make alone: H(z), H(z)^a for any z in the domain.
    rng = random.Random(4)
    domain = ["%03d" % i for i in range(1000)]
    ys = rng.sample(domain, 30)
    xs = ys[:5] + ["x%d" % i for i in range(5)]
    run = dh_psi(xs, ys, TOY_GROUP, rng)
    assert run.intersection == set(ys[:5])
    a = run.client_key
    offline = {hash_to_group(z, TOY_GROUP) for z in domain}
    offline |= {pow(h, a, TOY_GROUP.p) for h in offline}
    assert not offline & set(run.to_client_ys)


def test_cuckoo_table_places_every_item_once() -> None:
    rng = random.Random(5)
    items = ["k%d" % i for i in range(300)]
    nbins = 450
    table = cuckoo_insert(items, nbins, 77, rng)
    assert table is not None
    placed = [slot for slot in table if slot is not None]
    assert sorted(x for x, _ in placed) == sorted(items)
    assert all(bin_of(x, i, nbins, 77) == b for b, slot in enumerate(table) if slot for x, i in [slot])


def test_oprf_psi_is_correct_and_counts() -> None:
    rng = random.Random(2016)
    for n, m, c in ((50, 80, 20), (120, 40, 40), (30, 30, 0), (1, 1, 1)):
        xs, ys = random_sets(rng, n, m, c)
        run = oprf_psi(xs, ys, TOY_GROUP, rng)
        assert run.intersection == set(xs) & set(ys)
        assert run.oprf_calls == run.nbins >= len(xs)     # one per bin, not per pair
        assert run.sender_values == 3 * len(ys)
