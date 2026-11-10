---
tag: RB6W2D
kind: algorithm
slug: expander-walk-sampler
name: Expander walk sampler
aliases:
- expander random walk generator
- expander walk amplification
- random walk on an expander
area: randomized/derandomization
level: research
summary: Uses a random walk on an expander to produce many correlated samples, reducing error with few fresh random bits.
solves: [randomness-amplification]
model: word-ram
complexity:
  vars: {t: the number of walk vertices, d: the degree of the graph}
  time: {worst: Θ(t), average: Θ(t), best: Θ(t)}
  space: {extra: Θ(t)}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 1987
  people: [Miklós Ajtai, János Komlós, Endre Szemerédi]
  note: "Ajtai, Komlós and Szemerédi used walks on expanders to save random bits; Cohen and Wigderson and Impagliazzo and Zuckerman (1989) used them to reduce the error of RP and BPP algorithms."
prereqs: [spectral-gap, regular-graph, eigenvalue, rp]
see_also: [randomness-amplification, error-amplification, hitting-set-generator, disperser, chernoff-bound, pairwise-independence, expander-codes, mixing-time]
sources:
  - paper: doi:10.1145/28395.28410
    title: Miklós Ajtai, János Komlós and Endre Szemerédi, Deterministic simulation in LOGSPACE, STOC 1987
    locator: pages 132 to 140 (walks on expanders as a source of correlated random strings)
  - paper: doi:10.1109/sfcs.1989.63449
    title: Aviad Cohen and Avi Wigderson, Dispersers, deterministic amplification, and weak random sources, FOCS 1989
    locator: pages 14 to 19 (error reduction for RP and BPP with expander walks)
  - paper: doi:10.1109/sfcs.1989.63486
    title: Russell Impagliazzo and David Zuckerman, How to recycle random bits, FOCS 1989
    locator: pages 248 to 253 (expander walks to reuse random bits)
  - paper: doi:10.1137/S0097539794268765
    title: David Gillman, A Chernoff bound for random walks on expander graphs, SIAM Journal on Computing 27(4), 1998
    locator: pages 1203 to 1220 (the Chernoff bound for the average of a function along an expander walk)
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1-3), 2012
    locator: Chapter 4, Sections 4.1 (measures of expansion) and 4.2 (random walks on expanders, the hitting property and the Chernoff bound)
  - paper: doi:10.1016/0022-0000(81)90040-4
    title: Ofer Gabber and Zvi Galil, Explicit constructions of linear-sized superconcentrators, Journal of Computer and System Sciences 22(3), 1981
    locator: pages 407 to 420 (an explicit 8-regular expander family on Z_m x Z_m)
---

The expander walk sampler replaces $t$ independent random samples by the $t$ vertices of a random walk on an expander graph. The first vertex costs $\log_2 N$ random bits and each later step only $\log_2 d$, where $d$ is a constant degree, but the samples still behave almost like independent ones: the probability that all $t$ of them fall in a set of density $\mu$ is at most $\mu(\mu + \lambda(1 - \mu))^{t-1}$, where $\lambda < 1$ is the spectral expansion of the graph. Used on the random strings of an [RP](/rp/) algorithm with $m$ random bits, this reduces the error to $2^{-k}$ with $m + O(k)$ random bits, in place of $km$ for independent runs. The idea goes back to Ajtai, Komlós and Szemerédi (1987); Cohen and Wigderson and Impagliazzo and Zuckerman (1989) applied it to error reduction, and Gillman (1998) proved a [Chernoff bound](/chernoff-bound/) for the averages along the walk.

## In plain words

An algorithm uses a random string and is wrong for a few strings. Running it again with fresh strings makes errors rarer, but each run costs a whole new string.

Instead, arrange all possible strings as the points of a large, well-connected network, where each point has only a few links. Pick a random starting point, then move along a random link, again and again, and run the algorithm on each point that you visit. Each move costs only the few random bits that choose one of the links. The network is so well connected that a walk cannot stay long inside a small group of points: it leaves the group about as fast as fresh random points would. So the chance that every visited point is a bad one shrinks fast, almost as fast as with independent runs.

## The problem

Notation. $G$ is a $d$-regular undirected graph on $N$ vertices, with adjacency matrix $A$ and walk matrix $M = A/d$. The eigenvalues of $M$ are $1 = \lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_N \ge -1$, and the *spectral expansion* is $\lambda = \max(|\lambda_2|, |\lambda_N|)$. The [spectral gap](/spectral-gap/) is $1 - \lambda$. $B$ is a set of vertices with density $\mu = |B|/N$. $\Pr$ is over the random walk.

An [RP](/rp/) algorithm $\mathcal{A}$ uses $m$ random bits. On an input in the language it accepts for at least half of the $2^m$ random strings; on other inputs it never accepts. The task is to reduce the probability of a wrong reject to $2^{-k}$ with as few random bits as possible. The error is one-sided: a reject can be wrong, an accept is always right. Identify the random strings with the $N = 2^m$ vertices of $G$, and let $B$ be the set of strings on which $\mathcal{A}$ wrongly rejects, so $\mu \le 1/2$.

## The algorithm

```pseudo id=main
EXPANDER-WALK-AMPLIFY(A, w, G, t)     ▷ G is d-regular on N = 2^m vertices, with spectral expansion λ
L1  v_1 ← a uniform vertex of G        ▷ m random bits
L2  for i ← 2 to t do
L3      j ← a uniform number in {1, …, d}   ▷ log₂ d random bits
L4      v_i ← the j-th neighbour of v_{i−1}
L5  for i ← 1 to t do
L6      if A(w, v_i) accepts then return accept
L7  return reject
```

Lines L1 to L4 are the sampler: they output the $t$ vertices $v_1, \ldots, v_t$ of the walk. Lines L5 to L7 use the samples as random strings for $\mathcal{A}$. The graph must be *strongly explicit*: line L4 computes the $j$-th neighbour of a vertex in time polynomial in $m$, without writing down the graph.

## Example

The Petersen graph has $N = 10$, $d = 3$, and the eigenvalues $3, 1, -2$ of $A$, so $\lambda = 2/3$. Let $B$ be the outer 5-cycle, so $\mu = 1/2$. From an outer vertex, 2 of the 3 neighbours are outer, so the walk stays in $B$ for $t$ vertices with probability exactly $\frac{1}{2}(2/3)^{t-1}$. The hitting bound is $\frac{1}{2}(\frac{1}{2} + \frac{2}{3} \cdot \frac{1}{2})^{t-1} = \frac{1}{2}(5/6)^{t-1}$.

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| walk, exact | 1/2 | 1/3 | 2/9 | 4/27 | 8/81 | 16/243 |
| hitting bound | 1/2 | 5/12 | 25/72 | 125/432 | 625/2592 | 3125/15552 |
| independent samples | 1/2 | 1/4 | 1/8 | 1/16 | 1/32 | 1/64 |

The walk uses $\log_2 10 + (t - 1)\log_2 3$ random bits, about $11.2$ for $t = 6$, against $6 \log_2 10 \approx 19.9$ for 6 independent vertices. Over all 5-vertex sets, the outer cycle is the worst for $t = 4$, with $4/27$. For 4-vertex sets ($\mu = 2/5$), the worst value for $t = 4$ is $1/15$, against the bound $128/625$.

At scale: let $\mathcal{A}$ use $m = 100$ random bits, and ask for error $2^{-20}$. Twenty independent runs use 2000 random bits. Pairwise independent runs use 200 random bits but need about $2^{20}$ runs, since their error falls only like $1/t$. With a 16-regular graph on $2^{100}$ vertices with $\lambda \le 1/2$, the bound $\frac{1}{2}(3/4)^{t-1} \le 2^{-20}$ holds for $t = 47$, so the walk uses $100 + 46 \cdot 4 = 284$ random bits and 47 runs. See [randomness amplification](/randomness-amplification/) for the comparison.

## Correctness

The key fact is the **hitting property**: for every set $B$ of density $\mu$,

$$\Pr[v_1, \ldots, v_t \in B] \le \mu \big(\mu + \lambda(1 - \mu)\big)^{t-1}.$$

The proof writes the probability as $\mathbf{1}^\top (PMP)^{t-1} P \pi$, with $P$ the projection onto $B$ and $\pi$ the uniform distribution, and bounds the operator norm $\|PMP\| \le \mu + \lambda(1 - \mu)$ by splitting $M = (1 - \lambda)J + \lambda E$ with $J$ the uniform matrix and $\|E\| \le 1$. Then the algorithm never accepts a wrong input, since every accept is a witness of $\mathcal{A}$, and it rejects a right input only if all $t$ vertices are in $B$. With $\mu \le 1/2$ the error is at most $\frac{1}{2}\big(\frac{1 + \lambda}{2}\big)^{t-1}$, which is $2^{-k}$ for $t = 1 + \lceil (k - 1)/\log_2(2/(1 + \lambda)) \rceil = O(k)$ when $\lambda$ is a constant below 1. The full proof, with the expander mixing lemma, is below.

## Complexity

- **Random bits.** $\log_2 N + (t - 1)\log_2 d = m + (t - 1)\log_2 d$. With constant $d$ and $\lambda$, and $t = O(k)$, this is $m + O(k)$.
- **Time.** $t - 1$ neighbour computations and $t$ runs of $\mathcal{A}$. The early exit in line L6 can stop after one run.
- **Space.** The walk can be generated online, one vertex at a time, so only the current vertex is needed; storing the whole walk takes $t$ vertices.
- **Comparison.** Independent repetition uses $km$ random bits for error $2^{-k}$; pairwise independent repetition uses $2m$ random bits and $2^k$ runs. The walk needs $O(k)$ runs, as independent repetition does, and only $O(k)$ random bits beyond the $m$ bits of one run.

## Properties

- **Each vertex is uniform.** The uniform distribution is stationary for a regular graph, so each $v_i$ alone is a uniform random string, and the expected number of visits to a set of density $\mu$ is $\mu t$.
- **One-sided error stays one-sided.** The walk never makes $\mathcal{A}$ accept a wrong input.
- **Chernoff bound (Gillman 1998).** For $f : V \to [0, 1]$ with mean $\mu$, the average of $f$ along the walk deviates from $\mu$ by more than $\varepsilon$ with probability $e^{-\Omega((1 - \lambda)\varepsilon^2 t)}$. So the walk also reduces the error of two-sided [BPP](/bpp/) algorithms, by a majority vote, with $m + O(k)$ random bits.
- **Not a generator for all tests.** The samples are strongly correlated: $v_2$ is always a neighbour of $v_1$. Only tests that look at the membership of each vertex in a fixed set are fooled.
- **Monotone in the expansion.** A smaller $\lambda$ gives a smaller bound. For $\lambda = 0$ (the complete graph with loops) the walk is a sequence of independent samples, and the bound becomes $\mu^t$.

## Variants and improvements

- **Explicit expanders.** The graph must be explicit. Families of constant degree with $\lambda$ bounded away from 1 include the affine graphs on $\mathbb{Z}_m \times \mathbb{Z}_m$ of Margulis (1973) and Gabber and Galil (1981), the Ramanujan graphs of Lubotzky, Phillips and Sarnak, and the zig-zag product of Reingold, Vadhan and Wigderson (2000). For $\lambda \le 1/2$, take a power $G^r$ of the graph: it has degree $d^r$ and expansion $\lambda^r$.
- **Two-sided error.** Run $\mathcal{A}$ on the $t$ walk vertices and output the majority vote. The Chernoff bound for expander walks gives error $2^{-k}$ with $t = O(k)$.
- **Samplers for mean estimation.** The average of $f(v_i)$ estimates the mean of $f$ within $\varepsilon$ with probability $1 - \delta$ using $m + O(\log(1/\delta)/\varepsilon^2)$ random bits. Combining the walk with pairwise independence or extractors gives better dependence on $\varepsilon$.
- **Hitting sets.** If only the hitting property is needed, the walk is a [hitting set generator](/hitting-set-generator/) for sets of density at least $1 - \mu$.
- **Dispersers.** The bipartite graph that joins a seed of the walk to its vertices is a [disperser](/disperser/): every large set of seeds reaches almost all vertices.

## When to use it

Use it to reduce the error of a randomized algorithm when random bits are scarce, for example when the algorithm runs in small space and the random bits must be stored, or when the bits come from a weak source. For an RP algorithm, independent runs are simpler and good enough when random bits are cheap. For constant error reduction factors, pairwise independent runs are simpler.

## Pitfalls

- **Bipartite graphs.** A bipartite graph has $\lambda_N = -1$, so $\lambda = 1$ and the bound says nothing. A walk on a cycle of even length alternates between the two sides and can stay in a bad set of density $1/2$ forever. Use a graph with self-loops, or check $|\lambda_N|$ as well as $\lambda_2$.
- **Start from a uniform vertex.** A fixed start vertex can lie in $B$, and then the first sample is always bad. The bound $\mu(\ldots)^{t-1}$ needs the uniform start.
- **The bad set must be fixed in advance.** The analysis holds for a set $B$ that does not depend on the walk. An adversary who sees the walk can make it fail.
- **Constants matter.** With $\lambda$ close to 1, the factor $\mu + \lambda(1 - \mu)$ is close to 1, and $t$ must be large. For $\lambda = 0.9$ and $\mu = 1/2$ the factor is $0.95$, and $t$ grows to about $13.5 k$.
- **Graph size.** The graph needs exactly one vertex for each random string. If $N$ is not the size of a known family, embed the strings into a larger graph and treat the extra vertices as bad, which increases $\mu$.

## Implementations

## History

Ajtai, Komlós and Szemerédi (1987) used walks on expanders to simulate randomized logspace algorithms with fewer random bits. Cohen and Wigderson (1989) and Impagliazzo and Zuckerman (1989) showed that a walk on an expander reduces the error of RP and BPP algorithms to $2^{-k}$ with $m + O(k)$ random bits. Gillman (1998) proved the Chernoff bound for expander walks, with explicit constants in terms of the spectral gap. Expander walks became a standard tool of derandomization; they are used in Reingold's logspace algorithm for undirected connectivity and in constructions of small-bias spaces.

## References
