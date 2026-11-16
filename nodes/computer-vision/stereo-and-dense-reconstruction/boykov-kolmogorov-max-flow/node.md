---
tag: FXPM4P
kind: algorithm
slug: boykov-kolmogorov-max-flow
name: Boykov-Kolmogorov max-flow algorithm
aliases:
- BK max-flow
- BK algorithm
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: An augmenting path max-flow algorithm that grows search trees from the source and the sink and repairs them after each augmentation instead of starting again. Fast on vision grids.
solves: [max-flow-problem, min-cut-problem]
model: word-ram
complexity:
  vars: {n: the number of nodes, m: the number of edges, C: the capacity of a minimum cut with integer capacities}
  time: {worst: O(m n C), average: O(m n C), best: O(n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2004
  people: [Yuri Boykov, Vladimir Kolmogorov]
  note: Boykov and Kolmogorov designed the algorithm for the graphs of energy minimization in vision, and compared it with Dinic and push-relabel codes on segmentation, stereo and restoration graphs, where it was faster in most tests.
prereqs: [max-flow-min-cut-theorem, ford-fulkerson, residual-graph]
see_also: [push-relabel, dinic, edmonds-karp, graph-representable-energies, alpha-expansion, image-segmentation-graph-cuts, boykov-jolly-graph-cuts, augmenting-path]
sources:
  - paper: doi:10.1109/TPAMI.2004.60
    title: Yuri Boykov and Vladimir Kolmogorov, An experimental comparison of min-cut/max-flow algorithms for energy minimization in vision, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(9), 2004, 1124-1137
    locator: Section 3 (the algorithm and the bound O(mn^2|C|)), Section 3.2 (growth, augmentation and adoption stages), Section 3.3 (implementation details), Section 4 (experiments on vision graphs)
  - paper: doi:10.1109/TPAMI.2007.70844
    title: Richard Szeliski, Ramin Zabih, Daniel Scharstein, Olga Veksler, Vladimir Kolmogorov, Aseem Agarwala, Marshall Tappen and Carsten Rother, A comparative study of energy minimization methods for Markov random fields with smoothness-based priors, IEEE Transactions on Pattern Analysis and Machine Intelligence 30(6), 2008, 1068-1080
    locator: the graph cut methods of the comparison, which use this max-flow code
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 4, Model fitting and optimization (graph cuts for Markov random fields)
---

The Boykov-Kolmogorov algorithm computes a maximum flow and a minimum cut of a directed graph with a source $s$ and a sink $t$. It is an [augmenting path](/augmenting-path/) method in the family of [Ford-Fulkerson](/ford-fulkerson/), but it does not search for each path from the start. It keeps two search trees in the [residual graph](/residual-graph/): the S tree grows from the source, and the T tree grows into the sink. When the trees touch, the path through the meeting edge is augmented. The saturated edges break the trees into pieces, and the pieces are joined back to the trees by an adoption step, so most of the search work is reused. The worst case bound is weaker than that of [Edmonds-Karp](/edmonds-karp/), [Dinic](/dinic/) or [push-relabel](/push-relabel/), but on the grid graphs of vision, with a few edges per pixel and many short paths, the algorithm was faster than those codes in the experiments of Boykov and Kolmogorov (2004). It is the usual solver for the cuts of [alpha-expansion](/alpha-expansion/), [graph cut segmentation](/image-segmentation-graph-cuts/) and the other [graph-representable energies](/graph-representable-energies/).

## In plain words

Water must go from a source to a sink through pipes. Two teams explore the network. One team starts at the source and the other at the sink, and each team keeps a tree of the pipes it has used to reach places. When the two teams meet, there is a route from the source to the sink, and you send as much water along it as the narrowest pipe allows. That pipe is now full, so some places lose their route back to their team. Instead of starting over, each lost place looks at its neighbors for another way back. Only places with no way back are given up. When the teams can no longer meet, the places the source team holds are the cheapest cut.

## The problem

**Input.** A directed graph with $n$ nodes and $m$ edges, two nodes $s \ne t$, and a capacity $c(u, v) \ge 0$ on each edge. Parallel and opposite edges are allowed.

**Output.** A [maximum flow](/max-flow-problem/) from $s$ to $t$, and a [minimum cut](/min-cut-problem/), given as its source side $S$.

The residual capacity of an edge $u \to v$ is $r(u \to v) = c(u, v) - f(u, v) + f(v, u)$: the code stores each edge with its reverse and moves capacity between them. Each node is in the S tree, in the T tree, or free. In the S tree the parent edge of $q$ is an edge $p \to q$ with $r > 0$, and in the T tree it is an edge $q \to p$ with $r > 0$. Active nodes, in a FIFO queue $A$, are the nodes of the trees that may still grow. Orphans, in a list $O$, are nodes that lost their parent edge.

## The algorithm

```pseudo id=main
BK-MAX-FLOW(G, s, t)
L1   tree[s] ← S; tree[t] ← T; tree[v] ← free for the other nodes; parent[s], parent[t] ← terminal
L2   A ← (s, t); O ← empty; flow ← 0
L3   loop
L4       e ← GROW()                                 ▷ an edge from an S node to a T node, or nil
L5       if e = nil then return flow and the cut S = {v : tree[v] = S}
L6       P ← the parent edges from s to the tail of e, then e, then the parent edges to t
L7       Δ ← the least residual capacity on P; push Δ along P; flow ← flow + Δ
L8       for each edge of P except e that is now saturated do
L9           if it is an S edge p → q then parent[q] ← none; add q to O
L10          if it is a T edge p → q then parent[p] ← none; add p to O
L11      while O is not empty do take p from O; ADOPT(p)

GROW()
L12  while A is not empty do
L13      p ← the front of A; if tree[p] = free then remove it and go to the next node
L14      for each neighbor q with r(p → q) > 0 if p is in S, or r(q → p) > 0 if p is in T do
L15          if tree[q] = free then tree[q] ← tree[p]; parent[q] ← the edge between p and q; add q to A
L16          else if tree[q] ≠ tree[p] then return the edge between p and q, directed from S to T
L17      remove p from A
L18  return nil

ADOPT(p)
L19  for each neighbor q in the tree of p, with r(q → p) > 0 in S or r(p → q) > 0 in T do
L20      if the parent edges from q reach a terminal then parent[p] ← that edge; return
L21  for each neighbor q in the tree of p do
L22      if r(q → p) > 0 in S, or r(p → q) > 0 in T then add q to A
L23      if parent[q] is the edge between p and q then parent[q] ← none; add q to O
L24  tree[p] ← free
```

The main loop has three stages, the same as in Section 3.2 of the paper. Growth (lines L12 to L18) is a [breadth-first search](/breadth-first-search/) from both terminals at once over the residual graph; it stops at the first edge that joins the trees and keeps the node at the front of $A$, so the next growth stage starts from where it stopped. Augmentation (lines L6 to L10) pushes the bottleneck along the path. The saturated edges are cut out of the trees, and the nodes below them become orphans. Adoption (lines L19 to L24) gives each orphan a new parent in its own tree if one exists with a residual edge and a chain to the terminal; otherwise the orphan becomes free, its children become orphans, and its neighbors that could reach it become active again so that a later growth stage can take it back.

## Example

Take $s$, $a$, $b$, $t$ and the edges $s \to a$ of capacity 3, $s \to b$ of 2, $a \to b$ of 1, $a \to t$ of 2 and $b \to t$ of 3, scanned in this order.

| step | stage | what happens | flow |
|---|---|---|---|
| 1 | growth | $s$ adds $a$ and $b$ to S; $t$ finds the S node $a$ through $a \to t$ | 0 |
| 2 | augment | path $s \to a \to t$, $\Delta = 2$; $a \to t$ is the bridge, so no orphan | 2 |
| 3 | growth | $t$ finds the S node $b$ through $b \to t$ | 2 |
| 4 | augment | path $s \to b \to t$, $\Delta = 2$; $s \to b$ is saturated, $b$ is an orphan | 4 |
| 5 | adopt | $b$ takes $a$ as parent through $a \to b$ (residual 1), since $a$ hangs from $s$ | 4 |
| 6 | growth | $t$ finds $b$ through $b \to t$ (residual 1) | 4 |
| 7 | augment | path $s \to a \to b \to t$, $\Delta = 1$; $s \to a$ and $a \to b$ are saturated, $b$ and $a$ are orphans | 5 |
| 8 | adopt | $b$ and then $a$ find no parent in S and become free | 5 |
| 9 | growth | $t$ has no residual edge from a free or S node, and $A$ empties | 5 |

The maximum flow is 5, and the final S tree is $\{s\}$, the cut $s \to a$, $s \to b$ of capacity $3 + 2 = 5$. Step 5 is the point of the method: the tree of step 1 is repaired, not built again.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It keeps three invariants: the stored capacities are the residual capacities of a feasible flow; every tree edge has positive residual capacity in the direction of its tree, and the parent edges lead to the terminal without a cycle; and a passive S node has all its residual out-neighbors in S, a passive T node all its residual in-neighbors in T. Growth keeps them because a node leaves $A$ only after all its neighbors were seen. Augmentation keeps them because saturated tree edges make orphans, and the new reverse edges either join two nodes of the same tree or leave T toward S. Adoption keeps them because a new parent must have a chain to the terminal, which cannot pass through the orphan, and because a node that becomes free activates every neighbor that the third invariant could break. At the end $A$ is empty, so no residual edge leaves the S tree. Then the edges out of the S tree are saturated and the edges into it are empty, the flow value equals the cut capacity, and by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) both are optimal.

## Complexity

The model is the [word RAM](/word-ram/) with integer capacities.

- **Augmentations.** Each augmentation adds at least 1, and the flow is at most the minimum cut capacity $C$, so there are at most $C$ augmentations. This is the bound of the paper, Section 3.
- **Work between two augmentations.** A growth stage scans each node at most once, in $O(n + m)$ time. In an adoption stage each node is an orphan at most once, and each candidate parent costs a walk of at most $n$ nodes to check its chain, so the stage takes $O(m n)$ time.
- **Total.** $O(m n C)$ time. Boykov and Kolmogorov state $O(m n^2 C)$; the count in the proof is a little finer. Both depend on $C$, so the algorithm is not even polynomial, while Dinic takes $O(n^2 m)$ and push-relabel $O(n^3)$ or better.
- **In practice.** The paper measured it on segmentation, stereo and restoration graphs and found it faster than Dinic and the push-relabel codes of the time in most of the tests. This is an observation on those graphs, not a bound: the trees are shallow, paths are short, and adoption usually finds a parent nearby.
- **Space.** Two arrays of $2m$ edges for the residual graph, and $O(n)$ for the trees, the queue and the orphan list.

## Properties

- **Exact.** It returns a maximum flow and a minimum cut, like every Ford-Fulkerson method on integer capacities.
- **Not strongly polynomial.** The bound depends on $C$. With irrational capacities a Ford-Fulkerson method need not stop, and this one has no special protection against that.
- **Paths are not shortest.** The first path found by a fresh search is shortest, but after adoption the trees are not breadth-first trees, so the paths can be long. This is why the bound of Edmonds-Karp does not apply.
- **Source side.** The final S tree is the set of nodes that $s$ reaches in the residual graph, which is the smallest source side of a minimum cut.

## Variants and improvements

- **Distance and time stamps.** The code of the authors marks the nodes whose chain to a terminal was checked in the current stage, with their distance to the terminal, so that a later walk can stop early and an orphan can prefer a close parent (Section 3.3 of the paper).
- **Reuse between cuts.** In alpha-expansion and in interactive segmentation many cuts are solved on graphs that differ a little. Kohli and Torr (2007) reuse the flow and the trees of the last cut ("dynamic graph cuts").
- **Incremental breadth-first search.** Goldberg, Hed, Kaplan, Tarjan and Werneck (2011) keep the trees breadth-first and get a strongly polynomial bound with similar speed on vision graphs.
- **Grid codes.** For regular grids, the neighbors can be computed instead of stored, which saves memory on large volumes.

## When to use it

Use it for the min cuts of energy minimization in vision and graphics: [graph cut segmentation](/image-segmentation-graph-cuts/), [Boykov-Jolly](/boykov-jolly-graph-cuts/) interactive segmentation, the moves of [alpha-expansion](/alpha-expansion/) and [alpha-beta swap](/alpha-beta-swap/), and [QPBO](/qpbo/). Use [push-relabel](/push-relabel/) or a pseudoflow code on large graphs with long paths, such as dense 3D grids with many neighbors, and use a strongly polynomial method when a worst case guarantee matters.

## Pitfalls

- **Floating point capacities.** A small residual capacity can stay positive after an augmentation by rounding, and the loop can then make very many tiny augmentations. Scale the energies to integers, or treat capacities below a tolerance as zero.
- **The origin walk.** Without marks, each adoption walks the whole chain to the terminal. On deep trees this makes adoption slow. Use the time stamps of the paper.
- **Infinite capacities.** Hard constraints are often written as infinite edges. Use a large finite number that is larger than the sum of all finite capacities, and check that no path of only such edges joins $s$ and $t$.
- **Reading the cut.** The source side is the S tree, not the set of free nodes plus S. Free nodes at the end belong to the sink side.
- **Speed claims.** The speed is measured on grid graphs. Do not expect the same speed on graphs with long paths or high degree.

## Implementations

## History

Augmenting path methods go back to Ford and Fulkerson (1956), and the strongly polynomial methods of Edmonds and Karp (1972), Dinic (1970) and Goldberg and Tarjan (1988) followed. Greig, Porteous and Seheult (1989) brought minimum cuts to image analysis, and the work of Boykov, Veksler and Zabih (2001) made cuts a standard tool for vision energies. Boykov and Kolmogorov (2004) designed this algorithm for such graphs and published an experimental comparison with Dinic and push-relabel codes. Their code became the default solver in the vision literature and was used in the benchmark of Szeliski et al. (2008).

## References
