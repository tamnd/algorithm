---
tag: G0ENPS
kind: algorithm
slug: glauber-dynamics
name: Glauber dynamics
aliases:
- heat-bath dynamics
- single-site dynamics
area: randomized/markov-chain-monte-carlo
level: advanced
summary: A Markov chain for a distribution on configurations of sites. Pick a uniform site and redraw its value from π given the other sites. For proper q-colorings it mixes in O(n log n) steps when q > 2Δ.
solves: [sampling-from-stationary-distribution]
model: word-ram
complexity:
  vars: {t: "the number of steps", q: "the number of colors", d: "the maximum degree of the graph"}
  time: {worst: Θ(t·(d + q)), average: Θ(t·(d + q)), best: Θ(t·(d + q))}
  space: {extra: Θ(q)}
properties: {in_place: true, online: false, deterministic: false, recursive: false}
history:
  year: 1963
  people: [Roy J. Glauber]
  note: Glauber introduced the dynamics in 1963 as a model of how the Ising model evolves in time. Jerrum used it in 1995 to sample colorings of graphs with q > 2Δ.
prereqs: [markov-chain, detailed-balance, mixing-time]
see_also: [gibbs-sampling, metropolis-hastings, path-coupling, ising-model, hard-core-model, counting-graph-colorings, coupling-from-the-past, swendsen-wang]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 3.3, Glauber Dynamics; Theorem 5.8; Theorem 14.10 (equation (14.17))
  - paper: doi:10.1063/1.1703954
    title: Roy J. Glauber, Time-dependent statistics of the Ising model, Journal of Mathematical Physics 4(2), 1963
    locator: the single-spin dynamics of the Ising model
  - paper: doi:10.1002/rsa.3240070205
    title: Mark Jerrum, A very simple algorithm for estimating the number of k-colorings of a low-degree graph, Random Structures and Algorithms 7(2), 1995
    locator: pages 157 to 165 (rapid mixing for q > 2Δ)
  - paper: doi:10.1109/SFCS.1997.646111
    title: Russ Bubley and Martin Dyer, Path coupling, a technique for proving rapid mixing in Markov chains, Proceedings of the 38th Annual Symposium on Foundations of Computer Science (FOCS), 1997
    locator: pages 223 to 231
  - paper: doi:10.1063/1.533196
    title: Eric Vigoda, Improved bounds for sampling colorings, Journal of Mathematical Physics 41(3), 2000
    locator: pages 1555 to 1569 (q > 11Δ/6, through a chain that recolors clusters)
---

Glauber dynamics is the [Markov chain](/markov-chain/) that samples a distribution $\pi$ on configurations $x \in S^V$, an assignment of a value from a set $S$ to each site of a set $V$, by changing one site at a time. Each step picks a site $v$ uniformly at random and redraws $x(v)$ from the law of $\pi$ given the values at all other sites. The chain is reversible with respect to $\pi$, so $\pi$ is stationary. For uniform proper $q$-colorings of a graph with $n$ vertices and maximum degree $\Delta$ it mixes in $O(n\log n)$ steps when $q > 2\Delta$ (Jerrum 1995).

## In plain words

You want a random proper coloring of a map, with every coloring equally likely. Start from any proper coloring. At each step, choose one region at random. Look at the colors of its neighbors, and give the region a color chosen at random from the colors that no neighbor uses. Its old color is one of the choices, so the region may keep it. Repeat many times. Each step is fair to every coloring that agrees with the current one away from the chosen region, so the uniform choice over all proper colorings is never disturbed. When there are enough colors, a few rounds over every region make the coloring close to a fair random pick. The same rule works for other models: resample one site from its correct conditional law, given its neighbors.

## The problem

Given a graph $G = (V, E)$ with $n$ vertices, maximum degree $\Delta$ and $q \ge \Delta + 1$ colors, output a random proper $q$-coloring whose law is within $\varepsilon$ of uniform in [total variation](/total-variation-distance/). This is an instance of [sampling from a stationary distribution](/sampling-from-stationary-distribution/). The general form samples any $\pi$ on $S^V$ for which the conditional law at one site can be computed, such as the [Ising model](/ising-model/) or the [hard-core model](/hard-core-model/).

The notation is $d(t) = \max_x\|P^t(x, \cdot) - \pi\|_{TV}$, $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$ and $t_{mix} = t_{mix}(1/4)$.

## The algorithm

For a coloring $x$ and a vertex $v$, let $A_v(x) = \{1, \ldots, q\} \setminus \{x(w) : w \sim v\}$ be the colors that no neighbor of $v$ uses.

```pseudo id=main
GLAUBER-COLORING(G, q, x, t)                ▷ x is a q-coloring, changed in place
L1  repeat t times
L2      v ← a uniform vertex of G
L3      A ← the colors in 1..q that no neighbor of v uses
L4      x(v) ← a uniform element of A
```

The general heat-bath step replaces lines L3 and L4: draw $x(v) = s$ with probability $\pi(x^{v \to s}) / \sum_{s'}\pi(x^{v \to s'})$, where $x^{v \to s}$ is $x$ with the value at $v$ set to $s$. For uniform proper colorings this conditional law is uniform on $A_v(x)$. Only ratios of $\pi$ are needed, so the normalizing constant is never computed.

## Example

Take the path $0 - 1 - 2$ and $q = 5$ colors $\{0, \ldots, 4\}$, starting from $x = (0, 1, 0)$.

| step | $v$ | neighbor colors | $A$ | choice | new $x$ |
|---|---|---|---|---|---|
| 1 | 1 | $\{0\}$ | $(1, 2, 3, 4)$ | the element with index 2 | $(0, 3, 0)$ |
| 2 | 0 | $\{3\}$ | $(0, 1, 2, 4)$ | the element with index 3 | $(4, 3, 0)$ |

This path has $5 \cdot 4 \cdot 4 = 80$ proper colorings. Exact fractions give the mixing times in the table, against the path coupling bound $\lceil n(q - \Delta)/(q - 2\Delta)\cdot\ln(4n)\rceil$ for $\varepsilon = 1/4$.

| graph | $q$ | $\Delta$ | proper colorings | exact $t_{mix}$ | bound |
|---|---|---|---|---|---|
| one edge | 3 | 1 | 6 | 4 | 9 |
| path with 3 vertices | 5 | 2 | 80 | 6 | 23 |
| triangle | 5 | 2 | 60 | 7 | 23 |

The bound is a factor 2 to 4 above the truth on these graphs, and it holds at every $t$, not only at $1/4$.

## Correctness

The full proofs are below. In outline:

1. **The step is well defined.** $|A_v(x)| \ge q - \deg(v) \ge q - \Delta \ge 1$.
2. **Uniform is stationary.** If $x \ne y$ are proper and differ only at $v$, then $A_v(x) = A_v(y)$, because $A_v$ depends only on the colors off $v$. So $P(x, y) = 1/(n|A_v(x)|) = P(y, x)$. The matrix is symmetric, and the uniform law satisfies [detailed balance](/detailed-balance/). For a general $\pi$, $\pi(x)P(x, y) = \pi(x)\pi(y)/(n Z_v)$, where $Z_v$ is the sum of $\pi$ over the values at $v$, which is symmetric in $x$ and $y$.
3. **Ergodic when $q \ge \Delta + 2$.** Any proper coloring can be changed into any other by single recolorings that stay proper, so the chain is [irreducible](/irreducibility/). It is [aperiodic](/aperiodicity/) because $x(v) \in A_v(x)$ gives $P(x, x) > 0$. With $q = \Delta + 1$ it can fail: on a triangle with 3 colors every vertex has exactly one allowed color, and no coloring ever changes.
4. **Rapid mixing when $q > 2\Delta$.** Couple two copies that differ at one vertex $w$ by choosing the same $v$ and an optimal coupling of the two uniform laws on $A_v$. The disagreement disappears with probability $1/n$, and it spreads only when $v$ is a neighbor of $w$, with probability at most $1/(q - \Delta)$. So the expected distance becomes at most $1 - (q - 2\Delta)/(n(q - \Delta))$. [Path coupling](/path-coupling/) then gives
$$
d(t) \le n\Big(1 - \frac{q - 2\Delta}{n(q - \Delta)}\Big)^t, \qquad t_{mix}(\varepsilon) \le \Big\lceil\frac{q - \Delta}{q - 2\Delta}\,n\,\ln\frac{n}{\varepsilon}\Big\rceil.
$$

## Complexity

Line L3 reads the colors of at most $d$ neighbors and builds a list of at most $q$ colors, so one step takes $\Theta(d + q)$ time with a list of size $\Theta(q)$, and $t$ steps take $\Theta(t(d + q))$. A table of how many neighbors of each vertex use each color reduces the cost to $O(d)$ per step after an $O(nq)$ setup, and choosing a uniform allowed color by rejection costs $O(q/(q - d))$ expected draws.

For $q > 2\Delta$ the bound above gives a sample within $\varepsilon$ of uniform in $O(n\log(n/\varepsilon))$ steps, for a total of $O(n\log(n/\varepsilon)(\Delta + q))$ time. No chain that changes one site per step can do much better: until every vertex has been chosen at least once, which takes about $n\ln n$ steps by the [coupon collector](/coupon-collector-problem/) argument, the vertices not yet chosen still have their starting colors.

## Properties

- **Reversible.** Each step is a heat-bath move, so $P$ satisfies detailed balance with respect to $\pi$.
- **Local.** A step reads only the neighbors of one site, and only ratios of $\pi$ are used.
- **Lazy in effect.** The current value is always a possible outcome, so $P(x, x) > 0$ and the chain is aperiodic.
- **Fixes improper starts.** A recolored vertex has no conflict with its neighbors, and no step creates a conflict. So once every vertex has been chosen, the coloring is proper.
- **Monotone for attractive models.** For the ferromagnetic Ising model, heat-bath updates driven by a shared uniform number preserve the order of configurations, which [coupling from the past](/coupling-from-the-past/) needs.

## Variants and improvements

- **[Gibbs sampling](/gibbs-sampling/).** The same heat-bath move under its name in statistics, often with a fixed scan order over the coordinates and on continuous spaces. A systematic scan leaves $\pi$ stationary but is not reversible.
- **Metropolis Glauber dynamics.** Propose a uniform color at $v$ and accept it if no neighbor uses it. Coupling shows fast mixing for $q > 3\Delta$ (LPW Theorem 5.8); the heat-bath form needs only $q > 2\Delta$ for the path coupling bound. See [Metropolis-Hastings](/metropolis-hastings/).
- **Cluster and flip dynamics.** Vigoda (2000) recolored maximal two-colored clusters, the Kempe components, and proved $O(n\log n)$ mixing of that chain for $q > 11\Delta/6$. A comparison argument then gives polynomial mixing for Glauber dynamics. Chen, Delcourt, Moitra, Perarnau and Postle later lowered the constant $11/6$ slightly.
- **Block dynamics.** Resample a block of sites at once from its conditional law.
- **Continuous time.** Each site updates at the times of its own rate 1 Poisson clock. The two forms mix within constant factors of each other, after a time change by a factor of $n$.
- **Swendsen-Wang.** For the Ising and Potts models, the [Swendsen-Wang](/swendsen-wang/) chain updates whole clusters and can mix fast where single-site dynamics is slow.

## When to use it

Use Glauber dynamics when $\pi$ is a Gibbs distribution on a graph with local interactions, so that the conditional law at a site is cheap to compute. It is the standard chain for colorings, independent sets and spin systems, and the chain behind many FPRAS results through the reduction from counting to sampling; see [counting graph colorings](/counting-graph-colorings/). Prefer a cluster or tempering method, such as [parallel tempering](/parallel-tempering/), at low temperature, where single-site moves face a bottleneck. Prefer [coupling from the past](/coupling-from-the-past/) when exact samples are needed and the model is monotone.

## Pitfalls

- **Too few colors.** With $q = \Delta + 1$ the chain can be frozen, as on the triangle with 3 colors. With $q \le \Delta$ an allowed set can be empty, and the implementation raises an error.
- **Proper starts only for the stated law.** From an improper start the chain still becomes proper, but early states are not proper colorings.
- **Bounds are sufficient, not necessary.** $q > 2\Delta$ is where the simple proof works. Fast mixing is conjectured for $q \ge \Delta + 2$ and is not proved in general.
- **Counting steps, not rounds.** The bound counts single-site steps. One round over all sites is $n$ steps.
- **Phase transitions.** For the Ising model below the critical temperature, or the hard-core model above the uniqueness threshold, the chain can need exponential time.
- **Floating point.** The general heat-bath step draws from probabilities that may be tiny. Work with ratios or logarithms to avoid underflow.

## Implementations

## History

Glauber introduced the dynamics in 1963 as a stochastic model of the time evolution of the Ising model. In computer science it became a tool for sampling: Jerrum (1995) proved that the heat-bath chain on colorings mixes in $O(n\log n)$ steps when $q > 2\Delta$, and Salas and Sokal found the same condition independently in physics. Bubley and Dyer (1997) introduced path coupling, which made the proof short. Vigoda (2000) went below $2\Delta$ to $11\Delta/6$ with a cluster chain.

## References
