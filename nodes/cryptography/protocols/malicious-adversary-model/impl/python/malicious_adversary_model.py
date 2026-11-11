# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/malicious-adversary-model/. The authors are listed in prov/EASH3X.jsonl.
"""A malicious party against an additive sharing sum, and a SPDZ-style MAC check.

plain_sum: the two-round additive sharing sum, secure only against
semi-honest parties. A malicious party that adds an error e to one message
shifts the output by e and nobody notices.

mac_sum: the same sum on authenticated shares, in the style of SPDZ
(Damgard, Pastro, Smart and Zakarias 2012). A trusted dealer, standing in for
the preprocessing phase, gives each party
  * a share alpha_j of a global MAC key alpha that no single party knows;
  * for each input owner i, a random mask r_i known to party i, with additive
    shares of r_i and of alpha * r_i.
To input x_i, party i broadcasts eps_i = x_i - r_i. The shares of the sum
and of its MAC are local sums. To open, every party broadcasts its share of
the sum; then each party commits to sigma_j = m_j - alpha_j * y', all open,
and they accept y' only if the sigma_j add up to 0.

A party that adds e to its share of y must add alpha * e to its sigma to
pass, and it does not know alpha, so it passes with probability 1/p. Without
the commitments, the last party to speak can choose its sigma after seeing
the others and always passes; the tests show both.

For study only: not constant time, a trusted dealer instead of a real
preprocessing protocol, Python's random module, and toy fields. Use a
maintained framework such as MP-SPDZ for real data.
"""

import hashlib
import random
from dataclasses import dataclass
from typing import Optional, Sequence

P61 = 2**61 - 1  # a Mersenne prime


def share(x: int, n: int, p: int, rng: random.Random) -> list[int]:
    """Additive shares of x modulo p."""
    s = [rng.randrange(p) for _ in range(n - 1)]
    return s + [(x - sum(s)) % p]


@dataclass
class Cheat:
    """What the malicious party does.

    party: its index; error: added to its broadcast share of the result;
    target: if set, the cheater speaks last in the round (it is rushing) and
    picks its share so that the opened result equals target;
    mac_shift: added to its sigma; rushing: if True, it waits for the other
    sigmas (possible only when there are no commitments) and picks its own
    so that the check passes.
    """

    party: int
    error: int = 0
    target: Optional[int] = None
    mac_shift: int = 0
    rushing: bool = False


def _cheat_share(own: int, others_total: int, honest_total: int, cheat: Cheat, p: int) -> int:
    """The share the cheater broadcasts in place of its true share own."""
    if cheat.target is not None:
        return (cheat.target - others_total) % p
    return (own + cheat.error) % p


def plain_sum(inputs: Sequence[int], p: int, rng: random.Random, cheat: Optional[Cheat] = None) -> int:
    """Semi-honest additive sharing sum. The cheater changes its partial sum:
    by a fixed error, or (rushing) to force a chosen target output."""
    n = len(inputs)
    shares = [share(x, n, p, rng) for x in inputs]
    partials = [sum(shares[i][j] for i in range(n)) % p for j in range(n)]
    if cheat is not None:
        c = cheat.party
        others = sum(partials[j] for j in range(n) if j != c)
        partials[c] = _cheat_share(partials[c], others, sum(partials), cheat, p)
    return sum(partials) % p


def plain_sum_split_view(inputs: Sequence[int], p: int, rng: random.Random, party: int,
                         errors: Sequence[int]) -> list[int]:
    """Without a broadcast channel, the cheater sends partial + errors[k] to
    party k. Returns the output of each party; honest parties may disagree."""
    n = len(inputs)
    shares = [share(x, n, p, rng) for x in inputs]
    partials = [sum(shares[i][j] for i in range(n)) % p for j in range(n)]
    outs = []
    for k in range(n):
        seen = list(partials)
        seen[party] = (seen[party] + errors[k]) % p
        outs.append(sum(seen) % p)
    return outs


def commit(value: int, rng: random.Random) -> tuple[bytes, bytes]:
    """A hash commitment: (commitment, opening). Hiding and binding only in the
    random oracle model; a local copy for this demo."""
    nonce = rng.getrandbits(256).to_bytes(32, "big")
    c = hashlib.sha256(b"commit" + nonce + value.to_bytes(32, "big")).digest()
    return c, nonce


def check_opening(c: bytes, value: int, nonce: bytes) -> bool:
    return hashlib.sha256(b"commit" + nonce + value.to_bytes(32, "big")).digest() == c


@dataclass
class Preprocessing:
    alpha: int
    alpha_shares: list[int]
    masks: list[int]                 # r_i, known to party i
    mask_shares: list[list[int]]     # mask_shares[i][j]: party j's share of r_i
    mask_mac_shares: list[list[int]]  # party j's share of alpha * r_i


def dealer(n: int, p: int, rng: random.Random) -> Preprocessing:
    """The trusted dealer that stands in for the offline phase."""
    alpha = rng.randrange(p)
    masks = [rng.randrange(p) for _ in range(n)]
    return Preprocessing(
        alpha,
        share(alpha, n, p, rng),
        masks,
        [share(r, n, p, rng) for r in masks],
        [share(alpha * r % p, n, p, rng) for r in masks],
    )


def mac_sum(
    inputs: Sequence[int], p: int, rng: random.Random, cheat: Optional[Cheat] = None,
    use_commitments: bool = True,
) -> Optional[int]:
    """Sum with authenticated shares. Returns the sum, or None on abort.

    Cost: one broadcast round for the inputs, one for the opened shares, and
    two for the commit-then-open MAC check; O(n) field operations per party.
    """
    n = len(inputs)
    pre = dealer(n, p, rng)
    # Input phase: party i broadcasts eps_i = x_i - r_i.
    eps = [(inputs[i] - pre.masks[i]) % p for i in range(n)]
    # Local computation of <y> = sum_i (<r_i> + eps_i).
    y_share = [0] * n
    m_share = [0] * n
    for j in range(n):
        y = sum(pre.mask_shares[i][j] for i in range(n))
        if j == 0:
            y += sum(eps)  # one party adds the public constants
        y_share[j] = y % p
        m_share[j] = (sum(pre.mask_mac_shares[i][j] for i in range(n))
                      + pre.alpha_shares[j] * sum(eps)) % p
    # Opening: everyone broadcasts its share of y.
    opened = list(y_share)
    if cheat is not None:
        c = cheat.party
        others = sum(opened[j] for j in range(n) if j != c)
        opened[c] = _cheat_share(opened[c], others, sum(opened), cheat, p)
    y_open = sum(opened) % p
    # MAC check.
    sigma = [(m_share[j] - pre.alpha_shares[j] * y_open) % p for j in range(n)]
    if cheat is not None:
        c = cheat.party
        if cheat.rushing and not use_commitments:
            sigma[c] = (-sum(sigma[j] for j in range(n) if j != c)) % p
        else:
            sigma[c] = (sigma[c] + cheat.mac_shift) % p
    if use_commitments:
        coms = [commit(s, rng) for s in sigma]   # all commit first ...
        for (cm, nonce), s in zip(coms, sigma):  # ... then all open
            if not check_opening(cm, s, nonce):
                return None
    if sum(sigma) % p != 0:
        return None
    return y_open
