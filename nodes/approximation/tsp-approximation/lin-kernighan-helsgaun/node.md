---
tag: 44V9MX
kind: algorithm
slug: lin-kernighan-helsgaun
name: Lin-Kernighan-Helsgaun heuristic
aliases:
- Helsgaun heuristic
- LKH
area: approximation/tsp-approximation
level: research
summary: Lin-Kernighan with 5-opt basic steps and candidate lists from alpha-nearness, a sensitivity measure on minimum 1-trees; its tour quality is measured, not proved.
solves: [metric-tsp]
model: real-ram
complexity:
  vars: {n: the number of cities, r: the number of ascent rounds}
  time: {ascent: O(r n^2), alpha: O(n^2)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 2000
  people: [Keld Helsgaun]
  note: Helsgaun (2000) combined Lin-Kernighan search with 5-opt basic steps and alpha-nearness candidates; LKH-2 (2009) added general k-opt submoves.
prereqs: [lin-kernighan, held-karp-bound, minimum-spanning-tree, local-search]
see_also: [lin-kernighan, held-karp-bound, two-opt, three-opt, iterated-local-search, mst-lower-bound-for-tsp, christofides-algorithm, local-optimum]
sources:
  - paper: doi:10.1016/S0377-2217(99)00284-2
    title: Keld Helsgaun, An effective implementation of the Lin-Kernighan traveling salesman heuristic, European Journal of Operational Research 126(1), 2000
    locator: pages 106 to 130 (alpha-nearness, the subgradient ascent, the 5-opt basic move, and the measured results)
  - paper: doi:10.1007/s12532-009-0004-6
    title: Keld Helsgaun, General k-opt submoves for the Lin-Kernighan TSP heuristic, Mathematical Programming Computation 1(2), 2009
    locator: pages 119 to 163 (k-opt submoves for any k, and the measured results of LKH-2)
  - paper: doi:10.1287/opre.18.6.1138
    title: Michael Held and Richard M. Karp, The traveling-salesman problem and minimum spanning trees, Operations Research 18(6), 1970
    locator: pages 1138 to 1162 (1-trees, the transform by node values, and the lower bound)
---

The Lin-Kernighan-Helsgaun heuristic (LKH) is a version of the [Lin-Kernighan](/lin-kernighan/) local search for the TSP. It changes two parts of LK. First, its candidate lists do not hold the nearest cities but the *alpha-nearest* ones, where $\alpha(i, j)$ is how much a minimum 1-tree gets longer if it must hold the edge $\{i, j\}$. Before that, a subgradient ascent changes the costs by node values $\pi$ so that the 1-tree is close to a tour. Second, each basic step of the search is a sequential 5-opt move, not a 2-opt step. LKH finds optimal or best known tours of very many test instances. All quality claims for it are measured: no ratio is proved.

## In plain words

Plain Lin-Kernighan tries roads to the nearest cities first. But the best tour often uses a road that is not among the five shortest at a city.

LKH first finds a cheap tree that is almost a tour, the 1-tree. It adds a penalty or a bonus to each city until the tree is as close to a tour as it can get.

Then, for each possible road, it asks: if the tree had to use this road, how much longer would the tree be? Roads with a small answer are good candidates. Each city gets its five best candidates.

Then the search runs as in Lin-Kernighan, but with these candidates and with bigger steps. The tree length is also a lower bound, so it tells you how far from the best tour you can be.

## The problem

The input is a set $V$ of $n$ cities with costs $d(u, v) = d(v, u) \ge 0$ and a start tour. The output is a tour on which no search of the method gains. OPT is the least cost of a tour and ALG is the cost of the returned tour. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem. No ratio $\rho$ is proved for LKH. The candidate part also gives a lower bound $w \le$ OPT.

A 1-tree is a spanning tree on all cities but one special city $s$, plus two edges at $s$. Every tour is a 1-tree, so a minimum 1-tree is a lower bound; see the [Held-Karp bound](/held-karp-bound/). With node values $\pi$ the costs are $d_\pi(i, j) = d(i, j) + \pi_i + \pi_j$, and $w(\pi) = L(T_\pi) - 2 \sum_i \pi_i$, where $L(T_\pi)$ is the cost of a minimum 1-tree $T_\pi$ under $d_\pi$.

## The algorithm

```pseudo id=main
LKH(d, T)
L1  π = subgradient ascent on w(π), from π = 0, with steps π_i += t (deg(i) - 2)
L2  α(i, j) = L(minimum 1-tree under π that holds {i, j}) - L(T_π) for all pairs
L3  the candidate list of each city holds its 5 α-nearest cities
L4  repeat
L5      for each city t1 and each tour edge {t1, y}: run a variable-depth search over the candidates
L6      if a search gains then apply the best tour it found
L7  until no search gains; return T
```

On line L2, $\alpha$ is 0 for edges of $T_\pi$. For other edges it is $d_\pi(i, j)$ minus the largest edge on the tree path from $i$ to $j$, or minus the second edge at $s$ when $i = s$. So all values cost $O(n^2)$ time. In LKH the search on line L5 uses sequential 5-opt basic steps. **The code covers lines L1 to L4 in full, but its search uses the 2-opt step of the [Lin-Kernighan](/lin-kernighan/) page, not the 5-opt step.** Its ascent uses a fixed step that shrinks by 5 percent per round, and not the step rule of LKH.

## Example

Take the seven cities of the [3-opt](/three-opt/) page, $A(1,2)$, $B(0,5)$, $C(3,3)$, $D(1,0)$, $E(0,0)$, $F(3,4)$ and $G(2,6)$, with the Euclidean distance. The special city is $A$.

1. **The 1-tree with $\pi = 0$.** The minimum spanning tree on $B, \ldots, G$ has the edges $BG$ and $GF$ (2.236 each), $FC$ (1), $CD$ (3.606) and $DE$ (1). The two cheapest edges at $A$ are $AD$ (2) and $AC$ (2.236). The total is 14.314, below OPT = 15.476. The cities $C$ and $D$ have degree 3, and $B$ and $E$ have degree 1.
2. **Two alpha values.** If the tree must hold $AB$, it replaces $AC$, so $\alpha(A, B) = \sqrt{10} - \sqrt{5} = 0.926$. If it must hold $EC$, it drops the largest edge $CD$ on the tree path $E\,D\,C$, so $\alpha(E, C) = \sqrt{18} - \sqrt{13} = 0.637$.
3. **The ascent.** It lowers $\pi_B$ (to $-0.749$) and raises $\pi_D$ (to $0.423$), among other changes. Then the minimum 1-tree is the tour $A\,E\,D\,C\,F\,G\,B$, and $w = 15.476$. By the theorem below this tour is optimal, and the bound proves it.
4. **The lists.** With lists of 3, the alpha list of $A$ under the final $\pi$ is $E, B, D$. The 3 nearest cities of $A$ are $D, C, E$. The optimal edge $AB$ is in the alpha list but not in the nearest list.

**Measured behavior.** On 300 seeded instances of 10 uniform random points in the unit square, with OPT from the Held-Karp program, the ascent gave $w$ at 99.65 percent of OPT on average, against 85.1 percent for the 1-tree with $\pi = 0$. The 5 alpha-nearest lists held 5989 of the 6000 city ends of optimal tour edges, and the 5 nearest lists held 5615. The average rank of an optimal edge was 1.57 in the alpha lists and 2.29 in the nearest lists. The code found OPT in all 300 cases, with 3.5 improvements on average. On 50 instances of 12 points it found OPT in 49 cases. Helsgaun (2000) reports that 5 alpha-nearest candidates were enough to find optimal tours of many TSPLIB instances, and that LKH beat other LK codes by a wide margin. These are measured values, not bounds.

## Correctness

**Theorem.** For each $\pi$, $w(\pi) \le$ OPT, and if $T_\pi$ is a tour, it is optimal. The degree vector minus 2 is a subgradient of the concave function $w$. The formula for $\alpha$ on line L2 is exact and gives $\alpha \ge 0$. The search stops at a tour on which no search gains.

The proof has three steps.

1. **The bound.** Each tour is a 1-tree, and the transform adds $2 \sum_i \pi_i$ to every tour, so it does not change which tour is best.
2. **Alpha.** Forcing an edge $\{i, j\}$ into a minimum spanning tree costs exactly $d(i, j)$ minus the largest edge on the tree path, by an exchange argument in each direction.
3. **The search.** The steps and the termination proof of the [Lin-Kernighan](/lin-kernighan/) page do not depend on the candidate lists.

The full proof is in the proof file.

**What is not proved.** No worst-case ratio is known for LKH. The claim that alpha lists hold the optimal edges more often than nearest lists is measured. The PLS result of Papadimitriou (1992) for a version of LK suggests that no polynomial bound on the number of improvements holds for such searches.

**Hardness.** No polynomial algorithm has a ratio below $123/122$ for metric TSP unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **Ascent.** Each round builds a minimum 1-tree in $O(n^2)$ time with [Prim's algorithm](/prim/) on the full graph, so $r$ rounds cost $O(r n^2)$.
- **Alpha.** One walk over the tree per city gives all values in $O(n^2)$ time. Helsgaun computes them row by row in $O(n)$ extra space; this code stores the full table.
- **Search.** A 5-opt basic step in LKH tries many combinations of candidates, so one step costs much more than an LK step, but it finds more. In this code a step tests at most 5 candidates, plus the tour update.
- **Large instances.** LKH builds the 1-trees on a sparse graph, for example a [Delaunay triangulation](/delaunay-triangulation/) in the plane, to avoid the $n^2$ terms.

## Properties

- **A lower bound as a by-product.** The best $w$ is a [Held-Karp](/held-karp-bound/) lower bound, so a run can report how far its tour can be from OPT.
- **Order of tours unchanged.** The transform by $\pi$ adds the same constant to every tour, so the search can use $d$ or $d_\pi$.
- **Deep basic steps.** A 5-opt basic step finds improvements that need several bad 2-opt steps in plain LK.
- **No proved ratio.** The method is a heuristic in the strict sense.

## Variants and improvements

- **LKH-2 (2009).** Basic steps of any $k$, non-sequential moves, tour merging and partitioning of large instances.
- **LKH-3.** Extensions to constrained TSPs and vehicle routing problems, reported by Helsgaun in technical reports.
- **Other candidate sets.** Quadrant neighbors and Delaunay neighbors are options in LKH-2.
- **Kicks.** As in chained LK, LKH can restart from a changed tour; see [iterated local search](/iterated-local-search/).

## When to use it

Use LKH when you need the shortest tours you can get for large instances and can accept no guarantee. Its lower bound tells you how good the tour is. For a guarantee use [Christofides](/christofides-algorithm/) on metric costs, and for a proof of optimality use an exact solver.

## Pitfalls

- **Treating the results as bounds.** All quality figures for LKH are measured.
- **A lower bound from a bad ascent.** Every $w(\pi)$ is a lower bound, but a poor step rule gives a weak one. Keep the best $w$, not the last.
- **Forgetting the special city.** The alpha formula for edges at $s$ differs from the formula for the other edges.
- **Searching on $d_\pi$ with negative costs.** The transformed costs can be negative. This is fine for the search, but code that assumes $d \ge 0$ can break.
- **Full alpha tables.** $\Theta(n^2)$ memory is too much for large $n$; compute the lists row by row.

## Implementations

## History

Held and Karp (1970) introduced the 1-tree bound with node values. Helsgaun (2000) defined alpha-nearness for candidate lists, joined it with a 5-opt basic step in a Lin-Kernighan search, and reported large gains over LK. LKH-2 (2009) added general $k$-opt submoves. LKH and its descendants have found the best known tours of many large test instances, as reported by Helsgaun.

## References
