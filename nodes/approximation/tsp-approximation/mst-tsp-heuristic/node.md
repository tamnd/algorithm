---
tag: HM8R8X
kind: algorithm
slug: mst-tsp-heuristic
name: Minimum spanning tree TSP heuristic
aliases:
- MST-based TSP heuristics
- spanning tree heuristics for TSP
area: approximation/tsp-approximation
level: core
summary: The family of TSP heuristics that make a minimum spanning tree Eulerian, by doubling it or by a matching, shortcut an Euler circuit and often finish with 2-opt; ratio 2 or 3/2 for metric costs.
solves: [metric-tsp]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1976
  people: [Nicos Christofides, Daniel J. Rosenkrantz, Richard E. Stearns, Philip M. Lewis II]
  note: Tree-based tours with the bound 2 were known by the mid 1970s; Christofides added the matching for 3/2 in 1976.
prereqs: [metric-tsp, minimum-spanning-tree, eulerian-circuit, mst-lower-bound-for-tsp]
see_also: [double-tree-algorithm, mst-preorder-walk-tsp, christofides-algorithm, two-opt, lin-kernighan, nearest-neighbor-tsp, nearest-insertion]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 2, Section 2.4 (the double-tree algorithm and Christofides' algorithm)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 35.2.1 (APPROX-TSP-TOUR)
  - book: isbn:9780691129938
    title: David L. Applegate, Robert E. Bixby, Vašek Chvátal and William J. Cook, The Traveling Salesman Problem, A Computational Study
    locator: Chapter 15 (tour construction and local search)
  - paper: doi:10.1137/0206041
    title: Daniel J. Rosenkrantz, Richard E. Stearns and Philip M. Lewis II, An analysis of several heuristics for the traveling salesman problem, SIAM Journal on Computing 6(3), 1977
    locator: pages 563 to 581
---

The minimum spanning tree TSP heuristic is the family of tour construction methods that start from a [minimum spanning tree](/minimum-spanning-tree/), add edges until each degree is even, walk an [Euler circuit](/eulerian-circuit/) and skip the repeated vertices. With a second copy of the tree it is the [double-tree algorithm](/double-tree-algorithm/), or the equal [MST preorder walk](/mst-preorder-walk-tsp/), with ratio 2. With a matching on the odd-degree vertices it is [Christofides' algorithm](/christofides-algorithm/), with ratio 3/2. In practice a [2-opt](/two-opt/) pass usually follows, and it keeps the bound.

## In plain words

A cheap network that connects all cities, with no loops, is a good skeleton for a round trip. The best round trip always costs more than this network.

To turn the network into a round trip, each city must have an even number of roads, so that a walker who comes in can also go out. There are two ways to fix this. Copy every road, or add a cheap set of extra roads that pairs up the cities with an odd number of roads. Then walk all roads in one loop, and skip the cities that you already saw.

The second way costs more work but gives a better guarantee. After either way, you can improve the trip: whenever two parts of the trip cross, swap them so that they do not cross.

## The problem

The input is a set $V$ of $n$ vertices with symmetric non-negative costs that satisfy the [triangle inequality](/triangle-inequality/). The output is a tour through all vertices, and its cost includes the edge back to the start. OPT is the least cost of a tour and ALG is the cost of the output. A ratio $\rho$ means ALG $\le \rho \cdot$ OPT on each instance. This is the [metric TSP](/metric-tsp/).

## The algorithm

```pseudo id=main
MST-TSP(V, c, r, augment, improve)
L1  T ← a minimum spanning tree of (V, c)
L2  if augment = DOUBLE then
L3      A ← a second copy of each edge of T
L4  else A ← a minimum weight perfect matching on the odd-degree vertices of T
L5  W ← an Euler circuit of the multigraph T + A that starts at r
L6  H ← the vertices of W in the order of their first visit
L7  while improve and H has an improving 2-opt move (i, j) do
L8      reverse H[i + 1 .. j]
L9  return H
```

Lines L2 to L4 make each degree of $T + A$ even. Line L3 doubles each degree. Line L4 gives one extra edge to each vertex of odd degree; there is an even number of them by the [handshaking lemma](/handshaking-lemma/). Line L6 is the shortcut step. A 2-opt move removes the edges $\{h_i, h_{i+1}\}$ and $\{h_j, h_{j+1}\}$ and adds $\{h_i, h_j\}$ and $\{h_{i+1}, h_{j+1}\}$; it is improving when the two new edges cost less than the two old ones. Line L8 makes the move by reversing the part between them. The implementation takes the first improving move that it finds.

The members of the family are these.

| augment | improve | name | ratio | time |
|---|---|---|---|---|
| DOUBLE | no | [double tree](/double-tree-algorithm/), [preorder walk](/mst-preorder-walk-tsp/) | 2 | $\Theta(n^2)$ |
| MATCHING | no | [Christofides](/christofides-algorithm/) | 3/2 | $O(n^3)$ |
| DOUBLE | yes | double tree with 2-opt | 2 | $\Theta(n^2)$ per 2-opt round |
| MATCHING | yes | Christofides with 2-opt | 3/2 | $O(n^3)$, then $O(n^2)$ per round |

## Example

Seven cities with the Manhattan distance: $A(5,1)$, $B(6,5)$, $C(0,0)$, $D(8,0)$, $E(5,4)$, $F(0,4)$ and $G(3,0)$. The minimum spanning tree has the edges $AE$, $EB$, $AG$, $GC$, $AD$ and $CF$ and costs 19. The odd-degree vertices are $A$, $B$, $D$ and $F$, and the minimum matching on them is $\{AD, BF\}$ of cost 11. The optimum is 28.

| variant | tour | cost | ALG/OPT |
|---|---|---|---|
| DOUBLE, no 2-opt | $A\,E\,B\,G\,C\,F\,D$ | 36 | 1.29 |
| DOUBLE, with 2-opt | an optimal tour | 28 | 1 |
| MATCHING, no 2-opt | $A\,E\,B\,F\,C\,G\,D$ | 28 | 1 |
| MATCHING, with 2-opt | the same tour (no move improves it) | 28 | 1 |

The double-tree tour has the costly edges $BG$ (8) and $FD$ (12), and these two segments cross in the plane. The 2-opt move that replaces them by $BF$ (7) and $GD$ (5) gains $20 - 12 = 8$ and gives the tour $A\,E\,B\,F\,C\,G\,D$ of cost 28, which is the Christofides tour.

**Behaviour on random points.** We ran the four variants on 100 instances of 10 points, drawn uniformly in the unit square with the seed 12345, with the Euclidean distance, and computed OPT exactly by the [Held-Karp dynamic program](/held-karp-algorithm/).

| variant | mean ALG/OPT | worst ALG/OPT | optimal tours |
|---|---|---|---|
| DOUBLE, no 2-opt | 1.150 | 1.373 | 9 of 100 |
| DOUBLE, with 2-opt | 1.006 | 1.112 | 79 of 100 |
| MATCHING, no 2-opt | 1.054 | 1.216 | 18 of 100 |
| MATCHING, with 2-opt | 1.006 | 1.100 | 75 of 100 |

The tree itself cost 0.728 of OPT on average. So the bounds 2 and 3/2 are far from the typical ratio, the matching helps much without local search, and 2-opt removes most of the difference. On larger random instances the gaps of the plain variants grow, and 2-opt alone is no longer enough to get near the optimum; the computational study of Applegate, Bixby, Chvátal and Cook compares the methods on large instances.

## Correctness

**Theorem.** For metric costs, MST-TSP returns a tour of cost at most $2 \cdot \text{OPT}$ with DOUBLE and at most $\tfrac{3}{2} \cdot \text{OPT}$ with MATCHING. The bound is absolute. With improve, the loop of lines L7 and L8 stops, and the final tour costs at most the tour of line L6.

The lower bounds on OPT are $c(T) \le \text{OPT}$ (the [MST lower bound](/mst-lower-bound-for-tsp/)) and, for MATCHING, $c(A) \le \text{OPT}/2$. The circuit costs $c(T) + c(A)$, which is $2c(T)$ or $c(T) + c(A)$, and the shortcuts of line L6 do not raise the cost by the triangle inequality. Each move of line L8 lowers the cost strictly, and there are finitely many tours, so the loop stops. The invariant of the loop is: $H$ is a tour and $c(H)$ is at most the cost after line L6. The full proof is in the proof file, and the pages of the [double-tree algorithm](/double-tree-algorithm/) and of [Christofides' algorithm](/christofides-algorithm/) give the details of each case.

**Tightness.** Without 2-opt, both ratios are tight: the wheel example on the double-tree page gives $2(1 - 1/n)$, and the path example on the Christofides page tends to 3/2. With 2-opt the bounds are still the only general guarantee, because a tour where no 2-opt move helps can cost $\Theta(\sqrt{n})$ times OPT on some metric instances (Chandra, Karloff and Tovey 1999). On the wheel example of the double-tree page, 2-opt does improve the tour.

**Hardness.** No polynomial algorithm has a ratio below $123/122$ for metric TSP unless P = NP ([metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality, no constant ratio is possible ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **DOUBLE.** Prim's algorithm takes $\Theta(n^2)$ time on the complete graph, and the Euler circuit and the shortcuts take $O(n)$.
- **MATCHING.** The minimum weight perfect matching takes $O(n^3)$ time with a blossom algorithm. The implementation on this page uses an exact dynamic program over subsets of the odd-degree vertices instead, in $O(2^k k)$ time for $k$ of them, so it is only for small $n$.
- **2-opt.** One search for an improving move checks $O(n^2)$ pairs. The number of moves is not polynomial in the worst case, even for points in the plane (Englert, Röglin and Vöcking), but in practice it is small, and neighbor lists make each search much faster.
- **Space.** $O(n)$ extra for DOUBLE, and $O(n^2)$ for a blossom algorithm.

## Properties

- **Each member keeps its ratio after 2-opt.** Local search never raises the cost, so the start tour sets the guarantee.
- **A bound for each run.** The run computes $c(T) \le \text{OPT}$, and for MATCHING also $2c(A) \le \text{OPT}$. So the output comes with a certificate of quality for that instance.
- **Deterministic.** With fixed tie rules, the output depends only on the input.
- **Not online.** The tree needs all vertices first.

## Variants and improvements

- **Other start tours.** [Nearest neighbor](/nearest-neighbor-tsp/), [nearest insertion](/nearest-insertion/) and the [greedy edge heuristic](/greedy-edge-heuristic/) are other construction methods. Nearest insertion also has ratio 2 by an MST argument, and nearest neighbor has only a $O(\log n)$ ratio.
- **Stronger local search.** [Or-opt](/or-opt/), [3-opt](/three-opt/), [Lin-Kernighan](/lin-kernighan/) and [Lin-Kernighan-Helsgaun](/lin-kernighan-helsgaun/) give much better tours than 2-opt.
- **Trees from the LP.** The [Karlin-Klein-Oveis Gharan algorithm](/karlin-klein-oveis-gharan-algorithm/) samples a random tree from the solution of the [subtour LP](/subtour-elimination-lp/) and then adds the matching. Its ratio is $3/2 - 10^{-36}$ in expectation.
- **Directed costs.** For the [asymmetric TSP](/asymmetric-tsp/) the tree method fails, because a tree cannot be made Eulerian in a cheap way. The [Asadpour et al. algorithm](/asadpour-atsp-algorithm/) uses a thin tree and a circulation instead.

## When to use it

Use the DOUBLE member when you need a tour with a bound fast and with very little code, for example as a start tour of local search. Use the MATCHING member when the bound 3/2 matters, or when no local search follows. For good tours on large instances, use a strong local search such as Lin-Kernighan-Helsgaun; the tree gives the start and the lower bound $c(T)$.

## Pitfalls

- **Costs that are not metric.** Line L6 and the matching bound need the triangle inequality. On other costs the tour can be arbitrarily bad.
- **A set of edges in line L5.** $T + A$ is a multigraph. With DOUBLE each edge is there two times, and with MATCHING an edge of $A$ can repeat an edge of $T$. A set of edges loses the copies, and then the Euler circuit fails.
- **2-opt with floating point costs in line L7.** A move whose gain is only a rounding error can repeat forever. Ask for a gain larger than a small tolerance, or use integer costs.
- **The wrong segment in line L8.** The move must reverse $H[i + 1 .. j]$. Reversing $H[i .. j]$ makes a different tour, and the computed gain is wrong.

## Implementations

## History

Tours from minimum spanning trees, with the bound 2, were part of the analysis of TSP heuristics in the mid 1970s; Rosenkrantz, Stearns and Lewis (1977) used spanning trees to bound insertion methods. Christofides (1976) and Serdyukov (1978) replaced the second copy of the tree by a matching and got 3/2. Croes (1958) and Lin (1965) introduced 2-opt and 3-opt, and Lin and Kernighan (1973) the variable-depth search that is still the base of the best heuristics.

## References
