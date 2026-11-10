---
tag: F2HNR2
kind: algorithm
slug: two-opt
name: 2-opt
aliases:
- 2-opt TSP heuristic
- 2-opt local search
area: approximation/tsp-approximation
level: core
summary: Reverses a part of the tour while this makes the tour shorter; each local optimum is within O(√n) of OPT on metric instances, but the search can take exponentially many moves.
solves: [metric-tsp]
model: real-ram
complexity:
  vars: {n: the number of cities}
  time: {worst: 2^Ω(n), pass: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1958
  people: [G. A. Croes, Barun Chandra, Howard Karloff, Craig Tovey, Matthias Englert, Heiko Röglin, Berthold Vöcking]
  note: Croes used the move in 1958; Chandra, Karloff and Tovey (1999) proved the √n bounds; Englert, Röglin and Vöcking (2014) gave exponential runs in the plane and smoothed bounds.
prereqs: [metric-tsp, local-search, neighborhood-structure, local-optimum, triangle-inequality]
see_also: [three-opt, or-opt, lin-kernighan, lin-kernighan-helsgaun, nearest-neighbor-tsp, hill-climbing, iterated-local-search, smoothed-analysis]
sources:
  - paper: doi:10.1287/opre.6.6.791
    title: G. A. Croes, A method for solving traveling-salesman problems, Operations Research 6(6), 1958
    locator: pages 791 to 812 (the inversion move)
  - paper: doi:10.1137/S0097539793251244
    title: Barun Chandra, Howard Karloff and Craig Tovey, New results on the old k-opt algorithm for the traveling salesman problem, SIAM Journal on Computing 28(6), 1999
    locator: pages 1998 to 2029 (the 4√n upper bound, the (1/4)√n lower bound, and the bounds for Euclidean and random instances)
  - paper: doi:10.1016/j.orl.2020.05.007
    title: Stefan Hougardy, Fabian Zaiser and Xianghui Zhong, The approximation ratio of the 2-Opt heuristic for the metric traveling salesman problem, Operations Research Letters 48(4), 2020
    locator: pages 401 to 404 (the exact ratio √(n/2))
  - paper: doi:10.1007/s00453-013-9801-4
    title: Matthias Englert, Heiko Röglin and Berthold Vöcking, Worst case and probabilistic analysis of the 2-Opt algorithm for the TSP, Algorithmica 68(1), 2014
    locator: pages 190 to 264 (exponential runs in the Euclidean plane, smoothed and average bounds)
  - title: David S. Johnson and Lyle A. McGeoch, The traveling salesman problem, a case study in local optimization, in Aarts and Lenstra (eds.), Local Search in Combinatorial Optimization, Wiley, 1997
    locator: Section 3 (2-opt and 3-opt, neighbor lists, don't-look bits, results on random uniform instances)
---

2-opt is the basic [local search](/local-search/) for the [metric TSP](/metric-tsp/). It removes two edges of the tour and puts in the two edges that close the tour again, which reverses the path between them, and it does this while some such move makes the tour shorter. The tour that it returns is a [local optimum](/local-optimum/) for this [neighborhood](/neighborhood-structure/), called a 2-optimal tour. On metric instances each 2-optimal tour is within a factor $O(\sqrt{n})$ of OPT, and this order is tight. In the plane a 2-optimal tour has no crossing edges. The search always stops, but it can take exponentially many moves. In practice it is fast, and its tours are about 5 percent above OPT on large random instances.

## In plain words

Draw the tour on the map. If two roads of the tour cross, the tour is too long: uncross them. You cut both roads, and you join the four loose ends the other way. The part of the trip between the two cuts is now driven in the other direction.

2-opt does this with any pair of roads, crossing or not, when the new pair of roads is shorter than the old pair. It repeats until no pair can be improved.

The result is good but not best. A large number of small repairs cannot always find a change that needs many roads at once. The number of repairs is usually small, but bad cases need very many.

## The problem

The input is a set $V$ of $n$ cities with costs $d(u, v) = d(v, u) \ge 0$ that satisfy the [triangle inequality](/triangle-inequality/), and a start tour. The output is a 2-optimal tour. OPT is the least cost of a tour and ALG is the cost of the returned tour. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem. The bound on this page holds in the worst case for every 2-optimal tour, so it does not depend on the start tour or on the order of the moves.

## The algorithm

Write the tour as an array $T[0], \ldots, T[n-1]$. A move on the positions $i < j$ removes the edges $\{T[i], T[i+1]\}$ and $\{T[j], T[j+1]\}$ and adds $\{T[i], T[j]\}$ and $\{T[i+1], T[j+1]\}$, indices modulo $n$.

```pseudo id=main
TWO-OPT(d, T)
L1  repeat
L2      improved ← false
L3      for i ← 0 to n − 3 do
L4          for j ← i + 2 to n − 1, except j = n − 1 when i = 0, do
L5              if d(T[i], T[i+1]) + d(T[j], T[j+1]) > d(T[i], T[j]) + d(T[i+1], T[j+1]) then
L6                  reverse T[i+1 .. j]; improved ← true
L7  until not improved; return T
```

The test in line L5 uses four costs, so it is $O(1)$. The change of cost and the count $n(n-3)/2$ of the moves of one tour are on the [neighborhood structure](/neighborhood-structure/) page. The implementation takes the first move that gains, in this scan order, and accepts it only if it gains more than $10^{-12}$, so that rounding cannot make it loop.

## Example

Take the six cities $A(0,0)$, $B(2,0)$, $C(5,1)$, $D(4,4)$, $E(1,3)$ and $F(6,3)$ of the [nearest insertion](/nearest-insertion/) page, with the Euclidean distance, and start from the tour $A\,D\,B\,E\,C\,F$, which has crossings and length $26.708$.

| move | removed edges | added edges | gain | tour after the move | length |
|---|---|---|---|---|---|
| 1 | $AD$, $BE$ | $AB$, $DE$ | 3.657 | $A\,B\,D\,E\,C\,F$ | 23.051 |
| 2 | $AB$, $EC$ | $AE$, $BC$ | 0.148 | $A\,E\,D\,B\,C\,F$ | 22.903 |
| 3 | $DB$, $FA$ | $DF$, $BA$ | 6.944 | $A\,E\,D\,F\,C\,B$ | 15.959 |

No move gains on the last tour, and its length 15.959 is OPT.

**Measured behavior.** On 300 seeded instances of 10 uniform random points in the unit square, with OPT from the Held-Karp program, 2-opt from a random tour gave tours 1.05 percent above OPT on average, at most 1.212 times OPT, and the optimum in 203 cases, with 9.8 moves on average. From the [nearest-neighbor tour](/nearest-neighbor-tsp/) it gave 0.68 percent with 2.4 moves. On large random uniform instances, Johnson and McGeoch (1997) report 2-opt tours about 5 percent above the Held-Karp bound, with neighbor lists and a greedy start. These are measured values, not bounds.

## Correctness

The search stops, because each move makes the tour strictly shorter and there are finitely many tours. When it stops, no move gains, so the tour is 2-optimal.

**Theorem.** For metric costs, every 2-optimal tour satisfies

$$\text{ALG} \le 2\sqrt{2} \sum_{i=1}^{n} \frac{1}{\sqrt{i}} \cdot \text{OPT} < 4\sqrt{2}\,\sqrt{n} \cdot \text{OPT}.$$

Chandra, Karloff and Tovey (1999) proved the bound $4\sqrt{n}$. The proof on this page is of the same kind, with a slightly larger constant. It has three steps.

1. **The 2-opt inequality.** Orient the tour. For two tour edges $a \to b$ and $c \to e$, a 2-optimal tour has $d(a, b) + d(c, e) \le d(a, c) + d(b, e)$. So two edges longer than $\Lambda$ cannot have both their tails and their heads within $\Lambda / 2$ of each other.
2. **Few long edges.** Group the tails of the edges longer than $\Lambda$ along a shortcut of an optimal tour, into fewer than $2\,\text{OPT}/\Lambda + 1$ groups of close tails. In each group the heads are far apart, so a group has fewer than $2\,\text{OPT}/\Lambda$ edges. So fewer than $8 (\text{OPT}/\Lambda)^2$ edges are longer than $\Lambda$.
3. **Sum.** The $i$-th longest edge is at most $\sqrt{8/i}\,\text{OPT}$. Add over $i$.

The full proof is in the proof file. It also proves that in the Euclidean plane a 2-optimal tour has no two edges that cross: uncrossing them is a 2-opt move that gains, by the triangle inequality at the crossing point.

**Lower bounds.** Chandra, Karloff and Tovey gave metric instances with 2-optimal tours of ratio $\frac{1}{4}\sqrt{n}$, and Hougardy, Zaiser and Zhong (2020) showed that the exact worst-case ratio is $\sqrt{n/2}$. In the Euclidean plane the ratio is smaller: Chandra, Karloff and Tovey proved $O(\log n)$, and Brodowsky and Hougardy (2021) showed that the order is $\log n / \log \log n$. These results are quoted, not proved, here.

**Running time.** The number of moves can be exponential. Englert, Röglin and Vöcking (2014) gave instances in the Euclidean plane, with a start tour and a choice of improving moves, on which 2-opt makes exponentially many moves. They also proved that the expected number of moves is polynomial when the points are perturbed at random ([smoothed analysis](/smoothed-analysis/)). If only moves that remove a crossing are made, van Leeuwen and Schoone (1981) proved that at most $O(n^3)$ moves are needed in the plane. These are quoted results. The general question of finding a local optimum fast is the subject of the class [PLS](/pls/).

**Hardness.** A local optimum is not a good approximation in the worst case: the $\sqrt{n}$ ratio is much worse than the 3/2 of [Christofides' algorithm](/christofides-algorithm/). No polynomial algorithm has a ratio below $123/122$ for metric TSP unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **One pass.** Lines L3 to L5 test $n(n-3)/2$ moves at $O(1)$ each, so a pass without a move costs $\Theta(n^2)$.
- **One move.** The reversal in line L6 costs $O(n)$ in an array. Reverse the shorter of the two sides, since reversing either side gives the same cycle.
- **Number of moves.** At most the number of different tour lengths, and exponential in the worst case. With integer costs bounded by $W$, at most $nW$ moves, because each move gains at least 1.
- **Space.** $\Theta(n)$ besides the costs.

## Properties

- **Deterministic.** With a fixed scan order and a fixed start tour.
- **Local optimum, any start.** The bound holds for every 2-optimal tour, so it does not depend on the start. The start changes only the time and the tour in practice.
- **No crossings.** In the plane, a 2-optimal tour is a simple polygon when the points are in general position.
- **Contained in larger neighborhoods.** Each [3-opt](/three-opt/) and [Lin-Kernighan](/lin-kernighan/) local optimum is 2-optimal, so the bound holds for them too.
- **Not exact.** A 2-optimal tour need not be optimal. The [local optimum](/local-optimum/) page shows an instance with four 2-optimal tours.

## Variants and improvements

- **Neighbor lists.** Test only the moves where the new edge $\{T[i], T[j]\}$ goes to one of the $k$ nearest cities of $T[i]$. This keeps nearly all good moves and makes a pass close to linear.
- **Don't-look bits.** Skip a city whose neighbors have not changed since its last failed search.
- **Doubly linked or tree tours.** For large $n$, store the tour as a [splay tree](/splay-tree/) or a two-level [doubly linked list](/doubly-linked-list/) so that a reversal costs $O(\sqrt{n})$ or $O(\log n)$ amortized.
- **[Or-opt](/or-opt/) and [3-opt](/three-opt/).** Larger neighborhoods with better tours and more time per pass.
- **[Lin-Kernighan](/lin-kernighan/).** A variable depth chain of 2-opt moves.
- **Metaheuristics.** [Simulated annealing](/simulated-annealing/), [tabu search](/tabu-search/) and [iterated local search](/iterated-local-search/) use 2-opt moves and accept some bad moves to leave local optima.

## When to use it

Use 2-opt to improve a tour from a construction heuristic such as [nearest neighbor](/nearest-neighbor-tsp/) or [greedy](/greedy-edge-heuristic/), when you need a good tour fast and do not need a proved ratio. For better tours use [Or-opt](/or-opt/), [3-opt](/three-opt/) or [Lin-Kernighan](/lin-kernighan/). For a proved ratio use [Christofides' algorithm](/christofides-algorithm/), and then 2-opt on its tour; 2-opt does not make a tour longer.

## Pitfalls

- **The wrong pair of new edges.** For the oriented edges $a \to b$ and $c \to e$, the new edges are $\{a, c\}$ and $\{b, e\}$. The other pair, $\{a, e\}$ and $\{b, c\}$, splits the tour into two cycles.
- **Adjacent edges.** Two edges with a common city give no new tour. The loops in lines L3 and L4 leave them out, including the pair of the last edge and the first edge.
- **Rounding.** With floating-point costs, a move with gain $10^{-16}$ can be undone by another. Accept a move only if the gain is larger than a small $\varepsilon$.
- **Full scans on large inputs.** A full pass is $\Theta(n^2)$. On $10^5$ cities, use neighbor lists and don't-look bits.
- **Quoting the ratio as a constant.** 2-opt has no constant worst-case ratio on metric instances.

## Implementations

## History

Croes (1958) improved tours by inverting parts of them and made this move the base of a solution method; the move is now called 2-opt. Lin (1965) studied the $k$-opt moves, and Lin and Kernighan (1973) built a variable depth search on them. Johnson and McGeoch (1997) measured 2-opt with neighbor lists and don't-look bits on instances with up to $10^6$ cities. Chandra, Karloff and Tovey (1999) proved the $\Theta(\sqrt{n})$ bounds for metric instances, and Hougardy, Zaiser and Zhong (2020) found the exact constant. Englert, Röglin and Vöcking (2014) proved the exponential worst case in the plane and the smoothed bounds.

## References
