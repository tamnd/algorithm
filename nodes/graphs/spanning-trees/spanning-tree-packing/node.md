---
tag: 5A42P5
kind: problem
slug: spanning-tree-packing
name: Spanning tree packing problem
aliases:
- edge-disjoint spanning trees problem
area: graphs/spanning-trees
level: advanced
summary: Find the maximum number of pairwise edge-disjoint spanning trees in a graph.
prereqs: [spanning-tree, nash-williams-tutte-theorem, graphic-matroid]
see_also: [nash-williams-arboricity-theorem, arboricity, edge-connectivity, k-edge-connected-graph, spanning-tree-polytope, min-cut-problem, karger-min-cut, matroid]
sources:
  - paper: doi:10.1112/jlms/s1-36.1.445
    title: C. St. J. A. Nash-Williams, Edge-disjoint spanning trees of finite graphs, Journal of the London Mathematical Society 36 (1961), 445-450
    locator: the main theorem (the min-max formula for the packing number)
  - paper: doi:10.1112/jlms/s1-36.1.221
    title: W. T. Tutte, On the problem of decomposing a graph into n connected factors, Journal of the London Mathematical Society 36 (1961), 221-230
    locator: the main theorem
  - paper: doi:10.1287/moor.10.4.701
    title: James Roskind and Robert E. Tarjan, A note on finding minimum-cost edge-disjoint spanning trees, Mathematics of Operations Research 10(4) (1985), 701-708
    locator: the whole paper (an augmenting path algorithm for k disjoint spanning trees of least total cost)
  - paper: doi:10.1007/BF01758774
    title: Harold N. Gabow and Herbert H. Westermann, Forests, frames, and games, Algorithms for matroid sums and applications, Algorithmica 7 (1992), 465-497
    locator: the whole paper (fast algorithms for packing and covering by forests)
  - paper: doi:10.1145/3828.3829
    title: William H. Cunningham, Optimal attack and reinforcement of a network, Journal of the ACM 32(3) (1985), 549-561
    locator: the whole paper (the strength of a graph and its computation)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer Graduate Texts in Mathematics 173 (2017)
    locator: Chapter 2, Section 2.4, Tree-packing and arboricity
---

The spanning tree packing problem asks for the largest number of pairwise edge-disjoint [spanning trees](/spanning-tree/) in a graph, and for such a set of trees. The [Nash-Williams-Tutte theorem](/nash-williams-tutte-theorem/) gives the answer as a min-max formula over vertex partitions, and matroid partition algorithms find the trees in polynomial time. The packing number measures how robust a network is: it is at least half the [edge connectivity](/edge-connectivity/) and at most the edge connectivity.

## In plain words

You have a network of points and links. You want as many separate trees as possible, each one connecting all the points, with no link used by two trees. Each tree is a full backup of the network, so more trees means that more links can fail before the network splits.

The answer has a simple test. Split the points into groups. Every tree must link the groups together, so it needs one link fewer than the number of groups among the links between groups. The number of trees can never be more than the number of links between the groups divided by that amount. The smallest value of this ratio, over all ways to split the points, is exactly the answer.

## Definition

**Input.** A finite undirected multigraph $G = (V, E)$ with $n \ge 2$ vertices and $m$ edges. Parallel edges are allowed and count as different edges. Self-loops are allowed and are never in a tree.

**Output.** The *packing number* $\sigma(G)$, the largest $k$ such that $G$ has spanning trees $T_1, \ldots, T_k$ with $T_i \cap T_j = \emptyset$ for $i \ne j$, together with such trees.

**Min-max formula.** For a partition $\mathcal{P}$ of $V$ into nonempty parts, let $\delta(\mathcal{P})$ be the set of edges between different parts. By the Nash-Williams-Tutte theorem,

$$\sigma(G) = \min_{\mathcal{P} : |\mathcal{P}| \ge 2} \left\lfloor \frac{|\delta(\mathcal{P})|}{|\mathcal{P}| - 1} \right\rfloor.$$

**Connectivity.** If $G$ is not [connected](/connected-graph/), it has no spanning tree and $\sigma(G) = 0$; the partition into the components has no crossing edge. A graph with $n = 1$ has the empty spanning tree, which is disjoint from itself, so the problem is posed only for $n \ge 2$.

**Weights and ties.** The basic problem has no weights. In the weighted variant below, weights may tie, and ties only make the optimal set of trees non-unique; the optimal cost does not change.

## Variants

- **Decision version.** Given $k$, decide whether $\sigma(G) \ge k$. This is the test of the Nash-Williams-Tutte theorem.
- **Minimum-cost packing.** Given edge costs and $k \le \sigma(G)$, find $k$ edge-disjoint spanning trees of least total cost. Since the unions of $k$ disjoint forests are the independent sets of a matroid, the *union matroid*, this is a greedy problem on that matroid. Roskind and Tarjan gave an augmenting path algorithm for it.
- **Fractional packing.** Give each spanning tree a weight $\lambda_T \ge 0$ so that each edge has total weight at most 1, and maximize $\sum_T \lambda_T$. The optimum is the *strength* $\min_{\mathcal{P}} |\delta(\mathcal{P})| / (|\mathcal{P}| - 1)$ without the floor, studied by Cunningham; it is an LP over the [spanning tree polytope](/spanning-tree-polytope/).
- **Packing arborescences.** In a directed graph, find many arc-disjoint spanning arborescences rooted at $r$. By Edmonds' branching theorem, the answer is the least number of arcs entering a vertex set that does not contain $r$. Gabow gave a matroid algorithm for it.
- **Covering.** The dual problem asks for the least number of forests that cover all edges, the [arboricity](/arboricity/), given by the [Nash-Williams arboricity theorem](/nash-williams-arboricity-theorem/).
- **Steiner tree packing.** Pack trees that need only connect a set of terminals. This is NP-hard, and the min-max formula fails for it.

## Examples

**The complete graphs.** $K_4$ has 6 edges and $n - 1 = 3$, so $\sigma(K_4) \le 2$, and the paths $1, 2, 3, 4$ and $2, 4, 1, 3$ are two disjoint spanning trees, so $\sigma(K_4) = 2$. In general $\sigma(K_n) = \lfloor n / 2 \rfloor$: the partition into singletons gives $\lfloor n(n-1)/2 / (n-1) \rfloor = \lfloor n/2 \rfloor$. For $K_5$ this is 2, while the strength is $10/4 = 5/2$.

**A wheel.** Take a hub $0$ and a rim cycle $1, 2, 3, 4, 5$ with the edges $12, 23, 34, 45, 51$ and the spokes $01, \ldots, 05$, so $n = 6$ and $m = 10 = 2 \cdot 5$. The trees $\{01, 12, 23, 34, 45\}$ and $\{02, 03, 04, 05, 51\}$ are disjoint and use every edge, so $\sigma = 2$.

**A graph with six vertices.** The graph on $a$ to $f$ with the edges $ab, ac, bc, bd, cd, ce, de, df, ef$ has $m = 9 < 2 \cdot 5$, so $\sigma = 1$. Its strength is $9/5$, attained by the partition into singletons.

**A bottleneck.** Two copies of $K_5$ joined by one edge have $n = 10$ and $m = 21 \ge 2 \cdot 9$, yet $\sigma = 1$: the partition into the two copies has one crossing edge. The count of all edges alone does not decide the answer.

**A disconnected graph.** Two disjoint triangles have $\sigma = 0$.

## Known algorithms

| method | output | time |
|---|---|---|
| Brute force over sets of trees | $\sigma(G)$ and trees | exponential |
| Matroid partition (Edmonds 1965) | $\sigma(G)$ and trees | polynomial |
| Roskind and Tarjan (1985) | $k$ disjoint trees of least total cost | polynomial |
| Gabow and Westermann (1992) | $k$ disjoint forests of largest total size | faster matroid sum methods |
| Cunningham (1985) | the strength and a best partition | polynomial, by a sequence of minimum cut problems |

**Matroid partition.** Keep $k$ disjoint forests $F_1, \ldots, F_k$. To add a new edge $e$, look for an augmenting path: put $e$ into some $F_i$; if this closes a cycle, remove another edge $e'$ of that cycle and put $e'$ into some $F_j$, and so on until some forest takes an edge without a cycle. A breadth-first search over these moves finds a shortest such path or shows that none exists. The union of the forests is then as large as possible. With $k = \lfloor m / (n-1) \rfloor$ forests, the packing number is the largest $k$ for which the forests reach total size $k(n - 1)$. If the search fails, the edges it has reached give the partition that proves the bound, so the algorithm also returns a witness for the min-max formula.

**Small packing numbers.** For $k = 1$ the problem is a connectivity test in $O(n + m)$ time. For $k = 2$ one can find two disjoint trees, or a partition with too few crossing edges, by the same augmenting path method with only two forests.

## Bounds

**Lower bound.** Any algorithm must read all edges, so $\Omega(n + m)$ time is needed.

**Value bounds.** With $\lambda$ the edge connectivity, $\lfloor \lambda / 2 \rfloor \le \sigma(G) \le \lambda$. The upper bound holds since each tree crosses each cut; the lower bound follows from the min-max formula, since each part of a partition has at least $\lambda$ edges leaving it. Both bounds are attained: a cycle has $\lambda = 2$ and $\sigma = 1$, and a tree has $\lambda = \sigma = 1$. Also $\sigma(G) \le m / (n - 1)$.

**Upper bounds on time.** Matroid partition algorithms run in polynomial time; the precise bounds depend on $k$, and Gabow and Westermann give the fastest classical ones.

## Reductions

- **Packing to matroid partition.** The packing number is at least $k$ if and only if $E$ contains $k$ disjoint bases of the [graphic matroid](/graphic-matroid/), a matroid partition problem.
- **Strength to minimum cuts.** Cunningham computes the strength by a sequence of [minimum cut](/min-cut-problem/) problems in auxiliary networks.
- **Edge connectivity from packing.** Gabow's algorithm finds the edge connectivity by packing arborescences, and Karger's near-linear [minimum cut](/karger-min-cut/) algorithm uses a packing of spanning trees: some tree in a good fractional packing crosses a minimum cut at most twice.

## Applications

- **Network reliability.** Each tree is a backup that can broadcast to all nodes; $k$ disjoint trees keep the network connected after any $k - 1$ link failures.
- **Broadcast and gossip.** Disjoint trees give independent channels for sending data to all nodes at once, which raises throughput.
- **Minimum cuts.** Tree packing is the basis of near-linear time minimum cut algorithms.
- **Rigidity.** By Laman's and related theorems, rigidity of frameworks in the plane is tested with counts of the same kind, and some tests use the union of two forests.

## References
