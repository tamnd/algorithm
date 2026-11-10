---
tag: NQTQDC
kind: definition
slug: competitive-ratio
name: Competitive ratio
aliases:
- competitive factor
- c-competitive algorithm
area: online-and-streaming/competitive-analysis
level: intro
summary: The worst-case ratio of an online algorithm's cost to the offline optimum over all inputs.
prereqs: [online-algorithm, offline-optimum]
see_also: [offline-algorithm, ski-rental-problem, randomized-online-algorithm, oblivious-adversary, request-answer-game, approximation-ratio, paging-problem, regret]
sources:
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the comparison of on-line rules with the best off-line rule, up to a constant factor and an additive term
  - paper: doi:10.1007/BF01762111
    title: "Anna R. Karlin, Mark S. Manasse, Larry Rudolph and Daniel D. Sleator, Competitive snoopy caching, Algorithmica 3(1) (1988), 79-119"
    locator: the definition of a c-competitive algorithm
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 1 (the definition of competitiveness, with the additive constant)
  - paper: doi:10.1145/3056461
    title: "Joan Boyar, Lene M. Favrholdt, Christian Kudahl, Kim S. Larsen and Jesper W. Mikkelsen, Online algorithms with advice: a survey, ACM Computing Surveys 50(2) (2017), Article 19"
    locator: Section 1 (the competitive ratio for minimization and maximization problems)
---

The competitive ratio of an [online algorithm](/online-algorithm/) is the smallest factor $c$ such that, on every request sequence, its cost is at most $c$ times the [offline optimum](/offline-optimum/), up to an additive constant. It measures the price of not knowing the future in the worst case. The name and the definition come from Karlin, Manasse, Rudolph and Sleator (1988), after the analysis of list update and paging by Sleator and Tarjan (1985).

## Definition

**Notation.** $\sigma$ is the request sequence, $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the costs of the online algorithm and of the optimal offline solution on $\sigma$, $c$ is the competitive ratio, and $k$ is the cache size.

**Minimization.** A deterministic online algorithm ALG is **$c$-competitive** if there is a constant $b$ such that

$$\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b \quad \text{for every finite request sequence } \sigma.$$

The constant $b$ may depend on the problem parameters (for example $k$), but not on $\sigma$. ALG is **strictly $c$-competitive** if the inequality holds with $b = 0$. The **competitive ratio** of ALG is the infimum of all $c$ for which ALG is $c$-competitive. The **strict competitive ratio** is the infimum of all $c$ for which ALG is strictly $c$-competitive. When $\mathrm{ALG}(\sigma) = 0$ whenever $\mathrm{OPT}(\sigma) = 0$, the strict ratio is $\sup_\sigma \mathrm{ALG}(\sigma)/\mathrm{OPT}(\sigma)$ over the sequences with $\mathrm{OPT}(\sigma) > 0$.

The additive constant matters only when $\mathrm{OPT}(\sigma)$ can stay bounded while the inputs grow in number. It removes the effect of a start-up cost that does not grow with $\sigma$. The competitive ratio is at most the strict competitive ratio.

**Maximization.** For a problem where ALG and OPT are profits, ALG is $c$-competitive if there is a constant $b$ with

$$\mathrm{OPT}(\sigma) \le c \cdot \mathrm{ALG}(\sigma) + b \quad \text{for every } \sigma,$$

so that $c \ge 1$ in both cases. This is the convention of Borodin and El-Yaniv and of the survey of Boyar et al. Many papers use the inverse convention for maximization: $\mathrm{ALG}(\sigma) \ge c' \cdot \mathrm{OPT}(\sigma) - b$ with $c' \le 1$. The two are the same statement with $c' = 1/c$. For example, the ratio $1 - 1/e$ of the [ranking algorithm](/ranking-algorithm/) for [online bipartite matching](/online-bipartite-matching/) is $e/(e-1)$ in the first convention.

**Randomized algorithms.** For a [randomized online algorithm](/randomized-online-algorithm/), $\mathrm{ALG}(\sigma)$ is a random variable. Against an [oblivious adversary](/oblivious-adversary/), ALG is $c$-competitive if $\mathbb{E}[\mathrm{ALG}(\sigma)] \le c \cdot \mathrm{OPT}(\sigma) + b$ for every $\sigma$. Against the stronger [adaptive online](/adaptive-adversary/) and [adaptive offline](/adaptive-offline-adversary/) adversaries the sequence depends on the random choices, and the definition changes. A claim about a randomized ratio must name the adversary.

**The ratio of a problem.** The deterministic competitive ratio of a problem is the infimum of the competitive ratios of all deterministic online algorithms for it. An algorithm is **optimal** if it reaches this value. An upper bound is an algorithm and its analysis. A lower bound is an adversary argument that holds for every algorithm.

## Examples and non-examples

**Worked example: ski rental with $B = 4$.** Renting costs 1 per day and buying costs $B = 4$. The season has $n$ days, unknown in advance, and $\mathrm{OPT}(n) = \min(n, 4)$. The rule "buy on day $j$" rents on days $1, \ldots, j - 1$ and buys on day $j$, so it pays $n$ if $n < j$ and $j - 1 + 4$ if $n \ge j$. The worst season for this rule ends on day $j$, just after the purchase. The table gives the exact strict ratio $\sup_n \mathrm{ALG}(n)/\mathrm{OPT}(n)$ of each rule.

| buy on day $j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | never |
|---|---|---|---|---|---|---|---|---|
| worst ratio | $4$ | $5/2$ | $2$ | $7/4$ | $2$ | $9/4$ | $5/2$ | $\infty$ |

For $j = 4$: if $n \le 3$ the rule pays $n = \mathrm{OPT}$, and if $n \ge 4$ it pays $3 + 4 = 7$ against $\mathrm{OPT} = 4$. So the [break-even strategy](/break-even-strategy/) $j = B$ is strictly $7/4$-competitive, and $7/4 = 2 - 1/B$ is the best deterministic ratio. The rule "never buy" pays $n$ against $\mathrm{OPT} = 4$, so no constants $c$ and $b$ work for it. The [ski rental problem](/ski-rental-problem/) proves the general case.

**Strict and non-strict ratios differ.** In [paging](/paging-problem/), let the online algorithm and OPT start with different caches. On the sequence that requests the $k$ pages of OPT's cache once each, OPT pays 0 and the online algorithm pays up to $k$ faults. No finite strict ratio holds, but [LRU](/lru/) is $k$-competitive with $b = k$. With the same start cache for both, LRU is strictly $k$-competitive.

**Non-example: the approximation ratio.** The [approximation ratio](/approximation-ratio/) also compares a cost with $\mathrm{OPT}$, but for an offline algorithm with limited running time. The competitive ratio limits information, not time: an online algorithm with unlimited time still has a ratio above 1 for ski rental.

**Non-example: regret.** [Regret](/regret/) is the difference $\mathrm{ALG} - \mathrm{OPT}'$ against the best fixed action in hindsight $\mathrm{OPT}'$. It is a difference, not a ratio, and the benchmark is weaker than $\mathrm{OPT}(\sigma)$.

**Non-example: the average-case ratio.** The ratio $\mathbb{E}[\mathrm{ALG}]/\mathbb{E}[\mathrm{OPT}]$ under a fixed input distribution is an [average-case analysis](/average-case-analysis/). The competitive ratio takes the worst $\sigma$. For randomized algorithms, the [Yao principle](/yao-minimax-principle/) links the two: if every deterministic algorithm has $\mathbb{E}[\mathrm{ALG}] \ge c \cdot \mathbb{E}[\mathrm{OPT}]$ on one input distribution, then no randomized algorithm is strictly better than $c$-competitive against an oblivious adversary.

## Related definitions

- **[Offline optimum](/offline-optimum/).** The benchmark $\mathrm{OPT}(\sigma)$, and the cost of the optimal [offline algorithm](/offline-algorithm/).
- **[Request-answer game](/request-answer-game/).** The general framework where the definition applies to any online problem.
- **[Oblivious adversary](/oblivious-adversary/), [adaptive online adversary](/adaptive-adversary/), [adaptive offline adversary](/adaptive-offline-adversary/).** The three adversary models for randomized algorithms.
- **[Advice model](/advice-model/).** The competitive ratio as a function of the number of bits the algorithm may read about the future.
- **[Amortized cost](/amortized-cost/).** Many competitive proofs use a [potential function](/potential-function/) to compare ALG and OPT step by step, as in the analysis of [move to front](/move-to-front/).

## References
