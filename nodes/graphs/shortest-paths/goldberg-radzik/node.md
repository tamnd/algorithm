---
tag: FBHX78
kind: algorithm
slug: goldberg-radzik
name: Goldberg-Radzik algorithm
aliases:
- Goldberg-Radzik shortest paths
area: graphs/shortest-paths
level: advanced
summary: Bellman-Ford variant that alternates topological passes over a DAG of admissible edges with negative-cycle checks.
solves: [single-source-shortest-paths, negative-cycle-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [bellman-ford, topological-sort, potential-function-reduced-costs, depth-first-search]
see_also: [spfa, desopo-pape-algorithm, generic-shortest-path-algorithm, dag-shortest-paths, negative-cycle-detection, tarjan-subtree-disassembly, johnson, shortest-path-optimality-conditions]
sources:
  - paper: doi:10.1016/0893-9659(93)90022-f
    title: Andrew V. Goldberg and Tomasz Radzik, A heuristic improvement of the Bellman-Ford algorithm, Applied Mathematics Letters 6(3), 3 to 6 (1993)
    locator: the whole paper (the sets A and B, the admissible graph, topological-order scanning, and the O(nm) bound)
  - paper: doi:10.1007/BF02592101
    title: Boris V. Cherkassky, Andrew V. Goldberg and Tomasz Radzik, Shortest paths algorithms, theory and experimental evaluation, Mathematical Programming 73(2), 129 to 174 (1996)
    locator: the section describing the Goldberg-Radzik algorithm and the experiments comparing it with the other label-correcting methods
  - paper: doi:10.1007/s101070050058
    title: Boris V. Cherkassky and Andrew V. Goldberg, Negative-cycle detection algorithms, Mathematical Programming 85(2), 277 to 311 (1999)
    locator: the sections on cycle detection strategies, including admissible-graph search in the Goldberg-Radzik algorithm
---

The Goldberg-Radzik algorithm is a label-correcting algorithm for [single-source shortest paths](/single-source-shortest-paths/) with arbitrary real weights. Like [Bellman-Ford](/bellman-ford/) it works in passes and keeps the $O(nm)$ worst-case bound, but in each pass it scans vertices in a [topological order](/topological-sort/) of the *admissible graph*, the edges whose [reduced cost](/potential-function-reduced-costs/) $d[u] + w(u, v) - d[v]$ is at most zero. Distances then spread along whole chains of improvements in one pass, as in [DAG shortest paths](/dag-shortest-paths/). A cycle in the admissible graph that contains an edge of negative reduced cost is a [negative cycle](/negative-cycle/), so the depth-first search that computes the order also detects negative cycles early. Goldberg and Radzik published it in 1993; in the study of Cherkassky, Goldberg and Radzik (1996) it was among the most robust shortest-path codes.

## In plain words

Each place keeps its best distance so far from the start. Bellman-Ford improves them in rounds, and in each round it handles places in a fixed order, so an improvement often has to wait a round to move one step further.

Goldberg and Radzik first look at which roads currently "pay off", where going through one place gives a better or equal distance to the next. These roads form a plan with no loops, unless a loop runs at a loss, which means a negative cycle. They line the places up along this plan and handle them in that order, so one improvement can travel down a long chain of places in a single round.

Places whose distance changed after they were handled are kept for the next round. When no place is left, every distance is right.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, a real weight $w(u, v)$ on each edge, and a source $s$. The output is $\delta(s, v)$ for every $v$ with a [shortest-path tree](/shortest-path-tree/), or a report that a negative cycle is reachable from $s$.

**Weight assumptions.** Weights are any real numbers; negative weights, zero weights, parallel edges and self-loops are allowed. If no negative cycle is reachable from $s$, the algorithm returns the distances, with $+\infty$ for vertices that $s$ does not reach. If a negative cycle is reachable from $s$, it reports it, either when the depth-first search of a pass finds an admissible cycle with a negative edge, or at the latest when a pass number $n$ still has work. Negative cycles that $s$ cannot reach are never touched and do not affect the answer. Cycles of reduced cost exactly zero are not negative and are handled by ignoring the closing edge in the topological order.

## The algorithm

The *reduced cost* of an edge is $w_d(u, v) = d[u] + w(u, v) - d[v]$. An edge is *admissible* if $w_d(u, v) \le 0$ and *tense* if $w_d(u, v) < 0$. A vertex is *labeled* if its label has dropped since it was last scanned.

```pseudo id=main
GOLDBERG-RADZIK(G, w, s)
L1  d[v] ← ∞, π[v] ← nil for all v; d[s] ← 0; B ← {s}
L2  while B ≠ ∅ do                                    ▷ one pass
L3      remove from B every vertex with no tense outgoing edge
L4      A ← the vertices reachable from B by admissible edges, in topological order (by DFS)
L5      if the DFS closes a cycle with a tense edge, or this is pass n or later and A ≠ ∅, then return NEGATIVE-CYCLE
L6      for each u in A, in order do
L7          mark u unlabeled
L8          for each edge (u, v) with d[u] + w(u, v) < d[v] do
L9              d[v] ← d[u] + w(u, v); π[v] ← u; mark v labeled
L10     B ← the labeled vertices
L11 return d, π
```

Line L3 drops vertices that scanning would not help; they count as scanned. Line L4 is a [depth-first search](/depth-first-search/) from the remaining vertices of $B$ along admissible edges, with the reverse postorder as the topological order. Edges out of a vertex with label $\infty$ are not followed, and a back edge whose cycle has only zero reduced costs is ignored. Line L5 has two tests: an admissible cycle with a tense edge has negative total reduced cost, which equals its weight, so it is a negative cycle; and the pass count is a backstop, as in Bellman-Ford. Lines L6 to L9 scan the vertices of $A$ in order. A vertex whose label drops after its scan in this pass stays labeled and goes into the next $B$.

## Example

The vertices are $s, a, b, c, d$ and the edges $s \to a$ (2), $s \to b$ (6), $s \to c$ (7), $a \to b$ (3), $a \to d$ (8), $b \to d$ (1), $c \to a$ ($-6$). The distances are $\delta = (0, 1, 4, 7, 5)$ for $s, a, b, c, d$.

**Pass 1.** $B = \{s\}$, and $s$ has tense edges. The search from $s$ finds $a, b, c$, which have label $\infty$ and are not expanded, so the order is $s, c, b, a$.

| scan | changes | labels $s\,a\,b\,c\,d$ |
|---|---|---|
| $s$ | $a = 2$, $b = 6$, $c = 7$ | 0 2 6 7 ∞ |
| $c$ | $a = 1$ | 0 1 6 7 ∞ |
| $b$ | $d = 7$ | 0 1 6 7 7 |
| $a$ | $b = 4$ ($d$: $1 + 8 = 9$ is not better) | 0 1 4 7 7 |

The label of $b$ dropped after $b$ was scanned, and $d$ was never scanned, so $B = \{b, d\}$.

**Pass 2.** $d$ has no outgoing edges and is dropped by line L3; $b \to d$ has reduced cost $4 + 1 - 7 = -2$, so $b$ stays. The order is $b, d$. Scanning $b$ sets $d = 5$; scanning $d$ changes nothing. No vertex is labeled and the algorithm stops, with 6 scans in 2 passes. A FIFO queue ([SPFA](/spfa/)) on the same graph scans 8 times: $s, a, b, c, d, a, b, d$.

**Negative cycle.** With the edges $s \to a$ (1), $a \to b$ ($-2$), $b \to a$ (1), pass 1 scans $s, a$ and sets $a = 1$, $b = -1$. Now $a \to b$ and $b \to a$ have reduced costs $1 - 2 - (-1) = 0$ and $-1 + 1 - 1 = -1$. In pass 2, $B = \{b\}$, and the search goes $b \to a \to b$ along admissible edges, closes a cycle containing the tense edge $b \to a$, and line L5 reports the negative cycle $a, b, a$ of weight $-1$ before any scan of the pass.

**Unreachable vertices.** With the extra edges $x \to y$ (1) and $y \to s$ (1), the vertices $x$ and $y$ never enter $B$ or $A$, since nothing leads to them from $s$; they keep the label $\infty$. A negative cycle among such vertices is never seen.

## Correctness

**Theorem.** The algorithm ends. It returns NEGATIVE-CYCLE if and only if a negative cycle is reachable from $s$; otherwise $d[v] = \delta(s, v)$ for every $v$ and the predecessors form a shortest-path tree.

Every scan only relaxes tense edges, so the run is a run of the [generic relaxation method](/generic-shortest-path-algorithm/), and labels are always weights of walks from $s$. A reported cycle in line L5 is a real negative cycle, since reduced costs sum to the weight around a cycle. The key lemma is the Bellman-Ford pass property: if no negative cycle is reachable and a shortest path to $v$ has $k$ edges, then after pass $k$, $d[v] = \delta(s, v)$. It holds because a vertex whose label became final either is scanned later in the same pass, or stays labeled into the next pass, where line L3 keeps it if one of its edges is tense. So after pass $n - 1$ all labels are final, no edge is tense, and pass $n$ has no work: line L5 never fires without a negative cycle. With one, tense edges never disappear, so the loop cannot end with $B$ empty, and line L5 fires by pass $n$. The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/).

- **Time.** A pass costs $O(n + m)$: line L3 looks at the edges of $B$, the depth-first search at the edges out of $A$, and the scan at the same edges. By the pass property there are at most $n$ passes, so the time is $O(nm)$ for $m \ge n$, the Bellman-Ford bound.
- **Best case.** If the first pass leaves nothing labeled, as for a source whose out-neighbors have no outgoing edges, the time is $\Theta(n + m)$.
- **Space.** Labels, predecessors, flags, colors and the search stack take $\Theta(n)$ extra space.
- **In practice.** The number of passes is usually far below $n$; topological scanning moves improvements along long chains at once.

## Properties

- **Any real weights.** Negative weights are fine; only reachable negative cycles stop it, and they are reported.
- **Same worst case as Bellman-Ford, often much faster.** The pass bound is the same; the topological order makes passes do more.
- **Early negative-cycle detection.** An admissible cycle with a tense edge is found by the search of the pass in which it appears, often long before pass $n$.
- **Few passes on shallow graphs.** Without negative cycles, the number of passes is at most one more than the largest number of edges on a shortest path from $s$ (the minimal one, when shortest paths tie).
- **Label-correcting.** A vertex can be scanned many times, unlike in Dijkstra's algorithm.

## Variants and improvements

- **Admissible graph with zero-cost cycles.** The original paper treats the admissible graph as acyclic; with zero-cost cycles, contract them or ignore one edge of each, as the implementation does.
- **Combination with subtree disassembly.** Cherkassky and Goldberg combine the topological-scan idea with [Tarjan's subtree disassembly](/tarjan-subtree-disassembly/) and other cycle-detection strategies for [negative-cycle detection](/negative-cycle-detection/).
- **Scaling.** Goldberg's [scaling algorithm](/goldberg-scaling-sssp/) for integer weights uses similar admissible-graph ideas to reach $O(\sqrt n\, m \log N)$.
- **Bellman-Ford with a queue.** [SPFA](/spfa/) scans in FIFO order instead of topological order; it has the same worst case, but tends to do more scans when improvements run along chains.

## When to use it

Use it when weights can be negative and a robust label-correcting method is needed, for example in [Johnson's algorithm](/johnson/) or for [negative-cycle detection](/negative-cycle-detection/) in large sparse graphs, where it was among the best performers in the Cherkassky, Goldberg and Radzik experiments. With nonnegative weights, [Dijkstra](/dijkstra/) is better; on a known DAG, the one-pass [DAG algorithm](/dag-shortest-paths/) is better.

## Pitfalls

- **Expanding vertices with label $\infty$.** Their reduced costs are undefined; do not follow edges out of them in the search, and do not compute $\infty - \infty$.
- **Calling any admissible cycle negative.** A cycle of admissible edges is negative only if one of its edges is tense; a cycle of zero reduced costs is legal and must not be reported.
- **Forgetting dropped vertices.** A vertex removed in line L3 counts as scanned and must be marked unlabeled, or it returns to $B$ forever.
- **No backstop.** If the cycle test in the search misses a negative cycle, for example when parallel edges hide a tense one, the pass count must still stop the algorithm.

## Implementations

The Python version runs an iterative depth-first search per pass over admissible edges, checks each closed cycle for a tense edge, uses the pass count as a backstop, and can record the scan order of each pass.

## History

Goldberg and Radzik (1993) proposed the method as a heuristic improvement of Bellman-Ford with the same worst-case bound. Cherkassky, Goldberg and Radzik (1996) compared it with many label-correcting and label-setting codes and found it robust on all their families; Cherkassky and Goldberg (1999) studied it as a negative-cycle detection method.

## References
