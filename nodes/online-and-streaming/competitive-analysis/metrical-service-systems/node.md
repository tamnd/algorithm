---
tag: HM2B6B
kind: problem
slug: metrical-service-systems
name: Metrical service systems
aliases:
- MSS
- metrical service system
- layered graph traversal
area: online-and-streaming/competitive-analysis
level: advanced
summary: A server must move to a requested set of points in a metric; a special case of metrical task systems.
prereqs: [metrical-task-systems, competitive-ratio, metric-space]
see_also: [work-function, work-function-algorithm, k-server-problem, linear-search-problem, paging-problem, randomized-online-algorithm]
sources:
  - paper: "Marek Chrobak and Lawrence L. Larmore, The server problem and on-line games, in On-Line Algorithms, DIMACS Series in Discrete Mathematics and Theoretical Computer Science 7 (1992), 11-64"
    title: "Chrobak and Larmore, The server problem and on-line games (1992)"
    locator: the definition of metrical service systems, the relation with the k-server problem, and the bounds for small width
  - paper: "Christos H. Papadimitriou and Mihalis Yannakakis, Shortest paths without a map, Theoretical Computer Science 84(1) (1991), 127-150"
    title: "Papadimitriou and Yannakakis, Shortest paths without a map (1991)"
    locator: the layered graph traversal problem and the ratio 9 for width 2
  - paper: "Amos Fiat, Dean P. Foster, Howard Karloff, Yuval Rabani, Yiftach Ravid and Sundar Vishwanathan, Competitive algorithms for layered graph traversal, SIAM Journal on Computing 28(2) (1998)"
    title: "Fiat, Foster, Karloff, Rabani, Ravid and Vishwanathan, Competitive algorithms for layered graph traversal (1998)"
    locator: the equivalence of layered graph traversal and metrical service systems, the deterministic upper bound O(9^k) and the lower bound Omega(2^k)
  - url: https://arxiv.org/abs/2202.04551
    title: "Sebastien Bubeck, Christian Coester and Yuval Rabani, Shortest paths without a map, but with an entropic regularizer, FOCS 2022"
    locator: the randomized upper bound O(k^2) for layered graph traversal of width k
  - url: https://arxiv.org/abs/2211.05753
    title: "Sebastien Bubeck, Christian Coester and Yuval Rabani, The randomized k-server conjecture is false!, STOC 2023"
    locator: the randomized lower bound Omega(k^2) for metrical service systems with requests of k points
---

In the metrical service systems problem (MSS), one server lives in a [metric space](/metric-space/). Each request is a set of points, and the server must move to one of them before the next request arrives. The cost is the total distance moved. Chrobak and Larmore introduced the problem in 1991 and 1992, as the special case of [metrical task systems](/metrical-task-systems/) in which every task cost is $0$ or $\infty$. The competitive ratio depends on the width $k$, the largest size of a request, and not on the size of the space. MSS is equivalent to the layered graph traversal problem of Papadimitriou and Yannakakis, and the [k-server problem](/k-server-problem/) on $k + 1$ points is the case where every request has $k$ points.

## In plain words

A repair van must stand at one of a few listed places at each moment. Every hour, a new list of places arrives, and the van must drive to one of them. You pay for the distance the van drives. You do not know the next lists.

The nearest place on the list is not always the best choice. A place that is far away may stay on every list, while the near places change each hour. A van that always takes the nearest place can drive back and forth forever, while a van that went once to the far place pays nothing more. A good rule keeps track of the cost of each choice in hindsight, and moves to the far place once it is clear that it is worth the trip.

## Definition

**Notation.**

| Symbol | Meaning |
|---|---|
| $(M, d)$ | the metric space, finite or infinite |
| $\sigma = R_1, \ldots, R_m$ | the request sequence: $m$ nonempty finite sets of points |
| $k$ | the width, $\max_t \lvert R_t \rvert$ |
| $s_0$ | the start point of the server |
| $\mathrm{ALG}(\sigma)$, $\mathrm{OPT}(\sigma)$ | the online cost and the optimal offline cost |
| $c$ | the competitive ratio |

**Input.** A metric space, a start point $s_0$, and request sets $R_1, \ldots, R_m$ of size at most $k$ that arrive online.

**Output.** Points $s_1, \ldots, s_m$ with $s_t \in R_t$, where $s_t$ is chosen before $R_{t+1}$ is seen.

**Cost.** $\sum_{t=1}^{m} d(s_{t-1}, s_t)$.

**Competitive ratio.** A deterministic algorithm is $c$-competitive for width $k$ if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for every metric space and every $\sigma$ of width at most $k$, with $b$ independent of $\sigma$. For randomized algorithms the expected cost replaces ALG, against an [oblivious adversary](/oblivious-adversary/).

**Work function.** $w_0(x) = d(s_0, x)$ and $w_t(x) = \min_{y \in R_t} \big( w_{t-1}(y) + d(y, x) \big)$. Then $\mathrm{OPT}(\sigma) = \min_{y \in R_m} w_m(y)$. This is the [work function](/work-function/) of the MTS with costs $r_t(y) = 0$ for $y \in R_t$ and $\infty$ otherwise.

## Variants

- **Layered graph traversal.** A searcher walks in an unknown weighted graph whose vertices are in layers $L_0, L_1, \ldots$, with edges only between consecutive layers. When it reaches layer $t$, it sees layer $t + 1$ and the edges to it, and it must reach a vertex of the last layer. The width is the largest layer size. Fiat et al. proved that it is equivalent to MSS of the same width, up to a constant factor.
- **Width 2 and the cow path.** With two points per request on a line and one of the two sides always far, MSS of width $2$ contains the [linear search problem](/linear-search-problem/). Its deterministic ratio is $9$.
- **Uniform metric.** All distances are $1$. The problem behaves like paging, with ratio $k$ for deterministic algorithms and $H_k$ for randomized ones.
- **Metrical task systems.** MTS allows any costs. MSS keeps only the feasibility part, and the bounds are in terms of $k$ instead of the number $n$ of points.

## Examples

**Greedy is not competitive.** On the line, start at $0$, and let the requests alternate between $\{1, 10\}$ and $\{-1, 10\}$. The greedy rule moves to the nearest allowed point. It goes to $1$, then to $-1$, then to $1$, and so on, and after $m$ requests it has paid $2m - 1$. The optimum goes once to $10$ and pays $10$. So greedy has no finite ratio, even for width $2$.

**The work function algorithm on the same input.** The work function on the points $-1, 0, 1, 10$:

| $t$ | $R_t$ | $w_t(-1)$ | $w_t(0)$ | $w_t(1)$ | $w_t(10)$ | WFA at | WFA cost | OPT |
|---|---|---|---|---|---|---|---|---|
| 1 | $\{1, 10\}$ | 3 | 2 | 1 | 10 | 1 | 1 | 1 |
| 2 | $\{-1, 10\}$ | 3 | 4 | 5 | 10 | $-1$ | 3 | 3 |
| 3 | $\{1, 10\}$ | 7 | 6 | 5 | 10 | 1 | 5 | 5 |
| 4 | $\{-1, 10\}$ | 7 | 8 | 9 | 10 | $-1$ | 7 | 7 |
| 5 | $\{1, 10\}$ | 11 | 10 | 9 | 10 | 1 | 9 | 9 |
| 6 | $\{-1, 10\}$ | 11 | 12 | 13 | 10 | $-1$ | 11 | 10 |
| 7 | $\{1, 10\}$ | 15 | 14 | 13 | 10 | 1 | 13 | 10 |
| 8 | $\{-1, 10\}$ | 15 | 16 | 17 | 10 | $-1$ | 15 | 10 |
| 9 | $\{1, 10\}$ | 19 | 18 | 17 | 10 | 1 | 17 | 10 |
| 10 | $\{-1, 10\}$ | 19 | 20 | 19 | 10 | 10 | 26 | 10 |

At step $10$ the algorithm compares $w_{10}(-1) + d(1, -1) = 21$ with $w_{10}(10) + d(1, 10) = 19$, and it moves to $10$. After that it pays nothing. Its cost $26$ against $\mathrm{OPT} = 10$ is the familiar pattern: it pays about the distance in small moves, and then the distance once more.

**k-server on k + 1 points.** With $k$ servers on $k + 1$ points, a configuration is given by the one point with no server. A request at point $r$ allows exactly the $k$ configurations whose empty point is not $r$. So this k-server problem is an MSS of width $k$ on the configurations, with the induced distance between configurations.

## Known algorithms

- **Work function algorithm.** Move to a point $y \in R_t$ that minimizes $w_t(y) + d(s_{t-1}, y)$. Burley (1996) proved that a version of it is $O(k \cdot 2^k)$-competitive.
- **Doubling search.** For width $2$, the doubling strategy of the [linear search problem](/linear-search-problem/), applied to the two candidate paths, is $9$-competitive, which is optimal.
- **Recursive strategies.** Fiat et al. (1998) gave an $O(9^k)$-competitive deterministic algorithm, by recursion on the width.
- **Entropic mirror descent.** Bubeck, Coester and Rabani (2022) gave a randomized algorithm for layered graph traversal of width $k$ with ratio $O(k^2)$ against an oblivious adversary. It keeps a probability distribution over the current layer and updates it by mirror descent with an entropy regularizer.

## Bounds

| Setting | Lower bound | Upper bound |
|---|---|---|
| deterministic, width 2 | 9 | 9 (Chrobak and Larmore; Papadimitriou and Yannakakis) |
| deterministic, width $k$ | $\Omega(2^k)$ (Fiat et al. 1998) | $O(9^k)$ (Fiat et al. 1998); $O(k\,2^k)$ (Burley 1996) |
| randomized, oblivious, width $k$ | $\Omega(k^2 / \log^{1 + \epsilon} k)$ (Ramesh 1995); $\Omega(k^2)$ (Bubeck, Coester and Rabani 2023) | $O(k^{13})$ (Ramesh 1995); $O(k^2)$ (Bubeck, Coester and Rabani 2022) |
| uniform metric, width $k$ | $k$ deterministic, $H_k$ randomized | $k$ deterministic, $H_k$ randomized |

So the randomized ratio of MSS of width $k$ is $\Theta(k^2)$. The deterministic ratio is $2^{\Theta(k)}$, and the exact base of the exponent is the main open question. A 2026 preprint by Coester claims a deterministic $O(2^k)$ bound, which would close the gap up to a constant factor.

The lower bound $9$ for width $2$ comes from the [linear search problem](/linear-search-problem/). Take two rays from the start point. Request $t$ offers the two points at distance $t \varepsilon$ on the two rays, so the server must stand on one ray, as far out as the request. When the server has committed to one ray, the adversary ends that ray: from then on, the requests offer only points of the other ray. The lower bounds for the uniform metric are those of [paging](/paging-problem/) with a cache of $k$ pages, because width-$k$ requests on $k + 1$ uniform points are paging requests. Chrobak and Larmore gave matching upper bounds.

## Reductions

- **To and from MTS.** An MSS is an MTS with costs in $\{0, \infty\}$. The MTS bound $2n - 1$ is stated for finite costs and the number $n$ of states, while MSS bounds use only the width.
- **From k-server.** The k-server problem on $k + 1$ points reduces to MSS of width $k$, as in the example. So a better MSS bound for some width gives the same bound for k-server on $k + 1$ points.
- **Layered graph traversal.** Each MSS of width $k$ can be turned into a layered graph traversal of width $k$, and back, at the cost of a constant factor in the ratio (Fiat et al. 1998). Most algorithms are stated for layered graphs.
- **From search problems.** The [linear search problem](/linear-search-problem/) and its version with $m$ rays are special cases of width $2$ and $m$.

## Applications

- **Navigation without a map.** A robot that must reach a goal and sees only the next part of the terrain solves a layered graph traversal problem. This was the motivation of Papadimitriou and Yannakakis.
- **Server problems.** The reduction from k-server on $k + 1$ points made MSS the first tool for small server problems.
- **Lower bounds.** The randomized lower bound $\Omega(k^2)$ for MSS was a step to the proof by Bubeck, Coester and Rabani that the randomized k-server conjecture is false.

## References
