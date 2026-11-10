---
tag: Y4BCHJ
kind: theorem
slug: coupling-inequality
name: Coupling inequality
area: randomized/markov-chain-monte-carlo
level: core
summary: For any coupling (X, Y) of μ and ν, the TV distance is at most P(X ≠ Y), with equality for the best coupling. So d(t) is at most the chance that coupled copies have not met by time t.
prereqs: [total-variation-distance, markov-chain, probability-distribution]
see_also: [coupling-method, path-coupling, total-variation-distance, mixing-time, ergodicity, coupling-from-the-past, strong-uniform-time, markov-inequality]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 4.2 (Proposition 4.7, Remark 4.8); Section 4.4 (Lemma 4.10); Sections 5.1 and 5.2 (Theorem 5.4, Corollary 5.5); Section 5.3.1 (the hypercube); Notes to Chapter 5
  - book: isbn:9780521633963
    title: J. R. Norris, Markov Chains, Cambridge University Press, 1997
    locator: Section 1.8, Convergence to equilibrium (the coupling proof)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 12, Coupling of Markov Chains
---

The coupling inequality bounds the [total variation distance](/total-variation-distance/) between two distributions by the probability that two random variables, one with each law and built on a common probability space, differ. For [Markov chains](/markov-chain/) it says that the distance from stationarity at time $t$ is at most the probability that two coupled copies of the chain, started anywhere, have not met by time $t$. It turns a question about distributions into a question about one random time, and it is the basis of the [coupling method](/coupling-method/) and of [path coupling](/path-coupling/).

## Statement

Let $\mu$ and $\nu$ be probability distributions on a finite set $\mathcal X$. A *coupling* of $\mu$ and $\nu$ is a pair of random variables $(X, Y)$ on one probability space with $X \sim \mu$ and $Y \sim \nu$. The total variation distance is $\|\mu - \nu\|_{TV} = \max_{A \subseteq \mathcal X}|\mu(A) - \nu(A)|$.

**Theorem 1 (the coupling inequality; LPW Proposition 4.7).**

1. For every coupling $(X, Y)$ of $\mu$ and $\nu$, $\|\mu - \nu\|_{TV} \le \Pr[X \ne Y]$.
2. Some coupling attains equality, so $\|\mu - \nu\|_{TV} = \min\{\Pr[X \ne Y] : (X, Y) \text{ a coupling of } \mu, \nu\}$.

Let $P$ be an irreducible transition matrix on $\mathcal X$ with stationary distribution $\pi$. A coupling of two $P$-chains is a process $(X_t, Y_t)_{t \ge 0}$ in which each of $(X_t)$ and $(Y_t)$ is a Markov chain with matrix $P$. Assume that the copies stay together once they meet:
$$
X_s = Y_s \implies X_t = Y_t \text{ for all } t \ge s, \tag{$\ast$}
$$
and let $\tau_{couple} = \min\{t : X_s = Y_s \text{ for all } s \ge t\}$. Write $\Pr_{x, y}$ when $X_0 = x$ and $Y_0 = y$. The mixing notation is $d(t) = \max_x\|P^t(x, \cdot) - \pi\|_{TV}$, $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$ and $t_{mix} = t_{mix}(1/4)$.

**Theorem 2 (LPW Theorem 5.4 and Corollary 5.5).**

1. $\|P^t(x, \cdot) - P^t(y, \cdot)\|_{TV} \le \Pr_{x, y}[\tau_{couple} > t]$.
2. If such a coupling exists for each pair $x, y$, then $d(t) \le \max_{x, y}\Pr_{x, y}[\tau_{couple} > t]$.
3. Consequently $t_{mix} \le 4\max_{x, y}\mathbb E_{x, y}[\tau_{couple}]$.

Neither theorem needs reversibility, and Theorem 2 needs no aperiodicity: for a periodic chain no coupling can meet with probability 1, and the bound is then simply weak.

## In plain words

Two piles of sand have different shapes, and you want to know how different they are. One way is to move grains from the first pile to make the second, keeping as many grains in place as possible. The share of grains that must move is the distance between the piles. Any plan for moving grains gives an upper bound on that distance, and the best plan gives the exact value. For a random process, the same idea says: run two copies side by side from different starts, letting them share their random choices so that they tend to meet. Once they have met, they move together. By that time, the starting point no longer matters. So the chance that they have not yet met bounds how far the process still is from equilibrium.

## Proof

**Theorem 1, part 1.** Fix a coupling $(X, Y)$ and a set $A$. Then
$$
\mu(A) - \nu(A) = \Pr[X \in A] - \Pr[Y \in A] \le \Pr[X \in A, Y \notin A] \le \Pr[X \ne Y].
$$
The first inequality drops the event $\{X \notin A, Y \in A\}$ from the second term: $\Pr[X \in A] - \Pr[Y \in A] = \Pr[X \in A, Y \notin A] - \Pr[X \notin A, Y \in A]$. The same holds with $\mu$ and $\nu$ exchanged. Taking the maximum over $A$ gives the claim. $\square$

**Theorem 1, part 2 (the maximal coupling).** Let $m(z) = \min(\mu(z), \nu(z))$ and $p = \sum_zm(z)$. By the identity $\|\mu - \nu\|_{TV} = \sum_z(\mu(z) - \nu(z))^+$ (proved on [total variation distance](/total-variation-distance/)), $1 - p = \sum_z(\mu(z) - m(z)) = \|\mu - \nu\|_{TV}$. If $p = 1$ then $\mu = \nu$ and $X = Y \sim \mu$ works. If $p = 0$ any coupling works. Otherwise flip a coin $C$ with $\Pr[C = 1] = p$.

- If $C = 1$, draw $Z$ from $m/p$ and set $X = Y = Z$.
- If $C = 0$, draw $X$ from $(\mu - \nu)^+/(1 - p)$ and $Y$ from $(\nu - \mu)^+/(1 - p)$, independently.

The two measures in the second case have total mass $1 - p$ each, so they are probability distributions after the division. Then $\Pr[X = z] = m(z) + (\mu(z) - \nu(z))^+ = \mu(z)$, and in the same way $Y \sim \nu$. The measures $(\mu - \nu)^+$ and $(\nu - \mu)^+$ have disjoint supports, so $X \ne Y$ exactly when $C = 0$, and $\Pr[X \ne Y] = 1 - p = \|\mu - \nu\|_{TV}$. $\square$

**Theorem 2, part 1.** Under $\Pr_{x, y}$, $X_t \sim P^t(x, \cdot)$ and $Y_t \sim P^t(y, \cdot)$, so $(X_t, Y_t)$ is a coupling of these two laws. Theorem 1 gives $\|P^t(x, \cdot) - P^t(y, \cdot)\|_{TV} \le \Pr_{x, y}[X_t \ne Y_t]$. By $(\ast)$, $X_t \ne Y_t$ holds exactly when $\tau_{couple} > t$. $\square$

**Theorem 2, part 2.** Since $\pi = \pi P^t = \sum_y\pi(y)P^t(y, \cdot)$, for each $x$ and each set $A$,
$$
|P^t(x, A) - \pi(A)| = \Big|\sum_y\pi(y)\big(P^t(x, A) - P^t(y, A)\big)\Big| \le \sum_y\pi(y)\|P^t(x, \cdot) - P^t(y, \cdot)\|_{TV}.
$$
So $d(t) \le \bar d(t) := \max_{x, y}\|P^t(x, \cdot) - P^t(y, \cdot)\|_{TV}$ (this is half of LPW Lemma 4.10), and part 1 bounds each term. $\square$

**Theorem 2, part 3.** By [Markov's inequality](/markov-inequality/), $\Pr_{x, y}[\tau_{couple} > t] \le \mathbb E_{x, y}[\tau_{couple}]/t$. For $t = 4\max_{x, y}\mathbb E_{x, y}[\tau_{couple}]$ this is at most $1/4$, so $d(t) \le 1/4$. $\square$

## Consequences

**Convergence to equilibrium.** Let $P$ be irreducible and aperiodic on a finite set. Run two copies independently until they meet, then together. The independent product chain is irreducible, because aperiodicity gives an $r$ with $P^r(u, v) > 0$ for all $u, v$. So from any pair of states the copies meet within $r$ steps with probability at least some $\delta > 0$, and $\Pr_{x, y}[\tau_{couple} > kr] \le (1 - \delta)^k$. By Theorem 2, $d(t) \to 0$ geometrically fast. This is Doeblin's proof of the convergence theorem; see [ergodicity](/ergodicity/).

**Mixing bounds by coupling.** Each coupling gives an upper bound on $t_{mix}$. For the lazy walk on $\{0, 1\}^n$, pick the same coordinate in both copies and refresh it with the same fair bit (LPW Section 5.3.1). The copies have met once every coordinate where they differ has been picked, so $\Pr_{x, y}[\tau_{couple} > t] \le n(1 - 1/n)^t \le ne^{-t/n}$ by the [union bound](/union-bound/), and $t_{mix}(\varepsilon) \le \lceil n\log(n/\varepsilon)\rceil$. The [coupling method](/coupling-method/) collects such constructions, and [path coupling](/path-coupling/) builds them from couplings of neighboring states only.

**Exact sampling.** A coupling in which copies from all starting states meet gives more than a bound. [Coupling from the past](/coupling-from-the-past/) uses such a grand coupling, run backward in time, to produce an exact sample from $\pi$.

## Tightness

**For two distributions, the inequality is sharp.** Part 2 of Theorem 1 says the best coupling attains it. A bad coupling can be far off. For $\mu = (\tfrac12, \tfrac12, 0)$ and $\nu = (0, \tfrac12, \tfrac12)$ on $\{1, 2, 3\}$, $\|\mu - \nu\|_{TV} = 1/2$. The independent coupling has $\Pr[X \ne Y] = 1 - \tfrac12\cdot\tfrac12 = 3/4$, while the maximal coupling puts $X = Y = 2$ with probability $1/2$ and $(X, Y) = (1, 3)$ otherwise, with $\Pr[X \ne Y] = 1/2$.

**For chains, Markovian couplings can lose a constant or more.** The table compares, for the lazy walk on $\{0, 1\}^3$ with the coordinate coupling above, the exact $d(t)$ and $\bar d(t)$ with the coupling bound for the worst pair, two opposite corners. There $\tau_{couple}$ is the time to pick all 3 coordinates, so $\Pr[\tau_{couple} > t] = 3(2/3)^t - 3(1/3)^t$ exactly. The values were computed with exact fractions.

| $t$ | $d(t)$ | $\bar d(t)$ | $\Pr[\tau_{couple} > t]$ | union bound $3(2/3)^t$ |
|---|---|---|---|---|
| 1 | 0.500 | 1.000 | 1.000 | 2.000 |
| 3 | 0.222 | 0.444 | 0.778 | 0.889 |
| 5 | 0.099 | 0.198 | 0.383 | 0.395 |
| 6 | 0.066 | 0.132 | 0.259 | 0.263 |
| 7 | 0.044 | 0.088 | 0.174 | 0.176 |

Here $d(t) = \tfrac34(2/3)^t$ and $\bar d(t) = 2d(t)$ exactly. The exact $t_{mix}$ is 3, while the coupling gives $t_{mix} \le 7$ and the union bound gives $t_{mix} \le 8$. For each $t$ the coupling bound is about twice $\bar d(t)$.

**A maximal coupling of chains exists.** Griffeath (1974/75) proved that for any two starting states there is a coupling, in general not Markovian, with $\Pr_{x, y}[\tau_{couple} > t] = \|P^t(x, \cdot) - P^t(y, \cdot)\|_{TV}$ for all $t$ at the same time. So Theorem 2, part 1, is sharp over all couplings. Its proof does not give a usable construction, and in practice one uses Markovian couplings, which can be much weaker than the best one. LPW points to Hayes and Vigoda for a useful coupling that is not Markovian.

**The step from $\bar d$ to $d$ costs at most a factor 2**, because $\bar d(t) \le 2d(t)$ by the triangle inequality (LPW Lemma 4.10).

## History

The use of coupling in probability is usually traced back to Doeblin (1938), who used two independent copies of a chain to prove convergence to equilibrium. Couplings of Markov chains were studied as such by Pitman (1974) and Griffeath (1974/75), who constructed the maximal coupling. Aldous (1983) made the coupling inequality a standard tool for bounding mixing times of random walks on finite groups, and since the 1990s it has been the main way to prove that Markov chains for sampling combinatorial objects mix rapidly.

## References
