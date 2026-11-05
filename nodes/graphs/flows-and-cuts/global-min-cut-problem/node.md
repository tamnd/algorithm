---
tag: 1TS1R8
kind: problem
slug: global-min-cut-problem
name: Global minimum cut problem
aliases:
- global min cut
- minimum cut of an undirected graph
area: graphs/flows-and-cuts
level: core
summary: Find a minimum-capacity cut separating some nonempty proper subset of vertices.
prereqs: [cut, cut-capacity, min-cut-problem]
see_also: [stoer-wagner, karger-min-cut, karger-stein, hao-orlin, nagamochi-ibaraki, edge-connectivity, directed-global-min-cut-problem, all-pairs-min-cut-problem]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 13.2, Finding the Global Minimum Cut (the reduction to n - 1 s-t cuts, the contraction algorithm, and the number of global minimum cuts)
  - paper: doi:10.1145/263867.263872
    title: Mechthild Stoer and Frank Wagner, A simple min-cut algorithm, Journal of the ACM 44(4), 585 to 591 (1997)
    locator: the whole paper (maximum adjacency orderings and the O(nm + n^2 log n) bound)
  - paper: doi:10.1145/331605.331608
    title: David R. Karger, Minimum cuts in near-linear time, Journal of the ACM 47(1), 46 to 76 (2000)
    locator: the main theorem (an O(m log^3 n) randomized algorithm)
  - paper: doi:10.1006/jagm.1994.1043
    title: Jianxiu Hao and James B. Orlin, A faster algorithm for finding the minimum cut in a directed graph, Journal of Algorithms 17(3), 424 to 446 (1994)
    locator: the reduction of all n - 1 cut problems to one run of push-relabel
---

The global minimum cut problem asks, for an undirected graph with nonnegative edge weights, for a split of the vertices into two nonempty parts that cuts the least total weight. Unlike the [s-t minimum cut](/min-cut-problem/), no two vertices are fixed to lie on different sides. With unit weights its value is the [edge connectivity](/edge-connectivity/) of the graph: the fewest edges whose removal disconnects it. It can be solved by $n - 1$ maximum flows, but special algorithms are faster, such as [Stoer-Wagner](/stoer-wagner/) in $O(nm + n^2 \log n)$ and [Karger's](/karger-min-cut/) randomized methods in near-linear time.

## In plain words

A network of roads joins some towns. What is the cheapest set of roads to block so that the towns fall into two groups that cannot reach each other? Any split counts, as long as each group has at least one town.

The answer measures how well the network holds together: a small answer means a weak spot. One way to find it is to fix one town and, for every other town, find the cheapest way to separate the two with a flow method; the best of these is the answer, because the best split separates the fixed town from some other town. Faster methods avoid the flows: they merge towns that are tightly joined, step by step, and keep track of the cheapest split seen along the way.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n \ge 2$ vertices and $m$ edges, and a weight $w(e) \ge 0$ on each edge. Weights may be real numbers; with unit weights the problem is edge connectivity, an integer case. Parallel edges are allowed and their weights add up; self-loops cross no cut and can be removed.

**Output.** A set $S$ with $\emptyset \ne S \subsetneq V$ that minimizes
$$w(\delta(S)) = \sum_{\{u, v\} \in E,\ u \in S,\ v \notin S} w(\{u, v\}),$$
and the minimum value $\lambda(G)$. Since $\delta(S) = \delta(V \setminus S)$, the sets $S$ and $V \setminus S$ give the same cut.

**Relation to s-t cuts.** For each pair $s \ne t$ let $\lambda(s, t)$ be the least weight of a cut with $s \in S$ and $t \notin S$. Then $\lambda(G) = \min_{s \ne t} \lambda(s, t)$, and for any fixed $s$, $\lambda(G) = \min_{t \ne s} \lambda(s, t)$, since a minimum cut has $s$ on one side and some $t$ on the other.

**Directed graphs.** For a directed graph the cut is the weight of the edges leaving $S$, and $S$ and its complement differ. That is the [directed global minimum cut](/directed-global-min-cut-problem/). To compute an undirected cut with a directed maximum flow code, replace each edge $\{u, v\}$ by the two arcs $(u, v)$ and $(v, u)$, each of weight $w$, kept as two separate antiparallel arcs.

## Variants

- **Edge connectivity.** Unit weights; the answer is $\lambda(G)$, the largest $k$ such that $G$ is $k$-edge-connected.
- **All minimum cuts.** There are at most $\binom{n}{2}$ global minimum cuts, and the cactus representation stores all of them in $O(n)$ space.
- **Near-minimum cuts.** Cuts of weight at most $\alpha \lambda(G)$ number at most $O(n^{2\alpha})$, a bound from the analysis of the contraction algorithm.
- **Minimum $k$-cut.** Split into $k$ nonempty parts with least weight between parts; polynomial for fixed $k$, NP-hard when $k$ is part of the input.
- **Maximum cut.** The opposite goal, the heaviest cut, is NP-hard.
- **Balanced and sparsest cuts.** Requiring the parts to have similar size gives NP-hard problems such as the [sparsest cut](/sparsest-cut-problem/).

## Examples

**The running network, undirected.** Take the edges $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10 as undirected. The weighted degrees are $s$: 20, $a$: 24, $b$: 20, $c$: 21, $d$: 33, $t$: 20. Checking all 31 splits gives $\lambda(G) = 20$, reached by four cuts: $S = \{s\}$, $\{b\}$, $\{t\}$ and $\{b, t\}$, where $\{b, t\}$ cuts $a b$, $d b$ and $d t$, of weight $4 + 6 + 10 = 20$. The directed s-t minimum cut of this network is 19, because in the directed version only edges leaving $S$ count.

**A cycle.** The cycle $C_n$ with unit weights has $\lambda = 2$, and every split into two arcs of the cycle is a minimum cut: $\binom{n}{2}$ of them. This shows that the bound on the number of minimum cuts is tight.

**A disconnected graph.** If $G$ is not connected, take $S$ as one component: $\lambda(G) = 0$. There is no path between the two sides, and a flow based method sees a maximum flow of 0 for some $t$. Edges of weight 0 behave like missing edges, so a graph that is connected only through zero-weight edges also has $\lambda(G) = 0$.

**A minimum cut need not be a vertex.** Two complete graphs $K_4$ with unit weights, joined by one edge, have minimum degree 3 but $\lambda = 1$, from the bridge.

## Known algorithms

- **$n - 1$ maximum flows.** Fix $s$; for each $t \ne s$ compute a [minimum s-t cut](/min-cut-problem/) with a maximum flow algorithm, and keep the best. This costs $n - 1$ maximum flows.
- **[Hao-Orlin](/hao-orlin/).** Runs all $n - 1$ flows inside one execution of push-relabel, in the time of one: $O(nm \log(n^2/m))$. It also works for directed graphs.
- **[Nagamochi-Ibaraki](/nagamochi-ibaraki/) and [Stoer-Wagner](/stoer-wagner/).** A maximum adjacency ordering finds, without flows, a pair $s, t$ and their minimum cut $\lambda(s, t)$; merging $s$ and $t$ and repeating $n - 1$ times gives $O(nm + n^2 \log n)$ deterministic time.
- **[Karger's contraction](/karger-min-cut/).** Contract a random edge, chosen with probability proportional to weight, until two vertices remain; the result is a given minimum cut with probability at least $\binom{n}{2}^{-1}$. Repeating $O(n^2 \log n)$ times gives high probability.
- **[Karger-Stein](/karger-stein/).** Contract to about $n/\sqrt 2$ vertices, recurse twice: $O(n^2 \log^3 n)$ for high probability.
- **Karger's near-linear algorithm.** Tree packings and dynamic programming over spanning trees give $O(m \log^3 n)$ randomized time (2000), later improved by smaller log factors.
- **Deterministic near-linear time.** Kawarabayashi and Thorup gave a deterministic near-linear algorithm for simple unweighted graphs, and Li (2021) a deterministic $m^{1 + o(1)}$ algorithm for weighted graphs.

## Bounds

The best randomized algorithms run in $O(m \log^2 n)$ or near it, and deterministic ones in $m^{1 + o(1)}$ time. The trivial lower bound is $\Omega(m)$: an algorithm that skips an edge cannot tell whether it is the only edge across a cut. The problem is much easier than the s-t version in one sense: the global minimum can be found without any flow at all, which is not known for s-t cuts.

## Reductions

- **To $n - 1$ s-t minimum cuts**, as above, and to one [all-pairs minimum cut](/all-pairs-min-cut-problem/) structure: the lightest edge of a Gomory-Hu tree gives a global minimum cut.
- **Edge connectivity** is the unit weight case.
- **From $k$-edge-connectivity testing.** Deciding whether $\lambda(G) \ge k$ is a decision version.

## Applications

Network reliability (the fewest links whose failure splits a network), clustering and image segmentation by recursive cuts, the cutting plane method for the traveling salesman problem (separating subtour elimination constraints is a global minimum cut problem), and compiler and VLSI partitioning.

## References
