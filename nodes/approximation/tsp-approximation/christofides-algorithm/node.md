---
tag: XH4RYS
kind: algorithm
slug: christofides-algorithm
name: Christofides' algorithm
aliases:
- Christofides-Serdyukov algorithm
- Christofides heuristic
area: approximation/tsp-approximation
level: core
summary: A minimum spanning tree plus a minimum weight perfect matching on its odd-degree vertices gives an Eulerian multigraph; shortcutting its Euler circuit gives a 3/2-approximation for metric TSP.
solves: [metric-tsp]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1976
  people: [Nicos Christofides, Anatoliy I. Serdyukov]
  note: Christofides published the algorithm in a 1976 report; Serdyukov found it independently and published it in 1978 in Russian.
prereqs: [metric-tsp, minimum-spanning-tree, minimum-weight-perfect-matching, eulerian-circuit, handshaking-lemma, mst-lower-bound-for-tsp]
see_also: [double-tree-algorithm, mst-tsp-heuristic, karlin-klein-oveis-gharan-algorithm, held-karp-bound, subtour-elimination-lp, edmonds-blossom, metric-tsp-inapproximability]
sources:
  - title: Nicos Christofides, Worst-case analysis of a new heuristic for the travelling salesman problem, Report 388, Graduate School of Industrial Administration, Carnegie Mellon University, 1976
    locator: the main theorem (the ratio 3/2)
  - paper: doi:10.1016/j.hm.2020.04.003
    title: René van Bevern and Viktoriia A. Slugina, A historical note on the 3/2-approximation algorithm for the metric traveling salesman problem, Historia Mathematica 53, 2020
    locator: pages 118 to 127, with a translation of Serdyukov (1978)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 2, Section 2.4 (Christofides' algorithm and its ratio 3/2)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 3, Section 3.2 (the factor 3/2 algorithm and its tight example)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, sixth edition
    locator: Chapter 21, The Traveling Salesman Problem (approximation algorithms, Christofides' algorithm)
  - title: Laurence A. Wolsey, Heuristic analysis, linear programming and branch and bound, Mathematical Programming Study 13, 1980
    locator: pages 121 to 134 (the bound 3/2 with respect to the subtour LP)
---

Christofides' algorithm is a 3/2-approximation for [metric TSP](/metric-tsp/). It takes a [minimum spanning tree](/minimum-spanning-tree/) $T$, adds a [minimum weight perfect matching](/minimum-weight-perfect-matching/) $M$ on the vertices of odd degree in $T$, walks an [Euler circuit](/eulerian-circuit/) of $T + M$, and skips the repeated vertices. The tour costs at most $\tfrac{3}{2} \cdot \text{OPT}$ on each instance, and the ratio is tight. Christofides (1976) and Serdyukov (1978) found it independently, and for more than 40 years no better ratio was known.

## In plain words

Start as in the [double-tree algorithm](/double-tree-algorithm/): connect all cities as cheaply as possible without loops. A round trip must enter and leave each city, so each city needs an even number of roads. In the tree, some cities have an odd number of roads.

Instead of copying the whole tree, add only a few roads: pair up the cities that have an odd number of roads, in the cheapest way. Now each city has an even number of roads, and you can walk all of them in one closed trip. Skip the cities that you have already visited.

The tree costs less than the best trip. The pairing costs at most half of the best trip, because the best trip, when you look only at the odd cities, splits into two pairings. So the result is at most one and a half times the best trip.

## The problem

The input is a set $V$ of $n$ vertices with costs $c(u, v) = c(v, u) \ge 0$ that satisfy the [triangle inequality](/triangle-inequality/). The output is a tour through all vertices; its cost includes the edge back to the start. OPT is the least cost of a tour and ALG is the cost of the output. The ratio $\rho$ means ALG $\le \rho \cdot$ OPT on each instance.

## The algorithm

```pseudo id=main
CHRISTOFIDES(V, c, r)                      ▷ r is the start vertex
L1  T ← a minimum spanning tree of (V, c)
L2  O ← the vertices of odd degree in T
L3  M ← a minimum weight perfect matching of the complete graph on O
L4  W ← an Euler circuit of the multigraph T + M that starts at r
L5  H ← empty list
L6  for each vertex v of W, in order do
L7      if v is not in H then              ▷ the shortcut
L8          append v to H
L9  return H                               ▷ the tour visits H in order and returns to H[1]
```

By the [handshaking lemma](/handshaking-lemma/), the sum of the degrees in $T$ is even, so $|O|$ is even and the matching of line L3 exists. Line L3 uses [Edmonds' blossom algorithm](/edmonds-blossom/) with weights. Each vertex of $O$ gets one more edge, so in $T + M$ all degrees are even, and $T + M$ is connected because $T$ is. So the Euler circuit of line L4 exists. $T + M$ is a multigraph: an edge of $M$ can also be an edge of $T$, and then both copies stay. Lines L5 to L8 are the same shortcut step as in the double-tree algorithm.

## Example

Seven cities with the Manhattan distance: $A(5,1)$, $B(6,5)$, $C(0,0)$, $D(8,0)$, $E(5,4)$, $F(0,4)$ and $G(3,0)$. Line L1 gives the tree $AE$ (3), $EB$ (2), $AG$ (3), $GC$ (3), $AD$ (4) and $CF$ (4), of cost 19.

| vertex | $A$ | $B$ | $C$ | $D$ | $E$ | $F$ | $G$ |
|---|---|---|---|---|---|---|---|
| degree in $T$ | 3 | 1 | 2 | 1 | 2 | 1 | 2 |

So $O = \{A, B, D, F\}$. Four vertices have three perfect matchings:

| matching | cost |
|---|---|
| $AB$, $DF$ | $5 + 12 = 17$ |
| $AD$, $BF$ | $4 + 7 = 11$ |
| $AF$, $BD$ | $8 + 7 = 15$ |

Line L3 picks $M = \{AD, BF\}$ of cost 11. The edge $AD$ is now in $T + M$ two times. The multigraph has 8 edges of total cost 30, and line L4 finds the Euler circuit $A\,E\,B\,F\,C\,G\,A\,D\,A$. The shortcut skips only the second $A$, so the tour is $A\,E\,B\,F\,C\,G\,D\,A$ with cost $3 + 2 + 7 + 4 + 3 + 5 + 4 = 28$. The shortcut $G \to D$ (cost 5) replaced $G\,A\,D$ (cost 7). This tour is optimal; the double-tree algorithm gives 36 on the same instance. The bound promises at most $19 + 11 = 30 \le 1.5 \cdot 28 = 42$.

## Correctness

**Theorem.** For metric costs, CHRISTOFIDES returns a tour of cost at most $c(T) + c(M) \le \tfrac{3}{2} \cdot \text{OPT}$. The bound is absolute: it holds on each instance, for each choice of the tree, the matching and the circuit.

The analysis uses two lower bounds on OPT.

1. **The tree.** $c(T) \le \text{OPT}$, because an optimal tour without one edge is a spanning tree. This is the [MST lower bound](/mst-lower-bound-for-tsp/).
2. **The matching.** $c(M) \le \text{OPT}/2$. Shortcut an optimal tour so that it visits only the vertices of $O$, in the same order. By the triangle inequality this cycle $C_O$ costs at most OPT. It has $|O|$ edges, an even number, so its edges split into two perfect matchings of $O$: the odd-numbered edges and the even-numbered edges. The cheaper of the two costs at most $c(C_O)/2 \le \text{OPT}/2$, and $M$ is a minimum matching.

The Euler circuit $W$ costs $c(T) + c(M)$, and the shortcut step does not increase the cost, by the triangle inequality. So ALG $\le c(T) + c(M) \le \text{OPT} + \text{OPT}/2$. The full proof is in the proof file.

**A stronger lower bound.** Wolsey (1980) showed that the same tour costs at most $\tfrac{3}{2}$ times the value LP* of the [subtour elimination LP](/subtour-elimination-lp/), which is the [Held-Karp bound](/held-karp-bound/). The reason is that $(1 - 1/n)x^*$ lies in the [spanning tree polytope](/spanning-tree-polytope/), and $x^*/2$ lies in the dominant of the polytope of the $O$-joins. This is cited here, not proved. It shows that the integrality gap of the subtour LP is at most 3/2.

**Tightness.** Take $n$ odd and the vertices $1, \ldots, n$ on a line. The edges $\{i, i+1\}$ cost 1, the edges $\{i, i+2\}$ cost $1 + \varepsilon$, and each other pair costs its shortest path distance in this graph. The path $1, 2, \ldots, n$ is the only minimum spanning tree, with cost $n - 1$, and its odd-degree vertices are its two ends. The matching edge $\{1, n\}$ costs $\tfrac{n-1}{2}(1 + \varepsilon)$, by the edges of cost $1 + \varepsilon$. $T + M$ is already a tour, so

$$\text{ALG} = (n - 1) + \tfrac{n-1}{2}(1 + \varepsilon).$$

The tour $1, 3, 5, \ldots, n, n-1, n-3, \ldots, 2, 1$ uses $n - 2$ edges of cost $1 + \varepsilon$ and two edges of cost 1, so OPT $\le (n - 2)(1 + \varepsilon) + 2$. When $n$ grows and $\varepsilon$ goes to 0, ALG/OPT tends to $3/2$. For $n = 201$ and $\varepsilon = 1/1000$ the ratio is more than 1.48. So the analysis cannot be improved.

**Hardness.** No polynomial algorithm has a ratio below $123/122$ unless P = NP (Karlin, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). The best known ratio is $3/2 - 10^{-36}$, by the randomized [Karlin-Klein-Oveis Gharan algorithm](/karlin-klein-oveis-gharan-algorithm/).

## Complexity

- **Line L1.** Prim's algorithm takes $\Theta(n^2)$ time on the complete graph.
- **Line L3.** A minimum weight perfect matching on $|O| \le n$ vertices of a complete graph takes $O(n^3)$ time with the blossom algorithm in the forms of Lawler and of Gabow. This is the most costly step.
- **Lines L4 to L9.** $T + M$ has at most $\tfrac{3}{2}n$ edges, so the Euler circuit and the shortcut take $O(n)$ time.
- **Total.** $O(n^3)$ time in the worst case in the [word RAM](/word-ram/), and $O(n^2)$ extra space for the matching step.

The implementation on this page computes the matching of line L3 exactly by a dynamic program over the subsets of $O$, in $O(2^k k)$ time for $k = |O|$. This keeps the code short and exact, but it is only for small instances. A practical program uses a blossom code, for example Blossom V of Kolmogorov.

## Properties

- **Deterministic, absolute ratio.** The ratio 3/2 holds on each instance, not only in expectation.
- **A bound for each run.** The run computes $c(T)$ and $c(M)$, with $c(T) \le \text{OPT}$ and $2c(M) \le \text{OPT}$. So $\max(c(T), 2c(M))$ is a lower bound on OPT that comes free with the tour.
- **Compared with the LP.** ALG $\le \tfrac{3}{2} \cdot \text{LP}^*$ (Wolsey 1980), a stronger statement than ALG $\le \tfrac{3}{2} \cdot \text{OPT}$.
- **The circuit matters only a little.** Different Euler circuits give different tours, but each costs at most $c(T) + c(M)$.

## Variants and improvements

- **The best of many circuits.** Try several Euler circuits or several start vertices and keep the best tour. The bound stays 3/2.
- **Local search after.** [2-opt](/two-opt/) or [Lin-Kernighan](/lin-kernighan/) on the tour removes most of the extra cost in practice. The [MST TSP heuristic](/mst-tsp-heuristic/) page compares the choices.
- **A greedy matching.** A greedy matching in line L3 makes the step faster but loses the bound 3/2.
- **The $s$-$t$ path version.** For a path with fixed ends, Hoogeveen (1991) proved 5/3 for the same idea, and later work reached 3/2 for the path version too.
- **Better ratios.** The [Karlin-Klein-Oveis Gharan algorithm](/karlin-klein-oveis-gharan-algorithm/) samples a random spanning tree from the LP solution instead of taking a minimum one, and gets $3/2 - 10^{-36}$ in expectation. For graphic TSP, where the costs are shortest path lengths in an unweighted graph, Sebő and Vygen (2014) got 7/5.
- **Euclidean instances.** For points in the plane, the [Arora PTAS](/arora-euclidean-tsp-ptas/) gets $1 + \varepsilon$ for each fixed $\varepsilon > 0$.

## When to use it

Use Christofides' algorithm when you need the best simple guarantee for metric TSP, or a start tour with a proved bound. Use it as the textbook example of a matching argument and of a lower bound by two halves of OPT. When the quality in practice matters more than the guarantee, use [Lin-Kernighan-Helsgaun](/lin-kernighan-helsgaun/), which gives much better tours on most instances.

## Pitfalls

- **The wrong vertex set in line L2.** The matching must be on the vertices of odd degree in $T$, not on all vertices and not on the leaves only. A vertex of degree 3 is odd and must be matched.
- **A simple graph in line L4.** If an edge of $M$ is also an edge of $T$, as $AD$ is in the example, the multigraph has two copies of it. A program that stores $T + M$ as a set of edges loses one copy, and then two vertices have odd degree and the Euler circuit fails.
- **A matching that is not minimum in line L3.** The proof of $c(M) \le \text{OPT}/2$ needs a minimum matching. A greedy matching can cost much more.
- **Costs that are not metric.** Both the step to $C_O$ and lines L6 to L8 need the triangle inequality. For a graph, use shortest path costs first.

## Implementations

## History

Nicos Christofides described the algorithm in a 1976 report of the Graduate School of Industrial Administration of Carnegie Mellon University. Anatoliy Serdyukov found the same algorithm independently and published it in 1978 in the Russian journal Upravlyaemye Sistemy; van Bevern and Slugina (2020) told this story and translated the paper, and the name Christofides-Serdyukov algorithm is now common. Wolsey (1980) proved the bound with respect to the subtour LP. The ratio 3/2 stayed the best known for metric TSP until Karlin, Klein and Oveis Gharan improved it by a tiny constant in 2020 (STOC 2021).

## References
