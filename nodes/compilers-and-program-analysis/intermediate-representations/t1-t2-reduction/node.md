---
tag: VPKTQX
kind: algorithm
slug: t1-t2-reduction
name: T1-T2 reduction
aliases:
- Hecht-Ullman transformations
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: Tests reducibility by removing self-loops and merging nodes with a single predecessor; the graph is reducible if one node remains.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n^2 + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [control-flow-graph, reducible-flow-graph, dominators-problem]
see_also: [natural-loop, loop-nesting-forest, elimination-dataflow-methods, cooper-harvey-kennedy-dominance, depth-first-orders, disjoint-set-forest, strongly-connected-components]
sources:
  - paper: "Matthew S. Hecht and Jeffrey D. Ullman, Flow graph reducibility, SIAM Journal on Computing 1(2) (1972), 188-202"
    locator: the transformations T1 and T2, the definition of reducibility as reduction to one node, and the uniqueness of the limit graph
  - paper: doi:10.1145/321832.321835
    title: Matthew S. Hecht and Jeffrey D. Ullman, Characterizations of reducible flow graphs, Journal of the ACM 21(3), 1974
    locator: the equivalent forms of reducibility, among them the forbidden (*) subgraph and the uniqueness of the acyclic graph of forward edges
  - paper: doi:10.1016/S0022-0000(74)80049-8
    title: Robert Endre Tarjan, Testing flow graph reducibility, Journal of Computer and System Sciences 9(3), 1974, pages 355-365
    locator: the almost-linear test for reducibility with depth-first search and disjoint set union
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 9.6.4 (back edges and reducibility) and Section 9.7 (region-based analysis)
  - book: isbn:1558603204
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 7 (Control-Flow Analysis), reducibility and the analyses that collapse regions of a flow graph
---

The T1-T2 reduction tests whether a [control flow graph](/control-flow-graph/) is a [reducible flow graph](/reducible-flow-graph/). It uses two rules, the Hecht-Ullman transformations. T1 deletes a self-loop. T2 takes a node other than the entry that has exactly one predecessor and merges it into that predecessor. Apply the rules until neither applies. The graph is reducible if and only if one node is left, and the order of the steps does not change the answer. With a worklist the test takes $O(n^2 + m)$ time. The list of steps also tells in which order the regions of the graph collapse, which is what elimination data-flow methods use.

## In plain words

Think of the flow graph as a map of rooms joined by one-way doors. Two moves are allowed. If a door leads from a room back into the same room, remove it. If a room other than the entrance can be entered from only one other room, knock down the wall between them, so they become one room; its doors out now leave from the bigger room. Keep making moves until none is possible. If only the entrance room is left, every loop in the program had one way in, and the graph is reducible. If several rooms are left, each of them can be entered from two or more places, and some loop has more than one way in. It does not matter which move you make first. You always end with the same answer.

## The problem

**Input.** A flow graph $G = (N, E, r)$: a directed graph with $n$ vertices, $m$ edges and an entry vertex $r$. Vertices that $r$ does not reach are ignored, and parallel edges count as one edge.

**Output.** The *limit graph*, which is the graph left when neither T1 nor T2 applies, and the list of steps. $G$ is reducible exactly when the limit graph has one vertex.

**The rules.** T1 deletes an edge $(v, v)$. T2 applies to a vertex $v \ne r$ whose only predecessor is $u$. It deletes $v$ and the edge $(u, v)$, and it replaces each edge $(v, w)$ by $(u, w)$. An edge $(v, u)$ becomes a self-loop on $u$, which a later T1 removes. Reducibility itself is defined on the [reducible flow graph](/reducible-flow-graph/) page: the graph without its back edges, the edges $(t, h)$ where $h$ dominates $t$, has no cycle.

## The algorithm

A worklist $W$ holds the vertices that may need a step. A vertex whose sets change goes back on the list.

```pseudo id=main
T1-T2-REDUCE(G, r)
L1  keep the vertices that r reaches; succ[v], pred[v] <- sets of successors and predecessors
L2  W <- all kept vertices
L3  while W is not empty do
L4      v <- pop(W); if v was merged before, skip it
L5      if v is in succ[v] then
L6          T1: remove v from succ[v] and from pred[v]
L7      if v != r and pred[v] = {u} for one vertex u then
L8          T2: remove v from succ[u]
L9          for each w in succ[v] do
L10             replace v by u in pred[w]; add w to succ[u]
L11         delete v; push u and every w in succ[v] on W
L12 return the remaining graph; G is reducible if it has one vertex
```

Line L6 runs before line L7, so a vertex with a self-loop gets the loop removed and can then be merged in the same visit. Line L11 pushes exactly the vertices whose sets changed: $u$ lost an edge and gained others, and each moved successor $w$ has a new predecessor set, which may now have one element. A T1 changes only the sets of $v$, and line L7 tests $v$ again at once.

In the implementation, the sets are Python sets, the steps are returned as tuples `("T1", v)` and `("T2", v, u)`, and `cfg_is_reducible` runs the test on the blocks of a toy IR program.

## Example

Take the nested loops of the [natural loop](/natural-loop/) page:

```
B0:
  i = 0
  s = 0
  jump B1
B1:
  t = i < n
  br t B2 B6
B2:
  j = 0
  jump B3
B3:
  u = j < i
  br u B4 B5
B4:
  s = s + j
  j = j + 1
  jump B3
B5:
  i = i + 1
  jump B1
B6:
  ret s
```

The edges are $B0 \to B1$, $B1 \to B2$, $B1 \to B6$, $B2 \to B3$, $B3 \to B4$, $B3 \to B5$, $B4 \to B3$, $B5 \to B1$. The worklist starts with B0 to B6 and pops the smallest first.

| step | rule | what happens | edges after the step |
|---|---|---|---|
| 1 | T2 | B2 has only B1 before it; merge B2 into B1 | $B1 \to B3$ replaces $B1 \to B2 \to B3$ |
| 2 | T2 | B4 has only B3; merge B4 into B3 | $B4 \to B3$ becomes the self-loop $B3 \to B3$ |
| 3 | T1 | remove $B3 \to B3$ | now B3 has only B1 before it |
| 4 | T2 | merge B3 into B1 | $B1 \to B5$, $B1 \to B6$ |
| 5 | T2 | B5 has only B1; merge B5 into B1 | $B5 \to B1$ becomes the self-loop $B1 \to B1$ |
| 6 | T1 | remove $B1 \to B1$ | now B1 has only B0 before it |
| 7 | T2 | merge B1 into B0 | $B0 \to B6$ |
| 8 | T2 | merge B6 into B0 | no edges |

One vertex is left, so the graph is reducible. The inner loop $\{B3, B4\}$ collapsed in steps 2 and 3, and the outer loop in steps 4 to 6. Each T1 marks the moment a whole loop has become one node.

Now take the smallest irreducible graph from the [reducible flow graph](/reducible-flow-graph/) page: $r \to A$, $r \to B$, $A \to B$, $B \to A$, $A \to C$, $B \to C$. There is no self-loop, $r$ is the entry, and $A$, $B$ and $C$ have two predecessors each. No step applies, and the limit graph is the whole graph with 4 vertices. The cycle $A \to B \to A$ can be entered at both $A$ and $B$.

## Correctness

The proof file proves the whole claim. Its steps:

1. **T1 changes nothing that matters.** A self-loop lies on no path and is always a back edge, so dominance and the graph without back edges stay the same.
2. **T2 keeps reducibility in both directions.** When $v$ merges into $u$, the dominance relation among the other vertices does not change, and $(v, w)$ is a back edge exactly when $(u, w)$ is one. The edge $(u, v)$ is never a back edge. So the graph without back edges after the step is the graph before it with the edge $(u, v)$ contracted, and one has a cycle if and only if the other does.
3. **A reducible graph always allows a step.** If the graph is reducible, has at least two vertices and has no self-loop, some vertex other than $r$ has one predecessor. Take the first vertex $v$ after $r$ in a topological order of the graph without back edges. Either $r$ is its only predecessor, or the vertices that $v$ dominates form a smaller reducible flow graph with root $v$, and induction finds the vertex inside it.
4. **The theorem.** From 1 to 3: $G$ is reducible if and only if every maximal sequence of steps ends in one vertex, if and only if some sequence does. So the order does not matter.
5. **The worklist.** Each vertex that may allow a step is on $W$, so when $W$ is empty no step applies, and the algorithm has made a maximal sequence.

Hecht and Ullman proved more: the limit graph is the same, up to names, for every order of the steps. The proof file cites this and does not prove it; the test does not need it.

## Complexity

**Proved.** Line L1 takes $O(n + m)$ time. Each T2 removes a vertex, so there are at most $n - 1$ of them, and each pushes at most $n$ vertices, so the loop runs $O(n^2)$ times. Each T2 does $O(n)$ set operations, one per moved successor. The total is $O(n^2 + m)$, in expectation with hash sets and in the worst case with an $n \times n$ bit table for edge membership. The extra space is $\Theta(n + m)$ for the sets. On a star, where $r$ points to every other vertex, each vertex is merged with no successors to move, and the time is $\Theta(n + m)$.

**Measured, not proved.** In the tests, 1,500 seeded random digraphs with 1 to 8 vertices give the same verdict as the definition computed by brute force, and on 400 graphs a naive applier that picks steps in random orders always reaches the verdict of the worklist. A chain of 20,000 vertices with edges in both directions takes a few hundredths of a second in Python on a laptop.

## Properties

- **Deterministic.** The step list depends on the order of the worklist; the verdict does not.
- **Non-recursive.** The search of line L1 and the main loop use explicit lists.
- **Order-independent.** Any order of T1 and T2 steps gives the same answer, by the theorem of the proof file.
- **A parse of the graph.** On a reducible graph the steps form a hierarchy of regions: each T2 attaches a region to its single entry, and each T1 closes a loop.
- **Offline.** The whole graph is needed; after an edge change the test runs again.

## Variants and improvements

- **Tarjan's test.** Tarjan (1974) tests reducibility in almost linear time with one depth-first search and [disjoint set forests](/disjoint-set-forest/), which keep track of the vertices that have been collapsed together.
- **Test with one search.** Run one depth-first search, compute dominators, for example with the [Cooper-Harvey-Kennedy](/cooper-harvey-kennedy-dominance/) algorithm, and check that each retreating edge goes to a dominator of its source. This is form 5 on the reducible flow graph page.
- **Intervals.** Allen and Cocke's interval analysis collapses a whole single-entry region at a time, instead of one node. A graph is reducible exactly when the sequence of interval graphs ends in one node.
- **Elimination data-flow analysis.** The step list orders the work of [elimination methods](/elimination-dataflow-methods/): at a T2 step the transfer function of $v$ is composed into $u$, and at a T1 step the effect of the loop is closed. Then the results are spread back in reverse order.
- **Node splitting.** When the reduction gets stuck, copy a vertex with $k$ predecessors into $k$ vertices, one per predecessor. Each copy then allows a T2 step. Repeating this makes any flow graph reducible, but the graph can grow very large.

## When to use it

Use it when you need a simple and clearly correct reducibility test for the control flow graphs of single procedures, which are small, or when you also need the order in which the regions collapse. For large graphs, use Tarjan's test or a single search with dominators. If you need the loops themselves, compute [natural loops](/natural-loop/) or a [loop nesting forest](/loop-nesting-forest/) instead.

## Pitfalls

- **Unreachable vertices.** An edge from a vertex that $r$ does not reach still counts as a predecessor, so T2 cannot fire and a reducible graph looks irreducible. Delete unreachable vertices first, as line L1 does.
- **Parallel edges.** A branch `br c L L` gives two edges to `L`. Counted twice, they block T2 on `L`. Keep the edges as sets.
- **The self-loop as a predecessor.** A vertex with a self-loop has itself as a predecessor. Do T1 before testing T2, or the test fails on every loop header.
- **Merging the entry.** T2 must never merge $r$, even if $r$ has exactly one predecessor, for example the latch of a loop that starts at the entry. Merging it would remove the entry of the graph.
- **A worklist that forgets vertices.** After a T2, both $u$ and the moved successors must go back on the list. If they do not, the loop can stop while a step still applies, and the answer is wrong.

## Implementations

## History

Hecht and Ullman introduced the transformations T1 and T2 in 1972 and defined a flow graph to be reducible when they reduce it to one node; they also proved that the limit graph does not depend on the order of the steps. Their 1974 paper in the Journal of the ACM gave further equivalent forms, among them the forbidden $(*)$ subgraph. In the same year Tarjan gave an almost-linear test. The rules became the standard way to explain reducibility in textbooks, and the order of collapse that they define is the basis of T1-T2 elimination methods for data-flow analysis.

## References
