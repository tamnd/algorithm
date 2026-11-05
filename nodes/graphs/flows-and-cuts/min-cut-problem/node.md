---
tag: FZJKWS
kind: problem
slug: min-cut-problem
name: Minimum s-t cut problem
aliases:
- minimum cut
- s-t minimum cut
area: graphs/flows-and-cuts
level: intro
summary: Find a set of edges of minimum total capacity whose removal separates s from t.
prereqs: [cut, cut-capacity, max-flow-problem]
see_also: [max-flow-min-cut-theorem, residual-graph, global-min-cut-problem, image-segmentation-graph-cuts, maximum-weight-closure, multiway-cut-problem, gomory-hu-tree, submodular-function]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 24.2, The Ford-Fulkerson method (cuts of flow networks, the bound of a flow by a cut, and the max-flow min-cut theorem)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.2, Maximum Flows and Minimum Cuts in a Network (computing a minimum cut from a maximum flow)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 10, Maximum flow (minimum cuts and their computation)
  - paper: doi:10.4153/CJM-1956-045-5
    title: L. R. Ford Jr. and D. R. Fulkerson, Maximal flow through a network, Canadian Journal of Mathematics 8, 399 to 404 (1956)
    locator: the whole paper (the minimal cut theorem)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts, and Chapter 11, Applications of Flows and Cuts
---

The minimum $s$-$t$ cut problem asks, in a [flow network](/flow-network/), for a split of the vertices into a part $S$ that holds the source $s$ and a part $T$ that holds the sink $t$, such that the total capacity of the edges from $S$ to $T$ is as small as possible. Equivalently, it asks for the cheapest set of edges whose removal leaves no directed path from $s$ to $t$. By the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) its optimum equals the [maximum flow](/max-flow-problem/) value, and one search in the [residual graph](/residual-graph/) of a maximum flow finds a minimum cut. It is the model behind [image segmentation](/image-segmentation-graph-cuts/), [project selection](/maximum-weight-closure/) and many reliability questions.

## In plain words

You want to stop all traffic from one city to another on a road map with one-way roads. Each road has a price to close it. Which roads should you close so that no route is left, at the lowest total price?

Any such plan splits the cities into two groups: those you can still reach from the start, and the rest. The roads you must close are the ones that lead from the first group into the second. So the question is the same as: find a split into two groups, the start in one and the goal in the other, with the cheapest set of roads that go from the start's group to the other one. Roads that go the other way are free, because they do not help anyone leave the start's group.

## Definition

**Input.** A flow network $N = (G, c, s, t)$ with $G = (V, E)$ directed, capacities $c : E \to \mathbb{R}_{\ge 0}$ (real; integer in many uses), and $s \ne t$. Parallel edges, antiparallel edges and edges of capacity 0 are allowed.

**Output.** A set $S \subseteq V$ with $s \in S$ and $t \notin S$ that minimizes the [capacity](/cut-capacity/)

$$c(S) = \sum_{e = (u, v) \in E,\ u \in S,\ v \notin S} c(e).$$

The pair $(S, V \setminus S)$ is an [$s$-$t$ cut](/cut/). The minimum of $c(S)$ over the $2^{n-2}$ choices of $S$ is written $\lambda(s, t)$ or $\mathrm{mincut}(N)$.

**The edge-set form gives the same value.** Call $F \subseteq E$ an *$s$-$t$ separating set* if $G - F$ has no directed $s$-$t$ path. Then $\min_S c(S) = \min_F c(F)$. *Proof.* For each $S$, the set $F_S$ of edges from $S$ to $V \setminus S$ separates, since each $s$-$t$ path leaves $S$ along some edge, and $c(F_S) = c(S)$. Conversely, for a separating $F$, let $S$ be the set of vertices that $s$ reaches in $G - F$. Then $t \notin S$, and each edge from $S$ to $V \setminus S$ is in $F$ (otherwise its head would be reachable), so $c(S) \le c(F)$. $\square$

**Directed and undirected.** Only edges from $S$ to $T$ count; edges from $T$ to $S$ do not. For an undirected graph, replace each edge $\{u, v\}$ of capacity $k$ by the two directed edges $(u, v)$ and $(v, u)$; exactly one of them crosses from $S$ to $T$ when the edge is cut, so $c(S)$ becomes the usual undirected cut weight. An antiparallel pair counts once in each direction, and only the edge that leaves $S$ is paid.

**The structure of all minimum cuts.** The function $c$ is [submodular](/submodular-function/): $c(A) + c(B) \ge c(A \cup B) + c(A \cap B)$ for all $A, B \subseteq V$. *Proof.* Fix an edge $e = (u, v)$ and write $x_w = [w \in X]$ for a set $X$. The edge counts in $c(X)$ exactly when $x_u (1 - x_v) = 1$. For the four sets $A$, $B$, $A \cup B$, $A \cap B$, a check of the 16 cases of the bits $[u \in A], [u \in B], [v \in A], [v \in B]$ shows that the count of $e$ on the left side minus its count on the right side is 1 when $u \in A \setminus B$ and $v \in B \setminus A$, or $u \in B \setminus A$ and $v \in A \setminus B$, and 0 in each other case. Summing $c(e)$ times this difference over all edges gives $c(A) + c(B) - c(A \cup B) - c(A \cap B) = c(A \setminus B, B \setminus A) + c(B \setminus A, A \setminus B) \ge 0$. $\square$ So if $A$ and $B$ are minimum cuts, $c(A \cup B) + c(A \cap B) \le 2\lambda$ and each term is at least $\lambda$, so both are minimum cuts. The source sides of the minimum cuts are closed under union and intersection. In particular, there is a unique smallest one and a unique largest one.

## Variants

- **Value only.** The number $\lambda(s, t)$, which equals the maximum flow value.
- **Smallest and largest minimum cut.** After a maximum flow $f$, the set of vertices that $s$ reaches in $G_f$ is the smallest source side, and the complement of the set of vertices that reach $t$ in $G_f$ is the largest one.
- **Undirected $s$-$t$ cut.** As above, by doubling the edges.
- **Unit capacities.** The minimum number of edges whose removal separates $s$ from $t$, which by [Menger's theorem](/menger-theorem/) is the number of [edge-disjoint paths](/edge-disjoint-paths/).
- **Vertex cuts.** The fewest vertices whose removal separates $s$ from $t$: a [vertex cut](/vertex-cut/), found by [vertex splitting](/vertex-capacities-flow/).
- **Global minimum cut.** No $s$ and $t$ are given; the smallest cut over all pairs: [global min cut](/global-min-cut-problem/) and its [directed form](/directed-global-min-cut-problem/).
- **All pairs.** The minimum cut for each pair of vertices of an undirected graph, all stored in one [Gomory-Hu tree](/gomory-hu-tree/): the [all-pairs min cut problem](/all-pairs-min-cut-problem/).
- **More terminals.** Separating $k$ terminals from each other is the [multiway cut problem](/multiway-cut-problem/), and separating $k$ given pairs is the [multicut problem](/multicut-problem/). Both are NP-hard for $k \ge 3$.
- **Ratio objectives.** The [sparsest cut problem](/sparsest-cut-problem/) and [normalized cut](/normalized-cut/) divide the capacity by a measure of the sides, and are NP-hard.

## Examples

**The running example.** The network has the edges $s \to a$ (10), $s \to b$ (10), $a \to b$ (2), $a \to c$ (4), $a \to d$ (8), $b \to d$ (9), $d \to c$ (6), $c \to t$ (10), $d \to t$ (10). Of its 16 cuts, these are the cheapest:

| $S$ | edges from $S$ to $T$ | $c(S)$ |
|---|---|---|
| $\{s, b\}$ | $s \to a$, $b \to d$ | 19 |
| $\{s\}$ | $s \to a$, $s \to b$ | 20 |
| $\{s, a, b, d\}$ | $a \to c$, $d \to c$, $d \to t$ | 20 |
| $\{s, a, b, c, d\}$ | $c \to t$, $d \to t$ | 20 |
| $\{s, a, b\}$ | $a \to c$, $a \to d$, $b \to d$ | 21 |

The minimum is 19 and it is unique. For $S = \{s, b\}$ the edge $a \to b$ goes from $T$ to $S$ and costs nothing. The maximum flow value is also 19.

**Several minimum cuts.** In the network $s \to a$ (3), $s \to b$ (2), $a \to b$ (1), $a \to t$ (2), $b \to t$ (3), the cuts $\{s\}$, $\{s, a\}$ and $\{s, a, b\}$ all have capacity 5, and $\{s, b\}$ has 6. The smallest source side is $\{s\}$ and the largest is $\{s, a, b\}$. After the maximum flow that fills all edges, $s$ reaches only itself in the residual graph, and only $t$ reaches $t$.

**A zero-capacity edge.** If an edge $s \to t$ of capacity 0 is added, every cut contains it, and no cut value changes.

**No $s$-$t$ path.** If $s$ cannot reach $t$, the set $S$ of vertices that $s$ reaches is a cut with no edge from $S$ to $T$, so $\lambda(s, t) = 0$.

## Known algorithms

- **From a maximum flow.** Run any [maximum flow algorithm](/max-flow-problem/), then a [breadth-first](/breadth-first-search/) or [depth-first search](/depth-first-search/) from $s$ in the residual graph, in $O(n + m)$ more time. The bounds are those of maximum flow: $O(nm)$ strongly polynomial, $m^{1+o(1)} \log U$ for integer capacities.
- **From a preflow.** [Push-relabel](/push-relabel/) has a minimum cut at the end of its first phase, before it returns the excess to $s$; the cut is the set of vertices that can still reach $t$, complemented.
- **Planar graphs.** In an undirected planar graph with $s$ and $t$ given, a minimum $s$-$t$ cut is a shortest cycle in the [planar dual](/planar-dual-graph/) that separates the faces next to $s$ from those next to $t$.

## Bounds

The minimum cut problem and the maximum flow problem have the same value, and each converts to the other in $O(n + m)$ time once one side is known: a maximum flow gives a cut by one search, and a minimum cut certifies the flow. No algorithm is known that finds a minimum $s$-$t$ cut asymptotically faster than a maximum flow in general directed graphs. The lower bound is $\Omega(n + m)$: an unread edge could change the answer.

## Reductions

- **Min cut to max flow**, as above.
- **Maximum-weight closure to min cut.** Edges of capacity $\infty$ keep the closure condition, and source and sink edges carry the weights: [maximum-weight closure](/maximum-weight-closure/).
- **Binary labeling to min cut.** Minimizing $\sum_v D_v(x_v) + \sum_{uv} w_{uv} [x_u \ne x_v]$ over $x \in \{0, 1\}^V$ with $w_{uv} \ge 0$ is one minimum cut: [image segmentation](/image-segmentation-graph-cuts/). More generally, each submodular function of binary variables with terms of at most two variables reduces in this way.
- **Edge connectivity to min cut.** The [edge connectivity](/edge-connectivity/) of a graph is the minimum of $\lambda(s, t)$ over pairs, and $n - 1$ cut computations with one fixed $s$ suffice in undirected graphs.

## Applications

- Segmenting an image into foreground and background, and other labeling problems in vision.
- Choosing a set of projects with prerequisites, open-pit mining, and other closure problems.
- Finding the weakest part of a communication network, and testing [$k$-edge-connectivity](/k-edge-connected-graph/).
- Proving that a team is eliminated in [baseball elimination](/baseball-elimination/): the minimum cut is the certificate.

## References
