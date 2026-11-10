---
tag: A3D0QP
kind: algorithm
slug: parallel-dfs
name: Parallel depth-first search
aliases:
- parallel DFS
- lexicographic DFS by path relaxation
area: parallel/parallel-graph-algorithms
level: research
summary: The DFS order fixed by the adjacency lists is P-complete. Some DFS tree can be found in randomized polylog time (Aggarwal and Anderson), and in NC on planar graphs.
solves: [graph-exploration]
model: crew-pram
complexity:
  vars: {n: the number of vertices, m: the number of edges, h: the height of the DFS tree}
  time: {worst: O(m h^2 + n h log n)}
  depth: {worst: O(h log^2 n)}
  space: {extra: O(n h + m)}
properties: {deterministic: true, recursive: false}
prereqs: [depth-first-search, white-path-theorem, edge-classification, lexicographic-order, crew-pram]
see_also: [parallel-bfs, nc, rnc-perfect-matching, tarjan-vishkin, forward-backward-scc, coloring-scc, dfs-forest, parenthesis-theorem]
sources:
  - paper: doi:10.1016/0020-0190(85)90024-9
    title: John H. Reif, Depth-first search is inherently sequential, Information Processing Letters 20(5), 1985
    locator: the main theorem (the lexicographically first DFS order is P-complete)
  - paper: doi:10.1007/BF02122548
    title: Alok Aggarwal and Richard J. Anderson, A random NC algorithm for depth first search, Combinatorica 8(1), 1988
    locator: the main theorem (an RNC algorithm for a DFS tree of an undirected graph, with minimum-weight perfect matching as a subroutine)
  - paper: "Alok Aggarwal, Richard J. Anderson and Ming-Yang Kao, Parallel depth-first search in general directed graphs, SIAM Journal on Computing 19(2), 1990"
    title: Parallel depth-first search in general directed graphs
    locator: the main theorem (an RNC algorithm for a DFS tree of a directed graph); volume and pages to be checked
  - paper: "Justin R. Smith, Parallel algorithms for depth-first searches I. Planar graphs, SIAM Journal on Computing 15(3), 1986"
    title: Parallel algorithms for depth-first searches I. Planar graphs
    locator: the main theorem (DFS of an undirected planar graph in NC); pages to be checked
  - book: isbn:9780195085914
    title: Raymond Greenlaw, H. James Hoover and Walter L. Ruzzo, Limits to Parallel Computation, P-Completeness Theory, Oxford University Press, 1995
    locator: the entry for the lexicographically first DFS ordering in the list of P-complete problems; entry number to be checked
---

Parallel depth-first search is the problem of computing a [depth-first search](/depth-first-search/) order or tree with many processors at the same time. The DFS that the sequential algorithm returns, with each adjacency list scanned in order, is P-complete (Reif, 1985), so no polylogarithmic-time parallel algorithm for it is expected; some DFS tree, not a fixed one, can be found in randomized polylogarithmic time (Aggarwal and Anderson, 1988), but with a large polynomial amount of work. This page proves a simple method that computes the sequential DFS exactly in $h + 1$ synchronous rounds, where $h$ is the height of the DFS tree, and it gives the cost of the known results.

Notation on this page: $n$ is the number of vertices, $m$ the number of edges, $h$ the height of the DFS tree (the most edges on a tree path from the source), $W$ the work, $S$ the span and $T_p$ the time on $p$ processors. The model is the synchronous CREW PRAM: many processors may read one cell in a step, but each cell has at most one writer. The method on this page is a direct consequence of the [white-path theorem](/white-path-theorem/); it is proved here and not taken from one of the cited papers.

## In plain words

A depth-first search walks as deep as it can, and it goes back only when it is stuck. Each step depends on the whole walk so far, so the search is hard to split among many workers.

The method on this page gives each vertex a label that spells a route from the start: the list of the edge choices made on the way. In each round, every vertex reads the labels of the vertices that point to it, adds one more choice, and keeps the smallest label in dictionary order. Early labels can be wrong, but they only get smaller. After as many rounds as the depth of the search tree, they are exactly the routes of the sequential search, and sorting by label gives the search order. On a deep tree this takes as many rounds as there are vertices.

## The problem

The input is a graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, given as ordered adjacency lists (an undirected graph lists each edge at both ends), and a source $s$. The output is the preorder and the parent array of the DFS from $s$ that the sequential algorithm returns when it scans each list from the first entry to the last. This is the lexicographically first DFS. For a reachable $v$, write $T(v)$ for the sequence of list positions along the tree path from $s$ to $v$: if the path is $s = x_0, x_1, \ldots, x_k = v$ and $x_{j+1}$ is entry $i_j$ of the list of $x_j$, then $T(v) = (i_0, \ldots, i_{k-1})$. Sequences are compared in [lexicographic order](/lexicographic-order/), with a proper prefix before its extensions.

## The algorithm

Each round is one synchronous step: every vertex reads the labels of the round before, then all vertices write their new labels. The label $P[v]$ is a sequence of list positions that spells a walk from $s$ to $v$.

```pseudo id=main
PARALLEL-LEX-DFS(G, s)
L1  for all v in parallel do P[v] ← nil, parent[v] ← nil
L2  P[s] ← ( ), parent[s] ← s, changed ← true
L3  while changed do
L4      for all v ≠ s in parallel do
L5          Q[v] ← lex-min of {P[v]} ∪ {P[u]·i : v is entry i of adj[u], P[u] ≠ nil}, parent[v] ← the u of the minimum
L6      changed ← (Q[v] ≠ P[v] for some v)
L7      P ← Q
L8  R ← the vertices v with P[v] ≠ nil
L9  order ← R sorted by P in lexicographic order
L10 return order, parent
```

Line L5 reads only labels of the round before, so a vertex that changes in this round is not seen by the others until the next round. Line L6 is an OR over $n$ flags. Line L9 is a parallel comparison sort, for example [Cole's merge sort](/cole-merge-sort/), with one comparison of two labels as the basic step.

## Example

The directed graph has 4 vertices and the lists $adj[0] = [2, 1]$, $adj[1] = [3]$, $adj[2] = [1, 3]$, $adj[3] = [0]$, with source 0. The sequential DFS visits 0, then 2 (entry 0 of $adj[0]$), then 1 (entry 0 of $adj[2]$), then 3 (entry 0 of $adj[1]$). Its tree is the path $0, 2, 1, 3$, so $h = 3$.

| round | $P[1]$ | $P[2]$ | $P[3]$ | what changed |
|---|---|---|---|---|
| 1 | (1) | (0) | nil | 1 and 2 are reached from 0 |
| 2 | (0, 0) | (0) | (0, 1) | 1 is reached through 2; 3 is reached through 2 |
| 3 | (0, 0) | (0) | (0, 0, 0) | 3 is reached through 1, which is smaller |
| 4 | (0, 0) | (0) | (0, 0, 0) | nothing, the loop stops |

The labels in round 2 are not final: vertex 3 has parent 2 there, and gets its DFS parent 1 only in round 3. There are $h + 1 = 4$ rounds. Sorting by the labels $() < (0) < (0, 0) < (0, 0, 0)$ gives the preorder $0, 2, 1, 3$ and the parents $parent[1] = 2$, $parent[2] = 0$, $parent[3] = 1$.

## Correctness

Write $x \sqsupseteq y$ when $x = y$ or when $x$ and $y$ first differ at a position where $x$ has the larger entry. The proof shows the invariant $P[v] = nil$ or $P[v] \sqsupseteq T(v)$ for every vertex after every round. The DFS facts it needs come from the [edge classification](/edge-classification/): for an edge $(u, v)$ that is entry $i$ of $adj[u]$, the sequence $T(u) \cdot i$ equals $T(v)$ for a tree edge, is $\sqsupseteq T(v)$ for a forward or a cross edge, and has $T(v)$ as a proper prefix for a back edge. In the back edge case, a label that extends $T(v)$ can only appear after $P[v] = T(v)$ is already held, because each prefix of a label was the label of its end vertex in an earlier round. So no label ever drops below $T(v)$. Since the parent of $v$ offers exactly $T(v)$ once its own label is final, $P[v] = T(v)$ after round $\operatorname{depth}(v)$, and the loop stops after round $h + 1$. Sorting by $T$ gives the preorder, because two vertices that are not on one tree path first differ at a common ancestor $z$, and $z$ finishes the subtree of its smaller entry before it reads the larger one. The full proof is in the proof file.

## Complexity

The model is the CREW PRAM. These bounds are proved on this page.

- **Rounds.** Exactly $h + 1$. After round $r$ every label has at most $r$ entries, so a vertex at depth $h$ is not final before round $h$, and the loop cannot stop earlier: a round with no change is a fixed point, and the labels reach $T$ only at round $h$.
- **One round.** Every edge forms one candidate of length at most $h$, and every vertex takes the minimum over its in-edges by a tournament of $O(\log n)$ levels. One comparison of two sequences of length at most $h$ is an OR and a minimum over their positions: $O(h)$ work and $O(\log n)$ time. So a round costs $O(n + m h)$ work and $O(\log^2 n)$ time.
- **The sort.** $O(n \log n)$ comparisons in $O(\log n)$ comparison steps with Cole's merge sort, so $O(n h \log n)$ work and $O(\log^2 n)$ time.

In total,

$$W = O(m h^2 + n h \log n), \qquad S = O(h \log^2 n).$$

The method is far from work-efficient: the sequential DFS takes $O(n + m)$ time. Its span is small only when the DFS tree is shallow, which is the case that matters least, since DFS trees are often deep. On a path, $h = n - 1$ and there are $n$ rounds. The best known general results trade much more work for depth:

| graph | result | model | source |
|---|---|---|---|
| any, the DFS of the sequential algorithm | P-complete | | Reif (1985) |
| undirected, some DFS tree | RNC: polylogarithmic expected time, polynomial work | randomized PRAM | Aggarwal and Anderson (1988) |
| directed, some DFS tree | RNC | randomized PRAM | Aggarwal, Anderson and Kao (1990) |
| undirected planar | NC | PRAM | Smith (1986) |

The RNC algorithms call a parallel [minimum-weight perfect matching](/rnc-perfect-matching/) routine, and their work is a large polynomial in $n$. The page cites these results and does not prove them.

## Properties

- **Exact.** The output is the DFS of the sequential algorithm with the same list order, not only some DFS. This holds for directed and undirected graphs, with or without cycles.
- **Deterministic.** No step uses a random choice or a concurrent write.
- **Labels decrease.** A label never goes up: line L5 keeps the old label when no candidate is smaller.
- **Depth is the obstacle.** The number of rounds is set by the height of the DFS tree. This is the parallel form of the fact that a deep DFS is a long chain of dependent choices.

## Variants and improvements

- **Some DFS tree instead of the first one.** If any DFS tree will do, the RNC algorithm of Aggarwal and Anderson builds one in polylogarithmic expected time on undirected graphs. It finds a separator made of a few paths, with matching as a subroutine, and recurses on the small pieces that remain. Aggarwal, Anderson and Kao extend this to directed graphs.
- **Special graph classes.** Smith (1986) gives an NC algorithm for planar undirected graphs.
- **Avoid DFS.** Most uses of DFS have parallel replacements that do not compute a DFS: [Tarjan-Vishkin](/tarjan-vishkin/) uses any spanning tree for biconnected components, and [forward-backward](/forward-backward-scc/) and [coloring](/coloring-scc/) algorithms find strongly connected components by reachability.

## When to use it

Use the relaxation when the exact sequential DFS order is needed and the DFS tree is known to be shallow, or as a test oracle that runs in rounds. For connectivity, biconnectivity, strongly connected components or topological order, use the parallel algorithms that avoid DFS, listed above. When the DFS tree is deep, this method has a span of order $n$ and far more work than the sequential DFS, so the sequential DFS in $O(n + m)$ time is the better choice.

## Pitfalls

- **Reading labels of the current round.** If line L5 sees labels written in the same round, the number of rounds and the costs depend on the schedule, and the analysis of this page does not apply. Keep the old labels until all vertices have written.
- **Comparing by the parent only.** Two candidates $P[u] \cdot i$ and $P[u'] \cdot i'$ with $u \ne u'$ cannot be compared by the ranks of $P[u]$ and $P[u']$: if $P[u]$ is a proper prefix of $P[u']$, the candidate from $u$ can still be the larger one, as $(0) \cdot 5 > (0, 1) \cdot 2$ shows.
- **Taking "DFS is P-complete" too far.** The P-completeness result is for the DFS order fixed by the adjacency lists. Some DFS tree can be found in RNC, and a DFS of a planar graph in NC.
- **Losing the list order.** The result is the DFS for the given list order. A parallel graph loader that permutes the adjacency lists changes the DFS tree.

## Implementations

## History

Reif (1985) proved that the lexicographically first DFS order is P-complete, so that it is in NC only if all of P is. Smith (1986) gave an NC algorithm for planar undirected graphs. Aggarwal and Anderson (1988) showed that some DFS tree of an undirected graph can be found in RNC, and Aggarwal, Anderson and Kao (1990) did the same for directed graphs. Greenlaw, Hoover and Ruzzo (1995) list the lexicographic DFS among the standard P-complete problems.

## References
