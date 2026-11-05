---
tag: AA7K7S
kind: algorithm
slug: generic-mst-method
name: Generic minimum spanning tree method
aliases:
- Generic minimum-spanning-tree method
area: graphs/spanning-trees
level: core
summary: Framework that builds a minimum spanning tree by repeatedly adding an edge that is safe, which Kruskal and Prim both instantiate.
solves: [minimum-spanning-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n (n + m))}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [minimum-spanning-tree, cut-property, safe-edge, cut]
see_also: [kruskal, prim, boruvka, greedy-mst-algorithm, cycle-property, matroid-greedy-algorithm, reverse-delete, spanning-forest]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Section 21.1, Growing a minimum spanning tree (the procedure GENERIC-MST, safe edges, the theorem on light edges and its corollary)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 7, Minimum Spanning Trees (the section "The only minimum spanning tree algorithm")
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms, SIAM (1983)
    locator: Chapter 6, Minimum Spanning Trees (the blue rule and the classical algorithms as its applications)
---

The generic minimum spanning tree method grows a set $A$ of edges that is always a subset of some [minimum spanning tree](/minimum-spanning-tree/): at each step it picks a cut that no edge of $A$ crosses and adds a lightest edge of that cut. The [cut property](/cut-property/) shows that such an edge is [safe](/safe-edge/), so after $n - 1$ steps $A$ is a minimum spanning tree. [Kruskal's](/kruskal/), [Prim's](/prim/) and [Borůvka's](/boruvka/) algorithms are this method with three different rules for the choice of the cut. The method itself is a template: its cost depends on how the cut and its light edge are found, and the plain version on this page takes $O(n(n + m))$ time.

## In plain words

You build a network piece by piece. At each moment, the pieces you have built are part of some cheapest network, even if you do not know which one yet.

To add a piece, draw a line that splits the towns into two sides, in any way you like, as long as no road you already built goes across the line. Then build the cheapest road that does cross the line. Some road across the line is needed in the end, and the cheapest one never hurts.

The method leaves one thing open: where to draw the line. Different answers give different known algorithms. Grow one group of towns and always draw the line around it, and you get Prim's algorithm. Take the cheapest road in the whole list that joins two groups, and you get Kruskal's algorithm.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges and a real weight $w(e)$ on each edge. Weights may tie. The graph need not be [connected](/connected-graph/); then the method builds a minimum [spanning forest](/spanning-forest/). The output is a set of edges of least total weight among the spanning forests of $G$, which is a minimum spanning tree when $G$ is connected.

A *cut* $(S, V \setminus S)$ *respects* a set $A$ when no edge of $A$ has exactly one end in $S$. An edge is *light* for the cut when it crosses the cut and no crossing edge is lighter. An edge $e$ is *safe* for $A$ when $A \cup \{e\}$ is a subset of some minimum spanning forest.

## The algorithm

```pseudo id=main
GENERIC-MST(G, w)
L1  A ← ∅
L2  while some edge of G joins two different trees of (V, A) do
L3      choose a cut (S, V ∖ S) that respects A and that some edge crosses      ▷ the free choice
L4      let (u, v) be a light edge of the cut
L5      A ← A ∪ {(u, v)}                                                      ▷ (u, v) is safe for A
L6  return A
```

Line L3 is the only free step. A cut respects $A$ exactly when $S$ is a union of trees of the forest $(V, A)$, so the choice is a choice of some trees. Line L4 scans the edges that cross the cut. With ties, any light edge works; the implementation takes the one with the smallest index.

The three classical choices are:

| algorithm | the cut of line L3 | how the light edge is found |
|---|---|---|
| [Prim](/prim/) | the tree that holds a fixed start vertex | a [priority queue](/priority-queue/) of the edges, or of the vertices, at the tree |
| [Kruskal](/kruskal/) | the tree at one end of the lightest edge that joins two trees | sort all edges once, and test with a [disjoint-set](/disjoint-set/) structure |
| [Borůvka](/boruvka/) | every open tree at once, each with its own cut | one scan of all edges per round |

## Example

The graph has the vertices $a$ to $f$ and the edges $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$. Here line L3 makes five free choices, none of them the choice of a classical algorithm:

| step | trees of $A$ before | chosen $S$ | edges across the cut | light edge | $w(A)$ |
|---|---|---|---|---|---|
| 1 | six single vertices | $\{d\}$ | $bd = 2$, $cd = 4$, $de = 7$, $df = 6$ | $bd$ | 2 |
| 2 | $\{b, d\}$ and four single vertices | $\{e\}$ | $ce = 5$, $de = 7$, $ef = 2$ | $ef$ | 4 |
| 3 | $\{b, d\}$, $\{e, f\}$, $\{a\}$, $\{c\}$ | $\{a\}$ | $ab = 4$, $ac = 3$ | $ac$ | 7 |
| 4 | $\{b, d\}$, $\{e, f\}$, $\{a, c\}$ | $\{a, c\}$ | $ab = 4$, $bc = 1$, $cd = 4$, $ce = 5$ | $bc$ | 8 |
| 5 | $\{a, b, c, d\}$, $\{e, f\}$ | $\{e, f\}$ | $ce = 5$, $de = 7$, $df = 6$ | $ce$ | 13 |

After step 5, $A = \{bd, ef, ac, bc, ce\}$ is a spanning tree of weight 13, and no edge joins two trees, so the loop stops. Prim's choice from $a$ adds the same five edges in the order $ac, bc, bd, ce, ef$, and Kruskal's choice in the order $bc, bd, ef, ac, ce$. The tree is the same, because this graph has only one minimum spanning tree.

## Correctness

**Theorem.** For each finite undirected graph with real weights, and for each sequence of choices at line L3, GENERIC-MST stops after at most $n - 1$ iterations and returns a minimum spanning forest.

The invariant is: *$A$ is a subset of some minimum spanning forest.* It holds for $A = \emptyset$. At line L4, the cut respects $A$ and $(u, v)$ is light for it, so the [cut property](/cut-property/) (part 1, in its form for forests) shows that $(u, v)$ is safe for $A$, and the invariant holds after line L5. Since $S$ is a union of trees of $A$, a crossing edge joins two different trees, so each iteration adds an edge that closes no cycle, and $|A|$ grows by one. When the loop stops, no edge joins two trees, so $A$ is a spanning forest, and a spanning forest inside a minimum spanning forest is that forest. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM. The cost depends on line L3 and line L4; this page bounds the plain version, which finds the trees of $(V, A)$ by a graph search and scans all edges for the light edge.

- **Iterations.** Each iteration adds one edge to a forest, and a forest has at most $n - 1$ edges, so there are at most $n - 1$ iterations, and $n - c$ exactly, where $c$ is the number of components.
- **One iteration.** Labelling the trees of $(V, A)$ takes $O(n)$ time. The test of line L2 and the scan of line L4 take $O(m)$ time. The choice of line L3 is the caller's; the default choice of the implementation takes $O(n)$ time.
- **Total.** $O(n (n + m))$ time in the worst case, and $O(n + m)$ extra space.

This bound is not the point of the method. The point is that each MST algorithm is a way to make lines L3 and L4 fast: Kruskal's algorithm makes all iterations together cost $O(m \log m)$, and Prim's algorithm with a [Fibonacci heap](/fibonacci-heap/) makes them cost $O(m + n \log n)$.

| claim | bound | case |
|---|---|---|
| time, plain version | $O(n (n + m))$ | worst |
| iterations | $n - c \le n - 1$ | every input |
| extra space | $O(n + m)$ | worst |

## Properties

- **A template.** The method has one free step. Each choice of the cut gives a correct algorithm.
- **No undo.** An edge, once added, stays. This is what makes the method greedy.
- **Ties and forests.** Ties need no special care, since any light edge is safe. On a disconnected graph the method returns a minimum spanning forest.
- **Deterministic** once the choice of line L3 is fixed.

## Variants and improvements

- **The greedy MST algorithm with red and blue rules.** Tarjan's [greedy MST algorithm](/greedy-mst-algorithm/) adds the dual step of the [cycle property](/cycle-property/), which throws away a heaviest edge of a cycle. The generic method is the version with only the blue rule.
- **Matroids.** On any [matroid](/matroid/), a step that adds a lightest element that keeps the set independent is safe, and the [matroid greedy algorithm](/matroid-greedy-algorithm/) is the analogue of Kruskal's choice.
- **Reverse-delete.** The mirror method [reverse-delete](/reverse-delete/) removes unsafe edges instead of adding safe ones.

## When to use it

Use the generic method to prove a new MST algorithm correct: show that each edge it adds is a light edge of a cut that respects the edges added before. Do not run the plain version on large graphs; use [Kruskal](/kruskal/), [Prim](/prim/) or [Borůvka](/boruvka/), which are fast forms of it.

## Pitfalls

- **A cut that does not respect $A$.** If an edge of $A$ crosses the cut, the light edge can close a cycle with $A$. In the triangle with $w(ab) = 1$ and $w(bc) = w(ac) = 2$, after $A = \{ab, bc\}$ the cut $S = \{a, b\}$ is crossed by $bc \in A$ and by $ac$, and adding the light edge $ac$ closes a cycle. Choose $S$ as a union of trees of $A$.
- **Lightest at a vertex instead of across the cut.** Line L4 must take a lightest edge over all crossing edges. Taking the lightest crossing edge at one vertex of $S$ can add an edge that is in no minimum spanning tree.
- **Waiting for $n - 1$ edges.** The loop test must be "some edge joins two trees", not "$|A| < n - 1$". On a disconnected graph the second test never becomes false; the disconnected test case catches it.

## Implementations

## History

The view of the classical algorithms as one method with a free choice of the cut appears in Tarjan's 1983 monograph (Chapter 6), which calls the step the blue rule. CLRS present the same idea as the procedure GENERIC-MST in Section 21.1, with the notions of a cut that respects $A$, a light edge and a safe edge. Erickson calls it "the only minimum spanning tree algorithm".

## References
