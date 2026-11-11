---
tag: 2XVRJA
kind: theorem
slug: averaging-convergence-spectral-gap
name: Averaging convergence and spectral gap theorem
aliases:
- Boyd et al. convergence theorem
- averaging time and lambda_2
area: distributed/gossip
level: research
summary: The averaging time of randomized pairwise gossip is within constant factors of log(1/eps) / log(1/lambda_2), where lambda_2 is the second eigenvalue of the expected averaging matrix.
prereqs: [gossip-averaging, spectral-gap, eigenvalue, markov-inequality]
see_also: [distributed-averaging, push-sum, mixing-time, random-geometric-graph, laplacian-matrix, geographic-routing]
sources:
  - paper: doi:10.1109/TIT.2006.874516
    title: Stephen Boyd, Arpita Ghosh, Balaji Prabhakar and Devavrat Shah, Randomized gossip algorithms, IEEE Transactions on Information Theory 52(6), 2006
    locator: pages 2508 to 2530; Section II (the time model and Definition 1), Theorem 3 (the bounds), Section V (averaging time and mixing time), and the section on the geometric random graph (natural and optimal averaging have the same order)
  - paper: "Alexandros G. Dimakis, Anand D. Sarwate and Martin J. Wainwright, Geographic gossip: efficient averaging for sensor networks, IEEE Transactions on Signal Processing 56(3), 2008"
    locator: pages 1205 to 1216 (the transmission cost of standard gossip on random geometric graphs, and the gain of geographic gossip)
  - paper: doi:10.1016/j.sysconle.2004.02.022
    title: Lin Xiao and Stephen Boyd, Fast linear iterations for distributed averaging, Systems and Control Letters 53(1), 2004
    locator: pages 65 to 78 (the synchronous analogue, where the SLEM of W sets the rate)
---

This theorem, from Boyd, Ghosh, Prabhakar and Shah (2006), says that the averaging time of [randomized gossip averaging](/gossip-averaging/) is fixed, up to a constant factor, by one number: the second largest eigenvalue $\lambda_2(\bar W)$ of the expected averaging matrix. Since $\bar W$ is the identity minus a scaled [Laplacian](/laplacian-matrix/) of the graph, the averaging time is a [spectral gap](/spectral-gap/) quantity, like the [mixing time](/mixing-time/) of a random walk. Worked out on the complete graph, the cycle, the torus and the [random geometric graph](/random-geometric-graph/), it gives $\Theta(n)$, $\Theta(n^3)$, $\Theta(n^2)$ and $\Theta(n^2/\log n)$ clock ticks, times $\log \varepsilon^{-1}$.

## Statement

**Setting.** $G$ is a connected graph on $n$ nodes. Each node has a rate 1 Poisson clock; at the $k$-th tick of the merged clock, a uniform random node $i$ picks a neighbour $j$ with probability $P_{ij}$, and both set their values to $(x_i + x_j)/2$. So $x(k+1) = W(k) x(k)$, where $W(k) = I - \frac12 (e_i - e_j)(e_i - e_j)^T$ with probability $P_{ij}/n$. Let

$$\bar W = \mathbb{E}[W(k)] = I - \frac{1}{2n} D + \frac{P + P^T}{2n}, \qquad D_{ii} = \sum_j (P_{ij} + P_{ji}),$$

and let $\lambda_2(\bar W)$ be its second largest eigenvalue. The $\varepsilon$-averaging time is

$$T_{\mathrm{ave}}(\varepsilon, P) = \sup_{x(0) \ne 0} \inf\Big\{ k : \Pr\Big( \frac{\lVert x(k) - \bar x \mathbf 1 \rVert}{\lVert x(0) \rVert} \ge \varepsilon \Big) \le \varepsilon \Big\}.$$

**Theorem (Boyd, Ghosh, Prabhakar and Shah 2006, Theorem 3).** For $0 < \varepsilon < 1$, the averaging time in clock ticks satisfies

$$\frac{0.5 \, \log \varepsilon^{-1}}{\log \lambda_2(\bar W)^{-1}} \;\le\; T_{\mathrm{ave}}(\varepsilon, P) \;\le\; \frac{3 \, \log \varepsilon^{-1}}{\log \lambda_2(\bar W)^{-1}}.$$

**Corollary (symmetric $P$).** If $P = P^T$, then $\bar W = I - (I - P)/n$ and $1 - \lambda_2(\bar W) = (1 - \lambda_2(P))/n$. So $T_{\mathrm{ave}}(\varepsilon, P) = \Theta\big( n \log \varepsilon^{-1} / (1 - \lambda_2(P)) \big)$ ticks, and $\Theta\big( \log \varepsilon^{-1} / (1 - \lambda_2(P)) \big)$ units of absolute time.

## In plain words

Gossip averaging lets random pairs of neighbours meet and split the difference. How many meetings are needed before everyone is close to the average?

The answer depends on one number of the network, read off a matrix that describes one random meeting on average. That number measures how well the network is connected. If the network has a narrow bottleneck, values on the two sides mix slowly, and the number is close to its worst value. If every part of the network touches every other part, values mix fast.

The theorem shows that this one number tells the whole story, up to a small constant factor in both directions. A ring of computers is very slow, a square grid is faster, and a network where all pairs can talk is fastest. The same number also controls how fast a random walk on the network forgets where it started.

## Proof

We prove the upper bound for all $0 < \varepsilon < 1$, and the lower bound for $0 < \varepsilon \le \frac14$. Write $\lambda = \lambda_2(\bar W)$ and $e(k) = x(k) - \bar x \mathbf 1$.

**Facts about $\bar W$.** Each $W_{ij}$ is symmetric with $W_{ij}^2 = W_{ij}$, because $v = e_i - e_j$ has $v^T v = 2$, so $(vv^T)^2 = 2vv^T$. So each $W_{ij}$ is an orthogonal projection, and $W_{ij} \mathbf 1 = \mathbf 1$. Then $\bar W$ is symmetric, positive semidefinite, and $\bar W \mathbf 1 = \mathbf 1$. Its eigenvalues lie in $[0, 1]$, and on the subspace $\mathbf 1^\perp$ its largest eigenvalue is $\lambda$. The sum $\mathbf 1^T x(k)$ is kept by each step, so $e(k) \in \mathbf 1^\perp$ and $e(k+1) = W(k) e(k)$.

**Upper bound.** Given $e(k)$, the choice at tick $k$ is independent of it, so

$$\mathbb{E}\big[\lVert e(k+1) \rVert^2 \mid e(k)\big] = \mathbb{E}\big[e(k)^T W(k)^T W(k) e(k) \mid e(k)\big] = e(k)^T \bar W e(k) \le \lambda \lVert e(k) \rVert^2.$$

By induction, $\mathbb{E}\lVert e(k) \rVert^2 \le \lambda^k \lVert e(0) \rVert^2 \le \lambda^k \lVert x(0) \rVert^2$. By [Markov's inequality](/markov-inequality/), $\Pr(\lVert e(k) \rVert \ge \varepsilon \lVert x(0) \rVert) \le \lambda^k / \varepsilon^2$. For $k \ge 3 \log \varepsilon^{-1} / \log \lambda^{-1}$ we have $\lambda^k \le \varepsilon^3$, so the probability is at most $\varepsilon$ for every $x(0)$. Hence $T_{\mathrm{ave}} \le 3 \log \varepsilon^{-1} / \log \lambda^{-1}$.

**Lower bound.** Let $y$ be a unit eigenvector of $\bar W$ for $\lambda$ with $y \perp \mathbf 1$, and start at $x(0) = y$, so $\bar x = 0$ and $e(k) = x(k)$. The matrices $W(0), W(1), \ldots$ are independent, so

$$\mathbb{E}[x(k)] = \mathbb{E}[W(k-1)] \cdots \mathbb{E}[W(0)] \, y = \bar W^k y = \lambda^k y.$$

By Jensen's inequality for the convex function $\lVert \cdot \rVert$, $\mathbb{E}\lVert x(k) \rVert \ge \lVert \mathbb{E} x(k) \rVert = \lambda^k$. Also $\lVert x(k) \rVert \le \lVert x(0) \rVert = 1$, since projections do not increase the norm. Suppose that $\Pr(\lVert x(k) \rVert \ge \varepsilon) \le \varepsilon$. Then $\mathbb{E}\lVert x(k) \rVert \le \varepsilon \cdot 1 + 1 \cdot \varepsilon = 2\varepsilon$. So $\lambda^k \le 2\varepsilon$, that is, $k \ge \log((2\varepsilon)^{-1}) / \log \lambda^{-1}$. For $\varepsilon \le \frac14$, $2\varepsilon \le \varepsilon^{1/2}$, so $\log((2\varepsilon)^{-1}) \ge 0.5 \log \varepsilon^{-1}$, and the supremum over inputs is at least $0.5 \log \varepsilon^{-1} / \log \lambda^{-1}$.

**Corollary.** With $P = P^T$, $D = 2I$, so $\bar W = I - \frac1n I + \frac1n P = I - (I - P)/n$, and the eigenvalues of $\bar W$ are $1 - (1 - \mu)/n$ for the eigenvalues $\mu$ of $P$. Let $g = 1 - \lambda = (1 - \lambda_2(P))/n \le 2/n$. For $0 < g \le \frac12$, $g \le \log \frac1{1-g} \le 2g$, so $\log \lambda^{-1} = \Theta(g)$ and the theorem gives $\Theta(n \log \varepsilon^{-1} / (1 - \lambda_2(P)))$ ticks. The merged clock has rate $n$, so the absolute time is $1/n$ of this, up to the concentration of a Poisson process. $\square$

## Consequences

Take the natural walk $P_{ij} = 1/d_i$. On a regular graph $P$ is symmetric, so the corollary applies. The numbers in the last column are the value $\log \varepsilon^{-1} / \log \lambda_2(\bar W)^{-1}$ for $n = 100$ and $\varepsilon = 0.01$; the theorem places $T_{\mathrm{ave}}$ between half of it and three times it.

| graph | $1 - \lambda_2(P)$ | $1 - \lambda_2(\bar W)$ | $T_{\mathrm{ave}}$ in ticks | value at $n = 100$ |
|---|---|---|---|---|
| [complete graph](/complete-graph/) $K_n$ | $n/(n-1)$ | $1/(n-1)$ | $\Theta(n \log \varepsilon^{-1})$ | 454 |
| cycle $C_n$ | $1 - \cos(2\pi/n) \sim 2\pi^2/n^2$ | $\sim 2\pi^2/n^3$ | $\Theta(n^3 \log \varepsilon^{-1})$ | 233,375 |
| torus $\sqrt n \times \sqrt n$ | $(1 - \cos(2\pi/\sqrt n))/2 \sim \pi^2/n$ | $\sim \pi^2/n^2$ | $\Theta(n^2 \log \varepsilon^{-1})$ | 4,820 |

The eigenvalues of $P$ come from the circulant structure: on $C_n$ they are $\cos(2\pi k/n)$, and on the torus they are $(\cos(2\pi a/s) + \cos(2\pi b/s))/2$ with $s = \sqrt n$.

- **Complete graph.** $\Theta(n \log \varepsilon^{-1})$ ticks is $\Theta(\log \varepsilon^{-1})$ absolute time: each node takes part in a constant number of exchanges per unit of time, and the error drops by a constant factor per unit of time.
- **Cycle.** A value needs about $n^2$ exchanges per edge to diffuse around a ring of length $n$, so the absolute time is $\Theta(n^2 \log \varepsilon^{-1})$.
- **Torus and grid.** The torus needs $\Theta(n \log \varepsilon^{-1})$ absolute time, a factor $n$ better than the cycle with the same number of nodes, because its diameter is $\Theta(\sqrt n)$ in place of $\Theta(n)$.
- **Random geometric graph.** In $G(n, r)$, $n$ points are uniform in the unit square and two points are joined when their distance is at most $r$; it is connected with high probability for $r^2 \ge c \log n / n$ with a suitable constant $c$. Boyd et al. study $G(n, r)$ at this radius and show that the natural $P$ and the optimal $P$ give averaging times of the same order. With the spectral gap $\Theta(r^2)$ of the random walk on $G(n, r)$ and the formula $n \log \varepsilon^{-1} / (1 - \lambda_2(P))$ (the walk is close to, but not exactly, symmetric), this is $\Theta(n r^{-2} \log \varepsilon^{-1}) = \Theta(n^2 \log \varepsilon^{-1} / \log n)$ ticks. Each tick costs a constant number of radio transmissions, so standard gossip spends about $n^2 / \log n$ transmissions per factor of error.
- **Geographic gossip.** Dimakis, Sarwate and Wainwright exchange values with a random far node by [geographic routing](/geographic-routing/). Each exchange costs about $\sqrt{n / \log n}$ hops, but mixing is then as on a complete graph. Their total cost is $O(n^{1.5} \log \varepsilon^{-1} / \sqrt{\log n})$ transmissions on $G(n, r)$, a gain of a factor of about $\sqrt{n/\log n}$ over standard gossip.
- **Optimizing $P$.** $\lambda_2(\bar W)$ is a convex function of $P$, because $\bar W$ is affine in $P$ and the largest eigenvalue on $\mathbf 1^\perp$ is convex. So the fastest $P$ on a given graph is the solution of a [semidefinite program](/semidefinite-programming/), which Boyd et al. also solve in a distributed way by subgradient steps.
- **Mixing time.** Since the averaging time is $n$ times $\log \varepsilon^{-1} / (1 - \lambda_2(P))$ for symmetric $P$, it is close to $n$ times the [mixing time](/mixing-time/) of the random walk $P$. Boyd et al. make this link in their Section V; fast averaging and fast mixing are the same design problem.

## Tightness

- **Both sides are needed.** The constants 0.5 and 3 cannot be merged in general. In 200 seeded runs with $\varepsilon = 0.05$ and an input on the slowest eigenvector, the measured averaging time was $2.4$ times the central value $\log \varepsilon^{-1} / \log \lambda_2(\bar W)^{-1}$ on $K_{64}$ and $1.04$ times it on $C_{32}$; the [gossip averaging page](/gossip-averaging/) lists the runs.
- **The dependence on $\lambda_2$ is exact.** The lower bound proof uses an input on the eigenvector of $\lambda_2(\bar W)$, so no bound in terms of other spectral data can beat it for that input.
- **It is about the worst input and a fixed confidence.** For a typical input with energy spread over all eigenvectors, the error falls faster at first. The supremum in the definition and the confidence level $\varepsilon$ are part of the statement.
- **Only $\lambda_2$ of $\bar W$, not of $P$.** For non-symmetric $P$ the relevant matrix is $\bar W$, which depends on $(P + P^T)/2$. A walk $P$ that mixes fast but is far from symmetric does not give fast averaging by this theorem.

## History

The synchronous version of the question, with a fixed matrix $W$ and the SLEM as the rate, was studied by Xiao and Boyd (2004). Boyd, Ghosh, Prabhakar and Shah (2006) moved to asynchronous pairwise gossip, proved this theorem, linked averaging to mixing, and solved for the optimal $P$ by a semidefinite program. Their analysis of the geometric random graph showed that standard gossip is slow on wireless networks even with the optimal $P$, which led to geographic gossip by Dimakis, Sarwate and Wainwright (2008).

## References
