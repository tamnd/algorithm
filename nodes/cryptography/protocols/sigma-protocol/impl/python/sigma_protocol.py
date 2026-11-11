# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sigma-protocol/. The authors are listed in prov/T1TB5Q.jsonl.
"""A generic interface for sigma protocols, with four instances.

Each protocol has the moves of a sigma protocol:

    commit(stmt, w, coins)        -> a          prover's first message
    respond(stmt, w, coins, c)    -> z          prover's answer to challenge c
    verify(stmt, a, c, z)         -> bool
    extract(stmt, a, c1, z1, c2, z2) -> w       special soundness (c1 != c2)
    simulate(stmt, c, coins)      -> (a, z)     special honest-verifier ZK

The random coins of the prover and of the simulator are passed in as tuples
of elements of Z_q, so that the tests can enumerate them. Challenges are in
Z_q. `ncoins` and `nsim` give how many coins each side needs.

Instances:
  Schnorr        y = g^x
  ChaumPedersen  u = g^x and v = h^x (equal discrete logarithms)
  And(A, B)      a witness for both statements, one shared challenge
  Or(A, B)       a witness for one of two statements (Cramer, Damgard and
                 Schoenmakers): the prover simulates the branch it cannot
                 prove and splits the challenge as c = c0 + c1 mod q

For study only. The code is not constant time and the groups are toys. Use
a reviewed library such as libsodium or a FIPS 140 validated module for real
group operations.
"""

import random


class Group:
    """Subgroup of prime order q of Z_p^*, with p = 2q + 1, and two generators."""

    def __init__(self, p, g, h):
        self.p, self.q, self.g, self.h = p, (p - 1) // 2, g, h
        for e in (g, h):
            assert e != 1 and pow(e, self.q, p) == 1

    def exp(self, b, e):
        return pow(b, e % self.q, self.p)

    def mul(self, *xs):
        r = 1
        for x in xs:
            r = r * x % self.p
        return r


TINY = Group(23, 4, 9)        # q = 11: small enough to enumerate everything
TOY = Group(2039, 4, 9)       # q = 1019


class Schnorr:
    """Knowledge of x with y = g^x."""

    ncoins, nsim = 1, 1

    def __init__(self, G):
        self.G = G

    def commit(self, y, x, coins):
        return self.G.exp(self.G.g, coins[0])                     # @line L1

    def respond(self, y, x, coins, c):
        return (coins[0] + c * x) % self.G.q                       # @line L3

    def verify(self, y, a, c, z):
        G = self.G
        return G.exp(G.g, z) == G.mul(a, G.exp(y, c))              # @line L4

    def extract(self, y, a, c1, z1, c2, z2):
        return (z1 - z2) * pow(c1 - c2, -1, self.G.q) % self.G.q   # @line L5

    def simulate(self, y, c, coins):
        G = self.G
        z = coins[0] % G.q                                         # @line L6
        return G.mul(G.exp(G.g, z), G.exp(y, -c)), z               # @line L7


class ChaumPedersen:
    """Knowledge of x with u = g^x and v = h^x, so (g, h, u, v) is a DH tuple."""

    ncoins, nsim = 1, 1

    def __init__(self, G):
        self.G = G

    def commit(self, stmt, x, coins):
        G = self.G
        return G.exp(G.g, coins[0]), G.exp(G.h, coins[0])

    def respond(self, stmt, x, coins, c):
        return (coins[0] + c * x) % self.G.q

    def verify(self, stmt, a, c, z):
        G = self.G
        u, v = stmt
        return (
            G.exp(G.g, z) == G.mul(a[0], G.exp(u, c))
            and G.exp(G.h, z) == G.mul(a[1], G.exp(v, c))
        )

    def extract(self, stmt, a, c1, z1, c2, z2):
        return (z1 - z2) * pow(c1 - c2, -1, self.G.q) % self.G.q

    def simulate(self, stmt, c, coins):
        G = self.G
        u, v = stmt
        z = coins[0] % G.q
        return (G.mul(G.exp(G.g, z), G.exp(u, -c)), G.mul(G.exp(G.h, z), G.exp(v, -c))), z


class And:
    """Witnesses for both statements; one challenge for both branches."""

    def __init__(self, A, B):
        self.A, self.B = A, B
        self.ncoins = A.ncoins + B.ncoins
        self.nsim = A.nsim + B.nsim

    def _split(self, coins, n):
        return coins[:n], coins[n:]

    def commit(self, stmt, w, coins):
        ca, cb = self._split(coins, self.A.ncoins)
        return self.A.commit(stmt[0], w[0], ca), self.B.commit(stmt[1], w[1], cb)

    def respond(self, stmt, w, coins, c):
        ca, cb = self._split(coins, self.A.ncoins)
        return self.A.respond(stmt[0], w[0], ca, c), self.B.respond(stmt[1], w[1], cb, c)

    def verify(self, stmt, a, c, z):
        return self.A.verify(stmt[0], a[0], c, z[0]) and self.B.verify(stmt[1], a[1], c, z[1])

    def extract(self, stmt, a, c1, z1, c2, z2):
        return (
            self.A.extract(stmt[0], a[0], c1, z1[0], c2, z2[0]),
            self.B.extract(stmt[1], a[1], c1, z1[1], c2, z2[1]),
        )

    def simulate(self, stmt, c, coins):
        ca, cb = self._split(coins, self.A.nsim)
        a0, z0 = self.A.simulate(stmt[0], c, ca)
        a1, z1 = self.B.simulate(stmt[1], c, cb)
        return (a0, a1), (z0, z1)


class Or:
    """A witness for one of two statements. The witness is (i, w_i).

    Prover coins: (coins for its own branch, the other challenge c_other,
    simulator coins for the other branch). The answer is (c0, z0, z1); the
    verifier sets c1 = c - c0 mod q and checks both transcripts.
    """

    def __init__(self, A, B, q):
        self.br, self.q = (A, B), q
        self.ncoins = max(A.ncoins, B.ncoins) + 1 + max(A.nsim, B.nsim)
        self.nsim = 1 + A.nsim + B.nsim

    def _parts(self, i, coins):
        own = self.br[i].ncoins
        other_sim = self.br[1 - i].nsim
        k = max(self.br[0].ncoins, self.br[1].ncoins)
        return coins[:own], coins[k] % self.q, coins[k + 1:k + 1 + other_sim]

    def commit(self, stmt, w, coins):
        i, wi = w
        own, c_other, sim_coins = self._parts(i, coins)
        a = [None, None]
        a[i] = self.br[i].commit(stmt[i], wi, own)
        a[1 - i], _ = self.br[1 - i].simulate(stmt[1 - i], c_other, sim_coins)
        return tuple(a)

    def respond(self, stmt, w, coins, c):
        i, wi = w
        own, c_other, sim_coins = self._parts(i, coins)
        ci = (c - c_other) % self.q
        z = [None, None]
        z[i] = self.br[i].respond(stmt[i], wi, own, ci)
        _, z[1 - i] = self.br[1 - i].simulate(stmt[1 - i], c_other, sim_coins)
        c0 = ci if i == 0 else c_other
        return c0, z[0], z[1]

    def verify(self, stmt, a, c, z):
        c0, z0, z1 = z
        c1 = (c - c0) % self.q
        return self.br[0].verify(stmt[0], a[0], c0, z0) and self.br[1].verify(stmt[1], a[1], c1, z1)

    def extract(self, stmt, a, c, z, c2, z2):
        """Return (j, w_j) for a branch j whose sub-challenges differ."""
        sub = ((z[0], (c - z[0]) % self.q), (z2[0], (c2 - z2[0]) % self.q))
        for j in (0, 1):
            if sub[0][j] != sub[1][j]:
                w = self.br[j].extract(stmt[j], a[j], sub[0][j], z[1 + j], sub[1][j], z2[1 + j])
                return j, w
        raise ValueError("challenges are equal")

    def simulate(self, stmt, c, coins):
        c0 = coins[0] % self.q
        c1 = (c - c0) % self.q
        n0 = self.br[0].nsim
        a0, z0 = self.br[0].simulate(stmt[0], c0, coins[1:1 + n0])
        a1, z1 = self.br[1].simulate(stmt[1], c1, coins[1 + n0:])
        return (a0, a1), (c0, z0, z1)


def random_coins(n, q, rng):
    return tuple(rng.randrange(q) for _ in range(n))


def run(proto, stmt, w, q, rng):
    """One honest run: return the transcript (a, c, z)."""
    coins = random_coins(proto.ncoins, q, rng)
    a = proto.commit(stmt, w, coins)
    c = rng.randrange(q)                                           # @line L2
    return a, c, proto.respond(stmt, w, coins, c)
