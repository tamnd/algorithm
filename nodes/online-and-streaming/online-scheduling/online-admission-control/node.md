---
tag: WECXX0
kind: problem
slug: online-admission-control
name: Online admission control
aliases:
- online call admission
- throughput-competitive online routing
area: online-and-streaming/online-scheduling
level: advanced
summary: Requests arrive online and each must be accepted or rejected irrevocably, subject to resource capacity.
prereqs: [admission-control, online-algorithm, competitive-ratio]
see_also: [online-interval-scheduling, online-throughput-maximization, online-knapsack-problem, online-primal-dual, online-restricted-assignment-load-balancing, routing-problem, packet-scheduling, randomized-online-algorithm]
sources:
  - paper: doi:10.1109/SFCS.1993.366884
    title: Baruch Awerbuch, Yossi Azar and Serge Plotkin, Throughput-competitive on-line routing, FOCS 1993
    locator: pages 32 to 40 (the exponential cost function algorithm, the O(log mu) upper bound when each request uses a small fraction of each capacity, and the matching deterministic lower bound)
  - paper: "James Aspnes, Yossi Azar, Amos Fiat, Serge Plotkin and Orli Waarts, On-line routing of virtual circuits with applications to load balancing and machine scheduling, Journal of the ACM 44(3), 1997 (STOC 1993)"
    locator: pages 486 to 504 (the exponential cost function for the related problem of minimizing the maximum load)
  - paper: "Niv Buchbinder and Joseph Naor, Improved bounds for online routing and packing via a primal-dual approach, FOCS 2006"
    locator: the primal-dual analysis of the exponential update for online packing and routing
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 13 (call admission and circuit routing)
---

Online admission control is the problem in which requests for a share of a limited resource arrive one at a time, and an online algorithm must accept or reject each request at once, without knowing the later requests, so that the total profit of the accepted requests is large and no capacity is exceeded. The standard model is call admission in a network: a request asks for bandwidth along a path, and each edge has a capacity. The general concept is on the [admission control](/admission-control/) page. If a single request can use a large part of an edge, no deterministic algorithm has a good ratio. If each request is small compared with the capacities, the exponential cost function algorithm of Awerbuch, Azar and Plotkin (1993) is $O(\log \mu)$-competitive, with $\mu$ polynomial in the network size, and this is the best possible order for deterministic algorithms.

## In plain words

A network carries calls. Each call needs some bandwidth on each link of its route, and each link has a limited capacity. Calls come one at a time, and the network must say yes or no at once. An accepted call pays a profit.

If the network accepts everything while it can, a single call that uses many links may block many short calls that would pay more in total. If it is too careful, capacity stays unused. The good rule puts a price on each link that grows very fast as the link fills up. A call is accepted only if its profit is at least the price of the route. When a link is almost empty, the price is low, so the network accepts most calls. When a link is almost full, the price is high, so only valuable calls get the last capacity.

## Definition

**Input.** A graph $G = (V, E)$ with $|V| = n$ and a capacity $u(e) > 0$ for each edge. A sequence $\sigma$ of requests, revealed one at a time. Request $j$ gives a source $s_j$, a target $t_j$, a bandwidth $b_j > 0$ and a profit $\rho_j > 0$. In the model with durations, it also gives a start time and an end time.

**Decisions.** When request $j$ arrives, the algorithm either rejects it or accepts it and chooses an $s_j$ to $t_j$ path $P_j$. The decision is final. For each edge $e$, the total bandwidth of the accepted requests that use $e$ at the same time must be at most $u(e)$.

**Objective.** Maximize the total profit $\sum_{j \text{ accepted}} \rho_j$. In the model with durations, the profit is often bandwidth times duration.

**Notation.** ALG$(\sigma)$ and OPT$(\sigma)$ are the profit of the online algorithm and of the best offline set of accepted requests and paths. For this maximization problem, an algorithm is $c$-competitive if OPT$(\sigma) \le c \cdot$ ALG$(\sigma)$ for each $\sigma$, with additive constant $b = 0$. For a [randomized](/randomized-online-algorithm/) algorithm, OPT$(\sigma) \le c \cdot \mathbb{E}[\text{ALG}(\sigma)]$ against an [oblivious adversary](/oblivious-adversary/).

## Variants

- **Small or large requests.** In the small request case, $b_j \le u(e) / \log_2 \mu$ for each edge $e$. In the unit capacity case, $u(e) = b_j = 1$, so each request takes a whole edge.
- **Fixed paths.** The path of each request is given, and the only choice is to accept or reject. On a line, a request is an interval of edges, so this is close to [online interval scheduling](/online-interval-scheduling/), but the intervals arrive in any order.
- **Permanent or temporary requests.** A permanent request keeps its bandwidth forever. A temporary one leaves at its end time, which may or may not be known at arrival.
- **Preemption.** In some models an accepted request may be dropped later, with loss of its profit.
- **One edge.** With a single edge, admission control is the [online knapsack problem](/online-knapsack-problem/).
- **The load version.** Accept every request and minimize the largest ratio of load to capacity. This is online routing for congestion, close to [online load balancing with restricted assignment](/online-restricted-assignment-load-balancing/), and the exponential cost function also solves it (Aspnes, Azar, Fiat, Plotkin and Waarts).

## Examples

**The trap for large requests.** Take a line with 3 edges, capacity 1 on each edge, and unit bandwidth and unit profit for each request. The first request asks for the whole line, and then one request asks for each edge. An algorithm that accepts each request it can fit accepts the first one and must reject the other three, for a profit of 1. The optimum rejects the first request and accepts the other three, for a profit of 3.

**The exponential price on one edge.** Take one edge with $u = 4$, requests with $b_j = 1$, and the parameter $\mu = 8$. The price of the edge at load fraction $\lambda$ is $u (\mu^{\lambda} - 1)$, and a request pays its share $b_j / u$ of it, which is $8^{\lambda} - 1$. So a request is accepted if its profit is at least $8^{\lambda} - 1$.

| load before the request | price $8^{\lambda} - 1$ | accepted if $\rho_j = 1$ | if $\rho_j = 2$ | if $\rho_j = 4$ |
|---|---|---|---|---|
| $\lambda = 0$ | 0 | yes | yes | yes |
| $\lambda = 1/4$ | about 0.68 | yes | yes | yes |
| $\lambda = 1/2$ | about 1.83 | no | yes | yes |
| $\lambda = 3/4$ | about 3.76 | no | no | yes |

Requests with profit 1 can fill at most half the edge, and the last quarter is kept for requests with profit at least about 3.76.

## Known algorithms

**Greedy.** Accept each request if some path has room for it. With unit capacities this has no bounded ratio, as the first example shows on a line with $n$ edges, where the ratio is $n$.

**Exponential cost function (Awerbuch, Azar and Plotkin 1993).** Let $\lambda_e$ be the fraction of $u(e)$ in use on edge $e$ when request $j$ arrives, and let the cost of $e$ be $c_e = u(e) \left( \mu^{\lambda_e} - 1 \right)$. Find a path $P$ from $s_j$ to $t_j$ that minimizes $\sum_{e \in P} \frac{b_j}{u(e)} c_e$, with a shortest path algorithm. Accept $j$ on $P$ if this sum is at most $\rho_j$, and reject it otherwise. The parameter $\mu$ depends on $n$ and on the range of the profits and the durations; for permanent requests with bounded profit ratios it is $O(n)$.

The analysis has three steps. First, the cost of an edge reaches $u(e)(\mu - 1)$ only when it is full, and a request is accepted only if its profit pays for its share, so a request with small bandwidth never finds a full edge cheap enough. So the capacities are never exceeded. Second, each accepted request increases the total cost $\sum_e c_e$ by at most $O(\log \mu)$ times its profit, so the final total cost is $O(\log \mu) \cdot$ ALG. Third, each request that the optimum accepts and the algorithm rejects found every path too expensive, so the profit that the algorithm misses is at most the final total cost. Together, OPT $= O(\log \mu) \cdot$ ALG. This result is cited here, and these steps are only a sketch of the proof.

**Primal-dual view (Buchbinder and Naor 2006).** The edge costs are the dual variables of the linear program of the problem, and the exponential update is the online primal-dual rule for packing problems. See [online primal-dual](/online-primal-dual/).

## Bounds

**Theorem.** With unit capacities and fixed paths on a line with $n$ edges, no deterministic algorithm is better than $n$-competitive for unit profits.

*Proof.* The adversary first asks for the whole line. If the algorithm rejects it, the sequence ends, ALG $= 0$ and OPT $= 1$. If it accepts, each edge is full, and the adversary asks for each single edge; the algorithm must reject them all. Then ALG $= 1$ and OPT $= n$. $\square$

| model | bound | proved here or cited |
|---|---|---|
| unit capacity, deterministic, line | $n$, no better | proved above |
| small requests, deterministic | $O(\log \mu)$ with exponential costs | cited, Awerbuch, Azar and Plotkin |
| small requests, deterministic, lower | $\Omega(\log \mu)$ | cited, Awerbuch, Azar and Plotkin |
| one edge | see [online knapsack](/online-knapsack-problem/) | linked |

So the small request assumption is the price of a logarithmic ratio. It holds in large networks where each call is a small part of a link. Without it, randomization helps on special graphs such as lines and trees, but the deterministic lower bound above stays.

## Reductions

- **To online interval scheduling.** On a line with fixed paths and unit capacity, each request is an interval of edges. If the requests arrive in order of their left ends, the problem is [online interval scheduling](/online-interval-scheduling/) without abort.
- **To online knapsack.** With one edge, the only constraint is the capacity of that edge.
- **To online packing.** Each request is a column of a packing linear program with one row per edge, and the online algorithm must set the variable of each column when it arrives. The exponential cost is the dual update.

## Applications

Admission of calls and virtual circuits in telephone and ATM networks; reservation of bandwidth for video streams; allocation of capacity in cloud systems and in advertising budgets; and any system that sells a limited resource to customers who come one at a time.

## References
