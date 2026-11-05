---
tag: PSCBG5
kind: algorithm
slug: gomory-hu-algorithm
name: Gomory-Hu tree algorithm
aliases:
- Gomory-Hu construction
area: graphs/flows-and-cuts
level: advanced
summary: Build a Gomory-Hu tree using n-1 max-flow computations.
solves: [all-pairs-min-cut-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, T: the time of one maximum flow computation on a graph with at most n vertices and m edges}
  time: {worst: O(n T + n m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1961
  people: [Ralph E. Gomory, T. C. Hu, Dan Gusfield]
  note: Gomory and Hu gave the contraction method and the cut tree in 1961; Gusfield gave a version without contraction in 1990.
prereqs: [all-pairs-min-cut-problem, max-flow-min-cut-theorem, graph-contraction]
see_also: [gomory-hu-tree, edmonds-karp, dinic, submodular-function, stoer-wagner, global-min-cut-problem, edge-connectivity]
sources:
  - paper: doi:10.1137/0109047
    title: Ralph E. Gomory and T. C. Hu, Multi-terminal network flows, Journal of the Society for Industrial and Applied Mathematics 9(4), 551 to 570 (1961)
    locator: the whole paper (the condensation of a tree node and the cut tree)
  - paper: doi:10.1137/0219009
    title: Dan Gusfield, Very simple methods for all pairs network flow analysis, SIAM Journal on Computing 19(1), 143 to 155 (1990)
    locator: the whole paper (the method without contraction)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition
    locator: Chapter 8, Network Flows, the section on Gomory-Hu trees (the algorithm and its proof by uncrossing)
---

The Gomory-Hu algorithm builds a [Gomory-Hu tree](/gomory-hu-tree/) of an undirected graph with nonnegative edge weights: a weighted tree on the same vertices in which the minimum cut between any two vertices equals the lightest edge on their tree path, and removing that edge gives a minimum cut. It solves the [all-pairs minimum cut problem](/all-pairs-min-cut-problem/) with only $n - 1$ maximum flow computations. It keeps a tree whose nodes are groups of vertices, and repeatedly splits a group by a minimum cut computed in a graph where the rest of the tree is [contracted](/graph-contraction/). Uncrossing of cuts shows that the contraction loses nothing.

## In plain words

Start with all places in one bag. Pick a bag with at least two places and two places in it. Treat each part of the tree hanging off this bag as a single big place. Find the cheapest way to separate the two chosen places in this simpler picture. That splits the bag in two, joined by a link labelled with the cost. Each part that hung off the old bag now hangs off the half it fell into. Repeat until every bag holds one place. The final tree answers every question of the form "how cheap is it to cut these two apart": follow the tree path and take the smallest label.

## The problem

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges and weights $w(e) \ge 0$, real numbers. Parallel edges and edges of weight 0 are allowed; self-loops do not affect any cut.

**Output.** A tree $T$ on $V$ with weights such that for every pair $u \ne v$, if $e$ is a lightest edge on the $u$-$v$ path of $T$, then $w_T(e) = \lambda(u, v)$, the minimum $u$-$v$ cut value of $G$, and the two vertex sets of $T - e$ form a minimum $u$-$v$ cut of $G$.

The graph is undirected. The maximum flow subroutine works on a directed graph, so each undirected edge is given to it as two antiparallel arcs $u \to v$ and $v \to u$ of capacity $w(e)$, each with its own residual pair. The algorithm does not apply to directed graphs, where no such tree exists in general.

## The algorithm

```pseudo id=main
GOMORY-HU(G, w)
L1  T ← a tree with a single node holding V
L2  while some node X of T holds at least two vertices do
L3      pick two vertices s ≠ t in X
L4      G_X ← G with the vertices of each component C of T − X contracted to one vertex v_C
L5      (λ, S) ← a minimum s-t cut of G_X, with s ∈ S
L6      X_s ← X ∩ S;  X_t ← X ∖ S
L7      replace X in T by the nodes X_s and X_t, joined by an edge of weight λ
L8      for each former tree edge (X, Y) with Y in component C do attach Y to X_s if v_C ∈ S, else to X_t, keeping its weight
L9  return T, with each node a single vertex
```

Line L4 builds the contracted graph: vertices of $X$ stay, each subtree hanging off $X$ becomes one vertex, edges inside a subtree vanish, and parallel edges between the same two vertices are kept. Line L5 runs any maximum flow algorithm and takes $S$ as the set reachable from $s$ in the final residual graph. Line L8 keeps each old tree edge but moves its end from $X$ to the half that lies on the same side of the cut as its subtree.

## Example

Take the six vertices $p, q, r, s, u, v$ and the undirected edges $p q$ 1, $p r$ 7, $q r$ 1, $q s$ 3, $q u$ 2, $r u$ 4, $s u$ 1, $s v$ 6, $u v$ 2. Each round takes the first two vertices of the first node with two or more vertices.

| round | node $X$ | $s$, $t$ | contracted vertices | $\lambda$ | $X_s$ | $X_t$ |
|---|---|---|---|---|---|---|
| 1 | $\{p, q, r, s, u, v\}$ | $p$, $q$ | none | 6 | $\{p, r\}$ | $\{q, s, u, v\}$ |
| 2 | $\{p, r\}$ | $p$, $r$ | $\{q, s, u, v\}$ | 8 | $\{p\}$ | $\{r\}$ |
| 3 | $\{q, s, u, v\}$ | $q$, $s$ | $\{p, r\}$ | 6 | $\{q, u\}$ | $\{s, v\}$ |
| 4 | $\{q, u\}$ | $q$, $u$ | $\{p, r\}$, $\{s, v\}$ | 7 | $\{q\}$ | $\{u\}$ |
| 5 | $\{s, v\}$ | $s$, $v$ | $\{p, q, r, u\}$ | 8 | $\{s\}$ | $\{v\}$ |

In round 1 the cut $\{p, r\}$ crosses $p q$, $q r$ and $r u$ for $1 + 1 + 4 = 6$. In round 2 the node $\{q, s, u, v\}$ is one vertex, which falls on the side of $r$, so it hangs off $\{r\}$. In round 3 the contracted vertex $\{p, r\}$ has edges of weight $1 + 1 = 2$ to $q$ and 4 to $u$; the cut $\{q, u\}$ plus the contracted vertex crosses $q s$, $s u$ and $u v$ for $3 + 1 + 2 = 6$, and the old edge from $\{r\}$ is attached to $\{q, u\}$. In round 4 the cut $\{q\}$ crosses edges of weight $2 + 3 + 2 = 7$ in the contracted graph, and the edge to $\{r\}$ moves to $\{u\}$, as does the edge to $\{s, v\}$. The final tree has the five edges $p r$ 8, $r u$ 6, $u q$ 7, $u s$ 6 and $s v$ 8.

For example $\lambda(p, q)$ is the least weight on $p\,r\,u\,q$, namely 6, and deleting the edge $r u$ splits $V$ into $\{p, r\}$ and $\{q, s, u, v\}$, a cut of capacity 6. The page on [all-pairs minimum cut](/all-pairs-min-cut-problem/) lists all 15 values; every one is a path minimum in this tree. Gusfield's method on the same graph builds a different tree with the same path minima.

**Edge cases.** If $G$ is disconnected, a round with $s$ and $t$ in different components finds $\lambda = 0$ and the cut is a union of components, so the tree joins the components by edges of weight 0. An edge of weight 0 never appears in a residual graph and changes no cut. With no edges at all, the tree is any spanning tree with all weights 0. With $n = 1$ the tree has no edges.

## Correctness

The proof in [the correctness proof](proofs/correctness.md) keeps the invariant that each tree edge $(X, Y)$ of weight $\lambda$ has a witness pair $x \in X$, $y \in Y$ with $\lambda(x, y) = \lambda$, and that the side of $T - (X, Y)$ containing $Y$ is a minimum $x$-$y$ cut of $G$. Two uncrossing steps, both from the submodularity of the cut function $c(A) + c(B) \ge c(A \cap B) + c(A \cup B)$, carry it through a split: some minimum $s$-$t$ cut of $G$ does not split any subtree, so the contraction of line L4 does not change $\lambda(s, t)$; and an old edge whose witness ends up in the other half gets $s$ or $t$ as its new witness, with the same value. At the end all nodes are single vertices, and the triangle inequality $\lambda(a, c) \ge \min(\lambda(a, b), \lambda(b, c))$ turns the edge values into path minima.

## Complexity

Each round splits one node into two nonempty halves, since $s \in X_s$ and $t \in X_t$, so there are exactly $n - 1$ rounds. A round builds $G_X$ in $O(n + m)$ time, by labelling the vertices of each subtree with a search in $T$, and runs one maximum flow on a graph with at most $n$ vertices and $m$ edges. With $T$ the time of one maximum flow, the total is $O(nT + nm)$. The Python version uses shortest augmenting paths, so $T = O(nm^2)$ and the total is $O(n^2 m^2)$; with [Dinic](/dinic/) it is $O(n^3 m)$, and with a near-linear maximum flow it is $m^{1 + o(1)} n$. Space is $O(n + m)$ besides the flow routine.

## Properties

- **Exactly $n - 1$ maximum flows**, against $\binom{n}{2}$ for one flow per pair.
- **Flows on smaller graphs.** The contracted graphs are often much smaller than $G$, which helps in practice.
- **Any choice of $s$, $t$ and minimum cut works.** Different choices give different trees with the same path minima.
- **Deterministic** given a deterministic flow routine.
- **Undirected only.** The proof uses the symmetry $c(A) = c(V \setminus A)$ of the cut function.

## Variants and improvements

- **Gusfield's method (1990).** Every flow is run on $G$ itself, with no contraction, and a parent array is updated after each cut. It is simpler to code and also gives a cut tree; it is the construction used on the page [Gomory-Hu tree](/gomory-hu-tree/).
- **Equivalent flow trees.** If only the values are needed, a tree whose path minima match $\lambda$ but whose edges need not give minimum cuts is enough, and Gusfield's simplest version builds one.
- **Fewer than $n - 1$ flows.** From 2020 on, Abboud, Krauthgamer, Li, Panigrahi, Saranurak, Trabelsi and others found Gomory-Hu trees with polylogarithmically many maximum flow calls in expectation, first for unweighted and then for weighted graphs, reaching almost-linear time with the [almost-linear maximum flow](/almost-linear-max-flow/) algorithm.
- **Hypergraphs and symmetric submodular functions.** The construction works for any symmetric submodular cut function, for example hypergraph cuts.

## When to use it

Use it when many pairwise cut values of one undirected graph are needed, for example in network reliability, in clustering, or to separate cut inequalities in integer programming. For a single pair, one maximum flow is enough. For the global minimum cut alone, [Stoer-Wagner](/stoer-wagner/) or [Karger's algorithm](/karger-min-cut/) is simpler. For directed graphs it does not apply.

## Pitfalls

- **Contract the subtrees, not the whole rest.** Each component of $T - X$ becomes its own vertex; merging them all into one vertex gives wrong cut values.
- **Reattach by the side of the contracted vertex**, not by the side of the old witness.
- **Undirected edges as two arcs.** Giving the flow routine a single arc per edge computes directed cuts, which are wrong here.
- **Take the cut from the final residual graph.** The set reachable from $s$ is a minimum cut; an arbitrary set of saturated edges is not.
- **Directed graphs.** Running the method on a directed graph returns a tree, but its path minima are not the directed cut values.

## Implementations

The Python version takes the vertex count and a list of undirected edges $(u, v, w)$ and returns the $n - 1$ tree edges $(a, b, \lambda)$ with $a < b$. Weights may be `int`, `Fraction` or `float`. It picks the first two vertices of the first node with two or more vertices, runs shortest augmenting paths on the contracted graph, and an optional callback reports each split.

## History

Ralph Gomory and T. C. Hu published the method in 1961, in the paper that showed that the $\binom{n}{2}$ minimum cut values of an undirected network take at most $n - 1$ distinct values and fit in one tree. Dan Gusfield showed in 1990 that the contractions can be avoided. Since 2020 a line of work has reduced the number of maximum flow calls far below $n - 1$.

## References
