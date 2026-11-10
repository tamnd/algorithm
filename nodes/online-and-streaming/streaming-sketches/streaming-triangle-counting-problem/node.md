---
tag: TH991X
kind: problem
slug: streaming-triangle-counting-problem
name: Triangle counting in streams problem
aliases:
- triangle count in a graph stream
area: online-and-streaming/streaming-sketches
level: advanced
summary: Estimate the number T of triangles of a graph whose edges arrive as a stream. One pass needs Ω(m) bits in the worst case, and a few passes need Ω(m/T).
prereqs: [triangle-counting, streaming-model, index-problem, disjointness-problem, epsilon-delta-guarantee]
see_also: [streaming-triangle-counting, clustering-coefficient, frequency-moment-problem, triangle-listing-by-degree, triangle-detection-hypothesis, communication-complexity, streaming-maximal-matching-problem, stream-connectivity-problem]
sources:
  - url: https://arxiv.org/abs/1304.1458
    title: Vladimir Braverman, Rafail Ostrovsky and Dan Vilenchik, How hard is counting triangles in the streaming model, ICALP 2013
    locator: Section 1 (Definition 1, the survey of earlier algorithms, Theorems 1 to 3), Appendix A (the reduction from INDEX), Appendix B (the reduction from disjointness)
  - url: https://dl.acm.org/doi/10.5555/545381.545464
    title: Ziv Bar-Yossef, Ravi Kumar and D. Sivakumar, Reductions in streaming algorithms, with an application to counting triangles in graphs, SODA 2002
    locator: pp. 623 to 632; the reduction to frequency moments and the one-pass lower bound
  - paper: doi:10.1145/1142351.1142388
    title: Luciana S. Buriol, Gereon Frahling, Stefano Leonardi, Alberto Marchetti-Spaccamela and Christian Sohler, Counting triangles in data streams, PODS 2006
    locator: pp. 253 to 262; the sampling algorithms and their space in terms of T1, T2 and T3
  - url: https://www.vldb.org/pvldb/vol6/p1870-tirthapura.pdf
    title: A. Pavan, Kanat Tangwongsan, Srikanta Tirthapura and Kun-Lung Wu, Counting and sampling triangles from a graph stream, PVLDB 6(14), 2013
    locator: pp. 1870 to 1881; neighborhood sampling and its space bound in terms of m, the largest degree and T
  - paper: doi:10.1145/2627692.2627694
    title: Andrew McGregor, Graph stream algorithms, a survey, SIGMOD Record 43(1), 2014
    locator: the section on counting subgraphs (triangles in one and several passes)
---

The triangle counting in streams problem gives the edges of a graph one at a time and asks for an estimate of the number $T$ of triangles, using much less memory than the graph. Exact counting needs all the edges, so the goal is a $(1 \pm \varepsilon)$ approximation with probability at least $1 - \delta$. The difficulty depends strongly on $T$: one pass needs $\Omega(m)$ bits in the worst case even when $T$ is linear in $n$ (Bar-Yossef, Kumar and Sivakumar 2002; Braverman, Ostrovsky and Vilenchik 2013), and any constant number of passes needs $\Omega(m/T)$ bits. On this page $n$ is the number of vertices, $m$ the number of edges, $T$ the number of triangles, and $\Delta$ the largest degree.

## In plain words

A social network sends you its list of friendships, one pair at a time, and the list is too long to keep. You want to know how many groups of three people are all friends with each other. If you could keep the whole list, you would just count. With little memory you must guess from samples. A guess is easy when there are many such groups spread over the network. It is impossible when the groups are rare or all hang on one friendship that you may not have kept. So every method has a cost that grows when the number of groups is small compared with the size of the list.

## Definition

**Stream.** The input is a sequence of the $m$ edges of a simple graph $G = (V, E)$, $V = [n]$, in an order chosen by an adversary, each edge once. In the *dynamic* model edges can also be deleted.

**The problem.** Output $\hat T$ with $\Pr[|\hat T - T| \le \varepsilon T] \ge 1 - \delta$, using $p$ passes over the stream and as few bits of memory as possible. Braverman, Ostrovsky and Vilenchik call the case $\varepsilon = 0.1$, $\delta = 1/3$ with $p = c$ passes $\mathrm{Triangles}(c)$.

**The distinguishing version.** $\mathrm{Dist}(c)$: given that $G$ is either triangle-free or has at least $T$ triangles, decide which with probability at least $2/3$ in $c$ passes. Any algorithm for $\mathrm{Triangles}(c)$ solves $\mathrm{Dist}(c)$, since it outputs 0 on a triangle-free graph and at least $0.9\,T$ otherwise. So lower bounds for $\mathrm{Dist}$ hold for counting.

**Graph parameters.** For $i = 0, 1, 2, 3$ let $T_i$ be the number of vertex triples that span exactly $i$ edges, so $T_3 = T$ and $T_2$ is the number of open wedges. Most bounds are stated with $m$, $T$, and some of $\Delta$, $T_1$, $T_2$, or the largest number of triangles on one edge.

## Variants

- **One pass or several passes.** One pass is the main case; two passes already allow sublinear space for $\mathrm{Dist}$.
- **Insertion-only or dynamic streams.** With deletions, sketch methods replace sampling.
- **Adjacency-list order.** If all edges of a vertex arrive together, some bounds are better (Buriol et al. 2006).
- **Local counts.** Estimate the number of triangles at each vertex, used for the local [clustering coefficient](/clustering-coefficient/).
- **Transitivity.** Estimate $3T/(\text{number of wedges})$, the global clustering coefficient.
- **Sliding windows and other subgraphs**, such as cycles of length 4 and cliques.

## Examples

**Two triangles.** The stream $\{1,2\}$, $\{2,3\}$, $\{1,3\}$, $\{3,4\}$, $\{2,4\}$, $\{4,5\}$ has $T = 2$. The [neighborhood sampling](/streaming-triangle-counting/) page traces one estimator on it.

**Many wedges and no triangle.** Split $V$ into $A_0, A_1, A_2$ of size $n/3$ and join $A_0$ to $A_1$ and $A_1$ to $A_2$ completely. The graph is triangle-free, but it has $T_2 = \Theta(n^3)$ wedges. Methods whose space grows with $T_2/T$ or $(T_1 + T_2)/T$ are expensive here, even though the answer is simple (Braverman, Ostrovsky and Vilenchik).

**All triangles on one edge.** Take an edge $\{x, y\}$ and $T$ further vertices $z_1, \ldots, z_T$, each joined to $x$ and $y$. There are $T$ triangles, but all of them use the one edge $\{x, y\}$. An algorithm that does not keep this edge, or that cannot tell it apart, sees no triangle. This is the shape of the hard instances below.

## Known algorithms

| algorithm | passes | memory | needs to know |
|---|---|---|---|
| store all edges and count, for example with [triangle listing by degree](/triangle-listing-by-degree/) | 1 | $O(m)$ words | nothing |
| Bar-Yossef, Kumar and Sivakumar 2002, reduction to [frequency moments](/frequency-moment-problem/) | 1 | proportional to $((T_1 + T_2)/T)^3$, times factors in $\varepsilon$ and $\log n$ | $T_1$, $T_2$, $T$ |
| Jowhari and Ghodsi 2005, AMS sketches | 1 | about $(m^3 + mC_4 + C_6 + T^2)/T^2$, with $C_k$ the number of $k$-cycles | $m$, $C_4$, $C_6$, $T$ |
| Buriol et al. 2006, sample an edge and a vertex | 1 or 2 | proportional to $(T_0 + T_1 + T_2)/T$, or $(T_1 + T_2)/T$ | a bound on these ratios |
| [neighborhood sampling](/streaming-triangle-counting/), Pavan et al. 2013 | 1 | $O((m\Delta/(\varepsilon^2 T))\log(1/\delta))$ words | a bound on $m\Delta/T$ |
| Jha, Seshadhri and Pinar 2013, birthday paradox | 1 | $O(\sqrt{n})$ words when the transitivity is constant and there are more wedges than edges | nothing for these graphs |
| Braverman, Ostrovsky and Vilenchik 2013, Algorithm A for $\mathrm{Dist}(2)$ | 2 | at most $30m/T^{1/3}$ bits for $T \ge 216$ | $m$ and $T$ |

The table lists the space as it is stated by Braverman, Ostrovsky and Vilenchik for the first four rows. All these one-pass algorithms need $T$, or a bound on a ratio that contains $T$, to set their sample size; one can guess $T$ by doubling, at the cost of more passes or more space.

**Algorithm A** keeps each edge with probability $q = 6/T^{1/3}$ in the first pass, and fails if it stores more than $30m/T^{1/3}$ edges. If the stored graph $H$ has a triangle, it answers yes. In the second pass it answers yes if some edge closes a wedge of $H$. In a graph with at least $T$ triangles, some triangle has two edges in $H$ with probability at least $2/3$, while in a triangle-free graph the answer is always no.

Later work studies bounds in terms of other parameters, such as the largest number of triangles on one edge, and multi-pass bounds of order $m^{3/2}/T$ (see the survey of McGregor).

## Bounds

**Exact counting needs Ω(m) bits.** The hard instances below already need $\Omega(m)$ bits to tell $T = 0$ from $T \ge 1$. Offline, exact counting takes $O(m^{3/2})$ time, or matrix multiplication time; the [triangle detection hypothesis](/triangle-detection-hypothesis/) is about the offline time.

**One pass: Ω(m) bits, even with many triangles.** This is the reduction of Braverman, Ostrovsky and Vilenchik (Theorem 1), which extends the $\Omega(n^2)$ bound of Bar-Yossef, Kumar and Sivakumar. Use the [INDEX problem](/index-problem/) on $p = ab$ bits: Alice holds $x \in \{0, 1\}^{a \times b}$ and Bob holds a position $(i, j)$, and one message from Alice to Bob must let Bob find $x_{ij}$ with probability $2/3$. This needs $\Omega(p)$ bits. Take vertex sets $X = \{x_1, \ldots, x_a\}$, $Y = \{y_1, \ldots, y_b\}$ and $Z = \{z_1, \ldots, z_t\}$ with $1 \le t \le p$.

1. Alice streams the edge $\{x_k, y_l\}$ for each $(k, l)$ with $x_{kl} = 1$, then sends the memory of the algorithm to Bob.
2. Bob streams the $2t$ edges $\{z_r, x_i\}$ and $\{z_r, y_j\}$ for $r = 1, \ldots, t$, and reads the answer.

The graph has no edge inside $X$, $Y$ or $Z$, so a triangle has one vertex in each. A vertex $z_r$ is adjacent only to $x_i$ and $y_j$, so the only possible triangles are $\{z_r, x_i, y_j\}$, and they exist exactly when $x_{ij} = 1$. So the graph has $t$ triangles if $x_{ij} = 1$ and none otherwise, and it has at most $m = p + 2t \le 3p$ edges. A one-pass algorithm with $S$ bits that solves $\mathrm{Dist}(1)$ gives a protocol with $S$ bits, so $S = \Omega(p) = \Omega(m)$. With $a = b$, this gives $\Omega(n^2)$ for dense graphs, and by the choice of $a$, $b$ and $t$ it covers $m$ from $\Theta(n)$ to $\Theta(n^2)$ and up to a linear number of triangles. All $t$ triangles share the edge $\{x_i, y_j\}$, which is why sampling fails here.

**A constant number of passes: Ω(m/T) bits.** This is Theorem 2 of Braverman, Ostrovsky and Vilenchik, which improves the $\Omega(n/T)$ bound of Jowhari and Ghodsi (2005). Use the [disjointness problem](/disjointness-problem/): Alice and Bob hold sets $x, y \subseteq [k] \times [k]$ of size $r$, with the promise that $|x \cap y| = 0$ or $|x \cap y| \ge t$. Copying a disjointness instance on $r/t$ elements $t$ times shows that this promise version needs $\Omega(r/t)$ bits of communication, from the $\Omega(r')$ bound for disjointness of sets of size $r'$. Take vertex sets $A$, $B$, $C$ of size $k$ with the matching $\{a_l, c_l\}$ for all $l$.

1. Alice streams the matching and the edges $\{a_l, b_q\}$ for $(l, q) \in x$.
2. Bob streams the edges $\{c_l, b_q\}$ for $(l, q) \in y$.

There is no edge inside a part, so a triangle is $\{a_l, b_q, c_{l'}\}$, and the edge $\{a_l, c_{l'}\}$ forces $l' = l$. So the triangles are exactly the pairs $(l, q) \in x \cap y$, and $T = |x \cap y|$. An algorithm with $S$ bits and $c$ passes gives a protocol in which the memory crosses between Alice and Bob $2c - 1$ times, so $(2c - 1)S = \Omega(r/t)$. With $r \ge k$, the graph has $m = 2r + k = \Theta(r)$ edges and either no triangle or at least $t$ triangles, so $S = \Omega(m/(cT))$ with $T = t$.

**Two passes help.** Algorithm A shows that $\mathrm{Dist}(2)$ needs only $O(m/T^{1/3})$ bits, while by the one-pass bound $\mathrm{Dist}(1)$ needs $\Omega(m)$ bits on graphs with $T$ linear in $n$. So there is a space gap between one and two passes. Braverman, Ostrovsky and Vilenchik conjecture that the right bound for a constant number of passes is $\Omega(m/\rho)$, where $\rho$ is the number of vertices in triangles, so that $(6T)^{1/3} \le \rho \le 3T$.

**Variance bounds.** For one-pass sampling methods, the variance depends on how the triangles share edges, as in the example with all triangles on one edge. Neighborhood sampling has variance at most $m C T$ per estimator, where $C \le 2(\Delta - 1)$ is the largest number of later edges that touch an edge.

## Reductions

- **From INDEX and disjointness.** The lower bounds above reduce these communication problems to $\mathrm{Dist}(1)$ and $\mathrm{Dist}(O(1))$; see [communication complexity](/communication-complexity/).
- **To frequency moments (Bar-Yossef, Kumar and Sivakumar).** Give each vertex triple $S$ a counter $v_S$, the number of edges of $G$ inside $S$. An edge $\{u, w\}$ adds 1 to $v_{\{u, w, z\}}$ for each of the $n - 2$ other vertices $z$, so the counters form a stream of $m(n - 2)$ updates. Let $F_k = \sum_S v_S^k$ for $k = 1, 2$, and let $F_0$ be the number of nonzero counters. Then $F_0 = T_1 + T_2 + T_3$, $F_1 = T_1 + 2T_2 + 3T_3$ and $F_2 = T_1 + 4T_2 + 9T_3$, so
$$T = T_3 = F_0 - \tfrac{3}{2}F_1 + \tfrac{1}{2}F_2.$$
A check: the coefficients of $T_1$ are $1 - 3/2 + 1/2 = 0$, of $T_2$ are $1 - 3 + 2 = 0$, and of $T_3$ are $1 - 9/2 + 9/2 = 1$. Each moment is estimated with relative error, and the errors are of order $\varepsilon F_2$, which is why the space depends on $(T_1 + T_2)/T$.
- **To transitivity.** An estimate of $T$ and of the number of wedges $\sum_v \binom{\deg v}{2}$, which is easy to compute in one pass with $O(n)$ words, gives the global clustering coefficient.

## Applications

- The global and local clustering coefficient of social and web graphs.
- Features for spam and community detection, which use local triangle counts.
- Statistics for random graph models, such as exponential random graph models.
- A test case for lower bound methods that use communication complexity.

## References
