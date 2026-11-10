---
tag: 2533Z3
kind: concept
slug: mixing-time
name: Mixing time
aliases:
- convergence time
area: randomized/markov-chain-monte-carlo
level: core
summary: The mixing time t_mix(ε) is the first time at which the law of a chain is within total variation distance ε of π from every start. It sets how long an MCMC run must be.
prereqs: [total-variation-distance, ergodicity, stationary-distribution]
see_also: [rapid-mixing, spectral-gap, conductance, coupling-method, path-coupling, cheeger-inequality, burn-in, strong-uniform-time]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 4.4, Standardizing Distance from Stationarity (Lemma 4.10, Lemma 4.11); Section 4.5, Mixing Time (equations (4.30) to (4.34)); Section 7.2, Bottleneck Ratio (Theorem 7.4); Section 12.2, Relaxation Time (Theorem 12.4, Theorem 12.5); Section 18.2 (Theorem 18.3, cutoff for the hypercube)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 12, Coupling of Markov Chains (mixing time and coupling)
  - book: isbn:9783764369460
    title: Mark Jerrum, Counting, Sampling and Integrating, Algorithms and Complexity, Birkhäuser, 2003
    locator: Chapters 4 and 5 (coupling and canonical paths for mixing time bounds)
---

The mixing time of an [ergodic](/ergodicity/) [Markov chain](/markov-chain/) is the number of steps after which the law of the chain is close to its [stationary distribution](/stationary-distribution/) $\pi$, whatever the starting state. Closeness is measured in [total variation distance](/total-variation-distance/), and the standard threshold is $1/4$. The mixing time is the cost of one approximate sample in Markov chain Monte Carlo, so most of the theory of these chains is about bounding it. A chain whose mixing time is polynomial in the logarithm of the number of states is called [rapidly mixing](/rapid-mixing/).

## In plain words

Shuffle a deck of cards a few times and the order still depends on where you started. Shuffle it enough and the order looks random, whatever the start. The mixing time is the number of shuffles that "enough" means. It is a property of the shuffle, not of a particular run. It asks for closeness from the worst start, so a short mixing time is a guarantee. Once the chain is close to random, more steps keep it close, and each further block of the same length halves the remaining error. So the time to get very close is only a small factor larger than the time to get somewhat close. Chains with a bottleneck, a narrow passage between two large regions, mix slowly, because the chain needs a long time to pass through it.

## The idea

### Definitions

Let $P$ be an ergodic transition matrix on a finite set $\mathcal X$ with stationary distribution $\pi$. The notation of this group of pages is
$$
d(t) = \max_{x \in \mathcal X}\|P^t(x, \cdot) - \pi\|_{TV}, \qquad t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}, \qquad t_{mix} = t_{mix}(1/4).
$$
Also let $\bar d(t) = \max_{x, y}\|P^t(x, \cdot) - P^t(y, \cdot)\|_{TV}$. By LPW Lemma 4.10 (proved on [total variation distance](/total-variation-distance/)), $d(t) \le \bar d(t) \le 2d(t)$. The maximum over single states is the same as the maximum over all starting distributions, by convexity.

### Three basic facts

**Fact 1: $d(t)$ is non-increasing.** Write $P^{t+1}(x, \cdot) - \pi = \sum_z P(x, z)\big(P^t(z, \cdot) - \pi\big)$, using $\pi = \sum_z P(x, z)\pi$. By the triangle inequality, $\|P^{t+1}(x, \cdot) - \pi\|_{TV} \le \sum_z P(x, z)\|P^t(z, \cdot) - \pi\|_{TV} \le d(t)$. $\square$

So $t_{mix}(\varepsilon)$ is well defined: once $d(t) \le \varepsilon$, it stays there.

**Fact 2: $\bar d$ is submultiplicative (LPW Lemma 4.11).** For all $s, t \ge 0$, $\bar d(s + t) \le \bar d(s)\,\bar d(t)$.

*Proof.* Fix $x, y$. By Proposition 3 of [total variation distance](/total-variation-distance/), there is a coupling $(X_s, Y_s)$ of $P^s(x, \cdot)$ and $P^s(y, \cdot)$ with $\Pr[X_s \ne Y_s] = \|P^s(x, \cdot) - P^s(y, \cdot)\|_{TV} \le \bar d(s)$. Then $P^{s+t}(x, \cdot) = \mathbb E\,P^t(X_s, \cdot)$ and $P^{s+t}(y, \cdot) = \mathbb E\,P^t(Y_s, \cdot)$, so
$$
\|P^{s+t}(x, \cdot) - P^{s+t}(y, \cdot)\|_{TV} \le \mathbb E\,\|P^t(X_s, \cdot) - P^t(Y_s, \cdot)\|_{TV} \le \bar d(t)\Pr[X_s \ne Y_s] \le \bar d(t)\,\bar d(s),
$$
because the middle term is 0 when $X_s = Y_s$. Take the maximum over $x, y$. $\square$

**Fact 3: the threshold costs a logarithm (LPW (4.34)).** For $0 < \varepsilon < 1$,
$$
t_{mix}(\varepsilon) \le \lceil \log_2(1/\varepsilon) \rceil\, t_{mix}.
$$
*Proof.* Let $\ell \ge 1$. By Fact 2 and Lemma 4.10, $d(\ell\,t_{mix}) \le \bar d(\ell\,t_{mix}) \le \bar d(t_{mix})^\ell \le (2d(t_{mix}))^\ell \le 2^{-\ell}$. Take $\ell = \lceil\log_2(1/\varepsilon)\rceil$. $\square$

The same proof shows that any threshold below $1/2$ would do: if $d(t) \le \varepsilon_0 < 1/2$, then $d(\ell t) \le (2\varepsilon_0)^\ell$. The value $1/4$ is a convention. A threshold of $1/2$ or more does not work, because the periodic walk on a 4-cycle has $d(t) = 1/2$ for all $t \ge 1$ and never mixes.

### Upper bounds

| Method | What it bounds | Page |
|---|---|---|
| Coupling of two copies | $d(t) \le \max_{x, y}\Pr_{x, y}[\tau_{couple} > t]$ | [coupling method](/coupling-method/), [coupling inequality](/coupling-inequality/) |
| Path coupling | contraction on neighboring pairs only | [path coupling](/path-coupling/) |
| Spectral gap, reversible chains | $t_{mix}(\varepsilon) \le \lceil t_{rel}(\tfrac12\log\frac1{\pi_{min}} + \log\frac1{2\varepsilon})\rceil$ (LPW Theorem 12.4) | [spectral gap](/spectral-gap/) |
| Conductance | $\gamma \ge \Phi_*^2/2$, then the spectral bound | [conductance](/conductance/), [Cheeger inequality](/cheeger-inequality/) |
| Canonical paths | $\gamma \ge 1/B$, then the spectral bound | [canonical paths](/canonical-paths/) |
| Strong stationary times | $d(t) \le \Pr[\tau > t]$ | [strong uniform time](/strong-uniform-time/) |

Here $t_{rel} = 1/\gamma_*$ is the relaxation time, $\gamma_* = 1 - \max\{|\lambda| : \lambda \ne 1\}$, and $\pi_{min} = \min_x\pi(x)$.

### Lower bounds

- **Spectral (LPW Theorem 12.5).** For a reversible chain, $t_{mix}(\varepsilon) \ge (t_{rel} - 1)\log\frac{1}{2\varepsilon}$.
- **Bottleneck (LPW Theorem 7.4).** $t_{mix} \ge 1/(4\Phi_*)$, where $\Phi_*$ is the [conductance](/conductance/).
- **Diameter.** Suppose $P(x, y) > 0$ exactly when $P(y, x) > 0$, and let $L$ be the largest graph distance between two states in the graph of $P$. If $2t < L$, two states at distance $L$ have no common state within $t$ steps, so $P^t(x, \cdot)$ and $P^t(y, \cdot)$ have disjoint supports, $\bar d(t) = 1$ and $d(t) \ge 1/2$. So $t_{mix} \ge L/2$.

### Cutoff

For many families of chains, $d(t)$ stays near 1 and then drops to near 0 in a window that is short compared with $t_{mix}$. This is the *cutoff phenomenon*. The lazy walk on the hypercube $\{0, 1\}^n$ has its cutoff at $\tfrac12 n\log n$, with a window of size $O(n)$ (LPW Theorem 18.3). For such chains the choice of $\varepsilon$ barely matters.

### What the mixing time is not

The mixing time is a property of the matrix $P$, with a worst case over starts. The [burn-in](/burn-in/) of a simulation is a choice made for one run. Output statistics such as [effective sample size](/effective-sample-size/) or the [Gelman-Rubin diagnostic](/gelman-rubin-diagnostic/) can show that a run has not mixed, but they cannot prove that it has: a chain stuck on one side of a bottleneck can look stationary for a long time.

## Examples

The following values were computed exactly, with rational arithmetic, from the matrices. "Lazy" means $\tfrac12(I + P)$ for the simple random walk. The columns are the spectral upper bound of LPW Theorem 12.4 with $\varepsilon = 1/4$, the spectral lower bound $(t_{rel} - 1)\log 2$, and the bottleneck bound $1/(4\Phi_*)$.

| Chain | States | $t_{mix}$ | $t_{mix}(1/100)$ | $t_{rel}$ | upper (12.4) | lower (12.5) | $1/(4\Phi_*)$ |
|---|---|---|---|---|---|---|---|
| Land of Oz | 3 | 1 | 4 | 4/3 | 2 | 0.23 | 0.5 |
| lazy path, 3 vertices | 3 | 1 | 6 | 2 | 3 | 0.69 | 0.5 |
| lazy hypercube, $n = 3$ | 8 | 3 | 11 | 3 | 6 | 1.39 | 1.5 |
| lazy hypercube, $n = 4$ | 16 | 5 | 16 | 4 | 9 | 2.08 | 2 |
| lazy cycle, 8 vertices | 8 | 6 | 26 | 6.83 | 12 | 4.04 | 2 |
| two triangles joined by an edge, lazy | 6 | 8 | 38 | 9.77 | 17 | 6.08 | 3.5 |
| two copies of $K_4$ joined by an edge, lazy | 8 | 14 | 69 | 17.64 | 32 | 11.53 | 6.5 |

Each true value lies between the bounds. Fact 3 gives $t_{mix}(1/100) \le 7\,t_{mix}$, and each row satisfies it.

**The Land of Oz in detail.** From rain the distance is $\tfrac35\cdot4^{-t}$, and the worst start is "nice", with $d(t) = \tfrac45\cdot4^{-t}$. So $d(1) = 1/5 \le 1/4$ and $t_{mix} = 1$, while $d(3) = 1/80 > 1/100 \ge d(4) = 1/320$ gives $t_{mix}(1/100) = 4$.

**The lazy path on 3 vertices.** Here $d(t) = 3/4, 1/4, 1/8, 1/16, \ldots$ for $t = 0, 1, 2, 3, \ldots$, so $d(t) = 2^{-t-1}$ for $t \ge 1$. The values $t_{mix}(2^{-k})$ for $k = 1, \ldots, 7$ are $1, 1, 2, 3, 4, 5, 6$, below the bound $k\,t_{mix} = k$ of Fact 3.

**The lazy hypercube.** For $n = 3$, $d(t) = \tfrac12(2/3)^{t-1}$ for $t \ge 1$, so $d(2) = 1/3$, $d(3) = 2/9$ and $t_{mix} = 3$. The coupling on the page [coupling method](/coupling-method/) gives $t_{mix} \le \lceil n\log(4n)\rceil = 8$. For general $n$, $t_{mix}$ grows like $\tfrac12 n\log n$: the walk is rapidly mixing on its $2^n$ states.

**Bottlenecks.** The two cliques joined by one edge mix slowly for their size. The edge is the only way from one half to the other, so the chain must wait for it. With two copies of $K_k$, $\Phi_*$ is of order $1/k^2$ and $t_{mix}$ grows at least like $k^2$, against a constant for one $K_{2k}$.

## Where it is used

- **Markov chain Monte Carlo.** The cost of one approximate sample from $\pi$ is about $t_{mix}(\varepsilon)$ steps. See [sampling from a stationary distribution](/sampling-from-stationary-distribution/).
- **Approximate counting.** An [FPRAS](/fpras/) for a [counting problem](/counting-problem/) built by [self-reducibility](/self-reducibility/) needs many samples, each taken after a mixing time. A polynomial bound on $t_{mix}$ is the core of such results, for example for [graph colorings](/counting-graph-colorings/) and [perfect matchings](/counting-perfect-matchings/).
- **Card shuffling.** How many riffle shuffles mix a deck is a mixing time question; see [card shuffling](/card-shuffling/).
- **Exact sampling.** The running time of [coupling from the past](/coupling-from-the-past/) is tied to the mixing time of the chain it uses.
- **Spectral graph theory.** For a random walk on a graph, the mixing time is tied to the spectral gap and to [graph conductance](/graph-conductance/).

## References
