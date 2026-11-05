---
tag: SJPT89
kind: problem
slug: maximum-weight-closure
name: Maximum-weight closure problem
aliases:
- maximum weight closure
- project selection problem
area: graphs/flows-and-cuts
level: core
summary: Choose a precedence-closed set of vertices of maximum total weight, solvable by min-cut.
prereqs: [min-cut-problem, max-flow-problem, directed-acyclic-graph]
see_also: [parametric-max-flow-problem, image-segmentation-graph-cuts, max-flow-min-cut-theorem, submodular-minimization, topological-sort, baseball-elimination]
sources:
  - paper: doi:10.1287/mnsc.22.11.1268
    title: Jean-Claude Picard, Maximal closure of a graph and applications to combinatorial problems, Management Science 22(11), 1268 to 1272 (1976)
    locator: the whole paper (the reduction of maximum closure to a minimum cut)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.11, Project Selection
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 11, Applications of Flows and Cuts (project selection)
  - paper: doi:10.1287/opre.1080.0524
    title: Dorit S. Hochbaum, The pseudoflow algorithm, a new algorithm for the maximum-flow problem, Operations Research 56(4), 992 to 1009 (2008)
    locator: the whole paper (the pseudoflow algorithm, developed for the maximum closure problem and open-pit mining)
---

The maximum-weight closure problem asks, in a directed graph with a real weight on each vertex, for a set $C$ of vertices that is closed under the edges (if $u \in C$ and $u \to v$ is an edge, then $v \in C$) and has the largest total weight. Edges are prerequisites: choosing $u$ forces choosing $v$. Positive weights are profits and negative weights are costs. Picard showed in 1976 that it is one [minimum $s$-$t$ cut](/min-cut-problem/) in a network with an edge of infinite capacity for each prerequisite, so it is solved by one [maximum flow](/max-flow-problem/). It is also called project selection, and it models open-pit mining, the choice of a densest part of a graph, and the elimination test of [baseball elimination](/baseball-elimination/).

## In plain words

A company can run some projects, and each one earns money. But each project needs some tools, and each tool costs money to buy. Two projects can share a tool, and a tool needs to be bought only once. Which projects should the company run to make the most profit?

Make a list of all the items, projects and tools, with a value on each: a gain for a project, a loss for a tool. Draw an arrow from each item to each item it needs. A valid choice is a set of items that contains everything that any of its members needs. The task is to find the valid choice with the largest total value. The trick is that this is exactly the problem of cutting a pipe network as cheaply as possible.

## Definition

**Input.** A directed graph $D = (V, A)$ with $n$ vertices and $m$ edges and weights $w : V \to \mathbb{R}$; weights may be positive, negative or 0. Cycles, parallel edges and antiparallel edges are allowed. Integer weights are the common case, but the reduction works for real weights.

**Closure.** A set $C \subseteq V$ is a closure if no edge leaves it: for each $(u, v) \in A$, $u \in C$ implies $v \in C$. The empty set and $V$ are closures.

**Output.** A closure $C$ that maximizes $w(C) = \sum_{v \in C} w(v)$. The optimum is at least 0, by the empty set.

**The reduction to a minimum cut.** Build a network $N$ on $V \cup \{s, t\}$:

- an edge $s \to v$ of capacity $w(v)$ for each $v$ with $w(v) > 0$;
- an edge $v \to t$ of capacity $-w(v)$ for each $v$ with $w(v) < 0$;
- an edge $u \to v$ of capacity $\infty$ for each $(u, v) \in A$. Any number larger than $W^{+} = \sum_{w(v) > 0} w(v)$ works in place of $\infty$.

**Claim.** For $C \subseteq V$, the cut $S = \{s\} \cup C$ has finite capacity if and only if $C$ is a closure, and then $c(S) = W^{+} - w(C)$. So a minimum cut $S^{*}$ gives the maximum closure $C^{*} = S^{*} \setminus \{s\}$, of weight $W^{+} - \lambda(s, t)$.

*Proof.* An edge of infinite capacity leaves $S$ exactly when $u \in C$ and $v \notin C$ for some $(u, v) \in A$, that is, when $C$ is not a closure. If $C$ is a closure, the edges that leave $S$ are $s \to v$ for the positive vertices $v \notin C$ and $v \to t$ for the negative vertices $v \in C$. Their total is $\sum_{v \notin C,\ w(v) > 0} w(v) - \sum_{v \in C,\ w(v) < 0} w(v) = W^{+} - w(C)$. $\square$

## Variants

- **Minimum-weight closure.** Negate the weights.
- **The smallest and the largest optimal closure.** The source sides of the minimum cuts are closed under union and intersection, so among the optimal closures there is a smallest and a largest; both are read from the [residual graph](/residual-graph/) of a maximum flow.
- **Closure in a DAG.** If $D$ has a cycle, its vertices are all in or all out of every closure, so each strongly connected component can be merged into one vertex with the sum of the weights; the problem on a [directed acyclic graph](/directed-acyclic-graph/) remains.
- **Parametric closure.** If the weights depend linearly on a parameter $\lambda$, such as $w(v) = a(v) - \lambda b(v)$ with $b \ge 0$, the optimal closures are nested as $\lambda$ grows. All of them, and the best ratio $a(C) / b(C)$, come from one [parametric maximum flow](/parametric-max-flow-problem/).
- **Selection problem.** Items with profits and resources with costs, each item needing some resources, is the bipartite case shown below.

## Examples

**Projects and tools.** Projects $p_1$ (+15) and $p_2$ (+8); tools $t_1$ (−6), $t_2$ (−7), $t_3$ (−4); $p_1$ needs $t_1$ and $t_2$, and $p_2$ needs $t_2$ and $t_3$.

| closure | weight |
|---|---|
| $\emptyset$ | 0 |
| $\{p_1, t_1, t_2\}$ | 2 |
| $\{p_2, t_2, t_3\}$ | −3 |
| $\{p_1, p_2, t_1, t_2, t_3\}$ | 6 |

The best choice runs both projects, though $p_2$ alone loses money: $p_2$ shares $t_2$ with $p_1$. In the network, $W^{+} = 23$ and the maximum flow is 17: it fills all three tool edges $t_i \to t$ (6, 7 and 4) while $s \to p_1$ carries 13 and $s \to p_2$ carries 4. The minimum cut is $S = \{s, p_1, p_2, t_1, t_2, t_3\}$, of capacity $6 + 7 + 4 = 17$, and $23 - 17 = 6$.

**A cycle.** With the edges $u \to v$ and $v \to u$, an antiparallel pair, a closure holds both or neither, so only $w(u) + w(v)$ matters. The two edges of capacity $\infty$ in the network enforce this from both sides.

**Zero weights.** A vertex of weight 0 has no edge to $s$ or $t$. It sits on either side, depending on its neighbors, without changing the value.

**No $s$-$t$ path.** If no positive vertex can reach a negative vertex along $A$, the network has no $s$-$t$ path, the maximum flow is 0, and the answer is all vertices that are not able to reach a negative vertex, of weight $W^{+}$.

**All weights negative.** Then $W^{+} = 0$, $s$ has no edges, and the answer is $\emptyset$.

## Known algorithms

- **One minimum cut.** Build $N$ with $n + 2$ vertices and at most $n + m$ edges, and run any [maximum flow algorithm](/max-flow-problem/); the vertices that $s$ reaches in the final residual graph, minus $s$, form a maximum closure. With [push-relabel](/push-relabel/) or [Dinic](/dinic/) this is $O(n^2 \sqrt{m})$ or $O(n^2 m)$; with Orlin's algorithm it is $O(nm)$.
- **Pseudoflow.** Hochbaum's pseudoflow algorithm was designed for this problem and for open-pit mining, and solves the closure problem directly; it also solves the parametric version.
- **Lerchs-Grossmann.** The classical method of the mining industry, a combinatorial algorithm for maximum closure in mine block models.

## Bounds

The problem has the same complexity as minimum $s$-$t$ cut, up to $O(n + m)$ work for the reduction. With integer weights, the best known bounds are those of maximum flow, now $m^{1 + o(1)} \log W$ by the [almost-linear max-flow algorithm](/almost-linear-max-flow/). The problem is a special case of [submodular minimization](/submodular-minimization/), since $W^{+} - w(C)$ plus an infinite penalty for leaving edges is a cut function.

## Reductions

- **To minimum cut,** as in the definition.
- **Densest subgraph.** Deciding whether a graph has a subgraph with more than $\lambda$ edges per vertex is a closure problem: one vertex of weight 1 for each edge, needing its two ends, each of weight $-\lambda$. Searching over $\lambda$ gives the densest subgraph by [parametric max flow](/parametric-max-flow-problem/).
- **Baseball elimination.** The elimination of a team is decided by a flow network of the same form, and the certificate set is a closure; see [baseball elimination](/baseball-elimination/).
- **Binary labeling.** Each energy with unary terms and nonnegative pair terms $w_{uv} [x_u \ne x_v]$ is a minimum cut as in [image segmentation](/image-segmentation-graph-cuts/); with infinite pair terms only in one direction, it is a closure.

## Applications

- **Open-pit mining.** Blocks of ore have values, and a block can be dug only after the blocks above it in a cone; the maximum closure is the best final pit.
- **Project selection,** as in the example, and the choice of features or tasks with shared costs.
- **Scheduling with precedences.** Jobs that must come before others in a partial order, with a profit for each job that is done.
- **Densest subgraphs and ratio problems,** through parametric versions.

## References
