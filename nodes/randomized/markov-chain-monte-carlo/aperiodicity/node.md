---
tag: MW76GP
kind: definition
slug: aperiodicity
name: Aperiodicity
aliases:
- aperiodic Markov chain
area: randomized/markov-chain-monte-carlo
level: core
summary: A state has period d, the gcd of the times at which the chain can return to it. A chain is aperiodic when each period is 1. With irreducibility it makes some power of P positive in each entry.
prereqs: [markov-chain, irreducibility, gcd-of-two-integers]
see_also: [irreducibility, ergodicity, stationary-distribution, mixing-time, perron-frobenius-theorem, bipartite-graph, transition-matrix, ergodic-theorem]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 1.3, Irreducibility and Aperiodicity (Lemma 1.6, Proposition 1.7, the lazy version of a chain); Exercise 1.6 (chains with period b); Lemma 1.30 (Schur)
  - book: isbn:9780521633963
    title: J. R. Norris, Markov Chains, Cambridge University Press, 1997
    locator: Section 1.8, Convergence to equilibrium (aperiodicity and Lemma 1.8.2)
  - book: isbn:9780821807491
    title: Charles M. Grinstead and J. Laurie Snell, Introduction to Probability, second revised edition, American Mathematical Society, 1997
    locator: Section 11.3, Ergodic Markov Chains (regular chains)
---

The period of a state $x$ of a [Markov chain](/markov-chain/) is the greatest common divisor of the times $t \ge 1$ at which a chain that starts at $x$ can be back at $x$. The chain is aperiodic when each state has period 1. Periodicity is what stops the law of an [irreducible](/irreducibility/) chain from converging: the walk on a 4-cycle is at an even vertex at even times only. An irreducible aperiodic chain is called [ergodic](/ergodicity/) on these pages, and for it some power $P^r$ has all entries positive.

## Definition

Let $P$ be a transition matrix on a finite set $\mathcal X$. For a state $x$, let
$$
\mathcal T(x) = \{t \ge 1 : P^t(x, x) > 0\},
$$
the set of possible return times. The *period* of $x$ is $\gcd \mathcal T(x)$ (undefined, or $\infty$ by convention, if $\mathcal T(x)$ is empty). The chain is *aperiodic* if each state has period 1, and *periodic* with period $d \ge 2$ if it is irreducible and its common period is $d$.

The set $\mathcal T(x)$ is closed under addition, because $P^{s+t}(x, x) \ge P^s(x, x)P^t(x, x)$. Like [irreducibility](/irreducibility/), the period depends only on which entries of $P$ are positive, that is, on the directed graph $G(P)$: $\mathcal T(x)$ is the set of the lengths of the closed walks through $x$.

### Facts and proofs

**Lemma 1 (the period is a class property; LPW Lemma 1.6).** If $P$ is irreducible, all states have the same period.

*Proof.* Take states $x, y$, and times $r, \ell$ with $P^r(x, y) > 0$ and $P^\ell(y, x) > 0$. Then $r + \ell \in \mathcal T(x)$. For each $t \in \mathcal T(y)$, the walk $x \to y \to y \to x$ gives $r + t + \ell \in \mathcal T(x)$. So $g = \gcd\mathcal T(x)$ divides both $r + \ell$ and $r + t + \ell$, hence it divides $t$. So $g$ divides $\gcd\mathcal T(y)$. By symmetry the two periods divide each other and are equal. $\square$

**Lemma 2 (numerical semigroups; LPW Lemma 1.30).** Let $S$ be a set of positive integers that is closed under addition and has $\gcd S = 1$. Then $S$ contains each integer $n \ge n_0$ for some $n_0$.

*Proof.* The gcd of $S$ is already the gcd of a finite subset $\{s_1, \ldots, s_k\}$: the gcd of $\{s_1, \ldots, s_j\}$ can only go down as $j$ grows, and a positive integer can go down only finitely often. By Bézout's identity (see [GCD of two integers](/gcd-of-two-integers/)), $1 = \sum_i a_i s_i$ with integers $a_i$. Let $p = \sum_{a_i > 0} a_i s_i$ and $m = \sum_{a_i < 0} (-a_i)s_i$, so $p - m = 1$, $p \in S$, and $m \in S$ or $m = 0$. If $m = 0$, then $1 \in S$ and $S$ is all positive integers. If not, take $n \ge m^2$ and write $n = qm + r$ with $0 \le r < m$. Then $q \ge m > r$, and
$$
n = qm + r(p - m) = (q - r)m + rp,
$$
a sum of $q - r \ge 0$ copies of $m$ and $r \ge 0$ copies of $p$, not both zero. So $n \in S$, and $n_0 = m^2$ works. $\square$

**Proposition 3 (LPW Proposition 1.7).** Let $P$ be irreducible. Then $P$ is aperiodic if and only if there is an $r$ with $P^r(x, y) > 0$ for all $x, y$. Such a matrix is called *primitive*, or *regular* (Grinstead and Snell).

*Proof.* Assume $P$ is irreducible and aperiodic. By Lemma 2, each $x$ has a $t(x)$ with $t \in \mathcal T(x)$ for all $t \ge t(x)$. For each pair $x, y$ choose $r(x, y)$ with $P^{r(x, y)}(x, y) > 0$. For $t \ge t(x) + r(x, y)$, $P^t(x, y) \ge P^{t - r(x, y)}(x, x)P^{r(x, y)}(x, y) > 0$. So $r = \max_{x, y}(t(x) + r(x, y))$ works. Conversely, if $P^r > 0$ in each entry, then $P^{r+1} = P\,P^r$ is also positive in each entry, because each row of $P$ has a positive entry. So $r, r + 1 \in \mathcal T(x)$ and the period of $x$ is 1. $\square$

Proposition 3 is the step that the convergence theorem uses: with $\delta = \min_{x, y}P^r(x, y) > 0$, two copies of the chain meet within $r$ steps with probability at least $\delta$. See [ergodicity](/ergodicity/).

**Sufficient conditions.** An irreducible chain with $P(x, x) > 0$ for one state $x$ is aperiodic, because $1 \in \mathcal T(x)$. An irreducible chain with two closed walks through one state, of coprime lengths, is aperiodic.

**The lazy chain.** For any $P$, the lazy chain $P_L = \tfrac12(I + P)$ has $P_L(x, x) \ge 1/2$, so it is aperiodic when it is irreducible. It has the same stationary distributions as $P$, and it is about twice as slow. Its eigenvalues lie in $[0, 1]$ when $P$ is reversible, which is why the theory of [mixing time](/mixing-time/) often studies lazy chains.

**The structure of a periodic chain.** If $P$ is irreducible with period $d \ge 2$, the states split into $d$ classes $C_0, \ldots, C_{d-1}$, and each step goes from $C_i$ to $C_{i+1 \bmod d}$ (LPW Exercise 1.6). The chain $P^d$ restricted to one class is irreducible and aperiodic. By the [Perron-Frobenius theorem](/perron-frobenius-theorem/), the eigenvalues of modulus 1 of an irreducible $P$ with period $d$ are exactly the $d$-th roots of unity.

## Examples and non-examples

**Random walk on a graph.** The simple random walk on a connected graph is aperiodic if and only if the graph is not [bipartite](/bipartite-graph/). If the graph is bipartite, each closed walk has even length, so the period is 2. If it has an odd cycle, a state $x$ has a closed walk of odd length (go to the cycle, around it, and back) and one of length 2 (to a neighbor and back), so its period is 1.

**Cycles.** The simple random walk on the cycle with $n$ vertices has period 2 when $n$ is even and is aperiodic when $n$ is odd. The rotation $i \mapsto i + 1 \bmod n$ with probability 1 has period $n$.

**The hypercube.** The walk that flips a uniform coordinate of a string in $\{0, 1\}^n$ has period 2: the number of ones changes parity at each step. The lazy walk is aperiodic.

**The Land of Oz.** $P(R, R) = 1/2 > 0$ and the chain is irreducible, so it is aperiodic. Its square $P^2$ already has all entries positive (see [transition matrix](/transition-matrix/)).

**A biased 3-cycle.** On $\{0, 1, 2\}$ let $P(i, i + 1) = 2/3$ and $P(i, i - 1) = 1/3$, mod 3. A return can take 2 steps (forward and back) or 3 steps (around), and $\gcd(2, 3) = 1$, so the chain is aperiodic although no state has a self-loop.

**Aperiodic but not irreducible.** On $\{1, 2, 3\}$ with 1 and 3 absorbing and 2 moving to each with probability $1/2$, each period that is defined is 1 (state 2 has no return, so $\mathcal T(2)$ is empty). The law of $X_t$ converges, but its limit depends on the start. Aperiodicity without irreducibility does not give a unique limit.

**Periodic chains still have useful averages.** The walk on two states that always switches has period 2. Its law does not converge, but the fraction of time in each state tends to $1/2$ by the [ergodic theorem](/ergodic-theorem/), which does not need aperiodicity. Estimates of $\mathbb E_\pi f$ by time averages are valid for periodic chains; convergence of the law of one $X_t$ is not.

## Related definitions

- [Irreducibility](/irreducibility/): each state reaches each other state. Aperiodicity adds a condition on the times of the returns.
- [Ergodicity](/ergodicity/): irreducible and aperiodic, the condition of the convergence theorem $P^t(x, \cdot) \to \pi$.
- [Mixing time](/mixing-time/): the rate of that convergence. For a periodic chain $d(t)$ does not tend to 0, so $t_{mix}(\varepsilon)$ is infinite for small $\varepsilon$.
- [Stationary distribution](/stationary-distribution/): exists for periodic chains as well; it is the limit of the Cesàro averages $\frac1T\sum_{t < T}\mu P^t$.
- [Perron-Frobenius theorem](/perron-frobenius-theorem/): the spectral form of the period.

## References
