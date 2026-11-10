---
tag: NC4YZN
kind: problem
slug: k-server-problem
name: k-server problem
aliases:
- k-server
- k-server problem on metric spaces
area: online-and-streaming/paging-and-caching-online
level: advanced
summary: Move k servers in a metric space to satisfy a sequence of requests at points, minimizing total movement.
prereqs: [competitive-ratio, online-algorithm, offline-optimum, paging-problem]
see_also: [k-server-conjecture, double-coverage, work-function-algorithm, weighted-paging-problem, metrical-task-systems, metrical-service-systems, page-migration-problem, sleator-tarjan-paging-bound]
sources:
  - paper: doi:10.1016/0196-6774(90)90003-W
    title: Mark S. Manasse, Lyle A. McGeoch and Daniel D. Sleator, Competitive algorithms for server problems, Journal of Algorithms 11(2), 1990, 208-230
    locator: the definition of the k-server problem, the lower bound k for each deterministic algorithm on each metric space with at least k + 1 points, the k-competitive algorithms for k = 2 and for k + 1 points, and the conjecture
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 10 (the k-server problem, lazy algorithms, the lower bound k, double coverage on trees) and Chapter 11 (randomized k-server algorithms)
  - paper: doi:10.1016/j.cosrev.2009.04.002
    title: Elias Koutsoupias, The k-server problem, Computer Science Review 3(2), 2009, 105-118
    locator: the survey of the deterministic and randomized results, the work function algorithm, and the open problems
  - paper: doi:10.1145/210118.210128
    title: Elias Koutsoupias and Christos H. Papadimitriou, On the k-server conjecture, Journal of the ACM 42(5), 1995, 971-983
    locator: the bound 2k - 1 for the work function algorithm on every metric space
  - paper: doi:10.1137/0404017
    title: Marek Chrobak, Howard J. Karloff, Tom Payne and Sundar Vishwanathan, New results on server problems, SIAM Journal on Discrete Mathematics 4(2), 1991, 172-181
    locator: the double coverage algorithm and its bound k on the line
  - paper: doi:10.1145/3564246.3585132
    title: Sébastien Bubeck, Christian Coester and Yuval Rabani, The randomized k-server conjecture is false!, Proceedings of STOC 2023
    locator: the lower bound Ω(log^2 k) for randomized algorithms on some metric spaces; arXiv:2211.05753
---

The $k$-server problem asks how to move $k$ servers in a metric space so that each request, a point of the space, is covered by a server when it arrives, with the least total distance moved. Manasse, McGeoch and Sleator defined it in 1988 (journal version 1990) as a common model for [paging](/paging-problem/), for moving disk heads, and for many other online problems. Each deterministic online algorithm has a competitive ratio of at least $k$ on each metric space with more than $k$ points. The best known general upper bound is $2k - 1$, by the [work function algorithm](/work-function-algorithm/), and the [k-server conjecture](/k-server-conjecture/) says that $k$ is always possible.

## In plain words

Think of $k$ repair trucks in a city. Calls come in one at a time, each from some place in the city, and a truck must drive there before the next call. Which truck should go? The closest truck seems the obvious choice, but it can be a bad one: if calls jump between two close places, the same truck drives back and forth for ever, while a second truck could have come over once and stayed.

The company does not know the future calls. It wants a rule whose total driving is never more than some fixed factor times the driving of the best plan made with full knowledge of the calls. The $k$-server problem asks how small that factor can be.

## Definition

**Input.** A metric space $(M, d)$, a number $k \ge 1$, a start configuration $C_0$, which is a multiset of $k$ points of $M$, and a request sequence $\sigma = r_1, r_2, \ldots, r_n$ of points of $M$.

**Moves.** A configuration is a multiset of $k$ points, the positions of the servers. Before request $r_t$ is served, the algorithm moves from $C_{t-1}$ to a configuration $C_t$ with $r_t \in C_t$. The cost of a move from $C$ to $C'$ is the cost of a minimum matching between them, $\min_{\text{bijections } \pi} \sum_{x \in C} d(x, \pi(x))$.

**Online and offline.** An online algorithm chooses $C_t$ from $C_0, r_1, \ldots, r_t$ only. The offline optimum $\mathrm{OPT}(\sigma)$ is the least total cost over all valid sequences of configurations. An algorithm $A$ is $c$-competitive if there is a constant $b$ with $A(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$, where $b$ may depend on $M$, $k$ and $C_0$ but not on $\sigma$. For a randomized algorithm, $A(\sigma)$ is replaced by its expected cost against an [oblivious adversary](/oblivious-adversary/).

**Lazy algorithms.** An algorithm is *lazy* if it moves only when the request is not covered, and then moves one server, to the request. By the triangle inequality, every algorithm can be made lazy with no extra cost, as shown in the Bounds section.

## Variants

- **Paging.** The uniform metric, with $d(p, q) = 1$ for all distinct points, is the [paging problem](/paging-problem/): the points are the pages, the servers are the $k$ slots of the cache, and moving a server from $p$ to $q$ is the eviction of $p$ to load $q$. A lazy algorithm pays $1$ for each miss.
- **Weighted paging.** A star metric, with a center and a leaf for each page at distance $w_p / 2$, models the [weighted paging problem](/weighted-paging-problem/), where loading page $p$ costs $w_p$. The two costs differ by at most a constant.
- **The line and trees.** For points on a line or in a tree metric, [double coverage](/double-coverage/) is $k$-competitive.
- **Randomized $k$-server.** The algorithm may use random bits, and the cost is an expectation against an oblivious adversary.
- **Weighted $k$-server.** Each server has its own cost for each unit of distance. This problem is much harder: even on uniform metrics, the best deterministic ratio grows doubly exponentially in $k$ (Fiat and Ricklin 1994; Bansal, Eliáš and Koumoutsos 2017).
- **Generalizations.** [Metrical task systems](/metrical-task-systems/) allow any cost function for each request and any number of states; the $k$-server problem is the special case with the configurations as states. [Metrical service systems](/metrical-service-systems/) ask for a point in a given set, and the [page migration problem](/page-migration-problem/) moves one copy of a page in a network.

## Examples

**Paging as a special case.** Take the uniform metric on the pages $a, b, c$, with $k = 2$ servers at $a$ and $b$. The requests $c, a, c$ cost a lazy algorithm one move for each request not covered. If $a$ was used before $b$, LRU moves the server at $a$ to $c$ (cost $1$), then the server at $b$ to $a$ (cost $1$), and then $c$ is covered, so the total cost is $2$, the same as the number of misses of LRU with $2$ slots.

**The greedy rule is not competitive.** Greedy sends the closest server. On the real line with servers at $0$ and $10$, request $11$ and $10$ again and again, $m$ requests in total.

| request | greedy moves | greedy servers | greedy cost so far |
|---|---|---|---|
| 11 | the server at 10 | 0, 11 | 1 |
| 10 | the server at 11 | 0, 10 | 2 |
| 11 | the server at 10 | 0, 11 | 3 |
| 10 | the server at 11 | 0, 10 | 4 |

Greedy pays $1$ for each request, so $m$ in total, and the server at $0$ never moves. The optimum moves the server at $0$ to $10$ and the other server to $11$, for a cost of $11$, and then both points are covered. In fact $\mathrm{OPT} = \min(m, 11)$: in a schedule where the server from $0$ never reaches $10$ or $11$, the other server serves all requests and pays at least $1$ for each one, and in any other schedule the server from $0$ pays at least $10$, and at least $1$ more is paid to cover the other point. So the ratio of greedy is at least $m / 11$, which has no bound. A script checked the costs $10, 11, 12, 20$ of greedy and $10, 11, 11, 11$ of the optimum for $m = 10, 11, 12, 20$. Double coverage pays $30$ for $m = 20$, which is within its bound $2 \cdot 11 + b$.

**The adversary of the lower bound.** On the points $0, 1, 3$ with $k = 2$ servers at $0$ and $1$, the adversary always requests the one point that greedy does not cover. The requests are $3, 1, 0, 1, 0, \ldots$, and after $n$ requests greedy has paid $n + 1$, while the optimum pays $4$ for $n = 9$, $30$ and $99$, the values that a script checked. Against any deterministic algorithm, this adversary forces a cost of at least $k \cdot \mathrm{OPT}$ minus a constant, as the proof below shows.

## Known algorithms

- **[Work function algorithm](/work-function-algorithm/).** Koutsoupias and Papadimitriou (1995) proved that it is $(2k - 1)$-competitive on every metric space. It is $k$-competitive for $k = 2$, for metrics with $k + 1$ or $k + 2$ points, on the line, and on weighted stars. Its cost for each request can be exponential in $k$.
- **[Double coverage](/double-coverage/).** $k$-competitive on the line (Chrobak, Karloff, Payne and Vishwanathan 1991) and on trees (Chrobak and Larmore 1991). It is not lazy, and it is fast.
- **LRU, FIFO and the marking algorithms.** On the uniform metric they are $k$-competitive ([Sleator and Tarjan 1985](/sleator-tarjan-paging-bound/)), which matches the lower bound.
- **Algorithms for $k = 2$ and $k + 1$ points.** Manasse, McGeoch and Sleator gave $k$-competitive algorithms for these cases in the paper that defined the problem.
- **Randomized algorithms.** On the uniform metric, [randomized marking](/randomized-marking/) is $(2H_k - 1)$-competitive, and the optimum ratio there is $H_k$. On general metrics, Bansal, Buchbinder, Madry and Naor (2011) gave the first algorithm with a ratio that is polylogarithmic in $k$ and in the number of points.

## Bounds

**Theorem 1 (laziness costs nothing).** For each online algorithm $A$ there is a lazy online algorithm $A'$ with $A'(\sigma) \le A(\sigma)$ for all $\sigma$. If $A$ is deterministic, so is $A'$.

*Proof.* $A'$ runs $A$ in the background. Number the servers $1, \ldots, k$ for both, so that server $i$ of $A'$ starts where server $i$ of $A$ starts. Let $a_i$ and $a'_i$ be the positions, and let $\Phi = \sum_i d(a'_i, a_i)$, which is $0$ at the start. On a request $r$, first let $A$ move. By the triangle inequality, $\Phi$ grows by at most the cost that $A$ pays. If $A'$ already has a server at $r$, it does nothing. Else let $j$ be a server of $A$ at $r$; $A'$ moves its server $j$ to $r$, which costs $d(a'_j, r) = d(a'_j, a_j)$, and the term $j$ of $\Phi$ becomes $0$. So $\Phi$ falls by at least what $A'$ pays. In each step, the cost of $A'$ plus the change of $\Phi$ is at most the cost of $A$. Summing over all steps, $A'(\sigma) + \Phi_{end} \le A(\sigma)$, and $\Phi_{end} \ge 0$. $A'$ uses only the moves of $A$, so it is online. $\square$

**Theorem 2 (Manasse, McGeoch and Sleator 1990).** Let $M$ have at least $k + 1$ points and let the $k$ servers start on $k$ distinct points. Then no deterministic online algorithm is $c$-competitive for any $c < k$.

*Proof.* Let $A$ be a deterministic online algorithm. By Theorem 1 it is enough to prove the bound for a lazy one, since a lazy version costs at most as much on each sequence. So let $A$ be lazy. Let $S = C_0 \cup \{p\}$ for a point $p \notin C_0$, so $|S| = k + 1$. Let $D$ be the largest distance and $\delta > 0$ the smallest distance between two points of $S$.

*The sequence.* A lazy algorithm keeps its servers on $S$, on $k$ distinct points. So before each request there is exactly one point of $S$ that $A$ does not cover, the *hole*. The adversary requests the hole each time: $r_1, r_2, \ldots, r_n$. Then $A$ moves a server from some point $x_t$ to $r_t$, and the new hole is $x_t = r_{t+1}$. So the cost of $A$ for request $t$ is $d(r_{t+1}, r_t)$, with $r_{n+1}$ the hole after the last request, and

$$A(\sigma) = \sum_{t=1}^{n} d(r_t, r_{t+1}) \ge \sum_{t=2}^{n} d(r_{t-1}, r_t).$$

Since $r_{t+1} \ne r_t$, also $A(\sigma) \ge n \delta$.

*Offline algorithms.* Pick a point $r_0 \in S$ with $r_0 \ne r_1$. For each $y \in S \setminus \{r_0\}$, define an offline algorithm $B_y$. It first moves to the configuration $S \setminus \{y\}$: since $C_0 = S \setminus \{r_1\}$, this moves at most one server, from $y$ to $r_1$, for a cost of at most $D$. These $k$ algorithms have $k$ distinct holes, the points of $S \setminus \{r_0\}$, and all of them cover $r_0$.

*Invariant.* Before request $t$, the holes of the $k$ algorithms are exactly the points of $S \setminus \{r_{t-1}\}$, one hole each. This holds for $t = 1$. Request $r_t$ differs from $r_{t-1}$, so exactly one algorithm $B$ has its hole at $r_t$, and all the others cover $r_t$ and do not move. $B$ moves its server from $r_{t-1}$, which all of them cover, to $r_t$, for a cost of $d(r_{t-1}, r_t)$. Its new hole is $r_{t-1}$, so the holes are now the points of $S \setminus \{r_t\}$, and the invariant holds before request $t + 1$.

*Counting.* The total cost of the $k$ algorithms is at most

$$kD + \sum_{t=1}^{n} d(r_{t-1}, r_t) \le kD + D + A(\sigma).$$

The cheapest of them costs at most the average, so $\mathrm{OPT}(\sigma) \le (A(\sigma) + (k + 1) D) / k$, that is,

$$A(\sigma) \ge k \cdot \mathrm{OPT}(\sigma) - (k + 1) D.$$

*Conclusion.* Assume that $A(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$ with $c < k$. Then $(k - c) \mathrm{OPT}(\sigma) \le b + (k + 1) D$, so $\mathrm{OPT}$ is bounded on the sequences of the adversary. But then $n \delta \le A(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ is bounded too, which fails for large $n$. $\blacksquare$

On the uniform metric it gives the paging lower bound $k$ of Sleator and Tarjan.

**Other bounds.**

| setting | lower bound | upper bound |
|---|---|---|
| deterministic, every metric with more than $k$ points | $k$ (MMS 1990) | $2k - 1$ (WFA, Koutsoupias and Papadimitriou 1995) |
| deterministic, $k = 2$, or $k + 1$ points | $k$ | $k$ (MMS 1990) |
| deterministic, line and trees | $k$ | $k$ (double coverage) |
| deterministic, uniform metric (paging) | $k$ | $k$ (LRU, FIFO, marking) |
| randomized, uniform metric | $H_k$ | $H_k$ (McGeoch and Sleator 1991; Achlioptas, Chrobak and Noga 2000) |
| randomized, every metric with more than $k$ points | $\Omega(\log k / \log \log k)$ (Bartal, Bollobás and Mendel; Bartal, Linial, Mendel and Naor) | polylogarithmic in $k$ and the number of points (Bansal, Buchbinder, Madry and Naor 2011) |
| randomized, some metrics | $\Omega(\log^2 k)$ (Bubeck, Coester and Rabani 2023) | |

The last row refutes the randomized $k$-server conjecture, which said that $O(\log k)$ is possible on every metric. The [k-server conjecture](/k-server-conjecture/) page gives the history of both conjectures.

**The offline optimum.** $\mathrm{OPT}(\sigma)$ can be computed in polynomial time, as a minimum-cost flow with one unit for each server (Chrobak, Karloff, Payne and Vishwanathan 1991). It is also the value of the work function at the end of the sequence.

## Reductions

- **From paging.** Paging is the $k$-server problem on the uniform metric, so each $k$-server bound is a paging bound and each paging lower bound applies to $k$-server.
- **From weighted paging.** Weighted paging is $k$-server on a weighted star, up to an additive constant.
- **To metrical task systems.** A $k$-server instance on $n$ points is a metrical task system with $\binom{n + k - 1}{k}$ states. The work function algorithm comes from this view.
- **Lazy normal form.** By Theorem 1, every analysis can assume lazy algorithms, but some good algorithms, such as double coverage, are easier to describe when they are not lazy.

## Applications

- **Caching and paging.** The uniform and weighted stars model caches with equal and unequal fetch costs.
- **Moving heads and vehicles.** Disk heads on a line, robots or vehicles in a network, and service crews are the motivating examples of the original paper.
- **A test bed for online algorithms.** The problem drove the development of work functions, potential functions for online algorithms, and the use of tree embeddings and mirror descent in randomized online algorithms.

## References
