---
tag: CJMYDK
kind: problem
slug: network-diameter-estimation
name: Network diameter estimation
aliases:
- neighbourhood function estimation
area: graphs/network-analysis
level: advanced
summary: Estimate the diameter and neighbourhood function of very large graphs.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: "O(n m)"}
prereqs: [breadth-first-search, eccentricity, shortest-path, neighborhood-function]
see_also: [effective-diameter, anf-algorithm, hyperloglog, all-pairs-shortest-paths, tree-diameter, strong-exponential-time-hypothesis, six-degrees-of-separation, distributed-diameter]
sources:
  - paper: doi:10.1145/2488608.2488673
    title: Liam Roditty and Virginia Vassilevska Williams, Fast approximation algorithms for the diameter and radius of sparse graphs, Proceedings of the 45th ACM Symposium on Theory of Computing (STOC 2013), 515 to 524
    locator: the 3/2-approximation of the diameter in expected O~(m n^(1/2)) time, and the reduction showing that telling diameter 2 from 3 in sparse graphs in O(m^(2-ε)) time would refute the strong exponential time hypothesis
  - paper: doi:10.1137/S0097539796303421
    title: Donald Aingworth, Chandra Chekuri, Piotr Indyk and Rajeev Motwani, Fast estimation of diameter and shortest paths (without matrix multiplication), SIAM Journal on Computing 28(4), 1167 to 1181 (1999)
    locator: the estimate D' with floor(2D/3) <= D' <= D in O~(m n^(1/2) + n^2) time
  - paper: doi:10.1016/j.tcs.2012.09.018
    title: Pilu Crescenzi, Roberto Grossi, Michel Habib, Leonardo Lanzi and Andrea Marino, On computing the diameter of real-world undirected graphs, Theoretical Computer Science 514, 84 to 95 (2013)
    locator: the iFUB method (iterative fringe upper bound), its stopping rule, and the experiments on real graphs where few BFS are needed
  - paper: doi:10.1145/1412228.1455266
    title: Clémence Magnien, Matthieu Latapy and Michel Habib, Fast computation of empirically tight bounds for the diameter of massive graphs, ACM Journal of Experimental Algorithmics 13, article 1.10 (2009)
    locator: the double sweep lower bound and the upper bounds from BFS trees
  - paper: doi:10.1145/2063576.2063748
    title: Frank W. Takes and Walter A. Kosters, Determining the diameter of small world networks, Proceedings of the 20th ACM Conference on Information and Knowledge Management (CIKM 2011), 1191 to 1196
    locator: the BoundingDiameters method that keeps lower and upper bounds on every eccentricity
  - paper: doi:10.1145/775047.775059
    title: Christopher R. Palmer, Phillip B. Gibbons and Christos Faloutsos, ANF, a fast and scalable tool for data mining in massive graphs, Proceedings of the 8th ACM SIGKDD Conference (KDD 2002), 81 to 90
    locator: the approximate neighbourhood function with Flajolet-Martin counters, one pass over the edges per distance
  - paper: doi:10.1145/1963405.1963493
    title: Paolo Boldi, Marco Rosa and Sebastiano Vigna, HyperANF, approximating the neighbourhood function of very large graphs on a budget, Proceedings of the 20th International Conference on World Wide Web (WWW 2011), 625 to 634
    locator: the neighbourhood function with HyperLogLog counters, and the bound on the relative standard deviation of the estimate
  - paper: doi:10.1145/2380718.2380723
    title: Lars Backstrom, Paolo Boldi, Marco Rosa, Johan Ugander and Sebastiano Vigna, Four degrees of separation, Proceedings of the 4th ACM Web Science Conference (WebSci 2012), 33 to 42
    locator: the distance distribution of the Facebook graph of 721 million users computed with HyperANF, with average distance 4.74
  - paper: doi:10.1145/1081870.1081893
    title: Jure Leskovec, Jon Kleinberg and Christos Faloutsos, Graphs over time, densification laws, shrinking diameters and possible explanations, Proceedings of the 11th ACM SIGKDD Conference (KDD 2005), 177 to 187
    locator: the effective diameter as the 90th percentile of the distances, and the observation that it shrinks as real networks grow
  - paper: doi:10.1006/jcss.1995.1078
    title: Raimund Seidel, On the all-pairs-shortest-path problem in unweighted undirected graphs, Journal of Computer and System Sciences 51(3), 400 to 403 (1995)
    locator: all distances of an unweighted undirected graph in O(n^ω log n) time by matrix multiplication
---

Network diameter estimation asks for the diameter of a graph, the largest distance between two vertices, and more generally for its distance distribution, given by the [neighbourhood function](/neighborhood-function/), on graphs too large for one [breadth-first search](/breadth-first-search/) from every vertex. The exact answer takes $O(nm)$ time by $n$ searches, and under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) no algorithm is much faster on sparse graphs, even for telling diameter 2 from diameter 3. In practice, bounds from a few searches, such as the double sweep and the iFUB method, find the exact diameter of most real networks, and probabilistic counters such as [HyperLogLog](/hyperloglog/) estimate the whole distance distribution in a few passes over the edges.

## In plain words

The distance between two people in a social network is the smallest number of friendship links that join them. The diameter is the largest such distance: how far apart the two most distant people are. Other numbers describe the typical case: the average distance, or the distance within which 90 percent of the pairs lie.

Measuring these exactly means finding the distance between every pair of people, which is far too slow for a network of a billion people. Two shortcuts help. One finds the farthest people with a few clever searches and proves that no pair is farther. The other keeps a tiny summary of "who can I reach in $t$ steps" for each person and grows it one step at a time, which gives good estimates of how many pairs lie within each distance.

## Definition

**Input.** A [graph](/graph/) $G = (V, E)$ with $n$ vertices and $m$ edges, usually undirected and without weights, given by adjacency lists. Let $d(u, v)$ be the number of edges on a [shortest path](/shortest-path/) from $u$ to $v$, and $\infty$ if there is none.

**Quantities.** For a vertex $v$, its [eccentricity](/eccentricity/) is $\operatorname{ecc}(v) = \max_u d(v, u)$. For a connected graph,

$$D(G) = \max_{v} \operatorname{ecc}(v) = \max_{u, v} d(u, v), \qquad r(G) = \min_v \operatorname{ecc}(v)$$

are the *diameter* and the *radius*. The neighbourhood function is $N(t) = |\{(u, v) : d(u, v) \le t\}|$ over ordered pairs, self-pairs included, so $N(0) = n$. From it one reads the number of pairs at each distance, the average distance, and the [effective diameter](/effective-diameter/), the smallest $t$ with $N(t) - n \ge 0.9\,(N(\infty) - n)$, or its interpolated form.

**Output.** The exact problem asks for $D(G)$, or for all eccentricities. The estimation problem asks for a value $\hat D$ with $D/c \le \hat D \le D$ for a factor $c$, for lower and upper bounds that meet, or for estimates $\hat N(t)$ of the neighbourhood function with a small relative error.

**Disconnected and directed graphs.** If $G$ is not connected, $D(G) = \infty$ by the definition. Network analysis then takes the largest finite distance, or the diameter of the [giant component](/giant-component/), and the neighbourhood function counts only reachable pairs. For a directed graph, $d(u, v)$ follows the arcs and $\operatorname{ecc}$ splits into an out- and an in-eccentricity. With edge lengths, the searches become runs of [Dijkstra's algorithm](/dijkstra/).

## Variants

- **Exact diameter.** Compute $D(G)$ exactly, or decide whether $D(G) \le t$.
- **All eccentricities, radius and center.** Compute $\operatorname{ecc}(v)$ for every $v$, which gives the radius and the center, the vertices of smallest eccentricity.
- **Approximate diameter.** Output $\hat D$ with $\lfloor 2D/3 \rfloor \le \hat D \le D$, or with another factor.
- **Neighbourhood function.** Estimate $N(t)$ for every $t$, and from it the distance distribution, the average distance and the effective diameter.
- **Distributed.** Compute the diameter in the CONGEST model, where each round sends small messages along the edges ([distributed diameter](/distributed-diameter/)).

## Examples

Take the vertices 0 to 6 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$: a diamond on 0 to 3 joined by the edge $\{3, 4\}$ to the triangle on 4, 5 and 6.

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $\operatorname{ecc}(v)$ | 4 | 3 | 3 | 2 | 3 | 4 | 4 |

So $D = 4$, reached by the pairs $\{0, 5\}$ and $\{0, 6\}$, the radius is 2, and the center is $\{3\}$. The neighbourhood function is $N(0), \dots, N(4) = 7, 25, 35, 45, 49$, the average distance is 2, and the effective diameter is 3.

- **One search.** A BFS from 3 gives $\operatorname{ecc}(3) = 2$, so $2 \le D \le 4$ by the bound below.
- **Double sweep.** The farthest vertex from 3, with the smallest number on ties, is 0, and a second BFS from 0 gives $\operatorname{ecc}(0) = 4$, a lower bound that here equals $D$.
- **iFUB.** The BFS tree from 3 has the levels $\{3\}$, $\{1, 2, 4\}$ and $\{0, 5, 6\}$. Three searches from the last level give the lower bound $4 > 2 \cdot (2 - 1)$, which proves $D = 4$ with 4 searches instead of 7.

**Standard graphs.** The path $P_n$ has $D = n - 1$, the cycle $C_n$ has $D = \lfloor n/2 \rfloor$, the complete graph has $D = 1$, and a [tree](/tree/) has the diameter that two searches find exactly ([tree diameter](/tree-diameter/)). The Facebook graph of 721 million users in 2011 had an average distance of 4.74, computed by Backstrom, Boldi, Rosa, Ugander and Vigna with HyperANF.

## Known algorithms

| algorithm | time | output |
|---|---|---|
| BFS from every vertex | $O(nm)$ | all eccentricities, exact |
| Seidel, by matrix products | $O(n^\omega \log n)$ | all distances, exact, unweighted undirected |
| one BFS | $O(m)$ | $\operatorname{ecc}(v) \le D \le 2\operatorname{ecc}(v)$ |
| double sweep (Magnien, Latapy and Habib) | $O(m)$ | a lower bound, exact on trees |
| iFUB (Crescenzi and co-authors) | $O(nm)$ worst, few BFS in practice | exact |
| BoundingDiameters (Takes and Kosters) | $O(nm)$ worst, few BFS in practice | exact $D$ and radius |
| Aingworth, Chekuri, Indyk and Motwani | $\tilde O(m\sqrt n + n^2)$ | $\lfloor 2D/3 \rfloor \le \hat D \le D$ |
| Roditty and Vassilevska Williams | $\tilde O(m\sqrt n)$ expected | $\lfloor 2D/3 \rfloor \le \hat D \le D$ |
| BFS from $r$ random sources | $O(rm)$ | $N(t)$ within $\pm \varepsilon n^2$ |
| [ANF](/anf-algorithm/) and HyperANF | $O(Dm)$ counter operations | $N(t)$ within a small relative error |

Here $\omega < 2.372$ is the [exponent of matrix multiplication](/matrix-multiplication-exponent/), and $\tilde O$ hides factors of $\log n$. ANF keeps a Flajolet-Martin sketch of the ball $B(v, t)$ for each vertex and gets the sketch of $B(v, t + 1)$ as the union of the sketches of the neighbours, one pass over the edges per step. HyperANF does the same with HyperLogLog counters of $O(\log \log n)$ bits each, and the union is a maximum per register.

## Bounds

- **One search.** For every vertex $v$, $\operatorname{ecc}(v) \le D \le 2\operatorname{ecc}(v)$. *Proof.* The first inequality is the definition. For any $x, y$, $d(x, y) \le d(x, v) + d(v, y) \le 2\operatorname{ecc}(v)$. $\square$
- **The fringe bound of iFUB.** Let the BFS from $u$ have levels $L_0, \dots, L_e$ with $e = \operatorname{ecc}(u)$, and for $i \ge 1$ let $B_i = \max\{\operatorname{ecc}(x) : x \in L_i \cup \dots \cup L_e\}$. Then $D \le \max(B_i, 2(i - 1))$, so if $B_i > 2(i - 1)$ then $D = B_i$. *Proof.* Take a pair $x, y$. If one of them, say $x$, lies in a level $\ge i$, then $d(x, y) \le \operatorname{ecc}(x) \le B_i$. Otherwise both lie in levels $\le i - 1$, and $d(x, y) \le d(x, u) + d(u, y) \le 2(i - 1)$. Since $B_i \le D$, the equality follows. $\square$ iFUB computes $B_e, B_{e-1}, \dots$ one level at a time and stops at the first $i$ with $B_i > 2(i - 1)$. It stops at the latest at $i = 1$, since $B_1 > 0$ when $n \ge 2$, and then it has searched from every vertex but $u$; this is the worst case.
- **Sampling.** Pick $r$ sources $u_1, \dots, u_r$ uniformly and independently, run a BFS from each, and let $\hat N(t) = \frac{n}{r}\sum_i |B(u_i, t)|$. Since $N(t) = \sum_u |B(u, t)|$, this is unbiased, and since each $|B(u_i, t)| \in [1, n]$, the [Hoeffding inequality](/hoeffding-inequality/) gives $\Pr[|\hat N(t) - N(t)| \ge \varepsilon n^2] \le 2e^{-2r\varepsilon^2}$. So $r = \lceil \ln(2/\delta)/(2\varepsilon^2) \rceil$ searches give additive error $\varepsilon n^2$ with probability $1 - \delta$, for each $t$.
- **Conditional lower bound.** Roditty and Vassilevska Williams showed that an algorithm that tells diameter 2 from diameter 3 in undirected graphs with $m = O(n)$ edges in $O(m^{2 - \varepsilon})$ time, for some $\varepsilon > 0$, would refute the strong exponential time hypothesis, through the [orthogonal vectors](/orthogonal-vectors-hypothesis/) problem. So under SETH, no $(3/2 - \varepsilon)$-approximation runs in truly subquadratic time on sparse graphs, and the exact $O(nm)$ bound is tight up to $m^{o(1)}$ factors for $m = \Theta(n)$.
- **No unconditional bound.** No lower bound above the time to read the input is known for the diameter in the word RAM.

## Reductions

- **To all-pairs shortest paths.** The diameter is the largest entry of the distance matrix, so any [all-pairs shortest paths](/all-pairs-shortest-paths/) method computes it; for unweighted undirected graphs, Seidel's method gives $O(n^\omega \log n)$.
- **Diameter at most 2.** $D \le 2$ exactly when every entry of $(A + I)^2$ is positive, which is one Boolean matrix product.
- **From orthogonal vectors.** Given two sets of $N$ vectors in $\{0, 1\}^d$, Roditty and Vassilevska Williams build a graph with $O(N + d)$ vertices and $O(Nd)$ edges whose diameter is 3 if some pair of vectors is orthogonal and 2 otherwise. This is the reduction behind the conditional lower bound.
- **To distinct counting.** The size of the ball $B(v, t + 1)$ is the number of distinct elements in the union of the balls $B(w, t)$ over the neighbours $w$ of $v$ and $v$ itself. A mergeable distinct-count sketch, such as a [Flajolet-Martin sketch](/flajolet-martin-sketch/) or a HyperLogLog counter, turns the neighbourhood function into $D$ rounds of sketch unions.

## Applications

- **Small-world measurements.** The claims of [six degrees of separation](/six-degrees-of-separation/) and of [small-world networks](/small-world-network/) are statements about the distance distribution, which on social networks of hundreds of millions of users is measured with HyperANF.
- **Graph evolution.** Leskovec, Kleinberg and Faloutsos found with the effective diameter that the diameter of many real networks shrinks as they grow, which shaped later generators such as [Kronecker graphs](/kronecker-graph-model/).
- **Testing generators.** Comparing the distance distribution of a model with that of a real network is a standard check of a random graph model.
- **Networking and databases.** The diameter bounds the number of hops of a broadcast or a flooding protocol, and the number of rounds of a BFS-style distributed or graph-database computation.
- **Anomaly and robustness analysis.** Removing vertices and watching how the effective diameter grows measures how a network depends on its hubs.

## References
