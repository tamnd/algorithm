---
tag: 56M3CD
kind: concept
slug: graph-conductance
name: Graph conductance
aliases:
- Cheeger constant of a graph
- edge expansion
area: distributed/gossip
level: advanced
summary: Φ(G) is the least ratio, over vertex sets S with vol(S) ≤ |E|, of the edges leaving S to vol(S). It satisfies λ2/2 ≤ Φ ≤ √(2λ2) and bounds the time of push-pull gossip.
prereqs: [laplacian-matrix, eigenvalue, rayleigh-quotient, conductance]
see_also: [conductance, cheeger-inequality, conductance-rumor-spreading-bound, push-pull-gossip, spectral-gap, mixing-time, normalized-cut, spectral-clustering]
sources:
  - paper: doi:10.4230/LIPIcs.STACS.2011.57
    title: George Giakkoupis, Tight bounds for rumor spreading in graphs of a given conductance, Proceedings of the 28th Symposium on Theoretical Aspects of Computer Science (STACS), LIPIcs 9, 57-68, 2011
    locator: Section 2 (vol(S), cut(S, V - S) and the definition of φ), Lemma 15 (two stars joined at their centers)
  - book: isbn:9780821803158
    title: Fan R. K. Chung, Spectral Graph Theory, CBMS Regional Conference Series in Mathematics 92, American Mathematical Society, 1997
    locator: Chapter 1 (the normalized Laplacian), Chapter 2 (the Cheeger constant and the Cheeger inequality)
  - paper: doi:10.1137/1.9781611973402.59
    title: George Giakkoupis, Tight bounds for rumor spreading with vertex expansion, Proceedings of the 25th ACM-SIAM Symposium on Discrete Algorithms (SODA), 801-815, 2014
    locator: Section 2 (the boundary ∂S and the vertex expansion α(G)); Section 1 (vertex expansion and conductance are incomparable)
---

The conductance of a graph measures how hard it is to cut the graph into two parts: it is the smallest ratio, over all sets $S$ that hold at most half of the edge ends, of the number of edges that leave $S$ to the number of edge ends in $S$. A graph with high conductance has no bottleneck, and a graph with low conductance has a small cut that separates a large part. Cheeger's inequality ties it to the second eigenvalue $\lambda_2$ of the normalized Laplacian: $\lambda_2/2 \le \Phi \le \sqrt{2\lambda_2}$. In gossip, it bounds the time of [push-pull](/push-pull-gossip/): $O(\log n / \Phi)$ rounds on every graph.

## In plain words

Think of the graph as a road map. Pick a group of towns and count the roads that leave the group. Compare that with the total number of road ends in the group. If even the best choice of group, among groups that hold at most half of all road ends, has many roads leaving it, traffic can move freely and news travels fast. If some large group has very few roads out, those few roads are a bottleneck, and news that starts inside the group takes a long time to get out. Conductance is the ratio for the worst group. It is a number between 0 and 1; a complete graph has a value near one half, and two dense parts joined by a single road have a value near zero.

## The idea

### Notation and model

The graph $G = (V, E)$ is undirected, connected and without loops. It is the communication graph of the [random phone call model](/random-phone-call-model/) on a graph: in each round a node calls a uniformly random neighbor.

| Symbol | Meaning |
|---|---|
| $n$, $m$ | the numbers of vertices and edges, $n = \lvert V \rvert$, $m = \lvert E \rvert$ |
| $d(v)$ | the degree of $v$; $\Delta$ and $\delta$ are the maximum and the minimum degree |
| $D$ | the diameter |
| $\mathrm{vol}(S)$ | $\sum_{v \in S} d(v)$, the volume of $S$; $\mathrm{vol}(V) = 2m$ |
| $E(S, \bar S)$ | the set of edges with one end in $S$ and one in $\bar S = V \setminus S$ |
| $\Phi$ | the conductance |
| $\lambda_2$ | the second smallest eigenvalue of the normalized Laplacian |
| $f$ | not used on this page (the number of crashed nodes on other pages) |

### Definition

For a set $S$ with $0 < \mathrm{vol}(S)$ and $S \neq V$,
$$\Phi(S) = \frac{\lvert E(S, \bar S) \rvert}{\min\{\mathrm{vol}(S), \mathrm{vol}(\bar S)\}}, \qquad \Phi(G) = \min_{S} \Phi(S).$$
Equivalently, $\Phi(G)$ is the minimum of $\lvert E(S, \bar S)\rvert / \mathrm{vol}(S)$ over the sets with $0 < \mathrm{vol}(S) \le m$; this is the form of Giakkoupis (2011). Each edge that leaves $S$ adds 1 to the cut and 1 to $\mathrm{vol}(S)$, so $0 < \Phi \le 1$ for a connected graph with at least one edge.

**A random walk view.** For the simple random walk on $G$, the stationary probability of $v$ is $d(v)/2m$, and the probability flow from $S$ to $\bar S$ in one step is $\lvert E(S, \bar S)\rvert / 2m$. So $\Phi(S)$ is the probability that one step of the walk, started in the stationary distribution conditioned on $S$, leaves $S$. This makes $\Phi(G)$ the [conductance](/conductance/) of the random walk as a Markov chain.

**Related measures.**

- **Edge expansion.** $h(G) = \min_{0 < \lvert S \rvert \le n/2} \lvert E(S, \bar S) \rvert / \lvert S \rvert$ counts vertices instead of edge ends. For a $d$-regular graph, $h(G) = d\,\Phi(G)$. Some authors call $h$, and some call $\Phi$, the Cheeger constant of the graph.
- **Vertex expansion.** With the boundary $\partial S = \{v \notin S : v \text{ has a neighbor in } S\}$, the vertex expansion is $\alpha(G) = \min_{0 < \lvert S \rvert \le n/2} \lvert \partial S \rvert / \lvert S \rvert$ (Giakkoupis 2014). It counts the outside vertices that $S$ can reach, not the edges. Vertex expansion and conductance are incomparable: a graph can have one high and the other low.
- **Sparsest cut.** Replacing $\min\{\mathrm{vol}(S), \mathrm{vol}(\bar S)\}$ with $\mathrm{vol}(S)\,\mathrm{vol}(\bar S)/\mathrm{vol}(V)$ gives a quantity within a factor 2 of $\Phi(S)$; the [normalized cut](/normalized-cut/) of spectral clustering is a sum of two such ratios.

### Cheeger's inequality

Let $A$ be the adjacency matrix, $D_G$ the diagonal matrix of degrees, and $\mathcal{L} = I - D_G^{-1/2} A D_G^{-1/2}$ the normalized [Laplacian](/laplacian-matrix/). Its eigenvalues are $0 = \lambda_1 \le \lambda_2 \le \cdots \le \lambda_n \le 2$, and $\lambda_2 > 0$ when $G$ is connected. **Cheeger's inequality** for graphs says
$$\frac{\lambda_2}{2} \le \Phi(G) \le \sqrt{2\lambda_2}.$$
The upper bound is the hard direction; its proof sorts the vertices by the entries of an eigenvector of $\lambda_2$ and takes the best cut among the $n - 1$ prefix sets. It is cited here (Chung 1997, Chapter 2; the Markov chain form is on the page [Cheeger's inequality](/cheeger-inequality/)).

**Proof of the lower bound (complete).** By the Courant-Fischer theorem, with $x = D_G^{-1/2} y$,
$$\lambda_2 = \min \left\{ \frac{\sum_{\{u,v\} \in E} (x_u - x_v)^2}{\sum_v d(v) x_v^2} : x \neq 0, \ \sum_v d(v) x_v = 0 \right\}.$$
Take a set $S$ with $0 < \mathrm{vol}(S) \le m$, write $a = \mathrm{vol}(S)$ and $b = \mathrm{vol}(\bar S)$, and set $x_v = 1/a$ for $v \in S$ and $x_v = -1/b$ for $v \notin S$. Then $\sum_v d(v) x_v = 1 - 1 = 0$. An edge inside $S$ or inside $\bar S$ adds 0 to the numerator, and each cut edge adds $(1/a + 1/b)^2$. The denominator is $a/a^2 + b/b^2 = 1/a + 1/b$. So
$$\lambda_2 \le \lvert E(S, \bar S)\rvert \left(\frac{1}{a} + \frac{1}{b}\right) \le \frac{2\lvert E(S, \bar S)\rvert}{a} = 2\Phi(S),$$
because $b \ge a$. Taking the best $S$ gives $\lambda_2 \le 2\Phi(G)$. $\blacksquare$

## Examples

The values below are computed exactly by a brute force search over all vertex sets, with $\lambda_2$ from the Jacobi method, using the graph helpers in the implementation of the push-pull page.

| Graph | $n$ | $\Phi$ | $\lambda_2$ | $\lambda_2/2$ | $\sqrt{2\lambda_2}$ |
|---|---|---|---|---|---|
| complete graph $K_8$ | 8 | $4/7 \approx 0.571$ | 1.143 | 0.571 | 1.512 |
| star with 8 leaves | 9 | 1 | 1 | 0.5 | 1.414 |
| hypercube $Q_3$ | 8 | $1/3$ | 0.667 | 0.333 | 1.155 |
| hypercube $Q_4$ | 16 | $1/4$ | 0.5 | 0.25 | 1 |
| cycle $C_{12}$ | 12 | $1/6 \approx 0.167$ | 0.134 | 0.067 | 0.518 |
| two stars, 3 and 9 vertices, centers joined | 12 | $1/5$ | 0.230 | 0.115 | 0.679 |
| barbell: two $K_5$ joined by an edge | 10 | $1/21 \approx 0.048$ | 0.073 | 0.036 | 0.381 |

- **Complete graph.** For $\lvert S \rvert = k \le n/2$, $\Phi(S) = k(n-k)/(k(n-1)) = (n-k)/(n-1)$, which is smallest at $k = \lfloor n/2 \rfloor$: $\Phi(K_n) = \lceil n/2 \rceil/(n-1)$. Also $\lambda_2 = n/(n-1)$, so for even $n$ the lower bound $\lambda_2/2 \le \Phi$ is an equality.
- **Star.** Every set with volume at most $n - 1$ is a set of leaves or the center alone, and every edge at such a set leaves it, so $\Phi = 1$. The star is as well connected as a graph can be by this measure, but push from the center needs about $n \ln n$ rounds; see [the conductance bound on rumor spreading](/conductance-rumor-spreading-bound/).
- **Hypercube.** $Q_d$ has $2^d$ vertices, each of degree $d$. Cutting along one coordinate gives $2^{d-1}$ cut edges and volume $d\,2^{d-1}$, so $\Phi(Q_d) \le 1/d$, and the table shows equality for $d = 3$ and 4. Here $\lambda_2 = 2/d$, so the lower bound of Cheeger's inequality is again an equality.
- **Cycle.** Cutting $C_n$ into two paths of $n/2$ vertices gives 2 cut edges and volume $n$, so $\Phi = 2/n$ for even $n$. Here $\lambda_2 = 1 - \cos(2\pi/n) \approx 2\pi^2/n^2$, so $\Phi$ is of the order of $\sqrt{\lambda_2}$: the upper bound of Cheeger's inequality is tight up to a constant factor.
- **Barbell.** Two copies of $K_k$ joined by one edge have $\Phi = 1/(k(k-1) + 1)$: one clique has volume $k(k-1) + 1$ and one cut edge. The single edge is a bottleneck.
- **Two stars.** Giakkoupis (2011, Lemma 15) joins the centers of a star with $\lceil 1/\phi \rceil$ vertices and a star with the rest; the conductance is $\Theta(\phi)$. With $a$ vertices in the small star, the small star has volume $2a - 1$ and one cut edge, so $\Phi = 1/(2a - 1)$ when the small star is the worst set, as in the table with $a = 3$.

## Where it is used

- **Rumor spreading.** Push-pull informs all nodes of any connected graph in $O(\log n / \Phi)$ rounds with high probability, and some graphs need $\Omega(\log n / \Phi)$; see [the conductance bound on rumor spreading](/conductance-rumor-spreading-bound/). The reason is that, whatever the informed set $S$, at least $\Phi \min\{\mathrm{vol}(S), \mathrm{vol}(\bar S)\}$ edges join informed and uninformed nodes.
- **Mixing of random walks.** Through Cheeger's inequality, $\Phi^2/2 \le \lambda_2$, and $\lambda_2$ is twice the [spectral gap](/spectral-gap/) of the lazy random walk, which sets its [mixing time](/mixing-time/); a lazy random walk mixes fast if and only if there is no bottleneck.
- **Gossip averaging.** The time for [gossip averaging](/gossip-averaging/) to converge is set by a spectral gap, which Cheeger's inequality relates to conductance; see [averaging convergence and the spectral gap](/averaging-convergence-spectral-gap/).
- **Clustering and partitioning.** Spectral clustering looks for sets of low conductance, and the proof of the upper bound of Cheeger's inequality is an algorithm that finds a set $S$ with $\Phi(S) \le \sqrt{2\lambda_2}$ from an eigenvector; see [spectral clustering](/spectral-clustering/).
- **Overlay design.** Gossip overlays such as random regular graphs and the views of a [peer sampling service](/peer-sampling-service/) aim to keep the conductance high, so that no small part of the system is cut off by a few links.

## References
