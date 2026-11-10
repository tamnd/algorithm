---
tag: 98SJR0
kind: algorithm
slug: mst-preorder-walk-tsp
name: MST preorder walk 2-approximation for metric TSP
aliases:
- Minimum spanning tree and preorder tree walk for TSP
- APPROX-TSP-TOUR
area: approximation/tsp-approximation
level: core
summary: Builds a minimum spanning tree and visits the vertices in preorder; for metric TSP the tour costs at most twice the optimum, and it is the double-tree tour without the multigraph.
solves: [metric-tsp]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1977
  people: [Daniel J. Rosenkrantz, Richard E. Stearns, Philip M. Lewis II]
  note: The tour by a walk of a minimum spanning tree and its bound 2 appear in the TSP literature of the mid 1970s; CLRS presents it as APPROX-TSP-TOUR.
prereqs: [metric-tsp, minimum-spanning-tree, preorder-traversal, double-tree-algorithm, mst-lower-bound-for-tsp]
see_also: [double-tree-algorithm, mst-tsp-heuristic, christofides-algorithm, prim, iterative-depth-first-search, two-opt]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 35.2.1 (APPROX-TSP-TOUR, the full walk, and Theorem 35.2)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 2, Section 2.4 (the double-tree algorithm)
  - paper: doi:10.1137/0206041
    title: Daniel J. Rosenkrantz, Richard E. Stearns and Philip M. Lewis II, An analysis of several heuristics for the traveling salesman problem, SIAM Journal on Computing 6(3), 1977
    locator: pages 563 to 581
---

The MST preorder walk builds a [minimum spanning tree](/minimum-spanning-tree/), roots it at a start vertex, and visits the vertices in [preorder](/preorder-traversal/). For [metric TSP](/metric-tsp/) the tour costs at most $2(1 - 1/n) \cdot \text{OPT}$ on each instance, and this bound is tight. Its tours are exactly the tours of the [double-tree algorithm](/double-tree-algorithm/), but it needs no multigraph and no Euler circuit. It is APPROX-TSP-TOUR in CLRS.

## In plain words

Connect all cities as cheaply as possible without loops. This gives a tree. Hang the tree from the home city, like a family tree.

Now visit the cities in the order in which a reader of the family tree meets the names: first a parent, then all of the first child's family, then all of the second child's family, and so on. Go back home at the end.

This is the same trip that you get if you walk around the whole tree, using each road two times, and skip each city that you already saw. That walk costs two times the tree. Skipping never makes a trip longer when roads obey the rule that a direct road is never longer than a detour. The tree is cheaper than the best trip, so the trip is at most two times the best.

## The problem

The input is a set $V$ of $n$ vertices with costs $c(u, v) = c(v, u) \ge 0$ that satisfy the [triangle inequality](/triangle-inequality/). The output is a tour, an order of all vertices, and its cost includes the edge back to the first vertex. OPT is the least cost of a tour and ALG is the cost of the output. The ratio $\rho$ means ALG $\le \rho \cdot$ OPT on each instance.

## The algorithm

```pseudo id=main
APPROX-TSP-TOUR(V, c, r)                   ▷ r is the start vertex
L1  T ← a minimum spanning tree of (V, c), rooted at r
L2  H ← empty list, S ← a stack that holds r
L3  while S is not empty do
L4      v ← pop(S)
L5      append v to H
L6      push the children of v on S, the last child first
L7  return H                               ▷ the tour visits H in order and returns to r
```

Line L1 uses [Prim's algorithm](/prim/) from $r$, which gives the parent of each vertex. The children of each vertex keep the order in which Prim adds them. Lines L2 to L6 are an [iterative depth-first search](/iterative-depth-first-search/) of the tree. A tree has no cycle, so no vertex is pushed two times, and no "visited" array is needed. Line L6 pushes the children in reverse, so the first child is popped first, and $H$ is the preorder.

**Why this is the double-tree tour.** The *full walk* of $T$ goes down each edge to a child, walks the subtree of the child, and comes back up the same edge. It is an Euler circuit of the doubled tree. The first visit of each vertex in the full walk happens when the walk goes down to it, and the walk goes down in preorder. So skipping the repeated vertices of the full walk leaves exactly $H$. The converse is also true: each Euler circuit of the doubled tree that starts at $r$ is the full walk for some order of the children, because the walk crosses each tree edge only two times, so it must cross it down, finish the subtree, and then cross it up. So the two algorithms produce the same set of tours.

## Example

Seven cities with the Manhattan distance: $A(5,1)$, $B(6,5)$, $C(0,0)$, $D(8,0)$, $E(5,4)$, $F(0,4)$ and $G(3,0)$. Prim from $A$ adds $E$, $B$, $G$, $C$, $D$, $F$ in this order, with the tree edges $AE$ (3), $EB$ (2), $AG$ (3), $GC$ (3), $AD$ (4) and $CF$ (4), of total cost 19. So $A$ has the children $E$, $G$, $D$, the vertex $E$ has the child $B$, $G$ has $C$, and $C$ has $F$.

| step | pop (line L4) | $H$ after line L5 | stack after line L6, top at the right |
|---|---|---|---|
| 0 |  |  | $A$ |
| 1 | $A$ | $A$ | $D\,G\,E$ |
| 2 | $E$ | $A\,E$ | $D\,G\,B$ |
| 3 | $B$ | $A\,E\,B$ | $D\,G$ |
| 4 | $G$ | $A\,E\,B\,G$ | $D\,C$ |
| 5 | $C$ | $A\,E\,B\,G\,C$ | $D\,F$ |
| 6 | $F$ | $A\,E\,B\,G\,C\,F$ | $D$ |
| 7 | $D$ | $A\,E\,B\,G\,C\,F\,D$ | empty |

The tour $A\,E\,B\,G\,C\,F\,D\,A$ costs 36. The full walk of the same tree is $A\,E\,B\,E\,A\,G\,C\,F\,C\,G\,A\,D\,A$, of cost $2 \cdot 19 = 38$, and its first visits are the same tour, as the double-tree page shows step by step. The optimum is 28, so ALG/OPT $\approx 1.29$.

## Correctness

**Theorem.** For metric costs, APPROX-TSP-TOUR returns a tour of cost at most $2\,c(T) \le 2(1 - 1/n) \cdot \text{OPT}$, on each instance and for each order of the children.

The analysis has three steps. First, $c(T) \le (1 - 1/n) \cdot \text{OPT}$, because an optimal tour without its most costly edge is a spanning tree. This is the [MST lower bound](/mst-lower-bound-for-tsp/), and it is the only lower bound on OPT that the analysis uses. Second, the full walk costs $2\,c(T)$, and $H$ is its list of first visits. Third, each edge $\{h_i, h_{i+1}\}$ of the tour replaces a part of the full walk, and by the triangle inequality the edge costs at most that part. The invariant of the loop of line L3 is: $H$ followed by the stack, read from the top down, is a prefix of the preorder followed by the subtrees still to visit, in order. The full proof is in the proof file.

**Tightness.** The wheel example of the [double-tree page](/double-tree-algorithm/) applies without change: a center 0, leaves $1, \ldots, k$ ($k \ge 5$ odd), cost 1 on spokes and on rim edges between leaves whose numbers differ by 2 modulo $k$, and cost 2 on the other pairs. The star is a minimum spanning tree, the preorder is $0, 1, \ldots, k$, ALG $= 2k = 2n - 2$ and OPT $= n$. So the ratio $2(1 - 1/n)$ is reached for each even $n \ge 6$.

**Hardness.** Better algorithms exist: [Christofides' algorithm](/christofides-algorithm/) has ratio 3/2. No polynomial algorithm has a ratio below $123/122$ unless P = NP ([metric TSP inapproximability](/metric-tsp-inapproximability/)).

## Complexity

- **Line L1.** Prim's algorithm with an array takes $\Theta(n^2)$ time on the complete graph, which is linear in the size of the cost matrix.
- **Lines L2 to L7.** Each vertex is pushed and popped one time, so the walk takes $\Theta(n)$ time.
- **Total.** $\Theta(n^2)$ time in the worst case in the [word RAM](/word-ram/), and $\Theta(n)$ extra space for the parents, the child lists and the stack.

With points in the plane, a [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) makes the total $O(n \log n)$.

## Properties

- **Same tours as the double-tree algorithm.** The set of possible outputs, over all orders of the children, is the set of possible double-tree outputs, over all Euler circuits.
- **Simpler.** No multigraph, no edge marks and no Euler circuit. The code after Prim is about ten lines.
- **Deterministic.** With a fixed order of the children, the output depends only on the input.
- **The order of the children matters.** Different orders give tours of different costs, all at most $2\,c(T)$. The bound does not prefer one order.

## Variants and improvements

- **Better child orders.** Order the children of each vertex to reduce the cost, for example by the angle around the parent for points in the plane. This helps in practice but keeps the worst case.
- **Postorder.** A postorder walk gives the reverse of a preorder walk for the reversed child order, so it has the same bound.
- **[Christofides' algorithm](/christofides-algorithm/).** Add a matching on the odd-degree vertices instead of doubling the tree, for ratio 3/2.
- **Local search.** Use the tour as the start of [2-opt](/two-opt/). The [MST TSP heuristic](/mst-tsp-heuristic/) page compares the choices in practice.

## When to use it

Use the preorder walk when you want the double-tree guarantee with the least code: Prim and a stack. It is a good start tour for local search and a good teaching example of an approximation algorithm with a lower bound. Use [Christofides' algorithm](/christofides-algorithm/) for a better bound.

## Pitfalls

- **A recursive walk.** A recursive version of lines L3 to L6 has depth up to $n - 1$ when the tree is a path. In Python this passes the recursion limit at about 1000 vertices. Use the explicit stack.
- **The children in the wrong order in line L6.** Pushing the first child first makes the stack pop the last child first. The result is still a preorder, of the reversed child order, so the bound holds, but the tour differs from the one in a hand trace.
- **Missing the triangle inequality.** The proof of the third step needs it. For a graph with edge lengths, use the shortest path costs, and then expand each tour edge into a shortest path.
- **A tree that is not minimum in line L1.** Each spanning tree gives a tour of cost at most $2\,c(T)$, but only a minimum tree gives $c(T) \le \text{OPT}$.

## Implementations

## History

Tours from a walk of a minimum spanning tree, and the bound 2 for metric costs, appear in the analysis of TSP heuristics in the mid 1970s, for example in Rosenkrantz, Stearns and Lewis (1977). The preorder form with the name APPROX-TSP-TOUR is the one in the textbook of Cormen, Leiserson, Rivest and Stein, which proves Theorem 35.2 with the full walk.

## References
