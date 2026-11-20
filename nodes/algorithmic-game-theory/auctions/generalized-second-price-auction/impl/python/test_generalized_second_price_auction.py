# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-second-price-auction/. The authors are listed in prov/ATPJNQ.jsonl.

import itertools
import random
from fractions import Fraction

from generalized_second_price_auction import eos_bids, gsp, revenue, utility, vcg_payments

DELTA = Fraction(1, 1000)


def is_nash(values, bids, ctrs):
    """Every deviation of every bidder is tried: each slot can be reached by
    a bid just above, equal to or just below some other bid, or by 0."""
    for i, v in enumerate(values):
        current = utility(v, bids, ctrs, i)
        others = [bids[j] for j in range(len(bids)) if j != i]
        candidates = {0} | {b + d for b in others for d in (-DELTA, 0, DELTA) if b + d >= 0}
        for c in candidates:
            if utility(v, bids[:i] + [c] + bids[i + 1:], ctrs, i) > current:
                return False
    return True


def slot_offers(bids, ctrs):
    """Price per click and click-through rate of every slot, plus no slot."""
    winners, prices = gsp(bids, ctrs)
    return winners, [(ctrs[s], prices[s]) for s in range(len(winners))] + [(0, 0)]


def is_envy_free(values, bids, ctrs):
    """Varian's symmetric Nash equilibrium: nobody prefers another slot at its price."""
    winners, offers = slot_offers(bids, ctrs)
    for i, v in enumerate(values):
        current = utility(v, bids, ctrs, i)
        if any(a * (v - p) > current for a, p in offers):
            return False
    return True


def is_locally_envy_free(values, bids, ctrs):
    """Edelman, Ostrovsky and Schwarz: the bidder at rank r does not envy rank r - 1,
    for 2 <= r <= min(slots + 1, bidders)."""
    ranked = sorted(range(len(bids)), key=lambda i: (-bids[i], i))
    alpha = list(ctrs) + [0]
    for r in range(1, min(len(ctrs) + 1, len(bids))):
        i = ranked[r]
        nxt = bids[ranked[r + 1]] if r + 1 < len(ranked) else 0
        if alpha[r] * (values[i] - nxt) < alpha[r - 1] * (values[i] - bids[i]):
            return False
    return True


def test_example() -> None:
    # Edelman, Ostrovsky and Schwarz, Section II: values 10, 4, 2 and 200, 199 clicks.
    values, ctrs = [10, 4, 2], [200, 199]
    assert gsp(values, ctrs) == ([0, 1], [4, 2])
    assert utility(10, values, ctrs, 0) == 1200
    assert utility(10, [3, 4, 2], ctrs, 0) == 1592
    # The VCG payments and the equilibrium bids b* of Theorem 1.
    assert vcg_payments(values, ctrs) == ([0, 1], [402, 398])
    assert eos_bids(values, ctrs) == [10, Fraction(402, 200), 2]
    b = eos_bids(values, ctrs)
    assert revenue(b, ctrs) == 800 == sum(vcg_payments(values, ctrs)[1])


def test_edges() -> None:
    assert gsp([], [3, 2]) == ([], [])
    assert gsp([5], [3, 2]) == ([0], [0])
    assert gsp([5], [3, 2], reserve=2) == ([0], [2])
    assert gsp([1, 5], [3, 2], reserve=2) == ([1], [2])
    assert gsp([5, 5, 5], [3, 2]) == ([0, 1], [5, 5])
    # One slot: GSP is the Vickrey auction.
    assert gsp([3, 9, 7], [1]) == ([1], [7])


def test_truthful_revenue_at_least_vcg() -> None:
    rng = random.Random(1)
    for _ in range(500):
        n, k = rng.randrange(1, 6), rng.randrange(1, 4)
        values = [rng.randrange(0, 20) for _ in range(n)]
        ctrs = sorted((rng.randrange(1, 10) for _ in range(k)), reverse=True)
        winners, pay = vcg_payments(values, ctrs)
        assert gsp(values, ctrs)[0] == winners
        assert revenue(values, ctrs) >= sum(pay)


def random_instance(rng):
    n, k = rng.randrange(2, 5), rng.randrange(1, 4)
    values = rng.sample(range(1, 30), n)
    ctrs = sorted(rng.sample(range(1, 20), k), reverse=True)
    return values, ctrs


def test_eos_bids_are_envy_free_equilibrium_with_vcg_outcome() -> None:
    rng = random.Random(2)
    for _ in range(300):
        values, ctrs = random_instance(rng)
        b = eos_bids(values, ctrs)
        assert is_nash(values, b, ctrs)
        assert is_envy_free(values, b, ctrs)
        assert is_locally_envy_free(values, b, ctrs)
        winners, prices = gsp(b, ctrs)
        vcg_winners, vcg_pay = vcg_payments(values, ctrs)
        assert winners == vcg_winners
        assert [ctrs[s] * prices[s] for s in range(len(winners))] == vcg_pay


def test_envy_free_equilibria_on_a_grid() -> None:
    # Every envy-free bid profile (Varian's symmetric Nash equilibrium) is
    # efficient and pays for each slot at least its VCG payment.
    rng = random.Random(3)
    grid = range(0, 8)
    count = 0
    for slots in (2, 2, 2, 1, 1, 1):
        values = rng.sample(range(1, 8), 3)
        ctrs = sorted(rng.sample(range(1, 6), slots), reverse=True)
        vcg_winners, vcg_pay = vcg_payments(values, ctrs)
        for bids in itertools.product(grid, repeat=3):
            bids = list(bids)
            if not is_envy_free(values, bids, ctrs):
                continue
            count += 1
            winners, prices = gsp(bids, ctrs)
            assert winners == vcg_winners
            assert all(ctrs[s] * prices[s] >= vcg_pay[s] for s in range(len(winners)))
    assert count > 0


def test_locally_envy_free_can_be_below_vcg() -> None:
    # One slot, values 5, 1, 8 and bids 10, 2, 0: a locally envy-free Nash
    # equilibrium in which the bidder with value 8 loses and revenue is 2 < 5.
    values, bids, ctrs = [5, 1, 8], [10, 2, 0], [1]
    assert is_nash(values, bids, ctrs)
    assert is_locally_envy_free(values, bids, ctrs)
    assert not is_envy_free(values, bids, ctrs)
    assert gsp(bids, ctrs) == ([0], [2])
    assert vcg_payments(values, ctrs) == ([2], [5])


def test_truthful_bidding_is_not_dominant() -> None:
    rng = random.Random(4)
    found = 0
    for _ in range(200):
        values, ctrs = random_instance(rng)
        if len(ctrs) < 2:
            continue
        for i, v in enumerate(values):
            truthful = utility(v, values, ctrs, i)
            others = [values[j] for j in range(len(values)) if j != i]
            for c in {o + d for o in others for d in (-DELTA, DELTA) if o + d >= 0}:
                if utility(v, values[:i] + [c] + values[i + 1:], ctrs, i) > truthful:
                    found += 1
                    break
    assert found > 0
