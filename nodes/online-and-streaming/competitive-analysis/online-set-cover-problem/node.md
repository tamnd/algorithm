---
tag: GDSBT6
kind: problem
slug: online-set-cover-problem
name: Online set cover problem
aliases:
- online set cover
- online weighted set cover
area: online-and-streaming/competitive-analysis
level: advanced
summary: The sets are known; elements arrive one at a time and each must be covered at once by sets bought for good. The best ratio is O(log m log n), and deterministic algorithms cannot do much better.
prereqs: [set-cover, online-algorithm, competitive-ratio]
see_also: [online-randomized-set-cover, online-primal-dual, online-vertex-cover-problem, greedy-set-cover, set-cover-inapproximability, frequency-rounding-set-cover, online-facility-location-problem, oblivious-adversary]
sources:
  - paper: doi:10.1137/060661946
    title: "Noga Alon, Baruch Awerbuch, Yossi Azar, Niv Buchbinder and Joseph (Seffi) Naor, The online set cover problem, SIAM Journal on Computing 39(2) (2009), 361-370"
    locator: the model, the randomized and the deterministic O(log m log n) algorithms, and the lower bound for deterministic algorithms
  - paper: doi:10.1561/0400000024
    title: "Niv Buchbinder and Joseph (Seffi) Naor, The design of competitive online algorithms via a primal-dual approach, Foundations and Trends in Theoretical Computer Science 3(2-3) (2009), 93-263"
    locator: Chapter 4 (the fractional covering algorithm and the lower bound Omega(log d)) and Chapter 5 (online set cover and the discussion of its lower bounds)
  - paper: "Simon Korman, On the use of randomization in the online set cover problem, M.Sc. thesis, Weizmann Institute of Science, 2004"
    title: On the use of randomization in the online set cover problem
    locator: the lower bound Omega(log m log n) for randomized polynomial-time online algorithms unless NP is contained in BPP
---

Online set cover is the problem of covering elements that arrive one at a time with sets that are bought for good. The ground set and the family of sets with their costs are known at the start, but the elements that must be covered, a subset of the ground set, arrive one by one, and each must be covered when it arrives. The goal is a small total cost compared with the cheapest cover of the elements that arrived. Alon, Awerbuch, Azar, Buchbinder and Naor (2003, journal 2009) gave a randomized and a deterministic algorithm with ratio $O(\log m \log n)$ for $m$ sets and $n$ elements, and showed that deterministic algorithms cannot beat $\Omega(\log m \log n / (\log \log m + \log \log n))$. The [randomized algorithm](/online-randomized-set-cover/) is the standard example of the [online primal-dual method](/online-primal-dual/) followed by online rounding.

## In plain words

A company knows all the service packages it could buy and what each costs. Each package handles some of the customer needs. The needs appear one at a time, and each new need must be handled at once, by a package that the company already has or buys now. A package, once bought, is kept.

The company wants to spend little, compared with the cheapest set of packages that it would have bought had it known all the needs at the start. Buying the cheapest package for each new need can be very bad, because one larger package could have handled all the needs. The best methods pay about the product of two logarithms, one for the number of packages and one for the number of needs, times the best cost.

## Definition

**Input.** A ground set $X$ of $n$ elements, a family $\mathcal{S}$ of $m$ subsets of $X$, and a cost $c_S > 0$ for each $S \in \mathcal{S}$, all known at the start. Then a sequence $\sigma = j_1, j_2, \ldots, j_r$ of elements of $X$, revealed one at a time. For each element $j$, $\mathcal{S}(j)$ is the family of sets that contain $j$, and $d = \max_j \lvert \mathcal{S}(j) \rvert \le m$ is the largest frequency.

**Output.** A family $C_t \subseteq \mathcal{S}$ after each step $t$, with $C_{t-1} \subseteq C_t$ (no set is removed) and $j_t \in \bigcup C_t$.

**Cost.** $\mathrm{ALG}(\sigma) = \sum_{S \in C_r} c_S$. $\mathrm{OPT}(\sigma)$ is the least cost of a family that covers $\{j_1, \ldots, j_r\}$. An algorithm is $\rho$-competitive if $\mathrm{ALG}(\sigma) \le \rho \cdot \mathrm{OPT}(\sigma)$ for each $\sigma$, with no additive term. For a randomized algorithm, $\mathbb{E}[\mathrm{ALG}(\sigma)] \le \rho \cdot \mathrm{OPT}(\sigma)$ against an [oblivious adversary](/oblivious-adversary/), which fixes $\sigma$ in advance.

**What the algorithm knows.** The [randomized algorithm](/online-randomized-set-cover/) needs only $n$, $d$ (or the bound $m$) and, when $j$ arrives, the sets of $\mathcal{S}(j)$ with their costs. The rest of the set system may stay hidden. A repeated element changes nothing, so one may assume that the elements of $\sigma$ are distinct and $r \le n$.

**Fractional version.** The algorithm keeps $x_S \in [0, 1]$, which may only increase, with $\sum_{S \in \mathcal{S}(j_t)} x_S \ge 1$ after step $t$, at cost $\sum_S c_S x_S$. This is the online form of the set cover LP, and the benchmark is its optimum $\mathrm{OPT}_{LP} \le \mathrm{OPT}$.

## Variants

- **Unweighted.** All costs are 1, and the cost is the number of sets. The bounds below are the same.
- **Fractional.** As above. The best ratio is $\Theta(\log d)$.
- **Online vertex cover.** The sets are the vertices of a graph and the elements are its edges, so $d = 2$. This is [online vertex cover](/online-vertex-cover-problem/) in the edge arrival model.
- **Multicover.** Element $j$ must be covered by $b_j$ different sets. The primal-dual method extends to this and to covering integer programs.
- **Random order.** The adversary fixes the elements but their order is uniformly random. Gupta, Kehne and Levin (2021) gave an algorithm with ratio $O(\log m n)$ in this model, the same order as the offline [greedy algorithm](/greedy-set-cover/).
- **Learning-augmented.** The algorithm gets a predicted solution, which may be wrong. Bamas, Maggiori and Svensson (2020) gave versions of the primal-dual method that follow a good prediction and stay within the usual bounds when the prediction is bad; see [learning-augmented algorithms](/learning-augmented-algorithms/).

## Examples

**The cheapest set for each element is bad.** Take $X = \{1, \ldots, n\}$, the singletons $\{i\}$ with cost 1, and the whole set $X$ with cost $1 + \varepsilon$. The elements $1, 2, \ldots, n$ arrive in order. The rule "buy the cheapest set that contains each uncovered element" buys every singleton and pays $n$, while $\mathrm{OPT} = 1 + \varepsilon$. So this rule has ratio close to $n$, and with $m = n + 1$ also close to $m$. The rule pays at most $\mathrm{OPT}$ for each element, so $n$ is also an upper bound for it.

**The halving instance.** Take $m = 2^k$ sets $S_1, \ldots, S_m$, all with cost 1, as the leaves of a complete binary tree of depth $k$. The ground set has one element for each of the $2m - 1$ nodes of the tree, and the element of a node belongs to the sets of the leaves below it. The adversary keeps a group $F_t$ of sets, the leaves below a node, with $F_1 = \mathcal{S}$. Element $j_t$ is the element of that node, so it belongs exactly to the sets of $F_t$. After step $t$, the adversary splits $F_t$ into two halves and keeps as $F_{t+1}$ the half on which the algorithm has spent less. After $k + 1$ elements, $F_{k+1}$ is a single set $S^*$, which contains all the elements, so $\mathrm{OPT} = 1$. With $k = 3$ and the fractional rule that spreads the missing mass evenly, the steps are as follows.

| step $t$ | $\lvert F_t \rvert$ | mass on $F_t$ before | mass added | total cost after |
|---|---|---|---|---|
| 1 | 8 | 0 | 1 | 1 |
| 2 | 4 | 1/2 | 1/2 | 1.5 |
| 3 | 2 | 1/2 | 1/2 | 2 |
| 4 | 1 | 1/2 | 1/2 | 2.5 |

The total is $1 + k/2 = 2.5$ against $\mathrm{OPT} = 1$. Theorem 3 shows that every online algorithm pays at least this much.

## Known algorithms

- **[Online randomized set cover](/online-randomized-set-cover/)** (Alon, Awerbuch, Azar, Buchbinder and Naor). A multiplicative fractional update and threshold rounding with $\lceil 2 \ln n \rceil$ random values per set. Expected ratio $O(\log m \log n)$, more precisely $2 \lceil 2 \ln n \rceil \ln(1 + d) + 1/n$.
- **Deterministic algorithm of Alon et al.** The same fractional update, with the random thresholds replaced by a potential function that the algorithm keeps below a fixed bound. Ratio $O(\log m \log n)$.
- **Online fractional covering** (Buchbinder and Naor). The fractional layer alone, ratio $2 \ln(1 + d)$ for the fractional problem; see the [online primal-dual method](/online-primal-dual/).
- **Online primal-dual with frequency $d$.** When an uncovered element $j$ arrives, raise its dual $y_j$ until a set of $\mathcal{S}(j)$ becomes tight, and buy the tight sets. Deterministic, ratio $d$ (Theorem 2). For [vertex cover](/online-vertex-cover-problem/), $d = 2$.
- **Cheapest set per element.** Ratio $n$, and this is tight (see the examples).

## Bounds

**Theorem 1 (upper bound).** There is a randomized online algorithm with $\mathbb{E}[\mathrm{ALG}] \le \bigl(2 \lceil 2 \ln n \rceil \ln(1 + d) + 1/n\bigr) \mathrm{OPT}$ for $n \ge 2$, so $O(\log m \log n)$-competitive against an oblivious adversary.

*Proof.* The full proof is on the page of the [algorithm](/online-randomized-set-cover/). In short, the fractional update pays at most twice the dual, and the dual divided by $\ln(1 + d)$ is feasible, so the fractional cost $P$ is at most $2 \ln(1 + d) \mathrm{OPT}$. A set with threshold $\theta_S$, the minimum of $k = \lceil 2 \ln n \rceil$ uniform values, is bought with probability at most $k x_S$, so the threshold sets cost at most $kP$ in expectation. An element is missed with probability at most $e^{-k} \le 1/n^2$, and its fallback set costs at most $\mathrm{OPT}$. $\square$

**Theorem 2 (ratio $d$, deterministic).** The online primal-dual rule of the list above returns a cover of cost at most $d \cdot \mathrm{OPT}$.

*Proof.* Let $\mathrm{slack}(S) = c_S - \sum_{j \in S} y_j$. When an uncovered element $j$ arrives, the rule raises $y_j$ by $\min_{S \in \mathcal{S}(j)} \mathrm{slack}(S)$, which is at least 0, and buys the sets of $\mathcal{S}(j)$ whose slack becomes 0. At least one set of $\mathcal{S}(j)$ is bought, so the output is a cover. The slacks never become negative, so $y$ is a feasible solution of the dual LP $\max \sum_j y_j$, $\sum_{j \in S} y_j \le c_S$, and $\sum_j y_j \le \mathrm{OPT}_{LP} \le \mathrm{OPT}$ by [weak duality](/weak-duality/). Each bought set has slack 0, so

$$\mathrm{ALG} = \sum_{S \in C} c_S = \sum_{S \in C} \sum_{j \in S} y_j \le \sum_j \lvert \mathcal{S}(j) \rvert \, y_j \le d \sum_j y_j \le d \cdot \mathrm{OPT}.$$

$\square$

This is the online form of the offline [frequency rounding](/frequency-rounding-set-cover/) and [primal-dual](/set-cover-primal-dual/) algorithms. It is useful when $d$ is small.

**Theorem 3 (lower bound $1 + \frac{1}{2} \log_2 m$, all algorithms).** For each $k \ge 1$, each online algorithm for fractional set cover, and so each deterministic algorithm and each randomized algorithm against an oblivious adversary, pays at least $1 + k/2$ on the halving instance with $m = d = 2^k$ unit-cost sets and $n = 2m - 1$ elements, of which $k + 1$ arrive, where $\mathrm{OPT} = 1$.

*Proof.* For a fractional algorithm, let $x$ be its values. For a deterministic integral algorithm, $x_S \in \{0, 1\}$ marks the bought sets. For a randomized algorithm, let $x_S$ at step $t$ be the probability that $S$ is bought by step $t$. The adversary knows the algorithm, so it can compute these numbers without seeing any coins, and they never decrease. In all three cases $\sum_{S \in F_t} x_S \ge 1$ after step $t$, because the element $j_t$ is covered (for the randomized case, in every outcome, so also in expectation), and the cost, or the expected cost, is $\sum_S x_S$.

Let $M_t$ be the mass $\sum_{S \in F_t} x_S$ after step $t$, so $M_t \ge 1$. The adversary keeps the half $F_{t+1}$ with less mass, so the other half $F_t \setminus F_{t+1}$ has mass at least $M_t / 2 \ge 1/2$ at the end of step $t$. These halves, for $t = 1, \ldots, k$, are disjoint from each other and from $F_{k+1}$, whose mass is at least 1 after step $k + 1$. The values never decrease, so the final cost is at least $k/2 + 1$. The single set of $F_{k+1}$ lies in every $F_t$, so it contains all elements, and $\mathrm{OPT} = 1$. $\square$

So no algorithm is better than $\Omega(\log m)$-competitive, and no fractional algorithm is better than $\Omega(\log d)$-competitive. In this instance $\log n \approx \log m$, so it does not show that the two factors of Theorem 1 are both needed; Theorems 4 and 5 do that. The fractional algorithm of Buchbinder and Naor matches the bound up to a constant: it pays at most $2 \ln(1 + d)$.

**Theorem 4 (deterministic lower bound, cited).** Alon et al. showed that each deterministic online algorithm has ratio $\Omega\bigl(\log m \log n / (\log \log m + \log \log n)\bigr)$ on some instances, for a wide range of the values of $m$ and $n$. So the deterministic algorithm with ratio $O(\log m \log n)$ is optimal up to the $\log \log$ factor. The proof, in the journal paper, is a more careful adversary of the halving kind, which keeps a cheap cover alive while it forces the algorithm to buy sets that the cover does not need.

**Theorem 5 (randomized polynomial-time lower bound, cited).** The thesis of Korman (2004), as reported by Buchbinder and Naor, shows that no randomized online algorithm that runs in polynomial time has ratio $o(\log m \log n)$ unless $\mathrm{NP} \subseteq \mathrm{BPP}$. So for efficient algorithms the bound of Theorem 1 is optimal up to a constant.

**Offline hardness applies.** An online algorithm that runs in polynomial time is also an offline approximation algorithm with the same ratio: feed the elements in any order. So the [inapproximability of set cover](/set-cover-inapproximability/), a ratio of $(1 - \varepsilon) \ln n$ is NP-hard for each $\varepsilon > 0$, holds online too. The online lower bounds above are stronger, because they add the factor $\log m$ from not knowing the future.

| setting | upper bound | lower bound |
|---|---|---|
| fractional | $2 \ln(1 + d)$ | $1 + \frac{1}{2}\log_2 d$ (Theorem 3) |
| deterministic | $O(\log m \log n)$, and $d$ | $\Omega\bigl(\frac{\log m \log n}{\log \log m + \log \log n}\bigr)$ |
| randomized, oblivious | $O(\log m \log n)$ | $\Omega(\log m)$ in general; $\Omega(\log m \log n)$ in polynomial time unless $\mathrm{NP} \subseteq \mathrm{BPP}$ |

## Reductions

- **Vertex cover to set cover.** A graph with edges arriving is a set system with $d = 2$: each vertex is the set of its edges. Theorem 2 then gives ratio 2 for weighted [online vertex cover](/online-vertex-cover-problem/).
- **Set cover to its online version.** An offline instance becomes an online one by sending its elements in any order. So the offline [hardness](/set-cover-inapproximability/) limits polynomial-time online algorithms.
- **Hitting set.** Online hitting set, where sets arrive and each must be hit by a chosen element, is the same problem with the roles of elements and sets swapped.
- **Facility location.** Non-metric [online facility location](/online-facility-location-problem/) contains online set cover as the special case in which each client is at distance 0 from the facilities of its sets and at infinite distance from the others.

## Applications

- **Buying services as needs arise.** Licences, server images or cloud services that each serve a known group of requests, bought when the first request of a kind appears and kept afterwards.
- **Network and facility design.** Placing caches, sensors or monitors when the points that must be watched appear one at a time.
- **A building block.** The fractional covering update and its rounding are used inside online algorithms for facility location, weighted paging, network design and the [adwords problem](/online-adwords-problem/).

## References
