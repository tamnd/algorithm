---
tag: 701F07
kind: algorithm
slug: greedy-mst-algorithm
name: Greedy MST algorithm
area: graphs/spanning-trees
level: core
summary: General scheme that builds a minimum spanning tree by repeatedly coloring the lightest edge of a cut that has no colored crossing edge.
solves: [minimum-spanning-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m (n + m))}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [minimum-spanning-tree, cut-property, cycle-property, generic-mst-method]
see_also: [kruskal, prim, boruvka, reverse-delete, mst-verification, karger-klein-tarjan-mst, matroid-greedy-algorithm, fundamental-cycle]
sources:
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms, SIAM (1983)
    locator: Chapter 6, Minimum Spanning Trees (the blue rule, the red rule, and the theorem that the greedy method colors every edge and that the blue edges form a minimum spanning tree)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.3, Minimum Spanning Trees (the greedy MST algorithm, with the cut property and the black edges)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 7, Minimum Spanning Trees
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.5, The Minimum Spanning Tree Problem (the cut property and the cycle property)
---

The greedy MST algorithm is Tarjan's general scheme for the [minimum spanning tree](/minimum-spanning-tree/) problem. It colors the edges one at a time. The *blue rule* takes a cut that no blue edge crosses and colors blue a lightest uncolored edge of the cut. The *red rule* takes a cycle with no red edge and colors red a heaviest uncolored edge of the cycle. The rules may be applied in any order, and as long as some edge is uncolored, one of them applies. At the end the blue edges form a minimum spanning tree. [Kruskal's](/kruskal/), [Prim's](/prim/), [Borůvka's](/boruvka/) and [reverse-delete](/reverse-delete/) are all ways to choose the next rule, and the plain scheme on this page takes $O(m(n + m))$ time.

## In plain words

You must decide, for each road of a network, whether to build it or not. You mark a road blue when you decide to build it, and red when you decide not to.

There are two safe moves. Draw a line across the map that no blue road crosses; the cheapest unmarked road across the line can be marked blue. Or find a loop of roads with no red road on it; the most expensive unmarked road of the loop can be marked red.

You can make the moves in any order you like. While some road is still unmarked, one of the two moves is always possible. When every road is marked, the blue roads form a cheapest network that connects every town.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges and a real weight $w(e)$ on each edge. Weights may tie; then any lightest or heaviest edge may be chosen, and the result is one of the minimum spanning trees. The graph need not be [connected](/connected-graph/); then the blue edges form a minimum [spanning forest](/spanning-forest/). Parallel edges and self-loops are allowed: a self-loop is a cycle by itself and is colored red.

Each edge is *uncolored*, *blue* or *red*. The blue edges always form a forest, the *blue forest*, whose trees are the *blue trees*.

- **Blue rule.** Select a cut $(S, V \setminus S)$ that no blue edge crosses and that some uncolored edge crosses. Color blue a lightest uncolored edge that crosses it.
- **Red rule.** Select a [simple cycle](/simple-cycle/) $C$ that contains no red edge and some uncolored edge. Color red a heaviest uncolored edge of $C$.

## The algorithm

```pseudo id=main
GREEDY-MST(G, w)
L1  make every edge uncolored
L2  while some edge e = (u, v) is uncolored do
L3      if u and v are in different blue trees then
L4          S ← a union of blue trees with u ∈ S and v ∉ S
L5          color blue a lightest uncolored edge that crosses (S, V ∖ S)     ▷ blue rule
L6      else
L7          C ← e together with a path from u to v of non-red edges other than e
L8          color red a heaviest uncolored edge of C                          ▷ red rule
L9  return the blue edges
```

Lines L3 to L8 show that one of the two rules always applies to the chosen edge $e$. If its ends are in different blue trees, the cut of line L4 is crossed by no blue edge and by $e$. If its ends are in one blue tree, the blue path between them and $e$ form a cycle with no red edge, and $e$ is uncolored. The choices of $e$, of $S$ and of the path are free; the implementation takes the uncolored edge with the smallest index, the blue tree of $u$, and the blue path, and it breaks ties by the edge index.

## Example

The graph has the vertices $a$ to $f$ and the edges $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$, listed in index order. With the choices of the implementation, the run is:

| step | uncolored edge $e$ | rule | cut side $S$ or cycle $C$ | candidates | colored |
|---|---|---|---|---|---|
| 1 | $ab$ | blue | $\{a\}$ | $ab = 4$, $ac = 3$ | $ac$ blue |
| 2 | $ab$ | blue | $\{a, c\}$ | $ab = 4$, $bc = 1$, $cd = 4$, $ce = 5$ | $bc$ blue |
| 3 | $ab$ | red | $\{ab, bc, ca\}$ | $ab = 4$ | $ab$ red |
| 4 | $bd$ | blue | $\{a, b, c\}$ | $bd = 2$, $cd = 4$, $ce = 5$ | $bd$ blue |
| 5 | $cd$ | red | $\{cd, db, bc\}$ | $cd = 4$ | $cd$ red |
| 6 | $ce$ | blue | $\{a, b, c, d\}$ | $ce = 5$, $de = 7$, $df = 6$ | $ce$ blue |
| 7 | $de$ | red | $\{de, ec, cb, bd\}$ | $de = 7$ | $de$ red |
| 8 | $df$ | blue | $\{a, b, c, d, e\}$ | $df = 6$, $ef = 2$ | $ef$ blue |
| 9 | $df$ | red | $\{df, fe, ec, cb, bd\}$ | $df = 6$ | $df$ red |

The blue edges are $\{ac, bc, bd, ce, ef\}$, the only minimum spanning tree, of weight 13. The four red edges are the four non-tree edges, and each was colored red on its [fundamental cycle](/fundamental-cycle/) with the blue tree. Step 1 shows that the rule may color an edge other than $e$: the cut around $a$ is chosen for $ab$, but its lightest edge is $ac$.

## Correctness

**Theorem.** For each finite undirected graph with real weights, and for each sequence of choices, GREEDY-MST stops after exactly $m$ steps, and its blue edges form a minimum spanning forest.

The invariant is: *some minimum spanning forest $T$ contains every blue edge and no red edge.* It holds at the start. For the blue rule, if the new blue edge $e$ is not in $T$, the path in $T$ between its ends crosses the cut at an edge $f$; $f$ is not blue, since no blue edge crosses the cut, and not red, since $f \in T$, so $f$ is uncolored and $w(f) \ge w(e)$, and $T - f + e$ is a minimum spanning forest that keeps the invariant. For the red rule, if the new red edge $e$ is in $T$, removing it splits a tree of $T$, and the rest of the cycle has an edge $f$ that joins the two parts; $f$ is not in $T$, so not blue, and not red, since the cycle has no red edge, so $f$ is uncolored and $w(f) \le w(e)$, and $T - e + f$ keeps the invariant. Each step colors one edge, so there are $m$ steps; at the end every edge is colored, and $T$ is exactly the set of blue edges. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM. The cost depends on how the rules are found. This page bounds the plain version: in each step, label the blue trees by a graph search in $O(n + m)$ time, then scan the edges of the cut, or search for the path of line L7, in $O(n + m)$ time.

- **Steps.** Each step colors one edge, so there are exactly $m$ steps.
- **One step.** $O(n + m)$ time, as above.
- **Total.** $O(m (n + m))$ time in the worst case and $O(n + m)$ extra space.

The fast MST algorithms are fast ways to find the next rule. [Kruskal's algorithm](/kruskal/) applies each rule in $O(\alpha(n))$ amortized time after an $O(m \log m)$ sort, and [Prim's algorithm](/prim/) uses a [priority queue](/priority-queue/).

| claim | bound | case |
|---|---|---|
| time, plain version | $O(m (n + m))$ | worst |
| steps | exactly $m$ | every input |
| extra space | $O(n + m)$ | worst |

## Properties

- **A scheme, not one algorithm.** The order of the rules and the choice of the cut or the cycle are free. Each choice gives a correct algorithm.
- **Always applicable.** While an edge is uncolored, one of the two rules applies to it, as lines L3 to L8 show. So the scheme never gets stuck.
- **No undo.** A color, once given, stays.
- **Ties and forests.** Ties need no special care: any lightest or heaviest uncolored edge keeps the invariant. On a disconnected graph the blue edges form a minimum spanning forest.
- **Deterministic** once the choices are fixed.

## Variants and improvements

- **Blue rule only.** The [generic MST method](/generic-mst-method/) uses only the blue rule and stops when the blue forest spans; [Prim](/prim/), [Kruskal](/kruskal/) and [Borůvka](/boruvka/) are of this kind. Kruskal's skipped edges are red-rule steps on the cycle that the skipped edge closes.
- **Red rule only.** [Reverse-delete](/reverse-delete/) scans the edges from the heaviest and colors an edge red when it lies on a cycle of non-red edges.
- **Red rule in bulk.** The [Karger-Klein-Tarjan algorithm](/karger-klein-tarjan-mst/) colors red, in linear time, every edge that is the heaviest edge of a cycle with a sample forest, by [MST verification](/mst-verification/).
- **Matroids.** The two rules are the cut and circuit steps of the [matroid greedy algorithm](/matroid-greedy-algorithm/) on the [graphic matroid](/graphic-matroid/).

## When to use it

Use the scheme to prove an MST algorithm correct: show that each step is a blue-rule step or a red-rule step. Algorithms that mix both kinds of steps, such as those of Karger, Klein and Tarjan or of [Fredman and Tarjan](/fredman-tarjan-mst/), are proved this way. Do not run the plain version on large graphs; use [Kruskal](/kruskal/), [Prim](/prim/) or [Borůvka](/boruvka/).

## Pitfalls

- **A cut crossed by a blue edge.** The blue rule needs a cut with no blue crossing edge. In the triangle with $w(ab) = 1$ and $w(bc) = w(ca) = 2$, after $ab$ and $bc$ are blue, the cut $S = \{a, b\}$ is crossed by the blue edge $bc$, and coloring $ca$ blue would close a blue cycle.
- **A cycle with a red edge.** The red rule needs a cycle with no red edge. In a triangle with three edges of weight 1, after $ab$ is red, the cycle $\{ab, bc, ca\}$ contains it; coloring $bc$ red as well leaves only $ca$, which does not span.
- **Lightest overall, not lightest uncolored.** The blue rule picks among the uncolored crossing edges. A red edge can cross the cut and be the lightest crossing edge; it must be ignored.
- **Stopping too early.** Stop when every edge is colored, or when the blue forest has $n - c$ edges, where $c$ is the number of components. The test "$n - 1$ blue edges" never succeeds on a disconnected graph; the disconnected test case catches it.

## Implementations

## History

Tarjan stated the scheme in his 1983 monograph (Chapter 6). He named the two steps the blue rule and the red rule, proved that they can be applied in any order, and presented the algorithms of Borůvka, Kruskal and Prim as ways to apply them. The two properties behind the rules, the cut property and the cycle property, are older and appear in the early papers on the problem.

## References
