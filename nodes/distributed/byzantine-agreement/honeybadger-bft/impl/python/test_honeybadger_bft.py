# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/honeybadger-bft/. The authors are listed in prov/QX6G31.jsonl.

import itertools

from honeybadger_bft import STRATEGIES, Crypto, check, epoch


def test_agreement_and_termination_all_traitor_sets():
    rounds = []
    for n, f, seeds in ((4, 1, range(3)), (7, 2, range(1))):
        for faulty in itertools.combinations(range(n), f):
            slow_node = next(i for i in range(n) if i not in faulty)
            for strat in STRATEGIES:
                for seed in seeds:
                    for slow in ((), (slow_node,)):
                        res = epoch(n, f, set(faulty), strat, seed=seed, slow=slow)
                        assert check(res, n, f) == [], (n, faulty, strat, seed, slow)
                        rounds += res["aba_rounds"]
    mean = sum(rounds) / len(rounds)
    assert 1 <= mean <= 3, mean  # expected rounds of each binary agreement are constant


def test_block_holds_the_batches_of_the_subset():
    n, f = 4, 1
    res = epoch(n, f, {3}, "silent", seed=2, batch=40)
    subset = res["subsets"][0]
    assert len(subset) >= n - f and 3 not in subset
    assert res["txs"] == len(subset) * (40 // n)


def test_bad_encoding_is_left_out():
    for seed in range(5):
        res = epoch(4, 1, {1}, "bad_encoding", seed=seed)
        assert check(res, 4, 1) == []
        assert all(1 not in s for s in res["subsets"].values())


def test_linear_bytes_per_transaction_for_large_batches():
    ratios = {}
    for n, f in ((4, 1), (7, 2), (10, 3)):
        res = epoch(n, f, batch=40 * n * n)
        ratios[n] = res["bytes"] / res["txs"] / (250 * n)
    # Bytes per transaction divided by n * |tx| stay near n^2 / (n (n - 2f)) <= 3.
    assert all(2 <= r <= 3.5 for r in ratios.values()), ratios
    small = epoch(7, 2, batch=7)
    assert small["bytes"] / small["txs"] / (250 * 7) > 10  # small batches pay the overhead


def test_threshold_decryption_needs_f_plus_1_valid_shares():
    c = Crypto(4, 1, seed=0)
    ct = c.encrypt([("tx", 0, 0)])
    s0, s1 = c.dec_share(ct, 0), c.dec_share(ct, 1)
    assert c.decrypt(ct, {s0}) is None
    assert c.decrypt(ct, {s0, ("dec", ct, 2)}) is None  # a forged share for node 2
    assert c.decrypt(ct, {s0, s1}) == (("tx", 0, 0),)


def test_forged_fragments_and_coin_shares_are_rejected():
    c = Crypto(4, 1, seed=0)
    root, frags = c.encode("x", 100)
    assert c.frag_ok(root, frags[2])
    assert not c.frag_ok(root, ("frag", root, 9)) and not c.frag_ok(("root", 99), frags[2])
    share = c.coin_share(0, 0, 3)
    assert c.coin(0, 0, {share, ("coin", 0, 0, 1)}) is None
    assert c.coin(0, 0, {share, c.coin_share(0, 0, 2)}) in (0, 1)
