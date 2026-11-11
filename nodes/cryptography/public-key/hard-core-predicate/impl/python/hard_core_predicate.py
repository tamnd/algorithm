# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hard-core-predicate/. The authors are listed in prov/1M8WNB.jsonl.
"""The Goldreich-Levin predicate and its two decoding algorithms.

The predicate is the inner product modulo 2, b_r(x) = <x, r>. The theorem of
Goldreich and Levin (1989) says that for every one way function f, the pair
(f(x), r) hides b_r(x): an algorithm that predicts the digit can be turned
into an algorithm that finds x.

This file holds the two directions of that reduction as code.

* recover_from_three_quarter_predictor: the easy version. A predictor that is
  right for more than 3/4 of the strings r gives every digit of x by the pair
  of queries r and r xor e_i, with majority voting.
* recover_from_half_plus_predictor: the full version. A predictor that is
  right for a 1/2 + epsilon fraction gives a short list of candidates, using
  2^l guesses for l seed queries and the 2^l - 1 pairwise independent strings
  that the seeds span.

The predictor here is a simulation: it knows the secret and answers with a
fixed, reproducible error pattern of the chosen density. It stands for the
adversary that the theorem assumes, so the code is the reduction and not an
attack on any real system.

For study only. The parameters are toy parameters, the code is not constant
time, and everything runs in one local process.
"""

import hashlib
from dataclasses import dataclass, field

# A toy one way function candidate: modular exponentiation in a small group.
# PRIME is prime, BASE generates the whole group, and the order 1030 is above
# 2^10, so the map is injective on the 10 digit inputs used below.
PRIME = 1031
BASE = 14
TOY_DIGITS = 10


def inner_product(x: int, r: int) -> int:
    """The Goldreich-Levin predicate b_r(x) = <x, r> mod 2, for x and r as integers."""
    return bin(x & r).count("1") & 1


def toy_one_way_function(x: int) -> int:
    """BASE^x mod PRIME, injective on 0 <= x < 2^TOY_DIGITS. Not one way at this size."""
    return pow(BASE, x, PRIME)


@dataclass
class ParityPredictor:
    """A simulated adversary that guesses <x, r> from f(x) and r.

    The oracle is a deterministic function of r: the set of strings on which
    it errs is fixed by the seed, and its density is 1 - accuracy. A
    deterministic oracle is the right model, because an oracle that flipped a
    fresh coin on each call could be corrected by asking the same question
    twice, and the theorem must not use that.
    """

    secret: int
    accuracy: float
    seed: bytes = b"hard-core-predicate"
    queries: int = field(default=0)

    def _errs_on(self, r: int) -> bool:
        digest = hashlib.sha256(self.seed + r.to_bytes(8, "big")).digest()
        return int.from_bytes(digest[:8], "big") >= self.accuracy * 2**64

    def __call__(self, r: int) -> int:
        """Return a guess of <secret, r>."""
        self.queries += 1
        return inner_product(self.secret, r) ^ int(self._errs_on(r))


def true_accuracy(predictor: ParityPredictor, digits: int) -> float:
    """The exact fraction of the 2^digits strings r on which the predictor is right."""
    right = sum(
        1
        for r in range(1 << digits)
        if predictor(r) == inner_product(predictor.secret, r)
    )
    predictor.queries -= 1 << digits  # the measurement is not part of the attack
    return right / (1 << digits)


def recover_from_three_quarter_predictor(
    predictor, digits: int, rnd, trials: int = 200
) -> int:
    """Recover x from a predictor that is right on more than 3/4 of the strings.

    For each digit i, the identity <x, r xor e_i> = <x, r> xor x_i turns two
    queries into one guess of x_i. Both queries are right with probability
    above 1/2 when the predictor errs on less than 1/4 of the strings, so the
    majority over `trials` independent r is right with high probability.

    Cost: 2 * digits * trials queries, and no use of f.
    """
    recovered = 0
    for index in range(digits):
        bit = 1 << index
        votes = 0
        for _ in range(trials):
            r = rnd.randrange(1 << digits)
            guess = predictor(r) ^ predictor(r ^ bit)
            votes += 1 if guess else -1
        if votes > 0:
            recovered |= bit
    return recovered


def recover_from_half_plus_predictor(
    predictor, digits: int, rnd, seeds: int = 8, verifier=None
) -> list:
    """Recover x from a predictor that is right on a 1/2 + epsilon fraction.

    The trick of Goldreich and Levin. Draw `seeds` strings r_1, ..., r_l and
    guess the l values <x, r_j>; one of the 2^l guesses is right. For a
    nonempty set S of seeds, the string r_S = xor of the r_j for j in S has
    <x, r_S> = xor of the guessed values, so the 2^l - 1 strings r_S come with
    known predicate values and no query. The pairs (r_S, r_S xor e_i) then
    give votes for x_i that are pairwise independent, and Chebyshev's
    inequality makes the majority right with constant probability.

    The predictor is asked only about the strings r_S xor e_i, and those
    answers do not depend on the guess, so they are cached and the loop over
    the 2^l guesses costs no queries.

    Cost: (2^l - 1) * digits queries and O(2^l * digits * 2^l) integer
    operations. Returns the candidates that `verifier` accepts, or all 2^l
    candidates when `verifier` is None.
    """
    seed_strings = [rnd.randrange(1, 1 << digits) for _ in range(seeds)]
    subsets = list(range(1, 1 << seeds))
    # r_S for every nonempty subset S of the seeds, and the cached answers.
    combined = []
    for mask in subsets:
        r = 0
        for position, string in enumerate(seed_strings):
            if mask >> position & 1:
                r ^= string
        combined.append(r)
    answers = [
        [predictor(r ^ (1 << index)) for index in range(digits)] for r in combined
    ]

    candidates = []
    for guess in range(1 << seeds):
        # The guessed value of <x, r_S> is the parity of the guessed digits in S.
        known = [bin(mask & guess).count("1") & 1 for mask in subsets]
        recovered = 0
        for index in range(digits):
            votes = 0
            for position in range(len(subsets)):
                votes += 1 if known[position] ^ answers[position][index] else -1
            if votes > 0:
                recovered |= 1 << index
        if verifier is None or verifier(recovered):
            candidates.append(recovered)
    return candidates


def blum_micali_digits(start: int, digits: int) -> list:
    """The pseudorandom digits of the Blum-Micali chain on the toy function.

    Each step applies f and outputs one hard core digit of the new state. With
    a real one way permutation and a hard core predicate this is a
    pseudorandom generator; with the toy group of this file it is a
    demonstration of the shape only.
    """
    state = start
    out = []
    for _ in range(digits):
        state = toy_one_way_function(state) % (1 << TOY_DIGITS)
        out.append(inner_product(state, (1 << TOY_DIGITS) - 1))
    return out
