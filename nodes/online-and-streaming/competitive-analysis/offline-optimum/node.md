---
tag: M9ZEY9
kind: definition
slug: offline-optimum
name: Offline optimum
aliases:
- OPT
- optimal offline cost
area: online-and-streaming/competitive-analysis
level: intro
summary: The best cost any algorithm could achieve on a given input when it knows the whole input in advance.
prereqs: [online-algorithm, offline-algorithm]
see_also: [competitive-ratio, belady-algorithm, ski-rental-problem, adaptive-offline-adversary, regret, paging-problem]
sources:
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 1 (the optimal offline cost OPT and the definition of competitiveness)
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the comparison of each on-line rule with the optimum off-line rule on the same sequence
  - paper: doi:10.1147/sj.52.0078
    title: "L. A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2) (1966), 78-101"
    locator: the optimal replacement rule MIN
---

The offline optimum $\mathrm{OPT}(\sigma)$ of a request sequence $\sigma$ is the smallest cost that any algorithm can reach on $\sigma$ when it knows all of $\sigma$ in advance. It is the cost of an optimal [offline algorithm](/offline-algorithm/) on $\sigma$, and it is the benchmark of the [competitive ratio](/competitive-ratio/): an [online algorithm](/online-algorithm/) is judged by how far its cost can be from $\mathrm{OPT}(\sigma)$ on the worst $\sigma$.

## Definition

Fix a request set $R$, an answer set $A$ and cost functions $f_n : R^n \times A^n \to \mathbb{R}_{\ge 0} \cup \{\infty\}$, as in a [request-answer game](/request-answer-game/). For a minimization problem and $\sigma \in R^n$,

$$\mathrm{OPT}(\sigma) = \inf_{a \in A^n} f_n(\sigma, a).$$

When $A$ is finite, the infimum is a minimum, and an answer sequence $a^*$ with $f_n(\sigma, a^*) = \mathrm{OPT}(\sigma)$ exists. For a maximization problem with profit functions $f_n$, $\mathrm{OPT}(\sigma) = \sup_{a \in A^n} f_n(\sigma, a)$.

Three points of the definition matter in use.

- **One value for each sequence.** The optimum is taken again for each $\sigma$. The answers $a^*$ that reach $\mathrm{OPT}(\sigma)$ may depend on all of $\sigma$, and two sequences with the same prefix can need different first answers. So in general no single online algorithm reaches $\mathrm{OPT}(\sigma)$ on every $\sigma$.
- **Same start state.** The online algorithm and the optimum start in the same state (for example, the same cache contents), unless the problem says otherwise. If the start states differ, the additive constant $b$ of the competitive ratio absorbs the difference.
- **Cost, not time.** $\mathrm{OPT}(\sigma)$ is a number. Its definition says nothing about how fast it can be computed. For paging and ski rental it is easy to compute; for [bin packing](/bin-packing/) it is NP-hard, but it is still the benchmark of online bin packing.

For an algorithm ALG with $\mathrm{ALG}(\sigma) = 0$ whenever $\mathrm{OPT}(\sigma) = 0$, the strict competitive ratio is $\sup \mathrm{ALG}(\sigma)/\mathrm{OPT}(\sigma)$ over the sequences with $\mathrm{OPT}(\sigma) > 0$.

**Notation.** $\sigma$ is the request sequence, $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the costs of the online algorithm and of the optimal offline solution on $\sigma$, and $k$ is the cache size.

## Examples and non-examples

- **Ski rental.** Renting costs 1 per day and buying costs $B$. If the season has $n$ days, the optimum buys on day 1 when $n \ge B$ and rents every day otherwise: $\mathrm{OPT}(n) = \min(n, B)$. For $B = 10$: $\mathrm{OPT}(3) = 3$, $\mathrm{OPT}(10) = 10$ and $\mathrm{OPT}(15) = 10$. See the [ski rental problem](/ski-rental-problem/).
- **Paging.** For a cache of $k$ pages, [Belady's rule](/belady-algorithm/) (evict the page requested furthest in the future) reaches the optimum. On $\sigma = 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5$ with $k = 3$ and an empty cache, $\mathrm{OPT}(\sigma) = 7$ faults, while [LRU](/lru/) makes 10.
- **Bahncard.** In the [Bahncard problem](/bahncard-problem/), the optimum chooses the times to buy a discount card. A small dynamic program over the request times computes it.
- **Non-example: the best online algorithm.** The cost of the best online algorithm on $\sigma$ is not $\mathrm{OPT}(\sigma)$. For ski rental with $B = 10$, every deterministic online rule pays at least $1.9 \cdot \mathrm{OPT}$ on some season, and no online rule pays $\min(n, B)$ for every $n$: the rule would have to buy on day 1 for $n = 10$ and rent on day 1 for $n = 1$, while the two seasons look the same on day 1.
- **Non-example: the best fixed action in hindsight.** In online learning, [regret](/regret/) compares the learner with the best single action for the whole sequence. That benchmark is weaker than $\mathrm{OPT}(\sigma)$, which may change its action at each step.
- **Non-example: the adversary's cost against an online adversary.** Against an [adaptive online adversary](/adaptive-adversary/), the adversary serves its own sequence online, so its cost can be larger than $\mathrm{OPT}(\sigma)$. Only the [oblivious](/oblivious-adversary/) and the [adaptive offline](/adaptive-offline-adversary/) adversaries pay exactly $\mathrm{OPT}(\sigma)$.

## Related definitions

- **[Offline algorithm](/offline-algorithm/).** An algorithm that sees all of $\sigma$ first. An optimal one has cost $\mathrm{OPT}(\sigma)$ on each $\sigma$.
- **[Online algorithm](/online-algorithm/).** An algorithm whose answer to $r_i$ depends only on $r_1, \ldots, r_i$.
- **[Competitive ratio](/competitive-ratio/).** The smallest $c$ with $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$.
- **[Approximation ratio](/approximation-ratio/).** The same comparison with the optimum, but for an offline algorithm with limited running time. The competitive ratio limits information; the approximation ratio limits time.

## References
