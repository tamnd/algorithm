---
tag: 53V9N5
kind: algorithm
slug: rectilinear-minimum-spanning-tree
name: Rectilinear minimum spanning tree
aliases:
- RMST
- L1 minimum spanning tree
area: eda/routing
level: core
summary: Builds the minimum spanning tree of points under the L1 metric in O(n log n) time, from a sparse graph that joins each point to a nearest point in each octant.
solves: [minimum-spanning-tree]
model: real-ram
complexity:
  vars: {n: the number of points}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1979
  people: [F. K. Hwang, Andrew Chi-Chih Yao, Hai Zhou, Narendra Shenoy, William Nicholls]
  note: Hwang gave the first O(n log n) algorithm for the rectilinear MST in 1979, from the L1 Voronoi diagram. Yao showed in 1982 that nearest neighbors in cones contain an MST. Zhou, Shenoy and Nicholls gave a sweep without a Voronoi diagram in 2001.
prereqs: [minimum-spanning-tree, kruskal]
see_also: [minimum-spanning-tree, prim, kruskal, euclidean-minimum-spanning-tree, yao-graph, hwang-rectilinear-steiner-ratio, iterated-one-steiner, rectilinear-steiner-tree-problem]
sources:
  - paper: doi:10.1145/322123.322124
    title: F. K. Hwang, An O(n log n) algorithm for rectilinear minimal spanning trees, Journal of the ACM 26(2), 177 to 182, 1979
    locator: the O(n log n) algorithm from the Voronoi diagram in the L1 metric
  - paper: "Andrew Chi-Chih Yao, On constructing minimum spanning trees in k-dimensional spaces and related problems, SIAM Journal on Computing 11(4), 721 to 736, 1982"
    locator: the lemma that the nearest neighbors of each point in a set of narrow cones contain a minimum spanning tree (general locator)
  - paper: doi:10.1016/S0020-0190(01)00232-0
    title: Hai Zhou, Narendra Shenoy and William Nicholls, Efficient minimum spanning tree construction without Delaunay triangulation, Information Processing Letters 81(5), 271 to 276, 2002
    locator: the octant property of the L1 metric and the sweep that finds the octant neighbors in O(n log n) time
  - paper: "Hai Zhou, Narendra Shenoy and William Nicholls, Efficient minimum spanning tree construction without Delaunay triangulation, Proceedings of ASP-DAC 2001, Yokohama"
    locator: the conference version of the same method
---

The rectilinear minimum spanning tree (RMST) of a set of points in the plane is a [minimum spanning tree](/minimum-spanning-tree/) of the complete graph on the points, where an edge costs the L1 distance $|x_p - x_q| + |y_p - y_q|$. In electronic design automation (EDA) it is the first estimate of the wire of a net, and the start of Steiner tree heuristics such as [iterated 1-Steiner](/iterated-one-steiner/). Running [Prim's algorithm](/prim/) on all $\binom{n}{2}$ pairs takes $\Theta(n^2)$ time. The fast method on this page uses a fact about the L1 metric: some RMST uses only the edges from each point to a nearest point in each of eight octants around it. These at most $4n$ edges can be found by sweeps in $O(n \log n)$ time, and [Kruskal's algorithm](/kruskal/) then finds the tree in $O(n \log n)$.

## In plain words

You have pins on a chip and want to join them all with as little wire as possible, where each wire runs from pin to pin and its length is counted along the grid, across plus up.

The slow way compares every pair of pins. The fast way uses a trick. Stand at a pin and cut the plane around it into eight slices, like a pizza. In each slice you only need the nearest pin. A farther pin in the same slice is never needed, because the nearer pin is closer to it than you are.

So each pin has at most eight candidate wires, and each wire is found from both ends, which leaves at most four per pin. Sort these few wires by length and take them from the shortest, skipping any wire that joins pins that are already connected.

## The problem

The input is a list of $n$ points $p_1, \ldots, p_n$ with real coordinates. The L1 distance is $d(p, q) = |x_p - x_q| + |y_p - y_q|$. The output is a spanning tree of the points, a set of $n - 1$ pairs that connects them, of least total L1 length. Points that coincide can be joined by edges of length 0 first, so assume the points are distinct.

For a point $p$, the eight *octants* are the cones at $p$ bounded by the horizontal, vertical and diagonal lines through $p$. They are made half open, so that each other point lies in exactly one octant of $p$: octant $k$ holds the directions with angle in $[45k, 45(k+1))$ degrees. For two points, $q$ lies in an upper octant of $p$ (angles in $[0, 180)$) or $p$ lies in an upper octant of $q$, so it is enough to search the four upper octants of each point.

In the octant $[45, 90)$, the points $q$ have $x_q > x_p$ and $y_q - x_q \ge y_p - x_p$, and the distance is $d(p, q) = (x_q + y_q) - (x_p + y_p)$. So the nearest point there is the one with the least $x + y$ among the points in a region bounded by two inequalities. The other three upper octants become this one after a swap or a sign change of the coordinates, which keep L1 distances.

## The algorithm

```pseudo id=main
RMST(points)
L1  join repeated points by edges of length 0 and keep one copy of each
L2  for each of the four upper octants do
L3      map the coordinates so that this octant becomes {x' > x, y' − x' ≥ y − x}
L4      sort the points by decreasing x, and make an empty tree over the ranks of y − x
L5      for each point p in this order: find the point q with the least x + y among the points in the tree with y − x ≥ y_p − x_p
L6          if q exists then add the edge (p, q) with length d(p, q)
L7          insert p into the tree at the rank of y_p − x_p with the value x_p + y_p
L8  sort the edges by length and run Kruskal's algorithm with a disjoint-set forest
L9  return the tree edges
```

The tree of lines L4 to L7 is a [Fenwick tree](/fenwick-tree/) that answers "least value among ranks at least $r$" and takes inserts. The sweep goes in decreasing $x$, so when $p$ is handled, the tree holds the points to its right. The details of ties decide which of the two edges of each octant is open: points of equal $x$ are inserted after their queries when the octant needs $x' > x$ strictly, and a query asks for ranks above $y_p - x_p$ instead of at least it when the octant needs $y' - x' > y - x$. The [Yao graph](/yao-graph/) is the same construction with cones of any angle in the Euclidean plane.

## Example

Take the five points $a = (0, 0)$, $b = (4, 1)$, $c = (1, 4)$, $d = (5, 5)$ and $e = (2, 3)$. The nearest point in each upper octant is:

| point | $[0, 45)$ | $[45, 90)$ | $[90, 135)$ | $[135, 180)$ |
| --- | --- | --- | --- | --- |
| $a$ | $b$ (5) | $c$ (5) | none | none |
| $b$ | none | $d$ (5) | none | $e$ (4) |
| $c$ | $d$ (5) | none | none | none |
| $d$ | none | none | none | none |
| $e$ | $d$ (5) | none | none | $c$ (2) |

In the octant $[45, 90)$ of $a$, both $c$ and $e$ are at distance 5, and the tie goes to the lower index, $c$. The point $e$ is in the octant $[135, 180)$ of $b$, because the direction $(-2, 2)$ has angle exactly 135 degrees. The graph has 7 distinct edges, out of the 10 pairs: $ec$ of length 2, $be$ of 4, and $ab$, $ac$, $bd$, $cd$, $ed$ of 5. Kruskal takes $ec$ and $be$, then $ab$, skips $ac$ because $a$ and $c$ are now joined, and takes $bd$. The tree is

$ec = 2$, $be = 4$, $ab = 5$, $bd = 5$, with total length 16.

Prim's algorithm on all 10 pairs also gives 16. The pairs that the octant graph left out, such as $ad$ of length 10, are never needed.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Octant lemma.** If $q$ and $r$ lie in the same half-open octant of $p$ and $d(p, q) \le d(p, r)$, then $d(q, r) < d(p, r)$. The proof is a short case analysis in the octant $[45, 90)$, and the open side of the octant is what makes the inequality strict.
- **Short paths in the graph.** By induction on the length of a pair, every pair $p, r$ is joined in the octant graph by a path whose edges are all at most $d(p, r)$.
- **The MST survives.** An exchange argument, as in the [cycle property](/cycle-property/), turns any minimum spanning tree of all pairs into one that uses only edges of the octant graph, without making it longer. So the MST of the octant graph is an RMST.
- **The sweep finds the neighbors.** At the time $p$ is handled, the tree holds exactly the points of the region to the right of $p$, and the query on ranks returns the least $x + y$ among those with large enough $y - x$.

## Complexity

- **Time.** Each of the four sweeps sorts the points in $O(n \log n)$ and makes $n$ queries and $n$ inserts in a Fenwick tree, each $O(\log n)$. The graph has at most $4n$ edges, so Kruskal's algorithm takes $O(n \log n)$ for the sort and nearly linear time for the disjoint-set operations. The total is $O(n \log n)$.
- **Lower bound.** In the algebraic decision tree model, any RMST algorithm needs $\Omega(n \log n)$ time, since the tree of points on a line gives their sorted order. So the bound is $\Theta(n \log n)$.
- **Space.** The edges, the tree and the sorted orders take $\Theta(n)$ space.
- **Simple method.** Prim's algorithm with an array, on all pairs, takes $\Theta(n^2)$ time and $\Theta(n)$ space. For nets of a few dozen pins it is just as good.

## Properties

- **What is proved.** The algorithm returns a minimum spanning tree under the L1 metric for every input, in $O(n \log n)$ time.
- **Degree.** For distinct points, every RMST has at most one neighbor of $p$ in each half-open octant of $p$, so its maximum degree is at most 8. If $q$ and $r$ were tree neighbors of $p$ in the same octant with $d(p, q) \le d(p, r)$, replacing the edge $pr$ by $qr$ would give a shorter spanning tree, by the octant lemma.
- **Relation to Steiner trees.** By [Hwang's theorem](/hwang-rectilinear-steiner-ratio/), the RMST is at most 3/2 times the rectilinear Steiner minimum tree, and the ratio 3/2 is reached. So the RMST is a 3/2-approximation of the [rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/).
- **Not unique.** With ties in length, many trees have the same total length. The tie rules of the sweep and of Kruskal fix the one returned.

## Variants and improvements

- **Voronoi diagram.** Hwang (1979) built the L1 Voronoi diagram in $O(n \log n)$ time and took the MST from its dual graph, as in the Euclidean method from the [Delaunay triangulation](/delaunay-triangulation/).
- **Sweep with active sets.** Zhou, Shenoy and Nicholls (2001) found the octant neighbors with a sweep that keeps, for each octant, the points whose neighbor in that octant is not yet found. The Fenwick tree sweep of this page is another way to answer the same queries.
- **Other metrics.** In the Euclidean plane, the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) comes from the Delaunay triangulation. Yao (1982) used nearest neighbors in narrow cones for higher dimensions.
- **Steiner trees.** The RMST is the start of [iterated 1-Steiner](/iterated-one-steiner/), of edge-based Steiner heuristics, and of the [Prim-Dijkstra tradeoff](/prim-dijkstra-tradeoff/).

## When to use it

- To estimate the wire length of a net, or to start a Steiner tree heuristic, when the net has many pins.
- When an exact MST under L1 is needed for thousands or millions of points.

For nets with a few pins, Prim's algorithm on all pairs is simpler. For a better wire estimate use a Steiner tree, for example [FLUTE](/flute/), which is exact for small nets.

## Pitfalls

- **Closed octants.** If both boundary rays of an octant are included, the octant lemma only gives $d(q, r) \le d(p, r)$: for $p = (0, 0)$, $q = (1, 1)$ and $r = (0, 2)$ all three distances are 2. The proof by induction then breaks. Make each octant half open, and handle points of equal $x$ or equal $y - x$ by the rule of the octant.
- **Only four octants per point.** The four upper octants of every point cover every pair once. Searching only the octant $[45, 90)$ of each point, or only two octants, misses edges.
- **Repeated points.** Two points at the same place are in no octant of each other. Join them by edges of length 0 before the sweep.
- **Euclidean intuition.** The L1 metric is not the Euclidean metric. Methods that rely on Euclidean angles, such as the empty circle of the Delaunay triangulation, need the L1 versions.

## Implementations

## History

The minimum spanning tree under the L1 metric was studied with the rectilinear Steiner problem in the 1960s and 1970s, when Hanan (1966) studied the rectilinear Steiner problem and Hwang (1976) bounded the ratio of the two trees. F. K. Hwang gave the first $O(n \log n)$ algorithm in 1979, by building the Voronoi diagram in the L1 metric. Andrew Yao showed in 1982 that the nearest neighbors of each point in a fixed set of cones contain a minimum spanning tree, which gave the graphs now called Yao graphs. Hai Zhou, Narendra Shenoy and William Nicholls presented a simple sweep for the octant neighbors in the L1 metric at ASP-DAC 2001, and the journal version appeared in Information Processing Letters in 2002.

## References
