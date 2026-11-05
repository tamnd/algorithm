---
tag: M60CT8
kind: algorithm
slug: stoer-wagner
name: Stoer-Wagner algorithm
aliases:
- Stoer-Wagner minimum cut
area: graphs/flows-and-cuts
level: advanced
summary: Deterministic global min cut via repeated maximum-adjacency orderings and merging.
solves: [global-min-cut-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [global-min-cut-problem, graph-contraction, min-cut-problem]
see_also: [nagamochi-ibaraki, karger-min-cut, karger-stein, hao-orlin, edge-connectivity, fibonacci-heap, prim, gomory-hu-tree]
sources:
  - paper: doi:10.1145/263867.263872
    title: Mechthild Stoer and Frank Wagner, A simple min-cut algorithm, Journal of the ACM 44(4), 585 to 591 (1997)
    locator: the whole paper (the minimum cut phase, its lemma that the cut of the phase is a minimum s-t cut, and the O(nm + n^2 log n) bound)
  - paper: doi:10.1137/0405004
    title: Hiroshi Nagamochi and Toshihide Ibaraki, Computing edge-connectivity in multigraphs and capacitated graphs, SIAM Journal on Discrete Mathematics 5(1), 54 to 66 (1992)
    locator: the whole paper (the earlier minimum cut algorithm without flows that Stoer and Wagner simplified)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 15, Connectivity and Gomory-Hu trees (legal orderings and the Nagamochi-Ibaraki and Stoer-Wagner method for minimum cuts)
---

The Stoer-Wagner algorithm finds a [global minimum cut](/global-min-cut-problem/) of an undirected graph with nonnegative edge weights without computing any flow. It runs $n - 1$ phases. Each phase orders the vertices by *maximum adjacency*, always adding the vertex most strongly joined to those already chosen, much as [Prim's algorithm](/prim/) grows a tree. The last vertex $t$ of the order, cut off from the rest, is a [minimum $s$-$t$ cut](/min-cut-problem/) for the last two vertices $s$ and $t$. Then $s$ and $t$ are [merged](/graph-contraction/), and the best cut of all phases is the answer. It takes $O(n^3)$ time with arrays and $O(nm + n^2 \log n)$ with a [Fibonacci heap](/fibonacci-heap/), and it is deterministic, unlike [Karger's algorithm](/karger-min-cut/).

## In plain words

You want to split a network into two parts so that the links between the parts weigh as little as possible. Nobody tells you which two points to separate.

Build a sequence: start anywhere, and keep adding the point that has the heaviest links to the points already chosen. The very last point added has a special property: cutting it off from everything else is the cheapest way to separate it from the second-to-last point. Record that cut, then glue those last two points together, since any better cut keeps them on the same side. Repeat until one point is left. The cheapest cut you recorded is the answer.

## The problem

The input is an undirected graph $G = (V, E)$ with $n \ge 2$ vertices and $m$ edges, and weights $w(e) \ge 0$, integer or real. Parallel edges add up; self-loops are ignored. The graph may be disconnected, in which case the answer is 0. Edge direction plays no role, and there are no source and sink. The output is a set $S$ with $\emptyset \ne S \subsetneq V$ that minimizes $w(S, V \setminus S)$, the total weight of the edges with one end in $S$. For directed graphs, see the [directed global min cut problem](/directed-global-min-cut-problem/) and [Hao-Orlin](/hao-orlin/).

## The algorithm

Write $w(A, v)$ for the total weight of the edges between a vertex $v$ and a set $A$. Each vertex of the current graph stands for a group of original vertices.

```pseudo id=main
STOER-WAGNER(G, w)
L1  best ← ∞; each vertex v starts as the group {v}
L2  while G has more than one vertex do
L3      (s, t, c) ← MINIMUM-CUT-PHASE(G, w)
L4      if c < best then best ← c; bestS ← the group of t
L5      merge t into s: the group of s takes the group of t, w(s, x) ← w(s, x) + w(t, x) for each x, and t is deleted
L6  return best, bestS

MINIMUM-CUT-PHASE(G, w)
L7  A ← [a] for any vertex a; key(v) ← w(a, v) for each other v
L8  while some vertex is not in A do
L9      z ← the vertex not in A of largest key; append z to A
L10     for each vertex v not in A do key(v) ← key(v) + w(z, v)
L11 return the last two vertices s, t of A, and c = key(t) = w(V \ {t}, t)
```

When $z$ is chosen at line L9, $\mathrm{key}(z) = w(A, z)$ for the set $A$ before $z$; this is the maximum adjacency rule. So the key of the last vertex $t$ is the weight of all edges at $t$, which is the cut that separates the group of $t$ from the rest.

## Example

The graph has the vertices $a, \ldots, f$; the triangles $abc$ and $def$ have edges of weight 2, and the edges $c d$ and $b e$ have weight 1. The minimum cut is $\{a, b, c\}$ against $\{d, e, f\}$, of weight 2. Every phase starts at $a$, and ties are broken by the order $a, \ldots, f$.

| phase | order of the phase | $s$, $t$ | cut of the phase | merge |
|---|---|---|---|---|
| 1 | $a, b, c, d, e, f$ | $e$, $f$ | 4: $\{f\}$ | $ef$ |
| 2 | $a, b, c, d, ef$ | $d$, $ef$ | 5: $\{e, f\}$ | $def$ |
| 3 | $a, b, c, def$ | $c$, $def$ | 2: $\{d, e, f\}$ | $cdef$ |
| 4 | $a, b, cdef$ | $b$, $cdef$ | 5: $\{c, d, e, f\}$ | $bcdef$ |
| 5 | $a, bcdef$ | $a$, $bcdef$ | 4: $\{b, \ldots, f\}$ | |

In phase 1 the keys after $a$ are $b = 2$, $c = 2$; after $b$, $c = 4$ and $e = 1$; after $c$, $d = 1$ and $e = 1$; after $d$, $e = 3$ and $f = 2$; after $e$, $f = 4$. The answer is phase 3, with weight 2. Phase 1 alone found only a cut of weight 4, which is a minimum $e$-$f$ cut: $e$ and $f$ lie on the same side of the global minimum cut, so they can be merged safely.

Edge cases. A disconnected graph gives a phase whose last vertex has key 0, so the answer is 0. An edge of weight 0 is the same as no edge. With $n = 2$ there is one phase, and the cut is all the weight between the two vertices.

## Correctness

The key lemma: in each phase, $w(V \setminus \{t\}, t)$ is a minimum $s$-$t$ cut of the current graph. Given the lemma, consider a global minimum cut $C$. If it separates $s$ and $t$ of some phase, that phase records a cut of weight at most $w(C)$. Otherwise $s$ and $t$ are on the same side, merging them keeps $C$ as a cut of the smaller graph, and the argument continues on that graph; the last phase has two vertices, which every cut separates. The lemma is proved by comparing, for each vertex $v$ of the order, $w(A_v, v)$ with the part of an $s$-$t$ cut inside $A_v \cup \{v\}$, by induction over the vertices whose predecessor lies on the other side. The proof file below gives both steps in full.

## Complexity

The model is the [word RAM](/word-ram/), with weights that fit in a word.

- **One phase.** With an adjacency matrix and a linear scan for the largest key, $O(n^2)$. With a [Fibonacci heap](/fibonacci-heap/) of keys, $n$ extract-max and $O(m)$ increase-key operations: $O(m + n \log n)$.
- **Merging.** Adding row $t$ to row $s$ is $O(n)$.
- **Total.** $n - 1$ phases: $O(n^3)$ with the matrix, as in the implementation, or $O(nm + n^2 \log n)$ with the heap.
- **Space.** $\Theta(n^2)$ for the matrix, or $\Theta(n + m)$ with adjacency lists.

## Properties

- **Deterministic and exact.** No randomness and no flow computation.
- **Real weights.** Only additions and comparisons of weights are used, so real weights work.
- **Undirected only.** The maximum adjacency lemma fails for directed graphs.
- **Many cuts.** Each phase gives a minimum cut between some pair, so the run also gives $n - 1$ cuts, one per pair $(s, t)$ of the phases.

## Variants and improvements

- **Nagamochi-Ibaraki.** The earlier algorithm of [Nagamochi and Ibaraki](/nagamochi-ibaraki/) uses the same orderings but contracts many edges per phase, using a sparse certificate; Stoer and Wagner simplified its proof and structure.
- **Unweighted graphs.** With integer weights, a bucket structure replaces the heap, and a phase takes $O(m + n)$; the total is $O(nm)$.
- **Randomized methods.** [Karger-Stein](/karger-stein/) takes $O(n^2 \log^3 n)$ and Karger's tree packing method $O(m \log^3 n)$; recent deterministic methods are near-linear.
- **Directed graphs.** [Hao-Orlin](/hao-orlin/) solves the directed version in the time of one push-relabel run.

## When to use it

Use it for global minimum cuts of undirected weighted graphs when a deterministic, exact and short implementation is wanted, especially on dense graphs, where $O(n^3)$ with a matrix is competitive. For very large sparse graphs, near-linear algorithms or practical solvers based on contraction and certificates are faster. For an $s$-$t$ cut, use a [maximum flow](/max-flow-problem/) instead.

## Pitfalls

- **Stopping after one phase.** One phase gives a minimum cut only between its last two vertices, not a global minimum; all $n - 1$ phases are needed.
- **Returning the wrong side.** The cut of a phase is the group of $t$, all original vertices merged into $t$, not $t$ alone.
- **Updating keys of chosen vertices.** Line L10 updates only vertices not yet in $A$.
- **Directed input.** Treating a directed graph as undirected gives the cut of the symmetrized graph, not a directed minimum cut.
- **Negative weights.** The lemma needs $w \ge 0$; with negative weights the problem is a different one (maximum cut is NP-hard).

## Implementations

## History

Nagamochi and Ibaraki gave in 1992 the first minimum cut algorithm for undirected graphs that does not use flows, based on maximum adjacency orderings. Stoer and Wagner presented a simpler version and proof at ESA in 1994, and in the Journal of the ACM in 1997. Frank independently found a similar simple proof.

## References
