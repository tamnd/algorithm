---
tag: R4EPTY
kind: algorithm
slug: coloring-scc
name: Coloring SCC
aliases:
- Orzan's algorithm
- color propagation SCC
area: parallel/parallel-graph-algorithms
level: advanced
summary: Parallel SCC that propagates maximum vertex labels and then peels off the roots of each colour class.
solves: [strongly-connected-components]
model: work-span-model
complexity:
  vars: {n: the number of vertices, m: the number of arcs, r: the total number of rounds}
  time: {worst: O((n + m) r)}
  depth: {worst: O(r log n)}
  space: {extra: O(n + m)}
properties: {deterministic: false, recursive: false}
prereqs: [strongly-connected-components, frontier-based-processing, reachability, work-span-model]
see_also: [forward-backward-scc, tarjan-scc, kosaraju-sharir, condensation-graph, parallel-bfs, shiloach-vishkin, jones-plassmann, transitive-closure]
sources:
  - paper: "Simona Orzan, On distributed verification and verified distribution, PhD thesis, Vrije Universiteit Amsterdam, 2004"
    title: On distributed verification and verified distribution
    locator: the SCC decomposition by coloring, with its correctness argument; chapter and page to be checked
  - paper: doi:10.1093/logcom/exp003
    title: Jiří Barnat, Jakub Chaloupka and Jaco van de Pol, Distributed algorithms for SCC decomposition, Journal of Logic and Computation 21(1), 2011
    locator: the survey and comparison of distributed SCC algorithms, among them FW-BW and coloring; volume, pages and DOI to be checked
  - paper: doi:10.1109/IPDPS.2014.64
    title: George M. Slota, Sivasankaran Rajamanickam and Kamesh Madduri, BFS and coloring-based parallel algorithms for strongly connected components and related problems, IPDPS 2014
    locator: the multistep method (trimming, one FW-BW step for the giant SCC, then coloring); DOI to be checked
---

Coloring SCC finds the [strongly connected components](/strongly-connected-components/) of a directed graph by spreading labels. Every vertex starts with its own label as its color, and colors flow along the arcs, each vertex keeping the largest color it has seen; at the end, the color of $v$ is the largest label of a vertex that reaches $v$. A vertex whose color is its own label is a root, and its SCC is the set of vertices of its color that reach it, found by a backward search inside the color class. All these SCCs leave together, and the process repeats on the rest.

Notation on this page: $G = (V, A)$ is a directed graph with $n$ vertices and $m$ arcs; $\lambda(v)$ is the label of $v$, all labels distinct, by default a random permutation. $r$ is the total number of rounds: the propagation rounds plus, for each iteration, the rounds of the longest backward search. $W$ is the work, $S$ the span and $T_p$ the time on $p$ processors, in the [work-span model](/work-span-model/) with a priority (maximum) concurrent write. The bounds are worst case in terms of $r$; there is no general polylogarithmic bound on $r$.

## In plain words

Picture one-way streets between houses, and give each house a different number. Every house paints its door with its own number. Then, again and again, each house looks at the doors of houses with a street into it and repaints its door with the largest number it sees.

When nothing changes, each door shows the largest number of any house that can drive to it. A house whose door still shows its own number is a leader: no house with a larger number can reach it.

The leader's district is made of the houses with the leader's number on the door that can also drive back to the leader. Every leader finds its district at the same time. Those districts leave, and the rest starts again.

## The problem

The input is a directed graph. The output is its partition into strongly connected components: $u$ and $v$ are in one part exactly when each reaches the other. [Tarjan's algorithm](/tarjan-scc/) solves this in $O(n + m)$ sequential time with depth-first search. Coloring SCC uses only label propagation and BFS, which run in parallel rounds.

## The algorithm

Reachability and the arcs are taken inside the set $V$ of remaining vertices.

```pseudo id=main
COLORING-SCC(V, A, λ)
L1  while V is not empty do
L2      for all v in V in parallel do color(v) ← λ(v)
L3      repeat until no color changes
L4          for all arcs (u, v) inside V in parallel do color(v) ← max(color(v), color(u))      ▷ only from vertices that changed
L5      R ← the roots, the vertices with color(r) = λ(r)
L6      for all r in R in parallel do S(r) ← the vertices of color color(r) that reach r inside the color class      ▷ backward BFS
L7          output S(r) as an SCC
L8      V ← V minus all S(r)
L9  return
```

Line L4 is a frontier step: only vertices whose color changed in the last round send their color on. The roots of one iteration have different colors, so their backward searches run in disjoint color classes.

## Example

The graph has the vertices 0 to 7 and the arcs $0 \to 1$, $1 \to 2$, $2 \to 0$, $2 \to 3$, $3 \to 4$, $4 \to 3$, $5 \to 0$, $5 \to 6$, $6 \to 5$, $4 \to 7$, with $\lambda(v) = v$.

| iteration | colors after L3 and L4 (vertices 0 to 7) | roots (L5) | SCCs (L6 and L7) |
|---|---|---|---|
| 1 | 6, 6, 6, 6, 6, 6, 6, 7 | 6, 7 | $\{5, 6\}$, $\{7\}$ |
| 2 | 2, 2, 2, 4, 4 for the vertices 0 to 4 | 2, 4 | $\{0, 1, 2\}$, $\{3, 4\}$ |

In iteration 1, vertex 6 reaches every vertex, so all colors are at least 6, and only 7 reaches 7 among the larger labels. The backward search from 6 inside color 6 finds 5 and 6, but not 0 to 4, which 6 reaches but which do not reach 6. After 5, 6 and 7 leave, the largest label that reaches 0, 1 and 2 is 2, and the largest that reaches 3 and 4 is 4.

## Correctness

The proof file proves, in full:

1. after line L3, $color(v)$ is the largest label of a vertex that reaches $v$ inside $V$;
2. for a root $r$, $S(r)$ is exactly the SCC of $r$: a vertex of the SCC has the same reachers as $r$, so the same color, and every vertex on a path from it to $r$ is in the SCC too, so the backward search finds it; and a vertex of color $\lambda(r)$ is reached by $r$, so if it also reaches $r$, it is in the SCC;
3. the vertex with the largest label in $V$ is a root, so each iteration removes at least one SCC, and the removed sets are whole SCCs, so the SCCs of the rest are SCCs of $G$.

## Complexity

**Per round.** A propagation round does work proportional to the out-degrees of the vertices that changed, at most $O(n + m)$, with $O(\log n)$ span for the max writes and the pack of the next frontier. The backward searches of one iteration run in disjoint color classes, so their rounds together cost $O(n + m)$ work and their span is that of the longest one. So

$$W = O((n + m)\, r), \qquad S = O(r \log n).$$

**How large $r$ can be.** The number of iterations can be $n$: on the path $n-1 \to n-2 \to \cdots \to 0$ with $\lambda(v) = v$, every vertex has color $n - 1$ and only one SCC leaves per iteration, and the propagation takes up to $n$ rounds in each, so $r = \Theta(n^2)$. Random labels help with the number of iterations, but not with the length of the propagation: in the tests, on that path with random labels, the mean number of iterations is 8.4, 10.0 and 14.4 for $n = 64$, 256 and 1,024, but the total number of propagation rounds is about $2n$. On random digraphs with $2n$ arcs and random labels, the mean number of iterations is 3.6, 4.2 and 4.6, with 17 to 30 propagation rounds in total.

## Properties

- **Las Vegas.** The output is always correct; the labels change only the cost.
- **Many SCCs per iteration.** Every root finds its SCC in the same iteration, which suits graphs with many small and medium SCCs, where [FW-BW](/forward-backward-scc/) would need many levels.
- **Only local steps.** Propagation and backward search use only arcs and labels, so the method runs in vertex-centric and distributed systems.
- **Diameter-bound.** Each iteration needs at least as many rounds as the longest path that a color must travel, so graphs with long paths have large span.

## Variants and improvements

- **Trimming first.** Removing the vertices with no in-arc or no out-arc, as in FW-BW, takes away many single-vertex SCCs before any propagation.
- **Multistep.** Slota, Rajamanickam and Madduri (2014) trim, find the giant SCC with one FW-BW step, and use coloring only on the rest, where the SCCs are small.
- **Asynchronous propagation.** Updating colors in place, as soon as a larger color arrives, needs fewer rounds in practice; the final colors are the same.
- **Min instead of max.** Propagating the least label gives the same algorithm with the roles of large and small labels exchanged.
- **Connected components.** In an undirected graph, max-label propagation alone gives the connected components, a simple but slow relative of [Shiloach-Vishkin](/shiloach-vishkin/).

## When to use it

Use it as part of a parallel SCC code for graphs with many SCCs, after trimming and after a FW-BW step has removed the giant SCC. Its rounds are simple and regular, which suits GPUs and vertex-centric frameworks. Avoid it alone on graphs with long paths, where the propagation is sequential in effect.

## Pitfalls

- **Searching outside the color class.** The backward search from $r$ must stay inside the vertices of color $\lambda(r)$; outside it, the search can pick up vertices of other SCCs that reach $r$.
- **Searching forward instead of backward.** The color already says that $r$ reaches $v$; the search must check that $v$ reaches $r$, along the arcs in reverse.
- **Propagating through removed vertices.** Arcs to or from vertices that left in an earlier iteration must be ignored, or colors from removed SCCs keep the rest from finding roots.
- **Fixed labels on ordered inputs.** With labels that follow the arc direction, such as $\lambda(v) = v$ on a path whose arcs go from larger to smaller numbers, each iteration removes one vertex. Use random labels.

## Implementations

## History

Orzan (2004) introduced the coloring method for SCC decomposition in distributed model checking. Barnat, Chaloupka and van de Pol (2011) compared it with other distributed SCC algorithms. Slota, Rajamanickam and Madduri (2014) combined it with trimming and FW-BW in a multistep method for large graphs on multicore machines.

## References
