---
tag: K3DBM0
kind: algorithm
slug: double-tree-algorithm
name: Double-tree algorithm
aliases:
- tree doubling
- MST doubling 2-approximation
area: approximation/tsp-approximation
level: core
summary: Doubles a minimum spanning tree, takes an Euler circuit and skips the repeated vertices; a 2-approximation for metric TSP.
solves: [metric-tsp]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1976
  people: [Nicos Christofides, Daniel J. Rosenkrantz, Richard E. Stearns, Philip M. Lewis II]
  note: The tree-doubling bound of 2 for metric TSP was known by the mid 1970s; Christofides (1976) improved it to 3/2 by a matching.
prereqs: [metric-tsp, minimum-spanning-tree, mst-lower-bound-for-tsp, eulerian-circuit, triangle-inequality]
see_also: [mst-preorder-walk-tsp, mst-tsp-heuristic, christofides-algorithm, prim, hierholzer-algorithm, two-opt, metric-tsp-inapproximability]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 2, Section 2.4 (the double-tree algorithm and its ratio 2)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 3, Section 3.2 (metric TSP, a simple factor 2 algorithm and its tight example)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 35.2.1 (APPROX-TSP-TOUR and Theorem 35.2)
  - paper: doi:10.1137/0206041
    title: Daniel J. Rosenkrantz, Richard E. Stearns and Philip M. Lewis II, An analysis of several heuristics for the traveling salesman problem, SIAM Journal on Computing 6(3), 1977
    locator: pages 563 to 581
  - title: Nicos Christofides, Worst-case analysis of a new heuristic for the travelling salesman problem, Report 388, Graduate School of Industrial Administration, Carnegie Mellon University, 1976
    locator: the introduction (the tree method and its bound 2)
---

The double-tree algorithm is a 2-approximation for [metric TSP](/metric-tsp/). It takes a [minimum spanning tree](/minimum-spanning-tree/), uses each tree edge two times, walks along an [Euler circuit](/eulerian-circuit/) of the doubled tree, and skips each vertex that the walk already visited. The tour costs at most $2(1 - 1/n) \cdot \text{OPT}$ on each instance, and the analysis is tight. It runs in $\Theta(n^2)$ time on a cost matrix.

## In plain words

A salesman must visit each city one time and come back home. First connect all the cities as cheaply as possible, without any loop. This network is a tree, and the best round trip costs at least as much as the tree.

Now walk around the tree like an ant walks around the outline of a branch: go along each road out and later come back on it. This walk uses each road two times, so it costs two times the tree. It visits all cities, but it visits some of them many times.

Make the walk into a round trip: when the walk comes to a city that you already visited, go directly to the next new city. A direct road is never longer than a detour, so the round trip costs at most two times the tree, and so at most two times the best round trip.

## The problem

The input is a set $V$ of $n$ vertices and a cost $c(u, v) = c(v, u) \ge 0$ for each pair. The costs satisfy the [triangle inequality](/triangle-inequality/) $c(u, w) \le c(u, v) + c(v, w)$. The output is a tour: an order $v_1, \ldots, v_n$ of all vertices, with cost $c(v_1, v_2) + \cdots + c(v_{n-1}, v_n) + c(v_n, v_1)$. OPT is the least cost of a tour, and ALG is the cost of the tour that the algorithm returns. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem. This is the [metric TSP](/metric-tsp/).

## The algorithm

```pseudo id=main
DOUBLE-TREE(V, c, r)                       ▷ r is the start vertex
L1  T ← a minimum spanning tree of (V, c)
L2  D ← the multigraph with two copies of each edge of T
L3  W ← an Euler circuit of D that starts at r
L4  H ← empty list
L5  for each vertex v of W, in order do
L6      if v is not in H then              ▷ the shortcut: skip a vertex seen before
L7          append v to H
L8  return H                               ▷ the tour visits H in order and returns to H[1]
```

Line L1 uses [Prim's algorithm](/prim/) on the complete graph. Line L2 makes each degree even, because each tree degree is counted two times, and $D$ is connected because $T$ is. So by [Euler's theorem](/eulers-theorem-eulerian-graphs/) $D$ has an Euler circuit, and line L3 finds one with [Hierholzer's algorithm](/hierholzer-algorithm/). The circuit $W$ has $2(n-1)$ edges and visits each vertex at least one time. Lines L4 to L7 keep the first visit of each vertex and drop the others. When the tour goes from $H[i]$ to $H[i+1]$, it replaces a part of $W$ by one direct edge. The implementation keeps a Boolean array for the test of line L6.

## Example

Seven cities lie in the plane, and the cost is the Manhattan distance $|x_1 - x_2| + |y_1 - y_2|$, which is a metric. The cities are $A(5,1)$, $B(6,5)$, $C(0,0)$, $D(8,0)$, $E(5,4)$, $F(0,4)$ and $G(3,0)$.

Line L1 runs Prim's algorithm from $A$. It adds the edges $AE$ (3), $EB$ (2), $AG$ (3), $GC$ (3), $AD$ (4) and $CF$ (4), in this order. This is the only minimum spanning tree, and its cost is 19. The doubled tree has 12 edges, and line L3 finds the Euler circuit $W = A\,E\,B\,E\,A\,G\,C\,F\,C\,G\,A\,D\,A$, of cost 38.

| step | vertex of $W$ | line L6 | $H$ after the step |
|---|---|---|---|
| 1 | $A$ | new | $A$ |
| 2 | $E$ | new | $A\,E$ |
| 3 | $B$ | new | $A\,E\,B$ |
| 4 | $E$ | skip | $A\,E\,B$ |
| 5 | $A$ | skip | $A\,E\,B$ |
| 6 | $G$ | new | $A\,E\,B\,G$ |
| 7 | $C$ | new | $A\,E\,B\,G\,C$ |
| 8 | $F$ | new | $A\,E\,B\,G\,C\,F$ |
| 9 to 11 | $C$, $G$, $A$ | skip | $A\,E\,B\,G\,C\,F$ |
| 12 | $D$ | new | $A\,E\,B\,G\,C\,F\,D$ |
| 13 | $A$ | skip | $A\,E\,B\,G\,C\,F\,D$ |

The tour is $A\,E\,B\,G\,C\,F\,D\,A$ with cost $3 + 2 + 8 + 3 + 4 + 12 + 4 = 36$. The shortcut $B \to G$ replaces the part $B\,E\,A\,G$ of cost 8 by an edge of cost 8, and the shortcut $F \to D$ replaces $F\,C\,G\,A\,D$ of cost 14 by an edge of cost 12. An optimal tour is $A\,B\,E\,F\,C\,G\,D\,A$ with cost 28. So ALG/OPT $= 36/28 \approx 1.29$, below the bound $2 \cdot 19 = 38$.

## Correctness

**Theorem.** For metric costs, DOUBLE-TREE returns a tour of cost at most $2\,c(T) \le 2(1 - 1/n) \cdot \text{OPT}$. This bound holds on each instance (it is not an expected bound), for each choice of the tree in line L1 and of the circuit in line L3.

The proof has three steps.

1. **The lower bound on OPT.** Delete the most costly edge of an optimal tour. What is left is a spanning path, so a spanning tree, of cost at most $(1 - 1/n) \cdot \text{OPT}$. So $c(T) \le (1 - 1/n) \cdot \text{OPT}$. This is the [MST lower bound](/mst-lower-bound-for-tsp/), and it is the only lower bound on OPT that the analysis uses.
2. **The walk.** The circuit $W$ uses each edge of $T$ two times, so $c(W) = 2\,c(T)$.
3. **The shortcuts.** The invariant of the loop of line L5 is: $H$ is the list of distinct vertices of the part of $W$ read so far, in the order of their first visit, and the path through $H$ costs at most this part of $W$. A skip in line L6 keeps the path, and an append in line L7 adds one edge whose cost is at most the part of $W$ that it replaces, by the triangle inequality applied along that part. The closing edge back to $H[1]$ is handled in the same way.

So ALG $\le c(W) = 2\,c(T) \le 2(1 - 1/n) \cdot \text{OPT}$. The full proof is in the proof file.

**Tightness.** Take a center $0$ and leaves $1, \ldots, k$, with $k \ge 5$ odd, so $n = k + 1$. A spoke $\{0, i\}$ costs 1. A rim edge, between two leaves whose numbers differ by 2 modulo $k$, costs 1. Each other pair costs 2. All costs are 1 or 2, so they are a metric. The star of all spokes is a minimum spanning tree of cost $k$, and Prim's algorithm from the center returns it. The Euler circuit $0\,1\,0\,2\,0 \cdots 0\,k\,0$ gives the tour $0, 1, 2, \ldots, k$. Its edges $\{i, i+1\}$ between leaves cost 2, so ALG $= 1 + 2(k-1) + 1 = 2k$. The rim edges form one cycle through all leaves (because $k$ is odd), so the tour that starts at $0$, follows the rim from leaf 1 to leaf $k - 1$ and comes back to $0$ costs $k + 1 = n$. All tours cost at least $n$, so OPT $= n$ and

$$\frac{\text{ALG}}{\text{OPT}} = \frac{2n - 2}{n} = 2\left(1 - \frac{1}{n}\right).$$

This meets the theorem with equality, so the ratio $2$ of the double-tree algorithm cannot be improved by a better analysis.

**Hardness.** The ratio 2 is a property of this algorithm, not of the problem. [Christofides' algorithm](/christofides-algorithm/) gets 3/2. On the other side, no polynomial algorithm has a ratio below $123/122$ unless P = NP (Karlin, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality the shortcut step fails, and no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **Line L1.** Prim's algorithm with an array, on the complete graph, takes $\Theta(n^2)$ time. This is linear in the size of the cost matrix, so no algorithm that reads all costs can be faster.
- **Lines L2 and L3.** The doubled tree has $2(n-1)$ edges, and Hierholzer's algorithm takes $O(n)$ time on it.
- **Lines L4 to L8.** The walk has $2n - 1$ vertices, and each test of line L6 takes $O(1)$ time with a Boolean array.
- **Total.** $\Theta(n^2)$ time in the worst case, in the [word RAM](/word-ram/) with costs that fit in a word, and $\Theta(n)$ extra space besides the matrix.

For points in the plane, a [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) takes $O(n \log n)$ time, so the whole algorithm takes $O(n \log n)$ time.

## Properties

- **Deterministic.** With fixed tie rules in lines L1 and L3, the output depends only on the input.
- **Any tree, any circuit.** The bound $2\,c(T)$ holds for each spanning tree $T$ and each Euler circuit. Only the step $c(T) \le \text{OPT}$ needs a minimum tree.
- **The same tour as a preorder walk.** The first visits of an Euler circuit of the doubled tree, which goes down each edge and later back up, are a preorder of $T$. So the tour is the [MST preorder walk](/mst-preorder-walk-tsp/), which needs no multigraph.
- **A bound for each run.** The run computes $c(T)$, and $c(T) \le \text{OPT}$. So the value $\text{ALG}/c(T)$, which is at most 2, bounds the ratio of this tour on this instance, and it is often much smaller than 2.

## Variants and improvements

- **[MST preorder walk](/mst-preorder-walk-tsp/).** The same tour, by a depth-first walk of the tree. This is the form of CLRS (APPROX-TSP-TOUR).
- **[Christofides' algorithm](/christofides-algorithm/).** Replace the second copy of $T$ by a [minimum weight perfect matching](/minimum-weight-perfect-matching/) on the odd-degree vertices of $T$. The ratio becomes 3/2.
- **Local search after.** Run [2-opt](/two-opt/) or [Or-opt](/or-opt/) on the tour. In practice this removes most of the extra cost; the worst-case bound stays 2. The [MST TSP heuristic](/mst-tsp-heuristic/) page compares these choices.
- **Steiner tree.** The same argument, in reverse, shows that a minimum spanning tree on the terminals is a 2-approximation for the [Steiner tree problem](/steiner-tree-problem/).

## When to use it

Use the double-tree algorithm when you need a tour with a proved bound quickly and with little code. Use it as the start tour of a local search. For a better guarantee, use Christofides' algorithm. For good tours in practice, use [Lin-Kernighan](/lin-kernighan/) or another local search, because the double-tree tour is usually far from the optimum on random points. The [MST TSP heuristic](/mst-tsp-heuristic/) page gives measured numbers.

## Pitfalls

- **Costs that are not metric.** Line L6 is correct only with the triangle inequality. On a cost matrix that breaks it, one skipped part can be very cheap while the direct edge is very costly, and the tour can be arbitrarily bad. If the input is a graph, compute the shortest path costs first, for example with [Floyd-Warshall](/floyd-warshall/), and then map each edge of the tour back to a shortest path.
- **One copy of the tree in line L2.** A tree with $n \ge 3$ vertices has leaves of degree 1, so it has no Euler circuit. Line L3 then fails or returns a walk that misses edges.
- **Recursion in line L3.** A recursive Euler circuit or a recursive depth-first walk has depth up to $n - 1$ on a path-shaped tree. Use an explicit stack.
- **The closing edge.** The tour must return from the last vertex of $H$ to $H[1]$. A cost function that sums only $n - 1$ edges reports a value that is too small.

## Implementations

## History

The bound of 2 by doubling a minimum spanning tree was known by the mid 1970s. Rosenkrantz, Stearns and Lewis (1977) used minimum spanning trees to bound insertion heuristics by 2. Christofides (1976) and, independently, Serdyukov (1978) replaced the second copy of the tree by a matching and got 3/2. The algorithm is now the standard first example of an approximation algorithm for the TSP in textbooks.

## References
