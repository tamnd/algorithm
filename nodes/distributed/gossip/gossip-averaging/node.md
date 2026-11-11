---
tag: ZSVD30
kind: algorithm
slug: gossip-averaging
name: Randomized gossip averaging
aliases:
- Boyd et al. randomized gossip
- pairwise gossip averaging
area: distributed/gossip
level: advanced
summary: At each clock tick a random node and one random neighbour replace their values by the mean of the two; all values converge to the global average.
solves: [distributed-averaging]
model: asynchronous-model
complexity:
  vars: {n: the number of nodes, ε: the target relative error, λ: the second largest eigenvalue of the expected matrix W-bar}
  time: {ticks: Θ(log(1/ε) / log(1/λ))}
  space: {extra: O(1)}
properties: {deterministic: false, recursive: false}
prereqs: [distributed-averaging, spectral-gap, transition-matrix]
see_also: [averaging-convergence-spectral-gap, push-sum, gossip-aggregation, push-pull-gossip, gossip-protocol, mixing-time, random-geometric-graph]
sources:
  - paper: doi:10.1109/TIT.2006.874516
    title: Stephen Boyd, Arpita Ghosh, Balaji Prabhakar and Devavrat Shah, Randomized gossip algorithms, IEEE Transactions on Information Theory 52(6), 2006
    locator: pages 2508 to 2530; Section II (the asynchronous time model, Lemma 1 on ticks and absolute time, Definition 1 of the averaging time), Theorem 3 (the averaging time in terms of lambda_2 of W-bar), Section IV (optimizing P as a semidefinite program and a distributed subgradient method)
  - paper: doi:10.1016/j.sysconle.2004.02.022
    title: Lin Xiao and Stephen Boyd, Fast linear iterations for distributed averaging, Systems and Control Letters 53(1), 2004
    locator: pages 65 to 78 (the synchronous linear iteration that randomized gossip replaces)
  - paper: "Alexandros G. Dimakis, Anand D. Sarwate and Martin J. Wainwright, Geographic gossip: efficient averaging for sensor networks, IEEE Transactions on Signal Processing 56(3), 2008"
    locator: pages 1205 to 1216 (the cost of standard gossip on random geometric graphs and the geographic routing variant)
---

Randomized gossip averaging, from Boyd, Ghosh, Prabhakar and Shah (2006), solves [distributed averaging](/distributed-averaging/) with no global clock: at each tick of a random node's clock, that node and one neighbour chosen with a fixed probability replace both their values by the mean of the two. The sum of the values never changes, and the error shrinks in expectation by a factor $\lambda_2(\bar W)$ per tick, where $\bar W$ is the expected averaging matrix. Boyd et al. show that this one number sets the averaging time up to a constant factor. It differs from the synchronous [linear iteration](/distributed-averaging/) in that only two nodes act at a time, from [push-sum](/push-sum/) in that the exchange is two way and atomic, and from [gossip aggregation](/gossip-aggregation/) in that it runs on a fixed graph with no restarts.

## In plain words

Every computer in a network holds a number, and they want the average. Each computer has its own timer that rings at random moments. When a computer's timer rings, it calls one of its neighbours at random. The two compare numbers and both keep the midpoint.

The total of all numbers stays the same after each call, because one number goes up exactly as much as the other goes down. So the average never moves, and the numbers can only get closer to it. After enough calls, all numbers are close to the average.

On a network where everyone can call everyone, this is fast. On a ring, a value from one side needs many calls to cross to the other side, so it is much slower. One property of the network, its spectral gap, tells how slow.

## The problem

The network is a connected undirected graph $G = (V, E)$ with $n$ nodes. Node $i$ holds $x_i(0) \in \mathbb{R}$, and every node must approach $\bar x = \frac1n \sum_i x_i(0)$.

**Time model.** Each node has a clock that ticks at the times of a rate 1 Poisson process, independent of the other clocks. The ticks of all clocks together form one Poisson process of rate $n$, so the $k$-th tick belongs to a uniform random node, independent of the past. Boyd et al. count time in these global ticks; by their Lemma 1, $k$ ticks take about $k/n$ units of absolute time. A tick starts one exchange between two neighbours, which runs as an atomic step. There are no failures and no message loss in the analysis.

**Choice of partner.** A matrix $P$ with $P_{ij} \ge 0$, $P_{ij} > 0$ only if $\{i, j\} \in E$, and $\sum_j P_{ij} = 1$ gives the probability that node $i$ calls node $j$. The natural choice is $P_{ij} = 1/d_i$ for each neighbour $j$.

## The algorithm

```pseudo id=main
GOSSIP-AVERAGE(G, P, x)                     ▷ x_i is held by node i
L1  loop
L2      wait for the next clock tick; let i be the node whose clock ticked
L3      choose a neighbour j of i with probability P_ij
L4      i sends x_i to j and j sends x_j to i
L5      m ← (x_i + x_j) / 2
L6      x_i ← m; x_j ← m
```

In matrix form, tick $k$ applies $x(k+1) = W(k)\, x(k)$, where $W(k) = W_{ij} = I - \frac12 (e_i - e_j)(e_i - e_j)^T$ with probability $P_{ij}/n$. The expected matrix is

$$\bar W = \mathbb{E}[W(k)] = I - \frac{1}{2n} D + \frac{P + P^T}{2n}, \qquad D = \mathrm{diag}\Big(\sum_j (P_{ij} + P_{ji})\Big).$$

It equals $I - L/(2n)$, where $L$ is the [Laplacian](/laplacian-matrix/) of the graph with edge weights $P_{ij} + P_{ji}$. It is symmetric, $\bar W \mathbf 1 = \mathbf 1$, and its eigenvalues are $1 = \lambda_1(\bar W) \ge \lambda_2(\bar W) \ge \dots \ge \lambda_n(\bar W) \ge 0$.

**Averaging time.** Boyd et al. (Definition 1) define the $\varepsilon$-averaging time as

$$T_{\mathrm{ave}}(\varepsilon, P) = \sup_{x(0) \ne 0} \inf\Big\{ k : \Pr\Big( \frac{\lVert x(k) - \bar x \mathbf 1 \rVert}{\lVert x(0) \rVert} \ge \varepsilon \Big) \le \varepsilon \Big\}.$$

**Theorem 3 (Boyd, Ghosh, Prabhakar and Shah 2006).** The averaging time in ticks satisfies

$$\frac{0.5 \log \varepsilon^{-1}}{\log \lambda_2(\bar W)^{-1}} \;\le\; T_{\mathrm{ave}}(\varepsilon, P) \;\le\; \frac{3 \log \varepsilon^{-1}}{\log \lambda_2(\bar W)^{-1}}.$$

## Example

Take the cycle $1 - 2 - 3 - 4 - 1$ with $x(0) = (8, 0, 0, 0)$, so $\bar x = 2$. The error is $e = x - 2 \cdot \mathbf 1$.

| tick | caller $i$ | partner $j$ | $x$ after the tick | $\lVert e \rVert_2$ |
|---|---|---|---|---|
| 0 | | | (8, 0, 0, 0) | 6.93 |
| 1 | 3 | 4 | (8, 0, 0, 0) | 6.93 |
| 2 | 1 | 2 | (4, 4, 0, 0) | 4.00 |
| 3 | 2 | 3 | (4, 2, 2, 0) | 2.83 |
| 4 | 4 | 1 | (2, 2, 2, 2) | 0 |

Tick 1 is wasted: two equal values meet, and nothing changes. The sum stays 8 after every tick. This run hits the average exactly; a typical run only gets close. With $P_{ij} = \frac12$ on $C_4$, $\bar W = I - (I - P)/4$ and $\lambda_2(P) = \cos(\pi/2) = 0$, so $\lambda_2(\bar W) = \frac34$.

## Correctness

The full proof is below. It has four steps.

- **The sum is kept.** Lines L5 and L6 replace $x_i + x_j$ by $2m = x_i + x_j$. So $\mathbf 1^T x(k) = n \bar x$ for every $k$.
- **The error never grows.** Each $W_{ij}$ is the orthogonal projection onto the vectors with $x_i = x_j$, and $e(k+1) = W(k) e(k)$. A projection does not increase the norm.
- **Expected contraction.** Since $W_{ij}^T W_{ij} = W_{ij}$, $\mathbb{E}[\lVert e(k+1) \rVert^2 \mid e(k)] = e(k)^T \bar W e(k) \le \lambda_2(\bar W) \lVert e(k) \rVert^2$, because $e(k) \perp \mathbf 1$.
- **The upper bound.** So $\mathbb{E} \lVert e(k) \rVert^2 \le \lambda_2(\bar W)^k \lVert x(0) \rVert^2$, and by [Markov's inequality](/markov-inequality/) the error exceeds $\varepsilon \lVert x(0) \rVert$ with probability at most $\lambda_2(\bar W)^k / \varepsilon^2$. This is at most $\varepsilon$ once $k \ge 3 \log \varepsilon^{-1} / \log \lambda_2(\bar W)^{-1}$.

The values converge to $\bar x \mathbf 1$ with probability 1 if and only if $\lambda_2(\bar W) < 1$, that is, if and only if the graph of the edges with $P_{ij} + P_{ji} > 0$ is connected. The lower bound of Theorem 3 is proved in the paper.

## Complexity

Each tick costs two messages and $O(1)$ work at two nodes, and each node stores one number. The averaging time is in ticks; divide by $n$ for absolute time. For a symmetric $P$, $\bar W = I - (I - P)/n$, so $\lambda_2(\bar W) = 1 - (1 - \lambda_2(P))/n$ and $T_{\mathrm{ave}} = \Theta\big(n \log \varepsilon^{-1} / (1 - \lambda_2(P))\big)$ ticks: the averaging time is $n$ times the relaxation time of the random walk $P$. With the natural $P$:

| graph | $\lambda_2(P)$ | ticks $T_{\mathrm{ave}}$ | absolute time |
|---|---|---|---|
| [complete graph](/complete-graph/) $K_n$ | $-1/(n-1)$ | $\Theta(n \log \varepsilon^{-1})$ | $\Theta(\log \varepsilon^{-1})$ |
| cycle $C_n$ | $\cos(2\pi/n)$ | $\Theta(n^3 \log \varepsilon^{-1})$ | $\Theta(n^2 \log \varepsilon^{-1})$ |
| torus $\sqrt n \times \sqrt n$ | $(1 + \cos(2\pi/\sqrt n))/2$ | $\Theta(n^2 \log \varepsilon^{-1})$ | $\Theta(n \log \varepsilon^{-1})$ |

The [spectral gap theorem page](/averaging-convergence-spectral-gap/) works these out and adds the [random geometric graph](/random-geometric-graph/).

The table below gives, for $\varepsilon = 0.05$, the predicted value $\log \varepsilon^{-1} / \log \lambda_2(\bar W)^{-1}$ and the $0.95$ quantile of the number of ticks over 200 seeded runs that start on the slowest eigenvector (a spike on $K_n$). By Definition 1, this quantile is the averaging time for that input.

| graph | $n$ | prediction | 0.95 quantile | ratio |
|---|---|---|---|---|
| complete | 16 | 43.4 | 110 | 2.53 |
| complete | 64 | 187.2 | 448 | 2.39 |
| cycle | 16 | 628.2 | 693 | 1.10 |
| cycle | 32 | 4987.6 | 5179 | 1.04 |
| torus | 16 | 94.4 | 143 | 1.52 |
| torus | 64 | 1307.7 | 1481 | 1.13 |

All ratios are inside the window $[0.5, 3]$ of Theorem 3. Doubling $n$ on the cycle multiplies the time by about 8, and multiplying $n$ by 4 on the complete graph multiplies it by about 4.

## Properties

- **Randomized and asynchronous.** No rounds and no global clock are needed. Each node acts on its own clock.
- **Conserves the sum exactly.** In exact arithmetic the average is never lost, and in floating point the drift is at rounding level.
- **Monotone.** The distance to the average never increases along a run, not only in expectation.
- **Local.** A node needs only its neighbours and its row of $P$. No node needs $n$.
- **Anytime.** Every node holds an estimate at all times, and it improves with time.

## Variants and improvements

- **Optimized partner choice.** $\lambda_2(\bar W)$ is a convex function of $P$, so the $P$ that minimizes it is the solution of a [semidefinite program](/semidefinite-programming/). Boyd et al. give a distributed subgradient method for it. On the random geometric graph they show that the optimal $P$ and the natural $P$ give averaging times of the same order.
- **Geographic gossip.** Dimakis, Sarwate and Wainwright route each exchange to a random far node with [geographic routing](/geographic-routing/), so one tick mixes values over long distances. This saves about a factor $\sqrt{n / \log n}$ in radio transmissions on random geometric graphs.
- **Synchronous matching version.** In each round, the nodes of a random matching average in pairs. The analysis is the same with the expected matrix of one round.
- **One way exchanges.** If the partner cannot answer, an atomic two way exchange is not possible. [Push-sum](/push-sum/) keeps a weight next to each value and needs only one way messages.
- **Peer to peer overlays.** On an overlay where each node can reach a uniform random peer, push-pull averaging is [gossip aggregation](/gossip-aggregation/), with a variance reduction of about $1/(2\sqrt e)$ per cycle.

## When to use it

Use randomized gossip averaging when nodes have no common clock, the graph is fixed and well connected, and two neighbours can make an atomic exchange. It suits wireless sensor networks and data center fabrics where each link is cheap. On graphs with a small spectral gap, such as rings, grids and geometric graphs, it is slow: prefer geographic gossip, a spanning tree [convergecast](/convergecast/), or a synchronous iteration with optimized weights.

## Pitfalls

- **Ticks are not time.** Theorem 3 counts global ticks. With $n$ clocks of rate 1, the absolute time is $n$ times smaller, and the number of messages is twice the number of ticks.
- **Non-atomic exchanges.** If a message is lost after node $i$ has updated but before node $j$ has, the sum changes and the network converges to a wrong value. Two overlapping exchanges at the same node have the same effect.
- **Reading the theorem as a rate for every input.** Theorem 3 is about the worst input and a fixed confidence $\varepsilon$. A typical input with energy on fast modes reaches small error sooner, as the complete graph row of the table shows.
- **Floating point drift.** Over very many ticks, rounding changes the sum a little. Use exact arithmetic or reconcile the sum when it matters.
- **Disconnected support.** If the graph of $P + P^T$ is not connected, $\lambda_2(\bar W) = 1$ and each component converges to its own average.

## Implementations

## History

Boyd, Ghosh, Prabhakar and Shah analysed randomized gossip for averaging in the IEEE Transactions on Information Theory in 2006. They tied the averaging time to $\lambda_2(\bar W)$ and to the [mixing time](/mixing-time/) of the random walk $P$, and posed the choice of $P$ as a convex problem. The synchronous linear iteration with optimal weights is the earlier work of Xiao and Boyd (2004). Dimakis, Sarwate and Wainwright then showed that on geometric graphs standard gossip wastes most of its messages and gave geographic gossip as a remedy.

## References
