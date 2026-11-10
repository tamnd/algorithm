---
tag: MF0D9Q
kind: concept
slug: conductance
name: Conductance
aliases:
- Cheeger constant of a chain
- bottleneck ratio
area: randomized/markov-chain-monte-carlo
level: advanced
summary: The conductance Φ* of a chain is the least ratio, over sets S with π(S) ≤ 1/2, of the stationary flow out of S to π(S). A small Φ* is a bottleneck and forces t_mix ≥ 1/(4Φ*).
prereqs: [stationary-distribution, detailed-balance, mixing-time]
see_also: [cheeger-inequality, spectral-gap, canonical-paths, mixing-time, graph-conductance, conductance-rumor-spreading-bound, rapid-mixing, laplacian-matrix]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 7.2, Bottleneck Ratio (equation (7.7), Theorem 7.4); Section 13.2, The Dirichlet Form and the Bottleneck Ratio (Theorem 13.10, Examples 13.11 and 13.12); Notes to Chapter 13
  - paper: doi:10.1016/0890-5401(89)90067-9
    title: Alistair Sinclair and Mark Jerrum, Approximate counting, uniform generation and rapidly mixing Markov chains, Information and Computation 82(1), 1989
    locator: pages 93 to 133 (conductance and rapid mixing)
  - book: isbn:9783764369460
    title: Mark Jerrum, Counting, Sampling and Integrating, Algorithms and Complexity, Birkhäuser, 2003
    locator: Chapter 5, Canonical paths and applications
---

The conductance of a [Markov chain](/markov-chain/) measures its worst bottleneck. For a set of states $S$ it compares the probability flow out of $S$ at stationarity with the stationary mass of $S$, and $\Phi_*$ is the smallest such ratio over sets with at most half the mass. If $\Phi_*$ is small, some set is hard to leave, and the chain needs at least $1/(4\Phi_*)$ steps to mix. For reversible chains the [Cheeger inequality](/cheeger-inequality/) also gives the converse: $\Phi_*$ bounds the [spectral gap](/spectral-gap/) from below, and so the [mixing time](/mixing-time/) from above.

## In plain words

Think of the states as rooms and the chain as a crowd that moves between them. At equilibrium, some amount of the crowd walks out of each group of rooms at each step. If a large group of rooms has only a narrow door to the rest of the building, very few people pass through it per step. A crowd that starts inside that group stays inside for a long time, and the building is far from equilibrium until enough people get out. Conductance finds the worst such group: the one with the least traffic out compared with its size. Low conductance proves that the chain is slow. High conductance means that no narrow door exists, and for reversible chains that is enough to prove that the chain is fast, though the guarantee is weaker.

## The idea

### Definitions

Let $P$ be irreducible on a finite set $\mathcal X$ with stationary distribution $\pi$. The *edge measure* is $Q(x, y) = \pi(x)P(x, y)$, and $Q(A, B) = \sum_{x \in A, y \in B}Q(x, y)$, the probability that the stationary chain steps from $A$ to $B$. For $S$ with $\pi(S) > 0$,
$$
\Phi(S) = \frac{Q(S, S^c)}{\pi(S)} = \Pr_\pi[X_1 \notin S \mid X_0 \in S], \qquad \Phi_* = \min_{S : 0 < \pi(S) \le 1/2}\Phi(S).
$$
LPW calls $\Phi_*$ the *bottleneck ratio*, equation (7.7). The condition $\pi(S) \le 1/2$ matters: for $S = \mathcal X$ the ratio is 0. Since $\pi P = \pi$, $Q(S, S^c) = Q(S^c, S)$ for every chain, reversible or not: the flow out of $S$ equals the flow into $S$.

For the simple random walk on a graph, $\pi(x) = \deg(x)/2m$ and $Q(x, y) = 1/2m$ on each edge, so $\Phi(S) = |E(S, S^c)|/\operatorname{vol}(S)$, where $\operatorname{vol}(S)$ is the sum of the degrees in $S$. This is the [graph conductance](/graph-conductance/). The lazy walk has half this value.

The mixing notation is $d(t) = \max_x\|P^t(x, \cdot) - \pi\|_{TV}$, $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$ and $t_{mix} = t_{mix}(1/4)$.

### The bottleneck bound

**Theorem (LPW Theorem 7.4).** $t_{mix} \ge \dfrac{1}{4\Phi_*}$.

*Proof.* Take $S$ with $\pi(S) \le 1/2$ and $\Phi(S) = \Phi_*$, and let $\pi_S = \pi(\cdot \mid S)$, the stationary distribution restricted to $S$ and renormalized.

1. *One step moves $\pi_S$ by exactly $\Phi(S)$.* For $y \in S$, $(\pi_SP)(y) = \sum_{x \in S}\pi(x)P(x, y)/\pi(S) \le \pi(y)/\pi(S) = \pi_S(y)$. For $y \notin S$, $(\pi_SP)(y) \ge 0 = \pi_S(y)$. So the positive part of $\pi_SP - \pi_S$ lives on $S^c$, and $\|\pi_SP - \pi_S\|_{TV} = (\pi_SP)(S^c) = Q(S, S^c)/\pi(S) = \Phi(S)$.
2. *$t$ steps move it by at most $t\Phi(S)$.* By the triangle inequality and the contraction $\|\mu P - \nu P\|_{TV} \le \|\mu - \nu\|_{TV}$, $\|\pi_SP^t - \pi_S\|_{TV} \le \sum_{s < t}\|\pi_SP^{s+1} - \pi_SP^s\|_{TV} \le t\Phi(S)$.
3. *$\pi_S$ is far from $\pi$.* $\pi_S(S^c) = 0$ and $\pi(S^c) \ge 1/2$, so $\|\pi_S - \pi\|_{TV} \ge 1/2$.

So $\|\pi_SP^t - \pi\|_{TV} \ge \tfrac12 - t\Phi(S)$. The left side is at most $d(t)$, because $\pi_S$ is a mixture of point masses. At $t = t_{mix}$, $\tfrac14 \ge \tfrac12 - t_{mix}\Phi_*$. $\square$

The proof uses neither reversibility nor aperiodicity.

### The upper bound through the spectral gap

For a reversible chain, the [Cheeger inequality](/cheeger-inequality/) (LPW Theorem 13.10) says
$$
\frac{\Phi_*^2}{2} \le \gamma \le 2\Phi_*,
$$
where $\gamma = 1 - \lambda_2$. For a lazy reversible chain $\gamma$ is also the absolute gap, and LPW Theorem 12.4 on the page [spectral gap](/spectral-gap/) gives
$$
\frac1{4\Phi_*} \le t_{mix} \le \Big\lceil\frac{2}{\Phi_*^2}\Big(\frac12\log\frac1{\pi_{min}} + \log 2\Big)\Big\rceil.
$$
So for lazy reversible chains, conductance decides the mixing time up to squaring and a factor $\log(1/\pi_{min})$. This is the route that Jerrum and Sinclair used to prove rapid mixing of chains for [approximate counting](/approximate-counting/), for example for [perfect matchings](/counting-perfect-matchings/) in dense bipartite graphs, where $\Phi_*$ was bounded below by [canonical paths](/canonical-paths/).

### Computing it

The definition is a minimum over exponentially many sets. The brute force tries all $2^{|\mathcal X|}$ subsets, which is how the values below were found. For large chains, upper bounds on $\Phi_*$ come from exhibiting one bad set, and lower bounds need an argument for every set, such as canonical paths.

## Examples

Exact values, found by trying all subsets; "lazy" means $\tfrac12(I + P)$ for the simple random walk.

| Chain | $\Phi_*$ | a worst set $S$ | $1/(4\Phi_*)$ | $t_{mix}$ |
|---|---|---|---|---|
| Land of Oz | $1/2$ | {rain} | 0.5 | 1 |
| lazy path, 3 vertices | $1/2$ | an end vertex | 0.5 | 1 |
| lazy hypercube, $n = 3$ | $1/6$ | $\{x : x_1 = 0\}$ | 1.5 | 3 |
| lazy hypercube, $n = 4$ | $1/8$ | $\{x : x_1 = 0\}$ | 2 | 5 |
| lazy cycle, 8 vertices | $1/8$ | an arc of 4 vertices | 2 | 6 |
| two triangles joined by an edge, lazy | $1/14$ | one triangle | 3.5 | 8 |
| two copies of $K_4$ joined by an edge, lazy | $1/26$ | one $K_4$ | 6.5 | 14 |

**The Land of Oz.** With $S = \{R\}$, $\pi(R) = 2/5$ and $Q(R, \{N, S\}) = \tfrac25\cdot\tfrac12 = \tfrac15$, so $\Phi(S) = 1/2$. The other sets with $\pi(S) \le 1/2$ are $\{N\}$, with $\Phi = 1$, and $\{S\}$, with $\Phi = 1/2$.

**The hypercube.** For the lazy walk on $\{0, 1\}^n$ and $S = \{x : x_1 = 0\}$, a step leaves $S$ only if it picks coordinate 1 and draws a 1, with probability $\frac1n\cdot\frac12$. So $\Phi(S) = 1/(2n)$, and this set is the worst (LPW Example 13.11).

**Two cliques joined by an edge.** Let $S$ be one triangle, with degrees 2, 2 and 3, so $\pi(S) = 7/14 = 1/2$. The only way out is the bridge, taken from its end with probability $\tfrac12\cdot\tfrac13$, so $Q(S, S^c) = \tfrac3{14}\cdot\tfrac16 = \tfrac1{28}$ and $\Phi(S) = 1/14$. With two copies of $K_k$, $\Phi_*$ is of order $1/k^2$. One clique $K_{2k}$ has $\Phi_*$ near $1/4$ for the lazy walk.

**Physical bottlenecks.** Take the [Ising model](/ising-model/) on an $n \times n$ grid at low temperature. The set of configurations with more $+$ spins than $-$ spins has stationary mass about $1/2$, and the flow out of it passes through configurations with a long interface between the two signs, which have tiny weight. So $\Phi_*$ is exponentially small in $n$, and single-site dynamics needs exponential time to mix. The [hard-core model](/hard-core-model/) on a grid at high fugacity behaves in the same way, with the two checkerboard patterns in place of the two signs.

## Where it is used

- **Lower bounds on mixing times.** One bad set gives $t_{mix} \ge 1/(4\Phi(S))$. This is the standard way to prove that a chain is not [rapidly mixing](/rapid-mixing/).
- **Upper bounds on mixing times.** Through the [Cheeger inequality](/cheeger-inequality/), a lower bound on $\Phi_*$ gives one on the spectral gap. Jerrum and Sinclair used this for the chain on the matchings of a graph.
- **Graphs.** [Graph conductance](/graph-conductance/) is the same quantity for the random walk on a graph; it governs expansion, graph partitioning and the eigenvalues of the [Laplacian matrix](/laplacian-matrix/).
- **Rumor spreading.** The time of push-pull rumor spreading is bounded in terms of the graph conductance; see [conductance bound for rumor spreading](/conductance-rumor-spreading-bound/).

## References
